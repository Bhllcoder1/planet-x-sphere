"""07-05: T2 sub-pixel ladder and T3 injection/recovery test framework.

[SYNTHETIC] All tests use synthetic Gaussian PSF data only.
Real FITS images and ePSF grids required for production verification (H-04/H-05).
"""
import math
import unittest

import numpy as np


def _gaussian_stamp(x0: float, y0: float, sigma: float = 1.5, size: int = 15) -> np.ndarray:
    """Return a 2D Gaussian stamp centred at (x0, y0) within a size×size array."""
    yy, xx = np.mgrid[:size, :size]
    return np.exp(-((xx - x0) ** 2 + (yy - y0) ** 2) / (2 * sigma ** 2))


def _centroid_com(stamp: np.ndarray) -> tuple[float, float]:
    """Intensity-weighted centroid (centre-of-mass)."""
    yy, xx = np.mgrid[:stamp.shape[0], :stamp.shape[1]]
    total = float(stamp.sum())
    if total <= 0:
        raise ValueError("stamp sum <= 0")
    cx = float((stamp * xx).sum() / total)
    cy = float((stamp * yy).sum() / total)
    return cx, cy


class TestT2SubPixelLadder(unittest.TestCase):
    """T2: centroid bias vs sub-pixel injection phase across 10 fractional positions.

    [SYNTHETIC] Injects a Gaussian (sigma=1.5 px) at phases 0.0 .. 0.9 from pixel centre
    and measures CoM centroid recovery. Bias must be < 0.05 px for each phase.
    """

    SIGMA = 1.5
    SIZE = 15
    CENTRE = 7  # integer pixel centre of stamp
    MAX_BIAS_PX = 0.05

    def _bias_at_phase(self, phase: float) -> float:
        x0 = self.CENTRE + phase
        y0 = float(self.CENTRE)
        stamp = _gaussian_stamp(x0, y0, sigma=self.SIGMA, size=self.SIZE)
        cx, _ = _centroid_com(stamp)
        return abs(cx - x0)

    def test_bias_all_phases(self):
        """Centroid bias < 0.05 px across 10 sub-pixel phases [SYNTHETIC]."""
        for i in range(10):
            phase = i / 10.0
            bias = self._bias_at_phase(phase)
            self.assertLess(
                bias, self.MAX_BIAS_PX,
                f"Centroid bias {bias:.4f} px exceeds {self.MAX_BIAS_PX} px at phase {phase:.1f}",
            )

    def test_zero_phase_exact(self):
        """At phase 0.0 centroid should recover to < 1e-10 px [SYNTHETIC]."""
        bias = self._bias_at_phase(0.0)
        self.assertLess(bias, 1e-10)

    def test_half_phase(self):
        """At phase 0.5 bias must still satisfy threshold [SYNTHETIC]."""
        bias = self._bias_at_phase(0.5)
        self.assertLess(bias, self.MAX_BIAS_PX)


class TestT3InjectionRecovery(unittest.TestCase):
    """T3: injection/recovery - inject N sources, recover centroid, check rate > 95%.

    [SYNTHETIC] Uses Gaussian PSF (sigma=1.5 px) with Poisson-like noise. Centroid
    is considered recovered when |measured - injected| < 0.5 px in both axes.
    Real ePSF + FITS images needed for production (H-01/H-05).
    """

    N_SOURCES = 100
    SIGMA = 1.5
    SIZE = 21
    NOISE_SIGMA = 0.05
    RECOVERY_THRESHOLD_PX = 0.5
    MIN_RECOVERY_RATE = 0.95

    def test_recovery_rate(self):
        """95%+ of injected sources recovered within 0.5 px [SYNTHETIC]."""
        rng = np.random.default_rng(42)
        recovered = 0
        cx_ref = self.SIZE / 2.0
        cy_ref = self.SIZE / 2.0

        for _ in range(self.N_SOURCES):
            dx = rng.uniform(-0.4, 0.4)
            dy = rng.uniform(-0.4, 0.4)
            x0 = cx_ref + dx
            y0 = cy_ref + dy
            stamp = _gaussian_stamp(x0, y0, sigma=self.SIGMA, size=self.SIZE)
            noise = rng.normal(0, self.NOISE_SIGMA, stamp.shape)
            noisy = stamp + noise
            noisy = np.clip(noisy, 0, None)
            try:
                cx, cy = _centroid_com(noisy)
            except ValueError:
                continue
            if (abs(cx - x0) < self.RECOVERY_THRESHOLD_PX and
                    abs(cy - y0) < self.RECOVERY_THRESHOLD_PX):
                recovered += 1

        rate = recovered / self.N_SOURCES
        self.assertGreaterEqual(
            rate, self.MIN_RECOVERY_RATE,
            f"Recovery rate {rate:.2%} below {self.MIN_RECOVERY_RATE:.0%}",
        )

    def test_noiseless_perfect_recovery(self):
        """Noiseless injection recovers centroid to < 0.01 px [SYNTHETIC]."""
        cx_ref = self.SIZE / 2.0 + 0.3
        cy_ref = self.SIZE / 2.0 - 0.2
        stamp = _gaussian_stamp(cx_ref, cy_ref, sigma=self.SIGMA, size=self.SIZE)
        cx, cy = _centroid_com(stamp)
        self.assertLess(abs(cx - cx_ref), 0.01)
        self.assertLess(abs(cy - cy_ref), 0.01)


if __name__ == "__main__":
    unittest.main()
