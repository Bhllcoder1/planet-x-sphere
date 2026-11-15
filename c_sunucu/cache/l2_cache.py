"""
L2 önbelleği: Önceden hesaplanmış pencere dosyaları.

Her (frame_id, x0, y0, width, height) penceresi için numpy dizilerini ve
meta veriyi .npz formatında saklar. Thumbnail PNG dosyalarını da yönetir.

Dizin yapısı:
    L2_CACHE_DIR/{frame_id}/{x0}_{y0}_{width}_{height}.npz
    L2_CACHE_DIR/{frame_id}/thumb_64.png

NPZ içeriği:
    image     — float32 (height, width):  IMAGE HDU penceresi
    flags     — int32   (height, width):  FLAGS HDU penceresi
    variance  — float32 (height, width):  VARIANCE HDU penceresi
    zodi      — float32 (height, width):  ZODI HDU penceresi
    meta_json — str (0-boyutlu dizi):     JSON olarak kodlanmış meta sözlük

Not: numpy işlemleri bloke edici (senkron) olduğundan run_in_executor
kullanılır; böylece asyncio olay döngüsü bekleme süresinde askıya alınmaz.
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
import pathlib
from dataclasses import dataclass, field
from typing import Any

import aiofiles
import numpy as np

from .l0_cache import CacheMiss

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class WindowKey:
    """
    Bir L2 önbellek girişini benzersiz biçimde tanımlayan anahtar.

    Attributes:
        frame_id: SPHEREx kare tanımlayıcısı.
        x0:       Pencerenin sol kenarı (sütun, 0 tabanlı).
        y0:       Pencerenin üst kenarı (satır, 0 tabanlı).
        width:    Pencere genişliği (piksel).
        height:   Pencere yüksekliği (piksel).
    """

    frame_id: str
    x0: int
    y0: int
    width: int
    height: int

    def filename(self) -> str:
        """NPZ dosya adını döndürür."""
        return f"{self.x0}_{self.y0}_{self.width}_{self.height}.npz"

    def frame_dir(self, cache_dir: pathlib.Path) -> pathlib.Path:
        """Kareye ait L2 alt dizinini döndürür."""
        return cache_dir / self.frame_id

    def file_path(self, cache_dir: pathlib.Path) -> pathlib.Path:
        """NPZ dosyasının tam yolunu döndürür."""
        return self.frame_dir(cache_dir) / self.filename()


@dataclass
class WindowData:
    """
    Bir pencere için numpy dizileri ve meta veri.

    Attributes:
        image:    float32 (height, width) — IMAGE HDU penceresi.
        flags:    int32   (height, width) — FLAGS HDU penceresi.
        variance: float32 (height, width) — VARIANCE HDU penceresi.
        zodi:     float32 (height, width) — ZODI HDU penceresi.
        meta:     JSON serileştirilebilir meta sözlük
                  (örn. MJD, dönüş açısı, dedektör, geçiş bilgisi).
    """

    image: np.ndarray
    flags: np.ndarray
    variance: np.ndarray
    zodi: np.ndarray
    meta: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Dahili yardımcılar (senkron, executor'da çağrılır)
# ---------------------------------------------------------------------------

def _npz_stem(key: WindowKey, cache_dir: pathlib.Path) -> pathlib.Path:
    """
    numpy'ın '.npz' ekleyeceği kök yolu döndürür.
    'x0_y0_w_h_tmp' gibi görünür; numpy bunu 'x0_y0_w_h_tmp.npz' olarak kaydeder.
    """
    stem = f"{key.x0}_{key.y0}_{key.width}_{key.height}_tmp"
    return key.frame_dir(cache_dir) / stem


def _load_npz_sync(path: pathlib.Path) -> WindowData:
    """NPZ dosyasını senkron okur (executor için)."""
    with np.load(path, allow_pickle=False) as npz:
        image = npz["image"]
        flags = npz["flags"]
        variance = npz["variance"]
        zodi = npz["zodi"]
        meta_raw = npz["meta_json"].item()
        meta: dict[str, Any] = json.loads(meta_raw) if meta_raw else {}
    return WindowData(image=image, flags=flags, variance=variance, zodi=zodi, meta=meta)


def _save_npz_sync(path: pathlib.Path, data: WindowData) -> None:
    """
    NPZ dosyasını atomik biçimde senkron yazar (executor için).

    Geçici dosya ismi kaynak dosyadan türetilir; başarıyla yazıldıktan
    sonra os.replace() ile hedef konuma taşınır.
    """
    # Geçici dosya adı: 'stem_tmp' — numpy '.npz' ekler.
    stem = path.parent / (path.stem + "_tmp")
    meta_json = json.dumps(data.meta, ensure_ascii=False)

    np.savez_compressed(
        stem,  # numpy -> stem + '.npz' = path.stem + '_tmp.npz'
        image=data.image,
        flags=data.flags,
        variance=data.variance,
        zodi=data.zodi,
        meta_json=np.array(meta_json),
    )
    tmp_actual = path.parent / (path.stem + "_tmp.npz")
    os.replace(tmp_actual, path)


# ---------------------------------------------------------------------------
# Pencere (window) API'si
# ---------------------------------------------------------------------------

async def load_window(
    frame_id: str,
    x0: int,
    y0: int,
    width: int,
    height: int,
    cache_dir: pathlib.Path,
) -> WindowData:
    """
    L2 önbellekten pencere verisi yükler.

    Args:
        frame_id:  SPHEREx kare tanımlayıcısı.
        x0, y0:    Pencerenin sol üst köşesi (0 tabanlı piksel).
        width:     Pencere genişliği (piksel).
        height:    Pencere yüksekliği (piksel).
        cache_dir: L2 önbellek kök dizini.

    Returns:
        WindowData nesnesi (image, flags, variance, zodi, meta).

    Raises:
        CacheMiss: Dosya önbellekte bulunamazsa.
    """
    key = WindowKey(frame_id=frame_id, x0=x0, y0=y0, width=width, height=height)
    path = key.file_path(cache_dir)

    if not path.exists():
        raise CacheMiss(
            f"L2 cache miss for frame_id={frame_id!r} "
            f"window=({x0},{y0},{width},{height}): file not found at {path}"
        )

    logger.debug("L2 cache hit: %s", path)
    loop = asyncio.get_running_loop()
    data = await loop.run_in_executor(None, _load_npz_sync, path)
    return data


async def save_window(
    frame_id: str,
    x0: int,
    y0: int,
    width: int,
    height: int,
    window_data: WindowData,
    cache_dir: pathlib.Path,
) -> None:
    """
    Pencere verisini L2 önbelleğe yazar (atomic).

    Dizin yoksa oluşturulur. Yazma işlemi executor'da gerçekleşir.

    Args:
        frame_id:     SPHEREx kare tanımlayıcısı.
        x0, y0:       Pencerenin sol üst köşesi (0 tabanlı piksel).
        width:        Pencere genişliği (piksel).
        height:       Pencere yüksekliği (piksel).
        window_data:  Yazılacak WindowData nesnesi.
        cache_dir:    L2 önbellek kök dizini.
    """
    key = WindowKey(frame_id=frame_id, x0=x0, y0=y0, width=width, height=height)
    path = key.file_path(cache_dir)
    path.parent.mkdir(parents=True, exist_ok=True)

    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, _save_npz_sync, path, window_data)
    logger.info("L2 cache written: %s", path)


async def has_window(
    frame_id: str,
    x0: int,
    y0: int,
    width: int,
    height: int,
    cache_dir: pathlib.Path,
) -> bool:
    """
    L2 önbellekte belirtilen pencere olup olmadığını döndürür.

    Returns:
        True ise pencere mevcut, False ise yoktur.
    """
    key = WindowKey(frame_id=frame_id, x0=x0, y0=y0, width=width, height=height)
    return key.file_path(cache_dir).exists()


# ---------------------------------------------------------------------------
# Thumbnail API'si
# ---------------------------------------------------------------------------

def _thumb_path(frame_id: str, cache_dir: pathlib.Path) -> pathlib.Path:
    """Thumbnail PNG'nin tam yolunu döndürür."""
    return cache_dir / frame_id / "thumb_64.png"


