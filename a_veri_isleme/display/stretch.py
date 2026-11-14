"""
Alan A - Görev 02-15, 02-16, 02-19, 02-22: Gösterim İşleme Katmanı ve Germe Modülü
Doğrulama durumu:
- Temel kural: Ölçüm verisi (float32 MJy/sr) ASLA değiştirilmez; tüm gösterim işlemleri
  kopya üzerinde çalışır [V: DISPLAY_LAYER_DESIGN.md §2].
- Adımlar: maskeli limit hesabı -> arka plan görünümü (raw / zodi / flat) ->
  clip (fixed / percent / adapt / zscale) -> normalize -> asinh(x/a)/asinh(1/a) ->
  invert -> 8-bit RGBA + NaN ayrı renk (Okabe-Ito mavi).
"""

from __future__ import annotations
import copy
import hashlib
import json
import math
import os
import statistics
import struct
from typing import Any, Dict, List, Optional, Sequence, Tuple

try:
    import numpy as np
except ImportError:  # pragma: no cover
    np = None  # type: ignore

from a_veri_isleme.process.masks import (
    BASE_FIT_MASK,
    MASK_OVERFLOW,
    PROFILE_BACKGROUND_BASE_MASK,
    MASK_SOURCE,
    _flatten,
)

DEFAULTS_PATH = os.path.join(os.path.dirname(__file__), "display_defaults.json")
LIMIT_EXCLUSION_MASK = BASE_FIT_MASK | MASK_OVERFLOW


