# SPHEREx Blink: PLAN v2 (server-centred, precision-first, test-driven)

Supersedes v1 (`PLAN_spherex.md`, kept unchanged) where they conflict.
Tags: **[V]** = verified in the research notes (page, PDF, or live curl). **[NV]** = marked not verified in the notes. **[ASSUMPTION]** = added in this plan and not checked. Anything [NV] or [ASSUMPTION] counts as unknown until a Stage 0 test or an acceptance test closes it. No new web lookups were made for v2. The one open infrastructure question (AWS vs. a cheaper provider for reading the us-east-1 bucket) is answered by measurement (test D9), not by reading more pages.

Units: 1 native px = 6.15" [V]. 0.2 px = 1.23". WCS RMS 0.1–0.4" = 0.016–0.065 px [V].

---

## A. What changed vs v1

| Topic | v1 | v2 | Why |
|---|---|---|---|
| Processing | Offline precompute + static site | **Rented VM runs Python per request**. Precompute is just a warm cache | User decision 1 |
| Browser data sources | Static files only | Talks **only to our server** (no CORS issue) | Same; IRSA/Gaia send no ACAO header [V] |
| ePSF oversampling (R9) | 5 vs 10 conflict | **5x, 33x33, 21x21 zones (D3: 11x41)** [V Expsupp pp.13,52,59]. "10x / 101x101" was the old QR2 PSF HDU | Closed |
| WCS | "Unknown, maybe refine" | Header is TAN-SIP order 3 from astrometry.net + SCAMP against Gaia DR3 with PM, RMS <0.3" [V]. **A measured correction (shift/rot/scale vs propagated Gaia) is a standard pipeline step**, stored beside the raw values, shown with its σ | Re-solving from scratch will not beat 0.1–0.4" |
| Aberration | Assumed none | Irrelevant to us: WCS was fitted to catalog-frame Gaia positions, so it already outputs astrometric positions. Our Gaia correction absorbs any residual (reasoning, checked by D6) | RADESYS=ICRS, aberration not mentioned [V] |
| Flags | "decide in S0.2" | Table 16 bit sets adopted (C.4) | [V Expsupp pp.33–35, 45] |
| Display | One "affine-exact aligned" view | **Explicit display modes** (N, R, S) with separate guarantees. You cannot have native pixels and sky alignment in one view when the rolls differ | notes_viewer key concept |
| Viewer choice | Custom WebGL2 (assumed) | **Chosen by tests** among 6+ options (F) | User decision 3 |
| WISE 0855 | "pass-stack blink" | Only **cross-pass** motion (≈0.66 px per 6 months; 0.02 px within a pass). Detectability must be tested first | [V cadence] + arithmetic |
| Moving objects | Simple residual highlight | Catalog-space linking (CPU) + KBMOD-style shift-and-stack only where ≥8–10 frames overlap (GPU candidate) + SkyBoT tagging | notes_moving |
| Data access | Cutout service | **S3 byte-range windows vs. cutout service decided by test D8** | ~4 MB per cutout [V], most of it ePSF/tables [ASSUMPTION] |
| Time scale | NV | UTC, MJD-AVG midpoint, XPOSURE 113.58 s [V] | Closed |
| Hosting | GitHub/CF Pages | VM; region/provider by test D9; CPU first, GPU only on a measured trigger | User decision 1 |

---

## B. Architecture (server-centred)

### B.1 Components
```
Browser (thin client: viewer + overlays + controls; URL state)
   │ HTTPS (JSON + binary float32, zstd)
Caddy (TLS, compression, serves /cache/* immutable files, rate limit per IP)
   │
FastAPI (api)  ── enqueue ──►  Redis  ◄── workers (RQ or arq; N = vCPU-1 processes)
   │  /job/{id} SSE progress           │
   │                                   ├─ irsa_client  (TAP/SIA metadata; cutout service fallback)
   │                                   ├─ s3_reader    (anonymous fsspec, byte-range HDU windows)
   │                                   ├─ pipeline     (C.1–C.15: astropy, photutils, sep, reproject)
   │                                   ├─ catalogs     (Gaia TAP, SkyBoT, Horizons, server-side only)
   │                                   └─ writer       (products → content-addressed cache)
Disk cache (/cache, LRU by size) ── later: object storage
```

### B.2 Request flow
1. `POST /api/field {ra, dec, fov, release}` → returns `job_id` right away. If a full product already exists for (field key, release, pipeline version), returns the manifest URL instead.
2. Worker: metadata query (cached 24 h; IRSA updates weekly [V]) → frame list → fetch windows in parallel → per-frame steps C.3–C.10 in a process pool → per-pass steps C.11–C.13.
3. **Progressive results:** the manifest is rewritten after every 10 frames, and SSE pushes "n of N frames ready". The browser starts blinking from the first frames.
4. All products are immutable files: `/cache/{release}/{pipever}/{fieldkey}/...` with `Cache-Control: immutable`.

