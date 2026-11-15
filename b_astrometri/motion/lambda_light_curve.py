"""
Lambda-binned light curves for variable stars (RW Aur, R Dra).
[PARTIAL] H-12 (real SPHEREx λ-binned photometry) needed.
Provides binning and variability-index framework.
"""
from __future__ import annotations
import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class LambdaBin:
    lambda_min_um: float
    lambda_max_um: float
    mjd: np.ndarray            # shape (N,)
    flux: np.ndarray           # shape (N,)
    flux_err: np.ndarray       # shape (N,)

    @property
    def lambda_center_um(self) -> float:
        return (self.lambda_min_um + self.lambda_max_um) / 2.0

    def variability_index(self) -> float:
        """Stetson-J-like index; >1 → variable."""
        if len(self.flux) < 3:
            return 0.0
        wm = np.average(self.flux, weights=1.0 / self.flux_err**2)
        chi2 = np.sum(((self.flux - wm) / self.flux_err)**2)
        return float(chi2 / (len(self.flux) - 1))


@dataclass
class LightCurveResult:
    target: str
    bins: List[LambdaBin] = field(default_factory=list)
    notes: str = ""

    def variability_map(self) -> Dict[str, float]:
        return {
            f"{b.lambda_center_um:.2f}um": round(b.variability_index(), 3)
            for b in self.bins
        }


def build_light_curves(
    target: str,
    mjd: np.ndarray,
    flux_grid: np.ndarray,     # shape (N_obs, N_lambda)
    flux_err_grid: np.ndarray,
    lambda_edges_um: np.ndarray,  # shape (N_lambda+1,)
) -> LightCurveResult:
    """Build per-λ-bin light curves for a variable star target.

    Parameters
    ----------
    target : target name, e.g. 'RW_Aur' or 'R_Dra'
    mjd : MJD per observation, shape (N_obs,)
    flux_grid : flux per obs per λ-bin, shape (N_obs, N_lambda)
    flux_err_grid : same shape
    lambda_edges_um : bin edges in microns, length N_lambda+1
    """
    n_lambda = flux_grid.shape[1]
    bins = []
    for k in range(n_lambda):
        bins.append(LambdaBin(
            lambda_min_um=float(lambda_edges_um[k]),
            lambda_max_um=float(lambda_edges_um[k + 1]),
            mjd=mjd.copy(),
            flux=flux_grid[:, k].copy(),
            flux_err=flux_err_grid[:, k].copy(),
        ))
    return LightCurveResult(
        target=target,
        bins=bins,
        notes=f"[STUB] {len(bins)} λ-bins; real data from H-12 needed",
    )


if __name__ == "__main__":
    rng = np.random.default_rng(12)
    n_obs = 20
    # SPHEREx has 102 spectral channels; use 6 coarse bins for smoke test
    n_lambda = 6
    lambda_edges = np.array([0.75, 1.0, 1.5, 2.0, 2.5, 3.5, 5.0])
    mjd = np.sort(rng.uniform(60000, 60200, n_obs))
    # RW Aur: variable by factor ~2 at short λ
    base_flux = rng.uniform(50, 100, n_obs)
    flux_grid = np.outer(base_flux, np.ones(n_lambda)) + rng.normal(0, 5, (n_obs, n_lambda))
    flux_grid[:, 0] *= rng.uniform(0.5, 2.0, n_obs)  # inject variability in bin 0
    flux_err_grid = np.abs(rng.normal(5, 1, (n_obs, n_lambda)))

    result = build_light_curves("RW_Aur", mjd, flux_grid, flux_err_grid, lambda_edges)
    print(f"Target: {result.target}, bins: {len(result.bins)}")
    print("Variability map:", result.variability_map())
    print("04-12 lambda_light_curve: OK")
