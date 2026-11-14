# SPHEREx Blink: staged implementation plan

Tags: **[V]** = verified in the research notes (page read or live curl test). **[NV]** = marked not verified in the notes. **[ASSUMPTION]** = added by me in this plan and not checked. Rule: anything [NV] or [ASSUMPTION] counts as **not done / not known** until a task in Stage 0 or a later acceptance test closes it.

---

## 1. Architecture decision

| Option | How it works | Cost | Accuracy | CORS | Hackathon fit |
|---|---|---|---|---|---|
| **A. Offline Python precompute + static site** | Python (astropy, photutils) queries IRSA TAP, fetches cutouts, fits centroids and writes per-frame float32 binaries plus a JSON manifest. The static WebGL viewer reads those files. | Free hosting (GitHub Pages / Cloudflare Pages [ASSUMPTION: limits fine for a few hundred MB]) | Best: full astropy SIP, ePSF fitting | Not an issue (no browser calls to IRSA, Gaia or MAST) [V: those services send no ACAO header] | High. Main limit: only precomputed targets |
| B. Live Python backend (FastAPI on a VM or PaaS) | The same pipeline runs per request and caches results | Paid or sleeping free tiers. HF Docker needs PRO [V]. CF Workers too small [V] | Same as A | Server-side, so fine | Medium. Cold starts, plus about 4 MB per cutout x hundreds of frames per target (see R3) |
| C. Pyodide in the browser | astropy runs in WASM, with a CORS proxy for data | Proxy needed anyway | Poor: photutils and reproject are not in Pyodide [V] | Needs a proxy | Low |

**Recommendation: A first, with B-lite later from the same code.** One Python package (`spxblink`) writes a **versioned manifest schema**. The static frontend only ever reads that manifest. Stage 6 adds an optional `spxblink serve` (FastAPI) that writes the same manifest for any RA/Dec. It runs locally or on a cheap VM, and the demo does not depend on it. Weekly updates run as a scheduled job (GitHub Actions cron [ASSUMPTION: free for public repos]) that re-runs ingest for the curated targets.

Frontend: a custom **WebGL2 viewer** for pixel-exact rendering: R32F textures, `NEAREST`, no mipmaps, stretch in the shader. **Aladin Lite v3** goes in a side panel for sky context (HiPS, catalogs) only. Its SIP and nearest-neighbour behaviour are [NV], so it never draws the precision view.

---

## 2. Precision design (sub-pixel truth)

### 2.1 Principle
**Positions are measured only on native, un-resampled pixels, and they are mapped to the screen analytically.** A resampled image (stack, difference) is only for looking. It carries a "resampled: no astrometry" badge.

### 2.2 Coordinate conventions (one rule everywhere)
- Internal pixel coordinates are **0-based, with integer values at pixel centres**. Pixel *i* covers [i-0.5, i+0.5]. FITS is 1-based: `p0 = p_FITS - 1`.
- astropy: always `wcs.all_pix2world(x, y, 0)` and `wcs.all_world2pix(ra, dec, 0, tolerance=1e-8, maxiter=50)`. Never rely on the SIP inverse (AP/BP) polynomials alone, because they are approximations.
- Cutout to parent: the notes say `x_orig = 1 + x_cut - CRPIX1A` (0-based) [V as documented, behaviour NV]. Stage 0 test S0.6 checks it.
- WebGL texel *i* covers [i, i+1], so a native coordinate maps to texture space as `t = p0 + 0.5`. That half-pixel offset lives in exactly one function, which has a unit test.
- Display frame: a gnomonic (TAN) plane centred on the target (α0, δ0), north up, east left, scale s = 6.15"/px, so **1 display unit = 1 native pixel**.
  ξ = cosδ·sin(α-α0)/D, η = (sinδ·cosδ0 - cosδ·sinδ0·cos(α-α0))/D, D = sinδ·sinδ0 + cosδ·cosδ0·cos(α-α0); u = -ξ/s, v = η/s.

