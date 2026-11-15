"""
gpu_stack.py — GPU shift-and-stack (koşullu, Görev 06-13).

D9 tetikleyicisi: fetch p50 > 2.0 s olursa çalıştırılır.
CPU numpy ile temel yığma; GPU (CuPy) tetikleyici koşulunda.

Kullanım:
    python -m c_sunucu.ops.gpu_stack --target barnard --frames 50
    python -m c_sunucu.ops.gpu_stack --target barnard --frames 50 --gpu
"""
from __future__ import annotations

import argparse
import logging
import pathlib
import time
from typing import Optional

import numpy as np

# ---------------------------------------------------------------------------
# Sabitler
# ---------------------------------------------------------------------------
D9_P50_THRESHOLD_S: float = 2.0  # saniye — VASTAI_RUNBOOK.md ile senkronize
DEFAULT_OUTPUT_DIR: pathlib.Path = pathlib.Path("outputs")
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

# ---------------------------------------------------------------------------
# CuPy isteğe bağlı bağımlılık
# ---------------------------------------------------------------------------
GPU_AVAILABLE: bool = False

try:
    import cupy as cp  # type: ignore[import]

    GPU_AVAILABLE = True
except ImportError:
    cp = None  # type: ignore[assignment]

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Temel işlevler
# ---------------------------------------------------------------------------


def shift_and_stack_cpu(frames: list[np.ndarray]) -> np.ndarray:
    """
    CPU numpy ile medyan shift-and-stack.

    Yığma öncesi kaydırma uygulanmaz; koordinat hizalaması sonraki görevde
    (Görev 04-14) ele alınacaktır. Şu an her kare hizasız olduğundan salt
    medyan medyan kullanılır.

    Parametreler
    ----------
    frames:
        Aynı boyuttaki 2-B float32 dizilerin listesi.

    Döndürür
    -------
    np.ndarray
        Yığılmış medyan görüntüsü (float32).

    Raises
    ------
    ValueError
        Boş frame listesi veya tutarsız boyutlar.
    """
    if not frames:
        raise ValueError("frame listesi boş olamaz")

    boyut = frames[0].shape
    for i, kare in enumerate(frames):
        if kare.shape != boyut:
            raise ValueError(
                f"Kare {i} boyutu {kare.shape} != beklenen {boyut}"
            )

    kutu = np.stack(frames, axis=0)  # (N, H, W)
    sonuc = np.median(kutu, axis=0).astype(np.float32)
    logger.debug(
        "CPU yığma tamamlandı: %d kare, çıktı şekli %s", len(frames), sonuc.shape
    )
    return sonuc


def shift_and_stack_gpu(frames: list[np.ndarray]) -> np.ndarray:
    """
    CuPy ile GPU hızlandırmalı shift-and-stack.

    CuPy kurulu değilse otomatik olarak CPU uygulamasına düşer.

    Parametreler
    ----------
    frames:
        Aynı boyuttaki 2-B float32 NumPy dizilerin listesi.

    Döndürür
    -------
    np.ndarray
        Yığılmış medyan görüntüsü (float32, CPU belleğine kopyalanmış).

    Raises
    ------
    ValueError
        Boş frame listesi veya tutarsız boyutlar.
    """
    if not GPU_AVAILABLE:
        logger.warning("CuPy bulunamadı; CPU yoluna düşülüyor")
        return shift_and_stack_cpu(frames)

    if not frames:
        raise ValueError("frame listesi boş olamaz")

    boyut = frames[0].shape
    for i, kare in enumerate(frames):
        if kare.shape != boyut:
            raise ValueError(
                f"Kare {i} boyutu {kare.shape} != beklenen {boyut}"
            )

    logger.info("GPU yığma başlatılıyor: %d kare", len(frames))
    gpu_kareler = [cp.asarray(k, dtype=cp.float32) for k in frames]
    gpu_kutu = cp.stack(gpu_kareler, axis=0)  # (N, H, W) — GPU belleğinde
    gpu_sonuc = cp.median(gpu_kutu, axis=0).astype(cp.float32)
    sonuc: np.ndarray = cp.asnumpy(gpu_sonuc)
    logger.debug(
        "GPU yığma tamamlandı: %d kare, çıktı şekli %s", len(frames), sonuc.shape
    )
    return sonuc


# ---------------------------------------------------------------------------
# Sahte kare üretimi (gerçek veri yolu henüz entegre edilmedi)
# ---------------------------------------------------------------------------


def _sahte_kareler_olustur(
    n: int, yukseklik: int = 512, genislik: int = 512
) -> list[np.ndarray]:
    """
    Testler ve CLI demosu için rastgele kare listesi oluşturur.

    Gerçek kullanımda bu fonksiyon yerine önbellek okuyucu
    (Görev 04-14) yerleşecektir.
    """
    rng = np.random.default_rng(seed=42)
    return [
        rng.standard_normal((yukseklik, genislik)).astype(np.float32)
        for _ in range(n)
    ]


# ---------------------------------------------------------------------------
# Çıktı kaydetme
# ---------------------------------------------------------------------------


