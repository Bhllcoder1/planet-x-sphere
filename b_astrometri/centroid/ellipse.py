"""03-04: 2x2 konum kovaryansindan hata elipsi (piksel cercevesi, 0 tabanli).

Elips piksel cercevesinde saklanir; gok cercevesine donusum kare basina roll
gerektirir. Centroid belirsizligi (sig_cent) WCS duzeltme belirsizligi
(sig_corr, 03-09) ile karistirilmaz: ikisi ayri alanlarda tutulur.

2B Gauss'ta k-sigma elipsin kapsama olasiligi 1 - exp(-k^2/2) olur:
1 sigma -> %39,3 (%68 degil), 2 sigma -> %86,5.
"""
from __future__ import annotations

import math

import numpy as np


def coverage_probability(k: float) -> float:
    """2B Gauss'ta k-sigma elipsin icine dusme olasiligi."""
    return 1.0 - math.exp(-0.5 * k * k)


def error_ellipse(cov, k: float = 1.0) -> dict:
    """cov: 2x2 [[sxx, sxy],[sxy, syy]] (piksel^2). k-sigma elips parametreleri.

    Donus: a (buyuk yari eksen), b (kucuk), theta (x ekseninden radyan,
    (-pi/2, pi/2]), sig_x, sig_y, rho.
    """
    c = np.asarray(cov, dtype=float)
    if c.shape != (2, 2) or not np.all(np.isfinite(c)):
        raise ValueError("cov sonlu 2x2 olmali")
    if abs(c[0, 1] - c[1, 0]) > 1e-12 * max(1.0, np.abs(c).max()):
        raise ValueError("cov simetrik olmali")
    if k <= 0:
        raise ValueError("k > 0 olmali")
    sxx, syy, sxy = float(c[0, 0]), float(c[1, 1]), float(0.5 * (c[0, 1] + c[1, 0]))
    if sxx < 0 or syy < 0:
        raise ValueError("kosegen negatif olamaz")
    vals = np.linalg.eigvalsh(np.array([[sxx, sxy], [sxy, syy]]))
    if vals[0] < -1e-12 * max(1.0, vals[1]):
        raise ValueError("cov pozitif yari-tanimli degil")
    lam1, lam2 = float(max(vals[1], 0.0)), float(max(vals[0], 0.0))
    theta = 0.5 * math.atan2(2.0 * sxy, sxx - syy)
    sig_x, sig_y = math.sqrt(sxx), math.sqrt(syy)
    rho = sxy / (sig_x * sig_y) if sig_x > 0 and sig_y > 0 else 0.0
    return {
        "sig_x": sig_x, "sig_y": sig_y, "rho": rho,
        "a": k * math.sqrt(lam1), "b": k * math.sqrt(lam2), "theta": theta,
        "k": k, "coverage": coverage_probability(k),
    }


def catalog_fields(cov) -> dict:
    """cat.json alanlari: sig_x, sig_y, rho, a1, b1, theta (+ a2, b2 kesikli 2 sigma)."""
    e1, e2 = error_ellipse(cov, 1.0), error_ellipse(cov, 2.0)
    return {
        "sig_x": e1["sig_x"], "sig_y": e1["sig_y"], "rho": e1["rho"],
        "a1": e1["a"], "b1": e1["b"], "theta": e1["theta"],
        "a2": e2["a"], "b2": e2["b"],
    }


def position_catalog_record(x, y, centroid_covariance, *, frame_id,
                            coordinate_frame, covariance_unit,
                            wcs_correction=None, independent_errors=False):
    """Serialize a centered native-pixel position with separate error budgets.

Centroid covariance is 2x2 in (x,y) order. coordinate_frame is explicitly
parent_native_pixel or cutout_native_pixel; covariance_unit must be pixel^2.
wcs_correction, when present, needs covariance, frame_id, coordinate_frame and
covariance_unit keys. No sky/display conversion is performed. Only an explicit
independent_errors=True permits adding the two covariance matrices.
"""
    x, y = float(x), float(y)
    if not (math.isfinite(x) and math.isfinite(y)):
        raise ValueError("Position must contain finite native float coordinates")
    if not isinstance(frame_id, str) or not frame_id.strip():
        raise ValueError("An explicit nonempty frame_id is required")
    if coordinate_frame not in {"parent_native_pixel", "cutout_native_pixel"}:
        raise ValueError("Declare parent_native_pixel or cutout_native_pixel coordinates")
    if covariance_unit != "pixel^2":
        raise ValueError("Covariance must already be in native pixel^2")
    if not isinstance(independent_errors, bool):
        raise ValueError("independent_errors must be an explicit boolean")

    def component(covariance):
        error_ellipse(covariance)  # Validate without assuming upstream covariance.
        matrix = np.asarray(covariance, dtype=float)
        matrix = (matrix + matrix.T) / 2
        full_rank = bool(np.linalg.det(matrix) > 0)
        ellipses = {}
        for k in (1, 2):
            ellipse = error_ellipse(matrix, k)
            ellipses[f"{k}sigma"] = {
                "center_x": x, "center_y": y,
                "a": float(ellipse["a"]), "b": float(ellipse["b"]),
                "theta": float(ellipse["theta"]), "k": k,
                "line_style": "solid" if k == 1 else "dashed",
                "nominal_gaussian_coverage": float(ellipse["coverage"]) if full_rank else None,
            }
        return {"covariance": matrix.tolist(), **catalog_fields(matrix),
                "ellipses": ellipses, "degenerate_covariance": not full_rank}

    centroid = component(centroid_covariance)
    correction, total = None, None
    total_status = "not_available_no_wcs_covariance"
    if wcs_correction is not None:
        required = {"covariance", "frame_id", "coordinate_frame", "covariance_unit"}
        missing = required - wcs_correction.keys()
        if missing:
            raise ValueError(f"Incomplete WCS correction covariance: {sorted(missing)}")
        if (wcs_correction["frame_id"] != frame_id
                or wcs_correction["coordinate_frame"] != coordinate_frame
                or wcs_correction["covariance_unit"] != covariance_unit):
            raise ValueError("WCS covariance must share the position's frame, axes and pixel^2 units")
        correction = component(wcs_correction["covariance"])
        total_status = "not_combined_independence_not_declared"
        if independent_errors:
            summed = np.asarray(centroid["covariance"]) + np.asarray(correction["covariance"])
            total = component(summed)
            total_status = "sum_under_caller_declared_independence"
    elif independent_errors:
        raise ValueError("Cannot combine independent errors without WCS correction covariance")
    return {
        "frame_id": frame_id, "x": x, "y": y, "coordinate_frame": coordinate_frame,
        "pixel_origin": 0, "position_unit": "pixel", "covariance_unit": covariance_unit,
        "ellipse_axis_unit": "pixel", "theta_unit": "radian",
        "theta_reference": "+x toward +y in supplied native pixel frame",
        "coverage_model": "full-rank 2D Gaussian Mahalanobis contour, not 1D 68 percent",
        "centroid_uncertainty": centroid, "wcs_correction_uncertainty": correction,
        "total_uncertainty": total, "total_status": total_status,
        "independence_declared_by_caller": independent_errors,
    }