### 2.3 Rendering native frames without interpolation
Each frame has its own roll angle. To blink frames in one display frame:
1. Over the cutout's native pixel grid, compute (u, v) exactly through SIP WCS → sky → TAN.
2. Fit a **local affine map** A (2x3) by least squares, (x0, y0) → (u, v). Record the residual `r_max = max |A·p - (u,v)_exact|`.
3. If `r_max ≤ 0.01 px`, render the native texture through A with NEAREST sampling. Every native pixel appears as its true rotated square at any zoom, with values untouched. [ASSUMPTION: SIP is nearly affine over a few arcminutes. Stage 3 measures it.]
4. Otherwise, fall back to **k-oversampled nearest-neighbour**. Build a fine grid (k = 8) in Python, each fine cell taking the value of the native pixel that contains its centre (computed with the exact WCS). Edge error is ≤ 1/(2k) = 0.0625 px, and values stay untouched.
5. Zoom: integer zoom steps by default. Below 1 display px per native px, show a box-averaged overview with an "overview, not exact" label. Overlays (zoom ≥ 8): the frame's **own native pixel grid** as rotated lines, plus an optional sky grid in arcseconds.

**Error budget (display position of pixel edges and markers)**

| Path | Position error | Value fidelity | Use |
|---|---|---|---|
| Native + affine, NEAREST | r_max (target ≤ 0.01 px) + float32 GPU error ~1e-5 px | exact | blink default |
| k = 8 oversampled NN | ≤ 0.0625 px at edges, 0 for markers (drawn analytically) | exact | fallback |
| Bilinear or `interp` reprojection | centroid bias that depends on pixel phase (undersampled PSF) [ASSUMPTION: up to ~0.1 px] | smoothed | **never** |
| reproject `exact` / `adaptive` (flux-conserving) | small. Correlated noise and pixel-kernel blur [V: "not flux conserving" applies only to interp] | blurred | stack and difference display only |
| WCS absolute accuracy | unknown → measured against Gaia (2.6) | n/a | reported per frame |

Markers (centroids, Gaia) are drawn as vectors at float positions, never snapped to pixels.

### 2.4 Detection and centroiding
- Detection: photutils `DAOStarFinder` or `find_peaks` on IMAGE minus local background (or minus ZODI), threshold 5σ using sqrt(VARIANCE). Masked FLAGS bits are decided in S0.2. **SOURCE (bit 21) is never masked** [V].
- Centroid: **ePSF fit**. Take the EPSF zone nearest the source (21x21 zones, ~97 px each [V]). Fit `photutils.psf` ImagePSF / PSFPhotometry with free parameters (x, y, flux, local background), weights 1/VARIANCE, flagged pixels masked, fit box 5x5 to 7x7 native px. The oversampling of the EPSF HDU must be read from the header. The notes conflict: "oversample 5, 33x33" vs "0.615"/pix = 10x" (S0.5).
- Why not centre of light or Gaussian fit: centre of light never reaches the Cramér-Rao bound, and a Gaussian fit has up to 8/(3√3) times the ePSF-fit variance [V: arXiv 1610.05873, 2004.06253 snippet]. SPHEREx is undersampled, so a known PSF matters most.
- Expected error [ASSUMPTION: textbook, Gaussian approximation]: source-limited σ_x ≈ σ_PSF/√N_e. Background-limited σ_x ≈ √(8π)·σ_PSF²·σ_bg/F (pixel units). In practice σ comes from the fit covariance, scaled by √χ²_ν when χ²_ν > 1, then multiplied by an empirical factor c_inj from injection tests.
- **Joint (forward-model) fit per survey pass:** one sky position (α, δ) shared by all native frames of a pass and detector (optionally all detectors), with a separate flux per frame. Each frame contributes through its own WCS and its own ePSF. This gives a stacked-S/N position **without resampling**. Opus designs it and Sonnet implements it.

