# Decisions and current task (2026-11-14) - read this with PLAN_spherex_v3.md

## Decisions made by the user
- Backend: a rented machine; **hourly rental of any computer for a few hours is fine** (the presentation lasts a few hours). Budget is not a constraint for now.
- GPU: CPU-first. If a GPU is useful for a demo, rent one on-demand (vast.ai) for a few hours and show the result.
- WISE/unWISE overlay: optional in the challenge -> later list.
- Technology is chosen by small tests; the user looks at screenshots and answers the questions.
- Honesty rule: unverified = say "not done / not verified".

## Inferred, NOT confirmed (ask the user)
- The demo is shown live on a machine rented only for the presentation (no 24/7 hosting, no weekly cron, no public traffic, no per-IP limits needed). If wrong, v2 B.2-B.7 apply again.

## Still unanswered
- Hackathon deadline (date/time zone). Default in v3: 7 days.
- Provider/region preference (default: AWS us-east-1 or Hetzner Ashburn, decided by the D9 timing test).
- Top-2 demo targets (default: Barnard's Star + WISE 0855, fallback eps Indi B).
- AI upscaling: dropped unless the user objects.

## Added later
- Drizzle level 2: user said NO. User's idea: show fractional positions through brightness (light spread over neighbouring pixels). Design answer: positions stay float and are never rounded (4.47 at zoom 100 must be drawn at 447, not 500); a brightness-spread "smooth shift" view is allowed only as a labelled view-only mode (it is interpolation: blurs, correlates noise, biases centroids), never for measurement. Add the test: float position 4.47 at zoom 100 -> 447.0 +/- 0.5 screen px.

## Scope decision (user, 2026-11-14): the competition's 5 test targets
We are responsible for exactly the targets the competition names: Barnard's Star, Epsilon Indi B, WISE 0855, RW Aurigae, R Draconis. Other objects may be added by others later; they are not our commitment. This replaces v3's "Barnard + WISE 0855 (fallback eps Indi B)" demo choice.
Consequences:
- Final deliverable = all 5 targets handled with the same pipeline; each gets an honest result note (what is detected, what is not, with S/N). A target that SPHEREx cannot show (possibly WISE 0855) is reported as such, not replaced by another.
- Build order: Barnard first (clearest motion), then add the others one by one; unknown coverage of WISE 0855, RW Aur and R Dra (TAP failed) is the first Day 0 test.
- RW Aur and R Dra are variable stars: a minimal per-epoch brightness / lambda panel (v3 slice 7) is required, no longer optional. Eps Indi B is an unresolved pair next to bright eps Indi A: show it as one blended source with the caution flags.
- WISE 0855 detectability decides whether per-pass stacking / forced photometry (v3 slice 5) becomes required.
- Revised cut order: first cut drizzle/WISE overlay/GPU demo; keep coverage + blink + centroids for all 5 and the variable-star panel; stacks only if WISE 0855 needs them.

## What a few-hours rental changes in v3
1. D9 (in-region fetch timing) becomes cheap: 1-2 h on an AWS us-east-1 VM, run the 50-frame coalesced-read test.
2. The same VM can **prefetch the demo targets** (Barnard: 358 frames, ~4.2 GB estimated) in-region; then keep the cache on that VM (or copy it) and serve the demo from it.
3. Optional GPU: a few hours on vast.ai for the shift-and-stack demo only if the B.5 trigger fires.
4. Rent only after the code is ready to run, to avoid paying for idle hours (suggestion).

## Task now (build order)
Day 0 remaining Stage 0 tests (v3 section 5 items 1-4, 10) -> Day 1 prefetch + pixel-convention spec -> Day 2 viewer (Mode N) + checkerboard test (user screenshots) -> Day 3 ePSF centroiding -> Day 4 Gaia match + WCS shift correction + R-k raster for cross-orientation passes -> Day 5 second target, readout, deploy on the rented machine, screenshots to the user.
Known weakness: v3's own Mode N rule (leftover rotation <= 0.25 px at the window edge) will often fail within a pass for Barnard D2 (spread 0.72-1.42 deg vs the 0.68 deg limit for a 31x31 window), so the demo will often use the server resampled raster (R-k).

## Added: display-processing layer and WiseView review (2026-11-14)
- A display-processing layer is now explicit (tasks 02-15 .. 02-21): measurement data is never modified; every display step that changes pixel values is default OFF and shows a badge. Stretch runs in the browser; the server runs the same function for PNG and thumbnails; a golden test keeps them equal (02-17).
- WiseView source (public domain) is stored in sources_wiseview/. Its live Lambda is not available, so statements about what the live site does are [NV].
- URL parameter rename: view = n|rk|s (display mode), clip = fixed|percent|adapt|zscale (clip mode); WiseView link aliases accepted (05-18).
- New tasks added to ClickUp: 02-15..02-21, 03-15, 04-15..04-17, 05-15..05-19, 07-14, 10-17, 11-23 (19 tasks).
- Still waiting for the Sonnet limit to reset (00:30 Istanbul): enrichment of lists 06, 07, 10, 11 (original tasks), the preflight tool and the PRE-CHECK sections.

## Decisions of 2026-11-14 (display layer, user answers)
- ZODI subtraction in the display: a switch (raw / zodi / flat), default ON with a badge; measurements unaffected. (User answer was garbled; interpreted as "make it a general setting"; to be confirmed.)
- Stretch limits: shared per detector group for the whole blink sequence (per-frame is an option).
- Aladin Lite panel: NOT in the demo (user unsure; recommended default applied); Aladin is a map viewer, not a database.
- Small ML model (real/bogus): later; now only the data-collection hook (candidates_log). Tasks 04-18, 04-19 are 'sonra'.
- New tasks: 02-22, 05-20, 07-15, 07-16, 04-18, 04-19; updates appended to 02-15..02-20, 04-06..04-11, 05-14, 05-17, 11-06, 11-23. Design reference: plan/DISPLAY_LAYER_DESIGN.md.

## Team split into 4 skill areas (2026-11-14)
- Area tags on every ClickUp task: kişi-a (data integration + image processing), kişi-b (astrometry + analysis), kişi-c (server, accounts, rental), kişi-d (site, UI, presentation). No one is assigned; the team maps letters to people. Details and hand-offs: plan/TEAM_SPLIT.md. Total estimate 675 h (all tasks), the 5-day budget of 4 people is ~160 h: scope must be cut by the cut order.

## API ownership (2026-11-14)
- Rule: every task about OUR server's API, and any API-related task added later, goes to area C (kişi-c). Task 06-14 (OpenAPI contract + mock server, day 1) added.
- TAP/S3 client code is written once by area A (02-01, 02-02); area C only plugs it into the server (06-03, 06-04).

## Rebalanced split (2026-11-14, user: make it equal, forget the API rule)
- The 'API goes to C' rule was dropped. Split recomputed so that total hours, required (not 'sonra') hours are equal within a few hours, with explicit per-task allowed areas (viewer core, wireframes, accounts etc. stay in their own area; docs, rehearsals and coordination tasks are spread over all four).
- Area names: A data integration + image processing + data analysis; B astrometry + moving-object science; C server, accounts, rental; D site and UI. Details: plan/TEAM_SPLIT.md. Hours are rough estimates [ASSUMPTION].
