"""
prefetch.py — Demo öncesi önbellek ısıtma (çevrimdışı yedek planı).

Demo hedeflerinin kare listesini (L0) TAP'tan çeker, ardından her kare için
pencere verisini (L2) S3'ten indirip diske yazar. Böylece demo günü S3/TAP
erişilemese bile L0/L2 önbelleğinden gösterim yapılabilir.

Davranış:
  * TAP başarısız olursa (TapBusy/TapError) mevcut L0 dosyasından devam edilir.
  * Pencere indirmek için L1 byte-offset haritası gerekir; L1'de yoksa o kare
    atlanır ve uyarı loglanır.
  * Zaten L2'de bulunan pencereler yeniden indirilmez (idempotent).

Kullanım:
    python -m c_sunucu.ops.prefetch --targets barnard eps_indi_b --max-frames 50
    python -m c_sunucu.ops.prefetch --all

Ortam değişkenleri: L0_CACHE_DIR, L1_CACHE_DIR, L2_CACHE_DIR.
"""
from __future__ import annotations

import argparse
import asyncio
import logging
import os
import pathlib
import sys
from typing import Sequence

import httpx

from c_sunucu.api import s3_reader, tap_client
from c_sunucu.cache import l0_cache, l1_cache, l2_cache
from c_sunucu.cache.l0_cache import CacheMiss, FrameRecord

logger = logging.getLogger(__name__)

# Hedef koordinatları (RA, Dec; derece, ICRS). Barnard önce: demo'nun ana hedefi.
TARGETS: dict[str, tuple[float, float]] = {
    "barnard": (269.4521, 4.6933),
    "eps_indi_b": (330.84, -56.79),
    "wise0855": (133.79, -7.24),
    "rwaur": (75.495, 30.40),
    "rdra": (274.06, 68.13),
}

# [ASSUMPTION] Hedef konumunun piksel karşılığı WCS ile b_astrometri'de
# hesaplanır; burada varsayılan pencere görüntü merkezidir. --window ile değiştirilir.
DEFAULT_WINDOW = (970, 970, 100, 100)  # x0, y0, width, height
DEFAULT_CONCURRENCY = 2  # S3 tarafında zaten MAX_CONCURRENT=4 sınırı var


def _env_dir(name: str, default: str) -> pathlib.Path:
    """Ortam değişkeninden dizin okur; yoksa varsayılanı döndürür."""
    return pathlib.Path(os.environ.get(name, default))


def _to_frame_records(tap_frames: Sequence[tap_client.TapFrame]) -> list[FrameRecord]:
    """TapFrame listesini L0 için FrameRecord listesine dönüştürür."""
    return [
        FrameRecord(
            frame_id=tf.frame_id,
            s3_key=tf.s3_key,
            detector=tf.detector,
            pass_index=i,
            mjd_avg=tf.mjd_avg,
            sps_epa=tf.sps_epa,
            content_length=tf.content_length,
        )
        for i, tf in enumerate(tap_frames)
    ]


async def refresh_l0(
    target_id: str,
    ra: float,
    dec: float,
    l0_dir: pathlib.Path,
    client: httpx.AsyncClient,
) -> list[FrameRecord]:
    """
    Hedefin kare listesini TAP'tan yeniler; başarısızsa L0'dan okur.

    Returns:
        Kare listesi (TAP boş dönerse veya hata olursa L0 içeriği).
        L0'da da yoksa boş liste.
    """
    try:
        tap_frames = await tap_client.query_frames(ra, dec, target_id, client=client)
    except (tap_client.TapBusy, tap_client.TapError) as exc:
        logger.warning("[%s] TAP başarısız (%s); L0'dan devam ediliyor", target_id, exc)
    else:
        if tap_frames:
            records = _to_frame_records(tap_frames)
            await l0_cache.save_frames(target_id, records, l0_dir)
            return records
        logger.warning("[%s] TAP boş sonuç döndürdü; L0'a yazılmadı", target_id)

    try:
        return await l0_cache.load_frames(target_id, l0_dir)
    except CacheMiss:
        logger.error("[%s] L0 önbellekte de kayıt yok; hedef atlanıyor", target_id)
        return []


