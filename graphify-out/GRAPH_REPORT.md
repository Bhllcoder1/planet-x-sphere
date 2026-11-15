# Graph Report - planet-x-sphere  (2026-11-15)

## Corpus Check
- Corpus is ~20,525 words - fits in a single context window. You may not need a graph.

## Summary
- 320 nodes · 591 edges · 23 communities (17 shown, 6 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 3 edges (avg confidence: 0.85)
- Token cost: unavailable; host agent tools did not expose token usage

## Community Hubs (Navigation)
- ePSF model and epoch propagation
- Gaia catalogue fetch and retry behavior
- Centroid uncertainty and saturated-wing fitting
- Gaia request and HTTP transport tests
- SPHEREx pass grouping
- Forced ePSF photometry
- Zero-based floating-point coordinate rules
- Pixel-phase bias sweep
- Space motion and parallax geometry tests
- WiseView epoch-offset validation
- Moving-object candidate linking
- STREAK GHOST CROSSTALK veto guard
- Human gates and project task protocol
- ePSF grid model unit tests
- Gaia fetch and epoch evidence
- ePSF dependencies and production integration
- Target reports and viewer scope
- Current status, human gates and TypeSafe boundary
- Second Brain source map and evidence labels
- ePSF grid implementation
- Contribution rules and session handoff
- T1-T4 acceptance and real T4 WCS evidence
- Unresolved project decisions

## God Nodes (most connected - your core abstractions)
1. `numpy (external import)` - 35 edges
2. `math (external import)` - 19 edges
3. `document()` - 15 edges
4. `FetchTests` - 15 edges
5. `pathlib (external import)` - 13 edges
6. `unittest (external import)` - 13 edges
7. `EpochTests` - 12 edges
8. `Session` - 12 edges
9. `group_passes()` - 12 edges
10. `fit_epsf_wing()` - 11 edges

## Surprising Connections (you probably didn't know these)
- `Reject trailing QUERY_STATUS OVERFLOW or ERROR` --semantically_similar_to--> `WISE 0855 archive failure means unknown coverage, not zero`  [INFERRED] [semantically similar]
  docs/GAIA_FETCH.md → b_astrometri/reports/hedefler_sablon.md
- `Planet XSphere five-target pixel-precision viewer` --references--> `Second Brain persistent project memory index`  [EXTRACTED]
  README.md → docs/second-brain/README.md
- `Parallel agents and persistent handoff workflow` --references--> `Human decisions gate dependent work; independent prototypes continue`  [EXTRACTED]
  AGENTS.md → docs/second-brain/HUMAN_ACTIONS.md
- `Parallel agents and persistent handoff workflow` --references--> `Current Behl?l work status and next dependencies`  [EXTRACTED]
  AGENTS.md → docs/second-brain/NOW.md
- `Current Behl?l work status and next dependencies` --references--> `TypeSafe image Box support not validated for astronomy`  [EXTRACTED]
  docs/second-brain/NOW.md → AGENTS.md

## Import Cycles
- 1-file cycle: `b_astrometri/centroid/coord_audit.py -> b_astrometri/centroid/coord_audit.py`
- 1-file cycle: `b_astrometri/centroid/d5_check.py -> b_astrometri/centroid/d5_check.py`
- 1-file cycle: `b_astrometri/centroid/epsf.py -> b_astrometri/centroid/epsf.py`
- 1-file cycle: `b_astrometri/gaia/epoch.py -> b_astrometri/gaia/epoch.py`
- 1-file cycle: `b_astrometri/gaia/fetch.py -> b_astrometri/gaia/fetch.py`
- 1-file cycle: `b_astrometri/gaia/test_fetch.py -> b_astrometri/gaia/test_fetch.py`
- 1-file cycle: `b_astrometri/motion/passes.py -> b_astrometri/motion/passes.py`

## Communities (23 total, 6 thin omitted)

### Community 0 - "ePSF model and epoch propagation"
Cohesion: 0.09
Nodes (19): astropy_coordinates (external import), astropy_io (external import), astropy_nddata (external import), astropy_table (external import), astropy_time (external import), astropy_units (external import), compare_orientation(), _fit_chi2_nu() (+11 more)

### Community 1 - "Gaia catalogue fetch and retry behavior"
Cohesion: 0.11
Nodes (22): argparse (external import), astropy_io_votable (external import), astropy_wcs (external import), atomic_write(), fetch_frame(), fetch_tile(), frame_tiles(), main() (+14 more)

### Community 2 - "Centroid uncertainty and saturated-wing fitting"
Cohesion: 0.12
Nodes (9): catalog_fields(), coverage_probability(), error_ellipse(), EllipseTests, WingFitTests, fit_epsf_wing(), valid_pixel_mask(), math (external import) (+1 more)

### Community 3 - "Gaia request and HTTP transport tests"
Cohesion: 0.19
Nodes (3): document(), FetchTests, Session

### Community 4 - "SPHEREx pass grouping"
Cohesion: 0.20
Nodes (6): extract_detector(), extract_frame_id(), extract_mjd(), group_passes(), write_pass_outputs(), PassGroupingTests

### Community 5 - "Forced ePSF photometry"
Cohesion: 0.18
Nodes (6): combine_forced_flux(), forced_phot_frame(), ForcedPhotTests, importlib (external import), sys (external import), unittest (external import)

### Community 6 - "Zero-based floating-point coordinate rules"
Cohesion: 0.20
Nodes (4): audit_directory(), audit_source(), _is_timing_expr(), CoordAuditTests

### Community 7 - "Pixel-phase bias sweep"
Cohesion: 0.27
Nodes (5): run_phase_sweep(), write_phase_bias_csv(), PhaseBiasTests, csv (external import), pathlib (external import)

### Community 10 - "Moving-object candidate linking"
Cohesion: 0.24
Nodes (5): filter_static_detections(), _fit_line(), link_movers(), MoverLinkerTests, typing (external import)

### Community 11 - "STREAK GHOST CROSSTALK veto guard"
Cohesion: 0.26
Nodes (4): VetoGuardTests, crowded_field_guard(), evaluate_candidate_flags(), tag_candidates()

### Community 12 - "Human gates and project task protocol"
Cohesion: 0.17
Nodes (10): H-05 pending: 03-05 real images and 02-08/03-03 outputs, H-06 pending: 03-03 production fitter interface for 03-13, H-07 pending: human visual review of phase-bias plots, H-08 pending: forced photometry ePSF/WCS/masks/injection inputs, H-09 pending: WISE 0855 canonical List 01 coverage, H-10 pending: real asteroid inputs and common WCS plane, 04-06 mover linking prototype; real common-plane validation pending, 04-04 WISE 0855 coverage unknown; photometry not run (+2 more)

### Community 14 - "Gaia fetch and epoch evidence"
Cohesion: 0.20
Nodes (11): 01-03 Gaia DR3 access decision and validation, Gaia required 11-column schema and G<18 download, ESA large tiles: 2/4 validated; third timed out; no partial output, Provider trials: ESA first, MAST overflow; other mirrors and US machine unverified, Gaia live evidence: reports/gaia-B-small-live-result.json and validated FITS, ESA small tiles: 16/16 OK, 49176 sources, 67.364 seconds, Barnard epoch table is prediction with explicit RV=0 assumption, 03-07 epoch prototype: space motion and geometric observer parallax (+3 more)

### Community 15 - "ePSF dependencies and production integration"
Cohesion: 0.31
Nodes (9): H-01 pending: location or readiness of Akif 02-03 and 02-12 outputs, 03-01 ePSF prototype: 441 or 451 regions, 33x33 samples, 5x5 oversampling, 02-03 coordinate and pixel rules prerequisite, 02-12 L1 cache prerequisite, 03-01 ePSF model, 03-02 ePSF normalization and orientation, 03-07 Gaia epoch propagation, 04-03 forced ePSF photometry (+1 more)

### Community 16 - "Target reports and viewer scope"
Cohesion: 0.22
Nodes (5): Historical Barnard example: 358 frames, 3 passes, 08-01 six-section target result template, Fixed scope: Barnard, Epsilon Indi B, WISE 0855, RW Aur, R Dra, 08-01 target result template, Planet XSphere five-target pixel-precision viewer

### Community 17 - "Current status, human gates and TypeSafe boundary"
Cohesion: 0.29
Nodes (5): 04-01 pass grouping prototype and measured gap output, Human decisions block only dependent tasks, H-02 pending ClickUp token renewal after HTTP 401, H-03 pending canonical frame manifest and SPS_EPA source, Current Behl?l work status and next dependencies

### Community 18 - "Second Brain source map and evidence labels"
Cohesion: 0.38
Nodes (5): Behl?l astrometry and moving-object science: 46 tasks, Second Brain persistent project memory index, Source map: plans, Stage 0 and external local experiment archive, ClickUp snapshot: Behl?l 46 tasks all to do; local progress separate, Behl?l owns astrometry area B

### Community 21 - "T1-T4 acceptance and real T4 WCS evidence"
Cohesion: 0.67
Nodes (3): 07-04 T4 verified on 9 real SIP-3 cutouts: 7569 pixels; max round-trip error 4.47e-11 px, Centroid harness acceptance contract, H-11 pending: 100 real WCS windows and viewer Playwright evidence for 07-04

## Knowledge Gaps
- **24 isolated node(s):** `astropy_nddata (external import)`, `astropy_io_votable (external import)`, `unittest_mock (external import)`, `sys (external import)`, `Historical Barnard example: 358 frames, 3 passes` (+19 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 103 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `numpy (external import)` connect `ePSF model and epoch propagation` to `Centroid uncertainty and saturated-wing fitting`, `Forced ePSF photometry`, `Pixel-phase bias sweep`, `Moving-object candidate linking`, `STREAK GHOST CROSSTALK veto guard`, `ePSF grid model unit tests`?**
  _High betweenness centrality (0.293) - this node is a cross-community bridge._
- **What connects `astropy_nddata (external import)`, `astropy_io_votable (external import)`, `unittest_mock (external import)` to the rest of the system?**
  _24 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ePSF model and epoch propagation` be split into smaller, more focused modules?**
  _Cohesion score 0.08780487804878048 - nodes in this community are weakly interconnected._
- **Why does `Claude Code Codex session handoff` connect `Contribution rules and session handoff` to `ePSF model and epoch propagation`, `Gaia catalogue fetch and retry behavior`, `Gaia fetch and epoch evidence`, `ePSF dependencies and production integration`, `Second Brain source map and evidence labels`?**
  _High betweenness centrality (0.196) - this node is a cross-community bridge._
- **Should `Gaia catalogue fetch and retry behavior` be split into smaller, more focused modules?**
  _Cohesion score 0.10685483870967742 - nodes in this community are weakly interconnected._
- **Why does `pathlib (external import)` connect `Pixel-phase bias sweep` to `ePSF model and epoch propagation`, `Gaia catalogue fetch and retry behavior`, `SPHEREx pass grouping`, `Forced ePSF photometry`, `Zero-based floating-point coordinate rules`?**
  _High betweenness centrality (0.152) - this node is a cross-community bridge._
- **Should `Centroid uncertainty and saturated-wing fitting` be split into smaller, more focused modules?**
  _Cohesion score 0.11822660098522167 - nodes in this community are weakly interconnected._

## Memory scope and audit limits

Targeted snapshot of Behlül's project memory, handoff, task/protocol documents and new astrometry code. Archived plans/research/Stage 0 reports and other teams' implementation directories were excluded; linked sources outside this scope were not independently indexed. D5 (03-02) and saturated-core wing-fit (03-05) prototypes are indexed; real-data acceptance remains blocked by human inputs documented in HUMAN_ACTIONS.md.

External dependency nodes are materialized only from explicit AST imports; their package implementations were not indexed.

Semantic extraction token usage was **not exposed by the host collaboration tools**. Zero placeholders in extraction internals are not zero-cost measurements. Cost is unavailable, not measured as zero.

`graphify-out/` shareable outputs are graph.json, GRAPH_REPORT.md, graph.html, health.json, and manifest.json. Interpreter paths, extraction caches, temporary chunks, and the build helper are local working files, not portable source artifacts.

## Graph integrity

- Missing/dangling endpoints: 0/0
- Exact duplicate edges: 0
- Same-endpoint edges collapsed by the simple graph: 3
- Collapse example: `b_astrometri_centroid_phase_bias_write_phase_bias_csv` → `b_astrometri_centroid_phase_bias_py_path`; contexts: parameter_type, return_type.
- Collapse example: `b_astrometri_centroid_wing_fit_fit_epsf_wing` → `b_astrometri_centroid_wing_fit_fit_epsf_wing_residuals`; contexts: , argument.
- Collapse example: `b_astrometri_motion_passes_write_pass_outputs` → `b_astrometri_motion_passes_py_path`; contexts: generic_arg, parameter_type.
