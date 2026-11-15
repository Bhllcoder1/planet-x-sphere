"""
speed_test.py — Sunucu hız testi (Görev 07-10 / D9).

Barnard karelerinden rastgele 50 seçerek koalesan S3 okuması yapar.
p50 ve p95'i hesaplar; GPU tetikleyicisini kontrol eder.

Akış
----
1. Kare listesi: L0 önbellekten veya yerleşik Barnard anahtar üreticisinden.
2. Rastgele n kare seç (tekrarlanabilir seed).
3. Her kare için:
   - warm=False: önce 64 KB başlık Range GET (offset keşfi), ardından 4 HDU.
   - warm=True:  bilinen offsetlerle doğrudan 4 HDU Range GET.
   - 4 HDU (IMAGE/FLAGS/VARIANCE/ZODI) asyncio.gather() ile paralel.
4. p50 / p95 hesapla; GPU tetikleyicisi: p50 > 2.0 s.

Kullanım
--------
    python -m c_sunucu.ops.speed_test --target barnard --n 50
    python -m c_sunucu.ops.speed_test --target barnard --n 50 --warm
    python -m c_sunucu.ops.speed_test --target barnard --n 50 --cache-dir /cache

Çıktı
-----
    D9 Hız Testi — barnard (50 kare, soğuk)
    p50: 0.72s  p95: 1.84s  min: 0.41s  max: 2.31s
    GPU tetikleyicisi (p50 > 2.0 s): HAYIR
"""
from __future__ import annotations

import argparse
import asyncio
import logging
import pathlib
import random
import statistics
import time
from typing import Any

import httpx

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Sabitler
# ---------------------------------------------------------------------------

S3_BASE = "https://nasa-irsa-spherex.s3.amazonaws.com"
# Anonim erişim — kimlik bilgisi yok; us-east-1 kovası

# Dedektör geometrisi
NAXIS1 = 2040           # Piksel başına sütun (IMAGE/FLAGS/VARIANCE/ZODI)
BYTES_PER_PIXEL = 4     # float32 → 4 byte; int32 → 4 byte
ROW_STRIDE = NAXIS1 * BYTES_PER_PIXEL   # 8,160 bytes/satır

# Test penceresi (dedektör ortası, 100 × 100 piksel)
WINDOW_Y0 = 970
WINDOW_Y1 = 1070        # hariç; 100 satır

# GPU tetikleyici eşiği [PLAN v3]
GPU_TRIGGER_P50_S: float = 2.0

# Eşzamanlı S3 bağlantı limiti (kare başına)
MAX_CONCURRENT_HDU = 4

# Soğuk okuma için başlık Range GET boyutu (64 KB)
HEADER_RANGE_BYTES = 65_535

# Barnard varsayılan HDU veri başlangıç offsetleri [ASSUMPTION]
# Gerçek değerler L1 önbellekten alınmalı; bunlar s3_reader.py demo sabitlerinden
# türetilmiş temsili tahminlerdir — hız ölçümü için yeterli doğruluktadır.
# Kaynak: c_sunucu/api/s3_reader.py demo (ByteOffsetMap bölümü)
_IMAGE_DATA_START    = 2_880 * 10                           #  28,800
_FLAGS_DATA_START    = _IMAGE_DATA_START + 16_646_400       # 16,675,200
_VARIANCE_DATA_START = _IMAGE_DATA_START + 33_292_800       # 33,321,600
_ZODI_DATA_START     = _IMAGE_DATA_START + 49_939_200       # 49,968,000

# HDU adları (paralel GET sırası sabit tutulur)
_HDU_NAMES = ("IMAGE", "FLAGS", "VARIANCE", "ZODI")
_DEFAULT_OFFSETS: dict[str, int] = {
    "IMAGE":    _IMAGE_DATA_START,
    "FLAGS":    _FLAGS_DATA_START,
    "VARIANCE": _VARIANCE_DATA_START,
    "ZODI":     _ZODI_DATA_START,
}

# ---------------------------------------------------------------------------
# Barnard S3 anahtar üreticisi
# ---------------------------------------------------------------------------


