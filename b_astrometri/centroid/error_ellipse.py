"""
Compute 1σ/2σ error ellipse parameters from a 2×2 covariance matrix.
[PARTIAL] prototype; H-04 (real joint-fit covariance output) needed for end-to-end test.
"""
from __future__ import annotations
import math
import numpy as np
from dataclasses import dataclass


@dataclass
class ErrorEllipse:
    a: float          # semi-major axis (px), 1σ
    b: float          # semi-minor axis (px), 1σ
    pa_deg: float     # position angle of semi-major axis, degrees E of N
    cov: list         # [[cxx, cxy],[cyx, cyy]] raw covariance

    def scale(self, sigma: float = 2.0) -> "ErrorEllipse":
        """Return ellipse scaled to `sigma` standard deviations."""
        return ErrorEllipse(
            a=self.a * sigma,
            b=self.b * sigma,
            pa_deg=self.pa_deg,
            cov=self.cov,
        )

    def to_dict(self) -> dict:
        return {
            "a_1sigma_px": round(self.a, 6),
            "b_1sigma_px": round(self.b, 6),
            "pa_deg": round(self.pa_deg, 4),
            "a_2sigma_px": round(self.a * 2, 6),
            "b_2sigma_px": round(self.b * 2, 6),
        }


def ellipse_from_cov(cov: np.ndarray) -> ErrorEllipse:
    """Compute 1σ error ellipse from a 2×2 covariance matrix.

    Parameters
    ----------
    cov : (2,2) array  [[var_x, cov_xy], [cov_xy, var_y]]

    Returns
    -------
    ErrorEllipse with semi-axes in pixels and position angle in degrees.
    """
    if cov.shape != (2, 2):
        raise ValueError(f"cov must be (2,2), got {cov.shape}")

    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    # Sort descending
    order = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]

    # Semi-axes: sqrt of eigenvalues
    a = float(math.sqrt(max(eigenvalues[0], 0.0)))
    b = float(math.sqrt(max(eigenvalues[1], 0.0)))

    # Position angle of semi-major axis (from y-axis, degrees)
    vx, vy = eigenvectors[:, 0]
    pa_rad = math.atan2(float(vx), float(vy))
    pa_deg = math.degrees(pa_rad) % 180.0

    return ErrorEllipse(a=a, b=b, pa_deg=pa_deg, cov=cov.tolist())


if __name__ == "__main__":
    # Test: circular Gaussian → a ≈ b ≈ σ
    cov_circ = np.array([[0.04, 0.0], [0.0, 0.04]])
    e = ellipse_from_cov(cov_circ)
    assert abs(e.a - 0.2) < 1e-9, f"expected a=0.2, got {e.a}"
    assert abs(e.b - 0.2) < 1e-9, f"expected b=0.2, got {e.b}"
    print(f"Circular: a={e.a:.4f}, b={e.b:.4f}, pa={e.pa_deg:.1f}°")

    # Test: elongated
    cov_elong = np.array([[0.09, 0.0], [0.0, 0.01]])
    e2 = ellipse_from_cov(cov_elong)
    assert e2.a > e2.b, "semi-major must be larger"
    print(f"Elongated: a={e2.a:.4f} b={e2.b:.4f} pa={e2.pa_deg:.1f}°")
    print(e2.scale(2.0).to_dict())
    print("03-04 error_ellipse: OK")
