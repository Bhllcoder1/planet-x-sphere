"""
shift_stack_demo.py — CPU referans shift-and-stack karşılaştırması (Görev 04-14).

50 sentetik kare üretir, CPU medyan yığması yapar, süreyi ölçer.
p50 hesaplama: n_runs kez döngüde ölçüp numpy medyanı alır.

GPU tetikleyicisi (B.5):
  - p50 > 2.0 s  → vast.ai GPU adımlarına yönlendir
  - p50 ≤ 2.0 s  → CPU yolu yeterli, GPU gerekmez

SNR kazanç tahmini (Barnard, 358 kare, 64×64 pencere):
  stack_snr ≈ sqrt(N) * single_snr

Kullanım:
    python -m c_sunucu.ops.shift_stack_demo
    python c_sunucu/ops/shift_stack_demo.py --frames 50 --runs 10
"""
from __future__ import annotations

import argparse
import logging
import math
import statistics
import time
from typing import Optional

import numpy as np

# ---------------------------------------------------------------------------
# Sabitler
# ---------------------------------------------------------------------------
GPU_TRIGGER_THRESHOLD_S: float = 2.0   # B.5 tetikleyici eşiği (saniye)
BARNARD_TOTAL_FRAMES: int = 358        # Barnard yıldızı toplam kare sayısı
WINDOW_SIZE: int = 64                  # Algılama penceresi (piksel)
SINGLE_SNR_THRESHOLD: float = 5.0      # Tek kare SNR eşiği (GPU'ya gerek yok)
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Yardımcı: sentetik kare üretimi
# ---------------------------------------------------------------------------


def _uret_sentetik_kareler(n: int, yukseklik: int = 512, genislik: int = 512,
                            seed: int = 42) -> list[np.ndarray]:
    """n adet float32 gürültü karesi üretir (tekrarlanabilir)."""
    rng = np.random.default_rng(seed=seed)
    return [
        rng.standard_normal((yukseklik, genislik)).astype(np.float32)
        for _ in range(n)
    ]


# ---------------------------------------------------------------------------
# CPU shift-and-stack (referans uygulama)
# ---------------------------------------------------------------------------


def _cpu_shift_and_stack(frames: list[np.ndarray]) -> np.ndarray:
    """
    CPU numpy ile medyan shift-and-stack.

    Kaydırma vektörleri bu demo sürümünde sıfır kabul edilir;
    gerçek boru hattında astrometrik çözümden gelir.

    Parametreler
    ----------
    frames:
        Aynı boyuttaki 2-B float32 dizilerin listesi.

    Döndürür
    -------
    np.ndarray
        Yığılmış medyan görüntüsü (float32).
    """
    if not frames:
        raise ValueError("frame listesi boş olamaz")

    boyut = frames[0].shape
    for i, kare in enumerate(frames):
        if kare.shape != boyut:
            raise ValueError(
                f"Kare {i} boyutu {kare.shape} != beklenen {boyut}"
            )

    kutu = np.stack(frames, axis=0)       # (N, H, W)
    return np.median(kutu, axis=0).astype(np.float32)


# ---------------------------------------------------------------------------
# SNR kazanç tahmini
# ---------------------------------------------------------------------------


def snr_kazanim_tahmini(
    n_frames: int,
    single_snr: float,
    threshold: float = SINGLE_SNR_THRESHOLD,
) -> dict:
    """
    stack_snr ≈ sqrt(N) * single_snr formülüyle kazanım tahmini.

    Parametreler
    ----------
    n_frames:
        Yığılacak kare sayısı.
    single_snr:
        Tek karedeki kaynak SNR değeri.
    threshold:
        Tek kare SNR eşiği (bu değerin üstünde GPU'ya gerek yok).

    Döndürür
    -------
    dict
        {"single_snr": float, "stack_snr": float, "gpu_unnecessary": bool,
         "gain_factor": float}
    """
    stack_snr = math.sqrt(n_frames) * single_snr
    kazanim = math.sqrt(n_frames)
    gpu_gereksiz = single_snr > threshold

    return {
        "single_snr": single_snr,
        "stack_snr": stack_snr,
        "gain_factor": kazanim,
        "gpu_unnecessary": gpu_gereksiz,
    }


# ---------------------------------------------------------------------------
# Ana karşılaştırma fonksiyonu (public API)
# ---------------------------------------------------------------------------