async def _prefetch_window(
    frame: FrameRecord,
    window: tuple[int, int, int, int],
    dirs: tuple[pathlib.Path, pathlib.Path],
    client: httpx.AsyncClient,
) -> str:
    """
    Tek karenin penceresini L2'ye indirir.

    Returns:
        "cached" (zaten vardı), "fetched", "no_l1" veya "failed".
    """
    x0, y0, w, h = window
    l1_dir, l2_dir = dirs
    if await l2_cache.has_window(frame.frame_id, x0, y0, w, h, l2_dir):
        return "cached"

    try:
        l1_map = await l1_cache.load_offset_map(frame.frame_id, l1_dir)
    except CacheMiss:
        logger.warning("[%s] L1 offset haritası yok; pencere atlandı", frame.frame_id)
        return "no_l1"

    try:
        offsets = s3_reader.ByteOffsetMap(
            image_data_start=l1_map.get_hdu("IMAGE").data_start,
            flags_data_start=l1_map.get_hdu("FLAGS").data_start,
            variance_data_start=l1_map.get_hdu("VARIANCE").data_start,
            zodi_data_start=l1_map.get_hdu("ZODI").data_start,
        )
        req = s3_reader.WindowRequest(frame.frame_id, frame.s3_key, x0, y0, w, h)
        raw = await s3_reader.read_window(req, offsets, client=client)
        data = l2_cache.WindowData(
            image=raw.image,
            flags=raw.flags,
            variance=raw.variance,
            zodi=raw.zodi,
            meta={
                "frame_id": frame.frame_id,
                "detector": frame.detector,
                "mjd_avg": frame.mjd_avg,
                "sps_epa": frame.sps_epa,
            },
        )
        await l2_cache.save_window(frame.frame_id, x0, y0, w, h, data, l2_dir)
    except (s3_reader.S3Error, KeyError, ValueError) as exc:
        logger.error("[%s] pencere indirilemedi: %s", frame.frame_id, exc)
        return "failed"
    return "fetched"


async def prefetch_target(
    target_id: str,
    max_frames: int | None,
    window: tuple[int, int, int, int],
    concurrency: int,
    client: httpx.AsyncClient,
) -> dict[str, int]:
    """Bir hedef için L0'ı yeniler ve pencereleri L2'ye indirir; sayaçları döndürür."""
    ra, dec = TARGETS[target_id]
    l0_dir = _env_dir("L0_CACHE_DIR", "cache/l0")
    l1_dir = _env_dir("L1_CACHE_DIR", "cache/l1")
    l2_dir = _env_dir("L2_CACHE_DIR", "cache/l2")

    frames = await refresh_l0(target_id, ra, dec, l0_dir, client)
    if max_frames is not None:
        frames = frames[:max_frames]

    sem = asyncio.Semaphore(concurrency)

    async def _one(fr: FrameRecord) -> str:
        async with sem:
            return await _prefetch_window(fr, window, (l1_dir, l2_dir), client)

    results = await asyncio.gather(*(_one(fr) for fr in frames))
    counts: dict[str, int] = {"frames": len(frames)}
    for status in results:
        counts[status] = counts.get(status, 0) + 1
    logger.info("[%s] özet: %s", target_id, counts)
    return counts


async def run(
    target_ids: Sequence[str],
    max_frames: int | None,
    window: tuple[int, int, int, int],
    concurrency: int,
) -> int:
    """Hedefleri verilen sırayla (sıralı) işler; hata sayısını döndürür."""
    failures = 0
    async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:
        for tid in target_ids:
            try:
                await prefetch_target(tid, max_frames, window, concurrency, client)
            except Exception:  # bir hedef diğerlerini durdurmasın
                logger.exception("[%s] beklenmeyen hata", tid)
                failures += 1
    return failures


def _parse_window(text: str) -> tuple[int, int, int, int]:
    """'x0,y0,w,h' metnini dörtlüye çevirir."""
    try:
        x0, y0, w, h = (int(p) for p in text.split(","))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("biçim: x0,y0,genişlik,yükseklik") from exc
    return x0, y0, w, h


def build_parser() -> argparse.ArgumentParser:
    """CLI argüman ayrıştırıcısını oluşturur."""
    p = argparse.ArgumentParser(description="Demo hedefleri için L0/L2 önbellek ön çekme")
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--targets", nargs="+", choices=sorted(TARGETS), help="Hedef kimlikleri")
    group.add_argument("--all", action="store_true", help="Tüm hedefler (Barnard önce)")
    p.add_argument("--max-frames", type=int, default=None, help="Hedef başına kare üst sınırı")
    p.add_argument("--window", type=_parse_window, default=DEFAULT_WINDOW,
                   help="x0,y0,w,h (varsayılan 970,970,100,100)")
    p.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY)
    return p


def main(argv: Sequence[str] | None = None) -> int:
    """CLI girdi noktası. Çıkış kodu: 0 başarı, 1 en az bir hedef hatalı."""
    args = build_parser().parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    ids = list(TARGETS) if args.all else args.targets
    failures = asyncio.run(run(ids, args.max_frames, args.window, args.concurrency))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
