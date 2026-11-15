"""03-06 reproducible synthetic coverage experiment; no real Barnard claims.

Run with the Stage 0 environment's Python -I and an external --output path.
The synthetic ePSF fixture is shared with test_joint_fit.py, not downloaded data.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys
import time

import numpy as np

# -I omits the script directory; load only this explicit trusted source directory.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from joint_fit import fit_joint_pass
from test_epsf import EPSFTests, fixture
from test_joint_fit import _rotated_wcs


def run(trials: int, seed: int, output: Path) -> dict:
    if trials < 1:
        raise ValueError("trials must be positive")
    started = time.perf_counter()
    grid = EPSFTests().grid(fixture(detector=2), norm=1.0)
    truth = (269.4523, 4.6931)
    initial = (truth[0] + 1e-4, truth[1] - 1e-4)
    frames = []
    clean_images = []
    for k in range(20):
        wcs = _rotated_wcs(269.452, 4.693, roll_deg=k * 0.2)
        x, y = (float(v) for v in wcs.all_world2pix(*truth, 0))
        yy, xx = np.mgrid[-4:5, -4:5] + np.array([[[float(int(y))]], [[float(int(x))]]])
        clean = grid.model_at(x, y).evaluate(xx, yy, 2000. + 50. * k, x, y) + 8. + 0.5 * k
        clean_images.append(clean)
        frames.append({"frame_id": f"f_{k}", "grid": grid, "wcs": wcs,
                       "xx": xx, "yy": yy, "image": clean,
                       "variance": np.full_like(clean, 4.), "mjd": 60100. + k * 0.5,
                       "cwave_um": 1. + 0.05 * k})
    expected = 1. - math.exp(-0.5)
    rows = []

    def snapshot() -> dict:
        successful = [r for r in rows if r["status"] == "ok"]
        count = sum(r["mahalanobis_squared"] <= 1. for r in successful)
        n = len(successful)
        value = {"task": "03-06", "kind": "synthetic_only", "seed": seed,
                 "rng": "numpy.default_rng(SeedSequence([seed, trial_index]))",
                 "requested_trials": trials, "completed_trials": len(rows),
                 "successful_trials": n, "failed_trials": len(rows) - n,
                 "frames_per_trial": 20, "pixels_per_frame": 81,
                 "noise_sigma": 2., "input_variance": 4.,
                 "truth_ra_dec_deg": list(truth), "initial_ra_dec_deg": list(initial),
                 "coverage_ellipse_k": 1., "inside_count": count,
                 "coverage_fraction": count / n if n else None,
                 "expected_2d_gaussian_coverage": expected,
                 "expected_binomial_standard_error": math.sqrt(expected * (1. - expected) / n) if n else None,
                 "mean_formal_covariance_tangent_arcsec2": np.mean([r["covariance_tangent_arcsec2"] for r in successful], axis=0).tolist() if n else None,
                 "median_single_to_joint_sigma_ratio": np.median([r["single_to_joint_sigma_ratio"] for r in successful], axis=0).tolist() if n else None,
                 "elapsed_seconds": time.perf_counter() - started,
                 "complete": len(rows) == trials,
                 "limitations": ["synthetic fixed-source model only", "same ePSF for generation and fitting",
                                 "no WCS error or within-pass proper motion", "not real Barnard acceptance"],
                 "trials": rows}
        output.parent.mkdir(parents=True, exist_ok=True)
        temporary = output.with_name(output.name + ".tmp")
        temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")
        temporary.replace(output)
        return value

    for trial in range(trials):
        rng = np.random.default_rng(np.random.SeedSequence([seed, trial]))
        noisy = [{**frame, "image": clean + rng.normal(0., 2., clean.shape)}
                 for frame, clean in zip(frames, clean_images)]
        single = fit_joint_pass(noisy[:1], *initial)
        joint = fit_joint_pass(noisy, *initial)
        if single["status"] != "ok" or joint["status"] != "ok":
            rows.append({"trial": trial, "status": "fit_failed",
                         "single_status": single["status"], "joint_status": joint["status"]})
        else:
            delta = np.array([((joint["ra_deg"] - truth[0] + 180.) % 360. - 180.)
                              * math.cos(math.radians(initial[1])) * 3600.,
                              (joint["dec_deg"] - truth[1]) * 3600.])
            covariance = np.asarray(joint["covariance_tangent_arcsec2"])
            q = float(delta @ np.linalg.solve(covariance, delta))
            rows.append({"trial": trial, "status": "ok", "mahalanobis_squared": q,
                         "position_error_tangent_arcsec": delta.tolist(),
                         "covariance_tangent_arcsec2": covariance.tolist(),
                         "single_to_joint_sigma_ratio": [single["ellipse_arcsec"][key] / joint["ellipse_arcsec"][key]
                                                          for key in ("sig_x", "sig_y")],
                         "chi2_nu": joint["chi2_nu"]})
        if (trial + 1) % 25 == 0 or trial + 1 == trials:
            result = snapshot()
            print(json.dumps({key: result[key] for key in ("completed_trials", "successful_trials", "coverage_fraction", "elapsed_seconds")}), flush=True)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trials", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=55)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.trials, args.seed, args.output)
