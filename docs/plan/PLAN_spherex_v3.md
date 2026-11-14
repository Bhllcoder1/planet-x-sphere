# SPHEREx Blink: PLAN v3 (delta on v2 + thin-slice build order)

Written as changes on `PLAN_spherex_v2.md` (kept unchanged; v1 also kept). Any v2 section not named here stands as written. No web lookups for v3; only the local Stage 0 reports.

Tags: **[V: file]** = verified by a real-data run in that report. **[INTERIM]** = from a run that is not finished (one frame, or the report is still being updated). **[NV]** = not verified. **[ASSUMPTION]** = set in this plan, unchecked. Arithmetic on verified numbers is marked (arith).

Stage 0 status: `s0_B.md` FINAL, `s0_D.md` FINAL, `s0_A.md` INTERIM (Barnard, ε Indi A, ε Indi B complete; WISE 0855, RW Aur, R Dra TAP failed), `s0_C.md` **does not exist yet**: the aberration numbers below come from the orchestrator's brief (frame A only) and are [INTERIM].

---

## 1. What v3 changes vs v2

| Topic | v2 | v3 | Basis |
|---|---|---|---|
| Delivery | 9 stages, ~14 days, first demo at Stage 1 | **Thin slice first**: a "minimum convincing demo" (MCD) in ~5 working days on warm-cache targets; everything else is a ranked "next slice" (§4.2) | CRITIQUE #1; unknown deadline |
| Fetch (C.2) | S3 vs cutout decided by D8 (p50 < 1 s) | **S3 is the primary path** (works, exact, 0/30 failures). Cutout service demoted to last-resort fallback (5/14 HTTP 503, p50 12.4 s, ~4 MB each). D8 failed **from Turkey**; in-region timing still open (D9). Demo targets are **prefetched**, so the demo does not depend on D9 | [V: s0_B §2-5] |
| Metadata (C.1) | `cloud_access` column gives the key; TAP sync | No `cloud_access` column: key = `uri` minus `ibe/data/spherex/`. TAP took 202 s (Barnard) and failed outright (timeouts, 502) for 3 of 6 targets → **async TAP + L0 cache are mandatory**; demo frame lists are frozen files | [V: s0_B §1; s0_A WISE0855/RWAur/RDra] |
| Masks (C.4) | GHOST/STREAK/CROSSTALK/TRANSIENT as caution only, D13 decides | **Two mask profiles** (centroid, mover search), fixed by data (§2.1) | [V: s0_D §2-4] |
| Mode N (D) | Rigid integer moves incl. "exact 180° flip" between surveys; rolls within a survey ≲1° | **False as stated.** Same-detector roll spread *within one pass* is 0.7–1.4° (Barnard D2) and 1.1–3.8° (ε Indi D3); opposite-orientation passes differ from 180° by 0.0–0.6° (D2, D5) up to 3.5–7.8° (other detectors). Mode N is redefined (§2.2) | [V: s0_A roll tables] |
| Aberration (v2 A, C.9) | "Irrelevant" by reasoning | Supported on **one frame**: header WCS vs Gaia ~0.01 px, against ~1.9 px (11.7") predicted if aberration were left in. Keep C.9 correction; add an alarm (§2.3) | [INTERIM: s0_C frame A, from brief] |
| Mover search (C.13) | Flags undecided | Do **not** mask OUTLIER or SOURCE; promote compact OUTLIER clusters to candidates; STREAK/GHOST/CROSSTALK veto with reason code | [V: s0_D §3-4] |
| Pass model | "a few days", WISE 0855 0.02 px within a pass | A pass lasts **10–55 days** (Barnard 46/55/37 d; ε Indi 46/45/15/10 d) with 75–141 frames, 17–25 per detector (Barnard) | [V: s0_A] |
| Detection | `sep` | **photutils** (DAOStarFinder / segmentation) in prototype; `sep` optional on Linux | `sep` has no wheel for Python 3.14 here [V: environment] |
| Background (C.5) | window-local `sep.Background` | Background must **not depend on the request window** (window-dependent median moved COM by 9.7e-3 px): estimate on fixed parent-grid tiles | [V: s0_B §4 caveat 1] |
| GPU | RunPod on trigger | **vast.ai on-demand** on the same B.5 trigger, only for shift-and-stack; user accepted CPU-first | User decision; vast.ai price [NV] |
| WISE/unWISE overlay | absent | "Later" list (optional in the challenge) | User decision; CRITIQUE #7 |
| AI upscaling (E level 3) | recommend drop | **Still recommend drop**; not built unless the user says otherwise | User undecided |

### 1.1 CRITIQUE_v2 points

| # | Point | Status in v3 |
|---|---|---|
| 1 | Scope too big, deadline never asked | **Resolved**: MCD + ranked slices (§4); deadline is Q1 |
| 2 | GHOST/STREAK/CROSSTALK/TRANSIENT not masked | **Resolved by data**: STREAK + GHOST masked for centroids; CROSSTALK/TRANSIENT kept as caution flags because masking them removes 14–21 % of Galactic Centre frames and hits 9–17 % of star cores [V: s0_D] |
| 3 | Aberration is reasoning only | **Partly**: one frame says header WCS is catalog-frame [INTERIM]; frames B/C pending |
| 4 | Mode N relies on roll < 1° | **Resolved**: measured, assumption false, Mode N redefined [V: s0_A] |
| 5 | Can flags hide movers? | **Mostly resolved**: core pixels of 17/17 detected asteroids survive the fit mask; 11/17 carry OUTLIER, 6/17 SOURCE [V: s0_D]. Open: 2026 frames have ~0 OUTLIER (field vs epoch vs version), crowded fields (0/4 detected) |
| 6 | GPU not asked | **Resolved** (user: CPU-first, vast.ai on demand) |
| 7 | No WISE overlay | **Resolved** as "later" |
| 8 | Numbers that are assumptions | **Open** (error budget, VM price, Hetzner US, vast.ai price). Improved: file size 61–65 MB [V], fetch timings from Turkey [V] |
| 9 | User workload | **Resolved**: 6 questions + 3 screenshot questions (§7) |

---

## 2. Decisions now fixed by data

### 2.1 Masks (replaces v2 C.4 "our additions" and "caution flags")
Bit numbers as v2 C.4 (Table 16) [V: CRITIQUE confirms].

| Profile | Masked pixels | Kept as per-measurement caution (flag within 3 px of the fit) | Evidence |
|---|---|---|---|
| **Centroid / photometry** | fit mask `0x3C028E44` + OVERFLOW (1) + DICHROIC (7) + STREAK (25) + GHOST (22–24) | TRANSIENT (0), CROSSTALK (20), HALO, PERSIST | Extra cost 0.1–0.5 % of pixels in sparse frames [V: s0_D §4] |
| **Mover search** | fit mask only | STREAK, GHOST, CROSSTALK = **veto with reason code** (candidate kept, marked); TRANSIENT/HALO near bright candidates = caution | 0/17 mover cores hit by fit mask [V: s0_D §3] |
| **Never masked in mover search** | OUTLIER (19), SOURCE (21) | OUTLIER compact cluster (≤40 px) not matching Gaia = **candidate boost** | 11/17 movers OUTLIER vs ~3 % of static stars [V: s0_D §3] |
| **Background** | v2 background mask, **but drop SOURCE where SOURCE > 50 % of the frame** (crowded) and fall back to ZODI + sigma-clip | — | SOURCE = 100 % of GC frames [V: s0_D §2] |

Frames with fit-mask fraction > 50 % (e.g. gc3, 67.8 %, PERSIST 66.5 %) are shown but get "unusable for astrometry" [V: s0_D §2 numbers; threshold ASSUMPTION].

### 2.2 Mode N rules (replaces v2 D row "N")
Facts [V: s0_A]: within-pass same-detector roll spread 0.72° / 0.72° / 1.42° (Barnard D2, 3 passes); 1.24 / 3.15 / 1.08 / 3.84° (ε Indi A D3, 4 passes). Same-orientation passes: Barnard ≤ 0.62°; ε Indi D1/D4 differ by 3.17° (n=1 per cell). Opposite orientation: Barnard D2/D5 within 0.0–0.3° of 180°, D1/D3/D4/D6 off by 3.5–4.3°; ε Indi D3 off by 6.7–7.8° (n=6 per cell). Within one pass, detectors differ by up to ~3–7°. The keyword `SPS_EPA` (0/180) labels orientation [V: s0_A headers].

New rules:
1. **Mode N** = each frame on its own native grid, integer zoom, nearest; registration by **integer shift only** (plus an exact 180° turn when `SPS_EPA` differs and the detector matches). The leftover rotation θ_res and sub-pixel offset vs the reference frame are always computed from the corrected WCS and shown: "θ_res 0.7° → ≤ 0.26 px at window edge".
2. N is the **auto-default only when** same detector **and** r_edge·θ_res ≤ 0.25 px (r_edge = window half-diagonal). For a 31×31 window (r_edge ≈ 21 px) that means θ_res ≤ 0.68° (arith). Otherwise the viewer opens in Mode R / R-k with a one-line reason.
3. Overlays (centroids, Gaia) in Mode N are drawn in each frame's own native float coordinates, so markers and pixels never disagree; what is inexact is only frame-to-frame registration, and that is what the badge reports.
4. **R-k (server, k=4–8 NN raster) is promoted into the MCD** as the cross-orientation path, because it needs no WebGL work; the GPU affine Mode R moves to slice 2.

### 2.3 Aberration status (v2 §A row, C.9)
- Header WCS appears to give catalog-frame (astrometric) positions: frame A offset vs Gaia ≈ 0.01 px where 1.9 px would show if aberration were not absorbed [INTERIM: 1 frame; B/C pending].
- C.9 stays the standard step. **New alarm:** if the fitted shift is > 0.5 px, or shifts across frames correlate with the predicted aberration vector (r > 0.8 over ≥ 10 frames), set "aberration-like offset" on the frame and do not publish μ until reviewed [ASSUMPTION thresholds].
- Consequence for §3 risk 1: the header WCS is unlikely to explain the 1–3 px asteroid offset (but this rests on one frame).

### 2.4 Fetch strategy (replaces v2 C.2; updates B.3, B.4, D8, D9)
Measured from Ankara, residential link (not AWS) [V: s0_B]: S3 anonymous range reads work; compressed FLAGS `.section` works (100×100 → 359 KB, 101 GETs, no full HDU); astropy does **one GET per image row** (row stride 8,160 B), so `cache=none` = ~22 s per HDU window; 1 MiB readahead = p50 3.90 s / p95 12.7 s per 4-HDU frame-window, plus file open p50 5.1 s; HDU lookup by **name** scanned 19.6 MB, by **index** 4.2 MB. Cutout service: 4 MB per cutout regardless of size, p50 12.4 s, 5/14 HTTP 503.

Decisions:
1. **S3 primary.** Open HDUs by integer index (layout IMAGE=1, FLAGS=2, VARIANCE=3, ZODI=4, EPSF=5, WCS-WAVE=6) [V: one file; check per release]. Cache a per-file **byte-offset map** (header + data start of each HDU) in L1 so a warm read needs no header scan.
2. **Coalesced row-span reads**: for IMAGE/VARIANCE/ZODI, one Range GET covering rows y0..y1 (100 rows ≈ 0.8 MB; 256 rows ≈ 2.1 MB) (arith), the 4 HDUs fetched **in parallel** (`s3fs.cat_ranges` or aiohttp). FLAGS via astropy `.section` over a bytes cache with 64 KiB blocks (738 KB measured) [V: s0_B table]. The v2 D8 byte rule is replaced by "≤ 2× the row span".
3. **Cutout service** only if S3 fails for a file; at most 1 in flight; 503 → back off 45 s; never on the demo path.
4. **Prefetch + warm cache for demo targets**: Barnard's 358-frame list already exists from Stage 0 (`stage0/data/B`, `stage0/data/A`); reuse it, skip TAP. Barnard estimate: 358 × 4 HDUs × (0.8 + 2.1 MB) ≈ 4.2 GB (arith), fetched once in parallel by an offline script.
5. **Re-measure in us-east-1 (D9, mandatory before any "live field" claim)**: 50 frames, coalesced parallel reads, p50/p95 per frame-window, file open time, failure rate, from (a) AWS EC2 us-east-1 and (b) Hetzner Ashburn [ASSUMPTION: exists]. Target p50 < 1 s per frame-window. Not measured anywhere yet [NV].

### 2.5 Parent-pixel rule (closes v2 R2 for one case)
`x_orig = 1 + x_cut − CRPIX1A` (0-based both sides) agrees with the SIP WCS round trip to < 1e-7 px and pixel arrays match exactly for 2 cutouts × 4 HDUs, one frame, detector 2 [V: s0_B §4]. Not tested: edge-clipped cutouts, other detectors [NV] (cheap test in §5). Because S3 is primary, the rule matters only for the cutout fallback.

### 2.6 Pipeline step updates (only changed cells)
- **C.1 Query:** key from `uri`; async TAP (`/async`, poll, 15 min ceiling) with L0 cache; one `CONTAINS(POINT, poly)` per target (INTERSECTS/OR rejected) [V: s0_A]. Dedupe (obs id, detector) keeping the newest `l2b-v27-*` processing tag; DR1 and QR3 coexist for the same targets and may be mixed (both provenance 7.0.5) [V: s0_A]. On TAP failure: "archive busy, retry queued", never a silent "no coverage".
- **C.2 Fetch:** §2.4.
- **C.3 Ingest:** SIP order 3 present 20/20, FINAST 0, RADESYS ICRS, XPOSURE 113.58 s, MJD-AVG in the IMAGE header (not primary) [V: s0_A]. Read `SPS_EPA` for orientation. Roll from the corrected WCS.
- **C.4 Masking:** §2.1.
- **C.5 Background:** fixed parent-grid tiles (e.g. 64×64 aligned to parent pixel 0), not request windows.
- **C.6 Detection:** photutils; saturated/NaN cores (Barnard: 2×2 NaN core in IMAGE and VARIANCE, DAOStarFinder missed it) [V: s0_B] → the user's target is **always forced-fit at its predicted position**, never required to be detected.
- **C.7 Centroid:** NaN core = masked pixels inside the ePSF fit (wing fit), badge "saturated-fit"; σ from the fit covariance, which will be larger.
- **C.9 WCS correction:** unchanged method + alarm (§2.3). Shift-only model in the MCD; similarity/affine after D6.
- **C.12 Passes:** 30-day gap rule confirmed (passes 10–55 d, gaps > 100 d) [V: s0_A, 3 targets]. Pass blink pairs frames of the same detector.
- **C.13 Movers:** masks per §2.1; candidate match radius to SkyBoT = max(3 px, 3σ_eph) until the offset in §3 is explained; **disable linking** when SOURCE > 50 % of the window or local noise > 5× the sparse-field median (crowded: 0/4 found) [ASSUMPTION thresholds]. WISE 0855 within a 46-day pass moves 8.1"/yr × 46/365 ≈ 1.0" = 0.17 px (arith; v2 said 0.02 px) — still far too small for in-pass linking; slow-mover mode b' (cross-pass) unchanged.
- **C.14 SkyBoT:** use `-objFilter=100` (110 errored) [V: s0_D].

---

## 3. Open risks (updates to v2 §H; others unchanged)

| # | Risk | Status | Mitigation / next test |
|---|---|---|---|
| R1 | S3 range read fails | **Closed for correctness** [V: s0_B]; replaced by R1b | — |
| R1b | **Fetch latency**: 3.9 s p50 per frame-window from Turkey; in-region unknown | Open [NV in-region] | Coalesced parallel reads; D9 on EC2; warm cache for demo targets |
| R2 | Parent-pixel rule | Closed for 1 frame/detector [V]; edges open | §5 test |
| R22 | **TAP latency ~200 s and outright failures** (3/6 targets failed > 60 min) | Open [V: s0_A, s0_B] | Async jobs + L0 cache are mandatory; frozen frame lists for demo targets; UI shows "archive busy" |
| R23 | **Cutout service 503s** (5/14 at 1 in flight) | Open [V: s0_B] | Fallback only; never on the demo path |
| R24 | **1–3 px offset between SkyBoT prediction and observed asteroid** (ephemeris σ only 0.004–0.02") | Open [V offset exists: s0_D] | Likely parts (arith, untested): (a) the D run used the **brightest pixel**, not a centroid (±0.5 px quantisation); (b) geocentre (observer 500) vs LEO spacecraft: ~7,000 km / (1.5 AU) ≈ 6.4" ≈ 1.0 px for a main-belt object; (c) timing: at 65"/h a 1-px move takes ~340 s. WCS ruled out only by one frame [INTERIM]. Test in §5 |
| R5 | Saturated cores (Barnard NaN core) | Confirmed [V: s0_B] | Wing fit; forced position; badge; Barnard μ acceptance may become "wing-fit, wider σ" |
| R25 | **Crowded fields**: SOURCE 100 %, CROSSTALK 14–21 %, PERSIST up to 66 %, 0/4 movers found | Confirmed [V: s0_D] | Crowded-field banner; linking off; no CROSSTALK frame mask |
| R26 | **Roll differs within a pass** (0.7–3.8°) | Confirmed [V: s0_A] | §2.2 rules; R-k in MCD |
| R27 | OUTLIER ~2 % in 2025W51/52 frames, ~0 in 2026W12/13: field, epoch or version? | Open [V: s0_D] | If version-driven, OUTLIER promotion fails in some releases → never rely on it alone |
| R3/R4 | Coverage of WISE 0855, RW Aur, R Dra unknown (TAP failed); WISE 0855 detectability unknown | Open | §5 |
| R17 | Hetzner US location/price | Open [ASSUMPTION] | D9 |

---

## 4. Minimum convincing demo (MCD)

**Targets:** Barnard's Star + WISE 0855 (user may swap; if WISE 0855 coverage/SNR fails, fall back to **ε Indi B**, which has 458 frames in 4 passes [V: s0_A]).

**What a judge sees (one page, warm cache, no live archive call):**
1. Target picker (2 targets) → a ~31×31 native window around the target.
2. **Mode N blink** within a pass (same detector), integer zoom chosen per frame (z = 8…32), nearest-neighbour, pixel grid toggle; θ_res/offset badge (§2.2).
3. **Pass blink**: one representative stack-free frame (or frame sequence) per pass, same detector; Mode N if the §2.2 rule allows, otherwise server R-k raster, labelled.
4. **Centroid markers** (cross at float position + 1σ ellipse, 2σ dashed) for the target and field stars; target forced-fit; "saturated-fit" badge on Barnard.
5. **Gaia overlay** propagated to each frame's MJD-AVG.
6. **WCS correction badge** per frame: "shift 0.0x px, σ 0.00y px, N = n" (shift-only model).
7. Readout: target Δ between passes in px and arcsec with σ, vs Gaia prediction. Barnard moves ≈ 0.96 px pass 0→1 and ≈ 1.7 px pass 0→2 (arith from 10.4"/yr and pass mid-dates); WISE 0855 ≈ 0.66 px per ~6 months (v2 arith).

**Out of the MCD:** arbitrary fields, job queue, Mode R GPU, stacks/differences, mover finder, SkyBoT, spectra, drizzle, WISE overlay, GPU.

### 4.1 Day-by-day (working days; after Q1 is answered; S = Sonnet, H = Haiku, O = Opus)

| Day | Tasks | Tier | Done when |
|---|---|---|---|
| 0 (parallel, now) | Remaining Stage 0 items 1–4 and 10 of §5 | S/H | reports written |
| 1 | Offline prefetch script (frozen frame list, coalesced S3 reads, byte-offset map, L1 files) for Barnard; start WISE 0855 / ε Indi B frame list via async TAP | S | Barnard windows (target 64² + astrometry 256²) on disk for all 358 frames |
| 1 | Pixel-convention + transform spec (N, R-k, overlay transform; one function for p0/texture offset) | O (short) | spec + unit tests listed |
| 2 | Viewer: Canvas2D or WebGL2 texelFetch per D1 checkerboard harness; Mode N, integer zoom, blink, grid; static FastAPI serving precomputed files | S build, H runs T-V1 | T-V1 passes at DPR 1/1.25/2 |
| 3 | ePSF centroiding from the EPSF HDU (GriddedPSFModel, oversampling 5; D5 normalisation/orientation check first), masks per §2.1, NaN-core wing fit, covariance → ellipses | S code, O reviews maths (diff only) | T1/T2 synthetic: \|bias\| < 0.02 px at SNR > 50 |
| 4 | Gaia match + shift-only C.9 + badge; Gaia overlay; pass grouping; R-k raster for cross-orientation pass blink | S | ≥ 90 % Gaia stars within 3σ after shift [ASSUMPTION threshold for MCD] |
| 5 | Second target; readout vs Gaia; deploy on a small CPU VM (Docker, Caddy, static + FastAPI); screenshots to user (§7) | S, H checks links/screenshots | public URL, both targets render warm < 3 s |

**3-day emergency version (if the deadline is very close):** Barnard only; header WCS + Gaia overlay with residual readout (no fitted correction); centroid ellipses; within-pass blink in Mode N; recorded screen video if no deploy.

### 4.2 Next slices, in priority order
1. **Motion fit + track panel** (Barnard μ vs Gaia; joint per-pass fit C.7b) — S code, O review. ~1 day.
2. **Mode R (GPU affine NN)** + T-V2/D3 — S, H. ~1 day.
3. **Live arbitrary field**: RQ/Redis queue, async TAP, progressive SSE, politeness (v2 B.2–B.4) — S. ~1.5 days. **Requires D9 result**.
4. **Mover finder** (catalog linking, OUTLIER promotion, vetoes, SkyBoT with widened radius, time-scrambled false rate) — O design, S code, H runs. ~2 days.
5. **Stacks/differences + slow-mover mode** (v2 C.12, C.13 b') — S. ~1.5 days.
6. **Shift-and-stack on vast.ai GPU** — only if the v2 B.5 trigger fires on slice 4/5 timings: rent one on-demand GPU, run C.13b on the demo fields, record the result and screenshots, release the instance. S code, O decides. ~1 day + rental [vast.ai price NV].
7. Spectra / λ light curves (v2 Stage 7) — S.
8. Later list: WISE/unWISE overlay, drizzle level 2 (D15, if Q6 = yes), RW Aur/R Dra polish.

**Cut first** (from the end): 8 → 7 → 6 → 5 → 3 (keep the demo on warm targets) → 2 (R-k already covers rotation honestly). Slices 1 and 4 are the last to cut.

### 4.3 Model-tier rule (unchanged from v2 §G, made explicit)
Opus: spec writing, maths review of diffs, gate decisions, GPU decision. Sonnet: all code and analysis scripts. Haiku: running test harnesses, checking links/screenshots, collecting timings. One brief, one output file, then close.

---

## 5. Remaining Stage 0 items (one-line cheap test each)

1. **Coverage of WISE 0855, RW Aur, R Dra:** async TAP retried off-peak (or from the D9 VM), one `CONTAINS(POINT)` each; write frames/detector/pass. — S
2. **WISE 0855 detectability:** forced ePSF photometry at the propagated position on ~10 frames per pass in the long-λ detectors (D5/D6), plus an inverse-variance sum per pass; report SNR. — S, O reviews
3. **Aberration frames B and C:** finish `s0_C` (same script as frame A, two more frames, different epochs/orientations). — S
4. **In-region fetch timing (D9):** 1-hour EC2 us-east-1 VM (and Hetzner Ashburn if it exists), 50 frames, coalesced parallel reads; p50/p95, open time, failures. — S
5. **D5 ePSF normalisation/orientation:** fit the EPSF to itself at known offsets and transposed-χ² on 200 stars. — S
6. **D13 injection:** inject 500 ePSF stars into 10 real frames; core loss and centroid bias under the centroid profile vs fit mask only. — S
7. **Asteroid offset (R24):** refit the 17 detected movers with ePSF centroids, re-query ephemerides with a spacecraft/topocentric observer if available (else apply a computed LEO parallax), check residuals vs the parallax direction. — S
8. **OUTLIER cause (R27):** OUTLIER fraction for 10 frames of one sparse field across weeks and processing tags. — H
9. **Parent rule at edges:** one edge-clipped cutout + one other detector vs S3. — H
10. **D1 checkerboard harness** (Canvas2D + WebGL2), Playwright screenshots. — S build, H run
11. **S0.9 in-file ePSF vs calibration file** (byte compare). — H

Items 1–4 and 10 block the MCD (Day 0–2); the rest may run alongside the build.

---

## 6. Updated v2 sections, short list
- v2 §B.1–B.2, B.7: unchanged, but not built until slice 3; the MCD uses static files + a thin FastAPI.
- v2 §B.3: L1 adds the per-file byte-offset map; demo targets frozen in L0.
- v2 §B.4: S3 parallelism starts at 8 per worker, raise after D9 [ASSUMPTION]; cutout service 1 in flight with 45 s backoff on 503.
- v2 §B.5: RunPod → vast.ai on-demand; trigger rules unchanged.
- v2 §C.7b, C.8, C.10, C.11, C.15: unchanged.
- v2 §D error budget: unchanged except "Header WCS (raw)" may be checked against Gaia directly (frame A ~0.01 px [INTERIM]).
- v2 §E: unchanged; level 3 dropped by default.
- v2 §F: D8 criteria replaced (§2.4); D9 now blocks slice 3, not the MCD.
- v2 §G stages 1–8: superseded by §4 order.

---

## 7. Questions for the user

1. **Hackathon deadline (date and time zone)?** Default: assume 7 days → MCD + slices 1–2.
2. **Monthly budget cap?** Default: EUR 30/month CPU VM + up to $20 of on-demand vast.ai GPU, only if the trigger fires.
3. **Provider / region?** Default: whichever of AWS us-east-1 or Hetzner Ashburn wins D9; AWS if unsure.
4. **Expected traffic?** Default: jury/demo only (a few users/day) → warm-cache targets only, no IRSA helpdesk email yet.
5. **Top-2 demo targets?** Default: Barnard's Star + WISE 0855 (fallback ε Indi B if WISE 0855 is undetected).
6. **Drizzle (level 2): spend one day on it?** Default: no, keep it in the "later" list. (AI upscaling stays dropped unless you object.)

**Screenshot questions for the thin slice (only these three):**
- **Q-H1 (Day 2):** "In these checkerboard images at zoom 3, 7 and 16.5, do you see any grey, blurred, or unevenly wide squares? (yes/no per image)"
- **Q-H2 (Day 4):** "Barnard pass blink: can you see the star step while the field stars stay put? Is the 'θ_res / offset' badge and the 'resampled R-k' label understandable?"
- **Q-H3 (Day 5):** "Pick the stretch (asinh / linear / zscale) and dark or light theme from these 6 images."
