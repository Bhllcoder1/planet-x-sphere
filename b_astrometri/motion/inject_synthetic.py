"""04-17: Synthetic object injection into a viewing copy.

[PARTIAL] viewer integration (02-16) pending; injection logic complete.
Real ePSF from 03-01 available; this module stamps it onto a pixel copy.
"""

import numpy as np


_STAMP_HALF = 4   # 9x9 stamp: half-width = 4 pixels


def inject_object(
    image: np.ndarray,
    epsf_model,
    x_px: float,
    y_px: float,
    flux: float,
) -> dict:
    """Inject a synthetic point source into a copy of the image.

    Stamps a 9×9 ePSF at sub-pixel position (x_px, y_px) scaled by
    flux. Returns a dict wrapper so callers can access metadata.

    Args:
        image:      2-D float array (input, not modified in-place).
        epsf_model: photutils EPSFModel or callable f(x, y) → 2-D array.
        x_px:       Sub-pixel column position (0-based float).
        y_px:       Sub-pixel row position (0-based float).
        flux:       Total source flux to inject.

    Returns:
        dict with keys:
            'data'      — modified 2-D float array (copy)
            'SYNTHETIC' — True
            'x_px'      — injected x
            'y_px'      — injected y
            'flux'      — injected flux
    """
    out = image.astype(float, copy=True)
    ny, nx = out.shape

    # Integer centre of stamp
    ix = int(x_px)
    iy = int(y_px)

    # Pixel grid for 9x9 stamp (sub-pixel offset from stamp centre)
    half = _STAMP_HALF
    rows = np.arange(-half, half + 1)
    cols = np.arange(-half, half + 1)
    col_grid, row_grid = np.meshgrid(cols, rows)

    # Sub-pixel offset
    dx = x_px - ix
    dy = y_px - iy

    # Evaluate ePSF on the stamp grid
    stamp = epsf_model(col_grid - dx, row_grid - dy)
    stamp_norm = stamp / (stamp.sum() if stamp.sum() != 0.0 else 1.0)
    stamp_scaled = stamp_norm * flux

    # Paste into output with boundary clipping
    for dr in range(-half, half + 1):
        for dc in range(-half, half + 1):
            rr = iy + dr
            cc = ix + dc
            if 0 <= rr < ny and 0 <= cc < nx:
                stamp_r = dr + half
                stamp_c = dc + half
                out[rr, cc] += stamp_scaled[stamp_r, stamp_c]

    return {
        "data": out,
        "SYNTHETIC": True,
        "x_px": x_px,
        "y_px": y_px,
        "flux": flux,
    }


if __name__ == "__main__":
    rng = np.random.default_rng(17)
    base = rng.uniform(10, 20, (64, 64))
    flux_before = float(base.sum())

    # Simple Gaussian ePSF mock
    def gaussian_epsf(col, row, sigma=1.5):
        return np.exp(-(col**2 + row**2) / (2 * sigma**2))

    result = inject_object(base, gaussian_epsf, x_px=32.3, y_px=31.7, flux=500.0)

    assert result["SYNTHETIC"] is True, "SYNTHETIC flag must be True"
    flux_after = float(result["data"].sum())
    assert flux_after > flux_before, f"flux after {flux_after:.1f} must exceed before {flux_before:.1f}"
    print(f"Flux before: {flux_before:.1f}, after: {flux_after:.1f} (injected 500.0)")
    print("DONE 04-17")
