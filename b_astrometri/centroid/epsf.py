"""03-01 prototype: SPHEREx parent-coordinate ePSF models, before 02-03/02-12 integration.

PSF_NORM=1 preserves stored samples. Physical flux normalization and orientation
remain unvalidated until 03-02; fitted flux is a model amplitude, not calibrated flux.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from astropy.io import fits
from astropy.nddata import NDData
from photutils.psf import GriddedPSFModel, ImagePSF

PSF_NORM = 1.0


class EPSFGrid:
    def __init__(self, hdu, *, release, pipeline_version, norm=PSF_NORM):
        if release.upper() not in {"QR3", "DR1"}:
            raise ValueError("Only explicitly identified QR3/DR1 products are supported")
        try:
            version = tuple(int(p) for p in pipeline_version.split("."))
        except (AttributeError, ValueError) as error:
            raise ValueError("Missing or invalid pipeline VERSION") from error
        if version < (6, 5, 6):
            raise ValueError("Pipeline predates ePSF axis-order correction")
        header = hdu.header
        self.detector = int(header["DETECTOR"])
        if self.detector not in range(1, 7):
            raise ValueError("Unsupported detector")
        if header.get("DETCOORD") != "sky" or header.get("ORDERING") != "x-fast then y":
            raise ValueError("Unsupported ePSF coordinate/order convention")
        self.oversampling = (int(header["OVSMPY"]), int(header["OVSMPX"]))
        if self.oversampling != (5, 5):
            raise ValueError("Expected 5x5 oversampling")
        if not np.isfinite(norm) or norm <= 0:
            raise ValueError("Normalization multiplier must be finite and positive")
        data = hdu.data
        required = {"EPSF", "XCENTER", "YCENTER", "CWAVE", "CBAND"}
        if not required.issubset(data.names):
            raise ValueError("Missing ePSF data columns")
        self.positions = np.column_stack((data["XCENTER"], data["YCENTER"])).astype(float)
        self.samples = np.array(data["EPSF"], dtype=float, copy=True)
        expected = 451 if self.detector == 3 else 441
        if self.samples.shape != (expected, 33, 33):
            raise ValueError(f"Expected {expected} regions of 33x33 samples")
        if not np.isfinite(self.samples).all() or not np.isfinite(self.positions).all():
            raise ValueError("Non-finite ePSF samples or region centers")
        nx, ny = len(np.unique(self.positions[:, 0])), len(np.unique(self.positions[:, 1]))
        if (nx, ny) != ((11, 41) if self.detector == 3 else (21, 21)):
            raise ValueError("Unexpected detector region grid dimensions")
        if len(np.unique(self.positions, axis=0)) != expected:
            raise ValueError("Duplicate or missing region centers")
        self.raw_sums = self.samples.sum(axis=(1, 2))
        if np.any(self.raw_sums <= 0):
            raise ValueError("Non-positive ePSF sample sum")
        self.samples *= norm
        self.norm = float(norm)
        self.cwave = np.array(data["CWAVE"], dtype=float, copy=True)
        self.cband = np.array(data["CBAND"], dtype=float, copy=True)
        if not np.isfinite(self.cwave).all() or not np.isfinite(self.cband).all():
            raise ValueError("Non-finite spectral metadata")
        self.release = release.upper()
        self.pipeline_version = pipeline_version
        # FITS x-fast samples are already exposed by Astropy as [y, x].
        self.gridded = GriddedPSFModel(NDData(self.samples, meta={
            "grid_xypos": self.positions.tolist(), "oversampling": self.oversampling}))

    @classmethod
    def read(cls, path, *, release, norm=PSF_NORM):
        with fits.open(path, memmap=False) as hdus:
            return cls(hdus["EPSF"], release=release,
                       pipeline_version=hdus[0].header.get("VERSION"), norm=norm)

    def zone_at(self, x_parent, y_parent):
        if not np.isfinite([x_parent, y_parent]).all():
            raise ValueError("Parent coordinates must be finite")
        if not (0 <= x_parent < 2040 and 0 <= y_parent < 2040):
            raise ValueError("Parent coordinates outside 2040x2040 detector")
        index = int(np.argmin(np.sum((self.positions - [x_parent, y_parent]) ** 2, axis=1)))
        return {"index": index, "x": float(self.positions[index, 0]),
                "y": float(self.positions[index, 1]), "cwave_um": float(self.cwave[index]),
                "cband_um": float(self.cband[index])}

    def model_at(self, x_parent, y_parent, *, interpolation="nearest"):
        """Return a fresh model evaluated on 0-based parent-pixel coordinates."""
        zone = self.zone_at(x_parent, y_parent)
        if interpolation == "nearest":
            return ImagePSF(self.samples[zone["index"]], oversampling=self.oversampling,
                            x_0=x_parent, y_0=y_parent)
        if interpolation == "bilinear":
            model = self.gridded.copy()
            model.x_0, model.y_0 = x_parent, y_parent
            return model
        raise ValueError("Interpolation must be nearest or bilinear")


def recovery_check(grid):
    """Noiseless self-consistency only; not independent orientation/flux validation."""
    from scipy.optimize import least_squares
    center = grid.positions[len(grid.positions) // 2]
    yy, xx = np.mgrid[-4:5, -4:5] + center[:, None, None][::-1]
    errors, flux_errors = [], []
    for dx, dy in ((0.0, 0.0), (0.1, 0.9), (0.7, 0.3)):
        x, y = center + [dx, dy]
        model = grid.model_at(x, y)
        image = model.evaluate(xx, yy, 123.0, x, y)
        fit = least_squares(lambda p: (model.evaluate(xx, yy, p[2], p[0], p[1]) - image).ravel(),
                            [x + 0.08, y - 0.06, 110.0],
                            xtol=1e-12, ftol=1e-12, gtol=1e-12)
        errors.append(float(np.hypot(fit.x[0] - x, fit.x[1] - y)))
        flux_errors.append(float(abs(fit.x[2] / 123.0 - 1)))
    return {"max_position_error_px": max(errors),
            "max_model_amplitude_relative_error": max(flux_errors),
            "physical_flux_validated": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fits", type=Path)
    parser.add_argument("--release", choices=["QR3", "DR1"], required=True)
    args = parser.parse_args()
    grid = EPSFGrid.read(args.fits, release=args.release)
    result = {"regions": len(grid.samples), "detector": grid.detector,
              "sample_shape": list(grid.samples.shape[1:]), "oversampling": grid.oversampling,
              "raw_sum_min": float(grid.raw_sums.min()), "raw_sum_max": float(grid.raw_sums.max()),
              "norm_multiplier": grid.norm, "normalization_validation": "pending 03-02",
              "integration": "pending 02-03 and 02-12", **recovery_check(grid)}
    print(json.dumps(result, indent=2))
    if not (result["max_position_error_px"] < 0.001):  # NaN-safe: nan>=0.001 is False but nan<0.001 is also False
        raise SystemExit("Self-recovery failed")
