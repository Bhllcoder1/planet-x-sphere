import unittest

import numpy as np

from d5_check import compare_orientation, self_recovery_ladder
from test_epsf import EPSFTests, fixture


class D5CheckTests(unittest.TestCase):
    def test_norm_1_and_25_recovery_and_flux_scale(self):
        hdu = fixture(detector=2)
        g1 = EPSFTests().grid(hdu, norm=1.0)
        g25 = EPSFTests().grid(hdu, norm=25.0)
        r1 = self_recovery_ladder(g1)
        r25 = self_recovery_ladder(g25)
        self.assertTrue(r1["passed_recovery"])
        self.assertTrue(r25["passed_recovery"])
        self.assertLess(r1["max_pos_error_px"], 0.001)
        self.assertLess(r25["max_pos_error_px"], 0.001)

        # Sabit bir goruntuye x1 ve x25 modelleri uyarlandiginda aki genligi 25 kat degismeli.
        center = g1.positions[len(g1.positions) // 2]
        yy, xx = np.mgrid[-4:5, -4:5] + center[:, None, None][::-1]
        img = g1.model_at(center[0], center[1]).evaluate(xx, yy, 100.0, center[0], center[1])
        m25 = g25.model_at(center[0], center[1])
        from scipy.optimize import least_squares
        fit25 = least_squares(
            lambda p: (m25.evaluate(xx, yy, p[2], p[0], p[1]) - img).ravel(),
            [center[0], center[1], 4.0],
        )
        self.assertAlmostEqual(fit25.x[2], 4.0, places=4)

    def test_orientation_distinguishes_anisotropic_psf(self):
        # fixture() x ve y'de asimetrik Gauss (x^2/2 vs y^2/0.9) uretir.
        g = EPSFTests().grid(fixture(detector=2), norm=1.0)
        rng = np.random.default_rng(42)
        cutouts = []
        for _ in range(12):
            cx, cy = g.positions[220] + rng.uniform(-0.3, 0.3, size=2)
            yy, xx = np.mgrid[-4:5, -4:5] + np.array([[[cy]], [[cx]]])
            clean = g.model_at(cx, cy).evaluate(xx, yy, 2500.0, cx, cy)
            var = np.full_like(clean, 0.25)
            noisy = clean + rng.normal(0.0, 0.5, size=clean.shape)
            cutouts.append({"xx": xx, "yy": yy, "image": noisy, "variance": var,
                            "x_init": float(cx), "y_init": float(cy)})
        res = compare_orientation(g, cutouts)
        self.assertEqual(res["status"], "measured")
        self.assertFalse(res["psf_transpose"])
        self.assertGreater(res["normal_wins"], res["transposed_wins"])
        self.assertLess(res["normal_chi2_nu_median"], res["transposed_chi2_nu_median"])

    def test_empty_cutouts_marks_pending_02_07(self):
        g = EPSFTests().grid(fixture(detector=2), norm=1.0)
        res = compare_orientation(g, [])
        self.assertEqual(res["status"], "pending_02_07")
        self.assertIsNone(res["psf_transpose"])


if __name__ == "__main__":
    unittest.main()
