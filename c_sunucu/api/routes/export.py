"""
export.py — Kare PNG dışa aktarma uç noktası.

GET /export/frame/{frame_id}/png → işaretleyiciler + ızgara ile PNG

Sorgu parametreleri:
    x0, y0           — piksel penceresi sol üst köşesi (varsayılan: 0)
    width, height    — pencere boyutu (varsayılan: 100)
    grid             — ızgara açık/kapalı (varsayılan: false)
    stretch          — parlaklık dönüşümü: linear | log | asinh (varsayılan: linear)
    markers          — boşlukla ayrılmış "x,y" koordinat çiftleri (opsiyonel)
                       örnek: "50,80 120,30 200,150"
"""
from __future__ import annotations

import logging
import struct
import zlib
from pathlib import Path

import numpy as np
from fastapi import APIRouter, HTTPException, Query, Request, Response

from cache.l0_cache import CacheMiss
from cache.l2_cache import load_window

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/export", tags=["export"])

# PNG içerik türü sabiti
_PNG_CONTENT_TYPE = "image/png"
# Izgara çizgileri arasındaki piksel aralığı
_GRID_SPACING = 10
# Işaretleyici daire yarıçapı (piksel)
_MARKER_RADIUS = 4


# ---------------------------------------------------------------------------
# Stretch (parlaklık dönüşümü) fonksiyonları
# ---------------------------------------------------------------------------


def _stretch_linear(arr: np.ndarray) -> np.ndarray:
    """
    Diziyi [0, 255] aralığına doğrusal olarak normalize eder.

    Sonlu olmayan değerler (NaN, inf) siyah (0) olarak döndürülür.
    Tüm değerler eşitse düz siyah üretilir.

    Args:
        arr: float32 2-B numpy dizisi (yükseklik × genişlik).

    Returns:
        uint8 (0–255) 2-B numpy dizisi.
    """
    finite_mask = np.isfinite(arr)
    if not finite_mask.any():
        return np.zeros(arr.shape, dtype=np.uint8)

    lo = float(arr[finite_mask].min())
    hi = float(arr[finite_mask].max())

    if hi == lo:
        return np.zeros(arr.shape, dtype=np.uint8)

    normed = (arr - lo) / (hi - lo)
    normed = np.clip(np.where(finite_mask, normed, 0.0), 0.0, 1.0)
    return (normed * 255).astype(np.uint8)


def _stretch_log(arr: np.ndarray) -> np.ndarray:
    """
    Logaritmik parlaklık dönüşümü uygular, ardından doğrusal normalize eder.

    Minimum değere göre kaydırma yapılarak tüm değerler ≥ 1 yapılır;
    böylece log1p uygulanabilir hale gelir.

    Args:
        arr: float32 2-B numpy dizisi.

    Returns:
        uint8 (0–255) 2-B numpy dizisi.
    """
    finite_mask = np.isfinite(arr)
    min_val = float(arr[finite_mask].min()) if finite_mask.any() else 0.0
    # Minimum 1.0'a kaydır, negatif/sıfır değerleri kırp
    shifted = np.where(finite_mask, arr - min_val + 1.0, 1.0)
    logged = np.log1p(np.clip(shifted, 0.0, None))
    return _stretch_linear(logged)


def _stretch_asinh(arr: np.ndarray) -> np.ndarray:
    """
    Ters hiperbolik sinüs (arcsinh) dönüşümü uygular, ardından normalize eder.

    Yıldız benzeri kaynakların geniş dinamik aralıklarda görselleştirilmesi
    için uygundur; parlak kaynakları bastırmadan soluk kaynakları da gösterir.

    Args:
        arr: float32 2-B numpy dizisi.

    Returns:
        uint8 (0–255) 2-B numpy dizisi.
    """
    return _stretch_linear(np.arcsinh(arr))


