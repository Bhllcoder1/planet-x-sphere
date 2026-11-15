"""
L0 önbelleği: frame listesi JSON dosyaları.

Bir hedefin tüm karelerinin listesini TAP sorgusundan dondurur.
Demo hedefleri: load_frames() ile okunur; TAP başarısız olsa bile çalışır.

Dizin yapısı:
    L0_CACHE_DIR/{target_id}/frames.json

Dosya içeriği:
    {
        "target_id": "...",
        "frames": [
            {
                "frame_id": "...",
                "s3_key": "...",
                "detector": "D2",
                "pass_index": 0,
                "mjd_avg": 60123.456,
                "sps_epa": 0.0,
                "content_length": 65011712
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
from dataclasses import dataclass
from typing import Any

import aiofiles

logger = logging.getLogger(__name__)


class CacheMiss(Exception):
    """
    Önbellekte aranan varlık bulunamadı.

    Bu bir arama hatası değil, normal bir durumdur: çağıran taraf önce
    önbelleği sorgular; CacheMiss alırsa kaynaktan yeniden hesaplar veya
    indirir, sonra önbelleğe yazar.
    """


@dataclass(frozen=True)
class FrameRecord:
    """
    Tek bir SPHEREx L2b karesinin temel meta verisi.

    Attributes:
        frame_id:        TAP katalog tanımlayıcısı.
        s3_key:          S3 nesne anahtarı (ibe/data/spherex/ öneki hariç).
        detector:        Dedektör kodu: "D1" … "D6".
        pass_index:      Geçiş numarası (0 tabanlı, L0 listesi içinde).
        mjd_avg:         IMAGE HDU'dan MJD-AVG.
        sps_epa:         Yönelim açısı: 0.0 veya 180.0 (SPS_EPA anahtar sözcüğü).
        content_length:  S3 Content-Length (bayt).
    """

    frame_id: str
    s3_key: str
    detector: str    # D1..D6
    pass_index: int
    mjd_avg: float
    sps_epa: float   # 0.0 veya 180.0
    content_length: int

    def to_dict(self) -> dict[str, Any]:
        """JSON serileştirme için sözlüğe dönüştürür."""
        return {
            "frame_id": self.frame_id,
            "s3_key": self.s3_key,
            "detector": self.detector,
            "pass_index": self.pass_index,
            "mjd_avg": self.mjd_avg,
            "sps_epa": self.sps_epa,
            "content_length": self.content_length,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "FrameRecord":
        """JSON sözlüğünden FrameRecord nesnesi oluşturur."""
        return cls(
            frame_id=str(d["frame_id"]),
            s3_key=str(d["s3_key"]),
            detector=str(d["detector"]),
            pass_index=int(d["pass_index"]),
            mjd_avg=float(d["mjd_avg"]),
            sps_epa=float(d["sps_epa"]),
            content_length=int(d["content_length"]),
        )


def _l0_path(target_id: str, cache_dir: pathlib.Path) -> pathlib.Path:
    """Verilen hedef için L0 önbellek dosyasının tam yolunu döndürür."""
    return cache_dir / target_id / "frames.json"


async def load_frames(
    target_id: str,
    cache_dir: pathlib.Path,
) -> list[FrameRecord]:
    """
    L0 önbellekten kare listesi yükler.

    Args:
        target_id:  Hedef tanımlayıcısı (örn. "barnard", "eps_indi_a").
        cache_dir:  L0 önbellek kök dizini.

    Returns:
        FrameRecord listesi (en az bir eleman; boş liste diske yazılmaz).

    Raises:
        CacheMiss: Dosya önbellekte bulunamazsa.
        json.JSONDecodeError: Dosya bozuksa.
    """
    path = _l0_path(target_id, cache_dir)
    if not path.exists():
        raise CacheMiss(
            f"L0 cache miss for target_id={target_id!r}: file not found at {path}"
        )

    logger.debug("L0 cache hit: %s", path)
    async with aiofiles.open(path, "r", encoding="utf-8") as f:
        raw = await f.read()

    data: dict[str, Any] = json.loads(raw)
    frames = [FrameRecord.from_dict(item) for item in data["frames"]]
    logger.debug("L0 loaded %d frames for target=%r", len(frames), target_id)
    return frames


async def save_frames(
    target_id: str,
    frames: list[FrameRecord],
    cache_dir: pathlib.Path,
) -> None:
    """
    Kare listesini L0 önbelleğe yazar (atomic).

    Önce geçici bir .tmp dosyasına yazar, ardından os.replace() ile
    hedef dosyanın üzerine taşır. Böylece yarım yazılmış dosya kalıcı
    olmaz.

    Args:
        target_id:  Hedef tanımlayıcısı.
        frames:     Dondurulacak kare kayıtları.
        cache_dir:  L0 önbellek kök dizini.
    """
    path = _l0_path(target_id, cache_dir)
    path.parent.mkdir(parents=True, exist_ok=True)

    payload: dict[str, Any] = {
        "target_id": target_id,
        "frames": [fr.to_dict() for fr in frames],
    }
    text = json.dumps(payload, indent=2, ensure_ascii=False)

    tmp_path = path.parent / (path.name + ".tmp")
    async with aiofiles.open(tmp_path, "w", encoding="utf-8") as f:
        await f.write(text)

    # os.replace atomik: Windows NTFS ve POSIX üzerinde güvenlidir.
    os.replace(tmp_path, path)
    logger.info(
        "L0 cache written: target=%r, %d frames -> %s",
        target_id,
        len(frames),
        path,
    )
