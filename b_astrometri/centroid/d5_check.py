"""03-02 (D5): ePSF normalizasyon (x1 vs x25) ve yonelim (normal vs devrik x<->y) kontrolu.

Normalizasyon farki konumu degistirmez ama akiyi 25 kat degistirir; bu nedenle
hem konum kurtarma (< 0.001 px) hem aki orani olculur. Yonelim secimi
(PSF_TRANSPOSE) icin normal ve devrik ePSF ile reduced chi2 (chi2_nu)
karsilastirilir. 200 gercek yildiz (02-07) gelene kadar gercek veri kismi [NV].
"""
from __future__ import annotations

import numpy as np
from photutils.psf import ImagePSF
from scipy.optimize import least_squares


def self_recovery_ladder(grid, shifts=None, *, true_flux: float = 123.0) -> dict:
    """Bilinen alt-piksel kaymalarda (dx, dy) kendini kurtarma ve aki olcegi."""
    if shifts is None:
        steps = [0.0, 0.1, 0.3, 0.5, 0.7, 0.9]
        shifts = [(dx, dy) for dx in steps for dy in steps]
    center = grid.positions[len(grid.positions) // 2]
    yy, xx = np.mgrid[-4:5, -4:5] + center[:, None, None][::-1]
    pos_errors, flux_ratios = [], []
    for dx, dy in shifts:
        x, y = float(center[0] + dx), float(center[1] + dy)
        model = grid.model_at(x, y)
        image = model.evaluate(xx, yy, true_flux, x, y)
        fit = least_squares(
            lambda p: (model.evaluate(xx, yy, p[2], p[0], p[1]) - image).ravel(),
            [x + 0.08, y - 0.06, true_flux * 0.9],
            xtol=1e-12, ftol=1e-12, gtol=1e-12,
        )
        pos_errors.append(float(np.hypot(fit.x[0] - x, fit.x[1] - y)))
        flux_ratios.append(float(fit.x[2] / true_flux))
    return {
        "norm": float(grid.norm),
        "n_shifts": len(shifts),
        "max_pos_error_px": float(max(pos_errors)),
        "mean_flux_ratio": float(np.mean(flux_ratios)),
        "passed_recovery": bool(max(pos_errors) < 0.001),
    }


def _fit_chi2_nu(model_samples, oversampling, xx, yy, image, variance, x_init, y_init) -> float:
    model = ImagePSF(model_samples, oversampling=oversampling, x_0=x_init, y_0=y_init)
    inv_std = 1.0 / np.sqrt(variance)
    flux0 = float(np.sum(image))
    fit = least_squares(
        lambda p: ((model.evaluate(xx, yy, p[2], p[0], p[1]) - image) * inv_std).ravel(),
        [float(x_init), float(y_init), flux0],
        xtol=1e-10, ftol=1e-10, gtol=1e-10,
    )
    dof = image.size - 3
    return float(np.sum(fit.fun ** 2) / dof)


def compare_orientation(grid, cutouts: list[dict]) -> dict:
    """Her kesit ({xx, yy, image, variance, x_init, y_init}) icin normal vs devrik chi2_nu.

    cutouts bos ise [NV] bekleyen durum dondurur.
    """
    if not cutouts:
        return {"status": "pending_02_07", "n_stars": 0,
                "psf_transpose": None, "normal_wins": 0, "transposed_wins": 0}
    chi2_norm, chi2_trans = [], []
    for c in cutouts:
        zone = grid.zone_at(c["x_init"], c["y_init"])
        samples = grid.samples[zone["index"]]
        chi2_norm.append(_fit_chi2_nu(
            samples, grid.oversampling, c["xx"], c["yy"],
            c["image"], c["variance"], c["x_init"], c["y_init"]))
        chi2_trans.append(_fit_chi2_nu(
            samples.T, grid.oversampling, c["xx"], c["yy"],
            c["image"], c["variance"], c["x_init"], c["y_init"]))
    cn = np.asarray(chi2_norm, dtype=float)
    ct = np.asarray(chi2_trans, dtype=float)
    normal_wins = int(np.sum(cn < ct))
    transposed_wins = int(np.sum(ct < cn))
    return {
        "status": "measured",
        "n_stars": len(cutouts),
        "normal_chi2_nu_median": float(np.median(cn)),
        "transposed_chi2_nu_median": float(np.median(ct)),
        "normal_wins": normal_wins,
        "transposed_wins": transposed_wins,
        "psf_transpose": bool(transposed_wins > normal_wins),
    }