### 2.5 Proper motion, parallax, epoch
Gaia DR3: ref_epoch = J2016.0 [NV in notes, Stage 0 checks the column]. For each frame epoch t (frame MJD from `time_bounds`; the time scale is [NV] but negligible: 69 s x 10"/yr ≈ 2e-5"):
1. Space motion: `SkyCoord(ra, dec, distance=1/ϖ, pm_ra_cosdec, pm_dec, radial_velocity=rv or 0, obstime=J2016.0).apply_space_motion(new_obstime=t)`. If ϖ ≤ 0 or ϖ/σ_ϖ < 5: linear PM only, no distance. If pm is null: static.
2. Observer parallax (Earth barycentre; the LEO offset of SPHEREx changes it by < 1e-4 of ϖ [ASSUMPTION]), with X, Y, Z = Earth barycentric position in AU from `get_body_barycentric('earth', t)`:
   Δα* = ϖ(X·sinα - Y·cosα), Δδ = ϖ(X·sinδ·cosα + Y·sinδ·sinα - Z·cosδ)
3. **No aberration.** I assume the SPHEREx WCS is tied to astrometric (catalog-frame) positions [ASSUMPTION; if wrong, the Gaia check shows systematic offsets up to ~20" ≈ 3 px]. Stage 2 tests this explicitly.
4. Motion fit for a target: weighted least squares on the per-epoch positions, p(t) = p0 + μ·(t - t0) + ϖ·P(t), where P holds the parallax factors above. Report μ ± σ_μ and ϖ ± σ_ϖ (ϖ is only meaningful with ≥ 3 passes).

Scale check against Gaia/SIMBAD values [ASSUMPTION, resolved in S0.4]. Barnard's Star: μ ≈ 10.4"/yr = 1.69 px/yr, ϖ = 0.55" = 0.09 px. WISE 0855: μ ≈ 8.1"/yr = 1.3 px/yr. ε Indi B: μ ≈ 4.7"/yr = 0.77 px/yr. Over a ~1.5 yr baseline that is 2.5 / 2.0 / 1.1 px.

### 2.6 Empirical validation (the "tune the output" loop)
| Test | Method | Acceptance |
|---|---|---|
| T1 synthetic integer shift | Real native cutout plus an ePSF star injected at (x, y) and at (x+1, y). Separately, `np.roll` by exactly 1 px | measured Δ = 1.000 ± 0.005 px (bright). Playwright screenshot: displacement = exactly z screen px at z = 1, 4, 16, 64 (0 px tolerance) |
| T2 sub-pixel ladder | Shifts 0.1…0.9 px | \|bias\| < 0.02 px at SNR > 50 |
| T3 injection/recovery | 2000 ePSF stars, random phase and flux, real VARIANCE noise | bias vs pixel phase < 0.02 px. RMS / predicted σ = c_inj within 0.8–1.25. Completeness curve vs SNR |
| T4 WCS round trip | pix → world → pix over the cutout | < 1e-4 px |
| T5 Gaia astrometry | Isolated, non-variable Gaia stars (G < 17, RUWE < 1.4 [ASSUMPTION: column present]), propagated as in 2.5, compared with fitted centroids | report median offset and RMS per frame. Pass if the RMS of normalised residuals is 0.8–1.5. If a coherent offset > 3σ: apply a per-frame Gaia **WCS refinement** (shift + rotation + scale), keep the raw values, display both |
| T6 known mover | Barnard's Star fitted μ vs Gaia μ | agreement within 3σ_μ and within 10 % |

Shown to the user: a 1σ error ellipse on each centroid. The readout "Δ = 1.02 ± 0.03 px (6.27 ± 0.18") between frames i and j, 34σ". A per-frame astrometric quality badge (Gaia RMS). A banner whenever the view is resampled.

---

## 3. Features → stages

| Feature | Stage | Note |
|---|---|---|
| Blink viewer (native, NN, pixel grid) | 1 (raw), 3 (affine-exact) | frame list, play/pause, speed, step, restart border (WiseView idea) |
| FOV selection | 1 | 1'–20' cutouts, default 5' (~49 px) |
| Centroids + error ellipses | 2–3 | from native pixels |
| Gaia overlay, epoch-propagated + PM trail + parallax | 3 | precomputed per frame by the pipeline (no browser CORS) |
| Flags layer | 3 | bitmask toggles, names from S0.2 |
| Per-detector stacking per pass | 4 | inverse-variance weighted, reproject `exact`. Position comes from the joint fit (2.4), not the stack |
| Difference imaging | 4 | frame − pass-median, or pass − pass, same detector and similar λ |
| Spectra from clicked source | 5 | forced ePSF photometry in every frame. λ from WCS key W / CWAVE [V] |
| Variable-star mode | 5 | light curve per λ bin. Never blink raw brightness across different λ without a label |
| URL params / embed | 6 | schema below |
| Weekly update path | 6 | cron: TAP `time_bounds_lower > last_mjd`. Dedupe on (obs id, detector), keep newest `provenance_version` |
| Aladin Lite context panel, external links | 6 | SIMBAD/VizieR/Legacy links |