def barnard_s3_keys() -> list[str]:
    """
    358 Barnard karesi için S3 nesne anahtarı listesi üretir.

    SPHEREx L2b dosya adlandırma kuralı:
        cal/v01/barnard/spx_barnard_D{d}_p{p}_{seq:04d}_cal.fits

    Üretim: 3 geçiş (p0/p1/p2) × 6 dedektör (D1..D6) × 20 kare/çift = 360,
    son 2 eleman kırpılarak 358 kare döner.

    Returns:
        358 elemanlı S3 anahtar listesi.
    """
    keys: list[str] = []
    for pass_idx in range(3):       # geçiş: 0, 1, 2
        for det in range(1, 7):     # dedektör: 1 .. 6
            for seq in range(20):   # sıra: 0000 .. 0019
                keys.append(
                    f"cal/v01/barnard/"
                    f"spx_barnard_D{det}_p{pass_idx}_{seq:04d}_cal.fits"
                )
    return keys[:358]   # 360 → 358 kırpma


def _target_s3_keys(target_id: str) -> list[str]:
    """
    Verilen hedef için yerleşik S3 anahtar listesini döndürür.

    Şu an yalnızca 'barnard' desteklenir. Diğer hedefler için
    ``cache_dir`` parametresi ile L0 önbelleği sağlayın.

    Args:
        target_id: Hedef kimliği (örn. 'barnard').

    Returns:
        S3 anahtar listesi.

    Raises:
        ValueError: Desteklenmeyen hedef ve önbellek yoksa.
    """
    if target_id == "barnard":
        return barnard_s3_keys()
    raise ValueError(
        f"Hedef {target_id!r} için yerleşik anahtar üreteci yok; "
        "--cache-dir ile L0 önbelleği sağlayın."
    )


# ---------------------------------------------------------------------------
# Önbellek yardımcıları
# ---------------------------------------------------------------------------


async def _load_keys_from_cache(
    target_id: str,
    cache_dir: pathlib.Path,
) -> list[str] | None:
    """
    L0 önbellekten kare S3 anahtar listesini yükler.

    ``cache_dir/l0/{target_id}/frames.json`` yolunu dener.
    Yüklenemezse None döner (hata fırlatmaz).

    Args:
        target_id: Hedef kimliği.
        cache_dir: Önbellek kök dizini.

    Returns:
        S3 anahtar listesi; önbellek eksik veya okunamıyorsa None.
    """
    l0_dir = cache_dir / "l0"
    try:
        from c_sunucu.cache import load_frames  # type: ignore[import]

        frames = await load_frames(target_id, l0_dir)
        keys = [f.s3_key for f in frames if f.s3_key]
        logger.debug(
            "L0 önbellekten %d anahtar yüklendi (hedef=%r, dizin=%s)",
            len(keys), target_id, l0_dir,
        )
        return keys or None
    except Exception as exc:
        logger.debug("L0 önbellek yüklenemedi (%r): %s", target_id, exc)
        return None


async def _load_offsets_from_cache(
    s3_key: str,
    cache_dir: pathlib.Path,
) -> dict[str, int] | None:
    """
    L1 önbellekten HDU byte-offset haritasını yükler.

    ``cache_dir/l1/{frame_stem}.json`` yolunu dener.
    Yüklenemezse None döner (hata fırlatmaz).

    Args:
        s3_key: S3 nesne anahtarı.
        cache_dir: Önbellek kök dizini.

    Returns:
        {hdu_name: data_start} sözlüğü; önbellek eksikse None.
    """
    frame_id = pathlib.Path(s3_key).stem  # örn. 'spx_barnard_D1_p0_0000_cal'
    l1_dir = cache_dir / "l1"
    try:
        from c_sunucu.cache import load_offset_map  # type: ignore[import]

        omap = await load_offset_map(frame_id, l1_dir)
        offsets = {h.name: h.data_start for h in omap.hdus}
        logger.debug("L1 offsetleri yüklendi: frame_id=%r", frame_id)
        return offsets or None
    except Exception as exc:
        logger.debug("L1 önbellek yüklenemedi (%r): %s", frame_id, exc)
        return None


# ---------------------------------------------------------------------------
# Tek HDU Range GET
# ---------------------------------------------------------------------------


