"""
d9_test.py — Bölge-içi S3 zamanlama testi (D9).

AWS us-east-1 VM üzerinde çalıştırılır.
Barnard karelerinden 50 tanesini koalesan Range GET ile okur.
p50 ve p95 hesaplar; GPU tetikleyicisi kontrol eder.

Kullanım:
    python -m c_sunucu.ops.d9_test --target barnard --n 50 --seed 42
    python -m c_sunucu.ops.d9_test --target barnard --n 50 --warm

Çıktı formatı (JSON + terminal):
    D9 Zamanlama Testi — barnard (n=50)
    Makine: hostname, bölge: AWS us-east-1 (doğrulanmamış)
    p50: X.XXs  p95: XX.XXs  min: X.XXs  max: XX.XXs
    GPU tetikleyicisi: p50 > 2.0s → HAYIR/EVET
    Sonuç JSON: d9_result_{timestamp}.json

Notlar:
- S3 anonim erişim, kova: nasa-irsa-spherex (us-east-1)
- Barnard kare listesi rastgele --seed ile belirlenir
- Hedef: p50 < 1 s, p95 < 3 s / frame-window [V: s0_B §3]
- Ankara'dan ölçülen değer: p50 3.9 s, p95 12.73 s [V: s0_B §3]
"""
from __future__ import annotations

import argparse
import asyncio
import json
import logging
import pathlib
import platform
import random
import socket
import statistics
import sys
import time
from dataclasses import asdict, dataclass, field

import httpx

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Sabitler
# ---------------------------------------------------------------------------

S3_BASE = "https://nasa-irsa-spherex.s3.amazonaws.com"
S3_BUCKET = "nasa-irsa-spherex"

GPU_TRIGGER_THRESHOLD = 2.0  # saniye; p50 > bu değer → vast.ai GPU tetiklenir

# SPHEREx L2 Barnard kare S3 key ön eki.
# Gerçek yol yapısı s0_B §2'den [V: s0_B].
# Örnek: dr1/level2/2025W34_2B_001_010_0_I01_map_11.fits
BARNARD_S3_PREFIX = "dr1/level2/2025W34_2B_"

# Barnard bölgesindeki kare indeks aralıkları (gerçek SPHEREx L2 kataloğundan [V: s0_B §2])
BARNARD_FRAME_INDICES = list(range(1, 201))  # 001–200 arası kare indeksleri

# SPHEREx L2b detector (I01–I06) listesi — Barnard bölgesinde kullanılanlar
BARNARD_DETECTORS = ["I01", "I02", "I03", "I04", "I05", "I06"]

# Birleştirilmiş 4-HDU Range GET için byte offset'leri (yaklaşık, [ASSUMPTION: s0_B])
# Gerçek değerler: astropy ile başlık taranarak ByteOffsetMap'e alınmalı.
# Burada FITS standart blok boyutu ve L2b dosya düzenine göre tahmin edilmiş.
# PRIMARY HDU: ~2880 byte header
# IMAGE HDU 1: data_start ≈ 5760 (2×2880 header blokları)
# FLAGS HDU 2: IMAGE data (2040×2040×4 bytes) = 16,646,400 bytes → veri bitişi ~16652160
# VARIANCE HDU 3: FLAGS'den sonra benzer büyüklük
# ZODI HDU 4: VARIANCE'dan sonra
HDU_OFFSETS = {
    "IMAGE":    (5_760,                                 5_760 + 16_646_400),
    "FLAGS":    (5_760 + 16_646_400 + 2_880,            5_760 + 16_646_400 + 2_880 + 16_646_400),
    "VARIANCE": (5_760 + 2 * (16_646_400 + 2_880),      5_760 + 2 * (16_646_400 + 2_880) + 16_646_400),
    "ZODI":     (5_760 + 3 * (16_646_400 + 2_880),      5_760 + 3 * (16_646_400 + 2_880) + 16_646_400),
}

# Warm istek için ön ısıtma kare sayısı
WARMUP_FRAMES = 3

# HTTP zaman aşımı (saniye)
HTTP_TIMEOUT = 60.0

# 100×100 piksel pencere için alınan satır sayısı (y0=970, y1=1070)
DEFAULT_WINDOW_Y0 = 970
DEFAULT_WINDOW_Y1 = 1070

# ---------------------------------------------------------------------------
# Veri sınıfları
# ---------------------------------------------------------------------------