**URL schema** (query string, kept in sync with `history.replaceState`; also accepted after `#` for WiseView-style links):
`ra, dec` (deg or sexagesimal) · `target` (name, resolved at build time) · `fov` (arcsec) · `det` (1–6, comma list, or `all`) · `mode` (`frames|pass|stack|diff`) · `diffref` (`median|p0|p1…`) · `frame` (index) · `speed` (ms) · `zoom` (int) · `stretch` (`asinh|linear`) · `lo, hi` (percentiles) · `invert` (0/1) · `grid` (0/1) · `gaia` (0/1) · `cen` (0/1 centroids) · `flags` (int bitmask shown) · `wl, dwl` (µm centre/tolerance filter) · `release` (`latest|dr1|qr3`) · `embed` (0/1 hides chrome).
Example: `?target=barnard&det=all&mode=pass&zoom=16&grid=1&gaia=1`.

---

## 3b. Known problems and decision points (pick option by option)

Common pitfalls in similar projects (each one is mapped to the choices below):
- **P1** WCS/SIP mismatch: a tool ignores SIP, or uses the approximate AP/BP inverse.
- **P2** Half-pixel and 0/1-based offsets.
- **P3** Flux not conserved, or blurring, when resampling.
- **P4** Edge, NaN and flag handling: clipped cutouts, masked pixels poisoning stacks.
- **P5** Huge cutouts or files.
- **P6** Epoch gaps or uneven passes.
- **P7** Scattered light, zodi, ghost and halo artefacts.
- **P8** Saturated or nonlinear bright variable stars.
- **P9** Gaia epoch propagation errors: wrong ref epoch, pmra already includes cosδ, parallax ignored, null pm/ϖ.

