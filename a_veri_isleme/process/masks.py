"""
Alan A - Görev 02-04 & 02-13: Maske Profilleri (C.4) ve Kare Kalite Bayrakları
Doğrulama durumu:
- Bit numaraları ve iki profil: [V: PLAN_spherex_v3.md §2.1, s0_D §2-4]
- Kalite eşikleri (%50 fit-mask, %50 SOURCE kalabalık alan): [ASSUMPTION: PLAN_spherex_v3.md §2.1]
"""

from __future__ import annotations
from dataclasses import dataclass
import math
from typing import Any, Dict, List, Sequence

try:
    import numpy as np
except ImportError:  # pragma: no cover
    np = None  # type: ignore

# SPHEREx FLAGS bit tanımları [V: PLAN_spherex_v3.md §2.1, s0_D]
BIT_TRANSIENT = 0
BIT_OVERFLOW = 1
BIT_SUR_ERROR = 2
BIT_NONFUNC = 6
BIT_DICHROIC = 7
BIT_MISSING_DATA = 9
BIT_HOT = 10
BIT_COLD = 11
BIT_NORM_FACTOR = 14
BIT_PERSIST = 15
BIT_OUTLIER = 19
BIT_CROSSTALK = 20
BIT_SOURCE = 21
BIT_GHOST_1 = 22
BIT_GHOST_2 = 23
BIT_GHOST_3 = 24
BIT_STREAK = 25

# Temel uyum (fit) maskesi [V: s0_C, s0_D]: 0x3C028E44
BASE_FIT_MASK: int = 0x3C028E44

# Ek bit maskeleri
MASK_OVERFLOW: int = 1 << BIT_OVERFLOW          # 0x00000002
MASK_DICHROIC: int = 1 << BIT_DICHROIC          # 0x00000080
MASK_STREAK: int = 1 << BIT_STREAK              # 0x02000000
MASK_GHOST: int = (1 << BIT_GHOST_1) | (1 << BIT_GHOST_2) | (1 << BIT_GHOST_3)  # 0x01C00000
MASK_CROSSTALK: int = 1 << BIT_CROSSTALK        # 0x00100000
MASK_TRANSIENT: int = 1 << BIT_TRANSIENT        # 0x00000001
MASK_OUTLIER: int = 1 << BIT_OUTLIER            # 0x00080000
MASK_SOURCE: int = 1 << BIT_SOURCE              # 0x00200000
MASK_PERSIST: int = 1 << BIT_PERSIST            # 0x00008000

# Profil 1: Merkezleme ve Fotometri (Centroid / Photometry) [V: PLAN_spherex_v3.md §2.1]
# fit mask + OVERFLOW (1) + DICHROIC (7) + STREAK (25) + GHOST (22-24)
PROFILE_CENTROID_MASK: int = (
    BASE_FIT_MASK | MASK_OVERFLOW | MASK_DICHROIC | MASK_STREAK | MASK_GHOST
)

# Profil 2: Hareketli Cisim Arama (Mover Search) [V: PLAN_spherex_v3.md §2.1]
# Yalnızca temel fit maskesi; OUTLIER (19) ve SOURCE (21) ASLA maskelenmez!
PROFILE_MOVER_MASK: int = BASE_FIT_MASK

# Arka plan (Background) temel maskesi (SOURCE dahil, ancak kalabalık alanda SOURCE düşürülür)
PROFILE_BACKGROUND_BASE_MASK: int = PROFILE_CENTROID_MASK | MASK_SOURCE | MASK_OUTLIER


@dataclass(frozen=True)
class MaskProfileSpec:
    name: str
    hex_mask: str
    int_mask: int
    caution_bits: int
    never_mask_bits: int
    description: str


MASK_PROFILE_TABLE: Dict[str, MaskProfileSpec] = {
    "centroid": MaskProfileSpec(
        name="centroid",
        hex_mask=f"0x{PROFILE_CENTROID_MASK:08X}",
        int_mask=PROFILE_CENTROID_MASK,
        caution_bits=MASK_TRANSIENT | MASK_CROSSTALK | MASK_PERSIST,
        never_mask_bits=MASK_SOURCE,
        description="Merkezleme ve fotometri: fit mask + OVERFLOW + DICHROIC + STREAK + GHOST [V: s0_D §4]",
    ),
    "mover_search": MaskProfileSpec(
        name="mover_search",
        hex_mask=f"0x{PROFILE_MOVER_MASK:08X}",
        int_mask=PROFILE_MOVER_MASK,
        caution_bits=MASK_STREAK | MASK_GHOST | MASK_CROSSTALK | MASK_TRANSIENT,
        never_mask_bits=MASK_OUTLIER | MASK_SOURCE,
        description="Hareketli cisim arama: yalnız fit mask; OUTLIER ve SOURCE asla maskelenmez [V: s0_D §3]",
    ),
}


