"""04-16: Shift-and-add stacker for moving-object co-addition.

[STUB] Viewer integration (02-16) pending; stack logic is complete.
No round/floor/ceil — fractional shifts passed directly to scipy.
"""

import numpy as np
from scipy.ndimage import shift as nd_shift


def shift_add_stack(
    images: list,
    vx_px_hr: float,
    vy_px_hr: float,
    mjd_list: list,
    t_ref_mjd: float,
) -> np.ndarray:
    """Co-add frames shifted to track a moving object.

    Each image is shifted by (vx*dt, vy*dt) where dt = mjd - t_ref_mjd
    (converted hours: dt_hr = dt_days * 24). Fractional shifts are
    passed directly to scipy.ndimage.shift — no rounding.

    Args:
        images:     List of 2-D float arrays (must share shape).
        vx_px_hr:   Velocity in x (column) direction, pixels/hour.
        vy_px_hr:   Velocity in y (row) direction, pixels/hour.
        mjd_list:   MJD timestamps, one per image.
        t_ref_mjd:  Reference epoch MJD (zero-shift frame).

    Returns:
        Stacked 2-D array (mean of shifted frames, NaN-safe).
    """
    if len(images) != len(mjd_list):
        raise ValueError("images and mjd_list must have equal length")

    shifted = []
    for img, mjd in zip(images, mjd_list):
        dt_hr = (mjd - t_ref_mjd) * 24.0
        dy = vy_px_hr * dt_hr   # row shift
        dx = vx_px_hr * dt_hr   # col shift
        shifted_frame = nd_shift(
            img.astype(float),
            shift=(dy, dx),
            mode="constant",
            cval=float("nan"),
        )
        shifted.append(shifted_frame)

    stack = np.array(shifted)
    return np.nanmean(stack, axis=0)