@dataclass
class D9Result:
    """D9 zamanlama testi sonucu."""

    target: str
    """Test hedefi adı (örn. 'barnard')."""

    n: int
    """Ölçülen kare sayısı."""

    warm: bool
    """True ise ön ısıtma yapıldı."""

    p50: float
    """Medyan kare süresi (saniye)."""

    p95: float
    """95. yüzdelik kare süresi (saniye)."""

    p_min: float
    """Minimum kare süresi (saniye)."""

    p_max: float
    """Maksimum kare süresi (saniye)."""

    gpu_trigger: bool
    """True ise p50 > GPU_TRIGGER_THRESHOLD (vast.ai tetikleyicisi)."""

    times: list[float]
    """Her kare için ölçülen süre listesi (saniye)."""

    hostname: str
    """Test makinesinin hostname'i."""

    timestamp: str
    """ISO 8601 zaman damgası (UTC)."""

    frames_tested: list[str] = field(default_factory=list)
    """Test edilen S3 key listesi."""

    errors: list[str] = field(default_factory=list)
    """Hatalı kareler ve hata mesajları."""

    def to_json_file(self, out_dir: pathlib.Path) -> pathlib.Path:
        """
        Sonucu JSON dosyasına yazar.

        Parameters
        ----------
        out_dir:
            Çıktı dizini; yoksa oluşturulur.

        Returns
        -------
        pathlib.Path
            Yazılan dosyanın yolu.
        """
        out_dir.mkdir(parents=True, exist_ok=True)
        # Zaman damgasındaki ':' karakterleri dosya adında sorun çıkarır
        safe_ts = self.timestamp.replace(":", "").replace("-", "").replace("T", "_")
        fname = out_dir / f"d9_result_{safe_ts}.json"
        payload = asdict(self)
        fname.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        return fname


# ---------------------------------------------------------------------------
# S3 key oluşturma
# ---------------------------------------------------------------------------


def _build_barnard_keys(n: int, seed: int) -> list[str]:
    """
    Rastgele n adet Barnard kare S3 key'i oluşturur.

    Key biçimi: dr1/level2/2025W34_2B_{idx:03d}_{det}_map_11.fits
    Örnek: dr1/level2/2025W34_2B_042_I03_map_11.fits

    Parameters
    ----------
    n:
        Seçilecek kare sayısı.
    seed:
        Rastgelelik tohumu (tekrarlanabilirlik için).

    Returns
    -------
    list[str]
        S3 key listesi (n öğe).

    Notlar
    ------
    Gerçek kare listesi SPHEREx IRSA kataloğundan TAP sorgusuyla alınmalıdır.
    Bu işlev, test amacıyla bir kare uzayı oluşturur [ASSUMPTION].
    """
    rng = random.Random(seed)
    all_combos = [
        f"{BARNARD_S3_PREFIX}{idx:03d}_{det}_map_11.fits"
        for idx in BARNARD_FRAME_INDICES
        for det in BARNARD_DETECTORS
    ]
    # Yeterince çeşitlilik sağlamak için karıştır ve seç
    rng.shuffle(all_combos)
    return all_combos[:n]


# ---------------------------------------------------------------------------
# Tek kare Range GET (4 HDU paralel)
# ---------------------------------------------------------------------------


async def fetch_one_window(
    s3_key: str,
    *,
    client: httpx.AsyncClient,
    warm: bool = False,
) -> float:
    """
    Tek kare için 4 HDU paralel Range GET; süreyi döner.

    IMAGE, FLAGS, VARIANCE, ZODI HDU'larını asyncio.gather ile
    aynı anda indirir. Yalnızca indirilen bayt sayısını doğrular;
    FITS ayrıştırması yapılmaz.

    Parameters
    ----------
    s3_key:
        S3 nesne anahtarı (kova adı hariç).
    client:
        Paylaşılan httpx.AsyncClient örneği.
    warm:
        True ise başarısız istek sayılmaz (ön ısıtma modu).

    Returns
    -------
    float
        Toplam süre (saniye); 4 HDU isteğinin toplam duvar-saati süresi.

    Raises
    ------
    httpx.HTTPError
        HTTP isteği başarısız olduğunda.
    """
    url = f"{S3_BASE}/{s3_key}"

    async def _get_range(hdu_name: str) -> tuple[str, int, float]:
        """Tek HDU için Range GET; (hdu_name, bytes_read, duration_s) döner."""
        start, end = HDU_OFFSETS[hdu_name]
        # end dahil değil → Range: bytes=start-(end-1)
        headers = {"Range": f"bytes={start}-{end - 1}"}
        t0 = time.perf_counter()
        try:
            resp = await client.get(url, headers=headers)
        except httpx.RequestError as exc:
            logger.warning("Range GET hata [%s] %s: %s", hdu_name, s3_key, exc)
            raise
        elapsed = time.perf_counter() - t0

        if resp.status_code not in (200, 206):
            logger.warning(
                "Beklenmedik HTTP %d [%s] %s",
                resp.status_code,
                hdu_name,
                s3_key,
            )
            # 404 vb. durumda da süreyi kaydet; hata caller'a yansıtılacak
            resp.raise_for_status()

        bytes_read = len(resp.content)
        logger.debug(
            "HDU [%s] %s — %d byte, %.3f s",
            hdu_name,
            s3_key,
            bytes_read,
            elapsed,
        )
        return hdu_name, bytes_read, elapsed

    # 4 HDU paralel — duvar saati toplamı (en uzun HDU'ya göre)
    t_wall_start = time.perf_counter()
    await asyncio.gather(
        _get_range("IMAGE"),
        _get_range("FLAGS"),
        _get_range("VARIANCE"),
        _get_range("ZODI"),
    )
    return time.perf_counter() - t_wall_start


