"""03-06 (C.7b prototip): Gecis basina ortak uyum — tek (ra, dec) ile kareler boyunca.

Yeniden ornekleme (drizzle) yoktur: her kare kendi ePSF ve WCS'ini kullanir;
kare basina (F_k, b_k) serbesttir (LVF nedeniyle lambda kare basina degisir).
bad_fit / unusable_for_astrometry kareler sessizce atlanmaz, sayisi raporlanir.
WCS duzeltmesi (03-09) ve gercek Barnard L2 entegrasyonu [NV].
"""
from __future__ import annotations

import math
from typing import Any

import numpy as np
from scipy.optimize import least_squares

from ellipse import catalog_fields
from wing_fit import DEFAULT_BAD_FLAGS, valid_pixel_mask


def fit_joint_pass(
    frames: list[dict[str, Any]],
    ra_init_deg: float,
    dec_init_deg: float,
    *,
    bad_flags: int = DEFAULT_BAD_FLAGS,
) -> dict[str, Any]:
    """Gecis kareleri boyunca ortak (ra, dec) ve kare basina (F_k, b_k) uyumu."""
    usable: list[dict[str, Any]] = []
    excluded: list[dict[str, str]] = []
    for idx, f in enumerate(frames):
        fid = str(f.get("frame_id", f"frame_{idx}"))
        if f.get("bad_fit"):
            excluded.append({"frame_id": fid, "reason": "bad_fit"})
            continue
        if f.get("unusable_for_astrometry"):
            excluded.append({"frame_id": fid, "reason": "unusable_for_astrometry"})
            continue
        valid = valid_pixel_mask(f["image"], f["variance"], f.get("flags"), bad_flags=bad_flags)
        if int(np.sum(valid)) < 6:
            excluded.append({"frame_id": fid, "reason": "too_few_valid_pixels"})
            continue
        xv = np.asarray(f["xx"], dtype=float)[valid]
        yv = np.asarray(f["yy"], dtype=float)[valid]
        iv = np.asarray(f["image"], dtype=float)[valid]
        inv_std = 1.0 / np.sqrt(np.asarray(f["variance"], dtype=float)[valid])
        x_p, y_p = f["wcs"].all_world2pix(float(ra_init_deg), float(dec_init_deg), 0)
        model = f["grid"].model_at(float(x_p), float(y_p))
        bg0 = float(np.median(iv))
        flux0 = float(max(np.sum(iv - bg0), 1.0))
        usable.append({
            "frame_id": fid,
            "wcs": f["wcs"],
            "model": model,
            "xv": xv,
            "yv": yv,
            "iv": iv,
            "inv_std": inv_std,
            "flux0": flux0,
            "bg0": bg0,
            "mjd": f.get("mjd"),
            "cwave_um": f.get("cwave_um"),
        })

    if not usable:
        return {
            "status": "unmeasurable",
            "n_input": len(frames),
            "n_used": 0,
            "n_excluded": len(excluded),
            "excluded": excluded,
        }

    cos_dec0 = math.cos(math.radians(float(dec_init_deg)))
    # (dra_arcsec, ddec_arcsec) cinsinden optimize et: Jacobian kosullanmasi cok daha iyi
    p0 = [0.0, 0.0]
    lb = [-180.0, -180.0]
    ub = [180.0, 180.0]
    for u in usable:
        p0.extend([u["flux0"], u["bg0"]])
        lb.extend([0.0, -np.inf])
        ub.extend([np.inf, np.inf])

    def _to_radec(dra_arcsec: float, ddec_arcsec: float) -> tuple[float, float]:
        ra = float(ra_init_deg) + dra_arcsec / (3600.0 * max(cos_dec0, 1e-6))
        dec = float(dec_init_deg) + ddec_arcsec / 3600.0
        return ra, dec

    def residuals(p):
        ra, dec = _to_radec(p[0], p[1])
        parts = []
        for k, u in enumerate(usable):
            fk, bk = p[2 + 2 * k], p[3 + 2 * k]
            xk, yk = u["wcs"].all_world2pix(ra, dec, 0)
            pred = u["model"].evaluate(u["xv"], u["yv"], fk, float(xk), float(yk)) + bk
            parts.append((pred - u["iv"]) * u["inv_std"])
        return np.concatenate(parts)

    res = least_squares(
        residuals, p0, bounds=(lb, ub), x_scale="jac",
        xtol=1e-10, ftol=1e-10, gtol=1e-10,
    )
    n_pix = sum(len(u["iv"]) for u in usable)
    dof = max(n_pix - len(p0), 1)
    chi2_nu = float(np.sum(res.fun ** 2) / dof)

    try:
        cov_all = np.linalg.inv(res.jac.T @ res.jac)
    except np.linalg.LinAlgError:
        return {
            "status": "unmeasurable",
            "n_input": len(frames),
            "n_used": len(usable),
            "n_excluded": len(excluded),
            "excluded": excluded,
        }

    ra_out, dec_out = _to_radec(float(res.x[0]), float(res.x[1]))
    ellipse_arcsec = catalog_fields(cov_all[:2, :2])

    mjds = [float(u["mjd"]) for u in usable if u["mjd"] is not None]
    return {
        "status": "ok",
        "ra_deg": ra_out,
        "dec_deg": dec_out,
        "epoch_mid_mjd": float(np.mean(mjds)) if mjds else None,
        "chi2_nu": chi2_nu,
        "n_input": len(frames),
        "n_used": len(usable),
        "n_excluded": len(excluded),
        "excluded": excluded,
        "ellipse_arcsec": ellipse_arcsec,
        "frame_fluxes": [
            {"frame_id": u["frame_id"], "flux": float(res.x[2 + 2 * k]),
             "background": float(res.x[3 + 2 * k]), "cwave_um": u["cwave_um"]}
            for k, u in enumerate(usable)
        ],
    }
