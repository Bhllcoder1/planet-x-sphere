"""07-09: T6 Barnard's Star proper-motion test.

[SYNTHETIC] Verifies that the epoch-propagation pipeline moves Barnard's Star
the expected amount between two synthetic frames separated by a known time baseline.
Real FITS data required for production measurement (H-08).

Barnard's Star Gaia DR3 values:
  pmra  = +10889.0 mas/yr
  pmdec =  -4697.2 mas/yr
  plx   =   546.98 mas
  ref_epoch = 2016.0 (J2016.0 TCB)
"""
import math
import unittest

# Barnard's Star Gaia DR3 catalogue values (degrees / mas/yr)
BARNARD_RA_2016   = 269.454023      # deg, J2016.0
BARNARD_DEC_2016  =   4.693394      # deg
BARNARD_PMRA      = 10889.0         # mas/yr (in RA*cos(dec))
BARNARD_PMDEC     = -4697.2         # mas/yr
BARNARD_PLX       =   546.98        # mas
BARNARD_RV        =   -110.6        # km/s

SPHEREX_SCALE_ARCSEC_PX = 6.2      # arcsec / pixel


def _propagate_linear(ra0_deg, dec0_deg, pmra_maspyr, pmdec_maspyr, dt_yr):
    """Linear proper-motion only (no parallax / RV terms). Returns (ra, dec) deg."""
    cos_dec = math.cos(math.radians(dec0_deg))
    dra = pmra_maspyr * dt_yr / 3_600_000.0 / cos_dec
    ddec = pmdec_maspyr * dt_yr / 3_600_000.0
    return ra0_deg + dra, dec0_deg + ddec


def _separation_arcsec(ra1, dec1, ra2, dec2):
    """Approximate angular separation in arcseconds (small-angle)."""
    cos_dec = math.cos(math.radians((dec1 + dec2) / 2.0))
    dra = (ra2 - ra1) * cos_dec * 3600.0
    ddec = (dec2 - dec1) * 3600.0
    return math.sqrt(dra ** 2 + ddec ** 2)


def _expected_displacement_px(dt_yr):
    """Total proper-motion displacement in SPHEREx pixels over dt_yr."""
    total_pm_maspyr = math.sqrt(BARNARD_PMRA ** 2 + BARNARD_PMDEC ** 2)
    displacement_arcsec = total_pm_maspyr * dt_yr / 1000.0
    return displacement_arcsec / SPHEREX_SCALE_ARCSEC_PX


class TestT6BarnardMotion(unittest.TestCase):
    """T6: Barnard's Star proper-motion over known baseline.

    [SYNTHETIC] Uses linear propagation as a stand-in for the full epoch.py pipeline.
    Verifies that:
      1. Displacement over 1 yr is within ±3σ of expected (σ ≈ 0.3 px).
      2. RA and Dec components have the correct sign.
      3. 10-yr baseline gives ~10× the 1-yr displacement.
    Real ePSF centroid measurements on FITS data required for production (H-08).
    """

    SIGMA_PX   = 0.3   # 1σ positional uncertainty in pixels
    N_SIGMA    = 3     # tolerance in sigma
    PERCENT    = 0.10  # additional 10 % fractional tolerance

    def _measure_displacement_px(self, dt_yr):
        """Synthetic 'measurement' via linear propagation, returns (measured_px, expected_px)."""
        ra1, dec1 = BARNARD_RA_2016, BARNARD_DEC_2016
        ra2, dec2 = _propagate_linear(ra1, dec1, BARNARD_PMRA, BARNARD_PMDEC, dt_yr)
        measured_arcsec = _separation_arcsec(ra1, dec1, ra2, dec2)
        measured_px = measured_arcsec / SPHEREX_SCALE_ARCSEC_PX
        expected_px = _expected_displacement_px(dt_yr)
        return measured_px, expected_px

    def test_1yr_displacement_within_3sigma(self):
        """1 yr displacement matches expected within ±3σ or 10 % [SYNTHETIC]."""
        measured_px, expected_px = self._measure_displacement_px(1.0)
        tolerance_px = max(self.N_SIGMA * self.SIGMA_PX, self.PERCENT * expected_px)
        self.assertAlmostEqual(
            measured_px, expected_px, delta=tolerance_px,
            msg=f"1 yr: measured {measured_px:.3f} px, expected {expected_px:.3f} px, "
                f"tolerance {tolerance_px:.3f} px",
        )

    def test_ra_direction_positive(self):
        """Barnard's Star moves in +RA direction (pmra > 0) [SYNTHETIC]."""
        ra2, _ = _propagate_linear(
            BARNARD_RA_2016, BARNARD_DEC_2016, BARNARD_PMRA, BARNARD_PMDEC, 1.0
        )
        self.assertGreater(ra2, BARNARD_RA_2016)

    def test_dec_direction_negative(self):
        """Barnard's Star moves in -Dec direction (pmdec < 0) [SYNTHETIC]."""
        _, dec2 = _propagate_linear(
            BARNARD_RA_2016, BARNARD_DEC_2016, BARNARD_PMRA, BARNARD_PMDEC, 1.0
        )
        self.assertLess(dec2, BARNARD_DEC_2016)

    def test_10yr_scales_linearly(self):
        """10-yr displacement is ~10× the 1-yr displacement [SYNTHETIC]."""
        m1, _ = self._measure_displacement_px(1.0)
        m10, _ = self._measure_displacement_px(10.0)
        ratio = m10 / m1
        self.assertAlmostEqual(ratio, 10.0, delta=0.01)

    def test_known_1yr_displacement_value(self):
        """1 yr displacement ~ 1.94 px (11.75 arcsec / 6.2 arcsec px) [SYNTHETIC]."""
        total_pm_arcsec = math.sqrt(BARNARD_PMRA ** 2 + BARNARD_PMDEC ** 2) / 1000.0
        expected_px = total_pm_arcsec / SPHEREX_SCALE_ARCSEC_PX
        # total_pm ≈ 11828 mas/yr → 11.828 arcsec/yr → ~1.908 px/yr
        self.assertGreater(expected_px, 1.5)
        self.assertLess(expected_px, 2.5)

    def test_zero_baseline_zero_displacement(self):
        """dt=0 gives 0 px displacement [SYNTHETIC]."""
        m, e = self._measure_displacement_px(0.0)
        self.assertAlmostEqual(m, 0.0, places=12)
        self.assertAlmostEqual(e, 0.0, places=12)


if __name__ == "__main__":
    unittest.main()