def load_display_defaults() -> Dict[str, object]:
    with open(DEFAULTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def array_sha256(arr: Any) -> str:
    """Ölçüm dizisinin değişmediğini doğrulamak için SHA-256 özeti üretir."""
    if np is not None and isinstance(arr, np.ndarray):
        contiguous = np.ascontiguousarray(arr)
        return hashlib.sha256(contiguous.view(np.uint8)).hexdigest()
    flat = [float(x) for x in _flatten(arr)]
    buf = struct.pack(f"<{len(flat)}f", *flat)
    return hashlib.sha256(buf).hexdigest()


def _percentile(sorted_vals: List[float], pct: float) -> float:
    if not sorted_vals:
        return 0.0
    if len(sorted_vals) == 1:
        return sorted_vals[0]
    k = (len(sorted_vals) - 1) * (pct / 100.0)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return sorted_vals[int(k)]
    return sorted_vals[f] * (c - k) + sorted_vals[c] * (k - f)


def apply_display_background(
    image: Any,
    zodi: Any = None,
    flags: Any = None,
    mode: str = "zodi",
) -> Tuple[Any, Dict[str, object]]:
    """
    Görev 02-19: Yalnız gösterim amaçlı ZODI / arka plan çıkarma.
    Girdi dizilerini ASLA yerinde (in-place) değiştirmez.
    Modlar:
      - 'raw': v
      - 'zodi': v - ZODI
      - 'flat': v - ZODI - m_k (m_k = karenin maskeli medyanı)
    """
    if mode not in ("raw", "zodi", "flat"):
        raise ValueError(f"Geçersiz arka plan gösterim modu: {mode}")

    if mode == "raw":
        v_copy = np.array(image, dtype=np.float32, copy=True) if (np is not None and isinstance(image, np.ndarray)) else copy.deepcopy(image)
        return v_copy, {"background_mode": "raw", "badge": None, "units": "MJy/sr", "median_removed": 0.0}

    # 2B liste veya numpy dizisi üzerinde kopya oluştur
    if np is not None and isinstance(image, np.ndarray):
        v = np.array(image, dtype=np.float32, copy=True)
        if zodi is not None:
            v = v - np.asarray(zodi, dtype=np.float32)
        badge = "ZODI-subtracted (display only)" if zodi is not None else None
        median_removed = 0.0
        if mode == "flat":
            valid = np.isfinite(v)
            if flags is not None:
                flg = np.asarray(flags, dtype=np.uint32)
                source_frac = np.count_nonzero((flg & np.uint32(MASK_SOURCE)) != 0) / max(flg.size, 1)
                bg_mask = PROFILE_BACKGROUND_BASE_MASK
                if source_frac > 0.50:
                    bg_mask &= ~MASK_SOURCE
                valid = valid & ((flg & np.uint32(bg_mask)) == 0)
            if np.any(valid):
                vals = v[valid]
                med = float(np.median(vals))
                mad_std = 1.4826 * float(np.median(np.abs(vals - med)))
                if mad_std > 0:
                    inliers = vals[np.abs(vals - med) <= 3.0 * mad_std]
                    if inliers.size > 0:
                        med = float(np.median(inliers))
                median_removed = med
                v = v - np.float32(med)
            badge = "ZODI+flat-subtracted (display only)"
        return v, {
            "background_mode": mode,
            "badge": badge,
            "units": "MJy/sr",
            "median_removed": median_removed,
        }

    # Saf Python 2B liste desteği
    rows = copy.deepcopy(image)
    h = len(rows)
    w = len(rows[0]) if h > 0 else 0
    if zodi is not None:
        for r in range(h):
            for c in range(w):
                rows[r][c] = float(rows[r][c]) - float(zodi[r][c])
    badge = "ZODI-subtracted (display only)" if zodi is not None else None
    median_removed = 0.0
    if mode == "flat":
        bg_mask = PROFILE_BACKGROUND_BASE_MASK
        if flags is not None:
            flat_f = [int(x) for x in _flatten(flags)]
            if sum(1 for x in flat_f if (x & MASK_SOURCE) != 0) / max(len(flat_f), 1) > 0.50:
                bg_mask &= ~MASK_SOURCE
        valid_vals: List[float] = []
        for r in range(h):
            for c in range(w):
                val = float(rows[r][c])
                if not math.isfinite(val):
                    continue
                if flags is not None and (int(flags[r][c]) & bg_mask) != 0:
                    continue
                valid_vals.append(val)
        if valid_vals:
            med = float(statistics.median(valid_vals))
            mad_std = 1.4826 * float(statistics.median([abs(x - med) for x in valid_vals]))
            if mad_std > 0:
                inliers = [x for x in valid_vals if abs(x - med) <= 3.0 * mad_std]
                if inliers:
                    med = float(statistics.median(inliers))
            median_removed = med
            for r in range(h):
                for c in range(w):
                    rows[r][c] = float(rows[r][c]) - med
        badge = "ZODI+flat-subtracted (display only)"

    return rows, {
        "background_mode": mode,
        "badge": badge,
        "units": "MJy/sr",
        "median_removed": median_removed,
    }


def _zscale_limits_from_sorted(sorted_vals: List[float], contrast: float = 0.25) -> Tuple[float, float]:
    n = len(sorted_vals)
    if n == 0:
        return 0.0, 1.0
    if n < 10:
        return float(sorted_vals[0]), float(sorted_vals[-1])
    trim = max(1, int(0.15 * n))
    mid = sorted_vals[trim : n - trim]
    if len(mid) < 2:
        return float(sorted_vals[0]), float(sorted_vals[-1])
    slope = (mid[-1] - mid[0]) / 2.0
    med = sorted_vals[n // 2]
    z1 = max(float(sorted_vals[0]), med - slope / max(contrast, 1e-3))
    z2 = min(float(sorted_vals[-1]), med + slope / max(contrast, 1e-3))
    if z2 <= z1:
        return float(sorted_vals[0]), float(sorted_vals[-1])
    return z1, z2


def compute_clip_limits(
    frames: Sequence[Any],
    flags_list: Optional[Sequence[Any]] = None,
    clip_mode: str = "percent",
    low_pct: float = 0.5,
    high_pct: float = 99.5,
    fixed_limits: Optional[Tuple[float, float]] = None,
) -> Tuple[float, float]:
    """
    Görev 02-16 & 02-22: Maskeli piksellerden kırpma (clip) limitlerini hesaplar.
    Blink dizisinde tüm kareler için ortak limit (scope='sequence') veya tek kare
    için çalışabilir.
    """
    if clip_mode == "fixed":
        if fixed_limits is None:
            raise ValueError("clip_mode='fixed' için fixed_limits (lo, hi) gereklidir.")
        return float(fixed_limits[0]), float(fixed_limits[1])

    all_valid: List[float] = []
    for idx, frame in enumerate(frames):
        flat_vals = [float(x) for x in _flatten(frame)]
        flat_flgs = (
            [int(x) for x in _flatten(flags_list[idx])]
            if (flags_list is not None and idx < len(flags_list) and flags_list[idx] is not None)
            else None
        )
        for p_idx, val in enumerate(flat_vals):
            if not math.isfinite(val):
                continue
            if flat_flgs is not None and (flat_flgs[p_idx] & LIMIT_EXCLUSION_MASK) != 0:
                continue
            all_valid.append(val)

    if not all_valid:
        return 0.0, 1.0

    all_valid.sort()
    if clip_mode == "percent":
        lo = _percentile(all_valid, low_pct)
        hi = _percentile(all_valid, high_pct)
        if hi <= lo:
            return _zscale_limits_from_sorted(all_valid)
        return lo, hi
    if clip_mode in ("zscale", "adapt"):
        return _zscale_limits_from_sorted(all_valid)

    raise ValueError(f"Bilinmeyen clip_mode: {clip_mode}")


def stretch_array(
    image_display: Any,
    lo: float,
    hi: float,
    asinh_a: float = 0.1,
    invert: bool = False,
) -> Any:
    """
    Görev 02-16:
      1. Normalize: x = clamp((v' - lo) / (hi - lo), 0, 1); hi == lo ise x = 0
      2. AsinhStretch: y = asinh(x / a) / asinh(1 / a)
      3. Invert: y = 1 - y (açıksa)
    NaN pikseller NaN olarak korunur.
    """
    a = max(float(asinh_a), 1e-6)
    denom = math.asinh(1.0 / a)

    if np is not None and isinstance(image_display, np.ndarray):
        v = np.array(image_display, dtype=np.float32, copy=True)
        nan_mask = ~np.isfinite(v)
        if hi <= lo:
            x = np.zeros_like(v, dtype=np.float32)
        else:
            x = np.clip((v - np.float32(lo)) / np.float32(hi - lo), 0.0, 1.0)
        y = np.arcsinh(x / np.float32(a)) / np.float32(denom)
        if invert:
            y = 1.0 - y
        y[nan_mask] = np.nan
        return y

    out_rows = []
    for row in image_display:
        out_row = []
        for val in row:
            fval = float(val)
            if not math.isfinite(fval):
                out_row.append(float("nan"))
                continue
            if hi <= lo:
                x = 0.0
            else:
                x = min(1.0, max(0.0, (fval - lo) / (hi - lo)))
            y = math.asinh(x / a) / denom
            if invert:
                y = 1.0 - y
            out_row.append(y)
        out_rows.append(out_row)
    return out_rows


def render_rgba8(
    stretched: Any,
    nan_color_rgb: Tuple[int, int, int] = (0, 114, 178),
) -> Any:
    """
    Gerilmiş [0, 1] float32 görüntüyü 8-bit RGBA (H, W, 4) dizisine dönüştürür.
    NaN pikseller Okabe-Ito mavi (0, 114, 178) ile boyanır [V: DISPLAY_LAYER_DESIGN.md §2.1].
    """
    if np is not None and isinstance(stretched, np.ndarray):
        h, w = stretched.shape
        rgba = np.zeros((h, w, 4), dtype=np.uint8)
        nan_mask = ~np.isfinite(stretched)
        valid_mask = ~nan_mask
        gray = np.zeros((h, w), dtype=np.uint8)
        if np.any(valid_mask):
            gray[valid_mask] = np.clip(np.round(stretched[valid_mask] * 255.0), 0, 255).astype(np.uint8)
        rgba[:, :, 0] = gray
        rgba[:, :, 1] = gray
        rgba[:, :, 2] = gray
        rgba[:, :, 3] = 255
        if np.any(nan_mask):
            rgba[nan_mask, 0] = nan_color_rgb[0]
            rgba[nan_mask, 1] = nan_color_rgb[1]
            rgba[nan_mask, 2] = nan_color_rgb[2]
        return rgba

    rgba_rows = []
    for row in stretched:
        rgba_row = []
        for val in row:
            fval = float(val)
            if not math.isfinite(fval):
                rgba_row.append((nan_color_rgb[0], nan_color_rgb[1], nan_color_rgb[2], 255))
            else:
                g = max(0, min(255, int(round(fval * 255.0))))
                rgba_row.append((g, g, g, 255))
        rgba_rows.append(rgba_row)
    return rgba_rows
