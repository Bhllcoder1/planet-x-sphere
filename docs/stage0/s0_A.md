# Stage 0 test A: coverage, headers, roll (real data)

Scripts: stage0\scripts\a1_resolve.py, a1b_epsindB.py (positions), a2_tap.py (TAP), a4_headers.py (S3 headers), a5_report.py (this file).
Raw: stage0\data\A\tap_*.csv, frames_*.json, headers_*.json.

Method notes: SIMBAD was unreachable (cds.unistra.fr 404 page) so positions come from Sesame (SkyCoord.from_name, other server) + Gaia DR3 (epoch 2016, pm) [VERIFIED by this run: a1_resolve.py, a1b_epsindB.py]. WISE 0855 position was taken from the task (pm -8118,+680 mas/yr assumed from literature, NOT VERIFIED here). Query point = position propagated to 2026.0. IRSA TAP rejects INTERSECTS(CIRCLE,poly) and OR of CONTAINS (BAD_REQUEST), so ONE CONTAINS(POINT,poly) per target is used, not a 0.1 deg radius [VERIFIED: a2_tap.py log]. Footprints are ~3.5 deg wide, so the point-vs-0.1deg difference only matters at frame edges (not tested). Detector = directory digit in the uri; no detector column exists in spherex.plane [VERIFIED: a0_schema.py]. MJD = mid of time_bounds_lower/upper. Pass = MJD cluster, gap > 30 d.

## Barnard
TAP rows 358, science frames 358 [VERIFIED by this run: a2_tap.py]

Frames per release/collection x detector (provenance_version in brackets):

| collection | procver | D1 | D2 | D3 | D4 | D5 | D6 | total |
|---|---|---|---|---|---|---|---|---|
| dr1 | l2b-v27-2026-228 | 0 | 0 | 8 | 0 | 0 | 7 | 15 |
| dr1 | l2b-v27-2026-229 | 0 | 5 | 4 | 0 | 5 | 4 | 18 |
| dr1 | l2b-v27-2026-230 | 5 | 7 | 6 | 5 | 8 | 6 | 37 |
| dr1 | l2b-v27-2026-231 | 12 | 5 | 0 | 11 | 5 | 0 | 33 |
| dr1 | l2b-v27-2026-232 | 19 | 0 | 0 | 19 | 0 | 0 | 38 |
| dr1 | l2b-v27-2026-234 | 1 | 10 | 0 | 1 | 10 | 0 | 22 |
| dr1 | l2b-v27-2026-235 | 0 | 8 | 14 | 0 | 9 | 14 | 45 |
| dr1 | l2b-v27-2026-236 | 0 | 0 | 5 | 0 | 0 | 5 | 10 |
| dr1 | l2b-v27-2026-239 | 5 | 0 | 0 | 5 | 0 | 0 | 10 |
| dr1 | l2b-v27-2026-240 | 0 | 0 | 1 | 0 | 0 | 1 | 2 |
| dr1 | l2b-v27-2026-245 | 0 | 0 | 4 | 0 | 0 | 4 | 8 |
| dr1 | l2b_retry-v27-2026-230 | 0 | 1 | 0 | 0 | 0 | 0 | 1 |
| qr3 | l2b-v27-2026-241 | 0 | 0 | 1 | 0 | 0 | 1 | 2 |
| qr3 | l2b-v27-2026-243 | 13 | 23 | 16 | 13 | 22 | 16 | 103 |
| qr3 | l2b-v27-2026-246 | 4 | 1 | 0 | 4 | 1 | 0 | 10 |
| qr3 | l2b-v27-2026-252 | 1 | 0 | 0 | 1 | 0 | 0 | 2 |
| qr3 | l2b-v27-2026-268 | 0 | 1 | 0 | 0 | 1 | 0 | 2 |

provenance_version (pipeline): {'7.0.5': 358}

Passes (gap > 30 d):

| pass | MJD min | MJD max | n | D1 | D2 | D3 | D4 | D5 | D6 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 60902.87 | 60949.27 | 118 | 24 | 18 | 18 | 23 | 18 | 17 |
| 1 | 61110.09 | 61165.08 | 121 | 18 | 18 | 24 | 18 | 19 | 24 |
| 2 | 61268.63 | 61305.63 | 119 | 18 | 25 | 17 | 18 | 24 | 17 |

Epochs (passes): **3**

### Headers (20 read ok, 0 failed)
- CTYPE1 values: {'RA---TAN-SIP': 20}; CTYPE2: {'DEC--TAN-SIP': 20}
- '-SIP' in IMAGE CTYPE: 20/20; A_ORDER: {3: 20}; B_ORDER: {3: 20}; AP_ORDER: {3: 20}
- FINAST: {0: 20} (IMAGE hdr / else primary); RADESYS {'ICRS': 20}; EQUINOX {None: 20}
- XPOSURE: min 113.5826, max 113.5826; MJD-AVG present in IMAGE: 20, in primary: 0
- PA/survey-like keyword names in IMAGE: ['L2 N_GHOST_FPA', 'NON_SURVEY', 'SPS_ELAT', 'SPS_ELON', 'SPS_EPA', 'SPS_FLAGS', 'SPS_TARGET']; SPS_EPA values by pass: {0: {'180.0': 8}, 1: {'0.0': 6}, 2: {'180.0': 6}}
- NOTE: keyword SPS_PA_ECL does NOT exist in these headers if absent from the list above; the actual name is SPS_EPA.
- PA/survey-like keywords, primary (first 3 distinct): [('{}', 20)]
- HDUs: ['PRIMARY', 'IMAGE', 'FLAGS', 'VARIANCE', 'ZODI', 'EPSF', 'WCS-WAVE']; PC/CD keys: ['PCOUNT', 'PC1_1', 'PC1_2', 'PC2_1', 'PC2_2', 'CDELT1', 'CDELT2', 'CDELT1A']; SIP keys: ['A_ORDER', 'A_0_0', 'A_0_1', 'A_0_2', 'A_0_3', 'A_1_0', 'A_1_1', 'A_1_2', 'A_2_0', 'A_2_1']