async def _fetch_hdu_range(
    s3_key: str,
    data_start: int,
    y0: int,
    y1: int,
    hdu_name: str,
    *,
    client: httpx.AsyncClient,
    sem: asyncio.Semaphore,
) -> int:
    """
    Tek bir HDU için koalesan satır aralığı Range GET yapar.

    ``[y0, y1)`` satır aralığına karşılık gelen tek bir HTTP Range isteği
    gönderir; tam satır sınırlarına hizalıdır.

    Args:
        s3_key: S3 nesne anahtarı (kova adı hariç).
        data_start: HDU ham verisinin S3 nesnesi içindeki başlangıç byte offseti.
        y0: Başlangıç satırı (dahil, 0-tabanlı).
        y1: Bitiş satırı (hariç, 0-tabanlı).
        hdu_name: Log mesajı için HDU adı.
        client: Paylaşılan httpx.AsyncClient örneği.
        sem: Eşzamanlılık sınırı için asyncio.Semaphore.

    Returns:
        Alınan bayt sayısı.

    Raises:
        httpx.HTTPStatusError: HTTP 4xx / 5xx yanıtı alındığında.
        httpx.RequestError: TCP bağlantı veya zaman aşımı hatası.
    """
    byte_start = data_start + y0 * ROW_STRIDE
    byte_end   = data_start + y1 * ROW_STRIDE - 1  # Range dahil son bayt

    url     = f"{S3_BASE}/{s3_key}"
    headers = {"Range": f"bytes={byte_start}-{byte_end}"}

    async with sem:
        try:
            response = await client.get(url, headers=headers)
        except httpx.RequestError as exc:
            raise httpx.RequestError(
                f"S3 bağlantı hatası [{hdu_name}] {s3_key}: {exc}"
            ) from exc

    if response.status_code not in (200, 206):
        raise httpx.HTTPStatusError(
            f"S3 HTTP {response.status_code} [{hdu_name}] {s3_key}",
            request=response.request,
            response=response,
        )

    n_bytes = len(response.content)
    logger.debug(
        "Range GET [%s] %s bytes=%d-%d → HTTP %d (%d bytes)",
        hdu_name, s3_key, byte_start, byte_end,
        response.status_code, n_bytes,
    )
    return n_bytes


# ---------------------------------------------------------------------------
# Tek kare testi
# ---------------------------------------------------------------------------


async def fetch_one_frame(
    s3_key: str,
    *,
    warm: bool,
    offsets: dict[str, int] | None = None,
    client: httpx.AsyncClient | None = None,
) -> float:
    """
    Tek bir kare için 4 HDU paralel Range GET yapar.

    warm=True:  Önceden bilinen offset değerleri ile veri çekilir
                (L1 önbellek ısınmış senaryosu). Yalnızca 4 HDU Range GET.
    warm=False: Önce 64 KB başlık bölgesi okunur (offset keşfi benzetimi),
                ardından 4 HDU Range GET yapılır (soğuk okuma senaryosu).

    4 HDU isteği asyncio.gather() ile eşzamanlı gönderilir.

    Args:
        s3_key: S3 nesne anahtarı (kova adı hariç).
        warm: True ise ısınmış, False ise soğuk okuma senaryosu.
        offsets: {hdu_name: data_start} sözlüğü; None ise varsayılan kullanılır.
        client: Paylaşılan httpx.AsyncClient; None ise yeni örnek oluşturulur.

    Returns:
        Toplam geçen süre (saniye cinsinden float).

    Raises:
        httpx.HTTPStatusError: HTTP 404 / 403 / 503 vb.
        httpx.RequestError: TCP bağlantı veya zaman aşımı hatası.
    """
    if offsets is None:
        offsets = _DEFAULT_OFFSETS

    sem = asyncio.Semaphore(MAX_CONCURRENT_HDU)
    t0 = time.perf_counter()

    _owns_client = client is None
    if _owns_client:
        client = httpx.AsyncClient(
            timeout=httpx.Timeout(60.0, connect=10.0),
            follow_redirects=True,
            http2=False,
        )

    try:
        # --- Soğuk okuma: başlık bölgesini getir (offset keşfi benzetimi) ---
        if not warm:
            url = f"{S3_BASE}/{s3_key}"
            async with sem:
                hdr_resp = await client.get(
                    url,
                    headers={"Range": f"bytes=0-{HEADER_RANGE_BYTES}"},
                )
            if hdr_resp.status_code == 404:
                raise httpx.HTTPStatusError(
                    f"S3 404 (kare bulunamadı): {s3_key}",
                    request=hdr_resp.request,
                    response=hdr_resp,
                )
            if hdr_resp.status_code not in (200, 206):
                raise httpx.HTTPStatusError(
                    f"S3 başlık GET HTTP {hdr_resp.status_code}: {s3_key}",
                    request=hdr_resp.request,
                    response=hdr_resp,
                )
            logger.debug(
                "Başlık Range GET %s → HTTP %d (%d bytes)",
                s3_key, hdr_resp.status_code, len(hdr_resp.content),
            )

        # --- 4 HDU eşzamanlı Range GET ---
        await asyncio.gather(
            _fetch_hdu_range(
                s3_key, offsets["IMAGE"],
                WINDOW_Y0, WINDOW_Y1, "IMAGE",
                client=client, sem=sem,
            ),
            _fetch_hdu_range(
                s3_key, offsets["FLAGS"],
                WINDOW_Y0, WINDOW_Y1, "FLAGS",
                client=client, sem=sem,
            ),
            _fetch_hdu_range(
                s3_key, offsets["VARIANCE"],
                WINDOW_Y0, WINDOW_Y1, "VARIANCE",
                client=client, sem=sem,
            ),
            _fetch_hdu_range(
                s3_key, offsets["ZODI"],
                WINDOW_Y0, WINDOW_Y1, "ZODI",
                client=client, sem=sem,
            ),
        )
    finally:
        if _owns_client:
            await client.aclose()

    return time.perf_counter() - t0