# Stretch adından fonksiyona eşleme tablosu
_STRETCH_FN = {
    "linear": _stretch_linear,
    "log": _stretch_log,
    "asinh": _stretch_asinh,
}


# ---------------------------------------------------------------------------
# Çizim yardımcıları (RGBA dizisi üzerinde in-place)
# ---------------------------------------------------------------------------


def _draw_grid(rgba: np.ndarray, spacing: int = _GRID_SPACING) -> None:
    """
    RGBA dizisi üzerine piksel ızgarası çizer (in-place).

    Her ``spacing`` pikselde bir beyaz (%20 saydamlık) yatay ve dikey
    çizgi ekler.  Karıştırma formülü: out = 0.20 × beyaz + 0.80 × mevcut.

    Args:
        rgba:    uint8 (H, W, 4) RGBA numpy dizisi — değiştirilir.
        spacing: Izgara çizgileri arasındaki piksel aralığı.
    """
    height, width = rgba.shape[:2]
    alpha = 0.20

    # Yatay çizgiler
    for y in range(0, height, spacing):
        rgb = rgba[y, :, :3].astype(np.float32)
        rgba[y, :, :3] = (alpha * 255.0 + (1.0 - alpha) * rgb).astype(np.uint8)

    # Dikey çizgiler
    for x in range(0, width, spacing):
        rgb = rgba[:, x, :3].astype(np.float32)
        rgba[:, x, :3] = (alpha * 255.0 + (1.0 - alpha) * rgb).astype(np.uint8)


def _draw_markers(
    rgba: np.ndarray,
    markers: list[tuple[int, int]],
    radius: int = _MARKER_RADIUS,
) -> None:
    """
    RGBA dizisi üzerine dolu kırmızı daire işaretleyiciler çizer (in-place).

    İşaretleyici merkezi görüntü dışında olsa bile görüntü sınırları içinde
    kalan pikseller çizilir (kırpma).

    Args:
        rgba:    uint8 (H, W, 4) RGBA numpy dizisi — değiştirilir.
        markers: (x, y) piksel koordinat çiftlerinin listesi.
        radius:  Daire yarıçapı (piksel).
    """
    height, width = rgba.shape[:2]

    for cx, cy in markers:
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx * dx + dy * dy > radius * radius:
                    continue
                px = cx + dx
                py = cy + dy
                if 0 <= px < width and 0 <= py < height:
                    rgba[py, px, 0] = 220  # R — kırmızı
                    rgba[py, px, 1] = 30   # G
                    rgba[py, px, 2] = 30   # B
                    rgba[py, px, 3] = 255  # tam opak


# ---------------------------------------------------------------------------
# Minimal PNG kodlayıcı (stdlib: struct + zlib; PIL gerekmez)
# ---------------------------------------------------------------------------


def _png_chunk(chunk_type: bytes, data: bytes) -> bytes:
    """
    Tek bir PNG chunk'ı (blok) oluşturur.

    PNG chunk biçimi: uzunluk (4B) + tür (4B) + veri + CRC (4B).

    Args:
        chunk_type: 4 baytlık chunk türü (örn. b"IHDR").
        data:       Chunk veri içeriği.

    Returns:
        Tam chunk bayt dizisi.
    """
    length = struct.pack(">I", len(data))
    crc = struct.pack(">I", zlib.crc32(chunk_type + data) & 0xFFFFFFFF)
    return length + chunk_type + data + crc