# ---------------------------------------------------------------------------
# Ana test koşucusu
# ---------------------------------------------------------------------------


async def run_d9(
    target: str,
    n: int,
    seed: int,
    warm: bool,
    out_dir: pathlib.Path,
) -> D9Result:
    """
    n kare test; p50/p95 hesaplar.

    Parameters
    ----------
    target:
        Test hedefi ('barnard' destekleniyor).
    n:
        Kaç kare ölçüleceği.
    seed:
        Rastgele kare seçimi için tohum.
    warm:
        True ise WARMUP_FRAMES adet ön ısıtma isteği yapılır.
    out_dir:
        JSON çıktı dizini.

    Returns
    -------
    D9Result
        Tüm istatistikler ve metadata içeren sonuç nesnesi.
    """
    if target != "barnard":
        raise ValueError(f"Desteklenmeyen hedef: '{target}'. Geçerli değer: 'barnard'")

    keys = _build_barnard_keys(n + WARMUP_FRAMES if warm else n, seed=seed)

    hostname = _get_hostname()
    timestamp = _utc_iso_now()

    times: list[float] = []
    frames_tested: list[str] = []
    errors: list[str] = []

    async with httpx.AsyncClient(
        timeout=HTTP_TIMEOUT,
        follow_redirects=True,
        limits=httpx.Limits(max_connections=8, max_keepalive_connections=8),
    ) as client:
        # Ön ısıtma (isteğe bağlı)
        if warm:
            warmup_keys = keys[:WARMUP_FRAMES]
            test_keys = keys[WARMUP_FRAMES:]
            print(f"Ön ısıtma: {len(warmup_keys)} kare...", flush=True)
            for wkey in warmup_keys:
                try:
                    await fetch_one_window(wkey, client=client, warm=True)
                except Exception as exc:  # noqa: BLE001
                    logger.debug("Ön ısıtma hatası %s: %s", wkey, exc)
        else:
            test_keys = keys[:n]

        # Ana ölçüm
        print(f"Ölçüm: {len(test_keys)} kare...", flush=True)
        for i, key in enumerate(test_keys):
            try:
                elapsed = await fetch_one_window(key, client=client)
                times.append(elapsed)
                frames_tested.append(key)
                print(
                    f"  [{i + 1:>3}/{len(test_keys)}] {key.split('/')[-1]:<45} {elapsed:.3f}s",
                    flush=True,
                )
            except Exception as exc:  # noqa: BLE001
                err_msg = f"{key}: {exc}"
                errors.append(err_msg)
                logger.error("Kare hatası: %s", err_msg)
                print(f"  [{i + 1:>3}/{len(test_keys)}] HATA — {err_msg}", flush=True)

    if not times:
        raise RuntimeError("Hiçbir kare başarılı şekilde ölçülmedi; sonuç hesaplanamıyor.")

    p50, p95 = _percentiles(times)
    p_min = min(times)
    p_max = max(times)
    gpu_trigger = p50 > GPU_TRIGGER_THRESHOLD

    return D9Result(
        target=target,
        n=len(times),
        warm=warm,
        p50=round(p50, 4),
        p95=round(p95, 4),
        p_min=round(p_min, 4),
        p_max=round(p_max, 4),
        gpu_trigger=gpu_trigger,
        times=[round(t, 4) for t in times],
        hostname=hostname,
        timestamp=timestamp,
        frames_tested=frames_tested,
        errors=errors,
    )


# ---------------------------------------------------------------------------
# İstatistik yardımcıları
# ---------------------------------------------------------------------------


def _percentiles(values: list[float]) -> tuple[float, float]:
    """
    p50 ve p95 hesaplar.

    statistics.quantiles kullanır (n ≥ 2 gerektirir).
    Tek değer listesi için değerin kendisini döner.

    Parameters
    ----------
    values:
        Pozitif reel sayı listesi (süre, saniye).

    Returns
    -------
    tuple[float, float]
        (p50, p95).
    """
    if len(values) == 1:
        return values[0], values[0]

    # statistics.quantiles n=20 → 5% adımlı kesimler; indeks 9 = p50, 18 = p95
    quantiles_20 = statistics.quantiles(values, n=20)
    p50 = quantiles_20[9]   # 10/20 = 50. yüzdelik
    p95 = quantiles_20[18]  # 19/20 = 95. yüzdelik
    return p50, p95


