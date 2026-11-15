"""04-15: sliding-window stacks/differences on a common TAN grid, display only."""
from __future__ import annotations

import math

import numpy as np

from b_astrometri.motion.stacks import BADGE, difference_stacks, stack_pass


def rolling_window(frames, window_start_mjd, *, target_wcs, shape_out,
                   channel_width_um, window_days=None):
    """Build inside-minus-outside views for one detector/pass/release/channel.

    Input dictionaries follow ``stack_pass`` and additionally require finite
    ``mjd`` (UTC exposure midpoint). The window is [start, start + days).
    Default days = one third of the supplied pass span, a plan assumption.
    Both sides use exact reprojection through ``stack_pass``; neither native
    images nor their masks are changed. Fewer than two valid contributors at a
    pixel gives NaN, never a zero-flux measurement.

    Legend: '+' contributes to the window stack, '-' to the outside reference,
    '.' is unused (no valid projected pixels, or its stack is unavailable).
    These are roles in this window, not changes from a previous window.
    """
    frames = list(frames)
    if not frames:
        raise ValueError("A nonempty pass frame list is required")
    try:
        ids = [str(frame["frame_id"]) for frame in frames]
        times = np.asarray([frame["mjd"] for frame in frames], dtype=float)
        wavelengths = np.asarray([frame["wavelength_um"] for frame in frames], dtype=float)
        for field in ("detector", "pass_id", "release"):
            if len({frame[field] for frame in frames}) != 1:
                raise ValueError(f"Rolling views cannot mix {field} values")
    except KeyError as error:
        raise ValueError(f"Missing frame field: {error.args[0]}") from error
    if any(not fid for fid in ids) or len(ids) != len(set(ids)):
        raise ValueError("Frame IDs must be nonempty and unique")
    if times.shape != (len(frames),) or not np.all(np.isfinite(times)):
        raise ValueError("Each frame needs one finite UTC MJD")
    if frames[0]["detector"] not in range(1, 7) or frames[0]["release"] not in {"DR1", "QR3"}:
        raise ValueError("Require detector 1..6 and explicit DR1 or QR3 release")
    start, channel_width = float(window_start_mjd), float(channel_width_um)
    if not math.isfinite(start) or not math.isfinite(channel_width) or channel_width <= 0:
        raise ValueError("Window start must be finite and channel width positive")
    if (wavelengths.shape != times.shape or not np.all(np.isfinite(wavelengths))
            or np.any(wavelengths <= 0)):
        raise ValueError("Frame wavelengths must be finite positive micrometres")
    if float(np.ptp(wavelengths)) > channel_width:
        raise ValueError("All window/reference frames must fit within one wavelength channel")
    default_length = window_days is None
    days = float(np.ptp(times) / 3) if default_length else float(window_days)
    if not math.isfinite(days) or days <= 0 or not math.isfinite(start + days):
        raise ValueError("Window days must be positive; a zero-span pass needs an explicit length")
    inside = (times >= start) & (times < start + days)
    groups = {"inside": [f for f, keep in zip(frames, inside) if keep],
              "outside": [f for f, keep in zip(frames, inside) if not keep]}
    products, side_status = {}, {}
    for name, members in groups.items():
        if len(members) < 2:
            products[name], side_status[name] = None, "insufficient_frames"
        else:
            product = stack_pass(members, target_wcs=target_wcs, shape_out=shape_out)
            products[name] = product
            side_status[name] = "ok" if np.any(np.isfinite(product["image"])) else "no_valid_pixels"
    difference = None
    if all(status == "ok" for status in side_status.values()):
        difference = difference_stacks(products["inside"], products["outside"],
                                       channel_width_um=channel_width)
    if difference is None:
        status = "unavailable_difference"
    else:
        status = "ok" if np.any(np.isfinite(difference["image"])) else "no_common_coverage"
    roles = []
    for fid, mjd, is_inside in zip(ids, times, inside):
        side = "inside" if is_inside else "outside"
        product = products[side]
        count = product["frame_valid_pixels"][fid] if product is not None else None
        role = ("+" if is_inside else "-") if side_status[side] == "ok" and count else "."
        roles.append({"frame_id": fid, "mjd": float(mjd), "role": role,
                      "inside_window": bool(is_inside), "projected_valid_pixels": count})
    return {"status": status, "mode": "S", "view_only": True,
            "measurement_allowed": False, "astrometry_allowed": False, "badge": BADGE,
            "window_start_mjd": start, "window_end_mjd": start + days,
            "window_days": days, "window_interval": "start inclusive, end exclusive",
            "window_days_source": "ASSUMPTION: one third of supplied pass span" if default_length else "caller",
            "channel_width_um": channel_width, "detector": frames[0]["detector"],
            "pass_id": frames[0]["pass_id"], "release": frames[0]["release"],
            "inside": products["inside"], "outside": products["outside"],
            "side_status": side_status, "difference": difference, "frame_roles": roles,
            "legend": {"+": "window contribution", "-": "outside reference contribution", ".": "unused"},
            "noise_validation": "nominal diagonal variance; real blank-sky/Gaia/Barnard validation pending"}
