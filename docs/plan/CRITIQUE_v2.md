# Critique of PLAN_spherex_v2.md (2026-11-14)

Checked against research2/notes_expsupp.md, notes_moving.md, notes_server.md and research/notes_spherex.md.

## Confirmed against the notes
- Flag masks in C.4: all bit numbers match Table 16 (fit mask bits 2,6,9,10,11,15,17,26-29; background adds 0,1,19,21).
- QR1/QR2 PSF plane-order bug; KBMOD ~1e10 trajectories/min (arXiv 1901.02492); TAP first call ~28 s; ePSF 5x (33x33).
- "~4 MB per cutout, mostly ePSF" is correctly tagged an assumption (not verified in the notes).

## Problems, most important first
1. **Scope.** 15-step pipeline, 3 display modes, 16 tests, mover finder, drizzle, spectra, in ~14 days. The hackathon deadline was never asked. First demo only at Stage 1. Suggested thin slice: Stage 0 -> 1 -> 2 (Barnard, native pixels, precision tests); the rest later.
2. **GHOST / STREAK / CROSSTALK / TRANSIENT are not masked by default (C.4).** SPHEREx's own mosaic tool NaNs them (Expsupp p.46) and the all-sky cube rejects most. Satellite streaks are the classic false positive for mover searches. Safer default: mask, show on request. Plan defers to test D13.
3. **Aberration "irrelevant" is reasoning only.** Notes: the document never mentions aberration; the pipeline propagates Gaia by proper motion without mentioning parallax. Decides whether the correction is ~0.05 px or ~3 px. Move the check to Stage 0 (one frame).
4. **Mode N relies on "roll within a survey differs by <~1 deg".** Notes say PA is fixed per survey (supports it) but do not prove it. If false, the default mode fails. S0.5 measures it, but the main design depends on it.
5. **Unknown whether OUTLIER/TRANSIENT processing can flag real movers** (Expsupp Sect. 3.2.10 is not detailed in the notes). No injected-mover test passes through the flag layers.
6. **GPU:** user said a server with a discrete GPU; plan starts CPU-only (reasoned, measured trigger). The user's call, not asked.
7. **No WISE overlay** (challenge optional item; user wanted external catalogs queried server-side). Only Gaia.
8. **Numbers that are assumptions:** error budget (~0.01-0.03 px at SNR 100; Gaia propagation <0.005 px), CPU VM cost (EUR 15-40), AWS price, Hetzner US location. No web lookups were done for v2.
9. **User workload:** 6 tests need screenshot judgement plus 8 open questions; stages wait on answers.

## Limits of this critique
Written by the main session, not the user. Many PDF note lines were truncated ("long line omitted"), so time/visit-count details were not re-verified.
