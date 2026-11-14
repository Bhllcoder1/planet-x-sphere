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