Roll = position angle (deg E of N) of the image +y axis from WCS (astropy all_pix2world incl. SIP, 50 px step at centre):

| pass | det | n | pa_y min | pa_y max | spread | std |
|---|---|---|---|---|---|---|
| 0 | D1 | 2 | 179.908 | 179.922 | 0.014 | 0.007 |
| 0 | D2 | 2 | 181.133 | 181.133 | 0.000 | 0.000 |
| 0 | D3 | 1 | 182.996 | 182.996 | 0.000 | 0.000 |
| 0 | D4 | 1 | 180.017 | 180.017 | 0.000 | 0.000 |
| 0 | D5 | 1 | 181.410 | 181.410 | 0.000 | 0.000 |
| 0 | D6 | 1 | 183.101 | 183.101 | 0.000 | 0.000 |
| 1 | D1 | 1 | 4.122 | 4.122 | 0.000 | 0.000 |
| 1 | D2 | 1 | 1.126 | 1.126 | 0.000 | 0.000 |
| 1 | D3 | 1 | 358.906 | 358.906 | 0.000 | 0.000 |
| 1 | D4 | 1 | 4.233 | 4.233 | 0.000 | 0.000 |
| 1 | D5 | 1 | 1.404 | 1.404 | 0.000 | 0.000 |
| 1 | D6 | 1 | 359.012 | 359.012 | 0.000 | 0.000 |
| 2 | D1 | 1 | 179.841 | 179.841 | 0.000 | 0.000 |
| 2 | D2 | 1 | 181.749 | 181.749 | 0.000 | 0.000 |
| 2 | D3 | 1 | 182.425 | 182.425 | 0.000 | 0.000 |
| 2 | D4 | 1 | 179.949 | 179.949 | 0.000 | 0.000 |
| 2 | D5 | 1 | 182.024 | 182.024 | 0.000 | 0.000 |
| 2 | D6 | 1 | 182.531 | 182.531 | 0.000 | 0.000 |

Max within-(pass,detector) spread: **0.014 deg**
- pass 0 (all detectors) mean pa_y 181.202, spread 3.193, std 1.204, n=8
- pass 1 (all detectors) mean pa_y 1.467, spread 5.327, std 2.137, n=6
- pass 2 (all detectors) mean pa_y 181.420, spread 2.690, std 1.109, n=6
- pass 0 vs 1: mean difference -179.735 deg (|diff| - 180 = -0.265)
- pass 0 vs 2: mean difference 0.217 deg (|diff| - 180 = -179.783)
- pass 1 vs 2: mean difference 179.953 deg (|diff| - 180 = -0.047)
- per collection, pa_y folded mod 180 (removes the PA flip): dr1: min 0.02 max 179.92 (n=14), qr3: min 1.75 max 179.95 (n=6)

Within-pass test (extra reads, one detector D2, up to 6 frames/pass spread in MJD; n=18):

| pass | n | MJD span (d) | pa_y min | pa_y max | spread | std | SPS_EPA | collections |
|---|---|---|---|---|---|---|---|---|
| 0 | 6 | 8.7 | 180.413 | 181.133 | 0.720 | 0.268 | ['180.0'] | ['dr1'] |
| 1 | 6 | 7.2 | 0.408 | 1.127 | 0.719 | 0.338 | ['0.0'] | ['dr1'] |
| 2 | 6 | 34.8 | 180.327 | 181.749 | 1.421 | 0.487 | ['180.0'] | ['qr3'] |
- (same detector) pass 0 vs 1: 179.875 deg; deviation from exactly 180: 0.125 deg
- (same detector) pass 0 vs 2: 0.148 deg; deviation from exactly 180: 179.852 deg
- (same detector) pass 1 vs 2: -179.728 deg; deviation from exactly 180: 0.272 deg

Per-detector pass-to-pass comparison (mean pa_y per cell; n = header-read frames in the cell; 35 distinct frames):

