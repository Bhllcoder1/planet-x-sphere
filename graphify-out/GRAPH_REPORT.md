# Graph Report - planet-x-sphere  (2026-11-15)

## Corpus Check
- Corpus is ~21,353 words - fits in a single context window. You may not need a graph.

## Summary
- 332 nodes · 615 edges · 17 communities (13 shown, 4 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS · INFERRED: 3 edges (avg confidence: 0.85)
- Token cost: unavailable; host agent tools did not expose token usage

## Community Hubs (Navigation)
- Project workflow, task status and human gates
- Zero-based floating-point coordinate audit
- ePSF calibration and epoch propagation
- Gaia catalogue fetch and tile strategy
- Pixel-phase bias sweep
- Forced ePSF photometry and light curves
- Gaia request transport tests
- Centroid uncertainty and saturated-wing fitting
- Space motion and parallax geometry tests
- WiseView epoch-offset validation
- Moving-object candidate linking
- STREAK GHOST CROSSTALK veto guard
- ePSF grid model implementation
- ePSF grid model unit tests
- Target results and viewer scope
- T1-T4 acceptance and real WCS evidence
- Unresolved project decisions

## God Nodes (most connected - your core abstractions)
1. `numpy (external import)` - 35 edges
2. `math (external import)` - 21 edges
3. `document()` - 15 edges
4. `FetchTests` - 15 edges
5. `unittest (external import)` - 14 edges
6. `pathlib (external import)` - 13 edges
7. `EpochTests` - 12 edges
8. `Session` - 12 edges
9. `group_passes()` - 12 edges
10. `fit_epsf_wing()` - 11 edges

## Surprising Connections (you probably didn't know these)
- `Reject trailing QUERY_STATUS OVERFLOW or ERROR` --semantically_similar_to--> `WISE 0855 archive failure means unknown coverage, not zero`  [INFERRED] [semantically similar]
  docs/GAIA_FETCH.md → b_astrometri/reports/hedefler_sablon.md
- `Planet XSphere five-target pixel-precision viewer` --references--> `Second Brain persistent project memory index`  [EXTRACTED]
  README.md → docs/second-brain/README.md
- `Current Behl?l work status and next dependencies` --references--> `TypeSafe image Box support not validated for astronomy`  [EXTRACTED]
  docs/second-brain/NOW.md → AGENTS.md
- `Parallel agents and persistent handoff workflow` --references--> `Human decisions gate dependent work; independent prototypes continue`  [EXTRACTED]
  AGENTS.md → docs/second-brain/HUMAN_ACTIONS.md
- `Parallel agents and persistent handoff workflow` --references--> `Current Behl?l work status and next dependencies`  [EXTRACTED]
  AGENTS.md → docs/second-brain/NOW.md

## Import Cycles
- 1-file cycle: `b_astrometri/centroid/coord_audit.py -> b_astrometri/centroid/coord_audit.py`
- 1-file cycle: `b_astrometri/centroid/d5_check.py -> b_astrometri/centroid/d5_check.py`
- 1-file cycle: `b_astrometri/centroid/epsf.py -> b_astrometri/centroid/epsf.py`
- 1-file cycle: `b_astrometri/gaia/epoch.py -> b_astrometri/gaia/epoch.py`
- 1-file cycle: `b_astrometri/gaia/fetch.py -> b_astrometri/gaia/fetch.py`
- 1-file cycle: `b_astrometri/gaia/test_fetch.py -> b_astrometri/gaia/test_fetch.py`
- 1-file cycle: `b_astrometri/motion/lightcurves.py -> b_astrometri/motion/lightcurves.py`

## Communities (17 total, 4 thin omitted)

### Community 0 - "Project workflow, task status and human gates"
Cohesion: 0.06
Nodes (42): 04-01 pass grouping prototype and measured gap output, Behl?l astrometry and moving-object science: 46 tasks, Contribution and ownership rules, Human decisions block only dependent tasks, 01-03 Gaia DR3 access decision and validation, Gaia required 11-column schema and G<18 download, ESA large tiles: 2/4 validated; third timed out; no partial output, Provider trials: ESA first, MAST overflow; other mirrors and US machine unverified (+34 more)

### Community 1 - "Zero-based floating-point coordinate audit"
Cohesion: 0.09
Nodes (14): audit_directory(), audit_source(), _is_timing_expr(), CoordAuditTests, extract_detector(), extract_frame_id(), extract_mjd(), group_passes() (+6 more)

### Community 2 - "ePSF calibration and epoch propagation"
Cohesion: 0.11
Nodes (16): astropy_coordinates (external import), astropy_io (external import), astropy_table (external import), astropy_time (external import), astropy_units (external import), compare_orientation(), _fit_chi2_nu(), self_recovery_ladder() (+8 more)

### Community 3 - "Gaia catalogue fetch and tile strategy"
Cohesion: 0.11
Nodes (21): argparse (external import), astropy_io_votable (external import), astropy_wcs (external import), atomic_write(), fetch_frame(), fetch_tile(), frame_tiles(), main() (+13 more)

### Community 4 - "Pixel-phase bias sweep"
Cohesion: 0.13
Nodes (9): run_phase_sweep(), write_phase_bias_csv(), PhaseBiasTests, WingFitTests, fit_epsf_wing(), valid_pixel_mask(), csv (external import), importlib (external import) (+1 more)

### Community 5 - "Forced ePSF photometry and light curves"
Cohesion: 0.13
Nodes (6): combine_forced_flux(), forced_phot_frame(), _bin_label(), build_lambda_lightcurves(), ForcedPhotTests, LightcurveTests

### Community 6 - "Gaia request transport tests"
Cohesion: 0.19
Nodes (3): document(), FetchTests, Session

### Community 7 - "Centroid uncertainty and saturated-wing fitting"
Cohesion: 0.21
Nodes (5): catalog_fields(), coverage_probability(), error_ellipse(), EllipseTests, math (external import)

### Community 10 - "Moving-object candidate linking"
Cohesion: 0.24
Nodes (5): filter_static_detections(), _fit_line(), link_movers(), MoverLinkerTests, typing (external import)

### Community 11 - "STREAK GHOST CROSSTALK veto guard"
Cohesion: 0.26
Nodes (4): VetoGuardTests, crowded_field_guard(), evaluate_candidate_flags(), tag_candidates()

### Community 12 - "ePSF grid model implementation"
Cohesion: 0.18
Nodes (4): astropy_nddata (external import), EPSFGrid, recovery_check(), photutils_psf (external import)

### Community 14 - "Target results and viewer scope"
Cohesion: 0.22
Nodes (5): Historical Barnard example: 358 frames, 3 passes, 08-01 six-section target result template, Fixed scope: Barnard, Epsilon Indi B, WISE 0855, RW Aur, R Dra, 08-01 target result template, Planet XSphere five-target pixel-precision viewer

### Community 15 - "T1-T4 acceptance and real WCS evidence"
Cohesion: 0.67
Nodes (4): 07-04 T1 real-window injection: direct delta x 0.998404 px, np.roll 1.000000 px, tolerance 0.005 px, 07-04 T4 verified on 9 real SIP-3 cutouts: 7569 pixels; max round-trip error 4.47e-11 px, Centroid harness acceptance contract, H-11 pending: 100 real WCS windows and viewer Playwright evidence for 07-04

## Knowledge Gaps
- **22 isolated node(s):** `astropy_nddata (external import)`, `astropy_io_votable (external import)`, `unittest_mock (external import)`, `sys (external import)`, `Historical Barnard example: 358 frames, 3 passes` (+17 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 104 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `numpy (external import)` connect `ePSF calibration and epoch propagation` to `Zero-based floating-point coordinate audit`, `Pixel-phase bias sweep`, `Forced ePSF photometry and light curves`, `Centroid uncertainty and saturated-wing fitting`, `Moving-object candidate linking`, `STREAK GHOST CROSSTALK veto guard`, `ePSF grid model implementation`, `ePSF grid model unit tests`?**
  _High betweenness centrality (0.285) - this node is a cross-community bridge._
- **What connects `astropy_nddata (external import)`, `astropy_io_votable (external import)`, `unittest_mock (external import)` to the rest of the system?**
  _22 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Project workflow, task status and human gates` be split into smaller, more focused modules?**
  _Cohesion score 0.05580693815987934 - nodes in this community are weakly interconnected._
- **Why does `Claude Code Codex session handoff` connect `Project workflow, task status and human gates` to `ePSF calibration and epoch propagation`, `Gaia catalogue fetch and tile strategy`, `ePSF grid model implementation`?**
  _High betweenness centrality (0.190) - this node is a cross-community bridge._
- **Should `Zero-based floating-point coordinate audit` be split into smaller, more focused modules?**
  _Cohesion score 0.09246088193456614 - nodes in this community are weakly interconnected._
- **Why does `math (external import)` connect `Centroid uncertainty and saturated-wing fitting` to `Zero-based floating-point coordinate audit`, `Gaia catalogue fetch and tile strategy`, `Pixel-phase bias sweep`, `Forced ePSF photometry and light curves`, `Moving-object candidate linking`, `STREAK GHOST CROSSTALK veto guard`?**
  _High betweenness centrality (0.150) - this node is a cross-community bridge._
- **Should `ePSF calibration and epoch propagation` be split into smaller, more focused modules?**
  _Cohesion score 0.10588235294117647 - nodes in this community are weakly interconnected._

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
