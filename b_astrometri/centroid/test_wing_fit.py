import math
import importlib
import unittest

import numpy as np

from wing_fit import fit_epsf_wing

epsf_tests = importlib.import_module("test_epsf")


class WingFitTests(unittest.TestCase):
    def test_artificial_core_mask_matches_within_3sigma_and_widens_uncertainty(self):
        grid = getattr(epsf_tests, "EPSFTests")().grid(epsf_tests.fixture(detector=2), norm=1.0)
        rng = np.random.default_rng(7)
        cx, cy = grid.positions[220] + np.array([0.23, -0.17])
        yy, xx = np.mgrid[-4:5, -4:5] + np.array([[[cy]], [[cx]]])
        clean = grid.model_at(cx, cy).evaluate(xx, yy, 5000.0, cx, cy) + 10.0
        var = np.full_like(clean, 4.0)
        noisy = clean + rng.normal(0.0, 2.0, size=clean.shape)

        full = fit_epsf_wing(grid, xx, yy, noisy, var, float(cx + 0.05), float(cy - 0.05))
        self.assertEqual(full["status"], "ok")
        self.assertFalse(full["saturated_fit"])

        # 2x2 merkezi NaN + OVERFLOW (bit 1) ile maskele
        masked_img = noisy.copy()
        masked_var = var.copy()
        flags = np.zeros_like(noisy, dtype=np.int64)
        masked_img[3:5, 3:5] = np.nan
        masked_var[3:5, 3:5] = np.nan
        flags[3:5, 3:5] |= (1 << 1)

        wing = fit_epsf_wing(
            grid, xx, yy, masked_img, masked_var,
            float(cx + 0.05), float(cy - 0.05), flags=flags,
        )
        self.assertEqual(wing["status"], "ok")
        self.assertTrue(wing["saturated_fit"])
        self.assertGreater(wing["sig_x"], full["sig_x"])
        self.assertGreater(wing["sig_y"], full["sig_y"])
        dx = abs(wing["x"] - full["x"])
        dy = abs(wing["y"] - full["y"])
        self.assertLessEqual(dx, 3.0 * wing["sig_x"])
        self.assertLessEqual(dy, 3.0 * wing["sig_y"])
        self.assertLess(math.hypot(wing["x"] - cx, wing["y"] - cy), 0.15)

    def test_over_half_masked_returns_unmeasurable(self):
        grid = getattr(epsf_tests, "EPSFTests")().grid(epsf_tests.fixture(detector=2), norm=1.0)
        cx, cy = grid.positions[220]
        yy, xx = np.mgrid[-4:5, -4:5] + np.array([[[cy]], [[cx]]])
        img = np.full_like(xx, 10.0)
        var = np.ones_like(xx)
        img[:5, :] = np.nan  # 45/81 > %50
        res = fit_epsf_wing(grid, xx, yy, img, var, float(cx), float(cy))
        self.assertEqual(res["status"], "unmeasurable")
        self.assertTrue(res["saturated_fit"])


if __name__ == "__main__":
    unittest.main()
