# Stage 0 test C: header WCS versus Gaia DR3, and annual aberration (real data)

Run 2026-11-14. **Status: COMPLETED for 3 frames (A, B, C).** Scripts in `stage0\scripts\`: c1_tap.py, c2_pick.py, c3_probe.py, c4_hdr.py, c5_fetch.py, c5b_fetch_B.py, c6_gaia.py (ESA Gaia), c9_vizier.py (MAST Gaia; the file name is left over from the failed VizieR attempt), c9b_probe.py, c9c_compare.py, c9d_coverage.py, c7_analyze.py (analysis), c8_report.py (tables), c10_check.py. Data in `stage0\data\C\` (untrusted; tables in `tables.md`, raw numbers in `results_*.json`). TLS verification on; only the stage0 venv with `-I`.

## 1. Frames and provenance

- Field: Barnard's Star region in Ophiuchus (RA 269.452, Dec +4.693; ecliptic latitude about +27 deg, galactic latitude about +14 deg: star-rich). One TAP query (`spherex.artifact` joined to `spherex.plane`, `CONTAINS(POINT('ICRS',ra,dec), p.poly)=1`, 131 s) returned 363 L2 science images (`releasetype=data`, `calibrationlevel=2`, S3 path `dr1/level2/`, product suffix `l2b-v27-2026-2xx`, plane `provenance_version` 7.0.5) between MJD 60902.9 and 61305.6 [VERIFIED by this run: c1_tap.py, c2_pick.py]. I did not look up which public release name ("QR3/DR1") the `dr1` path corresponds to [NOT VERIFIED].
- Three detector-1 frames at three times of year, 1024x1024 windows read from anonymous S3 (IMAGE, VARIANCE, FLAGS; no cutout service) [VERIFIED: c5_fetch.py, c5b_fetch_B.py]:

| frame | obsid | file under s3://nasa-irsa-spherex/dr1/level2/ | UTC | window (x0,y0) |
|---|---|---|---|---|
| A | 2025W35_2A_0233_1 | 2025W35_2A/l2b-v27-2026-231/1/level2_2025W35_2A_0233_1D1_spx_l2b-v27-2026-231.fits | 2025-08-29 17:19 | (113, 0) |
| B | 2025W40_1A_0353_1 | 2025W40_1A/l2b-v27-2026-239/1/level2_2025W40_1A_0353_1D1_spx_l2b-v27-2026-239.fits | 2025-09-30 14:03 | (1016, 1016) |
| C | 2026W11_1A_0444_1 | 2026W11_1A/l2b-v27-2026-232/1/level2_2026W11_1A_0444_1D1_spx_l2b-v27-2026-232.fits | 2026-03-11 03:47 | (0, 1016) |

 Barnard's Star is NaN/masked in the images and excluded by the G>11 cut. In B it lies near the detector edge, so the window is the upper-right block; it still covers the field region.
- Header facts [VERIFIED: c4_hdr.py, hdr_?.txt]: `CTYPE RA---TAN-SIP / DEC--TAN-SIP`, `RADESYS ICRS`, SIP order 3 with AP/BP inverse terms; `FINAST = 0 / good fine-astrometric solution`; `MATCH_NSTARS = 3219` (frame A); `ASTRONETSOLVED = T`; processing history "Estimate Coarse Astrometry SSDC-MS-003 v2.4" and "Estimate Fine Astrometry SSDC-MS-016 v2.5". No keyword mentions aberration, parallax, Gaia or an RMS. The header holds spacecraft position and velocity (`X_SC`, `VX_SC`..., km and km/s, `VXYZ_SC_SYSTEM='GEOCENTER'`; the axes of this frame are not stated).

## 2. Method (all [VERIFIED by this run: c7_analyze.py])

- Mask: FLAGS & 0x3C028E44 (plan fit mask), non-finite, VARIANCE<=0; for centroiding also bits 1 (OVERFLOW) and 7 (DICHROIC). Masked fraction 1.7-2.3 % per window (c10_check.py).
- Background: photutils `Background2D`, 64x64 boxes, 3x3 filter, median estimator, flagged pixels masked, `exclude_percentile=50` (see sensitivity note in section 5). Detection: `DAOStarFinder(fwhm=2.5 px, threshold = 5 x median background RMS)`. Centroid: **5x5 centre of mass** of the positive background-subtracted pixels, iterated up to 3 times; a star is rejected if any pixel of its 5x5 box is masked. A 5x5 COM has a pixel-phase bias of a few hundredths of a pixel with zero mean over random phases; it inflates scatter but should not move the mean much (the sensitivity test in section 5 says it moves it by about 0.02 px).
- Gaia DR3 selection: 11<G<17, RUWE<1.4, 5/6-parameter solution, no other Gaia G<18 source within 20" (3.3 px), no other detected source within 3.5 px. Epoch propagation to MJD-AVG with `SkyCoord.apply_space_motion` (pm; distance 1/parallax, parallax clipped at >=0.05 mas, RV 0); **parallax added by hand** with the first-order formula and astropy's barycentric Earth position; the parallax term is at most 18 mas (0.003 px) and changes the median offset by <0.0001 px. Projection: `all_world2pix(ra, dec, 0, tolerance=1e-8, maxiter=50)`. Match: coarse 8 px histogram (single peak at the origin) then nearest detection within 2 px of the median-shifted prediction; matching without any shift gave the same N, i.e. nothing is displaced by more than 2 px.
- Fits: shift, similarity (shift, rotation, scale) and affine (6 parameters), clipped; held-out check on a 70/30 split (plan D6).
- Aberration prediction: Earth barycentric velocity from `get_body_barycentric_posvel('earth', t)` (t = MJD-AVG as UTC); first-order n' = n + (v - n (n.v))/c for each matched star, projected through the same WCS. A second prediction adds the header spacecraft velocity (7.5 km/s), assumed to be in an inertial equatorial frame parallel to ICRS [NOT VERIFIED: the header does not state the axes]. Stars move toward the apex; so if the WCS were in the unaberrated catalogue frame while the sky is aberrated, measured (centroid minus catalogue-projected) = predicted.

### Gaia sources used (two different services)

- **ESA Gaia archive TAP** (gea.esac.esa.int, `gaiadr3.gaia_source`): used for frame A only. For B only 2 of 4 tiles were obtained; the remaining tile queries returned HTTP 500 or connection resets (WinError 10054) through repeated retries and tile splitting (c6_gaia.py), so B and C could not be finished with it [VERIFIED: g.log, g3.log].
- **CDS VizieR TAP** (tapvizier.cds.unistra.fr) was tried first as the alternative: connection timed out twice; vizier.cfa.harvard.edu/TAPVizieR returned 404; vizier.cds.unistra.fr returned 404 for the TAP path [VERIFIED: c9_vizier.py first version, c9b_probe.py]. It was not used.
- **MAST Gaia DR3 TAP** (https://mast.stsci.edu/vo-tap/api/v0.1/gaiadr3/sync, table `dbo.gaia_source`, a different service run by STScI): **used for frames B and C** [VERIFIED: c9_vizier.py]. Equivalence with ESA tested on frame A (c9c_compare.py, c9d_coverage.py): 55,609 sources in common; ra, dec, parallax, pmra, pmdec, G, RUWE, ref_epoch (2016.0) and the astrometric-solution flag are **identical** (max |difference| = 0) and the same NaN pattern; the sources present in only one table lie outside the analysis window (0 inside the window for both; they come from the different tile footprints). The MAST response carried `QUERY_STATUS=OVERFLOW`; the per-tile counts (15.7-19.7 thousand) match ESA's and the analysis window is complete (previous sentence), so no truncation inside the window, but I cannot say what the MAST cap is [NOT VERIFIED]. Running the whole analysis of frame A with the MAST table reproduced the ESA result (N=602, median dx -0.0296, dy -0.0126 px, both identical to the digits printed) [VERIFIED: results_A_mast.json versus results_A.json].

## 3. Per-frame offsets, raw header WCS (centroid minus Gaia projected) [VERIFIED: c7_analyze.py, c8_report.py]

1 px = 6.15". Offsets are medians over the matched stars.

| frame | Gaia source | selected / in window | detections centroided | **N matched** | median dx px | median dy px | dx, dy arcsec | sky: dRA*cos(dec), dDec arcsec | robust sigma dx, dy px | s.e.m. dx, dy px |
|---|---|---|---|---|---|---|---|---|---|---|
| A | ESA | 6330 / 4776 | 2374 | 602 | -0.0296 | -0.0126 | -0.182, -0.077 | -0.182, +0.083 | 0.082, 0.100 | 0.0042, 0.0051 |
| B | MAST | 6684 / 4905 | 2419 | 622 | -0.0251 | -0.0035 | -0.155, -0.022 | -0.154, +0.013 | 0.086, 0.091 | 0.0043, 0.0046 |
| C | MAST | 6602 / 4882 | 2383 | 592 | -0.0285 | +0.0024 | -0.176, +0.015 | +0.192, +0.012 | 0.083, 0.095 | 0.0043, 0.0049 |

Fits to the offset field (clipped at about 3 sigma; scale and rotation in px/px and rad):

| frame | model | tx px | ty px | scale | rot rad | per-axis RMS px (arcsec) | held-out robust per-axis px |
|---|---|---|---|---|---|---|---|
| A | shift | -0.0315 | -0.0178 | | | 0.134 (0.83) | 0.1350 |
| A | similarity | -0.0314 | -0.0179 | -2.0e-6 | -6.0e-6 | 0.134 (0.83) | 0.1367 |
| A | affine | -0.0312 | -0.0179 | a,b,c,d = -1e-8, +2.5e-5, +1.3e-5, -6.9e-6 | | 0.134 (0.83) | 0.1354 |
| B | shift | -0.0265 | -0.0116 | | | 0.135 (0.83) | 0.1336 |
| B | similarity | -0.0266 | -0.0115 | -4.2e-6 | +4.9e-6 | 0.135 (0.83) | 0.1307 |
| B | affine | -0.0270 | -0.0115 | a,b,c,d = -1.6e-5, -1.1e-5, -1.2e-6, +6.9e-6 | | 0.135 (0.83) | 0.1294 |
| C | shift | -0.0334 | +0.0011 | | | 0.129 (0.79) | 0.1295 |
| C | similarity | -0.0334 | +0.0016 | -4.4e-6 | -1.5e-5 | 0.129 (0.79) | 0.1306 |
| C | affine | -0.0325 | +0.0017 | a,b,c,d = -3.2e-5, +4.9e-6, -2.5e-5, +2.6e-5 | | 0.128 (0.79) | 0.1274 |

Held-out improvement of the affine over the shift model: A 0 %, B 3.2 %, C 1.7 %, all below the 10 % rule of D6, so **a constant shift is the right model in all three frames**. Coefficient errors are about 9e-6 (rough: sigma/(sqrt(N) x 295 px)), so the fitted scale and rotation (up to 3e-5, i.e. 0.03 px across 1024 px) are at most 3 sigma. 3x3 grids of medians (tables.md): every cell is within -0.058 and +0.033 px; the cell error is about 0.013 px, so there is no spatial structure beyond noise (only the x components cluster at -0.03).

Scatter by Gaia G, robust per-axis sigma (px; arcsec): G 11-14: A 0.039 (0.24), B 0.039, C 0.042 (0.26); G 14-15.5: 0.076, 0.075, 0.073; G 15.5-17: 0.167, 0.168, 0.181. The median offset in each magnitude bin is -0.02 to -0.05 px in x with no trend.

## 4. Aberration: prediction versus measurement [VERIFIED: c7_analyze.py]

| frame | Earth speed km/s | angle field-apex deg | predicted shift, Earth only: dRA*, dDec, magnitude arcsec | predicted, Earth + header spacecraft velocity | **measured** dRA*, dDec arcsec (magnitude) |
|---|---|---|---|---|---|
| A (29 Aug 2025) | 29.50 | 144.7 | +7.75, +8.79, 11.72 | +6.53, +3.81, 7.56 | -0.182, +0.083 (0.20) |
| B (30 Sep 2025) | 29.74 | 149.8 | -3.15, +9.80, 10.30 | -4.12, +5.32, 6.73 | -0.154, +0.013 (0.15) |
| C (11 Mar 2026) | 29.98 | 29.5 | -3.54, -9.53, 10.17 | -4.35, -4.49, 6.25 | +0.192, +0.012 (0.19) |

(Check of size: 20.5" x sin(angle) gives 11.7", 10.3", 10.2", equal to the computed magnitudes.)

- The predicted aberration vectors are 6-12" and change in direction between the three dates (A toward NE, B toward NNW, C toward SSW). **The measured offsets are 0.15-0.20" (0.025-0.03 px), 50 to 70 times smaller than the prediction, and they do not rotate with it.** In pixel coordinates the offset is almost the same in all three frames (dx -0.025 to -0.030 px, dy -0.0035 to +0.0024), whereas the sign of its RA component in the sky changes between A/B and C (the field orientation on the sky differs in frame C). A pixel-fixed offset of 0.03 px is what a centroid bias or a pixel-origin convention would produce, not an effect tied to Earth's velocity. Only three dates, so a seasonal sinusoid with 3 points is not fitted, but there is no sign of the predicted rotation.
- Predicted differential aberration across the 1024 px window (affine a,d, px per px, Earth only): A +9.1e-5, +8.6e-5; B +9.1e-5, +9.3e-5; C -7.8e-5, -8.0e-5 (range about 0.09 px). Measured a,d: A -1e-8, -6.9e-6; B -1.6e-5, +6.9e-6; C -3.2e-5, +2.6e-5, with errors of about 9e-6. So the predicted gradient is also absent (differences of about 10-12 sigma in A and B; in C 5 sigma for a and 11 sigma for d), though at 0.09 px across the window it is a marginal effect and depends on my rough error estimate.

### Conclusion (H1 = header WCS is in the Gaia astrometric frame; H2 = stars are displaced as aberration would displace them)

- **The data show H1 and reject H2 as a simple "unaberrated WCS versus aberrated stars" situation:** at all three dates the header WCS reproduces Gaia's catalogue positions of the stars to 0.03 px (0.2") in the mean, not to 7-12".
- **What the data cannot decide:** whether the pipeline removes aberration (or never modelled it) because the WCS was fitted to the stars themselves. If SCAMP fitted the WCS (CRVAL and the linear and SIP terms) to the apparent stars against catalogue positions, the mean aberration and its gradient are absorbed in the fitted parameters, and the residual against Gaia is zero at every date, which is exactly what I see. So these data are equally compatible with "aberration corrected" and with "aberration present in the sky and absorbed by the per-frame fit". For the plan, only the second matters: **projected Gaia positions agree with the header WCS at each epoch, so the plan's row "Aberration: irrelevant to us" is supported for stars**. The cases that would not be absorbed (an object whose own light time/aberration differs from the stars', e.g. WISE 0855 at 2.3 pc with an apparent position not the same as the star frame) were not tested [NOT VERIFIED]. Time of year can in principle be tested better with a frame one year later (the TAP list contains Aug 2026 frames; not used).
- Unresolved: the physical origin of the common -0.03 px x offset (centroid bias versus WCS convention); the 0.05 px sensitivity to the background choice (section 5); the assumed frame of the header spacecraft velocity.

## 5. Accuracy against the stated RMS < 0.3" (0.05 px) [VERIFIED: c7_analyze.py]

- The mean offset (0.025-0.03 px, about 0.17" per axis) is inside 0.05 px (0.3") in all three frames. Per-star scatter is 0.039-0.042 px (0.24-0.26") for G 11-14, 0.075 px (0.46") for G 14-15.5 and 0.17-0.18 px for G 15.5-17 (that bin is dominated by centroid noise and may include confused sources). So the claim "RMS < 0.3"" is **consistent** with the data for bright stars (G<14) and for the mean offset, and **not demonstrable** for fainter stars with this 5x5 centre-of-mass centroider, which cannot separate WCS error from centroid noise.
- Sensitivity note (honest): an earlier run of frame A with the default Background2D setting (exclude_percentile=10, 10 % masked-box rejection) gave N=450, median offset (-0.011, -0.007) px and scatter 0.044, 0.064 px (bright bin 0.031 px); the setting had to be relaxed to 50 for frames B and C because Background2D refused to run (all boxes had under 90 % good pixels). With the relaxed setting A moved to (-0.030, -0.013) px with N=602. The mean offset thus depends on the background and star-selection settings at the level of 0.02 px, which is similar to the offset itself. All three frames in sections 3-4 use the same final setting; the earlier A run is listed only for this sensitivity.
- The header has no RMS keyword (checked A, B, C), so the stated 0.3" figure comes from the document only.

## 6. Relation to s0_D.md (1-3 px offsets between SkyBoT-predicted and observed asteroid positions)

- s0_D used observer 500 (geocentre). The header WCS agrees with Gaia to 0.03 px (mean) in three frames with no spatial structure above noise in the 1.75 deg windows, so a WCS error is **unlikely** to cause 1-3 px offsets near the detector-1 field centre at these epochs [VERIFIED here for detector 1, 3 frames, 1024 px windows].
- The header gives the spacecraft geocentric position: frame A has |R| = sqrt(2390^2 + 6301^2 + 2012^2) = 7170 km (arithmetic from `X_SC, Y_SC, Z_SC`). The topocentric parallax of an asteroid at distance D is 7170 km / D: 6.7" = 1.1 px at 1.5 AU, 3.4 px at 0.5 AU. That alone can explain offsets of the observed size, depending on geometry [arithmetic only; not checked against the D frames, NOT VERIFIED]. Aberration cannot: it displaces stars and asteroids alike (with an astrometric ephemeris), and its mean is absorbed by the WCS.

## 7. Not completed / open

- ESA Gaia tiles for frames B and C: NOT COMPLETED (server HTTP 500 and resets); replaced by the MAST service for B and C, validated against ESA on frame A.
- A one-year-later control frame (same season as A) and detectors other than 1: not done.
- Absolute pointing accuracy against an independent system (e.g. star tracker) and an explicit test whether the pipeline itself applies aberration: not possible with these data.
