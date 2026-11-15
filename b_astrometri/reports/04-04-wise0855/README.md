# 04-04 WISE 0855 coverage gate

Decision is **unknown**, not “no coverage”. The recorded TAP queries failed/timed out, and the SIA fallback did not complete. A single QR3-only probe returned no rows, which says nothing about DR1/QR2 or TAP coverage. Evidence is cited in `wise0855_detect.json` and `docs/stage0/s0_A.md` lines 383, 404, and 405.

Forced photometry and per-pass SNR were deliberately not run because the canonical frame coverage is unavailable. Next step: obtain/rerun List 01 coverage. Continue only with verified frames and passes. Do not substitute another target.
