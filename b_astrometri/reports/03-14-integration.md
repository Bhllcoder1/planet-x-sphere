# 03-14 — Shared native coordinate bridge

Task: https://app.clickup.com/t/z8qu5ddjx1

## Implementation, static review only

`b_astrometri/centroid/coordinates.py` exposes:

```python
sky_to_frame_coordinates(
    ra_deg, dec_deg, *, corrected_cutout_wcs, crpix1a, crpix2a
)
```

The supplied two-dimensional RA/Dec WCS must use degree world-axis units and belong to the actual native
cutout image and already contain the caller's astrometric correction. The
helper requests `all_world2pix(..., origin=0)` with explicit RA/Dec argument
order, then calls the existing A implementation
`a_veri_isleme.process.pixel_conventions.cutout_to_parent_pixel`.
It does not reproduce the parent bridge formula or add half-pixel offsets.

Both `crpix1a` and `crpix2a` are mandatory and must describe that cutout.
Their absence is not replaced by a guessed origin. For an uncut parent image
an identity bridge must be supplied explicitly. The output keeps distinct
`x_cutout`, `y_cutout`, `x_parent`, `y_parent` Python float values; there is no
rounding, integer conversion, clipping or resampling. Sky coordinates and
bridge values are validated; inverse-WCS convergence errors propagate.

The output record includes `pixel_origin=0`, `rounding_applied=false` and
the supplied WCS's sky reference-frame label. RA/Dec inputs must already use
that reference frame; this helper does not silently transform epochs or
celestial frames.

The forced-photometry caller can use parent floats for
`EPSFGrid.zone_at` / `model_at`, and cutout floats for its native image window.
The caller remains responsible for image/detector bounds and for verifying
that an actual corrected native WCS, rather than a raw/header/display WCS,
was supplied. A function argument name cannot establish the scientific
validity of an upstream WCS solution.

## Evidence limits [NV]

Per the current user instruction, **no tests were added or run**, and this
helper was not executed. Review consisted of reading the live 03-14 task,
A's pixel functions, and the ePSF parent-coordinate API, then inspecting the
implementation statically.

This narrow integration does not close 03-14 acceptance. Actual production
corrected-WCS provenance, 03-03 outputs, complete cat/geom/client coordinate
serialization, the 4.47 → 447 screen-value acceptance, and full-path rounding
audit remain unverified here. No new numerical result or target measurement
is claimed.
