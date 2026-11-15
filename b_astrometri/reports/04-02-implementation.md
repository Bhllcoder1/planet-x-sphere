# 04-02 — Pass stacks and differences

Task: https://app.clickup.com/t/z8qu5ddjx4

## Implemented [V: synthetic unit tests]

`b_astrometri/motion/stacks.py` provides:

- `stack_pass(frames, *, target_wcs, shape_out)`: same-detector, same-pass,
  same-release stack, using `reproject_exact` onto a supplied celestial TAN grid.
  Identical input/output grids avoid unnecessary resampling. Native input arrays
  are never changed. A's conservative centroid mask profile, explicit masks,
  nonfinite data and nonpositive variances are excluded.
- `inverse_variance_stack(images, variances, *, masks=None)`:
  `sum(image / variance) / sum(1 / variance)` with nominal variance
  `1 / sum(1 / variance)`. Fewer than two input frames raises an error; output
  pixels with fewer than two valid contributors stay NaN. Coverage and per-frame
  valid projected pixel counts remain available.
- `difference_stacks(left, right, *, channel_width_um)`: left minus right;
  rejects detector/release/grid mismatches, shared input frames, and wavelength
  lists whose full span exceeds one explicitly supplied channel width. No PSF
  matching is performed. QR1/QR2 and unknown releases are refused.
- `validation_metrics(...)`: supplied empty-sky noise ratio and median absolute
  static-source residual divided by nominal difference noise. It reports the
  task's 20% noise and 3-sigma residual criteria, without inventing sky/source
  regions.
- `compare_stack_modes(...)`: D10 rows for detector and channel candidates;
  selects a mode only with a strictly lower median residual and no lower display
  SNR. SNR here is a background-subtracted pixel diagnostic, not forced photometry.
- `write_stack_products(product, directory, *, stem)`: little-endian float32
  image and noise planes plus JSON shape, WCS, provenance, wavelength list and
  mandatory view-only labels. Use `stack_<det>_<pass>` or `diff_<det>_<passes>`
  stems. Scientific data should be written outside the source repository.

All products carry `mode="S"`, `view_only=true`,
`astrometry_allowed=false`, `measurement_allowed=false`, and the badge
**Yeniden örneklendi — astrometri yok**.

Frame dictionaries require `frame_id`, `detector`, `pass_id`, `release`,
`wavelength_um`, `image`, `variance`, `wcs`; optional `mask` and integer `flags`.
The caller supplies already prepared surface-brightness products (MJy/sr) and
their variances in the corresponding squared unit. Wavelengths are micrometres.
`passes.py` supplies pass membership; this helper does not silently regroup it.

## Validation

```powershell
& 'C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe' -I -m unittest discover -s b_astrometri/motion -p test_stacks.py -v
```

**9 tests passed**. Checks include independent weighted-mean values, rejection
of single-frame stacks, insufficient per-pixel coverage, A flag integration,
unchanged inputs, detector/pass/release/channel/grid guards, two rotated WCS
inputs through real `reproject_exact`, synthetic independent-noise reduction,
static-star cancellation, D10 selection, and float32/provenance exports.

The synthetic aligned-grid noise and residual checks pass the task thresholds.
These are software checks on injected data, not astronomical target results.
Runtime dependency is recorded in `motion/requirements.txt`:
`reproject>=0.21,<0.22` (tested with 0.21.0).

## Acceptance still pending [NV]

Reprojecting a variance plane linearly does **not** propagate squared pixel
overlap coefficients or interpolation covariance. Therefore resampled noise
maps are explicitly **nominal diagonal approximations**; only the aligned-grid
noise formula was independently validated. Neither a real-data 20% noise pass
nor astrometric/photometric uncertainty validity is claimed.

The task is conditional on 04-04. This implementation does not claim that the
trigger is satisfied. Real three-target difference screenshots (Q-H4), real
static-source residual measurements, the astronomical D10 comparison, and a
real-data `stacks_report.json` remain pending appropriate manifest/frame inputs.
No fabricated detections, SNR, target acceptance or user approval are recorded.

Local sources read: `spherex-kb/sources/irsa-tut-spherex-source-discovery.md`
and the live 04-02 task snapshot. Native-pixel measurement paths remain separate
from these S-mode display products.
