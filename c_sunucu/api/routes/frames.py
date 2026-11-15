from __future__ import annotations

"""
Kare (frame) uç noktaları.

GET /frames/{frame_id}/window     → piksel penceresi (NumPy .npy → JSON)
GET /frames/{frame_id}/thumbnail  → küçük resim (PNG)

NOT: Gerçek S3 okuması bir sonraki görevde (06-02 / 06-04) eklenecektir.
     Şimdilik yalnızca L2_CACHE_DIR içindeki önceden hesaplanmış dosyalar sunulur.
"""

import io
import logging
from pathlib import Path

import numpy as np
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import Response
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/frames", tags=["frames"])

# PNG içerik türü sabiti
_PNG_CONTENT_TYPE = "image/png"
# Küçük resim için hedef kısa kenar piksel sayısı
_THUMBNAIL_MAX_PX = 256


# ---------------------------------------------------------------------------
# Yanıt modelleri
# ---------------------------------------------------------------------------


class WindowResponse(BaseModel, frozen=True):
    """GET /frames/{frame_id}/window yanıt gövdesi."""

    frame_id: str
    shape: tuple[int, ...]
    dtype: str
    data: list[list[float]] = Field(
        ...,
        description="2-B piksel penceresi; satır-birinci sıralama",
    )


# ---------------------------------------------------------------------------
# Yardımcı fonksiyonlar
# ---------------------------------------------------------------------------


def _window_path(l2_cache_dir: str, frame_id: str) -> Path:
    """Pencere dosyasının tam yolunu döndürür."""
    return Path(l2_cache_dir) / f"{frame_id}_window.npy"


def _thumbnail_path(l2_cache_dir: str, frame_id: str) -> Path:
    """Küçük resim dosyasının tam yolunu döndürür."""
    return Path(l2_cache_dir) / f"{frame_id}_thumbnail.png"


def _load_npy(path: Path) -> np.ndarray:
    """
    NumPy .npy dosyasını okur.

    Raises:
        FileNotFoundError: Dosya mevcut değilse.
        ValueError: Dosya geçerli bir NumPy dizisi değilse.
    """
    if not path.is_file():
        raise FileNotFoundError(path)
    try:
        arr = np.load(path, allow_pickle=False)
    except Exception as exc:
        raise ValueError(f"NumPy dosyası okunamadı: {path}") from exc
    return arr


def _array_to_png(arr: np.ndarray, max_side: int = _THUMBNAIL_MAX_PX) -> bytes:
    """
    2-B NumPy dizisini küçültülmüş 8-bit gri tonlamalı PNG baytlarına dönüştürür.

    Dizinin min–max aralığı 0–255 değerine normalize edilir.
    En büyük kenar `max_side` pikseli aşmayacak şekilde yeniden boyutlandırılır.
    """
    # pillow gerektirmeden saf numpy + stdlib ile PNG üretimi
    import struct
    import zlib

    if arr.ndim != 2:
        # Çok kanallıysa ilk kanalı al
        arr = arr[:, :, 0] if arr.ndim == 3 else arr.reshape(arr.shape[0], -1)

    # Normalize et → uint8
    mn, mx = float(arr.min()), float(arr.max())
    if mx > mn:
        norm = ((arr.astype(np.float32) - mn) / (mx - mn) * 255).astype(np.uint8)
    else:
        norm = np.zeros_like(arr, dtype=np.uint8)

    h, w = norm.shape
    # Yeniden boyutlandır
    if max(h, w) > max_side:
        scale = max_side / max(h, w)
        new_h, new_w = max(1, int(h * scale)), max(1, int(w * scale))
        # En yakın komşu örnekleme
        row_idx = (np.arange(new_h) * h / new_h).astype(np.int32)
        col_idx = (np.arange(new_w) * w / new_w).astype(np.int32)
        norm = norm[np.ix_(row_idx, col_idx)]
        h, w = new_h, new_w

    def _png_chunk(chunk_type: bytes, data: bytes) -> bytes:
        length = struct.pack(">I", len(data))
        crc = struct.pack(">I", zlib.crc32(chunk_type + data) & 0xFFFFFFFF)
        return length + chunk_type + data + crc

    # PNG header
    signature = b"\x89PNG\r\n\x1a\n"

    # IHDR
    ihdr_data = struct.pack(">IIBBBBB", w, h, 8, 0, 0, 0, 0)
    ihdr = _png_chunk(b"IHDR", ihdr_data)

    # IDAT: filtrele (her satırın başına 0x00 filtre baytı ekle)
    raw_rows = b"".join(b"\x00" + bytes(norm[y]) for y in range(h))
    idat = _png_chunk(b"IDAT", zlib.compress(raw_rows, level=6))

    # IEND
    iend = _png_chunk(b"IEND", b"")

    return signature + ihdr + idat + iend


