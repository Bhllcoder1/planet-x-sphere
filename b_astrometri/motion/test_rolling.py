"""04-15 offline window, mask, reprojection and synthetic-noise checks."""
from pathlib import Path
import sys
import unittest

import numpy as np
from astropy.wcs import WCS

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from b_astrometri.motion.rolling import rolling_window
from b_astrometri.motion.stacks import DEFAULT_BAD_FLAGS, validation_metrics


def grid():
    wcs = WCS(naxis=2)
    wcs.wcs.crpix = [16., 16.]
    wcs.wcs.crval = [269.45, 4.7]
    wcs.wcs.cdelt = [-6.15 / 3600, 6.15 / 3600]
    wcs.wcs.ctype = ["RA---TAN", "DEC--TAN"]
    return wcs


def frames(count=6, shape=(32, 32)):
    wcs = grid()
    return [{"frame_id": f"f{i}", "mjd": 60000. + i, "detector": 1,
             "pass_id": 0, "release": "DR1", "wavelength_um": 1.2,
             "image": np.full(shape, 10. + i), "variance": np.full(shape, 4.),
             "wcs": wcs.deepcopy()} for i in range(count)]


def view(data, *, start=60000., days=3., target=None, width=0.05):
    return rolling_window(data, start, window_days=days, target_wcs=target or grid(),
                          shape_out=(32, 32), channel_width_um=width)


class RollingTests(unittest.TestCase):
    def test_half_open_inside_minus_outside_and_labels(self):
        result = view(frames())
        self.assertEqual(result["status"], "ok")
        np.testing.assert_allclose(result["inside"]["image"], 11.)
        np.testing.assert_allclose(result["outside"]["image"], 14.)
        np.testing.assert_allclose(result["difference"]["image"], -3.)
        np.testing.assert_allclose(result["difference"]["variance"], 8 / 3)
        self.assertEqual([r["role"] for r in result["frame_roles"]], list("+++---"))
        self.assertFalse(result["frame_roles"][3]["inside_window"])
        self.assertTrue(result["view_only"])
        self.assertFalse(result["measurement_allowed"])
        self.assertFalse(result["astrometry_allowed"])
        self.assertEqual(result["mode"], "S")
        self.assertIn("astrometri yok", result["badge"])

    def test_default_days_is_one_third_of_pass_span(self):
        result = view(frames(), start=60001., days=None)
        self.assertAlmostEqual(result["window_days"], 5 / 3)
        self.assertIn("ASSUMPTION", result["window_days_source"])
        self.assertEqual([r["frame_id"] for r in result["frame_roles"] if r["role"] == "+"], ["f1", "f2"])

    def test_short_or_outside_windows_never_fake_a_difference(self):
        result = view(frames(), days=1.)
        self.assertEqual(result["side_status"]["inside"], "insufficient_frames")
        self.assertIsNone(result["inside"])
        self.assertIsNone(result["difference"])
        self.assertEqual(result["frame_roles"][0]["role"], ".")
        result = view(frames(), start=60020.)
        self.assertEqual(result["status"], "unavailable_difference")
        self.assertIsNone(result["difference"])

    def test_masks_flags_nan_and_nonpositive_variance_remain_unused(self):
        data = frames()
        data[0]["mask"] = np.ones((32, 32), dtype=bool)
        data[1]["image"][0, 0] = np.nan
        data[2]["variance"][0, 0] = 0.
        data[3]["flags"] = np.full((32, 32), DEFAULT_BAD_FLAGS, dtype=np.uint32)
        originals = [{k: v.copy() for k, v in f.items() if isinstance(v, np.ndarray)} for f in data]
        result = view(data)
        self.assertEqual([result["frame_roles"][i]["role"] for i in (0, 3)], [".", "."])
        self.assertTrue(np.isnan(result["difference"]["image"][0, 0]))
        self.assertTrue(np.isfinite(result["difference"]["image"][5, 5]))
        for frame, before in zip(data, originals):
            for name, expected in before.items():
                np.testing.assert_array_equal(frame[name], expected)
        for frame in data[:3]:
            frame["mask"] = np.ones((32, 32), dtype=bool)
        result = view(data)
        self.assertEqual(result["side_status"]["inside"], "no_valid_pixels")
        self.assertIsNone(result["difference"])

    def test_reprojection_path_for_different_native_wcs(self):
        data = frames()
        for frame in data:
            frame["wcs"].wcs.crpix += [0.25, 0.15]
        result = view(data)
        self.assertEqual(result["status"], "ok")
        self.assertTrue(result["inside"]["resampled"])
        self.assertTrue(result["outside"]["resampled"])
        self.assertIn("covariance", result["inside"]["noise_model"])
        self.assertGreater(np.count_nonzero(np.isfinite(result["difference"]["image"])), 500)

    def test_disjoint_valid_coverage_is_not_a_zero_difference(self):
        data = frames()
        for i, frame in enumerate(data):
            mask = np.zeros((32, 32), dtype=bool)
            mask[:, 16:] = i < 3
            mask[:, :16] = i >= 3
            frame["mask"] = mask
        result = view(data)
        self.assertEqual(result["side_status"], {"inside": "ok", "outside": "ok"})
        self.assertEqual(result["status"], "no_common_coverage")
        self.assertTrue(np.all(np.isnan(result["difference"]["image"])))

    def test_synthetic_static_stars_and_blank_sky_noise(self):
        data = frames()
        rng = np.random.default_rng(20261115)
        stars = np.zeros((32, 32), dtype=bool)
        stars[[8, 16, 24], [8, 16, 24]] = True
        for frame in data:
            frame["image"] = rng.normal(0., 2., (32, 32)) + stars * 100.
        result = view(data)
        metrics = validation_metrics(result["inside"], result["difference"],
                                     empty_sky_mask=~stars, static_star_mask=stars)
        self.assertTrue(metrics["noise_within_20_percent"], metrics)
        self.assertTrue(metrics["static_residual_below_3_sigma"], metrics)

    def test_invalid_windows_and_mixed_pass_detector_release_channel(self):
        for start, days, width in ((np.nan, 3., 0.05), (60000., 0., 0.05),
                                   (60000., -1., 0.05), (60000., np.inf, 0.05),
                                   (60000., 3., 0.), (60000., 3., np.nan)):
            with self.subTest(start=start, days=days, width=width), self.assertRaises(ValueError):
                view(frames(), start=start, days=days, width=width)
        for field, value in (("pass_id", 2), ("detector", 2), ("release", "QR3"),
                             ("wavelength_um", 2.), ("mjd", np.nan), ("frame_id", "f0")):
            data = frames()
            data[1][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                view(data)
        data = frames()
        for frame in data:
            frame["mjd"] = 60000.
        with self.assertRaises(ValueError):
            view(data, days=None)
        with self.assertRaises(ValueError):
            view([])


if __name__ == "__main__":
    unittest.main()