# ---------------------------------------------------------------------------
# İstatistik yardımcıları
# ---------------------------------------------------------------------------


def _percentile(sorted_times: list[float], p: float) -> float:
    """
    Sıralı listede p. yüzdeliği lineer enterpolasyon ile hesaplar.

    ``statistics.quantiles`` kullanılabilir ama bu fonksiyon
    n=1 gibi uç durumlarda da güvenli çalışır.

    Args:
        sorted_times: Küçükten büyüğe sıralı süre listesi.
        p: Yüzdelik (0.0 .. 100.0 arası).

    Returns:
        Enterpolasyon sonucu float değer.
    """
    n = len(sorted_times)
    if n == 0:
        return 0.0
    if n == 1:
        return sorted_times[0]
    index = (p / 100.0) * (n - 1)
    lower = int(index)
    upper = min(lower + 1, n - 1)
    frac  = index - lower
    return sorted_times[lower] * (1.0 - frac) + sorted_times[upper] * frac


def _compute_stats(times: list[float]) -> dict[str, float]:
    """
    Süre listesinden p50, p95, min, max istatistiklerini hesaplar.

    ``statistics.quantiles(data, n=100)`` ≥ 2 veri noktası gerektirir;
    ``_percentile`` ise tüm durumlarda güvenlidir.

    Args:
        times: Kare başına ölçülen süreler (saniye).

    Returns:
        {p50, p95, min, max} sözlüğü; times boşsa tümü 0.0.
    """
    if not times:
        return {"p50": 0.0, "p95": 0.0, "min": 0.0, "max": 0.0}

    sorted_times = sorted(times)

    if len(times) >= 20:
        # statistics.quantiles daha doğru enterpolasyon sağlar
        quants = statistics.quantiles(times, n=100)
        p50 = quants[49]   # 50. yüzdelik (0-tabanlı dizin 49)
        p95 = quants[94]   # 95. yüzdelik (0-tabanlı dizin 94)
    else:
        p50 = _percentile(sorted_times, 50.0)
        p95 = _percentile(sorted_times, 95.0)

    return {
        "p50": p50,
        "p95": p95,
        "min": sorted_times[0],
        "max": sorted_times[-1],
    }


# ---------------------------------------------------------------------------
# Ana test koşucusu
# ---------------------------------------------------------------------------


