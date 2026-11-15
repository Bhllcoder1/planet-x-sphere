"""
L1 önbelleği: Dosya başına HDU byte-offset haritaları.

Her FITS dosyasının HDU başlık ve veri başlangıç konumlarını JSON olarak saklar.
Warm okumada HDU başlık taraması atlanır; doğrudan veri Range GET yapılır.

Dizin yapısı:
    L1_CACHE_DIR/{frame_id}.json

Dosya içeriği (ByteOffsetMap.to_dict() çıktısı):
    {
        "frame_id": "...",
        "s3_key": "spherex/l2b/...",
        "file_size": 65011712,
        "hdus": [
            {
                "name": "IMAGE",
                "index": 1,
                "header_start": 2880,
                "data_start": 17280,
                "naxis1": 2040,
                "naxis2": 2048,
                "bitpix": -32
            },
            ...
        ]
    }
"""
from __future__ import annotations

import json
import logging
import os
import pathlib
from typing import Any

import aiofiles

from .byte_offset_map import ByteOffsetMap
from .l0_cache import CacheMiss

logger = logging.getLogger(__name__)


def _l1_path(frame_id: str, cache_dir: pathlib.Path) -> pathlib.Path:
    """Verilen kare için L1 önbellek dosyasının tam yolunu döndürür."""
    return cache_dir / f"{frame_id}.json"


async def load_offset_map(
    frame_id: str,
    cache_dir: pathlib.Path,
) -> ByteOffsetMap:
    """
    L1 önbellekten byte-offset haritası yükler.

    Args:
        frame_id:   SPHEREx kare tanımlayıcısı.
        cache_dir:  L1 önbellek kök dizini.

    Returns:
        ByteOffsetMap nesnesi.

    Raises:
        CacheMiss: Dosya önbellekte bulunamazsa.
        json.JSONDecodeError: Dosya bozuksa.
        KeyError: Zorunlu bir alan eksikse.
    """
    path = _l1_path(frame_id, cache_dir)
    if not path.exists():
        raise CacheMiss(
            f"L1 cache miss for frame_id={frame_id!r}: file not found at {path}"
        )

    logger.debug("L1 cache hit: %s", path)
    async with aiofiles.open(path, "r", encoding="utf-8") as f:
        raw = await f.read()

    data: dict[str, Any] = json.loads(raw)
    offset_map = ByteOffsetMap.from_dict(data)
    logger.debug(
        "L1 loaded %d HDUs for frame=%r",
        len(offset_map.hdus),
        frame_id,
    )
    return offset_map


async def save_offset_map(
    offset_map: ByteOffsetMap,
    cache_dir: pathlib.Path,
) -> None:
    """
    Byte-offset haritasını L1 önbelleğe yazar (atomic).

    Önce geçici bir .tmp dosyasına yazar, ardından os.replace() ile
    hedef dosyanın üzerine taşır.

    Args:
        offset_map: Yazılacak ByteOffsetMap nesnesi.
        cache_dir:  L1 önbellek kök dizini.
    """
    path = _l1_path(offset_map.frame_id, cache_dir)
    path.parent.mkdir(parents=True, exist_ok=True)

    text = json.dumps(offset_map.to_dict(), indent=2, ensure_ascii=False)

    tmp_path = path.parent / (path.name + ".tmp")
    async with aiofiles.open(tmp_path, "w", encoding="utf-8") as f:
        await f.write(text)

    os.replace(tmp_path, path)
    logger.info(
        "L1 cache written: frame=%r, %d HDUs -> %s",
        offset_map.frame_id,
        len(offset_map.hdus),
        path,
    )


async def has_offset_map(frame_id: str, cache_dir: pathlib.Path) -> bool:
    """
    L1 önbellekte belirtilen kare için harita olup olmadığını döndürür.
    CacheMiss fırlatmadan önce kontrol etmek için kullanılır.

    Args:
        frame_id:   SPHEREx kare tanımlayıcısı.
        cache_dir:  L1 önbellek kök dizini.

    Returns:
        True ise harita mevcut, False ise yoktur.
    """
    return _l1_path(frame_id, cache_dir).exists()
