"""
d9_simulate.py — D9 VM zamanlama testinin yerel simülasyonu.

Gerçek bir AWS us-east-1 VM gerektirmeden bölge-dışı (Ankara) gecikme
profilini simüle eder. D9Result dataclass'ını kullanarak sahte ölçümler
üretir; referans değerler: p50 ~3.9 s, p95 ~12.73 s.

Kullanım:
    python -m c_sunucu.ops.d9_simulate
    python -m c_sunucu.ops.d9_simulate --n 50 --seed 42 --out-dir .

Çıktı:
    d9_result_simulated_{timestamp}.json
"""
from __future__ import annotations

import argparse
import datetime
import json
import logging
import pathlib
import random
import socket
import statistics
import sys
from dataclasses import asdict

# d9_test modülünden D9Result ve sabitlerini içe aktar
from c_sunucu.ops.d9_test import (
    GPU_TRIGGER_THRESHOLD,
    D9Result,
    _build_barnard_keys,
    _percentiles,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Simülasyon parametreleri (Ankara referans değerleri)
# ---------------------------------------------------------------------------

# Log-normal dağılım parametreleri: p50 ≈ 3.9 s, p95 ≈ 12.73 s üretmek için
# log-normal: mu = ln(median), sigma hesaplandı:
#   p95 = exp(mu + 1.645 * sigma)  → sigma = (ln(12.73) - ln(3.9)) / 1.645
#   sigma ≈ (2.5435 - 1.3610) / 1.645 ≈ 0.719
_LN_MU: float = 1.3610    # ln(3.9) ≈ medyan
_LN_SIGMA: float = 0.719  # log-normal sigma


def _utc_iso_now() -> str:
    """Şu anki UTC zamanını ISO 8601 biçiminde döner."""
    return datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _get_hostname() -> str:
    """Makine hostname'ini döner; hata durumunda 'localhost-sim' döner."""
    try:
        return socket.gethostname()
    except Exception:  # noqa: BLE001
        return "localhost-sim"


def simulate_d9(
    n: int = 50,
    seed: int = 42,
    target: str = "barnard",
    out_dir: pathlib.Path | None = None,
) -> tuple[D9Result, pathlib.Path]:
    """
    D9 testini log-normal gecikme dağılımıyla simüle eder.

    Ankara referans profili: p50 ≈ 3.9 s, p95 ≈ 12.73 s.
    gpu_trigger = True (p50 > 2.0 s).

    Parameters
    ----------
    n:
        Simüle edilecek kare sayısı (varsayılan: 50).
    seed:
        Rastgelelik tohumu (tekrarlanabilirlik için).
    target:
        Simülasyon hedefi ('barnard').
    out_dir:
        JSON çıktı dizini; None ise çalışma dizini.

    Returns
    -------
    tuple[D9Result, pathlib.Path]
        (sonuç nesnesi, yazılan JSON dosyası yolu).
    """
    if out_dir is None:
        out_dir = pathlib.Path(".")

    rng = random.Random(seed)
    # Log-normal örnekleme: her kare için simüle edilmiş gecikme
    times: list[float] = []
    for _ in range(n):
        # Log-normal: X = exp(mu + sigma * Z), Z ~ N(0,1)
        # random.gauss ile normal örnekleme
        z = rng.gauss(0.0, 1.0)
        t = _LN_MU + _LN_SIGMA * z
        # exp dönüşümü; alt sınır 0.1 s (ağ sıfıra düşmesin)
        times.append(max(0.1, 2.718281828 ** t))

    times_rounded = [round(t, 4) for t in times]

    # İstatistikler
    p50, p95 = _percentiles(times)
    p_min = min(times)
    p_max = max(times)
    gpu_trigger = p50 > GPU_TRIGGER_THRESHOLD

    # Kare listesi (gerçek key'ler gibi)
    frames_tested = _build_barnard_keys(n, seed=seed)

    timestamp = _utc_iso_now()
    hostname = _get_hostname()

    result = D9Result(
        target=target,
        n=n,
        warm=False,
        p50=round(p50, 4),
        p95=round(p95, 4),
        p_min=round(p_min, 4),
        p_max=round(p_max, 4),
        gpu_trigger=gpu_trigger,
        times=times_rounded,
        hostname=f"{hostname}-sim",
        timestamp=timestamp,
        frames_tested=frames_tested,
        errors=[],
    )

    # JSON dosyasını yaz
    json_path = _write_simulated_json(result, out_dir)

    return result, json_path


def _write_simulated_json(result: D9Result, out_dir: pathlib.Path) -> pathlib.Path:
    """
    Simülasyon sonucunu JSON dosyasına yazar.

    Dosya adı: d9_result_simulated_{timestamp}.json

    Parameters
    ----------
    result:
        D9Result nesnesi.
    out_dir:
        Çıktı dizini; yoksa oluşturulur.

    Returns
    -------
    pathlib.Path
        Yazılan dosyanın yolu.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    safe_ts = result.timestamp.replace(":", "").replace("-", "").replace("T", "_")
    fname = out_dir / f"d9_result_simulated_{safe_ts}.json"
    payload = asdict(result)
    # Simülasyon olduğunu belirten alan ekle
    payload["simulated"] = True
    payload["sim_profile"] = "ankara_reference"
    fname.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return fname


def _print_summary(result: D9Result, json_path: pathlib.Path) -> None:
    """Simülasyon özetini terminale basar."""
    gpu_str = "EVET (simüle)" if result.gpu_trigger else "HAYIR (simüle)"
    print()
    print("=" * 60)
    print(f"D9 SİMÜLASYONU — {result.target} (n={result.n})")
    print(f"Profil: Ankara referans (bölge-dışı)")
    print(f"Makine: {result.hostname}")
    print("-" * 60)
    print(f"p50: {result.p50:.3f}s  p95: {result.p95:.3f}s")
    print(f"min: {result.p_min:.3f}s  max: {result.p_max:.3f}s")
    print(f"GPU tetikleyicisi: p50 > {GPU_TRIGGER_THRESHOLD:.1f}s → {gpu_str}")
    print("-" * 60)
    p50_ok = "✓" if result.p50 < 1.0 else "✗"
    p95_ok = "✓" if result.p95 < 3.0 else "✗"
    print(f"Hedef p50 < 1.0s: {p50_ok}  ({result.p50:.3f}s)  [Ankara'dan beklenen: ✗]")
    print(f"Hedef p95 < 3.0s: {p95_ok}  ({result.p95:.3f}s)  [Ankara'dan beklenen: ✗]")
    print("=" * 60)
    print(f"Sonuç JSON: {json_path}")
    print()


# ---------------------------------------------------------------------------
# CLI giriş noktası
# ---------------------------------------------------------------------------


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="d9_simulate",
        description=(
            "D9 simülasyonu — Ankara bölge-dışı gecikme profiliyle yerel test.\n"
            "Gerçek VM gerektirmez; p50 ~3.9 s, p95 ~12.73 s üretir."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--n",
        type=int,
        default=50,
        metavar="N",
        help="Simüle edilecek kare sayısı (varsayılan: 50)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Rastgele tohum (varsayılan: 42)",
    )
    parser.add_argument(
        "--target",
        default="barnard",
        choices=["barnard"],
        help="Simülasyon hedefi (varsayılan: barnard)",
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
        Çıkış kodu: 0 = başarılı, 2 = GPU tetikleyicisi aktif.
    """
    args = _parse_args(argv)
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        stream=sys.stderr,
    )

    print(f"D9 Simülasyonu başlıyor — hedef={args.target} n={args.n} seed={args.seed}", flush=True)
    print("Profil: Ankara bölge-dışı (p50~3.9s, p95~12.73s)", flush=True)

    result, json_path = simulate_d9(
        n=args.n,
        seed=args.seed,
        target=args.target,
        out_dir=args.out_dir,
    )
    _print_summary(result, json_path)

    return 2 if result.gpu_trigger else 0


if __name__ == "__main__":
    sys.exit(main())
