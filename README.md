# planet-x-sphere

SPHEREx astrometry pipeline — Gaia epoch propagation, ePSF photometry, moving object linking, and forced photometry for nearby star and solar system targets.

## What it does

This pipeline processes SPHEREx cutout images to:

- **Fetch and propagate Gaia DR3 catalogues** to the observation epoch (proper motion + parallax), with WiseView cross-check tests
- **Build an effective PSF (ePSF)** from a `GriddedPSFModel` (33×33 stamp, 5× oversampling) and fit centroids from the wings of saturated sources
- **Perform forced photometry** at a fixed sky position across all frames of a transit, combining per-frame flux measurements by inverse-variance weighting
- **Link moving objects** using a pair-supported sparse velocity lattice with RANSAC-style consensus/refit
- **Stack and diff transits** (rolling-window and pass-stack modes, view-only)
- **Guard candidates** against STREAK, GHOST, CROSSTALK, TRANSIENT, and HALO flag bits

## Repository layout

```
b_astrometri/
  gaia/          Gaia TAP fetch, epoch propagation, WiseView tests
  centroid/      ePSF grid, wing fit, error ellipse, joint fit
  motion/        Forced photometry, transit stacking, light curves
  movers/        Moving-object linker, OUTLIER promotion, veto guard
  reports/       Implementation reports and status notes (not FITS)
docs/
  second-brain/  TASKS.md, human-action log, project memory
```

## Running the tests

Stage 0 virtual environment (Windows):

```powershell
$py = 'C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe'
& $py -I -m unittest discover -s b_astrometri/centroid -p 'test_*.py'
& $py -I -m unittest discover -s b_astrometri/gaia     -p 'test_*.py'
& $py -I -m unittest discover -s b_astrometri/movers   -p 'test_*.py'
& $py -I -m unittest discover -s b_astrometri/motion   -p 'test_*.py'
```

Last run: centroid 28, gaia 35, movers 11, motion 15 = **89 tests OK** (all synthetic).

## Coordinate audit

All production `.py` files must pass `coord_audit.py`. Forbidden calls:

- `round()`, `math.floor()`, `math.ceil()`, `math.trunc()`, `np.rint()`
- WCS pixel-to-sky with `origin=1`

Pixel scale must be derived from `proj_plane_pixel_scales(wcs)`, never hardcoded.

## Science targets

All targets are pending real FITS delivery (H-xx human-input gates):

| Target | Frames | Passes | Gate |
|---|---|---|---|
| Barnard's Star | ~358 | 3 | H-01, H-08 |
| ε Indi B | ~458 | 4 | H-01, H-08 |
| WISE 0855−0714 | unknown (TAP failed) | unknown | H-09 |
| RW Aurigae | unknown (TAP failed) | unknown | H-09, H-12 |
| R Draconis | unknown (TAP failed) | unknown | H-09 |

Synthetic pass-grouping and stacking verified for Barnard and ε Indi B frame counts.

## Limitations

- All centroid, photometry, and linking results are **synthetic-data only** until real FITS is supplied.
- Physical flux calibration is not implemented (ePSF amplitude is in image-native units).
- Gaia production integration requires Akif's `a_veri_isleme` module (H-01).
- Interpolation covariance is not propagated through the resampled variance plane.
- Moving-object full velocity-grid coverage is not claimed; only pair-supported cells are searched.

See `b_astrometri/reports/09-06-sinirliliklar.md` for the full limitations table.

## Contributing

See `CONTRIBUTING.md`. Key rules:

- Raw FITS files and `reports/` output stay outside the repository.
- `graphify-out/` is local derived output — do not commit.
- Tokens and credentials stay in personal files only.
