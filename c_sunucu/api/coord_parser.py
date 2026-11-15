"""
coord_parser.py — Koordinat ayrıştırıcı ve FOV seçici.

## Koordinat girişi (10-03):
Serbest metin ayrıştırma:
- "269.4521 4.6933" → RA/Dec ondalık
- "17h57m48.5s +04d41m36s" → HMS/DMS
- "barnard" → demo hedef adı arama
- "17 57 48.5 +04 41 36" → boşlukla ayrılmış HMS/DMS

## FOV seçici (10-04):
- Piksel ölçeği: SPHEREx ~6.2"/piksel [NV]
- Pencere: varsayılan 100×100 piksel = ~620"×620" = ~10'×10'
- Zoom: 1×..8× (k ile ilişkili: R-k modu)
- FOV seçenekleri: 50"×50", 2'×2', 10'×10', 30'×30'
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

SPHEREX_PIXEL_SCALE_ARCSEC = 6.2  # [NV]
DEFAULT_WINDOW_PX = 100

DEMO_TARGETS = {
    "barnard": (269.4521, 4.6933),
    "eps_indi_b": (330.8400, -56.7900),
    "wise0855": (133.7900, -7.2400),
    "rwaur": (75.4950, 30.4000),
    "rdra": (274.0600, 68.1300),
    # Alias'lar
    "barnard's star": (269.4521, 4.6933),
    "wise 0855": (133.7900, -7.2400),
    "rw aur": (75.4950, 30.4000),
    "r dra": (274.0600, 68.1300),
    "eps indi b": (330.8400, -56.7900),
}

# HMS/DMS regex desenleri
# "17h57m48.5s +04d41m36s" biçimi
_HMS_DMS_EXPLICIT = re.compile(
    r"""
    ^\s*
    (?P<ra_h>\d{1,2})h\s*(?P<ra_m>\d{1,2})m\s*(?P<ra_s>[\d.]+)s?
    \s+
    (?P<dec_sign>[+-]?)(?P<dec_d>\d{1,2})d\s*(?P<dec_m>\d{1,2})m\s*(?P<dec_s>[\d.]+)s?
    \s*$
    """,
    re.VERBOSE | re.IGNORECASE,
)

# "17 57 48.5 +04 41 36" biçimi (boşlukla ayrılmış 6 alan)
_HMS_DMS_SPACE = re.compile(
    r"""
    ^\s*
    (?P<ra_h>\d{1,2})\s+(?P<ra_m>\d{1,2})\s+(?P<ra_s>[\d.]+)
    \s+
    (?P<dec_sign>[+-]?)(?P<dec_d>\d{1,2})\s+(?P<dec_m>\d{1,2})\s+(?P<dec_s>[\d.]+)
    \s*$
    """,
    re.VERBOSE,
)

# İki ondalık sayı: "269.4521 4.6933"
_DECIMAL_TWO = re.compile(
    r"""
    ^\s*
    (?P<ra>[+-]?[\d]+\.[\d]*)
    \s+
    (?P<dec>[+-]?[\d]+\.[\d]*)
    \s*$
    """,
    re.VERBOSE,
)


@dataclass(frozen=True)
class ParsedCoord:
    """Ayrıştırılmış koordinat sonucu."""

    ra_deg: float
    dec_deg: float
    source: str  # "decimal", "hms_dms", "target_name"


@dataclass(frozen=True)
class FovConfig:
    """FOV yapılandırması."""

    window_px: int      # pencere piksel boyutu
    zoom_k: int         # zoom faktörü (R-k ile ilişkili)
    fov_arcsec: float   # görüş alanı arcsec


def parse_coord(text: str) -> Optional[ParsedCoord]:
    """
    Serbest metin koordinat ayrıştırır.

    Desteklenen biçimler (öncelik sırasıyla):
    1. Hedef adı: "barnard", "wise 0855", ...
    2. Ondalık RA/Dec: "269.4521 4.6933"
    3. HMS/DMS açık: "17h57m48.5s +04d41m36s"
    4. HMS/DMS boşluklu: "17 57 48.5 +04 41 36"

    Returns:
        ParsedCoord veya None (ayrıştırma başarısız olursa).
    """
    cleaned = text.strip()
    if not cleaned:
        return None

    # 1. Hedef adı araması
    lower = cleaned.lower()
    if lower in DEMO_TARGETS:
        ra, dec = DEMO_TARGETS[lower]
        return ParsedCoord(ra_deg=ra, dec_deg=dec, source="target_name")

    # 2. Ondalık biçim
    decimal_result = _parse_decimal(cleaned)
    if decimal_result is not None:
        ra, dec = decimal_result
        return ParsedCoord(ra_deg=ra, dec_deg=dec, source="decimal")

    # 3. HMS/DMS biçimi
    hms_result = _parse_hms_dms(cleaned)
    if hms_result is not None:
        ra, dec = hms_result
        return ParsedCoord(ra_deg=ra, dec_deg=dec, source="hms_dms")

    return None


def _parse_decimal(text: str) -> Optional[tuple[float, float]]:
    """
    "269.45 4.69" veya "269.45 -4.69" biçimini ayrıştırır.

    RA aralığı: 0..360, Dec aralığı: -90..90.
    Geçersiz aralıkta None döner.
    """
    match = _DECIMAL_TWO.match(text)
    if not match:
        return None

    try:
        ra = float(match.group("ra"))
        dec = float(match.group("dec"))
    except ValueError:
        return None

    if not (0.0 <= ra <= 360.0):
        return None
    if not (-90.0 <= dec <= 90.0):
        return None

    return ra, dec


def _parse_hms_dms(text: str) -> Optional[tuple[float, float]]:
    """
    HMS/DMS koordinat ayrıştırır.

    Desteklenen biçimler:
    - "17h57m48.5s +04d41m36s"
    - "17 57 48.5 +04 41 36"

    RA saatlerini dereceye çevirir (1 saat = 15 derece).
    Dec işareti "-" ise tüm bileşen negatif olur.
    """
    match = _HMS_DMS_EXPLICIT.match(text) or _HMS_DMS_SPACE.match(text)
    if not match:
        return None

    try:
        ra_h = float(match.group("ra_h"))
        ra_m = float(match.group("ra_m"))
        ra_s = float(match.group("ra_s"))

        dec_sign_str = match.group("dec_sign")
        dec_d = float(match.group("dec_d"))
        dec_m = float(match.group("dec_m"))
        dec_s = float(match.group("dec_s"))
    except (ValueError, IndexError):
        return None

    # RA: saat → derece
    ra_deg = (ra_h + ra_m / 60.0 + ra_s / 3600.0) * 15.0

    # Dec: işaretli bileşen
    dec_abs = dec_d + dec_m / 60.0 + dec_s / 3600.0
    dec_deg = -dec_abs if dec_sign_str == "-" else dec_abs

    if not (0.0 <= ra_deg <= 360.0):
        return None
    if not (-90.0 <= dec_deg <= 90.0):
        return None

    return ra_deg, dec_deg


def fov_from_window_px(window_px: int, zoom_k: int = 1) -> FovConfig:
    """
    Piksel penceresi ve zoom faktöründen FOV hesaplar.

    Args:
        window_px: Görüntü penceresi piksel boyutu (kare).
        zoom_k: Zoom faktörü (R-k modu; büyüdükçe FOV küçülür).

    Returns:
        FovConfig nesnesi.
    """
    if zoom_k < 1:
        raise ValueError(f"zoom_k en az 1 olmalı, alınan: {zoom_k}")
    return FovConfig(
        window_px=window_px,
        zoom_k=zoom_k,
        fov_arcsec=window_px * SPHEREX_PIXEL_SCALE_ARCSEC / zoom_k,
    )


FOV_PRESETS: dict[str, FovConfig] = {
    "50arcsec": fov_from_window_px(8),
    "2arcmin": fov_from_window_px(20),
    "10arcmin": fov_from_window_px(DEFAULT_WINDOW_PX),
    "30arcmin": fov_from_window_px(300),
}
