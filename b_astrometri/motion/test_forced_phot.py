import sys
import importlib
import unittest
from pathlib import Path

import numpy as np

CENTROID_DIR = str(Path(__file__).resolve().parents[1] / "centroid")
if CENTROID_DIR not in sys.path:
    sys.path.insert(0, CENTROID_DIR)

from forced_phot import combine_forced_flux, forced_phot_frame  # noqa: E402
epsf_tests = importlib.import_module("test_epsf")


class ForcedPhotTests(unittest.TestCase):
    def test_injected_constant_star_rms_over_sigma(self):
        grid = getattr(epsf_tests, "EPSFTests")().grid(epsf_tests.fixture(detector=2), norm=1.0)
        rng = np.random.default_rng(101)
        cx, cy = grid.positions[220] + np.array([0.31, -0.22])
        yy, xx = np.mgrid[-4:5, -4:5] + np.array([[[cy]], [[cx]]])
        true_flux, true_bg = 250.0, 12.0
        clean = grid.model_at(cx, cy).evaluate(xx, yy, true_flux, cx, cy) + true_bg
        var = np.full_like(clean, 2.25)

        fluxes, sigmas = [], []
        for _ in range(120):
            noisy = clean + rng.normal(0.0, 1.5, size=clean.shape)
            res = forced_phot_frame(grid, xx, yy, noisy, var, float(cx), float(cy))
            self.assertEqual(res["status"], "ok")
            self.assertFalse(res["bad_fit"])
            self.assertFalse(res["saturated_fit"])
            fluxes.append(res["flux"])
            sigmas.append(res["sigma_flux"])

        rms = float(np.sqrt(np.mean((np.array(fluxes) - true_flux) ** 2)))
        ros = rms / float(np.mean(sigmas))
        self.assertGreaterEqual(ros, 0.8)
        self.assertLessEqual(ros, 1.25)

        coadd = combine_forced_flux([
            {"status": "ok", "flux": f, "sigma_flux": s} for f, s in zip(fluxes, sigmas)
        ])
        self.assertEqual(coadd["status"], "ok")
        self.assertLess(abs(coadd["flux"] - true_flux), 3.0 * coadd["sigma_flux"])

    def test_bad_fit_chi2_over_5_returns_none_flux(self):
        grid = getattr(epsf_tests, "EPSFTests")().grid(epsf_tests.fixture(detector=2), norm=1.0)
        cx, cy = grid.positions[220]
        yy, xx = np.mgrid[-4:5, -4:5] + np.array([[[cy]], [[cx]]])
        img = np.zeros_like(xx)
        img[0, 0] = 1000.0  # PSF disi sert aykiri piksel -> yuksek chi2_nu
        var = np.ones_like(xx)
        res = forced_phot_frame(grid, xx, yy, img, var, float(cx), float(cy))
        self.assertEqual(res["status"], "bad_fit")
        self.assertTrue(res["bad_fit"])
        self.assertIsNone(res["flux"])
        self.assertIsNone(res["sigma_flux"])

    def test_nan_core_marks_saturated_fit(self):
        grid = getattr(epsf_tests, "EPSFTests")().grid(epsf_tests.fixture(detector=2), norm=1.0)
        cx, cy = grid.positions[220]
        yy, xx = np.mgrid[-4:5, -4:5] + np.array([[[cy]], [[cx]]])
        clean = grid.model_at(cx, cy).evaluate(xx, yy, 1000.0, cx, cy) + 5.0
        var = np.ones_like(clean)
        clean[3:5, 3:5] = np.nan
        res = forced_phot_frame(grid, xx, yy, clean, var, float(cx), float(cy))
        self.assertEqual(res["status"], "ok")
        self.assertTrue(res["saturated_fit"])
        self.assertAlmostEqual(res["flux"], 1000.0, places=5)

    def test_frame_metadata_cannot_override_fit_values(self):
        grid = getattr(epsf_tests, "EPSFTests")().grid(epsf_tests.fixture(detector=2), norm=1.0)
        cx, cy = grid.positions[220]
        yy, xx = np.mgrid[-4:5, -4:5] + np.array([[[cy]], [[cx]]])
        image = grid.model_at(cx, cy).evaluate(xx, yy, 250.0, cx, cy) + 12.0
        res = forced_phot_frame(
            grid, xx, yy, image, np.ones_like(image), float(cx), float(cy),
            frame_meta={"frame_id": "A", "status": "bad_fit", "flux": -1.0},
        )
        self.assertEqual(res["frame_id"], "A")
        self.assertEqual(res["status"], "ok")
        self.assertAlmostEqual(res["flux"], 250.0)

    def test_rejects_wrong_flag_shape_and_invalid_variance_scale(self):
        grid = getattr(epsf_tests, "EPSFTests")().grid(epsf_tests.fixture(detector=2), norm=1.0)
        cx, cy = grid.positions[220]
        yy, xx = np.mgrid[-4:5, -4:5] + np.array([[[cy]], [[cx]]])
        image, var = np.ones_like(xx), np.ones_like(xx)
        with self.assertRaises(ValueError):
            forced_phot_frame(grid, xx, yy, image, var, float(cx), float(cy), flags=np.zeros((2, 2)))
        with self.assertRaises(ValueError):
            forced_phot_frame(grid, xx, yy, image, var, float(cx), float(cy), var_scale=0.5)

    def test_coadd_ignores_nonfinite_measurements(self):
        out = combine_forced_flux([
            {"status": "ok", "flux": 250.0, "sigma_flux": 2.0},
            {"status": "ok", "flux": float("nan"), "sigma_flux": 1.0},
            {"status": "ok", "flux": 100.0, "sigma_flux": float("inf")},
        ])
        self.assertEqual(out["n_used"], 1)
        self.assertEqual(out["flux"], 250.0)
        self.assertEqual(out["sigma_flux"], 2.0)


if __name__ == "__main__":
    unittest.main()