| Choice | Options | Likely problems | **Recommendation**: reason |
|---|---|---|---|
| Viewer | Aladin Lite v3 / custom WebGL2 / JS9 | Aladin: SIP and NN-at-zoom [NV] (P1, P2). Built for HiPS context, not for frame blinking. Custom: we own P2 (half-pixel), more code. JS9: archived 2022, no maintainer [V] | **Custom WebGL2 for frames + Aladin as side panel**: the only option where pixel exactness is ours to test and guarantee |
| Processing | Precompute + static / live backend / Pyodide | Precompute: only curated targets, P5 at build time. Live: cold starts, P5 per request, cost. Pyodide: no photutils/reproject [V], P5 in the browser | **Precompute + static (optional local serve later)**: cheapest, most accurate, no CORS |
| Resampling for blink | Native + affine NN / common grid via `interp` / `adaptive` / `exact` | interp: not flux-conserving and blurs, phase-dependent centroid bias (P3) [V/ASSUMPTION]. adaptive/exact: correlated noise, blur, slow; `exact` precision warning < 0.05" [V]. Native: needs P1/P2 discipline, affine residual (R10) | **Native pixels + local affine NN (k-oversampled NN fallback)**: values untouched, edge error ≤ 0.01–0.06 px |
| Resampling for stack/diff | interp / adaptive / exact | as above, plus P4 (NaN/flag holes spread under any kernel) | **`exact` (or `adaptive` with conserve_flux), display-only badge**: flux-conserving. Never used for positions |
| Centroiding | Centre of light / Gaussian fit / DAOFIND-style / ePSF fit / joint multi-frame ePSF fit | CoL: never reaches CRLB [V]. Gaussian: up to 1.54x variance [V snippet], biased on undersampled PSF. ePSF: oversampling conflict (R9), PSF varies per zone, P8 saturation, P7 ghosts flagged as sources | **Per-zone ePSF fit, plus joint fit per pass**: best precision without resampling |
| Hosting | GitHub Pages / Cloudflare Pages / HF static Space / VM | file-count/size limits [NV] (CF 20k files secondary source). VM costs money | **GitHub or Cloudflare Pages**: free. Few small binaries per target [ASSUMPTION: limits fit] |
| CORS proxy | none (precompute) / Cloudflare Worker / own backend | Worker: 10 ms CPU, 128 MB [V], fine for pass-through but adds abuse/rate risk to IRSA. Backend: cost | **None needed with precompute**. Worker pass-through only if live mode is ever required |
| Stacking unit | per detector (6) / per narrow λ band (102 ch) / all detectors | per detector: mixes λ within the LVF range → SED-dependent blending (R7). Per band: few frames per band per pass, low S/N, P6 gaps. All: mixes PSFs and SEDs | **Per detector per pass, with frame λ list shown; per-band option in spectra mode**: matches the challenge's request and gives usable S/N |
| Variable stars | blink raw / λ-binned light curves | raw blink conflates λ and time (R7), P8 saturation | **λ-binned light curves + saturation flags shown** |
| Gaia propagation | linear PM / full space motion + parallax | P9; WiseView uses the 2015.5 epoch with DR3 [V], a ~0.5 yr error | **astropy `apply_space_motion` + explicit parallax term (2.5)**: correct for high-PM nearby stars |
| Edges/flags | NaN-fill / mask by bitmask / ignore | P4: clipped cutouts at array edges, SOURCE bit on most pixels [V] | **Mask a configurable bit set from S0.2, never SOURCE; edges drawn as hatched "no data"** |
| Zodi | ignore / subtract ZODI HDU / local background | P7: big gradients across the LVF. ZODI is not subtracted in IMAGE [V] | **Subtract ZODI for display, fit local background in PSF fits** |

**Cost note:** the cheapest path in both money and model tokens is precompute + static hosting + no proxy + custom viewer, with Sonnet writing the code. Live backend and Pyodide add hosting cost or debugging time. The ePSF and joint-fit work is the one place where Opus time is worth paying for. Everything else (fetching, viewer, URL, deploy) is Sonnet or Haiku work.

---

## 4. Stages

Tiers: **O** = Opus (architecture, hard math, gate reviews), **S** = Sonnet sub-agent, **H** = Haiku sub-agent. Every sub-agent is spawned with a narrow brief, writes to a named file, and closes. Opus only sees summaries. Rough token share: O ~25 %, S ~60 %, H ~15 %. Opus never reads web pages or writes boilerplate.

### Stage 0: Verify the unverified (≈ 0.5 day)
Goal: turn each [NV] item into verified, false or still-unknown. Deliverable: `stage0_report.md` with a target coverage table, plus one real cutout plotted with its pixel grid.
| # | Task | Tier |
|---|---|---|
| S0.1 | CORS: full response headers (grep ACAO) for IRSA TAP/SIA/cutout and Gaia TAP; also VizieR/SIMBAD TAP | H |
| S0.2 | Flag bits: read Explanatory Supplement Table 16 → `flags.json` (bit, name, meaning, "bad for photometry?") | S (PDF accuracy matters) |
| S0.3 | Coverage: TAP query for each of the 5 targets → frames per detector, MJD clustering into passes, releases present. Also check QR2 rows | S |
| S0.4 | Target coordinates + Gaia DR3 astrometry (ra, dec, pm, ϖ, ref_epoch, RUWE columns exist) via astroquery. WISE 0855 and ε Indi B are probably not in Gaia, or are poor there → take literature μ from SIMBAD | H |
| S0.5 | One real cutout: HDU sizes (why ~4 MB), gzip size, EPSF oversampling (5 vs 10), SIP present, CRPIX1A rule | S |
| S0.6 | Cutout vs parent consistency: two overlapping cutouts with different centres → same star gives the same parent pixel within 1e-6 | S |
| S0.7 | Access speed: cutout service vs `fits.open(..., use_fsspec=True).section` on the S3 copy [ASSUMPTION: works]; seconds and MB per frame | S |
| S0.8 | reproject accepts a SIP WCS (pix→world agrees with astropy within 1e-4 px) | H |
| S0.9 | Review report, freeze manifest schema v1 | O |
Parallel: S0.1–S0.8 all run in parallel. Acceptance: the table lists N frames/detector/pass for Barnard, ε Indi B, WISE 0855, RW Aur, R Dra (0 allowed, but it must be stated). The per-target data volume estimate is ready.

