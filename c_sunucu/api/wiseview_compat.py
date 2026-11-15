"""
wiseview_compat.py — WiseView URL parametrelerini SPHEREx şemasına çevirir.

WiseView'dan gelen URL parametreleri:
- ra, dec: koordinatlar (derece)
- band: 1=W1(3.4μm), 2=W2(4.6μm), 3=W3(12μm), 4=W4(22μm)
- size: görüntü boyutu arcsec
- minbright, maxbright: parlaklık sınırları (mag veya DN)
- color: 0=grayscale, 1=color

SPHEREx çevirisi:
- ra/dec → en yakın demo hedefine (eşik: 1 derece)
- band W2 (4.6μm) ≈ SPHEREx channel 11-14 → hdu=image
- size → w=size/pixel_scale, h=size/pixel_scale
- minbright/maxbright → clip_lo/clip_hi (yaklaşık dönüşüm)

[NV] WiseView live Lambda servisi mevcut değil; parametreler spec'ten çıkarıldı.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional
from urllib.parse import parse_qs

# Demo hedefleri (RA, Dec, J2000)
DEMO_TARGETS: dict[str, tuple[float, float]] = {
    "barnard": (269.4521, 4.6933),
    "eps_indi_b": (330.8400, -56.7900),
    "wise0855": (133.7900, -7.2400),
    "rwaur": (75.4950, 30.4000),
    "rdra": (274.0600, 68.1300),
}

SPHEREX_PIXEL_SCALE_ARCSEC: float = 6.2  # [NV: s0_A başlıklarından]

# WiseView band → SPHEREx HDU adı eşlemesi.
# W1 (3.4μm) ve W2 (4.6μm) SPHEREx kanallarına yakın düşer.
# W3 ve W4 SPHEREx bandının dışında; en yakın kanal olarak "image" kullanılır.
_BAND_TO_HDU: dict[int, str] = {
    1: "image",   # W1 3.4μm → SPHEREx ch 1-5 yakını
    2: "image",   # W2 4.6μm → SPHEREx ch 11-14 yakını
    3: "image",   # W3 12μm → SPHEREx dışı; varsayılan
    4: "image",   # W4 22μm → SPHEREx dışı; varsayılan
}


@dataclass(frozen=True)
class WiseViewParams:
    """WiseView URL parametreleri."""

    ra: float
    dec: float
    band: int = 1
    size: float = 162.0        # arcsec
    minbright: float = -50.0
    maxbright: float = 500.0
    color: int = 0


@dataclass(frozen=True)
class SPHERExParams:
    """SPHEREx görüntüleyici URL parametreleri."""

    target: str
    x: int
    y: int
    w: int
    h: int
    clip_lo: Optional[float]
    clip_hi: Optional[float]
    clip: str
    hdu: str


def angular_distance(ra1: float, dec1: float, ra2: float, dec2: float) -> float:
    """
    İki koordinat arasındaki açısal mesafeyi derece cinsinden döndürür.

    Haversine formülü kullanılır; küçük açılarda yuvarlama hatası minimumdur.

    Parametreler
    ------------
    ra1, dec1 : float
        Birinci noktanın sağ açıklığı ve kuzey çeşnimi (derece).
    ra2, dec2 : float
        İkinci noktanın sağ açıklığı ve kuzey çeşnimi (derece).

    Dönüş
    -----
    float
        İki nokta arasındaki büyük daire mesafesi (derece).
    """
    ra1_r = math.radians(ra1)
    dec1_r = math.radians(dec1)
    ra2_r = math.radians(ra2)
    dec2_r = math.radians(dec2)

    delta_ra = ra2_r - ra1_r
    delta_dec = dec2_r - dec1_r

    a = (
        math.sin(delta_dec / 2.0) ** 2
        + math.cos(dec1_r) * math.cos(dec2_r) * math.sin(delta_ra / 2.0) ** 2
    )
    c = 2.0 * math.asin(math.sqrt(a))
    return math.degrees(c)


def nearest_target(
    ra: float, dec: float, threshold_deg: float = 1.0
) -> Optional[str]:
    """
    Verilen koordinata en yakın demo hedefini döndürür.

    Eşik mesafesi içinde hiçbir hedef yoksa ``None`` döner.

    Parametreler
    ------------
    ra, dec : float
        Sorgu koordinatları (derece).
    threshold_deg : float
        Eşik mesafesi (derece). Varsayılan 1.0.

    Dönüş
    -----
    str veya None
        En yakın hedef adı ya da eşik dışındaysa ``None``.
    """
    best_name: Optional[str] = None
    best_dist = math.inf

    for name, (t_ra, t_dec) in DEMO_TARGETS.items():
        dist = angular_distance(ra, dec, t_ra, t_dec)
        if dist < best_dist:
            best_dist = dist
            best_name = name

    if best_dist <= threshold_deg:
        return best_name
    return None


def convert_wiseview_to_spherex(
    params: WiseViewParams,
) -> Optional[SPHERExParams]:
    """
    WiseView parametrelerini SPHEREx görüntüleyici şemasına çevirir.

    Yakın bir demo hedefi bulunamazsa ``None`` döner.

    Parametreler
    ------------
    params : WiseViewParams
        Dönüştürülecek WiseView parametreleri.

    Dönüş
    -----
    SPHERExParams veya None
        SPHEREx şemasına çevrilmiş parametreler;
        hedef eşik dışındaysa ``None``.

    Notlar
    ------
    - ``size`` arcsec cinsinden SPHEREx piksel ölçeğine bölünür.
    - ``minbright``/``maxbright`` yaklaşık olarak ``clip_lo``/``clip_hi``'ye
      eşlenir; birim kalibrasyonu kesin değildir.
    - ``color=1`` durumunda ``clip="zscale"`` seçilir, aksi halde ``clip="minmax"``.
    """
    target_name = nearest_target(params.ra, params.dec)
    if target_name is None:
        return None

    # Görüntü boyutunu piksele çevir (en az 1 piksel olmalı)
    size_px = max(1, round(params.size / SPHEREX_PIXEL_SCALE_ARCSEC))
    w = size_px
    h = size_px

    # Hedef görüntünün ortasında konumlandırılır
    x = w // 2
    y = h // 2

    # Band → HDU eşlemesi; bilinmeyen band için varsayılan "image"
    hdu = _BAND_TO_HDU.get(params.band, "image")

    # Renk kipine göre clip stratejisi
    clip = "zscale" if params.color == 1 else "minmax"

    # Parlaklık sınırları yaklaşık olarak geçirilir
    clip_lo: Optional[float] = params.minbright
    clip_hi: Optional[float] = params.maxbright

    return SPHERExParams(
        target=target_name,
        x=x,
        y=y,
        w=w,
        h=h,
        clip_lo=clip_lo,
        clip_hi=clip_hi,
        clip=clip,
        hdu=hdu,
    )


def _safe_float(value: str, default: float) -> float:
    """
    Dizeyi float'a çevirir; başarısız olursa varsayılana döner.

    Parametreler
    ------------
    value : str
        Dönüştürülecek dize.
    default : float
        Dönüşüm başarısız olursa kullanılacak değer.

    Dönüş
    -----
    float
        Dönüştürülmüş değer veya varsayılan.
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def _safe_int(value: str, default: int) -> int:
    """
    Dizeyi int'e çevirir; başarısız olursa varsayılana döner.

    Parametreler
    ------------
    value : str
        Dönüştürülecek dize.
    default : int
        Dönüşüm başarısız olursa kullanılacak değer.

    Dönüş
    -----
    int
        Dönüştürülmüş değer veya varsayılan.
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def parse_wiseview_url(query_string: str) -> Optional[WiseViewParams]:
    """
    WiseView URL sorgu dizesini ayrıştırır ve ``WiseViewParams`` döndürür.

    ``ra`` veya ``dec`` parametresi eksik ya da geçersizse ``None`` döner.
    Diğer geçersiz parametreler varsayılan değerlerine düşer.

    Parametreler
    ------------
    query_string : str
        ``?`` işareti olmaksızın URL sorgu dizesi.
        Örnek: ``"ra=269.4521&dec=4.6933&band=2&size=162"``

    Dönüş
    -----
    WiseViewParams veya None
        Ayrıştırılmış parametreler ya da zorunlu alan eksikse ``None``.

    Örnekler
    --------
    >>> p = parse_wiseview_url("ra=269.45&dec=4.69&band=2&size=162")
    >>> p.ra
    269.45
    >>> p.band
    2
    """
    # Baştaki "?" varsa kaldır
    qs = query_string.lstrip("?")
    parsed = parse_qs(qs, keep_blank_values=False)

    def _first(key: str) -> Optional[str]:
        """Çok değerli sözlükten ilk değeri döndürür."""
        values = parsed.get(key)
        if values:
            return values[0]
        return None

    ra_raw = _first("ra")
    dec_raw = _first("dec")

    if ra_raw is None or dec_raw is None:
        return None

    try:
        ra = float(ra_raw)
        dec = float(dec_raw)
    except (ValueError, TypeError):
        return None

    # RA: [0, 360) ve Dec: [-90, 90] aralık denetimi
    if not (0.0 <= ra < 360.0) or not (-90.0 <= dec <= 90.0):
        return None

    _defaults = WiseViewParams(ra=ra, dec=dec)

    band_raw = _first("band")
    band = _safe_int(band_raw, _defaults.band) if band_raw is not None else _defaults.band
    # Geçerli band değerleri: 1-4
    if band not in (1, 2, 3, 4):
        band = _defaults.band

    size_raw = _first("size")
    size = _safe_float(size_raw, _defaults.size) if size_raw is not None else _defaults.size
    if size <= 0.0:
        size = _defaults.size

    minbright_raw = _first("minbright")
    minbright = (
        _safe_float(minbright_raw, _defaults.minbright)
        if minbright_raw is not None
        else _defaults.minbright
    )

    maxbright_raw = _first("maxbright")
    maxbright = (
        _safe_float(maxbright_raw, _defaults.maxbright)
        if maxbright_raw is not None
        else _defaults.maxbright
    )

    # minbright > maxbright ise sıralamayı düzelt
    if minbright > maxbright:
        minbright, maxbright = maxbright, minbright

    color_raw = _first("color")
    color = _safe_int(color_raw, _defaults.color) if color_raw is not None else _defaults.color
    if color not in (0, 1):
        color = _defaults.color

    return WiseViewParams(
        ra=ra,
        dec=dec,
        band=band,
        size=size,
        minbright=minbright,
        maxbright=maxbright,
        color=color,
    )
