"""
fits_export.py — Pencere verisini FITS olarak dışa aktarma.

GET /export/frame/{frame_id}/fits → FITS dosyası döndürür

Sorgu parametreleri:
- x0, y0           : Pencerenin sol üst köşesi (0 tabanlı piksel, zorunlu)
- width=100        : Pencere genişliği (piksel)
- height=100       : Pencere yüksekliği (piksel)
- hdus=image,flags,variance,zodi  : Dahil edilecek HDU'lar (virgülle ayrılmış)

FITS yapısı:
- PRIMARY : Boş verili başlık (kare meta verisini taşır)
- IMAGE   : float32 2D dizi — ışık akısı/foton sayısı
- FLAGS   : int32   2D dizi — kalite bayrakları (opsiyonel)
- VARIANCE: float32 2D dizi — varyans düzlemi (opsiyonel)
- ZODI    : float32 2D dizi — zodyak ışığı modeli (opsiyonel)

Hata kodları:
- 400 : Geçersiz sorgu parametresi
- 503 : L2 önbellek girişi mevcut değil
- 500 : İç sunucu hatası (FITS oluşturma başarısız)
"""
from __future__ import annotations

import asyncio
import io
import logging
from pathlib import Path
from typing import Annotated

import numpy as np
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import StreamingResponse

from cache.l0_cache import CacheMiss
from cache.l2_cache import load_window

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/export", tags=["export"])

# Desteklenen HDU adları (küçük harf → büyük harf eşlemesi)
_SUPPORTED_HDUS: dict[str, str] = {
    "image": "IMAGE",
    "flags": "FLAGS",
    "variance": "VARIANCE",
    "zodi": "ZODI",
}

# Varsayılan HDU listesi
_DEFAULT_HDUS = "image,flags,variance,zodi"


# ---------------------------------------------------------------------------
# Yardımcı fonksiyonlar
# ---------------------------------------------------------------------------


def _parse_hdu_names(hdus_param: str) -> list[str]:
    """
    Virgülle ayrılmış HDU adı dizesini ayrıştırır ve doğrular.

    Args:
        hdus_param: "image,flags,variance,zodi" gibi virgülle ayrılmış dize.

    Returns:
        Küçük harfe normalleştirilmiş geçerli HDU adlarının listesi.

    Raises:
        HTTPException: Geçersiz bir HDU adı bulunursa 400 döner.
    """
    names = [name.strip().lower() for name in hdus_param.split(",") if name.strip()]
    if not names:
        raise HTTPException(
            status_code=400,
            detail="'hdus' parametresi en az bir HDU adı içermelidir.",
        )
    invalid = [n for n in names if n not in _SUPPORTED_HDUS]
    if invalid:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Geçersiz HDU adları: {invalid!r}. "
                f"Desteklenen değerler: {list(_SUPPORTED_HDUS)}"
            ),
        )
    return names


def _build_fits_bytes(
    frame_id: str,
    x0: int,
    y0: int,
    image: np.ndarray,
    flags: np.ndarray,
    variance: np.ndarray,
    zodi: np.ndarray,
    meta: dict,
    requested_hdus: list[str],
) -> bytes:
    """
    İstenen HDU'lardan FITS ikili içeriği oluşturur (senkron, executor için).

    PRIMARY HDU boş veri taşır; meta bilgilerini başlıkta saklar.
    Her ek HDU ImageHDU olarak eklenir.

    Args:
        frame_id      : SPHEREx kare tanımlayıcısı (başlık kaydı).
        x0, y0        : Pencerenin sol üst koordinatları.
        image         : float32 2D dizi.
        flags         : int32   2D dizi.
        variance      : float32 2D dizi.
        zodi          : float32 2D dizi.
        meta          : Kare meta sözlüğü (MJD, dedektör vb.).
        requested_hdus: Dahil edilecek HDU adları (küçük harf).

    Returns:
        FITS içeriğini temsil eden bayt dizisi.
    """
    # astropy içe aktarımını geciktir; başlangıç maliyetini azaltır
    from astropy.io import fits  # type: ignore[import-untyped]

    # PRIMARY HDU — boş veri, meta başlıkları taşır
    primary_hdu = fits.PrimaryHDU()
    primary_hdu.header["FRAME_ID"] = (frame_id, "SPHEREx kare tanımlayıcısı")
    primary_hdu.header["WIN_X0"] = (x0, "Pencere sol kenarı (piksel, 0-tabanlı)")
    primary_hdu.header["WIN_Y0"] = (y0, "Pencere üst kenarı (piksel, 0-tabanlı)")
    primary_hdu.header["WIN_W"] = (image.shape[1], "Pencere genişliği (piksel)")
    primary_hdu.header["WIN_H"] = (image.shape[0], "Pencere yüksekliği (piksel)")

    # Meta sözlüğünden ek başlık kayıtları ekle (güvenli alt küme)
    _safe_meta_keys = {
        "mjd_avg": ("MJD_AVG", "Ortalama modifiye Julian tarihi"),
        "detector": ("DETECTOR", "Dedektör kodu"),
        "pass_index": ("PASS_IDX", "Geçiş dizini"),
        "sps_epa": ("SPS_EPA", "SPS konumu (açısal mesafe)"),
    }
    for meta_key, (fits_key, comment) in _safe_meta_keys.items():
        value = meta.get(meta_key)
        if value is not None:
            try:
                primary_hdu.header[fits_key] = (value, comment)
            except Exception:  # noqa: BLE001
                # Geçersiz değer türlerini sessizce atla
                pass

    hdu_list = fits.HDUList([primary_hdu])

    # İstenen HDU'ları sırayla ekle
    hdu_data_map: dict[str, tuple[np.ndarray, str]] = {
        "image": (image.astype(np.float32), "Işık akısı/foton sayısı (float32)"),
        "flags": (flags.astype(np.int32), "Kalite bayrakları (int32)"),
        "variance": (variance.astype(np.float32), "Varyans düzlemi (float32)"),
        "zodi": (zodi.astype(np.float32), "Zodyak ışığı modeli (float32)"),
    }

    for hdu_name in requested_hdus:
        arr, btype_comment = hdu_data_map[hdu_name]
        ext_name = _SUPPORTED_HDUS[hdu_name]
        image_hdu = fits.ImageHDU(data=arr, name=ext_name)
        image_hdu.header["BTYPE"] = (ext_name, btype_comment)
        hdu_list.append(image_hdu)

    # io.BytesIO buffer'a yaz
    buf = io.BytesIO()
    hdu_list.writeto(buf, overwrite=True)
    buf.seek(0)
    return buf.read()


