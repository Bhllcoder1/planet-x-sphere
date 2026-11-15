"""07-04 T1 sayısal kontrolleri.

Sentetik birim testlerini çalıştırmak için doğrudan çalıştırın. Gerçek Stage 0
penceresi üzerinde enjeksiyon/kayma deneyi için --real-window, --epsf-fits ve
--frame-header argümanlarını verin.
"""
import argparse
import json
import sys
import unittest
from pathlib import Path

import numpy as np
from astropy.io import fits

CENTROID_DIR = str(Path(__file__).resolve().parents[1] / "b_astrometri" / "centroid")
if CENTROID_DIR not in sys.path:
    sys.path.insert(0, CENTROID_DIR)

from test_epsf import EPSFTests, fixture  # noqa: E402
from epsf import EPSFGrid  # noqa: E402
from wing_fit import DEFAULT_BAD_FLAGS, fit_epsf_wing  # noqa: E402


def _validate_real_window(window_path: Path, epsf_path: Path, header_path: Path) -> dict:
    with np.load(window_path, allow_pickle=False) as source:
        required = {"wx0", "wy0", "IMAGE", "FLAGS", "VARIANCE"}
        if not required.issubset(source.files):
            raise ValueError(f"Missing window arrays: {sorted(required - set(source.files))}")
        x0, y0 = int(source["wx0"]), int(source["wy0"])
        image = np.asarray(source["IMAGE"], dtype=float)
        flags = np.asarray(source["FLAGS"], dtype=np.int64)
        variance = np.asarray(source["VARIANCE"], dtype=float)
    frame_header = fits.Header.fromtextfile(str(header_path))
    with fits.open(epsf_path, memmap=False) as hdus:
        epsf_obsid = hdus["IMAGE"].header.get("OBSID")
    if not epsf_obsid or frame_header.get("OBSID") != epsf_obsid:
        raise ValueError("Stage 0 window and ePSF FITS OBSID must match")
    grid = EPSFGrid.read(epsf_path, release="DR1")
    if grid.detector != 2:
        raise ValueError("This Stage 0 window is detector 2")

    best = None
    for cy in range(7, image.shape[0] - 7):
        for cx in range(7, image.shape[1] - 7):
            patch = image[cy - 7:cy + 8, cx - 7:cx + 8]
            patch_flags = flags[cy - 7:cy + 8, cx - 7:cx + 8]
            patch_var = variance[cy - 7:cy + 8, cx - 7:cx + 8]
            bad = (~np.isfinite(patch) | ~np.isfinite(patch_var) | (patch_var <= 0)
                   | ((patch_flags & DEFAULT_BAD_FLAGS) != 0))
            if np.mean(bad) > 0.05:
                continue
            median = float(np.median(patch[~bad]))
            mad = float(np.median(np.abs(patch[~bad] - median)))
            if best is None or mad < best[0]:
                best = (mad, cx, cy)
    if best is None:
        raise ValueError("No mostly unmasked 15x15 injection stamp in the real window")

    _, cx, cy = best
    x_parent, y_parent = x0 + cx, y0 + cy
    ys, xs = np.mgrid[cy - 7:cy + 8, cx - 7:cx + 8]
    xx, yy = xs + x0, ys + y0
    stamp = image[ys, xs].copy()
    stamp_var = variance[ys, xs].copy()
    stamp_flags = flags[ys, xs].copy()
    flux = 5000.0
    star0 = grid.model_at(x_parent, y_parent).evaluate(xx, yy, flux, x_parent, y_parent)
    star1 = grid.model_at(x_parent + 1.0, y_parent).evaluate(
        xx, yy, flux, x_parent + 1.0, y_parent)
    image0, image1 = stamp + star0, stamp + star1
    fit0 = fit_epsf_wing(grid, xx, yy, image0, stamp_var, x_parent, y_parent,
                         flags=stamp_flags)
    fit1 = fit_epsf_wing(grid, xx, yy, image1, stamp_var, x_parent + 1.0, y_parent,
                         flags=stamp_flags)
    rolled = np.roll(image0, 1, axis=1)
    fit_roll = fit_epsf_wing(grid, xx, yy, rolled, np.roll(stamp_var, 1, axis=1),
                             x_parent + 1.0, y_parent,
                             flags=np.roll(stamp_flags, 1, axis=1))
    if any(result.get("status") != "ok" for result in (fit0, fit1, fit_roll)):
        raise AssertionError("One of the real-window T1 fits was not measurable")
    direct_dx = fit1["x"] - fit0["x"]
    direct_dy = fit1["y"] - fit0["y"]
    rolled_dx = fit_roll["x"] - fit0["x"]
    if abs(direct_dx - 1.0) > 0.005 or abs(direct_dy) > 0.005 or abs(rolled_dx - 1.0) > 0.005:
        raise AssertionError(
            f"Real-window T1 failed: direct dx={direct_dx:.6g}, dy={direct_dy:.6g}, "
            f"np.roll dx={rolled_dx:.6g}; tolerance=0.005 px")
    return {
        "obsid": epsf_obsid,
        "detector": grid.detector,
        "window_shape": list(image.shape),
        "injection_parent_xy": [x_parent, y_parent],
        "injected_amplitude": flux,
        "direct_delta_x_px": direct_dx,
        "direct_delta_y_px": direct_dy,
        "np_roll_delta_x_px": rolled_dx,
        "tolerance_px": 0.005,
    }


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
    if len(sys.argv) > 1 and sys.argv[1] == "--real-window":
        parser = argparse.ArgumentParser()
        parser.add_argument("--real-window", required=True, type=Path)
        parser.add_argument("--epsf-fits", required=True, type=Path)
        parser.add_argument("--frame-header", required=True, type=Path)
        args = parser.parse_args()
        print(json.dumps(_validate_real_window(args.real_window, args.epsf_fits,
                                               args.frame_header), indent=2))
    else:
        unittest.main()