| det | pass A (n, mean) | pass B (n, mean) | SPS_EPA A/B | diff B-A | diff mod 360 minus 180 (opposite) / diff (same orientation) |
|---|---|---|---|---|---|
| D1 | 0 (n=2, 179.915) | 1 (n=1, 4.122) | ['180.0']/['0.0'] | -175.793 | opposite: -4.207 |
| D1 | 0 (n=2, 179.915) | 2 (n=1, 179.841) | ['180.0']/['180.0'] | -0.074 | same: -0.074 |
| D1 | 1 (n=1, 4.122) | 2 (n=1, 179.841) | ['0.0']/['180.0'] | 175.719 | opposite: -4.281 |
| D2 | 0 (n=7, 181.030) | 1 (n=6, 0.887) | ['180.0']/['0.0'] | 179.858 | opposite: -0.142 |
| D2 | 0 (n=7, 181.030) | 2 (n=6, 181.160) | ['180.0']/['180.0'] | 0.130 | same: +0.130 |
| D2 | 1 (n=6, 0.887) | 2 (n=6, 181.160) | ['0.0']/['180.0'] | -179.728 | opposite: -0.272 |
| D3 | 0 (n=1, 182.996) | 1 (n=1, 358.906) | ['180.0']/['0.0'] | 175.910 | opposite: -4.090 |
| D3 | 0 (n=1, 182.996) | 2 (n=1, 182.425) | ['180.0']/['180.0'] | -0.571 | same: -0.571 |
| D3 | 1 (n=1, 358.906) | 2 (n=1, 182.425) | ['0.0']/['180.0'] | -176.481 | opposite: -3.519 |
| D4 | 0 (n=1, 180.017) | 1 (n=1, 4.233) | ['180.0']/['0.0'] | -175.785 | opposite: -4.215 |
| D4 | 0 (n=1, 180.017) | 2 (n=1, 179.949) | ['180.0']/['180.0'] | -0.069 | same: -0.069 |
| D4 | 1 (n=1, 4.233) | 2 (n=1, 179.949) | ['0.0']/['180.0'] | 175.716 | opposite: -4.284 |
| D5 | 0 (n=1, 181.410) | 1 (n=1, 1.404) | ['180.0']/['0.0'] | 179.994 | opposite: -0.006 |
| D5 | 0 (n=1, 181.410) | 2 (n=1, 182.024) | ['180.0']/['180.0'] | 0.614 | same: +0.614 |
| D5 | 1 (n=1, 1.404) | 2 (n=1, 182.024) | ['0.0']/['180.0'] | -179.380 | opposite: -0.620 |
| D6 | 0 (n=1, 183.101) | 1 (n=1, 359.012) | ['180.0']/['0.0'] | 175.911 | opposite: -4.089 |
| D6 | 0 (n=1, 183.101) | 2 (n=1, 182.531) | ['180.0']/['180.0'] | -0.570 | same: -0.570 |
| D6 | 1 (n=1, 359.012) | 2 (n=1, 182.531) | ['0.0']/['180.0'] | -176.481 | opposite: -3.519 |

Pass duration (days, MJD-mid min to max of ALL TAP frames): pass 0: 46.4 d (60902.9-60949.3), pass 1: 55.0 d (61110.1-61165.1), pass 2: 37.0 d (61268.6-61305.6)

## EpsInd_A
TAP rows 460, science frames 460 [VERIFIED by this run: a2_tap.py]

Frames per release/collection x detector (provenance_version in brackets):

| collection | procver | D1 | D2 | D3 | D4 | D5 | D6 | total |
|---|---|---|---|---|---|---|---|---|
| dr1 | l2b-v27-2026-196 | 4 | 16 | 15 | 4 | 15 | 15 | 69 |
| dr1 | l2b-v27-2026-197 | 0 | 3 | 9 | 0 | 3 | 8 | 23 |
| dr1 | l2b-v27-2026-199 | 0 | 0 | 1 | 0 | 0 | 1 | 2 |
| dr1 | l2b-v27-2026-201 | 0 | 13 | 3 | 0 | 12 | 3 | 31 |
| dr1 | l2b-v27-2026-206 | 4 | 0 | 0 | 4 | 0 | 0 | 8 |
| dr1 | l2b-v27-2026-239 | 0 | 8 | 18 | 0 | 7 | 17 | 50 |
| dr1 | l2b-v27-2026-241 | 11 | 7 | 1 | 11 | 7 | 1 | 38 |
| dr1 | l2b-v27-2026-242 | 23 | 2 | 0 | 22 | 2 | 0 | 49 |
| dr1 | l2b-v27-2026-243 | 4 | 8 | 0 | 3 | 5 | 0 | 20 |
| dr1 | l2b-v27-2026-244 | 3 | 1 | 11 | 3 | 1 | 10 | 29 |
| dr1 | l2b-v27-2026-245 | 0 | 2 | 1 | 0 | 2 | 1 | 6 |
| dr1 | l2b-v27-2026-246 | 0 | 0 | 1 | 0 | 0 | 1 | 2 |
| dr1 | l2b-v27-2026-247 | 0 | 4 | 3 | 0 | 4 | 3 | 14 |
| qr3 | l2b-v27-2026-268 | 0 | 0 | 10 | 0 | 0 | 9 | 19 |
| qr3 | l2b-v27-2026-271 | 0 | 0 | 24 | 0 | 0 | 23 | 47 |
| qr3 | l2b-v27-2026-276 | 0 | 17 | 2 | 0 | 16 | 2 | 37 |
| qr3 | l2b-v27-2026-285 | 0 | 7 | 0 | 0 | 7 | 0 | 14 |
| qr3 | l2b_retry-v27-2026-269 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |
| qr3 | l2b_retry-v27-2026-276 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |

provenance_version (pipeline): {'7.0.5': 460}

Passes (gap > 30 d):

| pass | MJD min | MJD max | n | D1 | D2 | D3 | D4 | D5 | D6 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 60789.86 | 60836.19 | 125 | 4 | 32 | 28 | 4 | 30 | 27 |
| 1 | 60946.96 | 60991.86 | 141 | 25 | 25 | 23 | 24 | 22 | 22 |
| 2 | 61148.85 | 61164.12 | 75 | 20 | 7 | 12 | 19 | 6 | 11 |
| 3 | 61305.23 | 61315.48 | 119 | 0 | 24 | 36 | 0 | 24 | 35 |

Epochs (passes): **4**

