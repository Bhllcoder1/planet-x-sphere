# Stage 0 test D (real data): do SPHEREx flags hide or mimic real movers?

Run 2026-11-14. Scripts in `stage0\scripts\`: d0_pdftext.py, d1_query.py, d2_flagstats.py, d2b_show.py, d3_skybot.py, d3b_stamps.py, d4_movers.py. Data in `stage0\data\D\` (untrusted). TLS verification on. pymupdf was pip-installed into stage0\venv only (for PDF text).
Frames used: **10 of 10 planned** for flag statistics (5 near the Galactic Centre "gc", 5 at RA 180 Dec 0 "sparse", on the ecliptic at high galactic latitude). SkyBoT mover check: **4 frames** (3 sparse, 1 gc). Frames were read whole (FLAGS and IMAGE) from anonymous S3; no cutouts were used.

## 1. What the Explanatory Supplement says (PDF page = printed page)

- OUTLIER and STREAK come from the per-image "Outlier Pixel Detection" module. [VERIFIED by this run: expsupp.txt / PDF p.41] "detects and flags transient events in each spectral image that may have bypassed onboard flagging procedures. It operates by applying a sigma-clipping algorithm to a median-filtered image with known sources masked." "For each exposure, the module generates a flag array ..." Inputs: spectral image, SOURCE mask, bad pixel mask, VARIANCE. Isolated outliers are flagged OUTLIER immediately; "streak seeds" (a slightly lower threshold) are grouped, fitted to a line (ZTF method, Laher 2014), elongated fragments are kept, co-linear fragments are joined, and all pixels of the track get STREAK.
- **Single exposure, not cross-exposure.** The text describes only the one image and its masks. A comparison between exposures is [NOT FOUND IN DOCUMENT]. [VERIFIED: p.41]
- **Can a mover be flagged?** The section never mentions moving objects. The only Solar System handling is that the SOURCE mini-catalog is built "from the Reference Catalog and the known Solar System object catalog" (p.38), so known objects *may* be SOURCE-masked and thus excluded from the outlier module. Which objects, magnitude limit and ephemeris accuracy used: [NOT FOUND IN DOCUMENT]. Anything not in that catalog is in principle open to OUTLIER (compact) or STREAK (trail). Empirical result in section 3.
- TRANSIENT (bit 0) is decided **onboard within one exposure's up-the-ramp read**: "Determined onboard (Level 0)"; "Transients occurring during the first ten seconds of the observation may not be flagged"; it also fires for bloom spill-over (Table 16, p.33). "Transient detection truncates the SUR algorithm and returns the slope corresponding only to frames prior to the transient" (p.24). Threshold about 100 e- (p.15). Whether a source moving *within* the ramp can trigger it is [NOT FOUND IN DOCUMENT]. Table 16 only says bright satellite tracks "are flagged on board as transients" (p.18).
- BLOOM, SNOWBALL, HALO, SATELLITE_HALO come from Level-1 flag layer + slope image + TELAPSE of the **same exposure** (Sect. 3.2.1, pp.24-27): BLOOM = transient flags attributed to source blooming; SNOWBALL = round OVERFLOW/TRANSIENT cores; HALO = pixels around cosmic rays/snowballs (radius from fluence, p.27); a core whose extent exceeds the snowball halo radius is treated as "most likely a saturating satellite streak" and given an extended SATELLITE_HALO (p.27). A bright real source with early-transient + overflow pixels is therefore a candidate for BLOOM/SNOWBALL/HALO; this is not said to be tested against moving sources [NOT FOUND IN DOCUMENT].
- Fainter satellite streaks get STREAK; "Satellite streaks near the noise level may not be flagged" (p.18). The L2 DQA fails an image if OUTLIER count is not within a factor 2 of the other flagged pixels (p.42).

## 2. Flag statistics (percent of 2040x2040 pixels; 10 whole frames) [VERIFIED by this run: d2_flagstats.py -> flagstats.json, shown by d2b_show.py]

gc1..gc5 = detectors D1..D5 of 2026W12/W13 (MJD 61117-61123, field RA266.4 Dec-29). sp6,sp1,sp2,sp3,sp4 = D6,D1,D2,D3,D4 of 2025W51/W52 (MJD 61030-61035, field RA180 Dec0). Field and processing epoch are confounded (see limits).

| bit | gc1 | gc2 | gc3 | gc4 | gc5 | sp6 | sp1 | sp2 | sp3 | sp4 |
|---|---|---|---|---|---|---|---|---|---|---|
| TRANSIENT | 0.82 | 1.05 | 2.46 | 3.33 | 0.98 | 0.52 | 0.55 | 0.35 | 0.47 | 0.51 |
| OVERFLOW | 0.15 | 1.00 | 2.76 | 5.68 | 0.50 | 0.05 | 0.01 | 0.01 | 0.01 | 0.06 |
| OUTLIER | 0.00007 | 0 | 0 | 0 | 0 | 1.71 | 1.77 | 1.96 | 2.11 | 1.94 |
| CROSSTALK | 20.76 | 17.13 | 13.77 | 0 | 0 | 0 | 0.056 | 0.0002 | 0 | 0 |
| SOURCE | 99.998 | 100 | 100 | 100 | 100 | 26.3 | 27.0 | 30.5 | 30.2 | 39.3 |
| GHOST | 0 | 0 | 0 | 0.209 | 0 | 0 | 0 | 0 | 0 | 0 |
| GHOST_FPA / GHOST_EXT | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| STREAK | 0 | 0 | 0 | 0 | 0 | 0.150 | 0.197 | 0.075 | 0.094 | 0.134 |
| BLOOM | 0.30 | 1.12 | 3.12 | 4.68 | 0.40 | 0.005 | 0.024 | 0.026 | 0.023 | 0.022 |
| SNOWBALL | 0.003 | 0.005 | 0.008 | 0.046 | 0.016 | 0.002 | 0 | 0.0005 | 0.0005 | 0.002 |
| HALO | 1.59 | 0.51 | 0.53 | 0.82 | 1.44 | 1.13 | 1.49 | 0.89 | 1.22 | 1.05 |
| SATELLITE_HALO | 0 | 0 | 0 | 0.0003 | 0 | 0 | 0 | 0 | 0 | 0 |
| NONLINEAR | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| PERSIST | 10.88 | 0.39 | 66.55 | 0.29 | 9.26 | 0.03 | 0.19 | 0.13 | 0.12 | 0.04 |
| HOT | 0.0002 | 0.0003 | 0.0003 | 0 | 0.0001 | 0.0001 | 0 | 0 | 0 | 0 |
| COLD | 0.015 | 0.003 | 0.004 | 0.024 | 0.021 | 0.060 | 0.036 | 0.023 | 0.037 | 0.045 |
| NONFUNC | 0.26 | 0.21 | 0.29 | 0.54 | 0.50 | 0.44 | 0.26 | 0.21 | 0.29 | 0.54 |
| DICHROIC | 0 | 0 | 2.64 | 2.70 | 0 | 0 | 0 | 0 | 2.64 | 2.70 |
| MISSING_DATA | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| SUR_ERROR | 0.59 | 0.62 | 1.33 | 2.00 | 0.79 | 0.43 | 0.34 | 0.24 | 0.32 | 0.42 |
| **Fit mask 0x3C028E44** | 12.81 | 2.22 | 67.76 | 6.25 | 11.42 | 1.59 | 1.97 | 1.26 | 1.66 | 1.64 |
| **Background mask 0x3C2A8E47** | 99.998 | 100 | 100 | 100 | 100 | 29.1 | 30.2 | 33.2 | 33.4 | 42.2 |
| **Extra mask alone** (bits 0,20,22-25) | 21.36 | 17.88 | 15.83 | 3.53 | 0.98 | 0.67 | 0.75 | 0.40 | 0.55 | 0.63 |
| Fit + extra | 26.70 | 18.80 | 70.56 | 6.43 | 11.42 | 1.74 | 2.12 | 1.29 | 1.72 | 1.74 |

Connected components (8-connectivity): STREAK = 0,0,0,0,0 in the gc frames; 4,16,5,3,2 in sp6,sp1,sp2,sp3,sp4. SATELLITE_HALO = 1 component in gc4 (size 26e-6 of frame), 0 elsewhere. OUTLIER components in sparse frames: 62,863 to 73,630 per frame, largest 25-40 pixels (so some are not single pixels). SNOWBALL components: 10, 14, 31, 270, 53 (gc) and 5, 0, 2, 2, 4 (sparse).

Observations (all [VERIFIED by this run: d2_flagstats.py]):
- GHOST, GHOST_FPA, GHOST_EXT, SATELLITE_HALO, HOT, NONLINEAR, MISSING_DATA are essentially absent (0 to 0.21 %) in these 10 frames. STREAK is 0.075-0.2 % of pixels but only in the five 2025W51/52 frames.
- SOURCE covers 100 % of every gc frame (so it cannot mean "star here" in a crowded field) and 26-39 % of the sparse frames. Any mask containing SOURCE (the background mask) removes the whole gc frame.
- The "extra" mask costs 0.4-0.75 % in the sparse frames, but 15.8-21.4 % in the gc frames D1-D3, dominated by CROSSTALK (13.8-20.8 %). PERSIST is 66.5 % in gc3 (that frame is unusable under the fit mask).
- OUTLIER is 1.7-2.1 % in all five 2025W51/52 frames and about 0 in all five 2026W12/13 frames. I cannot say whether this is field, epoch or reprocessing version (the file names show `l2b-v27-2026-211` vs `-235/-236`; provenance_version is 7.0.5 for all).

## 3. Real-mover check (SkyBoT) [VERIFIED by this run: d3_skybot.py, d3b_stamps.py, d4_movers.py]

- Query form used (documented at https://ssp.imcce.fr/webservices/skybot/api/conesearch ): `conesearch.php?-ep=<JD>&-ra=..&-dec=..&-rs=10800&-mime=json&-output=all&-observer=500&-filter=0&-objFilter=100&-refsys=EQJ2000&-from=...`. `-objFilter=110` returned a server error (calceph) for this epoch; `100` (asteroids only) works. JSON keys: `RA (hms)`, `DEC (dms)` (strings), `VMag (mag)`, `Err (arcsec)`. Epoch = MJD-AVG + 2400000.5, observer 500 (geocentre). One request per frame, sequential (4 total plus 4 diagnostic requests).
- The ephemeris position errors returned were 0.004-0.02 arcsec for every V<18 object (so the "hundreds of arcsec" caveat did not apply to these numbered main-belt asteroids; it can for poorly observed objects). Filter was set to 0 (off) and error read from the output.
- Cone radius 3 deg (frame is about 3.5 deg wide). Objects inside the footprint: 3,585 / 3,415 / 3,326 / 1,797; those with V<18: 7 / 10 / 8 / 4.
- Method: IMAGE background-subtracted (coarse median), noise by MAD, brightest pixel within +-4 px of the predicted position; "detected" = peak > 8 sigma and within 3 px of the prediction. Flags then read in the 3x3 core of that peak.
- **Detected movers: 17 of 25 in the three sparse frames; 0 of 4 in the gc frame** (crowded, noise sigma 0.36 vs 0.025; peaks near predictions were stars; not a conclusion either way). Brightest examples: Massalia V=10.9 peak 188 (saturating, OVERFLOW pixels in the core), Cybele V=13 peak 19-29, Columbia V=15.5 peak 45, Russia V=15 peak 3-5. Undetected ones had the best peak 3-5.7 px away or were faint; I did not follow them up. Detected peaks were 0.1-2.6 px from the prediction; the cause of the 1-3 px offsets (LEO versus geocentre parallax up to a few arcsec, timing, WCS) was not investigated [NOT VERIFIED].
- Motion during the exposure: the JSON gives up to 65 arcsec/h; over the 118.19 s TELAPSE that is below 2.2 arcsec = 0.36 px, so asteroids do not trail within an exposure (arithmetic from the data; fast NEOs untested).

**Flags in the 3x3 core of the 17 detected movers** (d4_movers.py):
| core flag content | count of 17 |
|---|---|
| OUTLIER present (2-9 of 9 core pixels) | 11 |
| SOURCE only (all 5-9 core pixels), no OUTLIER | 6 (Cybele x2, Columbia, Ots, Plevitskaya, Kodomonomori) |
| OUTLIER in a core without SOURCE | 11 of the 11 non-SOURCE-only cores |
| TRANSIENT, STREAK, HALO, GHOST, CROSSTALK, BLOOM, SNOWBALL in the 3x3 core | 0 |
| Core pixels removed by the **fit mask** 0x3C028E44 | 0 of 17 |
| Core pixels removed by the **extra mask** (bits 0,20,22-25) | 0 of 17 |
| Core pixels removed by the **background mask** 0x3C2A8E47 | 17 of 17 (via OUTLIER or SOURCE) |

In the +-3 px window (d3_skybot.py) HALO and TRANSIENT did appear around the brightest ones: Cybele (sp3) TRANSIENT 1 px, HALO 4 px; Columbia (sp2) TRANSIENT 1, HALO 4; Massalia (sp1) HALO 1.

**Static stars of similar brightness** (peak 0.5-2x of the movers, more than 10 px from any SkyBoT object; 8,622 / 34,252 / 20,620 stars): OUTLIER in the 3x3 core 3.7 %, 2.6 %, 2.6 %; SOURCE 91-96 %; TRANSIENT 8.7-16.7 %; HALO 5.3-9.4 %; STREAK 0.2-0.3 %; fit-mask hits in the core 12-21 %; extra-mask hits 9-17 %. So in these frames OUTLIER on a compact bright core is about 20x more common for known movers (11/17 = 65 %) than for static stars (about 3 %). Caveat: the static pool includes stars, galaxies and any unknown movers; the mover sample is small.

Reading: in the 2025W51/52 frames the pipeline does NOT hide the movers (core pixels survive the fit mask, 0/17), but it **tags many of them OUTLIER** (and 6 of 17 are inside the SOURCE mask, consistent with, but not proof of, the known Solar System catalog entering the source mask, p.38; Cybele, Columbia and Kodomonomori are isolated so a coincident star is unlikely, Ots and Plevitskaya were not checked). Not tested: whether streaks (4-16 per frame) cross real mover positions; whether the 2026 frames (almost no OUTLIER) tag movers at all (no gc mover detected).

## 4. Recommendation (from these numbers only)

**Centroiding / photometry of static sources (default):** fit mask 0x3C028E44 plus OVERFLOW (1), DICHROIC (7), STREAK (25), SATELLITE_HALO (already in fit mask), GHOST (22-24). Cost beyond the fit mask: 0.1-0.5 % of pixels in sparse frames, 0.2 % in one gc frame (GHOST). Do **not** mask CROSSTALK (20) or TRANSIENT (0) frame-wide by default: CROSSTALK removes 14-21 % of three gc frames and TRANSIENT hits 9-17 % of star cores; instead keep them as per-measurement caution flags (a window flag within 2.5-3 px), as the plan does. Do not use SOURCE in a mask for background in crowded fields (100 % of the gc frames).
**Moving-object search (default):** use the fit mask plus STREAK, GHOST, CROSSTALK as vetoes with a reason code, but do **not** mask OUTLIER (19) or SOURCE (21): 11 of 11 non-SOURCE-masked mover cores carried OUTLIER and 6 of 17 sat in SOURCE. Treat OUTLIER-flagged compact clusters as extra candidates (promote, not reject), and report TRANSIENT/HALO neighbours of bright candidates as caution only.

**What these data cannot decide:** (1) whether the OUTLIER difference (1.7-2.1 % vs about 0) is field, date, or pipeline version; (2) whether STREAK/GHOST would remove real movers (not cross-matched) or how fast NEOs / trailed objects behave (only main-belt asteroids with V up to 18); (3) any crowded-field mover (0 detections); (4) false-track rates from OUTLIER/STREAK in a linking search; (5) the cause of the 1-3 px offset between predicted and observed positions; (6) D13's injected-star core-loss and centroid-bias criteria (no injection was done here); (7) the quality of the SOURCE mask's Solar System entries beyond the six cores seen; (8) only 10 frames and 5+5 field/epoch split, so percentages are per-frame, not survey-wide.