async def run_test(
    target_id: str,
    n: int = 50,
    warm: bool = False,
    cache_dir: pathlib.Path | None = None,
) -> dict[str, Any]:
    """
    n kare için D9 testini çalıştırır.

    Kareler SIRAYLA işlenir (paralel değil); kare başına 4 HDU isteği
    asyncio.gather() ile paralel gönderilir. Tek bir httpx.AsyncClient
    tüm kareler boyunca yeniden kullanılır (TCP bağlantısı korunur).

    Args:
        target_id: Hedef kimliği (örn. 'barnard').
        n: Test edilecek kare sayısı.
        warm: True ise ısınmış (L1 önbellek / tahmin offsetleri);
              False ise soğuk okuma (başlık keşif aşaması dahil).
        cache_dir: Önbellek kök dizini (isteğe bağlı).
                   Alt dizin yapısı: ``l0/{target}/frames.json``,
                   ``l1/{frame_id}.json``.

    Returns:
        Sonuç sözlüğü::

            {
                "target":     str,     # hedef kimliği
                "n_requested": int,    # istenen kare sayısı
                "n_measured":  int,    # başarıyla ölçülen kare sayısı
                "n_errors":    int,    # atlanan kare sayısı
                "warm":       bool,
                "p50":        float,   # 50. yüzdelik (saniye)
                "p95":        float,   # 95. yüzdelik (saniye)
                "min":        float,
                "max":        float,
                "gpu_trigger": bool,   # p50 > 2.0 s ise True
                "times":      list[float],
                "errors":     list[str],
            }
    """
    # --- Kare anahtar listesini yükle ---
    all_keys: list[str] = []

    if cache_dir is not None:
        maybe_keys = await _load_keys_from_cache(target_id, cache_dir)
        if maybe_keys:
            all_keys = maybe_keys

    if not all_keys:
        try:
            all_keys = _target_s3_keys(target_id)
            logger.info(
                "Yerleşik anahtar üreticisi kullanılıyor: hedef=%r, %d anahtar",
                target_id, len(all_keys),
            )
        except ValueError as exc:
            raise ValueError(
                f"Kare listesi bulunamadı: {exc}. "
                "Önce TAP sorgusu çalıştırın veya --cache-dir belirtin."
            ) from exc

    # --- Rastgele n kare seç ---
    rng = random.Random(42)     # tekrarlanabilir seçim
    n_avail = len(all_keys)
    selected = rng.sample(all_keys, min(n, n_avail))

    if len(selected) < n:
        logger.warning(
            "İstenen %d kare için yalnızca %d anahtar mevcut; %d kare test edilecek",
            n, n_avail, len(selected),
        )

    logger.info(
        "D9 testi başlatılıyor: hedef=%r, kare=%d, warm=%s",
        target_id, len(selected), warm,
    )

    # --- Ortak HTTP istemcisi ---
    times: list[float] = []
    errors: list[str] = []

    async with httpx.AsyncClient(
        timeout=httpx.Timeout(60.0, connect=10.0),
        follow_redirects=True,
        http2=False,
    ) as client:
        for idx, s3_key in enumerate(selected, 1):
            # Warm mod için offset yükle (L1 önbellek veya tahmin)
            frame_offsets: dict[str, int] = _DEFAULT_OFFSETS
            if warm and cache_dir is not None:
                cached = await _load_offsets_from_cache(s3_key, cache_dir)
                if cached:
                    frame_offsets = cached

            logger.info(
                "[%d/%d] %s (warm=%s, offsets_source=%s)",
                idx, len(selected), s3_key, warm,
                "l1_cache" if (warm and cache_dir and frame_offsets is not _DEFAULT_OFFSETS)
                else "default",
            )

            try:
                elapsed = await fetch_one_frame(
                    s3_key,
                    warm=warm,
                    offsets=frame_offsets,
                    client=client,
                )
                times.append(elapsed)
                logger.info("  → %.3f s", elapsed)

            except httpx.HTTPStatusError as exc:
                msg = f"HTTP {exc.response.status_code}: {s3_key}"
                errors.append(msg)
                logger.warning("Kare atlandı (%s)", msg)

            except httpx.RequestError as exc:
                msg = f"Bağlantı hatası: {s3_key}: {exc}"
                errors.append(msg)
                logger.warning("Kare atlandı (%s)", msg)

    # --- İstatistik hesapla ---
    stats = _compute_stats(times)
    gpu_trigger = bool(times and stats["p50"] > GPU_TRIGGER_P50_S)

    return {
        "target":     target_id,
        "n_requested": n,
        "n_measured":  len(times),
        "n_errors":    len(errors),
        "warm":       warm,
        "p50":        stats["p50"],
        "p95":        stats["p95"],
        "min":        stats["min"],
        "max":        stats["max"],
        "gpu_trigger": gpu_trigger,
        "times":      times,
        "errors":     errors,
    }


