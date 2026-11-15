import unittest

import numpy as np

from veto_guard import (
    BIT_CROSSTALK,
    BIT_HALO,
    BIT_STREAK,
    BIT_TRANSIENT,
    MASK_GHOST,
    crowded_field_guard,
    evaluate_candidate_flags,
    tag_candidates,
)


class VetoGuardTests(unittest.TestCase):
    def test_veto_and_caution_within_3px_never_drops_candidates(self):
        flg = np.zeros((20, 20), dtype=np.int64)
        flg[10, 12] = BIT_STREAK | BIT_CROSSTALK
        flg[11, 10] = BIT_TRANSIENT
        res = evaluate_candidate_flags(flg, 10.0, 10.0, radius_px=3.0)
        self.assertEqual(res["veto_reason"], ["CROSSTALK", "STREAK"])
        self.assertEqual(res["caution"], ["TRANSIENT"])

        # 3 px disindaki GHOST tetiklememeli; aday da silinmemeli
        flg2 = np.zeros((20, 20), dtype=np.int64)
        flg2[0, 0] = MASK_GHOST | BIT_HALO
        cands = [
            {"id": "c1", "observations": [{"frame_id": "f1", "x": 10.0, "y": 10.0}]},
            {"id": "c2", "observations": [{"frame_id": "f2", "x": 10.0, "y": 10.0}]},
        ]
        tagged = tag_candidates(cands, {"f1": flg, "f2": flg2})
        self.assertEqual(len(tagged), 2)
        self.assertTrue(tagged[0]["vetoed"])
        self.assertFalse(tagged[1]["vetoed"])
        self.assertEqual(tagged[1]["veto_reason"], [])

    def test_crowded_guard_matches_s0_d_gc_vs_sp_numbers(self):
        # gc1..gc5: SOURCE=100%, gurultu ~0.36 vs seyrek 0.025 (~14.4x)
        for _ in range(5):
            g = crowded_field_guard(1.0, 0.36, 0.025)
            self.assertTrue(g["guard_triggered"])
            self.assertFalse(g["linking_enabled"])
            self.assertEqual(g["banner"], "kalabalik_alan")
            self.assertEqual(g["reasons"], ["SOURCE_GT_50PCT", "NOISE_GT_5X_SPARSE"])

        # sp1..sp4, sp6: SOURCE %26-39, gurultu ~0.025
        for src in (0.26, 0.30, 0.34, 0.37, 0.39):
            g = crowded_field_guard(src, 0.025, 0.025)
            self.assertFalse(g["guard_triggered"])
            self.assertTrue(g["linking_enabled"])
            self.assertIsNone(g["banner"])


if __name__ == "__main__":
    unittest.main()
