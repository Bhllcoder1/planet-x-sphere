# Graph Report - planet-x-sphere  (2026-11-15)

## Corpus Check
- Corpus is ~23,201 words - fits in a single context window. You may not need a graph.

## Summary
- 355 nodes · 681 edges · 19 communities (16 shown, 3 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 5 edges (avg confidence: 0.87)
- Token cost: unavailable; host agent tools did not expose token usage

## Community Hubs (Navigation)
- Project workflow, task status and human gates
- ePSF calibration and epoch propagation
- Centroid uncertainty and saturated-wing fitting
- Forced ePSF photometry and lambda-binned light curves
- Gaia catalogue fetch and tile strategy
- Gaia request transport tests
- SPHEREx pass grouping
- Zero-based floating-point coordinate audit
- STREAK GHOST CROSSTALK veto guard
- Pixel-phase bias sweep
- ePSF grid model unit tests
- Space motion and parallax geometry tests
- WiseView epoch-offset validation
- Moving-object candidate linking
- Target results and viewer scope
- ePSF grid model implementation
- T1-T4 acceptance and real WCS evidence
- Unresolved project decisions
- Community 18

## God Nodes (most connected - your core abstractions)
1. `numpy (external import)` - 38 edges
2. `math (external import)` - 25 edges
3. `document()` - 15 edges
4. `FetchTests` - 15 edges
5. `pathlib (external import)` - 15 edges
6. `unittest (external import)` - 15 edges
7. `build_lambda_lightcurves()` - 13 edges
8. `EPSFTests` - 12 edges
9. `EpochTests` - 12 edges
10. `Session` - 12 edges

## Surprising Connections (you probably didn't know these)
- `Reject trailing QUERY_STATUS OVERFLOW or ERROR` --semantically_similar_to--> `WISE 0855 archive failure means unknown coverage, not zero`  [INFERRED] [semantically similar]
  docs/GAIA_FETCH.md → b_astrometri/reports/hedefler_sablon.md
- `Planet XSphere five-target pixel-precision viewer` --references--> `Second Brain persistent project memory index`  [EXTRACTED]
  README.md → docs/second-brain/README.md
- `build_lambda_lightcurves()` --writes_status_for--> `04-12 RW Aur and R Dra outputs explicitly UNKNOWN; photometry not run because List 01 coverage failed`  [EXTRACTED]
  b_astrometri/motion/lightcurves.py → b_astrometri/reports/04-12-status/README.md
- `Current Behl?l work status and next dependencies` --references--> `TypeSafe image Box support not validated for astronomy`  [EXTRACTED]
  docs/second-brain/NOW.md → AGENTS.md
- `Parallel agents and persistent handoff workflow` --references--> `Human decisions gate dependent work; independent prototypes continue`  [EXTRACTED]
  AGENTS.md → docs/second-brain/HUMAN_ACTIONS.md

## Import Cycles
- 1-file cycle: `b_astrometri/centroid/coord_audit.py -> b_astrometri/centroid/coord_audit.py`
- 1-file cycle: `b_astrometri/centroid/d5_check.py -> b_astrometri/centroid/d5_check.py`
- 1-file cycle: `b_astrometri/centroid/joint_fit.py -> b_astrometri/centroid/joint_fit.py`
- 1-file cycle: `b_astrometri/centroid/epsf.py -> b_astrometri/centroid/epsf.py`
- 1-file cycle: `b_astrometri/centroid/test_joint_fit.py -> b_astrometri/centroid/test_joint_fit.py`
- 1-file cycle: `b_astrometri/gaia/epoch.py -> b_astrometri/gaia/epoch.py`
- 1-file cycle: `b_astrometri/gaia/fetch.py -> b_astrometri/gaia/fetch.py`
- 1-file cycle: `b_astrometri/gaia/test_fetch.py -> b_astrometri/gaia/test_fetch.py`
- 1-file cycle: `b_astrometri/motion/test_lightcurves.py -> b_astrometri/motion/test_lightcurves.py`

## Communities (19 total, 3 thin omitted)

### Community 0 - "Project workflow, task status and human gates"
Cohesion: 0.06
Nodes (42): 04-01 pass grouping prototype and measured gap output, Behl?l astrometry and moving-object science: 46 tasks, Contribution and ownership rules, Human decisions block only dependent tasks, 01-03 Gaia DR3 access decision and validation, Gaia required 11-column schema and G<18 download, ESA large tiles: 2/4 validated; third timed out; no partial output, Provider trials: ESA first, MAST overflow; other mirrors and US machine unverified (+34 more)

### Community 1 - "ePSF calibration and epoch propagation"
Cohesion: 0.10
Nodes (12): catalog_fields(), coverage_probability(), error_ellipse(), fit_joint_pass(), residuals(), _to_radec(), EllipseTests, WingFitTests (+4 more)

### Community 2 - "Centroid uncertainty and saturated-wing fitting"
Cohesion: 0.11
Nodes (17): astropy_coordinates (external import), astropy_table (external import), astropy_time (external import), astropy_units (external import), compare_orientation(), _fit_chi2_nu(), self_recovery_ladder(), D5CheckTests (+9 more)

### Community 3 - "Forced ePSF photometry and lambda-binned light curves"
Cohesion: 0.11
Nodes (22): argparse (external import), astropy_io_votable (external import), astropy_wcs (external import), atomic_write(), fetch_frame(), fetch_tile(), frame_tiles(), main() (+14 more)

### Community 4 - "Gaia catalogue fetch and tile strategy"
Cohesion: 0.15
Nodes (11): 04-12 RW Aur and R Dra outputs explicitly UNKNOWN; photometry not run because List 01 coverage failed, _bin_label(), build_lambda_lightcurves(), _lightcurve_svg(), write_lightcurve_outputs(), LightcurveTests, H-12 pending: RW Aur/R Dra coverage, control star, and 04-03 flux/variance/lambda/pass inputs, html (external import) (+3 more)

### Community 5 - "Gaia request transport tests"
Cohesion: 0.19
Nodes (3): document(), FetchTests, Session

### Community 6 - "SPHEREx pass grouping"
Cohesion: 0.19
Nodes (6): astropy_io (external import), EPSFTests, fixture(), JointFitTests, _rotated_wcs(), unittest (external import)

### Community 7 - "Zero-based floating-point coordinate audit"
Cohesion: 0.20
Nodes (6): extract_detector(), extract_frame_id(), extract_mjd(), group_passes(), write_pass_outputs(), PassGroupingTests

### Community 8 - "STREAK GHOST CROSSTALK veto guard"
Cohesion: 0.20
Nodes (4): audit_directory(), audit_source(), _is_timing_expr(), CoordAuditTests

### Community 9 - "Pixel-phase bias sweep"
Cohesion: 0.22
Nodes (4): combine_forced_flux(), forced_phot_frame(), ForcedPhotTests, sys (external import)

### Community 10 - "ePSF grid model unit tests"
Cohesion: 0.27
Nodes (5): run_phase_sweep(), write_phase_bias_csv(), PhaseBiasTests, csv (external import), pathlib (external import)

### Community 13 - "Moving-object candidate linking"
Cohesion: 0.26
Nodes (4): VetoGuardTests, crowded_field_guard(), evaluate_candidate_flags(), tag_candidates()

### Community 14 - "Target results and viewer scope"
Cohesion: 0.27
Nodes (4): filter_static_detections(), _fit_line(), link_movers(), MoverLinkerTests

### Community 15 - "ePSF grid model implementation"
Cohesion: 0.20
Nodes (3): astropy_nddata (external import), EPSFGrid, recovery_check()

### Community 16 - "T1-T4 acceptance and real WCS evidence"
Cohesion: 0.22
Nodes (5): Historical Barnard example: 358 frames, 3 passes, 08-01 six-section target result template, Fixed scope: Barnard, Epsilon Indi B, WISE 0855, RW Aur, R Dra, 08-01 target result template, Planet XSphere five-target pixel-precision viewer

### Community 17 - "Unresolved project decisions"
Cohesion: 0.67
Nodes (4): 07-04 T1 real-window injection: direct delta x 0.998404 px, np.roll 1.000000 px, tolerance 0.005 px, 07-04 T4 verified on 9 real SIP-3 cutouts: 7569 pixels; max round-trip error 4.47e-11 px, Centroid harness acceptance contract, H-11 pending: 100 real WCS windows and viewer Playwright evidence for 07-04

## Knowledge Gaps
- **24 isolated node(s):** `astropy_nddata (external import)`, `astropy_io_votable (external import)`, `unittest_mock (external import)`, `sys (external import)`, `xml_etree (external import)` (+19 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 111 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `numpy (external import)` connect `Centroid uncertainty and saturated-wing fitting` to `ePSF calibration and epoch propagation`, `SPHEREx pass grouping`, `Pixel-phase bias sweep`, `ePSF grid model unit tests`, `Moving-object candidate linking`, `Target results and viewer scope`, `ePSF grid model implementation`?**
  _High betweenness centrality (0.267) - this node is a cross-community bridge._
- **What connects `astropy_nddata (external import)`, `astropy_io_votable (external import)`, `unittest_mock (external import)` to the rest of the system?**
  _24 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Project workflow, task status and human gates` be split into smaller, more focused modules?**
  _Cohesion score 0.05580693815987934 - nodes in this community are weakly interconnected._
- **Why does `Claude Code Codex session handoff` connect `Project workflow, task status and human gates` to `Centroid uncertainty and saturated-wing fitting`, `Forced ePSF photometry and lambda-binned light curves`, `ePSF grid model implementation`?**
  _High betweenness centrality (0.179) - this node is a cross-community bridge._
- **Should `ePSF calibration and epoch propagation` be split into smaller, more focused modules?**
  _Cohesion score 0.10158730158730159 - nodes in this community are weakly interconnected._
- **Why does `math (external import)` connect `ePSF calibration and epoch propagation` to `Forced ePSF photometry and lambda-binned light curves`, `Gaia catalogue fetch and tile strategy`, `SPHEREx pass grouping`, `Zero-based floating-point coordinate audit`, `Pixel-phase bias sweep`, `ePSF grid model unit tests`, `Moving-object candidate linking`, `Target results and viewer scope`?**
  _High betweenness centrality (0.169) - this node is a cross-community bridge._
- **Should `Centroid uncertainty and saturated-wing fitting` be split into smaller, more focused modules?**
  _Cohesion score 0.10873440285204991 - nodes in this community are weakly interconnected._

## Memory scope and audit limits

Targeted snapshot of Behlül's project memory, handoff, task/protocol documents and new astrometry code. Archived plans/research/Stage 0 reports and other teams' implementation directories were excluded; linked sources outside this scope were not independently indexed. D5 (03-02) and saturated-core wing-fit (03-05) prototypes are indexed; real-data acceptance remains blocked by human inputs documented in HUMAN_ACTIONS.md.

External dependency nodes are materialized only from explicit AST imports; their package implementations were not indexed.

Semantic extraction token usage was **not exposed by the host collaboration tools**. Zero placeholders in extraction internals are not zero-cost measurements. Cost is unavailable, not measured as zero.

`graphify-out/` shareable outputs are graph.json, GRAPH_REPORT.md, graph.html, health.json, and manifest.json. Interpreter paths, extraction caches, temporary chunks, and the build helper are local working files, not portable source artifacts.

## Graph integrity

- Missing/dangling endpoints: 0/0
- Exact duplicate edges: 0
- Same-endpoint edges collapsed by the simple graph: 5
- Collapse example: `b_astrometri_centroid_joint_fit_fit_joint_pass` → `b_astrometri_centroid_joint_fit_fit_joint_pass_to_radec`; contexts: , call.
- Collapse example: `b_astrometri_centroid_joint_fit_fit_joint_pass` → `b_astrometri_centroid_joint_fit_fit_joint_pass_residuals`; contexts: , argument.
- Collapse example: `b_astrometri_centroid_phase_bias_write_phase_bias_csv` → `b_astrometri_centroid_phase_bias_py_path`; contexts: parameter_type, return_type.
- Collapse example: `b_astrometri_centroid_wing_fit_fit_epsf_wing` → `b_astrometri_centroid_wing_fit_fit_epsf_wing_residuals`; contexts: , argument.
- Collapse example: `b_astrometri_motion_passes_write_pass_outputs` → `b_astrometri_motion_passes_py_path`; contexts: generic_arg, parameter_type.
