"""03-15: WiseView/Gaia epoch-error prevention test.

WiseView overlays Gaia DR2/DR3 catalog positions onto WISE images without applying
proper motion. For high-mu stars (Barnard's Star: mu_dec ~10 300 mas/yr) the catalog
epoch is 2016.0, but WISE W1 images are from ~2010–2011. The resulting offset is tens
of arcseconds — easily mistaken for a detection mismatch or a moving-object candidate.

This module verifies that epoch.py:
  1. Correctly propagates positions from ref_epoch (2016.0) to a WISE-era MJD.
  2. Produces an offset that matches a simple linear approximation within tolerance.
  3. The epoch-uncorrected (WiseView-style) position differs by > THRESHOLD from ours.

Run offline with:
    python -I -m unittest b_astrometri/gaia/test_epoch_wiseview.py -v
"""
import importlib.util
from pathlib import Path
import unittest

import numpy as np
from astropy.table import Table

spec = importlib.util.spec_from_file_location("gaia_epoch", Path(__file__).with_name("epoch.py"))
epoch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(epoch)

# ---------------------------------------------------------------------------
# Reference star: Barnard's Star (Gaia DR3 source 4472832130942575872)
# Values from published Gaia DR3 catalog (approximate); [ASSUMPTION: RV = -110 km/s]
# ---------------------------------------------------------------------------
BARNARD = {
    "source_id": 4472832130942575872,
    "ra": 269.4520706,       # deg ICRS at ref_epoch
    "dec": 4.6933896,        # deg ICRS at ref_epoch
    "pmra": -800.804,        # mas/yr  (mu_alpha * cos(dec))
    "pmdec": 10362.394,      # mas/yr
    "parallax": 547.45,      # mas
    "ref_epoch": 2016.0,     # Julian year TCB (Gaia DR3 standard)
}
RV_KMS = -110.0              # [ASSUMPTION: taken from SIMBAD / stage-0 experiments]

# WISE W1 all-sky survey epoch: roughly 2010 Jan–2011 Feb.
# MJD 55197 ≈ 2010-01-14 UTC — conservative mid-survey choice.
WISE_MJD = 55197.0

# Minimum offset we expect between WiseView (no PM) and our propagated position.
# 10 arcsec is a very conservative lower bound; the true value is ~50 arcsec.
MIN_OFFSET_ARCSEC = 10.0

# Maximum allowed discrepancy between our result and a simple linear-PM approximation.
# Linear PM ignores observer parallax, curvature, and Römer delay.
# Barnard's parallax is ~547 mas, so the RA observer-parallax component alone
# can reach ~150–200 mas at WISE epoch (Jan 2010, Sun near ecl lon 283°, star at 266°).
# 600 mas = 0.600 arcsec is a generous but physically motivated upper bound.
LINEAR_TOLERANCE_ARCSEC = 0.600


def barnard_catalogue():
    return Table({k: [v] for k, v in BARNARD.items()})