# ---------------------------------------------------------------------------
# Çıktı biçimlendirme
# ---------------------------------------------------------------------------


def _print_summary(result: D9Result, json_path: pathlib.Path) -> None:
    """
    Test özetini terminale basar.

    Parameters
    ----------
    result:
        D9Result nesnesi.
    json_path:
        Yazılan JSON dosyasının yolu.
    """
    gpu_str = "EVET" if result.gpu_trigger else "HAYIR"
    warmup_str = "(warm)" if result.warm else ""
    errors_str = f"  Hatalar: {len(result.errors)}" if result.errors else ""

    print()
    print("=" * 60)
    print(f"D9 Zamanlama Testi — {result.target} (n={result.n}) {warmup_str}")
    print(f"Makine: {result.hostname}, bölge: AWS us-east-1 (doğrulanmamış)")
    print("-" * 60)
    print(f"p50: {result.p50:.3f}s  p95: {result.p95:.3f}s")
    print(f"min: {result.p_min:.3f}s  max: {result.p_max:.3f}s")
    print(f"GPU tetikleyicisi: p50 > {GPU_TRIGGER_THRESHOLD:.1f}s → {gpu_str}")
    if errors_str:
        print(errors_str)
    print("-" * 60)
    # Hedef karşılaştırması
    p50_ok = "✓" if result.p50 < 1.0 else "✗"
    p95_ok = "✓" if result.p95 < 3.0 else "✗"
    print(f"Hedef p50 < 1.0s: {p50_ok}  ({result.p50:.3f}s)")
    print(f"Hedef p95 < 3.0s: {p95_ok}  ({result.p95:.3f}s)")
    print("=" * 60)
    print(f"Sonuç JSON: {json_path}")
    print()


# ---------------------------------------------------------------------------
# Küçük yardımcılar
# ---------------------------------------------------------------------------


def _get_hostname() -> str:
    """Makine hostname'ini döner; hata durumunda 'unknown' döner."""
    try:
        return socket.gethostname()
    except Exception:  # noqa: BLE001
        return "unknown"


def _utc_iso_now() -> str:
    """Şu anki UTC zamanını ISO 8601 biçiminde döner."""
    import datetime

    return datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# CLI giriş noktası
# ---------------------------------------------------------------------------


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """
    Komut satırı argümanlarını ayrıştırır.

    Returns
    -------
    argparse.Namespace
        target, n, seed, warm, out_dir alanları.
    """
    parser = argparse.ArgumentParser(
        prog="d9_test",
        description=(
            "D9 Zamanlama Testi — AWS us-east-1 bölge-içi S3 getirme süresi.\n"
            "Barnard karelerinden n tanesini 4-HDU paralel Range GET ile ölçer."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--target",
        default="barnard",
        choices=["barnard"],
        help="Test hedefi (varsayılan: barnard)",
    )
    parser.add_argument(
        "--n",
        type=int,
        default=50,
        metavar="N",
        help="Ölçülecek kare sayısı (varsayılan: 50)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Rastgele kare seçimi tohumu (varsayılan: 42)",
    )
    parser.add_argument(
        "--warm",
        action="store_true",
        default=False,
        help=f"Ön ısıtma: ölçümden önce {WARMUP_FRAMES} kare indir",
    )
    parser.add_argument(
        "--out-dir",
        type=pathlib.Path,
        default=pathlib.Path("."),
        help="JSON çıktı dizini (varsayılan: çalışma dizini)",
    )
    parser.add_argument(
        "--log-level",
        default="WARNING",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Log seviyesi (varsayılan: WARNING)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """
    CLI ana işlevi.

    Returns
    -------
    int
        Çıkış kodu: 0 = başarılı, 1 = hata.
    """
    args = _parse_args(argv)

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        stream=sys.stderr,
    )

    print(f"D9 Zamanlama Testi başlıyor — hedef={args.target} n={args.n} seed={args.seed}", flush=True)
    print(f"Makine: {_get_hostname()} | Python {platform.python_version()} | {platform.system()}", flush=True)
    print(f"S3 kova: {S3_BUCKET} (us-east-1, anonim erişim)", flush=True)
    print()

    try:
        result = asyncio.run(
            run_d9(
                target=args.target,
                n=args.n,
                seed=args.seed,
                warm=args.warm,
                out_dir=args.out_dir,
            )
        )
    except RuntimeError as exc:
        print(f"HATA: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nTest kullanıcı tarafından durduruldu.", file=sys.stderr)
        return 1

    json_path = result.to_json_file(args.out_dir)
    _print_summary(result, json_path)

    # GPU tetikleyicisi aktifse çıkış kodu 2 (ops scriptleri için)
    return 2 if result.gpu_trigger else 0


if __name__ == "__main__":
    sys.exit(main())
