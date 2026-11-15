import unittest
import json
import tempfile
from pathlib import Path
from xml.etree import ElementTree

from lightcurves import build_lambda_lightcurves, write_lightcurve_outputs


class LightcurveTests(unittest.TestCase):
    def test_constant_control_star_stays_within_3sigma_and_separates_lambda(self):
        # Iki farkli lambda kutusu (1.02 um ve 2.02 um); farkli akilar ama sabit yildiz.
        meas = [
            {"frame_id": "f1", "pass_id": 1, "mjd": 60100.0, "cwave_um": 1.02, "status": "ok", "flux": 100.0, "sigma_flux": 2.0},
            {"frame_id": "f2", "pass_id": 2, "mjd": 60280.0, "cwave_um": 1.03, "status": "ok", "flux": 101.5, "sigma_flux": 2.0},
            {"frame_id": "f3", "pass_id": 1, "mjd": 60101.0, "cwave_um": 2.02, "status": "ok", "flux": 300.0, "sigma_flux": 3.0},
            {"frame_id": "f4", "pass_id": 2, "mjd": 60281.0, "cwave_um": 2.03, "status": "ok", "flux": 298.0, "sigma_flux": 3.0},
        ]
        res = build_lambda_lightcurves("ControlStar", meas, bin_width_um=0.05)
        self.assertEqual(res["status"], "ok")
        self.assertEqual(res["n_bins"], 2)
        for b in res["bins"]:
            self.assertFalse(b["variable_gt_3sigma"])
            self.assertLessEqual(b["max_delta_sigma"], 3.0)
            self.assertIn("_um", b["lambda_label"])

    def test_variable_star_r_dra_reports_sigma_and_saturation(self):
        meas = [
            {"frame_id": "f1", "pass_id": 1, "mjd": 60100.0, "cwave_um": 1.51, "status": "ok", "flux": 500.0, "sigma_flux": 10.0, "saturated_fit": False},
            {"frame_id": "f2", "pass_id": 2, "mjd": 60280.0, "cwave_um": 1.52, "status": "ok", "flux": 650.0, "sigma_flux": 15.0, "saturated_fit": True},
        ]
        res = build_lambda_lightcurves("R_Dra", meas, bin_width_um=0.05, all_pass_ids=[1, 2, 3])
        b = res["bins"][0]
        self.assertTrue(b["variable_gt_3sigma"])
        self.assertGreater(b["max_delta_sigma"], 8.0)
        self.assertTrue(b["any_saturated"])
        self.assertEqual(b["passes"][2]["status"], "no_data")

    def test_empty_coverage_reports_unknown_or_no_coverage(self):
        unknown = build_lambda_lightcurves(
            "RW_Aur", [], empty_status="unknown", empty_reason="TAP query did not complete")
        self.assertEqual(unknown["status"], "unknown")
        self.assertEqual(unknown["photometry_status"], "not_run")
        self.assertEqual(unknown["reason"], "TAP query did not complete")
        self.assertEqual(build_lambda_lightcurves("RW_Aur", [], empty_status="no_coverage")["status"], "no_coverage")

    def test_unknown_outputs_are_explicit_and_not_zero_flux(self):
        result = build_lambda_lightcurves(
            "RW_Aur", [], empty_status="unknown", empty_reason="Archive query incomplete")
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = write_lightcurve_outputs(result, temp_dir)
            data = json.loads(Path(paths["json"]).read_text(encoding="utf-8"))
            svg = Path(paths["svg"]).read_text(encoding="utf-8")
        ElementTree.fromstring(svg)
        self.assertEqual(data["coverage_status"], "unknown")
        self.assertIn("Coverage: UNKNOWN", svg)
        self.assertIn("not a zero-flux measurement", svg)

    def test_svg_labels_each_lambda_bin_and_sigma_errors(self):
        result = build_lambda_lightcurves("R_Dra", [
            {"pass_id": 1, "mjd": 60100, "cwave_um": 1.51, "status": "ok", "flux": 5, "sigma_flux": 1},
            {"pass_id": 2, "mjd": 60200, "cwave_um": 1.52, "status": "ok", "flux": 8, "sigma_flux": 1},
        ])
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = write_lightcurve_outputs(result, temp_dir)
            svg = Path(paths["svg"]).read_text(encoding="utf-8")
        ElementTree.fromstring(svg)
        self.assertIn("1.500-1.550_um", svg)
        self.assertEqual(svg.count("<circle "), 2)
        self.assertEqual(result["bins"][0]["max_delta_sigma"], 3 / (2 ** 0.5))


if __name__ == "__main__":
    unittest.main()
