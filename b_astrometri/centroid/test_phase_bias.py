import csv
import importlib
import tempfile
import unittest
from pathlib import Path

from phase_bias import run_phase_sweep, write_phase_bias_csv

epsf_tests = importlib.import_module("test_epsf")


class PhaseBiasTests(unittest.TestCase):
    def test_high_snr_phase_bias_within_t2_and_t3_bounds(self):
        grid = getattr(epsf_tests, "EPSFTests")().grid(epsf_tests.fixture(detector=2), norm=1.0)
        rows = run_phase_sweep(
            grid,
            phases=[0.0, 0.25, 0.5, 0.75],
            snr_levels=(100.0,),
            n_trials=200,
            seed=2026,
        )
        self.assertEqual(len(rows), 4)
        for r in rows:
            self.assertEqual(r["n_ok"], 200)
            self.assertLess(abs(r["bias_x_px"]), 0.02)
            self.assertLess(abs(r["bias_y_px"]), 0.02)
            self.assertGreaterEqual(r["rms_over_sigma_x"], 0.8)
            self.assertLessEqual(r["rms_over_sigma_x"], 1.25)
            self.assertGreaterEqual(r["rms_over_sigma_y"], 0.8)
            self.assertLessEqual(r["rms_over_sigma_y"], 1.25)
            self.assertTrue(r["passed_t2_t3"])

    def test_csv_roundtrip(self):
        grid = getattr(epsf_tests, "EPSFTests")().grid(epsf_tests.fixture(detector=2), norm=1.0)
        rows = run_phase_sweep(grid, phases=[0.1, 0.5], snr_levels=(50.0,), n_trials=5, seed=3)
        self.assertIsNone(rows[0]["passed_t2_t3"])
        with tempfile.TemporaryDirectory() as tmp:
            p = write_phase_bias_csv(rows, Path(tmp) / "phase_bias.csv")
            with p.open("r", encoding="utf-8") as fh:
                loaded = list(csv.DictReader(fh))
            self.assertEqual(len(loaded), 2)
            self.assertIn("rms_over_sigma_x", loaded[0])

    def test_snr_20_is_not_part_of_acceptance(self):
        grid = getattr(epsf_tests, "EPSFTests")().grid(epsf_tests.fixture(detector=2), norm=1.0)
        rows = run_phase_sweep(grid, phases=[0.25], snr_levels=(20.0, 50.0, 100.0), n_trials=10, seed=9)
        self.assertIsNone(rows[0]["passed_t2_t3"])


if __name__ == "__main__":
    unittest.main()