def sonucu_kaydet(
    dizi: np.ndarray,
    hedef: str,
    cikti_dizini: pathlib.Path,
    gpu_kullanildi: bool,
) -> pathlib.Path:
    """
    Yığılmış diziyi .npy dosyası olarak diske kaydeder.

    Parametreler
    ----------
    dizi:
        Kaydedilecek NumPy dizisi.
    hedef:
        Gözlem hedefinin adı (dosya adına eklenir).
    cikti_dizini:
        Çıktının yazılacağı dizin (yoksa oluşturulur).
    gpu_kullanildi:
        Dosya adına `_gpu` veya `_cpu` etiketi eklemek için kullanılır.

    Döndürür
    -------
    pathlib.Path
        Yazılan dosyanın yolu.
    """
    cikti_dizini.mkdir(parents=True, exist_ok=True)
    etiket = "gpu" if gpu_kullanildi else "cpu"
    zaman_damgasi = int(time.time())
    dosya_adi = f"stack_{hedef}_{etiket}_{zaman_damgasi}.npy"
    yol = cikti_dizini / dosya_adi
    np.save(yol, dizi)
    logger.info("Sonuç kaydedildi: %s (şekil=%s)", yol, dizi.shape)
    return yol


# ---------------------------------------------------------------------------
# Orkestrasyonu gerçekleştiren ana işlev
# ---------------------------------------------------------------------------


def calistir(
    hedef: str,
    kare_sayisi: int,
    gpu: bool = False,
    cikti_dizini: pathlib.Path = DEFAULT_OUTPUT_DIR,
    p50_saniye: Optional[float] = None,
) -> pathlib.Path:
    """
    Shift-and-stack boru hattını çalıştırır.

    D9 tetikleyicisini denetler; eşik aşılmadıysa ve GPU istenmediyse
    CPU yolunu zorla seçer.

    Parametreler
    ----------
    hedef:
        Gözlem hedefinin adı (örn. "barnard").
    kare_sayisi:
        Yığılacak kare sayısı.
    gpu:
        ``True`` ise GPU (CuPy) yolunu kullan.
    cikti_dizini:
        Çıktı .npy dosyasının yazılacağı dizin.
    p50_saniye:
        Dışarıdan ölçülmüş D9 p50 gecikmesi (saniye).
        ``None`` ise tetikleyici denetimi atlanır; ``gpu`` bayrağı geçerli.

    Döndürür
    -------
    pathlib.Path
        Kaydedilen çıktı dosyasının yolu.
    """
    # D9 tetikleyici denetimi
    if p50_saniye is not None:
        if p50_saniye <= D9_P50_THRESHOLD_S and not gpu:
            logger.info(
                "D9 p50=%.3f s <= %.1f s eşiği; GPU devredışı, CPU yolu kullanılıyor.",
                p50_saniye,
                D9_P50_THRESHOLD_S,
            )
            gpu = False
        elif p50_saniye > D9_P50_THRESHOLD_S:
            logger.info(
                "D9 p50=%.3f s > %.1f s eşiği; GPU yolu etkinleştiriliyor.",
                p50_saniye,
                D9_P50_THRESHOLD_S,
            )
            gpu = True

    logger.info(
        "Yığma başlıyor — hedef=%s, kareler=%d, mod=%s",
        hedef,
        kare_sayisi,
        "GPU" if gpu else "CPU",
    )

    t0 = time.perf_counter()
    kareler = _sahte_kareler_olustur(kare_sayisi)

    if gpu:
        yigilmis = shift_and_stack_gpu(kareler)
    else:
        yigilmis = shift_and_stack_cpu(kareler)

    sure = time.perf_counter() - t0
    logger.info("Yığma süresi: %.3f s", sure)

    return sonucu_kaydet(yigilmis, hedef, cikti_dizini, gpu_kullanildi=gpu)


# ---------------------------------------------------------------------------
# CLI giriş noktası
# ---------------------------------------------------------------------------


def _arg_ayristir() -> argparse.Namespace:
    """Komut satırı argümanlarını ayrıştırır."""
    ayristirici = argparse.ArgumentParser(
        description=(
            "gpu_stack — D9 tetikleyicili shift-and-stack. "
            "p50 > 2.0 s ise --gpu bayrağı ile GPU yolu etkinleştirilir."
        )
    )
    ayristirici.add_argument(
        "--target",
        required=True,
        help="Gözlem hedefinin adı (örn. barnard)",
    )
    ayristirici.add_argument(
        "--frames",
        type=int,
        default=50,
        help="Yığılacak kare sayısı (varsayılan: 50)",
    )
    ayristirici.add_argument(
        "--gpu",
        action="store_true",
        default=False,
        help="GPU (CuPy) yolunu zorla etkinleştir",
    )
    ayristirici.add_argument(
        "--p50",
        type=float,
        default=None,
        metavar="SANIYE",
        help=(
            "D9 fetch p50 gecikmesi (saniye). "
            "Belirtilirse %.1f s eşiği otomatik denetlenir." % D9_P50_THRESHOLD_S
        ),
    )
    ayristirici.add_argument(
        "--output-dir",
        type=pathlib.Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Çıktı dizini (varsayılan: outputs/)",
    )
    ayristirici.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Günlük seviyesi (varsayılan: INFO)",
    )
    return ayristirici.parse_args()


def main() -> None:
    """CLI giriş noktası."""
    args = _arg_ayristir()
    logging.basicConfig(level=args.log_level, format=LOG_FORMAT)

    cikti = calistir(
        hedef=args.target,
        kare_sayisi=args.frames,
        gpu=args.gpu,
        cikti_dizini=args.output_dir,
        p50_saniye=args.p50,
    )
    print(f"Çıktı: {cikti}")


if __name__ == "__main__":
    main()
