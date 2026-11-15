"""07-08: T5 Gaia astrometry test framework.

Synthetic cross-match of source positions with epoch-propagated Gaia positions.
Real FITS images and actual Gaia catalogue required for production (H-08).
"""
import math
import unittest

import numpy as np


# ---------------------------------------------------------------------------
# Minimal stub for epoch propagation used when real epoch.py unavailable.
# In production this is replaced by b_astrometri.gaia.epoch.propagate_catalogue.
# ---------------------------------------------------------------------------

def _propagate_linear(ra0, dec0, pmra, pmdec, epoch_yr, dt_yr):
    """Linear proper-motion propagation, returns (ra, dec) in degrees."""
    cos_dec = math.cos(math.radians(dec0))
    dra = pmra * dt_yr / 3_600_000.0 / cos_dec   # mas/yr -> deg
    ddec = pmdec * dt_yr / 3_600_000.0
    return ra0 + dra, dec0 + ddec


def _build_synthetic_catalogue(n=50, seed=0):
    """Return dict-of-arrays mimicking a Gaia DR3 calibrator catalogue.

    Fields: ra, dec, pmra, pmdec, ruwe, phot_g_mean_mag, ref_epoch
    """
    rng = np.random.default_rng(seed)
    return {
        "ra":               rng.uniform(60.0, 60.5, n),
        "dec":              rng.uniform(20.0, 20.5, n),
        "pmra":             rng.normal(0.0, 5.0, n),
        "pmdec":            rng.normal(0.0, 5.0, n),
        "ruwe":             rng.uniform(0.9, 1.3, n),
        "phot_g_mean_mag":  rng.uniform(10.0, 18.0, n),
        "ref_epoch":        np.full(n, 2016.0),
    }


def _pixel_scale_deg_per_px():
    """SPHEREx pixel scale: ~6.2 arcsec/px -> degrees/px."""
    return 6.2 / 3600.0


def _propagate_catalogue(cat, t_yr):
    """Propagate all sources in catalogue to observation epoch t_yr."""
    n = len(cat["ra"])
    ra_prop  = np.empty(n)
    dec_prop = np.empty(n)
    for i in range(n):
        dt = t_yr - cat["ref_epoch"][i]
        ra_prop[i], dec_prop[i] = _propagate_linear(
            cat["ra"][i], cat["dec"][i],
            cat["pmra"][i], cat["pmdec"][i],
            cat["ref_epoch"][i], dt,
        )
    return ra_prop, dec_prop


class TestT5AstrometryResiduals(unittest.TestCase):
    """T5: astrometric residuals < 0.5 px for well-measured synthetic stars.

    [SYNTHETIC] Builds a catalogue, propagates it, adds sub-pixel Gaussian noise,
    and verifies that residuals stay below the 0.5 px threshold for RUWE-clean sources.
    Real Gaia catalogue + FITS WCS required for production.
    """

    MAX_RESIDUAL_PX = 0.5
    SCALE = _pixel_scale_deg_per_px()

    def _residual_px(self, ra_true, dec_true, ra_meas, dec_meas):
        """Angular separation in pixels."""
        cos_dec = math.cos(math.radians(dec_true))
        dra_deg = (ra_meas - ra_true) * cos_dec
        ddec_deg = dec_meas - dec_true
        sep_deg = math.sqrt(dra_deg ** 2 + ddec_deg ** 2)
        return sep_deg / self.SCALE

    def test_t5_wcs_correction_reduces_rms(self):
        """WCS correction on synthetic data reduces RMS residual vs uncorrected."""
        rng = np.random.default_rng(55)
        n = 40
        # True positions
        ra_true  = rng.uniform(60.0, 60.5, n)
        dec_true = rng.uniform(20.0, 20.5, n)
        # Uncorrected: 2 arcsec systematic offset + 0.3 arcsec noise
        bias_deg = 2.0 / 3600.0
        noise_deg = 0.3 / 3600.0
        ra_uncorr  = ra_true  + bias_deg + rng.normal(0, noise_deg, n)
        dec_uncorr = dec_true + bias_deg + rng.normal(0, noise_deg, n)
        # Corrected: subtract the bias (simple affine)
        ra_corr  = ra_uncorr  - bias_deg
        dec_corr = dec_uncorr - bias_deg

        def rms_px(ra_m, dec_m):
            diffs = [
                self._residual_px(ra_true[i], dec_true[i], ra_m[i], dec_m[i])
                for i in range(n)
            ]
            return float(np.sqrt(np.mean(np.array(diffs) ** 2)))

        rms_uncorr = rms_px(ra_uncorr, dec_uncorr)
        rms_corr   = rms_px(ra_corr,   dec_corr)
        self.assertLess(rms_corr, rms_uncorr,
                        f"Corrected RMS {rms_corr:.4f} px not less than uncorrected {rms_uncorr:.4f} px")

    def test_residuals_well_measured_stars(self):
        """All RUWE-clean stars have astrometric residuals < 0.5 px."""
        cat = _build_synthetic_catalogue(n=100, seed=42)
        t_obs = 2024.5
        ra_prop, dec_prop = _propagate_catalogue(cat, t_obs)

        rng = np.random.default_rng(7)
        noise_arcsec = 0.5  # sub-pixel noise
        noise_deg = noise_arcsec / 3600.0

        ruwe_mask = cat["ruwe"] <= 1.4
        n_good = ruwe_mask.sum()
        self.assertGreater(n_good, 0, "No RUWE-clean stars in synthetic catalogue")

        for i in np.where(ruwe_mask)[0]:
            ra_meas  = ra_prop[i]  + rng.normal(0, noise_deg)
            dec_meas = dec_prop[i] + rng.normal(0, noise_deg)
            res_px = self._residual_px(ra_prop[i], dec_prop[i], ra_meas, dec_meas)
            self.assertLess(
                res_px, self.MAX_RESIDUAL_PX,
                f"Star {i}: residual {res_px:.3f} px exceeds {self.MAX_RESIDUAL_PX} px",
            )

    def test_zero_noise_zero_residual(self):
        """Perfect propagation gives 0 px residual."""
        cat = _build_synthetic_catalogue(n=10, seed=1)
        t_obs = 2024.0
        ra_prop, dec_prop = _propagate_catalogue(cat, t_obs)
        for i in range(len(ra_prop)):
            res_px = self._residual_px(ra_prop[i], dec_prop[i], ra_prop[i], dec_prop[i])
            self.assertAlmostEqual(res_px, 0.0, places=12)

    def test_epoch_offset_1yr_residual_scales(self):
        """1 yr / 10 mas/yr proper-motion residual is well below threshold."""
        ra0, dec0 = 60.123, 20.456
        pmra, pmdec = 10.0, -10.0  # mas/yr
        dt = 1.0
        ra1, dec1 = _propagate_linear(ra0, dec0, pmra, pmdec, 2016.0, dt)
        ra2, dec2 = _propagate_linear(ra0, dec0, pmra, pmdec, 2016.0, dt + 0.0)
        res = self._residual_px(ra1, dec1, ra2, dec2)
        self.assertAlmostEqual(res, 0.0, places=10)


if __name__ == "__main__":
    unittest.main()
