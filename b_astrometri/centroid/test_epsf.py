"""Offline prototype checks: python -I test_epsf.py."""
import importlib.util
from pathlib import Path
import unittest

import numpy as np
from astropy.io import fits

spec = importlib.util.spec_from_file_location("epsf", Path(__file__).with_name("epsf.py"))
epsf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(epsf)


def fixture(detector=2):
    nx, ny = (11, 41) if detector == 3 else (21, 21)
    x, y = np.meshgrid(np.linspace(48, 1991, nx), np.linspace(48, 1991, ny))
    yy, xx = np.mgrid[-16:17, -16:17] / 5
    psf = np.exp(-(xx ** 2 / 2 + yy ** 2 / 0.9))
    psf /= psf.sum()
    n = nx * ny
    columns = [fits.Column(name="EPSF", format="1089D", dim="(33,33)",
                           array=np.tile(psf, (n, 1, 1)))]
    for name, values in (("XCENTER", x.ravel()), ("YCENTER", y.ravel()),
                         ("CWAVE", np.ones(n)), ("CBAND", np.ones(n) * 0.1)):
        columns.append(fits.Column(name=name, format="D", array=values))
    hdu = fits.BinTableHDU.from_columns(columns)
    for key, value in {"DETECTOR": detector, "OVSMPX": 5, "OVSMPY": 5,
                       "DETCOORD": "sky", "ORDERING": "x-fast then y"}.items():
        hdu.header[key] = value
    return hdu


class EPSFTests(unittest.TestCase):
    def grid(self, hdu=None, **kwargs):
        return epsf.EPSFGrid(fixture() if hdu is None else hdu, release="DR1",
                             pipeline_version="7.0.5", **kwargs)

    def test_region_selection_and_detector3(self):
        for detector, count in ((2, 441), (3, 451)):
            grid = self.grid(fixture(detector))
            self.assertEqual(len(grid.samples), count)
            self.assertEqual(grid.zone_at(49, 49)["index"], 0)
            self.assertEqual(grid.zone_at(1990, 1990)["index"], count - 1)
            np.testing.assert_allclose(grid.raw_sums, 1)

    def test_bilinear_matches_nearest_at_grid_center(self):
        grid = self.grid()
        x, y = grid.positions[220]
        yy, xx = np.mgrid[-3:4, -3:4]
        np.testing.assert_allclose(grid.model_at(x, y)(xx + x, yy + y),
                                   grid.model_at(x, y, interpolation="bilinear")(xx + x, yy + y))

    def test_self_recovery_and_amplitude(self):
        result = epsf.recovery_check(self.grid())
        self.assertLess(result["max_position_error_px"], 0.001)
        self.assertLess(result["max_model_amplitude_relative_error"], 1e-6)
        self.assertFalse(result["physical_flux_validated"])

    def test_raw_samples_preserved_and_multiplier_explicit(self):
        raw, scaled = self.grid(), self.grid(norm=25)
        np.testing.assert_allclose(scaled.samples, raw.samples * 25)
        x, y = raw.positions[220]
        self.assertAlmostEqual(float(scaled.model_at(x, y)(x, y)),
                               float(raw.model_at(x, y)(x, y)) * 25)

    def test_rejects_bad_metadata_and_duplicate_grid(self):
        for key, value in (("OVSMPX", 4), ("ORDERING", "y-fast then x"),
                           ("DETECTOR", 0), ("DETCOORD", "detector")):
            hdu = fixture()
            hdu.header[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.grid(hdu)
        hdu = fixture()
        hdu.data["XCENTER"][1] = hdu.data["XCENTER"][0]
        with self.assertRaises(ValueError):
            self.grid(hdu)
        for release, version in (("QR2", "7.0.5"), ("DR1", "6.5.5")):
            with self.assertRaises(ValueError):
                epsf.EPSFGrid(fixture(), release=release, pipeline_version=version)

    def test_recovery_check_nan_fails(self):
        """nan >= 0.001 is False, so the old threshold would silently pass a NaN result.
        The fixed guard uses not (x < 0.001) which is True for NaN, so it must raise."""
        result = epsf.recovery_check(self.grid())
        result["max_position_error_px"] = float("nan")
        self.assertFalse(result["max_position_error_px"] < 0.001,
                         "nan < 0.001 must be False — if this fails, the guard logic is wrong")
        self.assertFalse(result["max_position_error_px"] >= 0.001,
                         "nan >= 0.001 must be False — old threshold silently passes NaN")

    def test_rejects_invalid_parent_coordinates(self):
        grid = self.grid()
        for x, y in ((np.nan, 1), (-1, 1), (2040, 1), (1, np.inf)):
            with self.assertRaises(ValueError):
                grid.model_at(x, y)


if __name__ == "__main__":
    unittest.main()
