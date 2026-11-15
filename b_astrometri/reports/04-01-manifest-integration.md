# 04-01 — Explicit manifest-to-pass integration

Task: https://app.clickup.com/t/z8qu5ddjx3

## New callable boundary (static review only)

`motion/passes.py` now provides:

```python
manifest = load_pass_manifest(path)
result = group_manifest_passes(manifest, gap_days=30.0)
write_pass_outputs(result, output_directory)
```

The existing permissive `group_passes` and output writers are unchanged.
The strict integration requires an object with:

- `target_id`: nonempty stable target identifier.
- `release`: explicitly `DR1` or `QR3`, homogeneous for this input. Any optional
  row-level release must agree. QR1/QR2 and unknown/mixed releases are refused.
- `status`: `ok` for nonempty frames, or explicit `unknown` / `no_coverage` for
  an empty list. A failed/missing query is never inferred to mean no coverage.
- `frames`: list of objects with nonempty `frame_id`, `obs_id`, integer detector
  1..6, finite numeric `mjd_avg` from IMAGE MJD-AVG, finite numeric `sps_epa`
  from the actual frame header, and explicit `procver` processing tag.

Supported processing-tag form is `l2b-v<version>-<year>-<build>` and the existing
`l2b_retry-v...` variant. Version/year/build are compared numerically, avoiding
lexicographic ordering of build numbers. No missing IDs, times, detector,
orientation or processing versions are guessed from row order or filenames.
Conflicting `MJD-AVG`/`mjd_avg` or `SPS_EPA`/`sps_epa` aliases are refused.

Duplicate `(obs_id, detector)` rows retain the newest processing version.
Equal-version conflicts and reuse of a frame ID for different metadata fail
explicitly; metadata-equivalent ties use stable frame-ID ordering. Discarded
rows are recorded with processing tag and reason. Output preserves retained
frame metadata and target/release provenance alongside pass assignments.

The existing strict `>30 days` split, detector counts, SPS_EPA sets, and
`stack_ok_by_detector` rule are reused after validation/deduplication. Distinct
frame identities are assigned exactly once by the existing grouping function.

## Scope and missing acceptance [NV]

This is an explicit **B input boundary**, not a claim that an approved shared
canonical manifest schema exists. At implementation time `contracts/` still
contains only its README. The upstream adapter must provide actual IMAGE
timestamps and SPS_EPA; field presence alone cannot prove those values came
from a real manifest or authoritative header. Output retains this limitation.

Per the user's current instruction, no tests were added or executed, and no
compile/import/runtime check was run. Review consisted of reading the live
04-01 task, existing pass code, A's processing-tag/deduplication helpers, and
available shared-contract files, then inspecting the implementation statically.

No canonical frame data, orientations, target durations, Barnard 358-frame
acceptance, Epsilon Indi pass counts, or real `passes.json` results were
fabricated. Those real-data acceptance checks remain pending. No ClickUp or
shared documentation changes were made by this implementation.
