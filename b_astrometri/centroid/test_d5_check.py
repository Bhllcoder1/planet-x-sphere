import importlib
import unittest
from unittest.mock import patch

import numpy as np

from d5_check import compare_orientation, self_recovery_ladder
epsf_tests = importlib.import_module("test_epsf")


class D5CheckTests(unittest.TestCase):
    def test_norm_1_and_25_recovery_and_flux_scale(self):
        hdu = epsf_tests.fixture(detector=2)
        g1 = getattr(epsf_tests, "EPSFTests")().grid(hdu, norm=1.0)
        g25 = getattr(epsf_tests, "EPSFTests")().grid(hdu, norm=25.0)
        with patch.object(g1, "model_at", wraps=g1.model_at) as model_at:
            r1 = self_recovery_ladder(g1)
        center = g1.positions[len(g1.positions) // 2]
        sampled_phases = {(round(call.args[0] - center[0], 1),
                           round(call.args[1] - center[1], 1))
                          for call in model_at.call_args_list}
        expected_phases = {(x / 10, y / 10) for x in range(10) for y in range(10)}
        self.assertEqual(sampled_phases, expected_phases)
        r25 = self_recovery_ladder(g25)
        self.assertEqual(r1["n_shifts"], 100)
        self.assertEqual(r25["n_shifts"], 100)
        self.assertAlmostEqual(r1["mean_flux_ratio"], 1.0, delta=1e-4)
        self.assertAlmostEqual(r25["mean_flux_ratio"], 1.0, delta=1e-4)
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
        g = getattr(epsf_tests, "EPSFTests")().grid(epsf_tests.fixture(detector=2), norm=1.0)
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
        g = getattr(epsf_tests, "EPSFTests")().grid(epsf_tests.fixture(detector=2), norm=1.0)
        res = compare_orientation(g, [])
        self.assertEqual(res["status"], "pending_02_07")
        self.assertIsNone(res["psf_transpose"])


if __name__ == "__main__":
    unittest.main()