# ---------------------------------------------------------------------------
# Uç noktalar
# ---------------------------------------------------------------------------


@router.get(
    "/{frame_id}/window",
    response_model=WindowResponse,
    summary="Piksel penceresi (JSON)",
)
async def get_frame_window(frame_id: str, request: Request) -> WindowResponse:
    """
    Önceden hesaplanmış piksel penceresini JSON olarak döndürür.

    L2_CACHE_DIR/{frame_id}_window.npy dosyasını okur.
    Dosya yoksa 503 döner. Gerçek S3 okuması görev 06-04'te eklenecektir.
    """
    settings = request.app.state.settings
    path = _window_path(settings.l2_cache_dir, frame_id)

    try:
        arr = _load_npy(path)
    except FileNotFoundError:
        logger.warning("Pencere dosyası bulunamadı: %s", path)
        raise HTTPException(
            status_code=503,
            detail=f"Cache not ready: window file missing for frame '{frame_id}'",
        )
    except ValueError as exc:
        logger.error("Pencere dosyası okunamadı (%s): %s", path, exc)
        raise HTTPException(
            status_code=503,
            detail="Cache not ready: window file read error",
        ) from exc

    # 2-B diziye zorla
    if arr.ndim == 1:
        arr = arr.reshape(1, -1)
    elif arr.ndim > 2:
        arr = arr[:, :, 0]

    return WindowResponse(
        frame_id=frame_id,
        shape=tuple(arr.shape),
        dtype=str(arr.dtype),
        data=arr.tolist(),
    )


@router.get(
    "/{frame_id}/thumbnail",
    summary="Küçük resim (PNG)",
    response_class=Response,
    responses={
        200: {"content": {_PNG_CONTENT_TYPE: {}}, "description": "Gri tonlamalı PNG"},
        503: {"description": "Önbellek hazır değil"},
    },
)
async def get_frame_thumbnail(frame_id: str, request: Request) -> Response:
    """
    Önceden hesaplanmış küçük resim PNG dosyasını döndürür.

    Önce L2_CACHE_DIR/{frame_id}_thumbnail.png aranır; yoksa
    _window.npy üzerinden anında türetilir. Her ikisi de yoksa 503 döner.
    """
    settings = request.app.state.settings
    thumb_path = _thumbnail_path(settings.l2_cache_dir, frame_id)

    # 1. Hazır küçük resim varsa doğrudan sun
    if thumb_path.is_file():
        try:
            png_bytes = thumb_path.read_bytes()
            return Response(content=png_bytes, media_type=_PNG_CONTENT_TYPE)
        except OSError as exc:
            logger.warning("Küçük resim dosyası okunamadı (%s): %s", thumb_path, exc)

    # 2. Pencere dosyasından türet
    win_path = _window_path(settings.l2_cache_dir, frame_id)
    try:
        arr = _load_npy(win_path)
    except FileNotFoundError:
        logger.warning("Küçük resim ve pencere dosyası bulunamadı: %s", frame_id)
        raise HTTPException(
            status_code=503,
            detail=f"Cache not ready: thumbnail/window file missing for frame '{frame_id}'",
        )
    except ValueError as exc:
        logger.error("Pencere dosyası okunamadı (thumbnail türetme) (%s): %s", win_path, exc)
        raise HTTPException(
            status_code=503,
            detail="Cache not ready: window file read error",
        ) from exc

    try:
        png_bytes = _array_to_png(arr)
    except Exception as exc:
        logger.error("PNG türetme hatası (frame=%s): %s", frame_id, exc)
        raise HTTPException(
            status_code=500,
            detail="Internal server error: thumbnail generation failed",
        ) from exc

    return Response(content=png_bytes, media_type=_PNG_CONTENT_TYPE)