### Headers (20 read ok, 0 failed)
- CTYPE1 values: {'RA---TAN-SIP': 20}; CTYPE2: {'DEC--TAN-SIP': 20}
- '-SIP' in IMAGE CTYPE: 20/20; A_ORDER: {3: 20}; B_ORDER: {3: 20}; AP_ORDER: {3: 20}
- FINAST: {0: 20} (IMAGE hdr / else primary); RADESYS {'ICRS': 20}; EQUINOX {None: 20}
- XPOSURE: min 113.5826, max 113.5826; MJD-AVG present in IMAGE: 20, in primary: 0
- PA/survey-like keyword names in IMAGE: ['L2 N_GHOST_FPA', 'NON_SURVEY', 'SPS_ELAT', 'SPS_ELON', 'SPS_EPA', 'SPS_FLAGS', 'SPS_TARGET']; SPS_EPA values by pass: {0: {'0.0': 6}, 1: {'180.0': 6}, 2: {'0.0': 6}, 3: {'180.0': 2}}
- NOTE: keyword SPS_PA_ECL does NOT exist in these headers if absent from the list above; the actual name is SPS_EPA.
- PA/survey-like keywords, primary (first 3 distinct): [('{}', 20)]
- HDUs: ['PRIMARY', 'IMAGE', 'FLAGS', 'VARIANCE', 'ZODI', 'EPSF', 'WCS-WAVE']; PC/CD keys: ['PCOUNT', 'PC1_1', 'PC1_2', 'PC2_1', 'PC2_2', 'CDELT1', 'CDELT2', 'CDELT1A']; SIP keys: ['A_ORDER', 'A_0_0', 'A_0_1', 'A_0_2', 'A_0_3', 'A_1_0', 'A_1_1', 'A_1_2', 'A_2_0', 'A_2_1']

Roll = position angle (deg E of N) of the image +y axis from WCS (astropy all_pix2world incl. SIP, 50 px step at centre):

| pass | det | n | pa_y min | pa_y max | spread | std |
|---|---|---|---|---|---|---|
| 0 | D1 | 1 | 328.560 | 328.560 | 0.000 | 0.000 |
| 0 | D2 | 1 | 334.661 | 334.661 | 0.000 | 0.000 |
| 0 | D3 | 1 | 335.338 | 335.338 | 0.000 | 0.000 |
| 0 | D4 | 1 | 328.677 | 328.677 | 0.000 | 0.000 |
| 0 | D5 | 1 | 334.943 | 334.943 | 0.000 | 0.000 |
| 0 | D6 | 1 | 335.460 | 335.460 | 0.000 | 0.000 |
| 1 | D1 | 1 | 156.367 | 156.367 | 0.000 | 0.000 |
| 1 | D2 | 1 | 154.740 | 154.740 | 0.000 | 0.000 |
| 1 | D3 | 1 | 150.611 | 150.611 | 0.000 | 0.000 |
| 1 | D4 | 1 | 156.475 | 156.475 | 0.000 | 0.000 |
| 1 | D5 | 1 | 155.145 | 155.145 | 0.000 | 0.000 |
| 1 | D6 | 1 | 150.701 | 150.701 | 0.000 | 0.000 |
| 2 | D1 | 1 | 331.729 | 331.729 | 0.000 | 0.000 |
| 2 | D2 | 1 | 331.797 | 331.797 | 0.000 | 0.000 |
| 2 | D3 | 1 | 335.810 | 335.810 | 0.000 | 0.000 |
| 2 | D4 | 1 | 331.842 | 331.842 | 0.000 | 0.000 |
| 2 | D5 | 1 | 332.081 | 332.081 | 0.000 | 0.000 |
| 2 | D6 | 1 | 335.931 | 335.931 | 0.000 | 0.000 |
| 3 | D2 | 1 | 154.611 | 154.611 | 0.000 | 0.000 |
| 3 | D3 | 1 | 150.951 | 150.951 | 0.000 | 0.000 |

Max within-(pass,detector) spread: **0.000 deg**
- pass 0 (all detectors) mean pa_y 332.941, spread 6.899, std 3.067, n=6
- pass 1 (all detectors) mean pa_y 154.007, spread 5.864, std 2.448, n=6
- pass 2 (all detectors) mean pa_y 333.198, spread 4.202, std 1.893, n=6
- pass 3 (all detectors) mean pa_y 152.781, spread 3.660, std 1.830, n=2
- pass 0 vs 1: mean difference -178.934 deg (|diff| - 180 = -1.066)
- pass 0 vs 2: mean difference 0.257 deg (|diff| - 180 = -179.743)
- pass 0 vs 3: mean difference 179.840 deg (|diff| - 180 = -0.160)
- pass 1 vs 2: mean difference 179.191 deg (|diff| - 180 = -0.809)
- pass 1 vs 3: mean difference -1.226 deg (|diff| - 180 = -178.774)
- pass 2 vs 3: mean difference 179.583 deg (|diff| - 180 = -0.417)
- per collection, pa_y folded mod 180 (removes the PA flip): dr1: min 148.56 max 156.48 (n=18), qr3: min 150.95 max 154.61 (n=2)

Within-pass test (extra reads, one detector D3, up to 6 frames/pass spread in MJD; n=24):

| pass | n | MJD span (d) | pa_y min | pa_y max | spread | std | SPS_EPA | collections |
|---|---|---|---|---|---|---|---|---|
| 0 | 6 | 42.1 | 335.338 | 336.578 | 1.240 | 0.446 | ['0.0'] | ['dr1'] |
| 1 | 6 | 36.5 | 147.466 | 150.611 | 3.145 | 1.028 | ['180.0'] | ['dr1'] |
| 2 | 6 | 5.0 | 335.810 | 336.890 | 1.080 | 0.346 | ['0.0'] | ['dr1'] |
| 3 | 6 | 6.1 | 147.107 | 150.951 | 3.844 | 1.315 | ['180.0'] | ['qr3'] |
- (same detector) pass 0 vs 1: 172.829 deg; deviation from exactly 180: 7.171 deg
- (same detector) pass 0 vs 2: 0.614 deg; deviation from exactly 180: 179.386 deg
- (same detector) pass 0 vs 3: 173.260 deg; deviation from exactly 180: 6.740 deg
- (same detector) pass 1 vs 2: -172.215 deg; deviation from exactly 180: 7.785 deg
- (same detector) pass 1 vs 3: 0.431 deg; deviation from exactly 180: 179.569 deg
- (same detector) pass 2 vs 3: 172.646 deg; deviation from exactly 180: 7.354 deg

