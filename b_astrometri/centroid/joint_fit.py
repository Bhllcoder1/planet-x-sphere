"""03-06 (C.7b prototip): Gecis basina ortak uyum — tek (ra, dec) ile kareler boyunca.

Yeniden ornekleme (drizzle) yoktur: her kare kendi ePSF ve WCS'ini kullanir;
kare basina (F_k, b_k) serbesttir (LVF nedeniyle lambda kare basina degisir).
bad_fit / unusable_for_astrometry kareler sessizce atlanmaz, sayisi raporlanir.
WCS duzeltmesi (03-09) ve gercek Barnard L2 entegrasyonu [NV].
"""
from __future__ import annotations

import math
import json
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import least_squares
from scipy.sparse import lil_matrix

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
    if not (np.isfinite(ra_init_deg) and np.isfinite(dec_init_deg)):
        raise ValueError("Initial sky position must be finite")
    if not (0 <= ra_init_deg < 360 and -90 < dec_init_deg < 90):
        raise ValueError("Require 0 <= RA < 360 and -90 < Dec < 90 degrees")
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
        image, variance, xx, yy = (np.asarray(f[key], dtype=float)
                                   for key in ("image", "variance", "xx", "yy"))
        if not (image.shape == variance.shape == xx.shape == yy.shape):
            raise ValueError(f"{fid}: image, variance, xx and yy shapes must match")
        if f.get("flags") is not None and np.shape(f["flags"]) != image.shape:
            raise ValueError(f"{fid}: flags shape must match image")
        valid = valid_pixel_mask(image, variance, f.get("flags"), bad_flags=bad_flags)
        valid &= np.isfinite(xx) & np.isfinite(yy)
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
    lb = [-180.0, max(-180.0, (-90.0 - float(dec_init_deg)) * 3600.0 + 1e-8)]
    ub = [180.0, min(180.0, (90.0 - float(dec_init_deg)) * 3600.0 - 1e-8)]
    for u in usable:
        p0.extend([u["flux0"], u["bg0"]])
        lb.extend([0.0, -np.inf])
        ub.extend([np.inf, np.inf])

    def _to_radec(dra_arcsec: float, ddec_arcsec: float) -> tuple[float, float]:
        ra = (float(ra_init_deg) + dra_arcsec / (3600.0 * cos_dec0)) % 360
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

    n_pix = sum(len(u["iv"]) for u in usable)
    sparsity = lil_matrix((n_pix, len(p0)), dtype=int)
    sparsity[:, :2] = 1
    offset = 0
    for k, u in enumerate(usable):
        n = len(u["iv"])
        sparsity[offset:offset + n, 2 + 2 * k:4 + 2 * k] = 1
        offset += n
    res = least_squares(
        residuals, p0, bounds=(lb, ub), x_scale="jac", jac_sparsity=sparsity.tocsr(),
        xtol=1e-10, ftol=1e-10, gtol=1e-10,
    )
    if not res.success:
        return {"status": "unmeasurable", "reason": "optimizer_failed",
                "n_input": len(frames), "n_used": len(usable),
                "n_excluded": len(excluded), "excluded": excluded}
    dof = max(n_pix - len(p0), 1)
    chi2_nu = float(np.sum(res.fun ** 2) / dof)

    try:
        cov_all = np.linalg.inv((res.jac.T @ res.jac).toarray())
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

    # Tangent east/north offsets are arcsec; catalogue RA has no cos(dec) factor.
    covariance = cov_all[:2, :2]
    to_deg = np.diag([1.0 / (3600.0 * cos_dec0), 1.0 / 3600.0])
    covariance_radec = to_deg @ covariance @ to_deg.T
    diagnostics = []
    offset = 0
    for u in usable:
        n = len(u["iv"])
        chi2 = float(np.sum(res.fun[offset:offset + n] ** 2))
        diagnostics.append({"frame_id": u["frame_id"], "n_pixels": n,
                            "chi2": chi2, "chi2_per_pixel": chi2 / n})
        offset += n

    mjds = [float(u["mjd"]) for u in usable if u["mjd"] is not None]
    return {
        "status": "ok",
        "ra_deg": ra_out,
        "dec_deg": dec_out,
        "epoch_mid_mjd": float((min(mjds) + max(mjds)) / 2) if mjds else None,
        "chi2_nu": chi2_nu,
        "chi2": float(np.sum(res.fun ** 2)),
        "dof": dof,
        "n_input": len(frames),
        "n_used": len(usable),
        "n_excluded": len(excluded),
        "excluded": excluded,
        "ellipse_arcsec": ellipse_arcsec,
        "covariance_tangent_arcsec2": covariance.tolist(),
        "covariance_radec_deg2": covariance_radec.tolist(),
        "frame_diagnostics": diagnostics,
        "uncertainty_note": "formal image-variance covariance; WCS systematics not included",
        "model_note": "constant sky position within pass; no within-pass proper-motion model",
        "frame_fluxes": [
            {"frame_id": u["frame_id"], "flux": float(res.x[2 + 2 * k]),
             "background": float(res.x[3 + 2 * k]), "cwave_um": u["cwave_um"]}
            for k, u in enumerate(usable)
        ],
    }


def write_pass_position(result: dict[str, Any], output_path: str | Path) -> None:
    """Write a strict JSON task product; NaN/Infinity cannot become catalogue values."""
    payload = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)
    Path(output_path).write_text(payload + "\n", encoding="utf-8")


def joint_fit_summary(result: dict) -> dict:
    """Summarise a fit_joint_pass result dict."""
    if not result or result.get("status") not in ("ok", "converged"):
        return {"status": result.get("status", "unknown"), "n_frames": 0, "converged": False}
    return {
        "status": result.get("status"),
        "n_frames": result.get("n_frames", 0),
        "n_excluded": result.get("n_excluded", 0),
        "converged": result.get("status") in ("ok", "converged"),
    }


if __name__ == "__main__":
    summary = joint_fit_summary({"status": "no_data"})
    print(f"joint_fit_summary (no_data): {summary}")
    assert not summary["converged"]
    print("03-06 joint_fit: OK")
