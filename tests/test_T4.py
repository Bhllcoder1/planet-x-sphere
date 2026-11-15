"""07-04 (T4): WCS piksel -> gok -> piksel gidis-donus dogrulamasi (< 1e-4 px).

AP/BP ters terimi tek basina kullanilmaz; all_pix2world(..., 0) ardindan
all_world2pix(..., 0, tolerance=1e-8, maxiter=50) kullanilir.
"""
import unittest

import numpy as np
from astropy.io import fits
from astropy.wcs import WCS


def _spherex_like_sip_wcs() -> WCS:
    """SPHEREx benzeri 6.15"/px, SIP duzeni 3 sentetik WCS."""
    hdr = fits.Header()
    hdr["NAXIS"] = 2
    hdr["NAXIS1"] = 2040
    hdr["NAXIS2"] = 2040
    hdr["CTYPE1"] = "RA---TAN-SIP"
    hdr["CTYPE2"] = "DEC--TAN-SIP"
    hdr["CRPIX1"] = 1020.5
    hdr["CRPIX2"] = 1020.5
    hdr["CRVAL1"] = 269.452
    hdr["CRVAL2"] = 4.693
    scale = 6.15 / 3600.0
    hdr["CD1_1"] = -scale
    hdr["CD1_2"] = 0.0
    hdr["CD2_1"] = 0.0
    hdr["CD2_2"] = scale
    hdr["A_ORDER"] = 3
    hdr["B_ORDER"] = 3
    hdr["A_2_0"] = 1.5e-6
    hdr["A_0_2"] = -1.2e-6
    hdr["A_3_0"] = 4.0e-10
    hdr["B_2_0"] = -1.1e-6
    hdr["B_0_2"] = 1.4e-6
    hdr["B_0_3"] = -3.5e-10
    return WCS(hdr)


class T4WCSRoundtripTests(unittest.TestCase):
    def test_t4_pix_to_world_to_pix_under_1e4_px(self):
        wcs = _spherex_like_sip_wcs()
        rng = np.random.default_rng(99)
        x_in = np.concatenate([[0.0, 2039.0, 1020.0], rng.uniform(0.0, 2039.0, 200)])
        y_in = np.concatenate([[0.0, 2039.0, 1020.0], rng.uniform(0.0, 2039.0, 200)])

        ra, dec = wcs.all_pix2world(x_in, y_in, 0)
        x_out, y_out = wcs.all_world2pix(ra, dec, 0, tolerance=1e-8, maxiter=50)
        err = np.hypot(x_out - x_in, y_out - y_in)
        self.assertLess(float(np.max(err)), 1e-4)


if __name__ == "__main__":
    unittest.main()
