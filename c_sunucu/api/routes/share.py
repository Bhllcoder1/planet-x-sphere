"""
share.py — URL paylaşım ve dışa aktarma uç noktaları.

GET  /share          → mevcut görüntüleyici durumu URL'si
POST /share/validate → URL parametrelerini doğrula
GET  /share/wiseview → WiseView URL'sini SPHEREx şemasına çevir
"""
from __future__ import annotations

import logging
from typing import Optional
from urllib.parse import urlencode, urlparse

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from api.wiseview_compat import (
    SPHERExParams,
    convert_wiseview_to_spherex,
    parse_wiseview_url,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/share", tags=["share"])

# Geçerli parametre değerleri
VALID_TARGETS: frozenset[str] = frozenset(
    {"barnard", "eps_indi_b", "wise0855", "rwaur", "rdra"}
)
VALID_VIEWS: frozenset[str] = frozenset({"n", "rk", "s"})
VALID_CLIPS: frozenset[str] = frozenset({"fixed", "percent", "adapt", "zscale"})
VALID_HDUS: frozenset[str] = frozenset({"image", "flags", "variance", "zodi"})
VALID_STRETCHES: frozenset[str] = frozenset({"linear", "log", "asinh"})


# ---------------------------------------------------------------------------
# Yanıt ve istek modelleri
# ---------------------------------------------------------------------------


class ShareUrlResponse(BaseModel, frozen=True):
    """GET /share yanıt gövdesi."""

    url: str
    valid: bool


class ValidateRequest(BaseModel, frozen=True):
    """
    POST /share/validate istek gövdesi.

    Tüm alanlar isteğe bağlıdır; yalnızca belirtilen alanlar doğrulanır.
    'pass' Python anahtar sözcüğü olduğundan model alanı 'pass_' adını kullanır.
    """

    target: Optional[str] = None
    frame: Optional[str] = None
    x: Optional[int] = None
    y: Optional[int] = None
    w: Optional[int] = None
    h: Optional[int] = None
    view: Optional[str] = None
    clip: Optional[str] = None
    clip_lo: Optional[float] = None
    clip_hi: Optional[float] = None
    stretch: Optional[str] = None
    blink: Optional[bool] = None
    blink_ms: Optional[int] = None
    zodi: Optional[bool] = None
    hdu: Optional[str] = None
    pass_: Optional[int] = None
    det: Optional[str] = None


class ValidateResponse(BaseModel, frozen=True):
    """POST /share/validate yanıt gövdesi."""

    valid: bool
    errors: list[str]


class WiseViewConvertResponse(BaseModel, frozen=True):
    """GET /share/wiseview yanıt gövdesi."""

    url: str
    target: str
    valid: bool


# ---------------------------------------------------------------------------
# Yardımcı fonksiyonlar
# ---------------------------------------------------------------------------


def _build_query_string(params: dict[str, object]) -> str:
    """
    Parametre sözlüğünden URL sorgu dizesi oluşturur.

    ``None`` değerli parametreler hariç tutulur.
    ``bool`` değerleri ``'true'`` / ``'false'`` dizesine çevrilir.

    Parametreler
    ------------
    params : dict[str, object]
        Parametre adı → değer eşlemesi.

    Dönüş
    -----
    str
        ``'?'`` ile başlayan sorgu dizesi; parametre yoksa boş dize döner.
    """
    filtered: dict[str, str] = {}
    for key, value in params.items():
        if value is None:
            continue
        if isinstance(value, bool):
            filtered[key] = "true" if value else "false"
        else:
            filtered[key] = str(value)

    if not filtered:
        return ""
    return "?" + urlencode(filtered)


def _validate_params(
    target: Optional[str],
    view: Optional[str],
    clip: Optional[str],
    hdu: Optional[str],
    stretch: Optional[str],
    clip_lo: Optional[float],
    clip_hi: Optional[float],
    w: Optional[int],
    h: Optional[int],
    blink_ms: Optional[int],
) -> list[str]:
    """
    Görüntüleyici parametre değerlerini doğrular.

    Yalnızca ``None`` olmayan alanlar denetlenir. Hata mesajları Türkçe döndürülür.

    Parametreler
    ------------
    target : str veya None
        Hedef kimliği; geçerli değerler ``VALID_TARGETS`` kümesinde tanımlıdır.
    view : str veya None
        Görüntü modu; geçerli değerler ``VALID_VIEWS`` kümesinde tanımlıdır.
    clip : str veya None
        Kırpma modu; geçerli değerler ``VALID_CLIPS`` kümesinde tanımlıdır.
    hdu : str veya None
        HDU katmanı; geçerli değerler ``VALID_HDUS`` kümesinde tanımlıdır.
    stretch : str veya None
        Renk germe modu; geçerli değerler ``VALID_STRETCHES`` kümesinde tanımlıdır.
    clip_lo : float veya None
        Alt kırpma sınırı; ``clip='fixed'`` iken zorunludur.
    clip_hi : float veya None
        Üst kırpma sınırı; ``clip='fixed'`` iken zorunludur.
    w : int veya None
        Pencere genişliği (piksel); sıfırdan büyük olmalıdır.
    h : int veya None
        Pencere yüksekliği (piksel); sıfırdan büyük olmalıdır.
    blink_ms : int veya None
        Blink hızı (milisaniye); sıfırdan büyük olmalıdır.

    Dönüş
    -----
    list[str]
        Hata mesajları listesi. Boş liste tüm parametrelerin geçerli olduğu anlamına gelir.
    """
    errors: list[str] = []

    if target is not None and target not in VALID_TARGETS:
        errors.append(
            f"Geçersiz 'target' değeri: '{target}'. "
            f"Geçerli değerler: {sorted(VALID_TARGETS)}"
        )

    if view is not None and view not in VALID_VIEWS:
        errors.append(
            f"Geçersiz 'view' değeri: '{view}'. "
            f"Geçerli değerler: {sorted(VALID_VIEWS)}"
        )

    if clip is not None and clip not in VALID_CLIPS:
        errors.append(
            f"Geçersiz 'clip' değeri: '{clip}'. "
            f"Geçerli değerler: {sorted(VALID_CLIPS)}"
        )

    if hdu is not None and hdu not in VALID_HDUS:
        errors.append(
            f"Geçersiz 'hdu' değeri: '{hdu}'. "
            f"Geçerli değerler: {sorted(VALID_HDUS)}"
        )

    if stretch is not None and stretch not in VALID_STRETCHES:
        errors.append(
            f"Geçersiz 'stretch' değeri: '{stretch}'. "
            f"Geçerli değerler: {sorted(VALID_STRETCHES)}"
        )

    # clip=fixed için clip_lo ve clip_hi birlikte zorunludur
    if clip == "fixed":
        if clip_lo is None or clip_hi is None:
            errors.append(
                "'clip=fixed' kullanıldığında 'clip_lo' ve 'clip_hi' "
                "birlikte sağlanmalıdır."
            )
        elif clip_lo >= clip_hi:
            errors.append(
                f"'clip_lo' ({clip_lo}) değeri 'clip_hi' ({clip_hi}) değerinden "
                "küçük olmalıdır."
            )

    if w is not None and w <= 0:
        errors.append(f"'w' sıfırdan büyük olmalıdır; alınan değer: {w}")

    if h is not None and h <= 0:
        errors.append(f"'h' sıfırdan büyük olmalıdır; alınan değer: {h}")

    if blink_ms is not None and blink_ms <= 0:
        errors.append(f"'blink_ms' sıfırdan büyük olmalıdır; alınan değer: {blink_ms}")

    return errors


def _spherex_params_to_query(sp: SPHERExParams) -> str:
    """
    ``SPHERExParams`` nesnesini URL sorgu dizesine dönüştürür.

    ``clip_lo`` ve ``clip_hi`` yalnızca ``None`` değilse eklenir.

    Parametreler
    ------------
    sp : SPHERExParams
        Dönüştürülecek SPHEREx parametreleri.

    Dönüş
    -----
    str
        ``'?'`` ile başlayan sorgu dizesi.
    """
    params: dict[str, object] = {
        "target": sp.target,
        "x": sp.x,
        "y": sp.y,
        "w": sp.w,
        "h": sp.h,
        "clip": sp.clip,
        "hdu": sp.hdu,
        "clip_lo": sp.clip_lo,
        "clip_hi": sp.clip_hi,
    }
    return _build_query_string(params)


def _extract_query_string(wv_url: str) -> str:
    """
    Tam URL veya ham sorgu dizesinden yalnızca sorgu bölümünü çıkarır.

    ``://`` veya ``//`` içeren girdi tam URL olarak değerlendirilir ve
    ``urllib.parse.urlparse`` ile ayrıştırılır. Aksi halde girdi olduğu
    gibi döner; baştaki ``'?'`` varsa kaldırılır.

    Parametreler
    ------------
    wv_url : str
        WiseView tam URL veya sorgu dizesi.

    Dönüş
    -----
    str
        Sorgu dizesi (``'?'`` işareti olmadan).
    """
    if "://" in wv_url or wv_url.startswith("//"):
        parsed = urlparse(wv_url)
        return parsed.query
    return wv_url.lstrip("?")


# ---------------------------------------------------------------------------
# Uç noktalar
# ---------------------------------------------------------------------------


@router.get(
    "",
    response_model=ShareUrlResponse,
    summary="Paylaşılabilir görüntüleyici URL'si oluşturur",
)
async def get_share_url(
    target: Optional[str] = Query(
        default=None,
        description="Hedef kimliği: barnard, eps_indi_b, wise0855, rwaur, rdra",
    ),
    frame: Optional[str] = Query(
        default=None,
        description="Kare kimliği; boşsa ilk kullanılabilir kare gösterilir",
    ),
    x: Optional[int] = Query(
        default=None,
        description="Pencere sol üst köşesi X koordinatı (piksel)",
    ),
    y: Optional[int] = Query(
        default=None,
        description="Pencere sol üst köşesi Y koordinatı (piksel)",
    ),
    w: Optional[int] = Query(default=None, description="Pencere genişliği (piksel)"),
    h: Optional[int] = Query(default=None, description="Pencere yüksekliği (piksel)"),
    view: Optional[str] = Query(
        default=None,
        description="Görüntü modu: n (N-shift), rk (R-k raster), s (Stack)",
    ),
    clip: Optional[str] = Query(
        default=None,
        description="Kırpma modu: fixed, percent, adapt, zscale",
    ),
    clip_lo: Optional[float] = Query(
        default=None,
        description="Alt kırpma sınırı; yalnızca clip=fixed ile geçerlidir",
    ),
    clip_hi: Optional[float] = Query(
        default=None,
        description="Üst kırpma sınırı; yalnızca clip=fixed ile geçerlidir",
    ),
    stretch: Optional[str] = Query(
        default=None,
        description="Renk germe: linear, log, asinh",
    ),
    blink: Optional[bool] = Query(
        default=None,
        description="Blink modunu açar (true) veya kapatır (false)",
    ),
    blink_ms: Optional[int] = Query(
        default=None,
        description="Blink hızı (milisaniye); blink=true olmadan görmezden gelinir",
    ),
    zodi: Optional[bool] = Query(
        default=None,
        description="ZODI çıkarma: true = çıkarma açık, false = ham veri",
    ),
    hdu: Optional[str] = Query(
        default=None,
        description="Gösterilen HDU katmanı: image, flags, variance, zodi",
    ),
    pass_no: Optional[int] = Query(
        default=None,
        alias="pass",
        description="Geçiş filtresi; boşsa tüm geçişler dahil edilir",
    ),
    det: Optional[str] = Query(
        default=None,
        description="Dedektör filtresi: D1-D6; boşsa tüm dedektörler dahil edilir",
    ),
) -> ShareUrlResponse:
    """
    Sorgu parametrelerinden paylaşılabilir görüntüleyici URL'si oluşturur.

    ``None`` olan parametreler URL'ye dahil edilmez. Parametreler doğrulanır;
    geçersiz değer varsa ``valid=False`` döner, URL ise yine de oluşturulur.
    Bu sayede istemci geçersiz durumu kullanıcıya bildirebilir.
    """
    validation_errors = _validate_params(
        target=target,
        view=view,
        clip=clip,
        hdu=hdu,
        stretch=stretch,
        clip_lo=clip_lo,
        clip_hi=clip_hi,
        w=w,
        h=h,
        blink_ms=blink_ms,
    )
    is_valid = len(validation_errors) == 0

    param_map: dict[str, object] = {
        "target": target,
        "frame": frame,
        "x": x,
        "y": y,
        "w": w,
        "h": h,
        "view": view,
        "clip": clip,
        "clip_lo": clip_lo,
        "clip_hi": clip_hi,
        "stretch": stretch,
        "blink": blink,
        "blink_ms": blink_ms,
        "zodi": zodi,
        "hdu": hdu,
        "pass": pass_no,
        "det": det,
    }

    url = _build_query_string(param_map)

    logger.debug(
        "Paylaşım URL'si oluşturuldu: %s (geçerli=%s, hata_sayısı=%d)",
        url,
        is_valid,
        len(validation_errors),
    )

    return ShareUrlResponse(url=url, valid=is_valid)


@router.post(
    "/validate",
    response_model=ValidateResponse,
    summary="Görüntüleyici URL parametrelerini doğrular",
)
async def validate_share_params(body: ValidateRequest) -> ValidateResponse:
    """
    İstek gövdesindeki görüntüleyici parametrelerini doğrular.

    Tüm alanlar isteğe bağlıdır; yalnızca belirtilen alanlar denetlenir.
    Geçersiz değer tespit edilirse ``422 Unprocessable Entity`` ile
    hata mesajları listesi döner. Tüm alanlar geçerliyse ``valid=true``
    ve boş ``errors`` listesi içeren yanıt döner.
    """
    errors = _validate_params(
        target=body.target,
        view=body.view,
        clip=body.clip,
        hdu=body.hdu,
        stretch=body.stretch,
        clip_lo=body.clip_lo,
        clip_hi=body.clip_hi,
        w=body.w,
        h=body.h,
        blink_ms=body.blink_ms,
    )

    if errors:
        logger.info(
            "Parametre doğrulama başarısız: %d hata — %s",
            len(errors),
            errors,
        )
        raise HTTPException(status_code=422, detail=errors)

    return ValidateResponse(valid=True, errors=[])


@router.get(
    "/wiseview",
    response_model=WiseViewConvertResponse,
    summary="WiseView URL'sini SPHEREx şemasına çevirir",
)
async def convert_wiseview_url(
    wv_url: str = Query(
        ...,
        description=(
            "Dönüştürülecek WiseView URL veya sorgu dizesi. "
            "Tam URL (https://wise-view.xyz/main.html?ra=...) veya "
            "yalnızca sorgu kısmı (ra=...&dec=...) kabul edilir."
        ),
    ),
) -> WiseViewConvertResponse:
    """
    WiseView URL'sini SPHEREx görüntüleyici şemasına çevirir.

    ``wiseview_compat.parse_wiseview_url`` ile parametreler ayrıştırılır,
    ardından ``convert_wiseview_to_spherex`` ile SPHEREx şemasına çevrilir.

    Dönüşüm başarısız olursa (URL ayrıştırılamıyorsa veya yakın demo hedef
    bulunamıyorsa) ``404 Not Found`` döner.
    """
    query_str = _extract_query_string(wv_url)

    wv_params = parse_wiseview_url(query_str)
    if wv_params is None:
        logger.warning(
            "WiseView URL ayrıştırılamadı veya zorunlu alanlar eksik: %r", wv_url
        )
        raise HTTPException(
            status_code=404,
            detail=(
                "WiseView URL ayrıştırılamadı: 'ra' ve 'dec' parametreleri zorunludur "
                "ve geçerli koordinat aralığında (RA: 0–360, Dec: -90–90) olmalıdır."
            ),
        )

    sp = convert_wiseview_to_spherex(wv_params)
    if sp is None:
        logger.info(
            "WiseView koordinatlarına yakın demo hedef bulunamadı: ra=%.4f, dec=%.4f",
            wv_params.ra,
            wv_params.dec,
        )
        raise HTTPException(
            status_code=404,
            detail=(
                f"RA={wv_params.ra:.4f}, Dec={wv_params.dec:.4f} koordinatlarına "
                "yakın demo hedef bulunamadı (eşik: 1 derece). "
                "Desteklenen hedefler: barnard, eps_indi_b, wise0855, rwaur, rdra."
            ),
        )

    url = _spherex_params_to_query(sp)

    logger.debug(
        "WiseView dönüşümü başarılı: ra=%.4f dec=%.4f → hedef=%s, url=%s",
        wv_params.ra,
        wv_params.dec,
        sp.target,
        url,
    )

    return WiseViewConvertResponse(url=url, target=sp.target, valid=True)