def _encode_png(rgba: np.ndarray) -> bytes:
    """
    RGBA numpy dizisini (H, W, 4) standart kütüphane ile geçerli PNG baytlarına dönüştürür.

    Her satıra filtre baytı (0x00 = None filter) eklendikten sonra
    tüm satırlar zlib ile sıkıştırılır.

    Desteklenen renk türü: RGBA (8 bit/kanal, color_type=6).

    Args:
        rgba: uint8 (H, W, 4) RGBA numpy dizisi.

    Returns:
        Geçerli PNG dosyası bayt dizisi.
    """
    height, width = rgba.shape[:2]

    # IHDR: genişlik(4B) + yükseklik(4B) + bit_derinliği(1) + renk_türü(1) +
    #        sıkıştırma(1) + filtre(1) + interlace(1) = 13 bayt
    ihdr_data = struct.pack(">II", width, height) + bytes([8, 6, 0, 0, 0])

    # Filtresiz satırlar: her satır başına 0x00 filtre baytı ekle
    rows: list[bytes] = []
    for row in rgba.astype(np.uint8):
        rows.append(b"\x00" + row.tobytes())
    compressed = zlib.compress(b"".join(rows), level=6)

    return (
        b"\x89PNG\r\n\x1a\n"              # PNG imzası (8 bayt)
        + _png_chunk(b"IHDR", ihdr_data)
        + _png_chunk(b"IDAT", compressed)
        + _png_chunk(b"IEND", b"")
    )


# ---------------------------------------------------------------------------
# İşaretleyici dize ayrıştırıcı
# ---------------------------------------------------------------------------


def _parse_markers(raw: str) -> list[tuple[int, int]]:
    """
    "x1,y1 x2,y2 ..." biçimindeki işaretleyici dizesini koordinat listesine dönüştürür.

    Her token "x,y" biçimindedir; tokenlar boşlukla ayrılır.
    Geçersiz veya eksik tokenlar sessizce atlanır.

    Örnek: ``"50,80 120,30"`` → ``[(50, 80), (120, 30)]``

    Args:
        raw: Kullanıcıdan gelen ham koordinat dizesi.

    Returns:
        (x, y) int çiftlerinin listesi; geçersiz giriş için boş liste.
    """
    if not raw.strip():
        return []

    result: list[tuple[int, int]] = []
    for token in raw.split():
        parts = token.split(",")
        if len(parts) != 2:
            logger.debug("Geçersiz işaretleyici token atlandı: %r", token)
            continue
        try:
            x = int(parts[0])
            y = int(parts[1])
            result.append((x, y))
        except ValueError:
            logger.debug("Sayıya dönüştürülemeyen işaretleyici atlandı: %r", token)

    return result


# ---------------------------------------------------------------------------
# Route tanımı
# ---------------------------------------------------------------------------


