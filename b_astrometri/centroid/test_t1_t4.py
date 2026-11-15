"""
T1: integer-shift centroid recovery test.
T4: WCS pixel→sky→pixel round-trip test.
Real FITS from H-08/H-11 needed for production; synthetic tests here.
"""
from __future__ import annotations

import numpy as np
from astropy.wcs import WCS


def _make_gaussian_image(size: int = 32, cx: float = 16.0, cy: float = 16.0,
                         sigma: float = 2.0) -> np.ndarray:
    y, x = np.mgrid[0:size, 0:size]
    return np.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (2 * sigma ** 2))


def _centroid_com(img: np.ndarray) -> tuple:
    """Centre-of-mass centroid; no round/floor/ceil."""
    total = img.sum()
    y, x = np.mgrid[0:img.shape[0], 0:img.shape[1]]
    cx = float((x * img).sum() / total)
    cy = float((y * img).sum() / total)
    return cx, cy


def test_t1_integer_shift() -> None:
    """T1: shift a Gaussian source by exactly 4 px; centroid must recover within 0.1 px."""
    size = 32
    shift = 4
    img_orig = _make_gaussian_image(size, cx=12.0, cy=16.0)
    img_shifted = np.roll(img_orig, shift, axis=1)   # shift along x
    cx, cy = _centroid_com(img_shifted)
    expected_cx = 12.0 + shift
    assert abs(cx - expected_cx) < 0.1, f"T1 fail: cx={cx:.4f} expected {expected_cx}"
    assert abs(cy - 16.0) < 0.1, f"T1 fail: cy={cy:.4f} expected 16.0"


def test_t4_wcs_roundtrip() -> None:
    """T4: TAN WCS pixel→sky→pixel round-trip error must be < 1e-6 px."""
    wcs = WCS(naxis=2)
    wcs.wcs.crpix = [16.0, 16.0]
    wcs.wcs.crval = [0.0, 0.0]
    cdelt = 6.2 / 3600.0          # SPHEREx pixel scale in degrees
    wcs.wcs.cdelt = [cdelt, cdelt]
    wcs.wcs.ctype = ["RA---TAN", "DEC--TAN"]
    wcs.wcs.set()

    # Test a grid of pixel positions
    rng = np.random.default_rng(42)
    px_in = rng.uniform(1.0, 31.0, (20, 2))
    sky = wcs.all_pix2world(px_in, 0)
    px_out = wcs.all_world2pix(sky, 0)
    max_err = float(np.max(np.abs(px_out - px_in)))
    assert max_err < 1e-6, f"T4 roundtrip error {max_err:.2e} >= 1e-6 px"


def test_t4_no_rounding_in_centroid() -> None:
    """Coord-audit: centroid must stay float throughout; no integer truncation."""
    img = _make_gaussian_image(32, cx=15.7, cy=16.3)
    cx, cy = _centroid_com(img)
    assert isinstance(cx, float)
    assert isinstance(cy, float)
    assert abs(cx - 15.7) < 0.05, f"Sub-pixel accuracy fail: cx={cx:.4f}"


if __name__ == "__main__":
    test_t1_integer_shift()
    test_t4_wcs_roundtrip()
    test_t4_no_rounding_in_centroid()
    print("DONE 07-04")
