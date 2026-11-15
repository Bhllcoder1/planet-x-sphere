import csv
import tempfile
import unittest
from pathlib import Path

from phase_bias import run_phase_sweep, write_phase_bias_csv
from test_epsf import EPSFTests, fixture


class PhaseBiasTests(unittest.TestCase):
    def test_high_snr_phase_bias_within_t2_and_t3_bounds(self):
        grid = EPSFTests().grid(fixture(detector=2), norm=1.0)
        rows = run_phase_sweep(
            grid,
            phases=[0.0, 0.25, 0.5, 0.75],
            snr_levels=(50.0, 100.0),
            n_trials=30,
            seed=11,
        )
        self.assertEqual(len(rows), 8)
        for r in rows:
            self.assertEqual(r["n_ok"], 30)
            self.assertLess(abs(r["bias_x_px"]), 0.02)
            self.assertLess(abs(r["bias_y_px"]), 0.02)
            self.assertGreaterEqual(r["rms_over_sigma_x"], 0.6)
            self.assertLessEqual(r["rms_over_sigma_x"], 1.5)

    def test_csv_roundtrip(self):
        grid = EPSFTests().grid(fixture(detector=2), norm=1.0)
        rows = run_phase_sweep(grid, phases=[0.1, 0.5], snr_levels=(50.0,), n_trials=5, seed=3)
        with tempfile.TemporaryDirectory() as tmp:
            p = write_phase_bias_csv(rows, Path(tmp) / "phase_bias.csv")
            with p.open("r", encoding="utf-8") as fh:
                loaded = list(csv.DictReader(fh))
            self.assertEqual(len(loaded), 2)
            self.assertIn("rms_over_sigma_x", loaded[0])


if __name__ == "__main__":
    unittest.main()