@router.get(
    "/frame/{frame_id}/png",
    response_class=Response,
    responses={
        200: {
            "content": {_PNG_CONTENT_TYPE: {}},
            "description": "Izgara ve işaretleyicilerle PNG görüntüsü",
        },
        503: {"description": "L2 önbelleği henüz hazır değil"},
        422: {"description": "Geçersiz sorgu parametresi"},
    },
    summary="Kare penceresini PNG olarak dışa aktar",
    description=(
        "Belirtilen frame_id için L2 önbellekten piksel penceresi okur, "
        "parlaklık dönüşümü (linear/log/asinh) uygular ve isteğe bağlı "
        "piksel ızgarası ile kırmızı daire işaretleyicilerle PNG döndürür. "
        "Görüntü PIL gerektirmeden yalnızca standart kütüphane (struct + zlib) ile kodlanır."
    ),
)
async def export_frame_png(
    frame_id: str,
    request: Request,
    x0: int = Query(
        default=0,
        ge=0,
        description="Pencerenin sol sütunu, 0 tabanlı piksel.",
    ),
    y0: int = Query(
        default=0,
        ge=0,
        description="Pencerenin üst satırı, 0 tabanlı piksel.",
    ),
    width: int = Query(
        default=100,
        ge=1,
        le=2048,
        description="Pencere genişliği (piksel); 1–2048 arası.",
    ),
    height: int = Query(
        default=100,
        ge=1,
        le=2048,
        description="Pencere yüksekliği (piksel); 1–2048 arası.",
    ),
    grid: bool = Query(
        default=False,
        description="True ise her 10 pikselde bir beyaz ızgara çizgileri eklenir.",
    ),
    stretch: str = Query(
        default="linear",
        pattern="^(linear|log|asinh)$",
        description="Parlaklık dönüşümü: linear | log | asinh.",
    ),
    markers: str = Query(
        default="",
        description=(
            'Boşlukla ayrılmış "x,y" koordinat çiftleri. '
            'Örnek: "50,80 120,30 200,150"'
        ),
    ),
) -> Response:
    """
    Belirtilen kare için işlenmiş PNG görüntüsü oluşturur ve döndürür.

    İşlem adımları:
      1. L2 önbellekten float32 piksel penceresi okunur.
      2. Seçilen stretch fonksiyonu ile uint8'e dönüştürülür.
      3. Gri görüntü RGBA'ya çevrilir (tam opak).
      4. İstek üzerine piksel ızgarası eklenir (beyaz, %20 saydamlık).
      5. İstek üzerine kırmızı daire işaretleyiciler eklenir.
      6. PIL olmadan stdlib (struct + zlib) ile PNG kodlanır ve döndürülür.

    Önbellek hazır değilse HTTP 503 döner.

    Args:
        frame_id: SPHEREx kare tanımlayıcısı.
        request:  FastAPI istek nesnesi; ``settings`` için kullanılır.
        x0:       Pencerenin sol sütunu.
        y0:       Pencerenin üst satırı.
        width:    Pencere genişliği.
        height:   Pencere yüksekliği.
        grid:     True ise ızgara çizgileri eklenir.
        stretch:  Parlaklık dönüşüm türü.
        markers:  Boşlukla ayrılmış "x,y" işaretleyici koordinatları.

    Returns:
        ``image/png`` içerik türünde HTTP 200 yanıtı.

    Raises:
        HTTPException 503: L2 önbelleğinde istenen pencere bulunamazsa.
    """
    settings = request.app.state.settings
    cache_dir = Path(settings.l2_cache_dir)

    # --- L2 önbellekten pencere yükle ---
    try:
        window_data = await load_window(
            frame_id=frame_id,
            x0=x0,
            y0=y0,
            width=width,
            height=height,
            cache_dir=cache_dir,
        )
    except CacheMiss:
        logger.warning(
            "L2 önbellek hazır değil: frame=%r pencere=(%d,%d,%d,%d)",
            frame_id,
            x0,
            y0,
            width,
            height,
        )
        raise HTTPException(
            status_code=503,
            detail=(
                f"L2 önbelleği henüz hazır değil: frame_id={frame_id!r} "
                f"pencere=({x0},{y0},{width},{height}). "
                "Lütfen daha sonra tekrar deneyin."
            ),
        )

    # --- Stretch uygula: float32 → uint8 ---
    stretch_fn = _STRETCH_FN.get(stretch, _stretch_linear)
    gray = stretch_fn(window_data.image)  # (H, W) uint8

    # --- Gri → RGBA (tam opak) ---
    rgba = np.stack(
        [gray, gray, gray, np.full(gray.shape, 255, dtype=np.uint8)],
        axis=-1,
    )  # (H, W, 4) uint8

    # --- Izgara çiz ---
    if grid:
        _draw_grid(rgba)

    # --- İşaretleyiciler çiz ---
    if markers:
        marker_list = _parse_markers(markers)
        if marker_list:
            _draw_markers(rgba, marker_list)

    # --- PNG kodla ve döndür ---
    png_bytes = _encode_png(rgba)

    logger.debug(
        "PNG dışa aktarıldı: frame=%r (%d,%d,%d,%d) stretch=%s grid=%s "
        "işaretleyici=%d boyut=%dB",
        frame_id,
        x0,
        y0,
        width,
        height,
        stretch,
        grid,
        len(_parse_markers(markers)) if markers else 0,
        len(png_bytes),
    )

    return Response(content=png_bytes, media_type=_PNG_CONTENT_TYPE)
