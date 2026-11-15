"""04-03: Zorlanmis (forced) ePSF fotometri modulu — sabit konumda kare basi aki.

Konum (x, y) 0-tabanli ebeveyn pikselde sabittir (WCS donusumu ve duzeltmesi
02-03/03-09 entegrasyonunda baglanir [NV]). Yalnizca (F, b) uydurulur;
agirlik 1 / (VAR * s^2), s >= 1.0. chi2_nu > 5.0 ise 'bad_fit' doner ve aki
degeri verilmez. NaN/OVERFLOW cekirdek 'saturated_fit' ile isaretlenir.
"""
from __future__ import annotations

import math

import numpy as np

# 0x3C028E44 + OVERFLOW(1) + DICHROIC(7) + GHOST(22-24) + STREAK(25)
DEFAULT_BAD_FLAGS = 0x3C028E44 | (1 << 1) | (1 << 7) | (0x7 << 22) | (1 << 25)
# TRANSIENT / CROSSTALK / HALO / PERSIST uyari bitleri (3 px icinde uyari)
WARN_FLAGS = (1 << 10) | (1 << 14) | (1 << 19) | (1 << 21)


def forced_phot_frame(
    grid,
    xx,
    yy,
    image,
    variance,
    x_px: float,
    y_px: float,
    *,
    flags=None,
    bad_flags: int = DEFAULT_BAD_FLAGS,
    warn_flags: int = WARN_FLAGS,
    var_scale: float = 1.0,
    frame_meta: dict | None = None,
) -> dict:
    """Sabit (x_px, y_px) konumunda agirlikli dogrusal en kucuk kareler (F, b)."""
    img = np.asarray(image, dtype=float)
    var_scale = float(var_scale)
    var = np.asarray(variance, dtype=float) * (var_scale ** 2)
    xx_a = np.asarray(xx, dtype=float)
    yy_a = np.asarray(yy, dtype=float)
    if not (img.shape == var.shape == xx_a.shape == yy_a.shape):
        raise ValueError("xx, yy, image ve variance ayni sekilde olmali")
    if var_scale < 1.0 or not math.isfinite(var_scale):
        raise ValueError("var_scale >= 1.0 ve sonlu olmali")
    if not (math.isfinite(float(x_px)) and math.isfinite(float(y_px))):
        raise ValueError("x_px ve y_px sonlu olmali")

    valid = np.isfinite(img) & np.isfinite(var) & (var > 0.0)
    warn_within_3px = False
    if flags is not None:
        flg = np.asarray(flags, dtype=np.int64)
        if flg.shape != img.shape:
            raise ValueError("flags, image ile ayni sekilde olmali")
        valid &= (flg & bad_flags) == 0
        r2_warn = (xx_a - float(x_px)) ** 2 + (yy_a - float(y_px)) ** 2
        warn_within_3px = bool(np.any((flg[r2_warn <= 9.0] & warn_flags) != 0))

    r2_core = (xx_a - float(x_px)) ** 2 + (yy_a - float(y_px)) ** 2
    saturated_fit = bool(np.any(~valid & (r2_core <= 2.25)))

    n_valid = int(np.sum(valid))
    if n_valid < 4:
        return {
            **(frame_meta or {}),
            "status": "unmeasurable",
            "flux": None,
            "sigma_flux": None,
            "background": None,
            "chi2_nu": None,
            "bad_fit": False,
            "saturated_fit": saturated_fit,
            "warn_within_3px": warn_within_3px,
            "n_valid": n_valid,
        }

    model = grid.model_at(float(x_px), float(y_px))
    xv, yv = xx_a[valid], yy_a[valid]
    iv, wv = img[valid], 1.0 / var[valid]
    pv = model.evaluate(xv, yv, 1.0, float(x_px), float(y_px))

    # Agirlikli 2x2 normal denklem: I = F * p + b
    sw = float(np.sum(wv))
    sp = float(np.sum(wv * pv))
    sp2 = float(np.sum(wv * pv * pv))
    si = float(np.sum(wv * iv))
    spi = float(np.sum(wv * pv * iv))
    det = sp2 * sw - sp * sp
    if det <= 0.0 or not math.isfinite(det):
        return {
            **(frame_meta or {}),
            "status": "unmeasurable",
            "flux": None,
            "sigma_flux": None,
            "background": None,
            "chi2_nu": None,
            "bad_fit": False,
            "saturated_fit": saturated_fit,
            "warn_within_3px": warn_within_3px,
            "n_valid": n_valid,
        }

    flux = (spi * sw - sp * si) / det
    bg = (sp2 * si - sp * spi) / det
    sigma_flux = math.sqrt(sw / det)
    resid = iv - (flux * pv + bg)
    chi2_nu = float(np.sum(wv * resid * resid) / max(n_valid - 2, 1))
    bad_fit = chi2_nu > 5.0

    return {
        **(frame_meta or {}),
        "status": "bad_fit" if bad_fit else "ok",
        "flux": None if bad_fit else float(flux),
        "sigma_flux": None if bad_fit else float(sigma_flux),
        "background": None if bad_fit else float(bg),
        "chi2_nu": chi2_nu,
        "bad_fit": bad_fit,
        "saturated_fit": saturated_fit,
        "warn_within_3px": warn_within_3px,
        "n_valid": n_valid,
    }


def combine_forced_flux(measurements: list[dict]) -> dict:
    """Ters-varyans agirlikli aki birlestirme (04-04 / gecis toplami icin)."""
    good = [m for m in measurements if m.get("status") == "ok"
            and m.get("flux") is not None and m.get("sigma_flux") is not None
            and math.isfinite(float(m["flux"]))
            and math.isfinite(float(m["sigma_flux"]))
            and m["sigma_flux"] > 0]
    if not good:
        return {"status": "unmeasurable", "n_used": 0, "flux": None, "sigma_flux": None, "snr": None}
    f = np.array([m["flux"] for m in good], dtype=float)
    w = 1.0 / (np.array([m["sigma_flux"] for m in good], dtype=float) ** 2)
    w_sum = float(np.sum(w))
    flux_mean = float(np.sum(w * f) / w_sum)
    sigma_mean = math.sqrt(1.0 / w_sum)
    return {
        "status": "ok",
        "n_used": len(good),
        "flux": flux_mean,
        "sigma_flux": sigma_mean,
        "snr": float(flux_mean / sigma_mean) if sigma_mean > 0 else math.nan,
    }
