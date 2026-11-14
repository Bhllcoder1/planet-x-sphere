# SPHEREx Blink: site requirements (SITE_SPEC)

Scope: the public web page of the challenge "display SPHEREx images of a sky patch as a video-like time series so anyone can spot moving objects". Written against PLAN_spherex_v2.md (v2) and PLAN_spherex_v3.md (v3), stage0 reports s0_A..s0_D, DECISIONS_AND_TASK.md. Language: English. Tags: [V] verified by a real run, [NV] not verified, [ASSUMPTION] set here, unchecked.

Priority: **M** = must for the 5-day demo (v3 §4 MCD plus what the 5-target scope forces), **S** = should (next slices, v3 §4.2), **L** = later. "Lists" = ClickUp lists 02..06 (02 image pipeline, 03 astrometry, 04 data analysis, 05 viewer, 06 server).

## 0. Challenge requirements to site features

| Challenge text | Site feature | Spec id |
|---|---|---|
| User enters RA/Dec of a patch | target picker + coordinate entry | W1, W2 |
| Series of images like a little video | blink player | W4 |
| Easy to update with new data releases | release + pipeline version in every cache key and shown on page; frame list is a query, not hand-edited | W22, W19 |
| 102 bands: add data per each of the six detector arrays for S/N | per-detector grouping, per-pass stacks (view-only) | W16 |
| Spectra on the fly (extra kudos) | spectrum / light-curve panel | W15 |
| Add/subtract images from different times | stack and difference views | W16 |
| User chooses field of view | FOV selector | W3 |
| Optional Gaia and WISE overlays | Gaia = M; WISE/unWISE = L | W10, L2 |
| Coordinates in URL, embeddable (WiseView-like) | URL schema + embed mode | W19 |
| Metadata such as contamination flags | metadata strip + flag layer | W5, W9 |
| Astropy and Aladin Lite suggested | Astropy server-side (all of lists 02-04); Aladin Lite = L (context panel only, D1b: not measurement) | L1 |

## 1. Feature table

Data names: manifest = `manifest.json` schema v2 (v2 C.15); per-frame files `img.f32 var.f32 flg.u32 cat.json geom.json meta` (v2 C.11). Header keywords as in s0_A (MJD-AVG, XPOSURE, SPS_EPA, SPS_PA_ECL, DETECTOR, RADESYS) and v2 C.3 (CWAVE/CBAND).