Per-detector pass-to-pass comparison (mean pa_y per cell; n = header-read frames in the cell; 40 distinct frames):

| det | pass A (n, mean) | pass B (n, mean) | SPS_EPA A/B | diff B-A | diff mod 360 minus 180 (opposite) / diff (same orientation) |
|---|---|---|---|---|---|
| D1 | 0 (n=1, 328.560) | 1 (n=1, 156.367) | ['0.0']/['180.0'] | -172.193 | opposite: -7.807 |
| D1 | 0 (n=1, 328.560) | 2 (n=1, 331.729) | ['0.0']/['0.0'] | 3.168 | same: +3.168 |
| D1 | 1 (n=1, 156.367) | 2 (n=1, 331.729) | ['180.0']/['0.0'] | 175.362 | opposite: -4.638 |
| D2 | 0 (n=1, 334.661) | 1 (n=1, 154.740) | ['0.0']/['180.0'] | -179.921 | opposite: -0.079 |
| D2 | 0 (n=1, 334.661) | 2 (n=1, 331.797) | ['0.0']/['0.0'] | -2.865 | same: -2.865 |
| D2 | 0 (n=1, 334.661) | 3 (n=1, 154.611) | ['0.0']/['180.0'] | 179.949 | opposite: -0.051 |
| D2 | 1 (n=1, 154.740) | 2 (n=1, 331.797) | ['180.0']/['0.0'] | 177.057 | opposite: -2.943 |
| D2 | 1 (n=1, 154.740) | 3 (n=1, 154.611) | ['180.0']/['180.0'] | -0.129 | same: -0.129 |
| D2 | 2 (n=1, 331.797) | 3 (n=1, 154.611) | ['0.0']/['180.0'] | -177.186 | opposite: -2.814 |
| D3 | 0 (n=6, 335.819) | 1 (n=6, 148.647) | ['0.0']/['180.0'] | 172.829 | opposite: -7.171 |
| D3 | 0 (n=6, 335.819) | 2 (n=6, 336.432) | ['0.0']/['0.0'] | 0.614 | same: +0.614 |
| D3 | 0 (n=6, 335.819) | 3 (n=6, 149.079) | ['0.0']/['180.0'] | 173.260 | opposite: -6.740 |
| D3 | 1 (n=6, 148.647) | 2 (n=6, 336.432) | ['180.0']/['0.0'] | -172.215 | opposite: -7.785 |
| D3 | 1 (n=6, 148.647) | 3 (n=6, 149.079) | ['180.0']/['180.0'] | 0.431 | same: +0.431 |
| D3 | 2 (n=6, 336.432) | 3 (n=6, 149.079) | ['0.0']/['180.0'] | 172.646 | opposite: -7.354 |
| D4 | 0 (n=1, 328.677) | 1 (n=1, 156.475) | ['0.0']/['180.0'] | -172.202 | opposite: -7.798 |
| D4 | 0 (n=1, 328.677) | 2 (n=1, 331.842) | ['0.0']/['0.0'] | 3.166 | same: +3.166 |
| D4 | 1 (n=1, 156.475) | 2 (n=1, 331.842) | ['180.0']/['0.0'] | 175.367 | opposite: -4.633 |
| D5 | 0 (n=1, 334.943) | 1 (n=1, 155.145) | ['0.0']/['180.0'] | -179.798 | opposite: -0.202 |
| D5 | 0 (n=1, 334.943) | 2 (n=1, 332.081) | ['0.0']/['0.0'] | -2.862 | same: -2.862 |
| D5 | 1 (n=1, 155.145) | 2 (n=1, 332.081) | ['180.0']/['0.0'] | 176.936 | opposite: -3.064 |
| D6 | 0 (n=1, 335.460) | 1 (n=1, 150.701) | ['0.0']/['180.0'] | 175.242 | opposite: -4.758 |
| D6 | 0 (n=1, 335.460) | 2 (n=1, 335.931) | ['0.0']/['0.0'] | 0.471 | same: +0.471 |
| D6 | 1 (n=1, 150.701) | 2 (n=1, 335.931) | ['180.0']/['0.0'] | -174.770 | opposite: -5.230 |

Pass duration (days, MJD-mid min to max of ALL TAP frames): pass 0: 46.3 d (60789.9-60836.2), pass 1: 44.9 d (60947.0-60991.9), pass 2: 15.3 d (61148.8-61164.1), pass 3: 10.3 d (61305.2-61315.5)

## EpsInd_B
TAP rows 458, science frames 458 [VERIFIED by this run: a2_tap.py]

Frames per release/collection x detector (provenance_version in brackets):

