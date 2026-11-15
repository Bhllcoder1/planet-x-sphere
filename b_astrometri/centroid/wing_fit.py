"""03-05: Doymus cekirdek kanat uyumu (NaN / OVERFLOW pikselleri maskeleyerek).

Cekirdek (baslangic konumuna <= 1.5 px) icinde NaN/OVERFLOW/gecersiz piksel
varsa uyum yalnizca gecerli kanat piksellerinde yapilir ve 'saturated_fit'
rozeti verilir. Maskeli piksel orani > 0.5 veya gecerli piksel < 6 ise
'olculemez' ('unmeasurable') doner.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import least_squares

from ellipse import catalog_fields

# 0x3C028E44 + OVERFLOW(1) + DICHROIC(7) + GHOST(22-24) + STREAK(25)
DEFAULT_BAD_FLAGS = 0x3C028E44 | (1 << 1) | (1 << 7) | (0x7 << 22) | (1 << 25)


def valid_pixel_mask(image, variance, flags=None, *, bad_flags: int = DEFAULT_BAD_FLAGS):
    """Sonlu IMAGE, pozitif sonlu VARIANCE ve kotu bayraksiz piksel maskesi."""
    img = np.asarray(image, dtype=float)
    var = np.asarray(variance, dtype=float)
    valid = np.isfinite(img) & np.isfinite(var) & (var > 0.0)
    if flags is not None:
        flg = np.asarray(flags, dtype=np.int64)
        valid &= (flg & bad_flags) == 0
    return valid


def fit_epsf_wing(
    grid,
    xx,
    yy,
    image,
    variance,
    x_init: float,
    y_init: float,
    *,
    flags=None,
    bad_flags: int = DEFAULT_BAD_FLAGS,
    core_radius_px: float = 1.5,
) -> dict:
    """ePSF kanat uyumu: (x, y, flux, bg) + 2x2 kovaryans + hata elipsi."""
    img = np.asarray(image, dtype=float)
    var = np.asarray(variance, dtype=float)
    xx_arr = np.asarray(xx, dtype=float)
    yy_arr = np.asarray(yy, dtype=float)
    if not (img.shape == var.shape == xx_arr.shape == yy_arr.shape):
        raise ValueError("xx, yy, image ve variance ayni sekilde olmali")

    valid = valid_pixel_mask(img, var, flags, bad_flags=bad_flags)
    r2 = (xx_arr - float(x_init)) ** 2 + (yy_arr - float(y_init)) ** 2
    core_mask = r2 <= (core_radius_px ** 2)
    saturated_fit = bool(np.any(~valid & core_mask))

    masked_fraction = float(1.0 - np.mean(valid))
    n_valid = int(np.sum(valid))
    if masked_fraction > 0.5 or n_valid < 6:
        return {
            "status": "unmeasurable",
            "saturated_fit": saturated_fit,
            "n_valid": n_valid,
            "masked_fraction": masked_fraction,
        }

    model = grid.model_at(float(x_init), float(y_init))
    xv, yv = xx_arr[valid], yy_arr[valid]
    iv, inv_std = img[valid], 1.0 / np.sqrt(var[valid])
    bg0 = float(np.median(iv))
    flux0 = float(max(np.sum(iv - bg0), 1.0))

    def residuals(p):
        pred = model.evaluate(xv, yv, p[2], p[0], p[1]) + p[3]
        return (pred - iv) * inv_std

    res = least_squares(
        residuals,
        [float(x_init), float(y_init), flux0, bg0],
        bounds=(
            [float(xv.min()), float(yv.min()), 0.0, -np.inf],
            [float(xv.max()), float(yv.max()), np.inf, np.inf],
        ),
        x_scale="jac",
        xtol=1e-10, ftol=1e-10, gtol=1e-10,
    )
    dof = max(n_valid - 4, 1)
    chi2_nu = float(np.sum(res.fun ** 2) / dof)
    try:
        jtj_inv = np.linalg.inv(res.jac.T @ res.jac)
    except np.linalg.LinAlgError:
        return {
            "status": "unmeasurable",
            "saturated_fit": saturated_fit,
            "n_valid": n_valid,
            "masked_fraction": masked_fraction,
        }

    cov_xy = jtj_inv[:2, :2]
    ellipse = catalog_fields(cov_xy)
    return {
        "status": "ok",
        "saturated_fit": saturated_fit,
        "x": float(res.x[0]),
        "y": float(res.x[1]),
        "flux": float(res.x[2]),
        "background": float(res.x[3]),
        "chi2_nu": chi2_nu,
        "n_valid": n_valid,
        "masked_fraction": masked_fraction,
        **ellipse,
    }
