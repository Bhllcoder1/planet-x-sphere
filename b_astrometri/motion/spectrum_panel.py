"""
Spectrum / light-curve viewer panel for RW Aurigae and R Draconis.
Minimum required: per-pass flux vs wavelength + per-lambda flux vs MJD.
[PARTIAL] Real lambda-binned data from 04-12/H-12 needed; layout logic complete.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np


PANEL_TARGETS = ["RW_Aur", "R_Dra"]
LAMBDA_EDGES_UM = [0.75, 1.0, 1.5, 2.0, 2.5, 3.5, 5.0]  # 6 coarse SPHEREx bins


@dataclass
class PanelDataset:
    target: str
    mjd: np.ndarray            # shape (N_obs,)
    lambda_centers_um: np.ndarray  # shape (N_lam,)
    flux_grid: np.ndarray      # shape (N_obs, N_lam)
    flux_err_grid: np.ndarray  # shape (N_obs, N_lam)


@dataclass
class PanelSpec:
    """Declarative spec for the spectrum/light-curve panel."""
    target: str
    panel_type: str            # "spectrum" | "lightcurve" | "combined"
    x_axis: str                # "lambda_um" | "mjd"
    y_axis: str = "flux_adu"
    highlight_variable_bins: bool = True
    variability_threshold: float = 1.5  # chi2/dof above which bin is flagged


def build_spectrum_panel_spec(target: str) -> PanelSpec:
    """Return the panel spec for the spectrum view (flux vs wavelength)."""
    if target not in PANEL_TARGETS:
        raise ValueError(f"Unknown target {target!r}; expected one of {PANEL_TARGETS}")
    return PanelSpec(
        target=target,
        panel_type="spectrum",
        x_axis="lambda_um",
        highlight_variable_bins=(target == "RW_Aur"),
    )


def build_lightcurve_panel_spec(target: str) -> PanelSpec:
    """Return the panel spec for the light-curve view (flux vs MJD per bin)."""
    if target not in PANEL_TARGETS:
        raise ValueError(f"Unknown target {target!r}; expected one of {PANEL_TARGETS}")
    return PanelSpec(
        target=target,
        panel_type="lightcurve",
        x_axis="mjd",
        highlight_variable_bins=True,
    )


def render_panel_data(
    dataset: PanelDataset, spec: PanelSpec
) -> Dict:
    """Compute display-ready data for the requested panel.

    Returns a dict suitable for JSON serialisation and viewer consumption.
    """
    n_obs, n_lam = dataset.flux_grid.shape
    result: Dict = {
        "target": dataset.target,
        "panel_type": spec.panel_type,
        "n_obs": n_obs,
        "n_lam": n_lam,
        "variable_bins": [],
    }

    if spec.panel_type == "spectrum":
        # Mean spectrum across all observations
        mean_flux = np.nanmean(dataset.flux_grid, axis=0)
        err_flux = np.nanmean(dataset.flux_err_grid, axis=0) / max(np.sqrt(n_obs), 1)
        result["lambda_um"] = dataset.lambda_centers_um.tolist()
        result["mean_flux"] = mean_flux.tolist()
        result["mean_flux_err"] = err_flux.tolist()

    elif spec.panel_type == "lightcurve":
        result["mjd"] = dataset.mjd.tolist()
        result["per_bin"] = []
        for k in range(n_lam):
            lc = {
                "lambda_um": float(dataset.lambda_centers_um[k]),
                "flux": dataset.flux_grid[:, k].tolist(),
                "flux_err": dataset.flux_err_grid[:, k].tolist(),
            }
            result["per_bin"].append(lc)

    # Flag variable bins (chi2/dof > threshold)
    for k in range(n_lam):
        f = dataset.flux_grid[:, k]
        e = dataset.flux_err_grid[:, k]
        valid = e > 0
        if valid.sum() < 3:
            continue
        wm = float(np.average(f[valid], weights=1.0 / e[valid] ** 2))
        chi2 = float(np.sum(((f[valid] - wm) / e[valid]) ** 2) / (valid.sum() - 1))
        if chi2 > spec.variability_threshold:
            result["variable_bins"].append(
                {"bin_idx": k, "lambda_um": float(dataset.lambda_centers_um[k]), "chi2_dof": float(chi2)}
            )

    return result


def save_panel_json(data: Dict, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, indent=2), encoding="utf-8")


if __name__ == "__main__":
    rng = np.random.default_rng(55)
    edges = np.array(LAMBDA_EDGES_UM)
    lam_centers = (edges[:-1] + edges[1:]) / 2.0
    n_obs, n_lam = 18, len(lam_centers)
    mjd = np.sort(rng.uniform(60100, 60300, n_obs))

    # RW Aur: variable at short wavelengths
    flux = rng.uniform(80, 120, (n_obs, n_lam))
    flux[:, 0] *= rng.uniform(0.4, 2.5, n_obs)
    flux_err = np.abs(rng.normal(5, 1, (n_obs, n_lam)))

    ds = PanelDataset("RW_Aur", mjd, lam_centers, flux, flux_err)

    spec_sp = build_spectrum_panel_spec("RW_Aur")
    out_sp = render_panel_data(ds, spec_sp)
    print(f"Spectrum panel — variable bins: {out_sp['variable_bins']}")

    spec_lc = build_lightcurve_panel_spec("RW_Aur")
    out_lc = render_panel_data(ds, spec_lc)
    print(f"Lightcurve panel — {len(out_lc['per_bin'])} bins, {out_lc['n_obs']} obs")

    # R Dra (Mira-type, long-period — less variable at short lambda)
    flux_rdra = rng.uniform(60, 90, (n_obs, n_lam))
    flux_rdra[:, -1] *= rng.uniform(0.8, 1.3, n_obs)
    ds_rdra = PanelDataset("R_Dra", mjd, lam_centers, flux_rdra, flux_err)
    out_rdra = render_panel_data(ds_rdra, build_spectrum_panel_spec("R_Dra"))
    print(f"R Dra spectrum panel — variable bins: {out_rdra['variable_bins']}")

    print("10-12 spectrum_panel: OK")
