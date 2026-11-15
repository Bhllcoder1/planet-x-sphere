"""04-07 deterministic synthetic tests; no real-asteroid acceptance claimed."""
from pathlib import Path
import json
import sys
import tempfile
import unittest

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from a_veri_isleme.process.masks import BASE_FIT_MASK, MASK_OUTLIER, MASK_SOURCE
from b_astrometri.movers.linker import link_movers
from b_astrometri.movers.outlier_candidates import promote_outliers, score_linked_candidates, write_candidates


class OutlierTests(unittest.TestCase):
    def promote(self, flags, detections=None, **kwargs):
        return promote_outliers(flags, [] if detections is None else detections,
                                frame_id="f", mjd=61000, catalog_positions=[], **kwargs)

    def test_8_connectivity_inclusive_40_limit_and_fit_mask(self):
        flags = np.zeros((30, 30), dtype=np.uint32)
        flags[1, 1] = flags[2, 2] = MASK_OUTLIER
        flags[5:10, 1:9] = MASK_OUTLIER  # exactly 40
        flags[15:22, 1:7] = MASK_OUTLIER  # 42
        flags[25, 25] = MASK_OUTLIER | BASE_FIT_MASK
        result = self.promote(flags)
        self.assertEqual(result["statistics"]["n_components"], 4)
        self.assertEqual([c["size_px"] for c in result["outlier_candidates"]], [2, 40])
        self.assertEqual([c["reason"] for c in result["component_log"]],
                         ["promoted", "promoted", "noncompact_gt40", "fit_masked"])

    def test_source_is_retained_and_existing_detection_not_duplicated(self):
        flags = np.zeros((8, 8), dtype=np.uint32)
        flags[3, 4] = MASK_OUTLIER | MASK_SOURCE
        original = [{"frame_id": "f", "mjd": 61000, "det_id": "d", "x": 4.1, "y": 3.1}]
        result = self.promote(flags, original)
        self.assertEqual(len(result["detections"]), 1)
        self.assertTrue(result["outlier_candidates"][0]["source_overlap"])
        self.assertEqual(result["detections"][0]["outlier_score_bonus"], 1)
        self.assertNotIn("outlier_score_bonus", original[0])
        self.assertEqual(result["mask"], "0x3C028E44")

    def test_catalog_match_is_not_promoted(self):
        flags = np.zeros((8, 8), dtype=np.uint32)
        flags[3, 4] = MASK_OUTLIER
        result = promote_outliers(flags, [], frame_id="f", mjd=61000,
                                  catalog_positions=[(4, 3)])
        self.assertEqual(result["outlier_candidates"], [])
        self.assertEqual(result["component_log"][0]["reason"], "catalog_match")

    def test_measures_static_reference_promotion_without_claiming_real_rate(self):
        flags = np.zeros((12, 12), dtype=np.uint32)
        flags[2, 2] = MASK_OUTLIER
        result = self.promote(flags, static_positions=[(2, 2), (10, 10)])
        self.assertEqual(result["statistics"]["static_promotion_fraction"], 0.5)
        self.assertEqual(self.promote(flags)["statistics"]["static_promotion_status"], "not_measured")
        self.assertIsNone(self.promote(flags, static_positions=[])["statistics"]["static_promotion_fraction"])

    def test_linking_without_outliers_and_additive_evidence(self):
        detections, promoted = [], []
        for index in range(3):
            frame_id, mjd = f"f{index}", 61000 + index / 24
            detection = {"frame_id": frame_id, "mjd": mjd, "det_id": "mover",
                         "x": 5 + 3 * index, "y": 5.0}
            detections.append(detection)
            flags = np.zeros((20, 20), dtype=np.uint32)
            result = promote_outliers(flags, [detection], frame_id=frame_id,
                                      mjd=mjd, catalog_positions=[])
            self.assertEqual(result["statistics"]["n_promoted_components"], 0)
            promoted.extend(result["detections"])
        # Synthetic frames deliberately share one native/tangent pixel grid.
        linked = link_movers(promoted)
        self.assertTrue(linked["tracks"])
        no_bonus = score_linked_candidates(linked, promoted)
        self.assertEqual(no_bonus["tracks"][0]["score"], linked["tracks"][0]["score"])
        promoted[0]["outlier_score_bonus"] = 1.0
        scored = score_linked_candidates(linked, promoted)
        self.assertEqual(len(scored["tracks"]), len(linked["tracks"]))
        self.assertAlmostEqual(scored["tracks"][0]["score"], linked["tracks"][0]["score"] + 1)
        self.assertAlmostEqual(scored["candidates_log"][0]["outlier_score_bonus"], 1)
        self.assertNotIn("base_score", linked["tracks"][0])

    def test_invalid_flags_coordinates_and_serialization(self):
        for flags in (np.zeros((2, 2), dtype=float), np.array([[-1]]), np.array([[2 ** 32]])):
            with self.assertRaises(ValueError):
                self.promote(flags)
        with self.assertRaises(ValueError):
            self.promote(np.zeros((4, 4), dtype=np.uint32), score_bonus=float("nan"))
        result = self.promote(np.zeros((4, 4), dtype=np.uint32))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "outlier_candidates.json"
            write_candidates(path, result)
            self.assertEqual(json.loads(path.read_text())["outlier_candidates"], [])


if __name__ == "__main__":
    unittest.main()