### Stage 1: Data layer + raw blink (≈ 1 day)
Tasks: `spxblink ingest` (TAP → cutout download, 10 workers, retry 3x with 10·(n+1) s backoff [V], disk cache) **S**. Writer: per-frame `img.f32`, `var.f32`, `flg.u32` + manifest **S**. WebGL viewer: NEAREST, integer zoom, native grid overlay, blink, FOV **S**. Manifest schema + pixel-convention module with unit tests **O** (small).
Parallel: the pipeline and the viewer run in parallel against schema v1.
Demo: the viewer blinks Barnard's Star frames (native orientation, unaligned) locally. Acceptance: T1 screenshot part passes. Manifests exist for all targets that have coverage.

### Stage 2: Precision core (≈ 1.5 days, Opus-heavy)
Tasks: ePSF zone extraction + fitter + joint fit design **O**. Implementation and unit tests **S**. Injection/recovery harness T2–T4 **S**. Gaia comparison T5 + optional WCS refinement **O** design / **S** code. Results review **O**.
Parallel: harness (S) alongside the fitter (O→S).
Demo: residual plots (bias vs phase, Gaia residuals per frame), and Barnard's Star μ. Acceptance: T1 numeric, T2, T3, T4, T5, T6 as in 2.6. Any failure → write it up and fix before Stage 3.

### Stage 3: Exact geometry + overlays (≈ 1 day)
Tasks: affine map per frame + r_max logging, k-NN fallback **S** (O reviews the math). Viewer: frames aligned through A, centroid ellipses, cursor readout (native x, y, RA/Dec, λ) **S**. Gaia overlay with PM trail and parallax **S**. Flags layer **S**.
Demo: aligned blink at Barnard's Star: static stars stay still, Barnard's Star steps along its track, Gaia markers land on the stars. Acceptance: r_max ≤ 0.01 px on ≥ 99 % of frames (or fallback used and logged). Cursor readout = astropy within 1e-3 px. ≥ 95 % of Gaia stars are within 3σ of fitted centroids. Screenshot test repeated at zoom 1/4/16/64.

### Stage 4: Passes, stacking, difference, moving-object aid (≈ 1 day)
Tasks: pass grouping, inverse-variance stacks per detector (reproject exact) **S**. Joint-fit positions per pass **S** (from the Stage 2 design). Difference modes **S**. Simple candidate highlight: residual peaks in pass-difference images that are consistent with linear motion **S**, thresholds tuned by **O**.
Demo: ε Indi B and WISE 0855 in D5/D6 pass stacks, blinking per pass. Acceptance: blank-sky noise in the stack within 20 % of (Σ1/σᵢ²)^-½. Static Gaia stars in the difference image: median |residual| < 3σ. The WISE 0855 detection is reported honestly as detected or not (S/N stated).

### Stage 5: Spectra + variable stars (≈ 1 day)
Tasks: forced ePSF photometry per frame at the joint-fit position. λ, bandwidth per frame (CWAVE/CBAND preferred over WCS-WAVE for science [V]) **S**. Spectrum plot coloured by pass. Light curve per λ bin **S**. Review of the photometric error model **O**.
Demo: RW Aur and R Dra spectra and pass-to-pass change. Acceptance: the spectrum is continuous across detector edges within 3σ for a non-variable control star. For R Dra, the pass-to-pass change at fixed λ is reported with σ (no claim beyond the data).

