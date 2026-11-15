"""07-04 (T1 sayisal): Tam 1.000 px kayma testi (ekran/Playwright kismi d_site bekliyor [NV])."""
import sys
import unittest
from pathlib import Path

import numpy as np

CENTROID_DIR = str(Path(__file__).resolve().parents[1] / "b_astrometri" / "centroid")
if CENTROID_DIR not in sys.path:
    sys.path.insert(0, CENTROID_DIR)

from test_epsf import EPSFTests, fixture  # noqa: E402
from wing_fit import fit_epsf_wing  # noqa: E402


class T1IntegerShiftTests(unittest.TestCase):
    def test_t1_numerical_one_pixel_shift_within_0_005_px(self):
        grid = EPSFTests().grid(fixture(detector=2), norm=1.0)
        cx, cy = grid.positions[220]
        yy, xx = np.mgrid[-4:5, -4:5] + np.array([[[cy]], [[cx]]])
        img0 = grid.model_at(cx, cy).evaluate(xx, yy, 5000.0, cx, cy) + 10.0
        img1 = grid.model_at(cx + 1.0, cy).evaluate(xx, yy, 5000.0, cx + 1.0, cy) + 10.0
        var = np.ones_like(img0)

        f0 = fit_epsf_wing(grid, xx, yy, img0, var, float(cx), float(cy))
        f1 = fit_epsf_wing(grid, xx, yy, img1, var, float(cx + 1.0), float(cy))
        self.assertEqual(f0["status"], "ok")
        self.assertEqual(f1["status"], "ok")
        delta_x = f1["x"] - f0["x"]
        delta_y = f1["y"] - f0["y"]
        self.assertLessEqual(abs(delta_x - 1.0), 0.005)
        self.assertLessEqual(abs(delta_y), 0.005)

    def test_t1_np_roll_one_pixel_shift(self):
        grid = EPSFTests().grid(fixture(detector=2), norm=1.0)
        cx, cy = grid.positions[220]
        yy, xx = np.mgrid[-5:6, -5:6] + np.array([[[cy]], [[cx]]])
        img0 = grid.model_at(cx, cy).evaluate(xx, yy, 5000.0, cx, cy) + 10.0
        img1 = np.roll(img0, shift=1, axis=1)
        var = np.ones_like(img0)

        f0 = fit_epsf_wing(grid, xx, yy, img0, var, float(cx), float(cy))
        f1 = fit_epsf_wing(grid, xx, yy, img1, var, float(cx + 1.0), float(cy))
        self.assertEqual(f0["status"], "ok")
        self.assertEqual(f1["status"], "ok")
        self.assertLessEqual(abs((f1["x"] - f0["x"]) - 1.0), 0.005)


if __name__ == "__main__":
    unittest.main()