def _flatten(data: Any) -> List[Any]:
    if isinstance(data, (list, tuple)):
        out: List[Any] = []
        for item in data:
            out.extend(_flatten(item))
        return out
    return [data]


def build_pixel_mask(
    flags: Any,
    image: Any = None,
    variance: Any = None,
    profile: str = "centroid",
) -> Any:
    """
    Verilen FLAGS (uint32) dizisi ve isteğe bağlı IMAGE/VARIANCE için
    boolean maske üretir (True = maskelenmiş / kullanılmaz piksel).
    """
    if profile not in MASK_PROFILE_TABLE:
        raise ValueError(f"Bilinmeyen maske profili: {profile}")
    bitmask = MASK_PROFILE_TABLE[profile].int_mask

    if np is not None and isinstance(flags, np.ndarray):
        flg = np.asarray(flags, dtype=np.uint32)
        masked = (flg & np.uint32(bitmask)) != 0
        if image is not None:
            masked = masked | (~np.isfinite(image))
        if variance is not None:
            masked = masked | (~np.isfinite(variance)) | (variance <= 0)
        return masked

    # Saf Python geri dönüşü (numpy kurulu değilse bile çalışır)
    flat_f = _flatten(flags)
    flat_i = _flatten(image) if image is not None else None
    flat_v = _flatten(variance) if variance is not None else None
    res: List[bool] = []
    for idx, fval in enumerate(flat_f):
        m = (int(fval) & bitmask) != 0
        if flat_i is not None and not math.isfinite(float(flat_i[idx])):
            m = True
        if flat_v is not None and (not math.isfinite(float(flat_v[idx])) or float(flat_v[idx]) <= 0):
            m = True
        res.append(m)
    return res


def evaluate_frame_quality(
    flags: Any,
    unusable_threshold: float = 0.50,
    crowded_source_threshold: float = 0.50,
) -> Dict[str, object]:
    """
    Görev 02-13: Kare kalite bayrakları ve kalabalık alan kontrolü.
    - Fit-mask oranı > %50 ise 'unusable_for_astrometry' [ASSUMPTION: PLAN_spherex_v3.md §2.1]
    - SOURCE oranı > %50 ise 'crowded_field' (arka planda SOURCE maskesi düşürülür,
      hareketli cisim bağlama/linking kapatılır) [V: s0_D §2].
    """
    if np is not None and isinstance(flags, np.ndarray):
        flg = np.asarray(flags, dtype=np.uint32)
        total_px = max(flg.size, 1)
        fit_masked_frac = float(np.count_nonzero((flg & np.uint32(BASE_FIT_MASK)) != 0)) / total_px
        source_frac = float(np.count_nonzero((flg & np.uint32(MASK_SOURCE)) != 0)) / total_px
        persist_frac = float(np.count_nonzero((flg & np.uint32(MASK_PERSIST)) != 0)) / total_px
    else:
        flat_f = [int(x) for x in _flatten(flags)]
        total_px = max(len(flat_f), 1)
        fit_masked_frac = sum(1 for x in flat_f if (x & BASE_FIT_MASK) != 0) / total_px
        source_frac = sum(1 for x in flat_f if (x & MASK_SOURCE) != 0) / total_px
        persist_frac = sum(1 for x in flat_f if (x & MASK_PERSIST) != 0) / total_px

    unusable = fit_masked_frac > unusable_threshold
    crowded = source_frac > crowded_source_threshold

    badges: List[str] = []
    if unusable:
        badges.append("unusable-for-astrometry")
    if crowded:
        badges.append("crowded-field")

    return {
        "fit_mask_fraction": round(fit_masked_frac, 4),
        "source_fraction": round(source_frac, 4),
        "persist_fraction": round(persist_frac, 4),
        "unusable_for_astrometry": unusable,
        "crowded_field": crowded,
        "mover_linking_enabled": not (unusable or crowded),
        "background_drop_source_bit": crowded,
        "badges": badges,
    }