| collection | procver | D1 | D2 | D3 | D4 | D5 | D6 | total |
|---|---|---|---|---|---|---|---|---|
| dr1 | l2b-v27-2026-196 | 3 | 16 | 14 | 4 | 15 | 14 | 66 |
| dr1 | l2b-v27-2026-197 | 0 | 3 | 7 | 0 | 3 | 6 | 19 |
| dr1 | l2b-v27-2026-199 | 0 | 0 | 1 | 0 | 0 | 1 | 2 |
| dr1 | l2b-v27-2026-201 | 0 | 13 | 3 | 0 | 12 | 3 | 31 |
| dr1 | l2b-v27-2026-206 | 4 | 0 | 0 | 4 | 0 | 0 | 8 |
| dr1 | l2b-v27-2026-239 | 0 | 8 | 18 | 0 | 6 | 17 | 49 |
| dr1 | l2b-v27-2026-241 | 11 | 9 | 1 | 11 | 7 | 1 | 40 |
| dr1 | l2b-v27-2026-242 | 21 | 5 | 0 | 21 | 5 | 0 | 52 |
| dr1 | l2b-v27-2026-243 | 4 | 8 | 0 | 3 | 5 | 0 | 20 |
| dr1 | l2b-v27-2026-244 | 3 | 1 | 11 | 3 | 1 | 10 | 29 |
| dr1 | l2b-v27-2026-245 | 0 | 2 | 1 | 0 | 2 | 1 | 6 |
| dr1 | l2b-v27-2026-246 | 0 | 0 | 1 | 0 | 0 | 1 | 2 |
| dr1 | l2b-v27-2026-247 | 0 | 4 | 3 | 0 | 4 | 3 | 14 |
| qr3 | l2b-v27-2026-268 | 0 | 0 | 10 | 0 | 0 | 9 | 19 |
| qr3 | l2b-v27-2026-271 | 0 | 0 | 24 | 0 | 0 | 24 | 48 |
| qr3 | l2b-v27-2026-276 | 0 | 17 | 2 | 0 | 16 | 2 | 37 |
| qr3 | l2b-v27-2026-285 | 0 | 7 | 0 | 0 | 7 | 0 | 14 |
| qr3 | l2b_retry-v27-2026-269 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |
| qr3 | l2b_retry-v27-2026-276 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |

provenance_version (pipeline): {'7.0.5': 458}

Passes (gap > 30 d):

| pass | MJD min | MJD max | n | D1 | D2 | D3 | D4 | D5 | D6 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 60789.86 | 60836.19 | 118 | 3 | 32 | 25 | 4 | 30 | 24 |
| 1 | 60946.96 | 60991.86 | 146 | 24 | 30 | 23 | 23 | 24 | 22 |
| 2 | 61148.85 | 61164.12 | 74 | 19 | 7 | 12 | 19 | 6 | 11 |
| 3 | 61305.23 | 61315.48 | 120 | 0 | 24 | 36 | 0 | 24 | 36 |

Epochs (passes): **4**

### Headers (20 read ok, 0 failed)
- CTYPE1 values: {'RA---TAN-SIP': 20}; CTYPE2: {'DEC--TAN-SIP': 20}
- '-SIP' in IMAGE CTYPE: 20/20; A_ORDER: {3: 20}; B_ORDER: {3: 20}; AP_ORDER: {3: 20}
- FINAST: {0: 20} (IMAGE hdr / else primary); RADESYS {'ICRS': 20}; EQUINOX {None: 20}
- XPOSURE: min 113.5826, max 113.5826; MJD-AVG present in IMAGE: 20, in primary: 0
- PA/survey-like keyword names in IMAGE: ['L2 N_GHOST_FPA', 'NON_SURVEY', 'SPS_ELAT', 'SPS_ELON', 'SPS_EPA', 'SPS_FLAGS', 'SPS_TARGET']; SPS_EPA values by pass: {0: {'0.0': 6}, 1: {'180.0': 6}, 2: {'0.0': 6}, 3: {'180.0': 2}}
- NOTE: keyword SPS_PA_ECL does NOT exist in these headers if absent from the list above; the actual name is SPS_EPA.
- PA/survey-like keywords, primary (first 3 distinct): [('{}', 20)]
- HDUs: ['PRIMARY', 'IMAGE', 'FLAGS', 'VARIANCE', 'ZODI', 'EPSF', 'WCS-WAVE']; PC/CD keys: ['PCOUNT', 'PC1_1', 'PC1_2', 'PC2_1', 'PC2_2', 'CDELT1', 'CDELT2', 'CDELT1A']; SIP keys: ['A_ORDER', 'A_0_0', 'A_0_1', 'A_0_2', 'A_0_3', 'A_1_0', 'A_1_1', 'A_1_2', 'A_2_0', 'A_2_1']

Roll = position angle (deg E of N) of the image +y axis from WCS (astropy all_pix2world incl. SIP, 50 px step at centre):

| pass | det | n | pa_y min | pa_y max | spread | std |
|---|---|---|---|---|---|---|
| 0 | D1 | 1 | 328.560 | 328.560 | 0.000 | 0.000 |
| 0 | D2 | 1 | 334.661 | 334.661 | 0.000 | 0.000 |
| 0 | D3 | 1 | 335.338 | 335.338 | 0.000 | 0.000 |
| 0 | D4 | 1 | 328.500 | 328.500 | 0.000 | 0.000 |
| 0 | D5 | 1 | 334.943 | 334.943 | 0.000 | 0.000 |
| 0 | D6 | 1 | 335.460 | 335.460 | 0.000 | 0.000 |
| 1 | D1 | 1 | 156.367 | 156.367 | 0.000 | 0.000 |
| 1 | D2 | 1 | 154.740 | 154.740 | 0.000 | 0.000 |
| 1 | D3 | 1 | 150.611 | 150.611 | 0.000 | 0.000 |
| 1 | D4 | 1 | 156.475 | 156.475 | 0.000 | 0.000 |
| 1 | D5 | 1 | 153.728 | 153.728 | 0.000 | 0.000 |
| 1 | D6 | 1 | 150.701 | 150.701 | 0.000 | 0.000 |
| 2 | D1 | 1 | 331.729 | 331.729 | 0.000 | 0.000 |
| 2 | D2 | 1 | 331.797 | 331.797 | 0.000 | 0.000 |
| 2 | D3 | 1 | 335.810 | 335.810 | 0.000 | 0.000 |
| 2 | D4 | 1 | 331.842 | 331.842 | 0.000 | 0.000 |
| 2 | D5 | 1 | 332.081 | 332.081 | 0.000 | 0.000 |
| 2 | D6 | 1 | 335.931 | 335.931 | 0.000 | 0.000 |
| 3 | D2 | 1 | 154.611 | 154.611 | 0.000 | 0.000 |
| 3 | D3 | 1 | 150.951 | 150.951 | 0.000 | 0.000 |