# ---------------------------------------------------------------------------
# Uç nokta
# ---------------------------------------------------------------------------


@router.get(
    "/frame/{frame_id}/fits",
    summary="Pencere verisini FITS olarak dışa aktar",
    response_class=StreamingResponse,
    responses={
        200: {
            "content": {"application/fits": {}},
            "description": "Çok-HDU'lu FITS dosyası",
        },
        400: {"description": "Geçersiz sorgu parametresi"},
        503: {"description": "L2 önbellek hazır değil (pencere dosyası bulunamadı)"},
        500: {"description": "İç sunucu hatası"},
    },
)
async def export_frame_fits(
    frame_id: str,
    request: Request,
    x0: Annotated[int, Query(ge=0, description="Pencerenin sol kenarı (piksel, 0-tabanlı)")],
    y0: Annotated[int, Query(ge=0, description="Pencerenin üst kenarı (piksel, 0-tabanlı)")],
    width: Annotated[int, Query(ge=1, le=4096, description="Pencere genişliği (piksel)")] = 100,
    height: Annotated[int, Query(ge=1, le=4096, description="Pencere yüksekliği (piksel)")] = 100,
    hdus: Annotated[
        str,
        Query(description="Virgülle ayrılmış HDU adları: image,flags,variance,zodi"),
    ] = _DEFAULT_HDUS,
) -> StreamingResponse:
    """
    Belirtilen pencere için L2 önbellekten veri okur ve FITS formatında döndürür.

    İstenen HDU'lar FITS dosyasına eklenir; istenmeyenler atlanır.
    Pencere L2 önbellekte yoksa 503 hatası döner.

    Args:
        frame_id : SPHEREx kare tanımlayıcısı.
        request  : FastAPI istek nesnesi (settings erişimi için).
        x0       : Pencerenin sol kenarı (piksel, 0-tabanlı).
        y0       : Pencerenin üst kenarı (piksel, 0-tabanlı).
        width    : Pencere genişliği (1–4096 piksel arası).
        height   : Pencere yüksekliği (1–4096 piksel arası).
        hdus     : Dahil edilecek HDU adları (virgülle ayrılmış).

    Returns:
        StreamingResponse: FITS ikili içeriği, indirilebilir dosya olarak.

    Raises:
        HTTPException 400: Geçersiz 'hdus' parametresi.
        HTTPException 503: Pencere L2 önbellekte mevcut değil.
        HTTPException 500: FITS oluşturma başarısız.
    """
    # HDU adlarını ayrıştır ve doğrula
    requested_hdus = _parse_hdu_names(hdus)

    # L2 önbellek dizinini ayarlardan al
    settings = request.app.state.settings
    cache_dir = Path(settings.l2_cache_dir)

    # L2 önbellekten pencere verisini yükle (asenkron)
    try:
        window = await load_window(
            frame_id=frame_id,
            x0=x0,
            y0=y0,
            width=width,
            height=height,
            cache_dir=cache_dir,
        )
    except CacheMiss:
        logger.warning(
            "L2 cache miss: frame=%r window=(%d,%d,%d,%d)",
            frame_id, x0, y0, width, height,
        )
        raise HTTPException(
            status_code=503,
            detail=(
                f"Cache not ready: pencere mevcut değil — "
                f"frame_id={frame_id!r}, window=({x0},{y0},{width},{height})"
            ),
        )

    # FITS içeriğini executor'da oluştur (bloke edici işlem)
    loop = asyncio.get_running_loop()
    try:
        fits_bytes = await loop.run_in_executor(
            None,
            _build_fits_bytes,
            frame_id,
            x0,
            y0,
            window.image,
            window.flags,
            window.variance,
            window.zodi,
            window.meta,
            requested_hdus,
        )
    except Exception as exc:
        logger.error(
            "FITS oluşturma hatası: frame=%r window=(%d,%d,%d,%d): %s",
            frame_id, x0, y0, width, height, exc,
        )
        raise HTTPException(
            status_code=500,
            detail="Internal server error: FITS dosyası oluşturulamadı.",
        ) from exc

    # İndirilebilir dosya adı: frame_id + pencere koordinatları
    filename = f"{frame_id}_{x0}_{y0}_{width}x{height}.fits"

    logger.info(
        "FITS dışa aktarma: frame=%r window=(%d,%d,%d,%d) hdus=%s size=%d B",
        frame_id, x0, y0, width, height, requested_hdus, len(fits_bytes),
    )

    return StreamingResponse(
        content=io.BytesIO(fits_bytes),
        media_type="application/fits",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Length": str(len(fits_bytes)),
        },
    )