Field key = HEALPix cell (nside 4096, ~52") of the centre + fov bucket. Nearby requests then share the per-frame work [ASSUMPTION: good enough reuse; measure the hit rate].

### B.3 Caching (three levels)
| Level | Key | Content | Reason |
|---|---|---|---|
| L0 metadata | (cone, release, day) | TAP rows | TAP sync can take ~28 s per call [V live] |
| L1 raw window | (s3 key, HDU, window) | float32 IMAGE/VAR/ZODI, u32 FLAGS, headers | Never fetch the same bytes twice |
| L1b ePSF | (detector, ePSF cal version or file hash) | 441/451 x 33x33 | If the in-file ePSF equals the calibration file, it is fetched once per detector (test S0.9) |
| L2 products | (fieldkey, pipever) | per-frame products, stacks, catalogs, manifest | Repeat visits cost nothing |
Warm cache: the 5 test targets are precomputed after each weekly release.

### B.4 Politeness to IRSA (no rate limits are documented [V by absence])
- IRSA HTTP (TAP, SIA, cutouts): a global semaphore of **4** in flight (the tutorial ceiling is 7–12 for batch use [V]). Retries 3x with 10·(n+1) s backoff [V], identical in-flight requests merged, at most 1 uncached job per client IP at a time.
- S3 (AWS Open Data, not IRSA's servers [V]): up to 32 parallel range GETs [ASSUMPTION: acceptable; lower if we see throttling].
- Before public launch: email the IRSA helpdesk with the expected load (Q5) and set a User-Agent with an operator contact that the user chooses.

### B.5 VM region, provider, GPU
Facts: the bucket is in us-east-1, anonymous, and has no egress charge to us [V]. Same-region EC2 reads are probably fastest [NV]. Verified prices: Hetzner Cloud from **EUR 5.49/mo** (Regular) / 5.99 (Cost-Optimized) excl. VAT, entry size only [V]; Hetzner GEX45 GPU **EUR 214/mo + EUR 209 setup** (RTX PRO 4000 24 GB, EU) [V]; RunPod RTX 4090 **$0.89/h**, L40S $1.09/h [V]; Lambda A10 **$1.29/h** [V]. AWS EC2 prices: **not verified**.

**Recommendation (CPU first):** a 4–8 vCPU / 16 GB CPU VM placed as close to us-east-1 as possible. Candidates: (a) Hetzner US East (Ashburn, VA, beside us-east-1) [ASSUMPTION: location exists and is priced near the EU plans]; (b) AWS EC2 in us-east-1. Test D9 picks one: run the same 50-frame fetch script from both for one hour each. **Rule: take the cheaper provider unless its p50 per-frame fetch time is >1.5x the EC2 time or its failure rate is >1 %.**

**Where a GPU pays, and where it does not:**
| Step | GPU? | Reason |
|---|---|---|
| TAP/S3/cutout fetch, FITS parse, WCS, JSON/binary encoding | No | I/O-bound; the data per request is MBs [V notes_server] |
| Per-frame detection + ePSF fits (~50 stars x ~500 frames) | Probably not | ~25k small fits; vectorised numpy on 8 cores is estimated at tens of seconds [ASSUMPTION; measured in S2] |
| Catalog linking, SkyBoT, scoring | No | Thousands of points, network latency [V notes_moving] |
| reproject `exact` stacks for a few hundred 100x100 windows | Marginal | CPU takes seconds |
| KBMOD-style shift-and-stack (C.13b) | **Yes** | Grid of (start px x velocity x frames); the GPU design does 1e10 trajectories/min [V arXiv 1901.02492] |
| Optional AI upscaling (E, level 3) | Yes | Only if kept at all |

**GPU trigger (measured, not guessed):** add a GPU only when, on the CPU VM after vectorisation, **either** (1) shift-and-stack p95 > 60 s per field over the 5 targets plus 10 random fields with ≥8 overlapping frames, **or** (2) the compute part of an uncached field has p95 > 120 s while fetch is <50 % of wall time, **or** (3) the queue wait p95 > 2 min under real traffic and the profile shows compute as the cause. First step after a trigger: an **on-demand** GPU worker (RunPod 4090 $0.89/h) that only takes C.13b jobs. A flat GEX45 (EUR 214/mo) is worth it only above ~240 GPU-h/month (214 EUR / 0.89 $ ≈ 240 h, ignoring the exchange rate) [arithmetic on verified prices].

### B.6 Rough monthly cost
| Item | Cost | Status |
|---|---|---|
| CPU VM | from EUR 5.49–5.99 (entry). A 4–8 vCPU plan costs more; **price not verified**, estimate EUR 15–40 [ASSUMPTION] | D9 confirms |
| Disk cache 100–200 GB | included or a few EUR [ASSUMPTION] | |
| Data egress from IRSA bucket | 0 [V] | |
| GPU on-demand, e.g. 20 h/mo | $18 (20 x $0.89) | [V price] |
| GPU always-on 4090 | ~$650 (730 x $0.89) — **not recommended** | [V price] |
| GPU flat GEX45 | EUR 214 + 209 setup | [V price] |
**Expected start: ~EUR 20–45/month, CPU only.**

### B.7 Deployment
Docker Compose (caddy, api, worker, redis) on one VM; `.env` holds the release and pipeline version; GitHub Actions builds the image, then SSH deploys it. A weekly cron re-warms the 5 targets and drops L2 entries from old pipeline versions. Logs: per-step timings (fetch/compute/serialize) go to a JSON log, which is what D12/the GPU trigger reads.

---

## C. End-to-end image pipeline

Conventions (v1 §2.2 still holds): 0-based internal pixels with integers at pixel centres; `p0 = p_FITS − 1`; always `all_pix2world(...,0)` / `all_world2pix(...,0, tolerance=1e-8, maxiter=50)`, never the AP/BP inverse alone or `wcs_*` (those ignore SIP [V]). The texture half-pixel offset `t = p0 + 0.5` lives in one function with a unit test.

| # | Step | Input → Output | Key method / formula | Failure handling |
|---|---|---|---|---|
| C.1 | **Query** | (ra, dec, fov, release) → frame list: s3 key, detector, MJD-AVG, provenance_version, footprint | TAP sync: `spherex.artifact JOIN spherex.plane ... CONTAINS(POINT, p.poly)` [V]; `cloud_access` column gives bucket/key [V]. Release filter: DR1+QR3 only (never mix QR1/QR2 [V]). Dedupe (obs id, detector), keep newest provenance | TAP >5 min timeout [V] → async TAP; empty → "no coverage" plus the date of the next possible pass |
| C.2 | **Fetch** | key + window → raw window HDUs + full headers | Primary (if D8 passes): `fits.open(s3://..., fsspec anon)`, headers, `.section[y0:y1,x0:x1]` for IMAGE/VARIANCE/ZODI, FLAGS tile-compressed section [NV]. Fallback: cutout service `?center=&size=&gzip=false` [V]. Two windows: **target window** (fov) and **astrometry window** (size from D7, e.g. 256²) | Retry/backoff; partial overlap → clipped window marked; NaN-pad edges, drawn hatched as "no data" |
| C.3 | **Ingest & pixel conventions** | headers → WCS objects, metadata | Celestial WCS from the IMAGE header (check `-SIP`, A_ORDER=3 — S0.3). Parent offset: for a cutout, `x_parent = 1 + x_cut − CRPIX1A` [V documented, behaviour NV → S0.4]; for an S3 window the offset is known exactly. Store parent coordinates for every pixel (needed for ePSF zone and λ). Reject FINAST≠0 (the archive already requires 0 [V]). λ at the target from CWAVE/CBAND (science) — WCS-WAVE only for display [V]. Survey = SPS_PA_ECL [V]. Roll angle from the PC matrix | Missing SIP → frame flagged "no distortion", correction step gets more freedom |
| C.4 | **Masking (Table 16)** | FLAGS → masks | **Fit mask** (doc photometry list [V]): bits 2,6,9,10,11,15,17,26,27,28,29 = `0x3C028E44`. **Background mask** = fit mask + bits 0,1,19,21 = `0x3C2A8E47` [V p.45]. **Our additions for centroiding:** mask OVERFLOW (1) and DICHROIC (7). **Caution flags on the measurement** (not masked by default, decided by D13): TRANSIENT 0, CROSSTALK 20, GHOST 22–24, STREAK 25. SOURCE (21) is never a defect. Display: nothing hidden; flag layer toggles | No bit exists for the 8° ghost or Moon stray light [V] → background-gradient check in C.5 and a per-frame "stray-light suspect" flag |
| C.5 | **Background / ZODI** | IMAGE, ZODI, VAR, bkg mask → D = IMAGE − ZODI − B | ZODI is not subtracted in IMAGE [V]. B = `sep.Background` (box ~32 px, bkg-masked) over the astrometry window. In PSF fits a local constant b is still free | Gradient > k·σ across the window → stray-light flag |
| C.6 | **Detection (whole astrometry window)** | D, VAR, mask → source list | Matched filter with the local ePSF resampled to native sampling; `sep.extract` thresh 5σ (σ = √VAR). Classes: astrometric stars = SNR>20, isolated (no neighbour within 3 px brighter than 10 % — same as the pipeline calibrator rule [V]), unflagged | <N_min stars (D7) → correction falls back to "header only" with a wider σ |
| C.7 | **ePSF centroiding** | stamps → (x, y, F, b), covariance, χ²_ν | Model `GriddedPSFModel` from the frame's EPSF HDU: grid_xypos = XCENTER/YCENTER, oversampling 5; scale so sum = 25 if photutils needs Σ = oversampling² [V photutils req; SPHEREx stores unit total flux [V] → S0.8 verifies]. QR3/DR1 only (QR1/QR2 x/y order bug [V]). Fit 5x5 (bright: 7x7), weights 1/VAR'. **VAR' = VAR·s²** with s = max(1, √χ²_ν of the population) (variance underestimates scatter [V p.44]). Σ = (JᵀWJ)⁻¹ over (x, y, F, b); σ_x = √Σ_xx. Iterative 5σ pixel clipping, at most 2 rounds. Saturated (OVERFLOW core): wing-only fit, marked "saturated-fit" | Non-convergence or χ²_ν > 5 → "bad fit", no position reported |
| C.7b | **Joint fit per pass** | all frames of one pass/detector for one source → (α, δ), per-frame F_k, b_k | Minimise Σ_k Σ_i w_ki (d_ki − F_k·P_k(p_i − W̃_k⁻¹(α, δ)) − b_k)², with W̃_k = corrected WCS (C.9). No resampling; each frame keeps its own ePSF and WCS. Optional (α₀, δ₀, μ_α*, μ_δ, ϖ) across passes (v1 §2.5 formula) | Frames with C.7 "bad fit" dropped; χ² outliers reported |
| C.8 | **Gaia match** | stars + frame epoch → matched pairs | Gaia DR3 cone over the astrometry window (server-side TAP, cached per HEALPix cell). Propagate to MJD-AVG (UTC; ±69 s vs TT is negligible): `apply_space_motion` + Earth-barycentre parallax term (v1 §2.5, unchanged). Exclude RUWE >1.4 [ASSUMPTION column check S0.7], G<9 (saturation), anything within 3 px of the user's target, and pm null | KD-tree match within 2 px, ambiguous pairs removed |
| C.9 | **Measured WCS correction** (standard) | matched pairs → correction T and Cov(T) | Δp = p_meas − W_raw⁻¹(Gaia_t). Fit Δp = t + (sR(θ) − I)(p − c) (4 params) or affine (6), chosen by held-out RMS (D6), robust (Huber, 3σ clip). σ_corr(p) from the parameter covariance. Store raw WCS, T, Cov(T), N, RMS, χ²_ν. All published positions: p_corr = T(p), with σ_tot² = σ_cent² + σ_corr²(p). UI badge: "WCS corr: 0.31 px shift, σ 0.008 px, N=42" | N < N_min or RMS > 0.3 px → "uncorrected" badge; frame still shown |
| C.10 | **Outliers / CR / transients** | per frame + across frames | **Already flagged by the pipeline:** TRANSIENT (≥~100 e⁻ onboard [V]), OUTLIER, SNOWBALL, HALO, STREAK (incomplete [V]), PERSIST. **We add:** (a) per-fit residual clipping (C.7); (b) shape test: sharpness and χ² vs ePSF → "not PSF-like" (single-pixel CR); (c) cross-frame persistence test (a detection repeating at the same *detector* pixel in consecutive frames = persistence/ghost); (d) astroscrappy **only as an extra mask, never replacing pixels**, away from Gaia/SOURCE stars, if D13 passes | Every rejected item is kept in the catalog with a reason code |
| C.11 | **Per-frame products** | → files | `img.f32` (D, target window), `var.f32`, `flg.u32`, `cat.json` (x, y, σ ellipse, F, SNR, flags, Gaia id, residual), `geom.json` (raw WCS header, T, Cov, roll, Mode-N/R transforms, r_max), meta (MJD-AVG, detector, λ at target, survey) | — |
| C.12 | **Pass grouping, stacks, differences** | frames → passes, stacks | Pass = MJD clusters split at gaps > 30 d [ASSUMPTION; set from the S0.5 histogram]. Stacks per detector per pass on the Mode-R grid with reproject `exact` (masked → NaN), inverse-variance weights; the λ list is shown with the stack. Difference = pass − pass, same detector **and** λ within one channel width (LVF [V]); no PSF matching (decided NOT). Badge "resampled — no astrometry" | Fewer than 2 frames → no stack |
| C.13 | **Moving-object candidates** | catalogs (+ images) → candidate tracks | Algorithm from notes_moving §3. (a) static removal: Gaia/2MASS match + recurrence within 1 px in ≥2 frames; (b) **catalog linking (CPU, primary)**: pairs in the allowed Δt → velocity in [v_min, v_max]; hypothesis grid with step s.t. Δv·T_total ≤ 1 px [V KBMOD grid logic]; RANSAC linear fit; accept ≥3 detections with residual < 1 px; 2 detections = "low-confidence tracklet". (b') **slow-mover mode** (WISE 0855 class): per-pass joint positions (C.7b) → μ fit across passes; flag sources with |μ| > 3σ that have no Gaia PM. (c) **shift-and-stack (C.13b, GPU candidate)** only if ≥8 overlapping frames within the pass: Mode-R grid, per-frame SNR weights (flux changes with λ [V LVF]), likelihood Σ(f/var)/√Σ(1/var), keep >7σ [V DEEP]. (d) scoring + false-track rate from time-scrambled runs | Fewer than 3 frames in a pass → linking off; this is reported |
| C.14 | **Known-object tagging** | candidates + epochs → labels | SkyBoT cone per frame epoch (observer 500 = geocentre; SPHEREx is in LEO → NEO parallax caveat [NV]); match radius max(3 px, ephemeris σ); `-filter` on position error [V]. Cache per (field, epoch). Link out to MOST (object → images [V]) | SkyBoT down → "untagged" label, job not blocked |
| C.15 | **Serialization** | → browser | `manifest.json` (schema v2: frames, modes, transforms, passes, links) + little-endian float32/u32 binaries, zstd at Caddy; overlays as JSON in **native float coordinates per frame**, transformed in the client with the same matrix used for the pixels | Schema version check in the client |

---

## D. Display modes and precision guarantees

Core fact: frames with different roll cannot show exact native pixels **and** be aligned on the sky in one view. So the viewer has modes, and the active mode and its guarantee are always shown.

| Mode | What is drawn | Guarantee | Typical use |
|---|---|---|---|
| **N — Native** | Each frame on its own detector grid, integer zoom z, texelFetch/NEAREST, **only rigid integer moves: shifts, 90°/180° rotations, flips** chosen to best line up with frame 0 | Every native px = exactly z×z screen px; a 1-px shift = exactly z screen px. **Residual misalignment** (leftover rotation θ_res, sub-pixel offset) is computed and shown, e.g. "θ_res 0.12° → ≤0.10 px at the window edge" | Default for frames from one survey (similar roll) and Survey 1 vs 2 (PA 0 vs 180 [V] = exact 180° flip) [ASSUMPTION: rolls within a survey differ by ≲1°; S0.5 measures] |
| **R — Sky-aligned, exact geometry** | Target TAN grid, north up, 1 display unit = 1 native px. Each native pixel drawn as its true rotated square: GPU affine map A per frame (v1 §2.3), NEAREST lookup per screen pixel | Values untouched. Pixel edges within ±0.5 screen px (= 0.5/z native px) + r_max (≤0.01 px target). A 1-px shift along the frame's own axis shows as a vector of length 1.000 native px in that frame's direction | Blink across different rolls, comparing passes |
| **R-k — server fallback** | Same as R, but a server k-oversampled NN raster (k=8) when A fails (r_max > 0.01) or the client lacks WebGL2 | Edge error ≤ 1/(2k) = 0.0625 px; values untouched | Fallback |
| **S — Resampled science view** | reproject `exact` stacks and differences | Flux-conserving, blurred, correlated noise. **No astrometry.** Banner shown | Stacks, differences, drizzle (E2) |

Overlays in all modes: centroids, Gaia, candidates are stored in native float coordinates and pushed through *the same* transform as the pixels, so markers and pixels cannot drift apart. Markers are never snapped to pixels.

**Showing 0.2 px honestly**
- Centroid = a cross at the float position plus a 1σ ellipse (2σ dashed). In a 64x zoom, 0.2 px = 12.8 screen px, which is clearly visible.
- Motion vector between epochs: drawn true-length, plus an optional scaled copy labelled "×10" in a different colour (never unlabelled).
- Readout: "Δ = 0.21 ± 0.03 px (1.29 ± 0.18"), 7.0σ, frames 12→31, Δt 183 d".
- Track panel: x(t), y(t) with error bars, with the Gaia-predicted line for the target.
- Below 1 screen px per native px: box-averaged overview labelled "overview, not exact".

**Error budget (position of a well-measured star, SNR ~100)**
| Term | Size | Source / status |
|---|---|---|
| Centroid statistics (Fisher) | ~0.01–0.03 px at SNR 100; ~0.1 px at SNR 10 | [ASSUMPTION scale]; measured T3 |
| ePSF model / pixel phase | target < 0.02 px; best case 0.002 px (Anderson & King) | [V A&K]; T2/T3 |
| ePSF zone interpolation + λ dependence | unknown | [NV] → D4/D5 |
| Header WCS (raw) | 0.016–0.065 px (0.1–0.4") | [V] |
| After measured correction (C.9) | target σ_corr ≤ 0.01 px at the target position | D6/D7 |
| Gaia propagation (G<17, 10 yr) | < 0.005 px | [ASSUMPTION] |
| Time stamp (UTC midpoint) | negligible (10"/yr x 60 s ~ 2e-5") | [V] |
| Display, Mode N | 0 | by construction, T-V1 |
| Display, Mode R | ≤ 0.5/z px + r_max | T-V2 |
| Display, Mode R-k | ≤ 0.0625 px (edges); markers 0 | T-V2 |

---

## E. Resolution enhancement: 3-level decision point (user has not chosen yet)

| Level | What | Real information? | Use for measurement? | Label |
|---|---|---|---|---|
| 1 | Native pixels, no smoothing (Modes N/R) | Yes, all of it | **Yes, the only source** | none |
| 2 | Drizzle-like combination of dithered frames from one pass, same detector, **λ within one channel** (PSF and flux change with λ [V]). Output scale 1/2 px, pixfrac ~0.6 | Yes, if ≥4 frames with spread sub-pixel phases/rolls. Gain must be measured: FWHM of injected stars vs native, noise correlation | **No** (Mode S rules) | "Combined from N frames (drizzle) — not for astrometry" |
| 3 | AI super-resolution | **No** — can invent sources and edges | Never | "AI-generated, cosmetic" — off by default |

**Recommendation:** build level 1 (required); prototype level 2 as a Stage 8 test and ship it only if test D15 shows a real FWHM gain ≥15 % with no artefacts in a human look; **drop level 3** — in a tool meant for spotting faint movers, a hallucinated dot is the worst possible failure. If the user still wants it (Q1), it ships off by default, watermarked, and never enters any computation.

---

## F. Technology decision tests

Tiers: **O** Opus, **S** Sonnet, **H** Haiku. "Human" = a user screenshot judgement is required (questions in I and G).

| ID | Decision | Candidates | Cheap test | Pass / fail | Runs | Cost | Human |
|---|---|---|---|---|---|---|---|
| **D1 / T-V1** | Viewer core | Canvas2D; WebGL2 texelFetch; WebGPU; Firefly (Docker); Aladin Lite v3; JS9; OpenSeadragon + server tiles; server PNG | **Synthetic checkerboard:** 64x64 FITS, 1-px checkerboard + bright px at (10,10); frame 2 = shifted exactly 1 px. Playwright screenshots at z = 1, 3, 7, 16.5 and DPR 1, 1.25, 2, Chrome + Firefox. Measure block widths and blink offset in device px | All blocks at integer device zoom = z device px exactly, **only 3 distinct pixel values** (no grey), blink offset = z. At non-integer device zoom: viewer must snap to integer or say so | S builds harness, H runs | ~3 h for custom candidates; Firefly/Aladin +2 h each | **Yes**: shimmer while panning, legibility |
| D1b | Library SIP accuracy | Firefly, Aladin | 5 star/corner pixels pix→sky vs astropy | Firefly < 0.01 px; Aladin < 0.1 px; else context-only | H | 1 h each | No |
| **D2 / T-V2** | Rotated-frame rendering | GPU affine NN (R); server k=8 NN (R-k); integer-rigid (N) | Synthetic rotated checkerboard at θ = 0.5°, 37°, 180°; compare drawn edges with analytic edges | R: ≤ 0.5 screen px + 0.01 native; R-k: ≤ 0.0625 px; N: exact at 180° | S | 3 h | **Yes**: which mode makes motion easiest to see (Q7) |
| D3 | Affine residual | — | r_max over 100 real windows of 50/100/200 px | ≤ 0.01 px for ≥99 % at default fov | H | 1 h | No |
| **D4** | Centroiding | GriddedPSFModel ePSF fit; single-zone ePSF; SEP winpos; Gaussian; joint fit | T2 ladder 0.1…0.9 px; T3 2000 injected stars on real noise; real Gaia residuals | ePSF: \|bias(phase)\| < 0.02 px at SNR>50; RMS/σ_pred ∈ [0.8, 1.25]. Choose simplest passing | O designs, S codes | 1 day | No |
| D5 | ePSF handling | Normalisation ×1 vs ×25; x/y order; in-file vs cal-file ePSF | Fit ePSF to itself at known offsets; transposed-ePSF χ² on 200 real stars; byte compare | Self-recovery < 0.001 px; correct orientation gives clearly lower χ² | S | 2 h | No |
| **D6** | WCS correction model | none / shift / similarity / affine / +poly2 | Fit on 70 % of Gaia stars, held-out RMS on 30 %, 50 frames | Take the more complex model only if held-out RMS improves ≥10 % | O reviews, S codes | 3 h | No |
| D7 | Astrometry window | 128², 256², 512², full frame | N matched stars and σ_corr at all 5 targets (R Dra high latitude = sparse) | Smallest window with σ_corr ≤ 0.01 px and N ≥ 20 | S | 2 h | No |
| **D8** | Fetch method | S3 byte-range `.section`; cutout service | 50 frames: bytes on the wire (log GET ranges), p50/p95 latency, failures, FLAGS (compressed) section works | S3 wins if bytes ≤ 2x (window + headers) and p50 < 1 s/frame | S | 2 h | No |
| **D9** | Provider/region | Hetzner US-East; AWS EC2 us-east-1; Hetzner EU | Run the D8 script from each, 1 h rental each | Cheapest within 1.5x EC2 p50 and <1 % failures | S | ~3 h + < EUR 5 | No |
| D10 | Stacking unit | per detector per pass; per channel (λ-matched) | Static-star residuals in differences; SNR of ε Indi B / WISE 0855 | Lower median residual at ≥ equal SNR wins | S | 3 h | **Yes**: artefacts acceptable? |
| **D11** | Moving-object method | catalog linking; + shift-and-stack; KBMOD package | Inject synthetic linear movers into real frame sets (fields with ≈4 and ≥8 frames); time-scrambled runs; 1 real SkyBoT asteroid | Linking: ≥90 % completeness at per-frame SNR ≥ 7, ≤0.1 false tracks/field; S&S must add ≥1 mag depth to be kept | O designs, S codes | 1.5 days | **Yes**: candidate blink strips look real? |
| D12 | GPU | CPU only; on-demand GPU worker | Per-step timings on CPU VM (B.5 trigger) | Trigger rules in B.5 | H collects, O decides | free (logs) | No |
| D13 | Extra CR / flag masking | none; residual clipping; astroscrappy-as-mask; mask GHOST/STREAK/TRANSIENT | Injection: star-core loss rate; centroid bias with/without | Core loss < 1 %, no added bias > 0.005 px | S | 3 h | No |
| D14 | Transport format | float32+zstd; float16; 8-bit PNG | Size and load time for 500 frames of 64² | float32 unless > 2x slower than float16 | H | 1 h | No |
| D15 | Resolution level 2 | drizzle (pixfrac 0.6, scale 0.5); none | Injected stars: FWHM gain, artefacts | Gain ≥ 15 % | S | 4 h | **Yes** (Q1) |
| D16 | Stretch default | asinh; linear; zscale | Screenshot set of 3 targets | user picks | H | 30 min | **Yes** (Q7) |

---

## G. Stages

Rules: each sub-agent gets a narrow brief, writes one named file, and closes (spawn → finish → close). Opus reads only summaries and diffs. Approximate token share: O 20 %, S 65 %, H 15 %.

### Stage 0 — Verify the unverified + cheap tests (≈1.5 days)
| # | Task | Tier |
|---|---|---|
| S0.1 | CORS re-check is no longer needed (server-side). Instead: full TAP query for the 5 targets → frames per detector/survey/release | S |
| S0.2 | **S3 byte-range read** (D8): log GET ranges for header + IMAGE section + FLAGS compressed section | S |
| S0.3 | **SIP present in the real IMAGE HDU** (CTYPE `-SIP`, A_ORDER=3) for 20 frames + cutout headers keep SIP | H |
| S0.4 | **Cutout parent-pixel rule:** two overlapping cutouts + the S3 window of the same frame → same star, same parent pixel within 1e-6 | S |
| S0.5 | **Visits per sky position:** MJD histogram per target → passes, frames per pass per detector, roll spread within a pass (feeds Mode N assumption and the 30 d gap rule) | S |
| S0.6 | **WISE 0855 detectability:** forced ePSF photometry at the predicted position in D5/D6 frames and a quick stack; report SNR per frame and per pass | S (O reviews) |
| S0.7 | Gaia columns (ref_epoch, RUWE, pm) for all 5 targets; literature μ for WISE 0855 / ε Indi B if Gaia is missing | H |
| S0.8 | ePSF normalisation and orientation (D5) | S |
| S0.9 | In-file ePSF vs calibration file identical? (cache L1b) | H |
| S0.10 | D1 checkerboard harness on Canvas2D + WebGL2 (+ WebGPU if cheap) | S build / H run |
| S0.11 | D9 provider timing (two 1-h rentals) | S |
| S0.12 | Gate review: update risks, freeze manifest schema v2 | O |
Parallel: everything except S0.12. **Demo:** coverage table + one real window with its pixel grid + checkerboard screenshots. **Acceptance:** table lists N frames / detector / pass for Barnard, ε Indi B, WISE 0855, RW Aur, R Dra (0 allowed but stated); each item above is marked V / false / still unknown. **Human:** checkerboard screenshots (Q-H1 below).

### Stage 1 — Server skeleton + ingest + Mode N blink (≈1.5 days)
FastAPI/RQ/Redis/Caddy compose **S**; fetcher with politeness + L0/L1 cache **S**; pixel-convention module + tests **O** (small) → **S**; viewer per D1 winner, Mode N, integer zoom, grid overlay, blink, progressive loading **S**. Parallel: server ‖ viewer against schema v2.
Demo: type Barnard's coordinates → frames start blinking in native mode. Acceptance: T-V1 passes in the real viewer; first frame on screen < 30 s uncached [ASSUMPTION target], full field < 3 min; 0 duplicate IRSA requests in the log.

### Stage 2 — Precision core (≈2 days, Opus-heavy design)
ePSF model + fitter + joint-fit design **O**; implementation **S**; injection harness T1–T4 **S**; D13 **S**; review **O**.
Demo: bias-vs-phase plot, RMS/σ_pred plot. Acceptance: T1 Δ = 1.000 ± 0.005 px (bright); T2 \|bias\| < 0.02 px at SNR>50; T3 ratio in [0.8, 1.25]; T4 round trip < 1e-4 px. CPU timing per frame is logged.

### Stage 3 — Gaia match + measured WCS correction + motion fits (≈1.5 days)
C.8/C.9 **S** (O reviews math); D6/D7 **S**; motion fit (v1 §2.5) **S**.
Demo: per-frame correction badges; Barnard's track with Gaia line. Acceptance: ≥95 % of Gaia stars within 3σ_tot after correction; held-out RMS per frame reported; **Barnard μ** within 3σ and 10 % of Gaia (if saturation allows; else a wing-fit note); **ε Indi B** μ within 3σ of the literature value.

### Stage 4 — Display modes R / R-k + overlays + sub-pixel presentation (≈1.5 days)
GPU affine path + r_max **S**; server R-k fallback **S**; overlays in shared transform, ellipses, scaled vectors, readout, track panel **S**; T-V2/D3 **H**.
Demo: Barnard in Mode N and Mode R side by side. Acceptance: T-V2 thresholds; cursor readout = astropy within 1e-3 px; a synthetic 0.2 px shift shows as 0.2 ± 0.01 px on the overlay at z = 16 and 64. **Human:** Q7.

### Stage 5 — Passes, stacks, differences, slow-mover mode (≈1.5 days)
C.12 **S**; D10 **S**; C.13 b' slow-mover **S** (O sets thresholds).
Demo: pass blink for ε Indi B and WISE 0855. Acceptance: blank-sky stack noise within 20 % of (Σ1/σᵢ²)^-½; static-star residual median < 3σ in differences; **WISE 0855**: detected or not, stated with SNR; if detected in ≥2 passes, measured Δ vs prediction within 3σ.

### Stage 6 — Moving-object finder + SkyBoT (≈2 days)
C.13 a/b/c/d **S** from an **O** design; C.14 **S**; D11 **S**; D12 timing **H**; GPU decision **O**.
Demo: a field with a known asteroid; its track found and labelled by SkyBoT. Acceptance: D11 thresholds; every candidate has a reason/score; time-scrambled false-track rate printed.

### Stage 7 — Spectra/variables + product hardening (≈1.5 days)
Forced photometry at joint positions, CWAVE/CBAND **S**; λ-binned light curves **S**; URL schema (v1 list + `mode=N|R|S`, `vecscale`) **S**; per-IP limits, monitoring, warm cache cron, deploy **S/H**; README **H**.
Demo: public URL; 5 target links. Acceptance: **RW Aur** and **R Dra** spectra continuous across detector edges within 3σ for a non-variable control star; R Dra pass-to-pass change reported with σ; all 5 links render warm in < 3 s; a reloaded URL reproduces the state exactly.

### Stage 8 — Gate review + honesty report + level-2 test (≈1 day)
Diff-only code and maths review **O**; full test run + numbers **H**; D15 drizzle prototype **S** (only if Q1 allows). Deliverable `STATUS.md`: done / partial / not done, with numbers.

**Total ≈ 14 working days.** Cut order if short: Stage 8 level-2 test → Stage 7 spectra → shift-and-stack part of Stage 6.

**Human-in-the-loop screenshot questions** (answered by the user at the gates):
- Q-H1 (S0): "In these checkerboard images at zoom 3, 7 and 16.5, do you see any grey, blurred, or unevenly wide squares? (yes/no per image)"
- Q-H2 (S4): "Barnard in Mode N and Mode R: in which is the star's step easier to see? Does the rotated-square look of Mode R bother you?"
- Q-H3 (S4): "Is a ×10 scaled vector next to the true one clear, or confusing?"
- Q-H4 (S5): "In these difference images, are the leftover star residuals acceptable, or do they hide the target?"
- Q-H5 (S6): "For these 5 candidate blink strips, which look like real moving dots?" (also gives a small ground-truth set)

---

## H. Risk register (updated)

| # | Risk / unknown | Impact | Cheap test / mitigation |
|---|---|---|---|
| R1 | S3 byte-range / compressed FLAGS section does not work [NV] | Fall back to ~4 MB cutouts, ~2 GB per target [ASSUMPTION ~500 frames] | S0.2/D8; cutout fallback + L1 cache |
| R2 | Cutout parent-pixel rule wrong [NV] | Wrong ePSF zone / λ; wrong grid offsets | S0.4 |
| R3 | Visits per position per pass not stated [V absent]; few passes per target | Weak PM, linking impossible in some fields | S0.5; report N per field in UI |
| R4 | WISE 0855 too faint in D5/D6 | Target not shown | S0.6; honest report |
| R5 | Bright targets saturate (Barnard, R Dra, RW Aur: OVERFLOW/NONLINEAR) | Biased centroids | wing fit; "saturated-fit" badge; Stage 3 note |
| R6 | ε Indi Ba/Bb unresolved; nearby bright ε Indi A ghosts | Blend, false offsets | State in UI; GHOST caution flags |
| R7 | λ changes per frame (LVF) → flux and PSF changes, chromatic centroid shift | False variability or motion | Per-zone ePSF; λ shown per frame; λ-matched differences |
| R8 | ePSF interpolation in λ not specified [V absent] | Systematic centroid error | D4/D5; empirical bias curve |
| R9 | **Closed:** ePSF 5x, 33x33 | — | — |
| R10 | Affine map insufficient | Edge error in Mode R | D3; R-k fallback |
| R11 | Pixel-phase bias | sub-pixel bias | T2/T3 |
| R12 | Too few Gaia stars at high latitude for correction | Larger σ_corr | D7 larger window; "header only" badge |
| R13 | Correction circularity: target or unknown movers in the fit | Biased correction | exclude target ±3 px; robust fit |
| R14 | Flags incomplete (streaks, crosstalk, bloom before 2025W51) [V] | False candidates | C.10 own tests; candidate reason codes |
| R15 | No flag for 8° ghost / Moon stray light [V] | Background errors | gradient check C.5 |
| R16 | Hidden IRSA throttling; public traffic spikes | Failed jobs, IRSA complaints | semaphore 4, per-IP limit, helpdesk contact, warm cache |
| R17 | Hetzner US region missing or pricier [ASSUMPTION] | Cost | D9 picks EC2 instead |
| R18 | CPU too slow for uncached fields | Bad UX | B.5 trigger; progressive results |
| R19 | SkyBoT ephemeris errors large; LEO parallax for NEOs [V/NV] | Wrong tags | ephemeris-σ match radius; "probable" wording |
| R20 | Release reprocessing changes frames | Stale cache | key by release + pipeline version; dedupe provenance |
| R21 | AI upscaling (if kept) misleads users | Credibility | off by default, watermark, never measured |

**Decided NOT to do:** Pyodide/in-browser astropy; astrometry on any resampled image; bilinear/bicubic display; re-solving WCS from scratch (only the measured correction); PSF-matched difference imaging; our own HiPS; all-sky automatic discovery (per-field only); MPC reporting; accounts/auth; full-file (hundreds of MB) downloads as the normal path; always-on GPU before the trigger; mixing QR1/QR2 with QR3/DR1; using WCS-WAVE for science λ.

---

## I. Questions for the user (one line each)

1. **AI upscaling (E, level 3): drop it, or keep it off by default and labelled?** → changes whether a GPU model and a cosmetic layer are built. (Recommendation: drop.)
2. **Monthly budget cap (e.g. EUR 30 / 100 / 300)?** → sets CPU size and whether an on-demand GPU is allowed after the trigger.
3. **Provider preference or restriction (AWS ok? Hetzner ok? other)?** → limits the D9 candidates.
4. **Region constraint, or is "closest to us-east-1" fine?** → VM location.
5. **Is public traffic expected (rough users/day), or demo/jury only?** → politeness limits, the IRSA email, queue size, warm-cache scope.
6. **Which 2 targets matter most for the demo?** → order of Stage 3–5 acceptance work (default: Barnard + WISE 0855).
7. **Visual preference after screenshots: default mode N or R, stretch asinh/linear/zscale, light or dark?** → viewer defaults (answered via Q-H1–H3).
8. **Is drizzle-like level 2 worth one day if it gives a real but labelled ~15 % sharper look?** → Stage 8 scope.

---

## J. First 3 actions

1. **Spawn Stage 0 sub-agents in parallel (spawn → finish → close):** H: S0.3, S0.7, S0.9. S: S0.1+S0.5 (coverage and visits), S0.2+S0.4 (S3 range read and parent rule, one script), S0.6, S0.8, S0.10 (checkerboard harness). Each writes `stage0/s0_<id>.md` with [V]/[NV] tags and raw numbers.
2. **Opus writes manifest schema v2 + the pixel-convention / transform spec** (Modes N, R, R-k; overlay transform shared with pixels) while Stage 0 runs, so Stage 1 can start as soon as the gate passes.
3. **Gate:** after S0.11 (provider timing), Opus reads only the summaries, updates sections B.5 and H, and sends the user the coverage table, checkerboard screenshots (Q-H1) and questions I.1–I.6 in one message. Stage 1 starts after the user answers.