Max within-(pass,detector) spread: **0.000 deg**
- pass 0 (all detectors) mean pa_y 332.911, spread 6.960, std 3.108, n=6
- pass 1 (all detectors) mean pa_y 153.771, spread 5.864, std 2.394, n=6
- pass 2 (all detectors) mean pa_y 333.198, spread 4.202, std 1.893, n=6
- pass 3 (all detectors) mean pa_y 152.781, spread 3.660, std 1.830, n=2
- pass 0 vs 1: mean difference -179.141 deg (|diff| - 180 = -0.859)
- pass 0 vs 2: mean difference 0.287 deg (|diff| - 180 = -179.713)
- pass 0 vs 3: mean difference 179.869 deg (|diff| - 180 = -0.131)
- pass 1 vs 2: mean difference 179.427 deg (|diff| - 180 = -0.573)
- pass 1 vs 3: mean difference -0.990 deg (|diff| - 180 = -179.010)
- pass 2 vs 3: mean difference 179.583 deg (|diff| - 180 = -0.417)
- per collection, pa_y folded mod 180 (removes the PA flip): dr1: min 148.50 max 156.48 (n=18), qr3: min 150.95 max 154.61 (n=2)

Within-pass test (extra reads, one detector D3, up to 6 frames/pass spread in MJD; n=6):

| pass | n | MJD span (d) | pa_y min | pa_y max | spread | std | SPS_EPA | collections |
|---|---|---|---|---|---|---|---|---|
| 0 | 6 | 42.1 | 335.338 | 336.474 | 1.137 | 0.435 | ['0.0'] | ['dr1'] |

Per-detector pass-to-pass comparison (mean pa_y per cell; n = header-read frames in the cell; 25 distinct frames):

| det | pass A (n, mean) | pass B (n, mean) | SPS_EPA A/B | diff B-A | diff mod 360 minus 180 (opposite) / diff (same orientation) |
|---|---|---|---|---|---|
| D1 | 0 (n=1, 328.560) | 1 (n=1, 156.367) | ['0.0']/['180.0'] | -172.193 | opposite: -7.807 |
| D1 | 0 (n=1, 328.560) | 2 (n=1, 331.729) | ['0.0']/['0.0'] | 3.168 | same: +3.168 |
| D1 | 1 (n=1, 156.367) | 2 (n=1, 331.729) | ['180.0']/['0.0'] | 175.362 | opposite: -4.638 |
| D2 | 0 (n=1, 334.661) | 1 (n=1, 154.740) | ['0.0']/['180.0'] | -179.921 | opposite: -0.079 |
| D2 | 0 (n=1, 334.661) | 2 (n=1, 331.797) | ['0.0']/['0.0'] | -2.865 | same: -2.865 |
| D2 | 0 (n=1, 334.661) | 3 (n=1, 154.611) | ['0.0']/['180.0'] | 179.949 | opposite: -0.051 |
| D2 | 1 (n=1, 154.740) | 2 (n=1, 331.797) | ['180.0']/['0.0'] | 177.057 | opposite: -2.943 |
| D2 | 1 (n=1, 154.740) | 3 (n=1, 154.611) | ['180.0']/['180.0'] | -0.129 | same: -0.129 |
| D2 | 2 (n=1, 331.797) | 3 (n=1, 154.611) | ['0.0']/['180.0'] | -177.186 | opposite: -2.814 |
| D3 | 0 (n=6, 335.782) | 1 (n=1, 150.611) | ['0.0']/['180.0'] | 174.829 | opposite: -5.171 |
| D3 | 0 (n=6, 335.782) | 2 (n=1, 335.810) | ['0.0']/['0.0'] | 0.028 | same: +0.028 |
| D3 | 0 (n=6, 335.782) | 3 (n=1, 150.951) | ['0.0']/['180.0'] | 175.169 | opposite: -4.831 |
| D3 | 1 (n=1, 150.611) | 2 (n=1, 335.810) | ['180.0']/['0.0'] | -174.801 | opposite: -5.199 |
| D3 | 1 (n=1, 150.611) | 3 (n=1, 150.951) | ['180.0']/['180.0'] | 0.340 | same: +0.340 |
| D3 | 2 (n=1, 335.810) | 3 (n=1, 150.951) | ['0.0']/['180.0'] | 175.141 | opposite: -4.859 |
| D4 | 0 (n=1, 328.500) | 1 (n=1, 156.475) | ['0.0']/['180.0'] | -172.025 | opposite: -7.975 |
| D4 | 0 (n=1, 328.500) | 2 (n=1, 331.842) | ['0.0']/['0.0'] | 3.343 | same: +3.343 |
| D4 | 1 (n=1, 156.475) | 2 (n=1, 331.842) | ['180.0']/['0.0'] | 175.367 | opposite: -4.633 |
| D5 | 0 (n=1, 334.943) | 1 (n=1, 153.728) | ['0.0']/['180.0'] | 178.785 | opposite: -1.215 |
| D5 | 0 (n=1, 334.943) | 2 (n=1, 332.081) | ['0.0']/['0.0'] | -2.862 | same: -2.862 |
| D5 | 1 (n=1, 153.728) | 2 (n=1, 332.081) | ['180.0']/['0.0'] | 178.353 | opposite: -1.647 |
| D6 | 0 (n=1, 335.460) | 1 (n=1, 150.701) | ['0.0']/['180.0'] | 175.242 | opposite: -4.758 |
| D6 | 0 (n=1, 335.460) | 2 (n=1, 335.931) | ['0.0']/['0.0'] | 0.471 | same: +0.471 |
| D6 | 1 (n=1, 150.701) | 2 (n=1, 335.931) | ['180.0']/['0.0'] | -174.770 | opposite: -5.230 |

