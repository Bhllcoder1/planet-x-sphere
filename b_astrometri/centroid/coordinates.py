"""Native float coordinate bridge using A's shared zero-based pixel convention.

The caller must supply the corrected WCS of the actual cutout image, not a
parent-image WCS or an S-mode display projection. This helper does not derive or
verify an astrometric correction and never resamples or snaps image positions.
"""
from __future__ import annotations

import math

from astropy.wcs import WCS

from a_veri_isleme.process.pixel_conventions import cutout_to_parent_pixel


def sky_to_frame_coordinates(
    ra_deg,
    dec_deg,
    *,
    corrected_cutout_wcs,
    crpix1a,
    crpix2a,
):
    """Return scalar cutout and parent x/y positions as zero-based Python floats.

    RA/Dec are degrees in the supplied WCS reference frame. CRPIX1A/2A must
    describe this cutout's alternate parent-pixel WCS; they have no default.
    A's cutout_to_parent_pixel owns the parent bridge arithmetic. For an
    uncut parent grid the caller must explicitly supply an identity bridge.

    Positions outside the image/detector remain unchanged; the measurement
    caller must check its actual image bounds before indexing or ePSF fitting.
    Inverse-WCS errors propagate, so a nonconvergent solution is never accepted.
    """
    try:
        ra, dec, bridge_x, bridge_y = map(float, (ra_deg, dec_deg, crpix1a, crpix2a))
    except (TypeError, ValueError, OverflowError) as error:
        raise ValueError("Sky coordinates and both parent bridge values must be finite scalars") from error
    if not all(math.isfinite(value) for value in (ra, dec, bridge_x, bridge_y)):
        raise ValueError("Sky coordinates and both parent bridge values must be finite scalars")
    if not 0 <= ra < 360 or not -90 <= dec <= 90:
        raise ValueError("Require RA in [0,360) and Dec in [-90,90] degrees")
    if (not isinstance(corrected_cutout_wcs, WCS)
            or corrected_cutout_wcs.pixel_n_dim != 2
            or corrected_cutout_wcs.world_n_dim != 2
            or not corrected_cutout_wcs.has_celestial
            or any(unit != "deg" for unit in corrected_cutout_wcs.world_axis_units)
            or corrected_cutout_wcs.wcs.lngtyp != "RA"
            or corrected_cutout_wcs.wcs.lattyp != "DEC"):
        raise ValueError("An explicit two-dimensional RA/Dec corrected cutout WCS in degrees is required")
    x_cutout, y_cutout = map(float, corrected_cutout_wcs.all_world2pix(
        ra, dec, 0, ra_dec_order=True, tolerance=1e-10, maxiter=50))
    x_parent, y_parent = cutout_to_parent_pixel(x_cutout, y_cutout, bridge_x, bridge_y)
    if not all(math.isfinite(value) for value in (x_cutout, y_cutout, x_parent, y_parent)):
        raise ValueError("WCS/parent conversion returned nonfinite coordinates")
    return {
        "ra_deg": ra,
        "dec_deg": dec,
        "x_cutout": x_cutout,
        "y_cutout": y_cutout,
        "x_parent": x_parent,
        "y_parent": y_parent,
        "pixel_origin": 0,
        "coordinate_frame": "corrected_cutout_and_parent",
        "rounding_applied": False,
        "sky_reference_frame": corrected_cutout_wcs.wcs.radesys or "unspecified",
    }
