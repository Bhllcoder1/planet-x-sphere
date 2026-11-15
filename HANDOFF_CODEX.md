# Codex handoff - Planet XSphere

Owner: Codex. Claude owns its own handoff; Codex will not update HANDOFF.md further.
Last update: 2026-11-15.

## Scope and instructions

Area B, explicitly reconfirmed by the user. Continue Behlul-assigned ClickUp tasks in dependency order with parallel agents. Skip adding/running new tests for now. Report implemented code separately from runtime/scientific acceptance. Preserve existing user/Claude edits; use explicit file ownership and staging.

The existing /goal objective remains unfinished. Its backend status was blocked earlier; creating a replacement goal was rejected because an unfinished goal exists. Work continues on that same scope; do not mark the goal complete to bypass this restriction.

## Git and access

Repository: C:/Users/behlu/planet-x-sphere
Branch: b/01-03-gaia-fetch
PR: https://github.com/Bhllcoder1/planet-x-sphere/pull/1 (open/draft)
Latest Codex pushes: 3b02704 (coordinates and sky photometry), 2838b58 (velocity lattice and handoff).
Read the current remote head before pushing; Claude may commit concurrently.
ClickUp authentication works: extract the pk_ value from the private local token file. Do not read entire lines as the Authorization header, print the token, or commit it. Earlier401 reports were caused by parsing.

## Delivered code

- 03-14: centroid/coordinates.py bridges explicitly supplied corrected native cutout WCS through A pixel conventions to float cutout and parent coordinates.
- 04-03: motion/forced_phot.py supplies forced_phot(ra,dec,frames) and CSV; corrected WCS is caller-supplied/unverified, physical flux normalization remains unverified.
- 04-06: movers/linker.py implements a bounded pair-supported sparse velocity lattice plus consensus refinement. It does not search every empty velocity cell; search diagnostics state that explicitly.
- Earlier batch: 04-02 exact-TAN display stacks, 04-07 OUTLIER promotion, 04-15 rolling displays, 03-06 full covariances/JSON and sparse joint solver. Task-specific reports are under b_astrometri/reports/.
- Latest ordered batch was static-reviewed only; no new tests or code runs were performed by Codex.

## Active parallel batch

1. gaia_review: motion/passes.py + reports/04-01-manifest-integration.md. Explicit manifest ingestion, stable IDs, release/version dedup and pass grouping.
2. next_dependencies: centroid/ellipse.py + reports/03-04-catalog-integration.md. Centered ellipse/catalog output with separate centroid and WCS correction covariance.
3. gaia_epoch: motion/lightcurves.py + reports/04-12-photometry-integration.md. Target/control actual-frame photometry to lambda-binned outputs.
4. work_protocol: movers/outlier_comparison.py + reports/01-12-outlier-comparison.md. OUTLIER fractions by week/procver with same-field controls and no invented causal conclusions.

All workers are instructed not to add/run tests or edit shared docs, Git, ClickUp, or each other's files.

## Live statuses

08-01 was verified and marked complete. Current active statuses include00-05,01-03,03-02,03-04,03-06,03-07,03-14,04-01,04-02,04-03,04-06,04-07,04-12,04-15,01-12. Re-read live API for exact counts. No unverified full scientific task was marked complete.

## Existing long-running experiment

The previously started03-06 thousand-trial coverage process continues; no new run has been started after the user requested no new tests.
Evidence: C:/Users/behlu/reports/03-06-coverage.json
The worker's session92791 is agent-local; root cannot poll that session ID. Monitor the actual existing process/PID and JSON; do not restart on observation failure.
One trial584 had a failed single-frame baseline but successful joint fit. Current runner reports paired-success coverage, excluding that joint-only result. Preserve this denominator limitation in any final claim. Wait for complete=true before describing final results. No real Barnard acceptance follows from this synthetic experiment.

## Shared worktree caution

Other-session changes have appeared in gaia/fetch.py, gaia/test_fetch.py, docs/second-brain/TASKS.md and reports/09-06-sinirliliklar.md. Do not stage or overwrite them without inspection. Shared Graphify outputs currently represent the earlier snapshot; README explicitly notes that the latest ordered integration batch has not been reindexed.

## Next action

Collect current four workers, statically review their owned files without executing tests, push only reviewed files and this Codex handoff, and update PR evidence. Continue the next eligible B work slice. Human decisions, missing corrected-WCS/calibration data and actual target acceptance must stay explicit.