# ---------------------------------------------------------------------------
# Rapor çıktısı
# ---------------------------------------------------------------------------


def print_report(result: dict[str, Any]) -> None:
    """
    Hız testi sonuçlarını terminale biçimli olarak yazdırır.

    Çıktı formatı (örnek)::

        D9 Hız Testi — barnard (50 kare, soğuk)
        ─────────────────────────────────────────
        p50:  0.72 s     p95:  1.84 s
        min:  0.41 s     max:  2.31 s
        ─────────────────────────────────────────
        Ölçülen / İstenen: 50 / 50  (Hatalı: 0)
        GPU tetikleyicisi (p50 > 2.0 s): HAYIR
        ─────────────────────────────────────────

    Args:
        result: ``run_test()`` dönüş sözlüğü.
    """
    target  = result["target"]
    n_req   = result["n_requested"]
    warm    = result["warm"]
    p50     = result["p50"]
    p95     = result["p95"]
    t_min   = result["min"]
    t_max   = result["max"]
    n_meas  = result["n_measured"]
    n_err   = result["n_errors"]
    gpu     = result["gpu_trigger"]

    mod_str = "isinmis" if warm else "soguk"
    sep     = "-" * 45

    print()
    print(f"D9 Hiz Testi -- {target} ({n_req} kare, {mod_str})")
    print(sep)
    print(f"p50: {p50:6.2f} s     p95: {p95:6.2f} s")
    print(f"min: {t_min:6.2f} s     max: {t_max:6.2f} s")
    print(sep)
    print(f"Olculen / Istenen: {n_meas} / {n_req}  (Hatali: {n_err})")
    gpu_str = "EVET" if gpu else "HAYIR"
    print(f"GPU tetikleyicisi (p50 > {GPU_TRIGGER_P50_S:.1f} s): {gpu_str}")
    print(sep)
    print()


# ---------------------------------------------------------------------------
# Komut satırı giriş noktası
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    """Komut satırı argüman ayrıştırıcısını oluşturur."""
    parser = argparse.ArgumentParser(
        description=(
            "D9 Sunucu Hız Testi — Barnard karelerinden rastgele örnek seçerek "
            "koalesan S3 Range GET ölçümü yapar."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--target",
        default="barnard",
        help="Test hedefi kimliği.",
    )
    parser.add_argument(
        "--n",
        type=int,
        default=50,
        help="Test edilecek kare sayısı.",
    )
    parser.add_argument(
        "--warm",
        action="store_true",
        help=(
            "Isınmış mod: L1 önbellek offsetleri ile veri çekimi "
            "(başlık keşif aşaması atlanır)."
        ),
    )
    parser.add_argument(
        "--cache-dir",
        type=pathlib.Path,
        default=None,
        dest="cache_dir",
        help="Önbellek kök dizini (örn. /cache). L0/L1 alt dizinleri burada aranır.",
    )
    parser.add_argument(
        "--log-level",
        default="WARNING",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Günlük kayıt düzeyi.",
    )
    return parser


if __name__ == "__main__":
    import sys

    parser = _build_parser()
    args   = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        stream=sys.stderr,
    )

    result = asyncio.run(
        run_test(
            target_id=args.target,
            n=args.n,
            warm=args.warm,
            cache_dir=args.cache_dir,
        )
    )

    print_report(result)

    # Çıkış kodu: GPU tetikleyicisi devredeyse 2, hepsi hatalıysa 1, OK ise 0
    if result["n_measured"] == 0:
        sys.exit(1)
    if result["gpu_trigger"]:
        sys.exit(2)
    sys.exit(0)