class WiseViewEpochTests(unittest.TestCase):
    """03-15 — confirm our code avoids the WiseView epoch-offset error."""

    def setUp(self):
        self.cat = barnard_catalogue()
        self.result = epoch.propagate_catalogue(
            self.cat, WISE_MJD, radial_velocity_kms=RV_KMS
        )

    # ------------------------------------------------------------------
    # 1. Propagated position is finite and in valid ranges
    # ------------------------------------------------------------------
    def test_propagated_position_is_finite_and_valid(self):
        ra = float(self.result["ra_deg"][0])
        dec = float(self.result["dec_deg"][0])
        self.assertTrue(np.isfinite(ra), "Propagated RA is not finite")
        self.assertTrue(np.isfinite(dec), "Propagated Dec is not finite")
        self.assertGreaterEqual(ra, 0.0)
        self.assertLess(ra, 360.0)
        self.assertGreaterEqual(dec, -90.0)
        self.assertLessEqual(dec, 90.0)

    # ------------------------------------------------------------------
    # 2. Offset from catalog epoch vs WISE epoch is large (WiseView error)
    # ------------------------------------------------------------------
    def test_wiseview_epoch_offset_exceeds_threshold(self):
        """Without proper motion (WiseView style), the catalog position (2016.0)
        is offset from the WISE-era true position by more than MIN_OFFSET_ARCSEC."""
        ra_catalog = BARNARD["ra"]
        dec_catalog = BARNARD["dec"]
        ra_prop = float(self.result["ra_deg"][0])
        dec_prop = float(self.result["dec_deg"][0])

        # Great-circle separation in arcsec (small-angle approximation is fine here)
        d_ra_arcsec = (ra_prop - ra_catalog) * np.cos(np.deg2rad(dec_catalog)) * 3600.0
        d_dec_arcsec = (dec_prop - dec_catalog) * 3600.0
        offset_arcsec = np.hypot(d_ra_arcsec, d_dec_arcsec)

        self.assertGreater(
            offset_arcsec, MIN_OFFSET_ARCSEC,
            f"Epoch offset {offset_arcsec:.2f}\" is unexpectedly small; "
            f"expected >{MIN_OFFSET_ARCSEC}\" for Barnard's Star over ~5.5 yr"
        )

    # ------------------------------------------------------------------
    # 3. Our result agrees with a simple linear-PM approximation (no parallax)
    #    to within LINEAR_TOLERANCE_ARCSEC.  This guards against sign errors
    #    or unit confusion in the propagation direction.
    # ------------------------------------------------------------------
    def test_propagation_direction_matches_linear_approximation(self):
        """Linear PM (ignoring parallax/curvature) should agree with epoch.py
        to within LINEAR_TOLERANCE_ARCSEC in each axis."""
        # Julian years from ref_epoch 2016.0 to WISE MJD
        # MJD 51544.5 = J2000.0, so J_year = 2000.0 + (MJD - 51544.5) / 365.25
        wise_jyear = 2000.0 + (WISE_MJD - 51544.5) / 365.25
        dt_yr = wise_jyear - BARNARD["ref_epoch"]   # negative: WISE is before 2016

        cos_dec = np.cos(np.deg2rad(BARNARD["dec"]))
        # Linear: delta in degrees
        d_ra_linear_deg = BARNARD["pmra"] * dt_yr / (1000.0 * 3600.0 * cos_dec)
        d_dec_linear_deg = BARNARD["pmdec"] * dt_yr / (1000.0 * 3600.0)

        ra_linear = BARNARD["ra"] + d_ra_linear_deg
        dec_linear = BARNARD["dec"] + d_dec_linear_deg

        ra_prop = float(self.result["ra_deg"][0])
        dec_prop = float(self.result["dec_deg"][0])

        # RA difference in arcsec (along the sky, not on the equator)
        d_ra_arcsec = abs(ra_prop - ra_linear) * cos_dec * 3600.0
        d_dec_arcsec = abs(dec_prop - dec_linear) * 3600.0

        self.assertLess(
            d_ra_arcsec, LINEAR_TOLERANCE_ARCSEC,
            f"RA differs from linear approx by {d_ra_arcsec:.4f}\"; "
            f"expected <{LINEAR_TOLERANCE_ARCSEC}\""
        )
        self.assertLess(
            d_dec_arcsec, LINEAR_TOLERANCE_ARCSEC,
            f"Dec differs from linear approx by {d_dec_arcsec:.4f}\"; "
            f"expected <{LINEAR_TOLERANCE_ARCSEC}\""
        )

    # ------------------------------------------------------------------
    # 4. Direction of motion is correct: Barnard moves north and westward
    #    (pmra < 0, pmdec > 0).  Going back in time to 2010 means the star
    #    was to the SOUTH and to the EAST of its 2016 catalog position.
    # ------------------------------------------------------------------
    def test_barnard_was_south_and_east_at_wise_epoch(self):
        """In 2010 Barnard was south (lower Dec) and east (higher RA) of 2016 catalog."""
        ra_prop = float(self.result["ra_deg"][0])
        dec_prop = float(self.result["dec_deg"][0])
        # Dec must be less than catalog Dec (star moves north, so 2010 it was further south)
        self.assertLess(dec_prop, BARNARD["dec"],
                        "In 2010 Barnard should be south of its 2016 position")
        # RA must be greater (star moves west, i.e. decreasing RA over time, so 2010 it was east)
        self.assertGreater(ra_prop, BARNARD["ra"],
                           "In 2010 Barnard should be east of (higher RA than) its 2016 position")

    # ------------------------------------------------------------------
    # 5. Barycentric RA/Dec fields are also populated and finite
    # ------------------------------------------------------------------
    def test_barycentric_fields_populated(self):
        self.assertIn("ra_bary_deg", self.result.colnames)
        self.assertIn("dec_bary_deg", self.result.colnames)
        self.assertTrue(np.isfinite(float(self.result["ra_bary_deg"][0])))
        self.assertTrue(np.isfinite(float(self.result["dec_bary_deg"][0])))

    # ------------------------------------------------------------------
    # 6. Meta records the WISE MJD used (traceability)
    # ------------------------------------------------------------------
    def test_result_meta_records_mjd(self):
        self.assertAlmostEqual(self.result.meta["mjd_utc"], WISE_MJD)


if __name__ == "__main__":
    unittest.main()
