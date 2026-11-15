import math
import unittest

import numpy as np
from astropy.io import fits
from astropy.wcs import WCS

from joint_fit import fit_joint_pass
from test_epsf import EPSFTests, fixture


def _rotated_wcs(ra0: float, dec0: float, roll_deg: float) -> WCS:
    hdr = fits.Header()
    hdr["NAXIS"] = 2
    hdr["NAXIS1"] = 2040
    hdr["NAXIS2"] = 2040
    hdr["CTYPE1"] = "RA---TAN"
    hdr["CTYPE2"] = "DEC--TAN"
    hdr["CRPIX1"] = 1020.5
    hdr["CRPIX2"] = 1020.5
    hdr["CRVAL1"] = ra0
    hdr["CRVAL2"] = dec0
    scale = 6.15 / 3600.0
    th = math.radians(roll_deg)
    c, s = math.cos(th), math.sin(th)
    hdr["CD1_1"] = -scale * c
    hdr["CD1_2"] = scale * s
    hdr["CD2_1"] = scale * s
    hdr["CD2_2"] = scale * c
    return WCS(hdr)


class JointFitTests(unittest.TestCase):
    def test_20_frame_joint_pass_beats_single_frame_sigma_and_reports_exclusions(self):
        grid = EPSFTests().grid(fixture(detector=2), norm=1.0)
        rng = np.random.default_rng(55)
        ra_true, dec_true = 269.4523, 4.6931

        frames = []
        for k in range(20):
            wcs = _rotated_wcs(269.452, 4.693, roll_deg=float(k) * 0.2)
            xk, yk = wcs.all_world2pix(ra_true, dec_true, 0)
            cx0, cy0 = float(int(xk)), float(int(yk))
            yy, xx = np.mgrid[-4:5, -4:5] + np.array([[[cy0]], [[cx0]]])
            flux_k = 2000.0 + 50.0 * k
            bg_k = 8.0 + 0.5 * k
            clean = grid.model_at(float(xk), float(yk)).evaluate(xx, yy, flux_k, float(xk), float(yk)) + bg_k
            var = np.full_like(clean, 4.0)
            noisy = clean + rng.normal(0.0, 2.0, size=clean.shape)
            frames.append({
                "frame_id": f"f_{k}",
                "grid": grid,
                "wcs": wcs,
                "xx": xx,
                "yy": yy,
                "image": noisy,
                "variance": var,
                "mjd": 60100.0 + k * 0.5,
                "cwave_um": 1.0 + 0.05 * k,
            })

        # 2 kareyi bad_fit ve unusable_for_astrometry olarak ekle -> sessizce dusmemeli, raporlanmali
        frames.append({**frames[0], "frame_id": "bad_1", "bad_fit": True})
        frames.append({**frames[1], "frame_id": "unusable_1", "unusable_for_astrometry": True})

        single = fit_joint_pass([frames[0]], ra_true + 1e-4, dec_true - 1e-4)
        joint = fit_joint_pass(frames, ra_true + 1e-4, dec_true - 1e-4)
        self.assertEqual(joint["status"], "ok")
        self.assertEqual(joint["n_used"], 20)
        self.assertEqual(joint["n_excluded"], 2)
        self.assertLess(joint["ellipse_arcsec"]["sig_x"], single["ellipse_arcsec"]["sig_x"] / 3.0)
        self.assertLess(joint["ellipse_arcsec"]["sig_y"], single["ellipse_arcsec"]["sig_y"] / 3.0)

        err_ra = (joint["ra_deg"] - ra_true) * math.cos(math.radians(dec_true)) * 3600.0
        err_dec = (joint["dec_deg"] - dec_true) * 3600.0
        self.assertLess(abs(err_ra), 3.0 * joint["ellipse_arcsec"]["sig_x"])
        self.assertLess(abs(err_dec), 3.0 * joint["ellipse_arcsec"]["sig_y"])


if __name__ == "__main__":
    unittest.main()