| Id | Feature | What the user sees | Data / field | Produced by | Pri |
|---|---|---|---|---|---|
| W1 | Landing / target picker | Header, one-line purpose, 5 preset cards (Barnard's Star, Epsilon Indi B, WISE 0855, RW Aur, R Dra), each with coverage status (frames, passes) and a "result note" link | Frozen frame lists, coverage table; WISE 0855 position RA 08h55m10.831s Dec -07d14m42.53s | Stage 0 coverage (list 01), manifests (list 02 C.1, C.15), notes (list 08) | M |
| W2 | Coordinate entry | One field accepting decimal degrees and sexagesimal (`08 55 10.83 -07 14 42.5`, `08h55m10.83s`), plus a name box; parse errors in plain words; echo of the parsed RA/Dec in degrees | Parsed ra, dec; name resolve **server-side only** (browser never calls SIMBAD/Sesame; service and exact endpoint [NV]) | Server endpoint (list 06); parser unit tests (list 07) | M (coords, presets), S (free name) |
| W3 | Field-of-view selector | Choice of window size (default ~31x31 native px = 190") and a larger option; changing it re-requests the window without losing the frame | `fov` (arcsec); window = target window, astrometry window separate (v2 C.2) | List 02 C.2 windows; list 05 | M (2 sizes), S (free value) |
| W4 | Blink player | Play/pause, speed slider, step back/forward, restart marker, frame counter "12 / 358", progress bar with pass boundaries ticked | `frames[]` order in manifest; `frame`, `speed` URL params; passes from C.12 | List 02 manifest, list 04 pass grouping; list 05 | M |
| W5 | Per-frame metadata strip | Under the image: date and MJD-AVG (UTC), detector (D1..D6), wavelength at the target (CWAVE +- CBAND), pass number, release (DR1/QR3), processing tag (`l2b-v27-*`) | meta: MJD-AVG, DETECTOR, CWAVE/CBAND, pass id, release, provenance_version, file-name tag | List 02 C.3 ingest, C.11; list 04 C.12 | M |
| W6 | Mode badge + offset badge | Badge "N", "R-k" or "S" with a tooltip stating that mode's guarantee; badge "leftover rotation 0.7 deg, offset 0.31 px, <= 0.26 px at window edge"; one-line reason when the viewer left N | geom.json: transforms, theta_res, r_max; rule: N auto only if same detector and r_edge*theta_res <= 0.25 px (v3 §2.2) | List 03 (WCS), list 02 C.11 geom; list 05 | M |
| W7 | Pixel grid + zoom | Grid toggle, integer zoom buttons (z = 8..32 default), zoom label; fixed text: "Each native pixel is drawn exactly z x z screen pixels; a 1-pixel shift is exactly z screen pixels; positions are never rounded." Below 1 screen px per native px: label "overview, not exact" | zoom int; float marker coordinates | List 05 viewer; tests T-V1, float-position test 4.47 at zoom 100 -> 447.0 +- 0.5 (list 07) | M |
| W8 | Stretch + invert | asinh / linear / zscale choice, lo/hi percentile sliders, invert toggle, dark/light theme | `stretch lo hi invert` (v1 URL list); default decided by user screenshot (Q-H3) | List 05 | M (asinh, linear, invert), S (zscale, sliders) |
| W9 | Flag layer | Per-bit toggles named as in the flag table (TRANSIENT, OVERFLOW, OUTLIER, CROSSTALK, SOURCE, GHOST, GHOST_FPA, GHOST_EXT, STREAK, BLOOM, SNOWBALL, HALO, SATELLITE_HALO, NONLINEAR, PERSIST, HOT, COLD, NONFUNC, DICHROIC, MISSING_DATA, SUR_ERROR) as coloured outlines; presets "Centroid profile", "Mover-search profile", "Background profile"; crowded-field banner when fit-mask fraction > 50 % ("unusable for astrometry") | flg.u32; bit numbers: 0 TRANSIENT, 1 OVERFLOW, 7 DICHROIC, 19 OUTLIER, 20 CROSSTALK, 21 SOURCE, 22-24 GHOST*, 25 STREAK; fit mask 0x3C028E44; background 0x3C2A8E47; other bit numbers from Table 16 in code (not restated in plan: take from list 02) | List 02 C.4 masks, v3 §2.1; list 05 | M (toggle + 2 profiles), S (background profile, per-window caution counts) |
| W10 | Gaia overlay | Gaia DR3 stars as open circles at the frame epoch; for the target a proper-motion trail (past and future dots) with epoch labels; toggle `gaia` | Gaia cone propagated to MJD-AVG (space motion + parallax), per frame in cat.json | List 03 C.8; list 05 | M |
| W11 | Centroid markers | Cross at the float position + 1-sigma ellipse, 2-sigma dashed; saturated cores get "saturated-fit" badge; target is forced-fit (shown even if not detected) | cat.json: x, y, sigma ellipse, chi2_nu, flags | List 03 C.7, C.7b | M |
| W12 | Readout panel | Cursor: native x,y (float), RA/Dec, flux and its error. Pick two frames: delta in px and arcsec with sigma, e.g. "0.21 +- 0.03 px (1.29 +- 0.18"), 7.0 sigma, frames 12 to 31, dt 183 d" | img/var, corrected WCS, cat.json covariance | List 03 (covariance, WCS), list 05 (astropy-equal within 1e-3 px, list 07) | M |
| W13 | WCS-correction badge | "WCS corr: 0.31 px shift, sigma 0.008 px, N = 42"; "uncorrected" if N < N_min or RMS > 0.3 px; "aberration-like offset" alarm text | geom.json: raw WCS, T, Cov(T), N, RMS | List 03 C.9 + alarm (v3 §2.3) | M (shift-only), S (similarity/affine) |
| W14 | Measurement panel (motion between passes) | Table per pass: position (float) and sigma, motion vector drawn true-length, optional scaled copy labelled "x10" in another colour, measured mu vs Gaia mu with the difference in sigma; for Barnard expected about 0.96 px pass 0 to 1 and 1.7 px pass 0 to 2 (arith, v3 §4) | joint per-pass positions (C.7b), mu fit, Gaia propagation | List 03 motion fit (v3 slice 1); list 05 | M (two-pass readout), S (track plot x(t), y(t) with error bars) |
| W15 | Spectrum / light-curve panel | For the clicked source or the target: flux vs wavelength (points coloured by detector) and per-pass flux, error bars; required for RW Aur and R Dra; note "variable star, flux changes between passes" | forced photometry per frame, CWAVE/CBAND; detector grouping | List 04 (lambda-binned curves, v2 Stage 7); list 05 | M for RW Aur and R Dra (minimal), S otherwise |
| W16 | Stacks and differences | Mode "stack" per detector per pass (six detector arrays shown separately or summed where lambda allows, for S/N), mode "diff" = pass minus pass, same detector and lambda within one channel; user picks A and B (add or subtract); always banner "S: resampled, view only, no astrometry"; list of lambdas used | reproject-exact stacks on Mode R grid (C.12) | List 04 C.12; list 05 | S (view-only; M only if WISE 0855 needs it, DECISIONS) |
| W17 | Per-target result note | Card per target: coverage, what is detected, S/N, motion vs literature/Gaia, caveats, the date of the data release. Honest-outcome wording: "SPHEREx does not show this target in release X (0 frames in the field)" or "not detected above N sigma in M frames". Epsilon Indi B: "unresolved pair next to bright eps Indi A, shown as one blended source". Never replaced by another object | result notes | List 08 | M |
| W18 | Coverage and error states | (a) no coverage: "no SPHEREx frame covers this position in release X" + date of next pass if known; (b) archive busy: "archive busy, retry queued" (never "no coverage"); (c) still processing: progressive frames "n of N ready", blink starts from first frames; (d) saturated/NaN core, crowded field banners | TAP async result, L0 cache state, job SSE | List 06 (async TAP, SSE), list 02 C.1; list 05 | M (a, b, d from frozen lists), S (c live progressive: v3 slice 3) |
| W19 | URL schema + embed | Every control state written to the URL; reload reproduces the view exactly; `embed=1` hides all chrome and shows only image, frame counter and a link "open full view" | Names from v1 URL list (PLAN_spherex.md, "URL schema"): `ra dec target fov det mode diffref frame speed zoom stretch lo hi invert grid gaia cen flags wl dwl release embed`; v2 Stage 7 adds `mode=N|R|S` and `vecscale`; v2 §3 does not hold URL names, v1 does | List 05 (URL state), list 06 (route), list 07 (reload test) | M |
| W20 | Share / export | Buttons: copy link, PNG of the current view (with grid, markers and badge text burned in), CSV of measurements (frame, MJD-AVG, detector, x, y, sigma_x, sigma_y, flux, flags, WCS-corr) | current view; cat.json rows | List 05; CSV column list from list 03 | S |
| W21 | Links out | SIMBAD, VizieR, IRSA MOST (object to images) and IRSA SPHEREx archive for the position | name/coordinates; exact URL forms [NV] | List 05; link check in list 07 | S |
| W22 | About / limitations / versions | About page: what the tool does, honesty rules, limitations (Drizzle off, no AI upscaling, display modes and guarantees, no mover finder claim until tested, crowded fields, saturated cores). Footer shows data release, pipeline version, frame-list date; acknowledgements for SPHEREx/IRSA, Gaia, astropy, photutils, SkyBoT/MOST if used | build constants | List 09 (limitations, acknowledgements); list 06 (version in manifest) | M |
| W23 | Accessibility and mobile | Keyboard: space play/pause, left/right step, `[` `]` speed, `g` grid, `i` invert, `f` flags, `r` restart; overlay colours from a colour-blind-safe set (Okabe-Ito) plus distinct marker shapes; visible focus; 16 px side gutters, no horizontal scroll at phone width, touch targets >= 44 px [ASSUMPTION] | none | List 05 | M (keys, colours, gutters), S (screen-reader labels) |
| W24 | UI language | English UI | open decision | user | M (decision) |

## 2. Later (not committed)
- L1 Aladin Lite context panel (not for measurement; D1b accuracy rule: library below 0.1 px or context only).
- L2 WISE/unWISE overlay (optional in the challenge; DECISIONS).
- L3 Brightness-spread "smooth shift" view: only as a labelled view-only mode, never for measurement (DECISIONS). Shown only if the user asks.
- L4 Mover-candidate panel (list 04, v3 slice 4) with reason codes and SkyBoT tags (`-objFilter=100`).
- L5 Mode R GPU affine (v3 slice 2).

Excluded on purpose: Drizzle (user said no), AI upscaling (dropped), Google/OAuth or any third-party login and public sign-up (accounts are NOT excluded any more: a small set of predefined accounts, up to ~10, see section 2a), all-sky discovery, any measurement on resampled images.

## 2a. Accounts, history, profile, outputs, UI/UX (new user requirements, authoritative; ClickUp list 11)

Source: user message of this round (A..E). Tags as above. The number of accounts (up to ~10, design for 10, 4 is just the start) is a **config value** (`USERS_COUNT` / length of the seed file), not a code constant. Ids continue the table in section 1. "Lists" = ClickUp lists 05 viewer, 06 server, 07 tests, 11 this block.

| Id | Feature | What the user sees | Data / field | Produced by | Pri |
|---|---|---|---|---|---|
| W25 | Login screen | Name + password form on a plain page reached from the shared link; no sign-up link, no "forgot password" (we reset by hand); wrong login gives one neutral message; after too many tries "wait N s" | `users` table (name, display_name, pw_hash, created); accounts read from a seed file outside git (secrets) | List 11 (server + UI); Caddy HTTPS from list 06 | M |
| W26 | Session and security | Stays logged in on reload; "Log out" in header; session expires after an idle time [ASSUMPTION: 12 h, longer than the presentation] | HttpOnly + Secure + SameSite cookie, server-side session id; passwords hashed (argon2id or bcrypt [ASSUMPTION: library chosen in task]); HTTPS only; login rate limit per IP and per name | List 11, list 06 (Caddy) | M |
| W27 | Search history recording | Nothing extra to do: every search is saved. Entry shows target/RA-Dec, time, a small summary line and the outcome | `searches` row: user, ts, target name and/or ra,dec, fov, mode (N/R-k/S), det, release, stretch type, lo, hi (percentile or value, with a unit field), invert, zoom, frame index or pass, overlays (gaia, cen, flags), flag-mask profile, n_frames, outcome (found / no_coverage / archive_busy), duration_ms, `query` (the URL query string) | List 11 server; list 05 emits the state | M |
| W28 | History restore | Click an entry: the whole screen is restored (target, FOV, mode, detector, release, stretch, brightness limits, invert, zoom, frame, overlays, flag profile) and the URL equals the stored query. Same mechanism as share link and embed | `query` = URL-parameter schema (PLAN_spherex.md section 3 and PLAN_spherex_v2.md section 3; names listed in W19); keys without a URL name are added there, not in a second schema | List 05 URL state (W19); list 11 | M |
| W29 | Profile page | User name, total searches, number of distinct objects examined, last visit, history list (filter by target text, sort by time, newest first default), list of examined objects. Only the logged-in user's data. Admin view for the team: [ASSUMPTION] none | Aggregates over `searches`, `examined`; `last_visit` in `users` | List 11 | M |
| W30 | Examined objects | An object = a source the user clicked or measured. List row: name (when known) or position, stable id, and the measurement shown at that moment: flux, motion, S/N; click re-opens the view at that object | `examined`: user, ts, object_id (Gaia DR3 source id if matched, else `pos:<ra>,<dec>` at 6 decimals), name or null, ra, dec, flux (value, unit), motion (mas/yr or px/pass, as shown), snr, `query`. Name from resolver [NV: service and endpoint not verified] | List 11; readout panel W12 emits | M |
| W31 | PNG export | "Save image": PNG of the current view with grid, markers, ellipses and badge text (mode, offset, WCS-corr, release) burned in; Mode S image carries the "resampled, no astrometry" label | canvas render at integer zoom | List 11 + list 05 | M |
| W32 | Measurement CSV | "Download table (CSV)": one row per frame: frame, MJD-AVG, detector, x, y, sigma_x, sigma_y, flux_MJy_sr, flux_mJy, flags, wcs_corr, CWAVE, CBAND, plus provenance header lines. Exact output columns and units of the IRSA tools [NV: documentation https://irsa.ipac.caltech.edu/onlinehelp/spherex/#sp not yet read; task 11-01] | cat.json rows | List 11 | M |
| W33 | Cutout FITS | "Download cutout (FITS)": multi-extension file for the selected window in the IRSA layout: IMAGE, FLAGS, VARIANCE, ZODI, EPSF, WCS-WAVE, each with headers. IMAGE units MJy/sr [V: sources\irsa-tut-spherex-intro.md]. Layout details checked against IRSA's cutout output [NV] | per-frame products (v2 C.11) re-packed | List 11 + list 02 | S |
| W34 | Spectrum plot and table | Flux vs wavelength with error bars, points coloured by detector (Okabe-Ito), table beside it (wavelength, band width, flux, error, detector, frame); PNG and CSV of both. IRSA's Spectrophotometry Tool is the reference [V: sources\irsa-spherex.md]; our spectrum is our own forced photometry, not IRSA's | forced photometry per frame, CWAVE/CBAND (extends W15) | List 04 data, list 11 export | M for RW Aur, R Dra; S otherwise |
| W35 | Provenance and honest limits on every export | Block at top of CSV/FITS header/PNG footer: target, RA/Dec, release, pipeline version, frame ids, masks used, WCS correction, date, tool version; plus the note that view-only products (Mode S, stacks) are resampled and carry no astrometry | build constants + manifest | List 11 | M |
| W36 | Design system | Design tokens (colour, type scale, spacing, radius, motion), dark and light themes, Okabe-Ito overlay colours, 16 px mobile gutters | `tokens.css` single file | List 11 design | M |
| W37 | Screen states | Empty, loading, error, no-coverage and archive-busy states for the main screen, profile and export panel, each with plain words and one action | state table + strings | List 11 + W18 | M |
| W38 | First-run onboarding | First login: 3-step overlay (pick target, blink, save/export), skippable, "show again" in help; completion stored per user | `users.onboarded` | List 11 | S |
| W39 | Keyboard shortcuts | Extends W23: `?` opens the shortcut sheet; `e` export panel, `h` history, `p` profile; no shortcut fires inside text fields | key map | List 11 + list 05 | M |
| W40 | Performance feel | Frames appear progressively ("n of N ready"), skeleton in place of the image, blink starts from the first frames, no layout shift; timings logged | job SSE (W18c) | List 11 + list 06 | S |
| W41 | Strings in one file | All UI text in `strings.en.json`; switching language = another file; language choice open (W24) | one strings file | List 11 | M |
| W42 | Backup and restore (operator) | Not user-visible; operator copies the SQLite file off the VM before shutdown and restores it on a new one; banner "history restored at <date>" optional | `.backup` copy + checksum | List 11 + list 06 runbook | M |

Decisions written down here (all [ASSUMPTION] unless stated): storage = one SQLite file on the VM in WAL mode; history key = user NAME; every history and examined row is private to its user (no admin view); the accounts (up to ~10), their display names and first passwords come from a seed file we generate and hand out; no email, no password reset page.

Output data-display work (so products are display-ready, not raw): one export schema file fixes column names, units, order and number formats (flux in MJy/sr and mJy, positions as floats in native px, time as MJD-AVG and ISO UTC, wavelength in um); pipeline products get the same names (no `x_fit` in one place and `x` in another); FITS extensions keep IRSA's extension names and header keywords; every number shown in the UI and in files shares one formatter so a value reads identically on screen, in CSV and in PNG. mJy conversion: [mJy] = [MJy/sr] x 23.5045 x (pixel scale in arcsec)^2 / 1000 [V formula in sources\irsa-tut-spherex-mosaic.md]; which pixel scale it assumes, and its use for L2 pixels of 6.15 arcsec, is [NV] and is checked in task 11-02.

## 3. Cross-cutting rules for every screen
1. Positions are floats, never rounded; markers are transformed with the same matrix as the pixels (v2 §D).
2. Any value not measured shows "not measured", not a default.
3. Anything unverified in the UI text carries a visible "unverified" or "assumption" note.
4. Mode S images never carry an astrometric readout.
5. The site talks only to our server (no browser calls to IRSA, Gaia, SIMBAD).
6. Data and pipeline versions are part of every cache key and shown in the footer.

## 4. Open questions for the user
1. **UI language**: English (assumed: the challenge is international) or Turkish, or both with a switch?
2. **Deadline** (date, time zone): decides how much of "S" lands in the demo (still unanswered in DECISIONS).
3. **Free coordinate/name entry live, or presets only?** Live entry needs the queue and async TAP (v3 slice 3) and the D9 timing test; the default is presets plus frozen frame lists.
4. **Public traffic expected**, or jury/demo only (decides the archive-busy and per-IP limits copy)?
5. **Name resolver**: is SIMBAD/Sesame acceptable as the server-side service (not verified which endpoint and its terms)?
6. **Default look** from screenshots: asinh / linear / zscale, dark or light theme (Q-H3).
7. **PNG and CSV export** in the demo, or later?
8. **Operator contact** for the footer and the IRSA User-Agent (which name/email may be shown publicly)?
9. **WISE 0855 outcome**: if SPHEREx has no usable frames, confirm the card says exactly that and nothing replaces it.

### Open questions for the user (accounts, history, outputs, UI/UX)
10. **Where do the names come from** (up to ~10 accounts; real people, roles, or generic user1..user10)? Is the display name the same as the login?
11. **Passwords**: generated by us and handed out (assumed), or chosen by the users? Over which channel are they handed out?
12. **Is history private to each user** (assumed yes)? Or should users see each other's searches?
13. **Admin view for the team**: wanted? Assumed no; if yes, who and what may it see?
14. **Number of accounts**: up to ~10 and not more (design for 10; we start with 4 and keep it a config value). Confirm the cap.
15. **History retention**: keep everything until the VM is deleted (assumed), or a cap per user?
16. **Backup**: where may we copy the database off the VM (your laptop, a cloud bucket)? Is the data sensitive enough to encrypt the copy?
17. **Name resolver for object names** in the profile (SIMBAD/Sesame, server-side): acceptable?
18. **Export priorities**: all four (PNG, CSV, cutout FITS, spectrum) in the 5-day demo, or FITS later (assumed later)?
19. **Output format details** wait for the IRSA documentation read (task 11-01); we will ask again if our columns differ from IRSA's.
20. **UI language** (see 1): English assumed; the strings file allows a Turkish switch later.
21. **Usability test**: may we show the site to your users (up to 10; a subset is fine) before the presentation, and when?
22. **Session length**: is 12 h idle timeout fine, and should the page warn before logout?

---

## 2b. WiseView'den alınan özellikler ve gösterim işleme katmanı (added 2026-11-14)

Source: the open-source WiseView repository (github.com/backyardworlds/wiseview, public domain) and its page text; copies in sources_wiseview/. The live site's AWS Lambda code is NOT in the repository [NV]. Priority: M = must for the 5-day demo, S = should, L = later.

| ID | Feature | What the user sees | Producing component / task | Priority |
|---|---|---|---|---|
| W43 | Epoch legend (+ / - / .) and loop-restart border | A bar next to the image showing which frames are added, subtracted or unused in the current frame; dashed border when the loop restarts | 05-15 (needs 04-02, 04-15) | M |
| W44 | Sliding-window coadd and window-minus-outside difference (view only) | Window-length slider; difference view labelled resampled / no astrometry | 04-15 | L |
| W45 | Click to recentre, drag for a new field of view | Click moves the centre; drag opens a new view with another FOV | 05-16 | L |
| W46 | Stretch controls: clip modes (fixed / percent / adapt / zscale), min-max boxes, linearity slider, maximize dynamic range, invert | Controls plus a colour bar in MJy/sr | 05-17 on top of 02-16, 02-17, 02-19 | M |
| W47 | WiseView-compatible URL aliases | A WiseView link (ra, dec, size, speed, zoom, invert) opens a comparable view; unsupported parameters are listed | 05-18 | M |
| W48 | Prefilled context links (Simbad, VizieR, Legacy Survey, Pan-STARRS) | Four links with the target position (epoch and radius stated) | 05-19 | L |
| W49 | Shift-and-add for a user-given motion (view only) | Enter proper motion; frames are shifted and summed | 04-16 | L |
| W50 | Synthetic object (labelled SYNTHETIC) | Add a fake mover to the view copy; never enters measurements or caches | 04-17, test 07-14 | L |
| W51 | Colour composite from detectors (view only) | Short / medium / long wavelength as B / G / R | 02-21 | L |
| W52 | Display-processing layer | Stretch, clip, invert, ZODI subtraction, optional hot-pixel smoothing (default OFF), PNG and thumbnails; measurement data is never modified | 02-15 .. 02-20 | M |
| W53 | History thumbnails | Small preview per history entry | 11-23 | S |

Design decisions from this review:
- URL parameter clash: WiseView's mode means the clip mode (fixed / percent / adapt); our mode meant the display mode (N / R-k / S). Our parameters are renamed: view = n | rk | s and clip = fixed | percent | adapt | zscale (task 05-18).
- Not copied on purpose: replacing hot or outlier pixels in the data (display switch, default off, 02-18), the 2015.5 base epoch for Gaia positions (we use the DR3 epoch 2016.0, MJD 57388; comparison test 03-15), 8-bit PNGs as a basis for measurements, WISE-specific Zooniverse links.
- Fundamental difference: WiseView frames share one fixed tile grid (2048 x 2048, 2.75 arcsec per pixel, one WCS per tile), so blinking needs no resampling. SPHEREx frames each have their own grid and roll, which is why we have display modes N / R-k / S.

| W54 | Background (ZODI) switch | Selector in the image panel: Raw / ZODI subtracted (default) / Flattened; badge on the image; stored in the URL (bg=raw|zodi|flat) and in the search history; PNG carries the label; CSV and measurements are never affected | 02-19, 05-20, test 07-16 | M |
| W55 | Shared stretch limits and automatic defaults | One lo/hi per detector group for the whole blink sequence (per-frame is a switch); "Default (auto)" button reads display_defaults.json | 02-16, 02-22, 05-17 | M |