def shift_and_stack_cpu_benchmark(
    n_frames: int = 50,
    n_runs: int = 10,
    frame_height: int = 512,
    frame_width: int = 512,
    seed: int = 42,
    single_snr: Optional[float] = None,
) -> dict:
    """
    CPU shift-and-stack için p50/p95 karşılaştırması çalıştırır.

    Parametreler
    ----------
    n_frames:
        Her çalıştırma için üretilecek kare sayısı (varsayılan 50).
    n_runs:
        Karşılaştırma döngüsü sayısı (varsayılan 10).
    frame_height:
        Kare yüksekliği piksel (varsayılan 512).
    frame_width:
        Kare genişliği piksel (varsayılan 512).
    seed:
        Rastgele sayı üreteci için başlangıç değeri.
    single_snr:
        Tek kare SNR değeri; None ise SNR tahmini atlanır.

    Döndürür
    -------
    dict
        {
          "p50_s": float,          # medyan süre (saniye)
          "p95_s": float,          # 95. yüzdelik süre (saniye)
          "trigger_gpu": bool,     # p50 > GPU_TRIGGER_THRESHOLD_S mı?
          "n_frames": int,
          "n_runs": int,
          "times_s": list[float],  # tüm çalışma süreleri
        }
    """
    sureler: list[float] = []

    for calisma in range(n_runs):
        kareler = _uret_sentetik_kareler(
            n_frames, yukseklik=frame_height, genislik=frame_width, seed=seed + calisma
        )
        t0 = time.perf_counter()
        _cpu_shift_and_stack(kareler)
        sure = time.perf_counter() - t0
        sureler.append(sure)
        logger.debug("Çalışma %d/%d: %.4f s", calisma + 1, n_runs, sure)

    sureler_sirali = sorted(sureler)
    p50 = statistics.median(sureler)
    # p95 indeksi
    p95_idx = min(int(math.ceil(0.95 * n_runs)) - 1, n_runs - 1)
    p95 = sureler_sirali[p95_idx]

    gpu_tetikle = p50 > GPU_TRIGGER_THRESHOLD_S

    sonuc = {
        "p50_s": p50,
        "p95_s": p95,
        "trigger_gpu": gpu_tetikle,
        "n_frames": n_frames,
        "n_runs": n_runs,
        "times_s": sureler,
    }

    # --- Konsol çıktısı ---
    print("\n" + "=" * 60)
    print("  Shift-and-Stack CPU Karşılaştırma Sonuçları")
    print("=" * 60)
    print(f"  Kare sayısı   : {n_frames}")
    print(f"  Çalışma sayısı: {n_runs}")
    print(f"  Kare boyutu   : {frame_height}×{frame_width}")
    print(f"  p50 (medyan)  : {p50:.4f} s")
    print(f"  p95           : {p95:.4f} s")
    print(f"  Eşik          : {GPU_TRIGGER_THRESHOLD_S:.1f} s")
    print("-" * 60)

    if gpu_tetikle:
        print("  ⚠  GPU TETİKLEYİCİ: EVET")
        print("     p50 > 2.0 s — vast.ai GPU adımları için bkz:")
        print("     c_sunucu/ops/SHIFT_STACK_RUNBOOK.md  §GPU Yolu")
    else:
        print("  ✓  GPU TETİKLEYİCİ: HAYIR")
        print("     p50 ≤ 2.0 s — CPU yolu yeterli, GPU gerekmez.")

    # --- SNR tahmini ---
    if single_snr is not None:
        snr = snr_kazanim_tahmini(BARNARD_TOTAL_FRAMES, single_snr)
        print("-" * 60)
        print("  SNR Kazanım Tahmini (Barnard, 358 kare, 64×64 pencere)")
        print(f"  Tek kare SNR   : {snr['single_snr']:.2f}")
        print(f"  Kazanım faktörü: √{BARNARD_TOTAL_FRAMES} ≈ {snr['gain_factor']:.2f}×")
        print(f"  Yığılmış SNR   : {snr['stack_snr']:.2f}")
        if snr["gpu_unnecessary"]:
            print(f"  → Tek kare SNR > {SINGLE_SNR_THRESHOLD:.1f} eşiği: GPU'ya GEREK YOK.")
        else:
            print(f"  → Tek kare SNR ≤ {SINGLE_SNR_THRESHOLD:.1f} eşiği: yığma kazanımı kritik.")
        sonuc["snr"] = snr

    print("=" * 60 + "\n")
    return sonuc


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _arg_ayristir() -> argparse.Namespace:
    ayristirici = argparse.ArgumentParser(
        description=(
            "shift_stack_demo — CPU shift-and-stack referans karşılaştırması. "
            "p50 > 2.0 s ise GPU tetikleyicisi devreye girer."
        )
    )
    ayristirici.add_argument(
        "--frames", type=int, default=50,
        help="Kare sayısı (varsayılan: 50)"
    )
    ayristirici.add_argument(
        "--runs", type=int, default=10,
        help="Karşılaştırma döngüsü sayısı (varsayılan: 10)"
    )
    ayristirici.add_argument(
        "--height", type=int, default=512,
        help="Kare yüksekliği piksel (varsayılan: 512)"
    )
    ayristirici.add_argument(
        "--width", type=int, default=512,
        help="Kare genişliği piksel (varsayılan: 512)"
    )
    ayristirici.add_argument(
        "--single-snr", type=float, default=None,
        help="Tek kare SNR değeri (SNR tahmini için, isteğe bağlı)"
    )
    ayristirici.add_argument(
        "--log-level", default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Günlük seviyesi (varsayılan: INFO)"
    )
    return ayristirici.parse_args()


def main() -> None:
    args = _arg_ayristir()
    logging.basicConfig(level=args.log_level, format=LOG_FORMAT)
    shift_and_stack_cpu_benchmark(
        n_frames=args.frames,
        n_runs=args.runs,
        frame_height=args.height,
        frame_width=args.width,
        single_snr=args.single_snr,
    )


if __name__ == "__main__":
    main()