async def load_thumbnail(frame_id: str, cache_dir: pathlib.Path) -> bytes:
    """
    L2 önbellekten 64×64 thumbnail PNG'yi yükler.

    Args:
        frame_id:  SPHEREx kare tanımlayıcısı.
        cache_dir: L2 önbellek kök dizini.

    Returns:
        PNG içeriği ham bayt olarak.

    Raises:
        CacheMiss: Dosya önbellekte bulunamazsa.
    """
    path = _thumb_path(frame_id, cache_dir)
    if not path.exists():
        raise CacheMiss(
            f"L2 thumbnail cache miss for frame_id={frame_id!r}: "
            f"file not found at {path}"
        )

    logger.debug("L2 thumbnail cache hit: %s", path)
    async with aiofiles.open(path, "rb") as f:
        return await f.read()


async def save_thumbnail(
    frame_id: str,
    png_bytes: bytes,
    cache_dir: pathlib.Path,
) -> None:
    """
    64×64 thumbnail PNG'yi L2 önbelleğe yazar (atomic).

    Args:
        frame_id:  SPHEREx kare tanımlayıcısı.
        png_bytes: PNG içeriği ham bayt olarak.
        cache_dir: L2 önbellek kök dizini.
    """
    path = _thumb_path(frame_id, cache_dir)
    path.parent.mkdir(parents=True, exist_ok=True)

    tmp_path = path.parent / (path.stem + "_tmp.png")
    async with aiofiles.open(tmp_path, "wb") as f:
        await f.write(png_bytes)

    os.replace(tmp_path, path)
    logger.info("L2 thumbnail written: frame=%r -> %s", frame_id, path)