Pass duration (days, MJD-mid min to max of ALL TAP frames): pass 0: 46.3 d (60789.9-60836.2), pass 1: 44.9 d (60947.0-60991.9), pass 2: 15.3 d (61148.8-61164.1), pass 3: 10.3 d (61305.2-61315.5)

## WISE0855
NOT COMPLETED: IRSA TAP query for this target failed (sync: read timeouts at 400 s, HTTP 502 Proxy Error, connection reset; async submit also 502; a TOP-5 variant also 502/timeout/reset) after several retries over >60 min [VERIFIED: data/a2_log*.txt, a2_retry_*.txt, a2b_*.txt, a2d_top.py output]. Frame count UNKNOWN [NOT VERIFIED]; absence of frames is NOT implied.

## RWAur
NOT COMPLETED: IRSA TAP query for this target failed (sync: read timeouts at 400 s, HTTP 502 Proxy Error, connection reset; async submit also 502; a TOP-5 variant also 502/timeout/reset) after several retries over >60 min [VERIFIED: data/a2_log*.txt, a2_retry_*.txt, a2b_*.txt, a2d_top.py output]. Frame count UNKNOWN [NOT VERIFIED]; absence of frames is NOT implied.

## RDra
NOT COMPLETED: IRSA TAP query for this target failed (sync: read timeouts at 400 s, HTTP 502 Proxy Error, connection reset; async submit also 502; a TOP-5 variant also 502/timeout/reset) after several retries over >60 min [VERIFIED: data/a2_log*.txt, a2_retry_*.txt, a2b_*.txt, a2d_top.py output]. Frame count UNKNOWN [NOT VERIFIED]; absence of frames is NOT implied.

## Plan questions

- Barnard: 358 frames, 3 passes, SIP 20/20, max within pass/detector roll spread in 20-frame set 0.014 deg (n/detector/pass is 1-2: weak); within-pass extension spreads per pass: [0.72, 0.719, 1.421]
- EpsInd_A: 460 frames, 4 passes, SIP 20/20, max within pass/detector roll spread in 20-frame set 0.000 deg (n/detector/pass is 1-2: weak); within-pass extension spreads per pass: [1.24, 3.145, 1.08, 3.844]
- EpsInd_B: 458 frames, 4 passes, SIP 20/20, max within pass/detector roll spread in 20-frame set 0.000 deg (n/detector/pass is 1-2: weak); within-pass extension spreads per pass: [1.137]

## Completeness notes (added by hand after generation)
- WISE0855, RWAur, RDra: NOT COMPLETED. IRSA TAP failed repeatedly (read timeouts, HTTP 502, connection reset; async submit 502). Coverage/roll for these is UNKNOWN [NOT VERIFIED]; do not read it as 0 frames.
- EpsInd_B within-pass extension is PARTIAL: only pass 0 (6 frames) read; 18 reads failed with S3 EndpointConnectionError (transient network cut). The per-detector EpsInd_B table above mixes n=1 cells for passes 1-3. EpsInd_A (same detector D3, 24 frames) is the complete within-pass reference.
- Header sets: 20 diverse frames per target plus 18-24 extra same-detector frames (exceeds the 20-frame cap; S3 header reads only).
- Pass-ordering note: Barnard and Eps Indi passes alternate SPS_EPA 0/180; keyword SPS_PA_ECL does not exist, the key is SPS_EPA (plus SPS_ELON/SPS_ELAT).

## Retry round 2 for WISE0855 / RWAur / RDra (20-minute cap reached; all still NOT COMPLETED)
- Async TAP (scripts\a2b_async.py): submit succeeded for WISE0855 (job 28302595, HTTP 303) but the job stayed QUEUED for >10 min and polls returned 502; checked again later: phase still QUEUED [VERIFIED: data\a2b_WISE0855.txt, curl of the job phase]. RWAur and RDra were not submitted (one target at a time, cap reached).
- SIA fallback (different service, scripts\a2e_sia.py, COLLECTION spherex_dr1/qr3/qr2, circle 0.1 deg): the WISE0855 run did not return within ~10 min (300 s timeouts with retries) and was killed. A single quick probe, COLLECTION=spherex_qr3 only, radius 0.05 deg at the 2026.0-propagated position, returned an empty table (header only, 641 bytes, 14 s) [VERIFIED: data\A\sia_test.xml]. That says only "no qr3 SIA rows at that radius", NOT that dr1/qr2 or TAP have none; coverage of WISE0855 remains UNKNOWN [NOT VERIFIED].
- No headers/roll/SIP were read for these three targets.
