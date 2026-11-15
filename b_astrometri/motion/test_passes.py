import json
import tempfile
import unittest
from pathlib import Path

from passes import group_passes, write_pass_outputs


class PassGroupingTests(unittest.TestCase):
    def test_exact_30_day_boundary(self):
        # 30.0 gun tam sinirda ayni geciste kalir; >30.0 gun yeni gecis baslatir.
        frames = [
            {"frame_id": "a", "mjd": 60000.0, "det": 1},
            {"frame_id": "b", "mjd": 60030.0, "det": 1},
            {"frame_id": "c", "mjd": 60060.0001, "det": 2},
        ]
        res = group_passes(frames, gap_days=30.0)
        self.assertEqual(res["n_passes"], 2)
        self.assertEqual(res["pass_of_frame"], {"a": 1, "b": 1, "c": 2})
        self.assertEqual(len(res["gaps"]), 1)
        self.assertEqual((res["gaps"][0]["from_frame"], res["gaps"][0]["to_frame"],
                          res["gaps"][0]["new_pass_id"]), ("b", "c", 2))
        self.assertAlmostEqual(res["gaps"][0]["gap_days"], 30.0001, places=8)
        self.assertTrue(res["passes"][0]["stack_ok_by_detector"]["1"])
        self.assertFalse(res["passes"][1]["stack_ok_by_detector"]["2"])

    def test_empty_list_distinguishes_unknown_and_no_coverage(self):
        unk = group_passes([], empty_status="unknown")
        nocov = group_passes([], empty_status="no_coverage")
        self.assertEqual(unk["status"], "unknown")
        self.assertEqual(nocov["status"], "no_coverage")
        self.assertEqual(unk["passes"], [])
        self.assertEqual(unk["gaps"], [])

    def test_write_outputs_roundtrip(self):
        frames = [
            {"frame_id": "f1", "MJD-AVG": 60100.0, "detector": "D1", "SPS_EPA": 0},
            {"frame_id": "f2", "MJD-AVG": 60102.5, "detector": "D1", "SPS_EPA": 0},
        ]
        res = group_passes(frames)
        with tempfile.TemporaryDirectory() as tmp:
            p_path, f_path = write_pass_outputs(res, tmp)
            p_data = json.loads(p_path.read_text(encoding="utf-8"))
            f_data = json.loads(f_path.read_text(encoding="utf-8"))
            self.assertEqual(p_data["n_passes"], 1)
            self.assertEqual(p_data["passes"][0]["sps_epa"], [0.0])
            self.assertEqual(p_data["gaps"], [])
            self.assertEqual(f_data, {"f1": 1, "f2": 1})

    def test_stage0_barnard_and_eps_ind_if_available(self):
        stage0_a = Path("C:/Users/behlu/spherex-kb/stage0/data/A")
        barnard = stage0_a / "frames_Barnard.json"
        eps_b = stage0_a / "frames_EpsInd_B.json"
        if not (barnard.exists() and eps_b.exists()):
            self.skipTest("stage0/data/A yerel dosyalari yok")
        b_frames = json.loads(barnard.read_text(encoding="utf-8"))["science"]
        b_res = group_passes(b_frames)
        self.assertEqual(b_res["n_frames"], 358)
        self.assertEqual(b_res["n_passes"], 3)
        self.assertEqual(len(b_res["pass_of_frame"]), 358)
        self.assertEqual(len(b_res["gaps"]), 2)
        self.assertEqual([round(p["duration_days"]) for p in b_res["passes"]], [46, 55, 37])
        self.assertTrue(all(g["gap_days"] > 30 for g in b_res["gaps"]))

        e_frames = json.loads(eps_b.read_text(encoding="utf-8"))["science"]
        e_res = group_passes(e_frames)
        self.assertEqual(e_res["n_passes"], 4)
        self.assertEqual(len(e_res["gaps"]), 3)
        self.assertEqual([round(p["duration_days"]) for p in e_res["passes"]], [46, 45, 15, 10])
        self.assertTrue(all(g["gap_days"] > 30 for g in e_res["gaps"]))


if __name__ == "__main__":
    unittest.main()