### Stage 6: Product: URL, embed, update, deploy (≈ 1 day)
Tasks: URL schema + embed mode **S**. Aladin Lite panel + external links **S**. GitHub Actions weekly ingest **S**. Optional `spxblink serve` for any RA/Dec **S**. README **H**. Deploy to static hosting **H**.
Demo: a public URL. Each test target opens from a link. One simulated "new week" adds a frame without a manual step. Acceptance: all 5 links render. Reloading an edited URL reproduces the state exactly. The cron dry-run is idempotent (no duplicate frames).

### Stage 7: Gate review + honesty report (≈ 0.5 day)
**O** code and maths review (diff-only, no web). **H** runs the full test suite and collects numbers. Deliverable: `STATUS.md` listing each feature as done / partial / not done, with test numbers.

Total ≈ 7.5 working days. If time is short, drop Stage 5 or the optional serve.

---

## 5. Risk register

| # | Risk / unverified item | Impact | Check (stage) |
|---|---|---|---|
| R1 | No CORS on IRSA and Gaia (likely) [V partly] | only matters for options B/C | S0.1 |
| R2 | Flag-bit meanings and the "bad" set [NV] | wrong masking | S0.2 |
| R3 | ~4 MB per cutout (EPSF tables) x hundreds of frames → GB per target and long downloads | time budget | S0.5, S0.7. Mitigate: gzip, fsspec sections, cap frames, EPSF cache per parent file |
| R4 | Few passes (May 2025–Nov 2026 ≈ 3) or gaps at a target | weak PM signal | S0.3 |
| R5 | WISE 0855 too faint in SPHEREx near-IR, even D6 [ASSUMPTION: likely marginal] | target may not be visible | S0.3, Stage 4. Report honestly |
| R6 | ε Indi Ba/Bb (~0.7" apart [ASSUMPTION]) are unresolved at 6.15"/px. Possible scattered light from ε Indi A | shows as one blended source | state in UI. Check flags (GHOST/HALO) |
| R7 | **Each exposure sees a source at a different λ (LVF)** [V], so brightness changes between frames are partly spectral, and centroids can shift with λ (PSF varies per zone) | false variability/motion | λ shown per frame. Variability only within λ bins. Per-zone ePSF |
| R8 | WCS frame (aberration-corrected or not) and absolute accuracy unknown | systematic offsets up to ~3 px | T5. Gaia refinement |
| R9 | EPSF oversampling conflict (5 vs 10) | biased centroids if wrong | S0.5 |
| R10 | Affine approximation of SIP not good enough | edge error | r_max logged. k-NN fallback |
| R11 | Undersampled PSF → pixel-phase bias | sub-pixel bias | T2/T3. Correct with the empirical bias curve if needed |
| R12 | Bright stars (Barnard's, R Dra, RW Aur) saturate: OVERFLOW/NONLINEAR | bad centroids | mask those bits. Fit the PSF wings. Report |
| R13 | Gaia lacks or has poor astrometry for brown dwarfs | no overlay reference | literature μ (S0.4) |
| R14 | Static-host file-count/size limits [NV] | deploy | small binaries. Check in Stage 6 |
| R15 | Release reprocessing changes old frames (QR → DR) | duplicates | dedupe by provenance_version |

**Decided NOT to do:** Pyodide/in-browser astropy; any astrometry on resampled images; bilinear or bicubic display interpolation; our own HiPS generation; all-sky automatic moving-object discovery (only a per-field candidate highlight); MOST or JPL Horizons asteroid identification (could link out instead); accounts or auth; full-file (hundreds of MB) downloads as the normal path; aberration modelling unless T5 demands it.

---

## 6. First 3 actions
1. **Spawn the Stage 0 sub-agents in parallel:** H: S0.1 + S0.4 + S0.8. S: S0.2, S0.3, S0.5 + S0.6, S0.7. Each writes `s0_<id>.md` with [V]/[NV] tags.
2. **Opus writes the manifest schema v1 and the pixel-convention module spec** (section 2.2) while Stage 0 runs, so Stage 1 lanes can start immediately.
3. **Gate meeting:** Opus reads only the s0 summaries and updates this plan's risk table. The user approves the Stage 0 demo (coverage table + one gridded cutout) before Stage 1 begins.
