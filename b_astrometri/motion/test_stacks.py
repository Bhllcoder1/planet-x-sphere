"""04-02 synthetic checks; no downloaded files or scientific detection claims."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

import numpy as np
from astropy.wcs import WCS

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from stacks import (DEFAULT_BAD_FLAGS, compare_stack_modes, difference_stacks, inverse_variance_stack,
                    stack_pass, validation_metrics, write_stack_products)


def wcs_grid(angle=0):
    wcs = WCS(naxis=2)
    wcs.wcs.ctype = ["RA---TAN", "DEC--TAN"]
    wcs.wcs.crval = [269.452, 4.693]
    wcs.wcs.crpix = [16.5, 16.5]
    angle = np.deg2rad(angle)
    wcs.wcs.cd = 6.15 / 3600 * np.array([[-np.cos(angle), np.sin(angle)],
                                       [np.sin(angle), np.cos(angle)]])
    return wcs


def frame(index, image, *, variance=None, wavelength=1.2, pass_id=1, wcs=None):
    return {"frame_id": str(index), "detector": 1, "pass_id": pass_id,
            "release": "DR1", "wavelength_um": wavelength, "image": np.array(image),
            "variance": np.ones_like(image) if variance is None else np.array(variance),
            "wcs": wcs_grid() if wcs is None else wcs}


class StackTests(unittest.TestCase):
    def test_inverse_variance_weights_and_no_input_mutation(self):
        images = np.array([[[2., 6.]], [[10., 2.]]])
        variances = np.array([[[1., 4.]], [[3., 4.]]])
        before = images.copy()
        result = inverse_variance_stack(images, variances)
        np.testing.assert_allclose(result["image"], [[4., 4.]])
        np.testing.assert_allclose(result["variance"], [[0.75, 2.]])
        np.testing.assert_array_equal(images, before)
        self.assertEqual(result["mode"], "S")
        self.assertFalse(result["astrometry_allowed"])
        self.assertFalse(result["measurement_allowed"])

    def test_at_least_two_frames_and_two_valid_pixels(self):
        with self.assertRaises(ValueError):
            inverse_variance_stack([[[1.]]], [[[1.]]])
        result = inverse_variance_stack([[[1., np.nan]], [[2., 3.]]],
                                        [[[0., 1.]], [[1., 1.]]])
        self.assertTrue(np.isnan(result["image"]).all())
        np.testing.assert_array_equal(result["coverage"], [[1, 1]])
        with self.assertRaises(ValueError):
            inverse_variance_stack(np.ones((2, 2, 2)), np.ones((2, 2, 2)),
                                   masks=np.zeros((2, 2, 2), dtype=int))

    def test_a_flags_and_user_mask_preserved(self):
        first, second = frame(1, np.ones((3, 3))), frame(2, np.ones((3, 3)) * 3)
        first["flags"] = np.zeros((3, 3), dtype=np.uint32)
        first["flags"][0, 0] = DEFAULT_BAD_FLAGS
        second["mask"] = np.zeros((3, 3), dtype=bool)
        second["mask"][1, 1] = True
        result = stack_pass([first, second], target_wcs=wcs_grid(), shape_out=(3, 3))
        self.assertTrue(np.isnan(result["image"][0, 0]))
        self.assertTrue(np.isnan(result["image"][1, 1]))
        self.assertEqual(result["image"][2, 2], 2)
        self.assertEqual(result["frame_valid_pixels"], {"1": 8, "2": 8})
        self.assertEqual(first["image"][0, 0], 1)

    def test_reject_mixed_identity_detector_pass_release_and_wcs(self):
        baseline = frame(1, np.ones((3, 3)))
        for key, value in (("frame_id", "1"), ("detector", 2), ("pass_id", 2),
                           ("release", "QR3"), ("wavelength_um", np.nan)):
            other = frame(2, np.ones((3, 3)))
            other[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                stack_pass([baseline, other], target_wcs=wcs_grid(), shape_out=(3, 3))
        bad = wcs_grid()
        bad.wcs.ctype = ["RA---CAR", "DEC--CAR"]
        with self.assertRaises(ValueError):
            stack_pass([baseline, frame(2, np.ones((3, 3)))], target_wcs=bad, shape_out=(3, 3))
        for release in ("QR1", "QR2", "unknown"):
            frames = [frame(i, np.ones((3, 3))) for i in range(2)]
            for item in frames:
                item["release"] = release
            with self.assertRaises(ValueError):
                stack_pass(frames, target_wcs=wcs_grid(), shape_out=(3, 3))

    def test_exact_reprojection_rotation_constant_brightness(self):
        frames = [frame(i, np.full((32, 32), 17.0), wcs=wcs_grid(angle))
                  for i, angle in enumerate((1.2, -2.8))]
        result = stack_pass(frames, target_wcs=wcs_grid(), shape_out=(32, 32))
        np.testing.assert_allclose(result["image"][8:24, 8:24], 17., atol=1e-6)
        self.assertTrue(result["resampled"])
        self.assertIn("unpropagated", result["noise_model"])
        self.assertIn("pending", result["noise_validation"])
        self.assertFalse(result["astrometry_allowed"])

    def test_differences_channel_grid_and_independence_guards(self):
        left = stack_pass([frame(i, np.ones((4, 4)) * 8, wavelength=1.2) for i in (1, 2)],
                          target_wcs=wcs_grid(), shape_out=(4, 4))
        right = stack_pass([frame(i, np.ones((4, 4)) * 3, wavelength=1.21, pass_id=2) for i in (3, 4)],
                           target_wcs=wcs_grid(), shape_out=(4, 4))
        diff = difference_stacks(left, right, channel_width_um=0.02)
        np.testing.assert_allclose(diff["image"], 5)
        np.testing.assert_allclose(diff["noise"], 1)
        self.assertFalse(diff["psf_matched"])
        with self.assertRaises(ValueError):
            difference_stacks(left, right, channel_width_um=0.005)
        with self.assertRaises(ValueError):
            difference_stacks(left, left, channel_width_um=0.02)
        for field, value in (("detector", 2), ("release", "QR3"), ("target_wcs", wcs_grid(2))):
            altered = dict(right, **{field: value})
            with self.subTest(field=field), self.assertRaises(ValueError):
                difference_stacks(left, altered, channel_width_um=0.02)

    def test_independent_synthetic_noise_and_static_star_residual(self):
        rng = np.random.default_rng(402)
        yy, xx = np.mgrid[:128, :128]
        star = 50 * np.exp(-((xx - 64.2) ** 2 + (yy - 63.7) ** 2) / 4)
        stacks = []
        for pass_id in (1, 2):
            frames = [frame(f"{pass_id}-{i}", star + rng.normal(0, 2, star.shape),
                            variance=np.full(star.shape, 4.), pass_id=pass_id) for i in range(8)]
            stacks.append(stack_pass(frames, target_wcs=wcs_grid(), shape_out=star.shape))
        diff = difference_stacks(*stacks, channel_width_um=.02)
        metrics = validation_metrics(stacks[0], diff, empty_sky_mask=star < .001,
                                     static_star_mask=star > 1)
        self.assertTrue(metrics["noise_within_20_percent"], metrics)
        self.assertTrue(metrics["static_residual_below_3_sigma"], metrics)
        self.assertAlmostEqual(float(stacks[0]["noise"][0, 0]), np.sqrt(4 / 8))

    def test_output_files_keep_view_only_provenance(self):
        product = stack_pass([frame(i, np.ones((4, 4))) for i in (1, 2)],
                             target_wcs=wcs_grid(), shape_out=(4, 4))
        with tempfile.TemporaryDirectory() as directory:
            files = write_stack_products(product, directory, stem="stack_1_1")
            self.assertEqual(np.fromfile(files["image"], dtype="<f4").size, 16)
            metadata = json.loads(Path(files["metadata"]).read_text(encoding="utf-8"))
            self.assertEqual(metadata["mode"], "S")
            self.assertFalse(metadata["astrometry_allowed"])
            self.assertEqual(metadata["wavelengths_um"], [1.2, 1.2])
            self.assertEqual(metadata["shape"], [4, 4])
            with self.assertRaises(ValueError):
                write_stack_products(product, directory, stem="../unsafe")

    def test_d10_requires_better_residual_and_no_snr_loss(self):
        yy, xx = np.mgrid[:8, :8]
        source = np.zeros((8, 8))
        source[3:5, 3:5] = 10
        stack = stack_pass([frame(i, source) for i in (1, 2)],
                           target_wcs=wcs_grid(), shape_out=source.shape)
        other = stack_pass([frame(i, source, pass_id=2) for i in (3, 4)],
                           target_wcs=wcs_grid(), shape_out=source.shape)
        good = difference_stacks(stack, other, channel_width_um=.02)
        bad = dict(good, image=good["image"] + 4)
        result = compare_stack_modes({"detector": (stack, bad), "channel": (stack, good)},
            empty_sky_mask=source == 0, static_star_mask=source > 0, source_mask=source > 0)
        self.assertEqual(result["winner"], "channel")
        self.assertFalse(result["physical_snr_validated"])
        self.assertEqual(result["rows"]["detector"]["static_residual_median_sigma"], 4)


if __name__ == "__main__":
    unittest.main()
