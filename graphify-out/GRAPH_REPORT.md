# Graph Report - planet-x-sphere  (2026-11-15)

## Corpus Check
- Corpus is ~30,696 words - fits in a single context window. You may not need a graph.

## Summary
- 456 nodes · 956 edges · 25 communities (19 shown, 6 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS · INFERRED: 4 edges (avg confidence: 0.85)
- Token cost: unavailable; host agent tools did not expose token usage

## Community Hubs (Navigation)
- Coordinate audit and sparse joint-fit coverage
- Validated Gaia fetch and failure handling
- Epoch propagation and D5 calibration checks
- OUTLIER promotion and moving-object linking
- Forced photometry and light curves
- Centroid covariance and saturated-wing fits
- Exact-TAN display stacks and differences
- Pass grouping
- Sliding-window display and frame roles
- Epoch propagation regression tests
- Contamination vetoes and crowded-field guard
- WiseView epoch comparison
- Pixel-phase bias
- Human data inputs and visual decisions
- Agent workflow and current batch
- ePSF implementation evidence
- Target report template and constraints
- Gaia access evidence and unresolved options
- Real WCS checks and missing target data
- Persistent project memory index
- Task assignments and production dependencies
- ePSF grid internals
- Contribution and handoff workflow
- Unresolved decisions
- Exact reprojection dependency

## God Nodes (most connected - your core abstractions)
1. `numpy (external import)` - 59 edges
2. `math (external import)` - 35 edges
3. `pathlib (external import)` - 23 edges
4. `json (external import)` - 23 edges
5. `unittest (external import)` - 18 edges
6. `FetchTests` - 17 edges
7. `document()` - 16 edges
8. `stack_pass()` - 16 edges
9. `fit_joint_pass()` - 15 edges
10. `EpochTests` - 15 edges

## Surprising Connections (you probably didn't know these)
- `Reject trailing QUERY_STATUS OVERFLOW or ERROR` --semantically_similar_to--> `WISE 0855 archive failure means unknown coverage, not zero`  [INFERRED] [semantically similar]
  docs/GAIA_FETCH.md → b_astrometri/reports/hedefler_sablon.md
- `03-07 task-defined Gaia calibrator quality selection` --references--> `select_calibrators()`  [EXTRACTED]
  docs/second-brain/IMPLEMENTATION.md → b_astrometri/gaia/epoch.py
- `build_lambda_lightcurves()` --writes_status_for--> `04-12 RW Aur and R Dra outputs explicitly UNKNOWN; photometry not run because List 01 coverage failed`  [EXTRACTED]
  b_astrometri/motion/lightcurves.py → b_astrometri/reports/04-12-status/README.md
- `Planet XSphere five-target pixel-precision viewer` --references--> `Second Brain persistent project memory index`  [EXTRACTED]
  README.md → docs/second-brain/README.md
- `D5 100-phase self-recovery on real EPSF templates, not real stars` --references--> `self_recovery_ladder()`  [EXTRACTED]
  b_astrometri/centroid/d5_result.md → b_astrometri/centroid/d5_check.py

## Import Cycles
- 1-file cycle: `b_astrometri/centroid/coord_audit.py -> b_astrometri/centroid/coord_audit.py`
- 1-file cycle: `b_astrometri/centroid/d5_check.py -> b_astrometri/centroid/d5_check.py`
- 1-file cycle: `b_astrometri/centroid/test_d5_check.py -> b_astrometri/centroid/test_d5_check.py`
- 1-file cycle: `b_astrometri/centroid/joint_fit.py -> b_astrometri/centroid/joint_fit.py`
- 1-file cycle: `b_astrometri/centroid/epsf.py -> b_astrometri/centroid/epsf.py`
- 1-file cycle: `b_astrometri/centroid/test_joint_fit.py -> b_astrometri/centroid/test_joint_fit.py`
- 1-file cycle: `b_astrometri/gaia/epoch.py -> b_astrometri/gaia/epoch.py`
- 1-file cycle: `b_astrometri/gaia/fetch.py -> b_astrometri/gaia/fetch.py`
- 1-file cycle: `b_astrometri/motion/test_lightcurves.py -> b_astrometri/motion/test_lightcurves.py`
- 1-file cycle: `b_astrometri/motion/stacks.py -> b_astrometri/motion/stacks.py`
- 1-file cycle: `b_astrometri/movers/outlier_candidates.py -> b_astrometri/movers/outlier_candidates.py`

## Communities (25 total, 6 thin omitted)

### Community 0 - "Coordinate audit and sparse joint-fit coverage"
Cohesion: 0.07
Nodes (17): astropy_io (external import), audit_directory(), audit_source(), _is_timing_expr(), run(), fit_joint_pass(), residuals(), _to_radec() (+9 more)

### Community 1 - "Validated Gaia fetch and failure handling"
Cohesion: 0.07
Nodes (23): argparse (external import), astropy_io_votable (external import), astropy_wcs (external import), atomic_write(), fetch_frame(), fetch_tile(), frame_tiles(), main() (+15 more)

### Community 2 - "Epoch propagation and D5 calibration checks"
Cohesion: 0.08
Nodes (22): D5 100-phase self-recovery on real EPSF templates, not real stars, astropy_coordinates (external import), astropy_table (external import), astropy_time (external import), astropy_units (external import), compare_orientation(), _fit_chi2_nu(), self_recovery_ladder() (+14 more)

### Community 3 - "OUTLIER promotion and moving-object linking"
Cohesion: 0.09
Nodes (14): a_veri_isleme_process_masks (external import), filter_static_detections(), _fit_line(), link_movers(), _positions(), promote_outliers(), score_linked_candidates(), write_candidates() (+6 more)

### Community 4 - "Forced photometry and light curves"
Cohesion: 0.10
Nodes (11): combine_forced_flux(), forced_phot_frame(), _bin_label(), build_lambda_lightcurves(), _lightcurve_svg(), write_lightcurve_outputs(), ForcedPhotTests, LightcurveTests (+3 more)

### Community 5 - "Centroid covariance and saturated-wing fits"
Cohesion: 0.11
Nodes (10): catalog_fields(), coverage_probability(), error_ellipse(), EllipseTests, WingFitTests, fit_epsf_wing(), valid_pixel_mask(), math (external import) (+2 more)

### Community 6 - "Exact-TAN display stacks and differences"
Cohesion: 0.16
Nodes (11): compare_stack_modes(), difference_stacks(), inverse_variance_stack(), _labels(), _same_grid(), stack_pass(), validation_metrics(), write_stack_products() (+3 more)

### Community 7 - "Pass grouping"
Cohesion: 0.20
Nodes (6): extract_detector(), extract_frame_id(), extract_mjd(), group_passes(), write_pass_outputs(), PassGroupingTests

### Community 8 - "Sliding-window display and frame roles"
Cohesion: 0.24
Nodes (5): rolling_window(), frames(), grid(), RollingTests, view()

### Community 10 - "Contamination vetoes and crowded-field guard"
Cohesion: 0.22
Nodes (5): VetoGuardTests, crowded_field_guard(), evaluate_candidate_flags(), tag_candidates(), typing (external import)

### Community 12 - "Pixel-phase bias"
Cohesion: 0.29
Nodes (4): run_phase_sweep(), write_phase_bias_csv(), PhaseBiasTests, csv (external import)

### Community 13 - "Human data inputs and visual decisions"
Cohesion: 0.17
Nodes (10): H-05 pending: 03-05 real images and 02-08/03-03 outputs, H-06 pending: 03-03 production fitter interface for 03-13, H-07 pending: human visual review of phase-bias plots, H-08 pending: forced photometry ePSF/WCS/masks/injection inputs, H-09 pending: WISE 0855 canonical List 01 coverage, H-10 pending: real asteroid inputs and common WCS plane, 04-06 mover linking prototype; real common-plane validation pending, 04-04 WISE 0855 coverage unknown; photometry not run (+2 more)

### Community 14 - "Agent workflow and current batch"
Cohesion: 0.18
Nodes (5): 04-01 pass grouping prototype and measured gap output, Human decisions block only dependent tasks, H-02 resolved: token parsing corrected and live ClickUp access restored, H-03 pending canonical frame manifest and SPS_EPA source, Current Behl?l work status and next dependencies

### Community 15 - "ePSF implementation evidence"
Cohesion: 0.25
Nodes (6): astropy_nddata (external import), Barnard epoch table is prediction with explicit RV=0 assumption, 03-07 epoch prototype: space motion and geometric observer parallax, 03-01 ePSF prototype: 441 or 451 regions, 33x33 samples, 5x5 oversampling, Implementation evidence: 35 Gaia, 14 epoch, 32 centroid tests; D5 100 phases, 03-02 ePSF normalization and orientation

### Community 16 - "Target report template and constraints"
Cohesion: 0.22
Nodes (5): Historical Barnard example: 358 frames, 3 passes, 08-01 six-section target result template, Fixed scope: Barnard, Epsilon Indi B, WISE 0855, RW Aur, R Dra, 08-01 target result template, Planet XSphere five-target pixel-precision viewer

### Community 17 - "Gaia access evidence and unresolved options"
Cohesion: 0.25
Nodes (8): 01-03 Gaia DR3 access decision and validation, Gaia required 11-column schema and G<18 download, ESA large tiles: 2/4 validated; third timed out; no partial output, Provider trials: ESA first, MAST overflow; other mirrors and US machine unverified, Gaia live evidence: reports/gaia-B-small-live-result.json and validated FITS, ESA 128px default validated live: 16/16 tiles, 49,176 sources, Independent geometry audit: all 1048576 B pixel centres covered, 01-03 Gaia fetching

### Community 18 - "Real WCS checks and missing target data"
Cohesion: 0.33
Nodes (6): 04-12 RW Aur and R Dra outputs explicitly UNKNOWN; photometry not run because List 01 coverage failed, 07-04 T1 real-window injection: direct delta x 0.998404 px, np.roll 1.000000 px, tolerance 0.005 px, 07-04 T4 verified on 9 real SIP-3 cutouts: 7569 pixels; max round-trip error 4.47e-11 px, Centroid harness acceptance contract, H-11 pending: 100 real WCS windows and viewer Playwright evidence for 07-04, H-12 pending: RW Aur/R Dra coverage, control star, and 04-03 flux/variance/lambda/pass inputs

### Community 19 - "Persistent project memory index"
Cohesion: 0.38
Nodes (5): Behl?l astrometry and moving-object science: 46 tasks, Second Brain persistent project memory index, Source map: plans, Stage 0 and external local experiment archive, ClickUp snapshot: Behl?l 46 tasks all to do; local progress separate, Behl?l owns astrometry area B

### Community 20 - "Task assignments and production dependencies"
Cohesion: 0.48
Nodes (7): H-01 pending: location or readiness of Akif 02-03 and 02-12 outputs, 02-03 coordinate and pixel rules prerequisite, 02-12 L1 cache prerequisite, 03-01 ePSF model, 03-07 Gaia epoch propagation, 04-03 forced ePSF photometry, Akif owns data integration and image processing area A

## Knowledge Gaps
- **27 isolated node(s):** `astropy_nddata (external import)`, `scipy_sparse (external import)`, `astropy_io_votable (external import)`, `xml_etree (external import)`, `copy (external import)` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 141 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `numpy (external import)` connect `Epoch propagation and D5 calibration checks` to `Coordinate audit and sparse joint-fit coverage`, `OUTLIER promotion and moving-object linking`, `Forced photometry and light curves`, `Centroid covariance and saturated-wing fits`, `Exact-TAN display stacks and differences`, `Sliding-window display and frame roles`, `Contamination vetoes and crowded-field guard`, `Pixel-phase bias`, `ePSF implementation evidence`?**
  _High betweenness centrality (0.340) - this node is a cross-community bridge._
- **What connects `astropy_nddata (external import)`, `scipy_sparse (external import)`, `astropy_io_votable (external import)` to the rest of the system?**
  _27 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Coordinate audit and sparse joint-fit coverage` be split into smaller, more focused modules?**
  _Cohesion score 0.06778476589797344 - nodes in this community are weakly interconnected._
- **Why does `Claude Code Codex session handoff` connect `Contribution and handoff workflow` to `Validated Gaia fetch and failure handling`, `Epoch propagation and D5 calibration checks`, `ePSF implementation evidence`, `Persistent project memory index`, `Task assignments and production dependencies`?**
  _High betweenness centrality (0.168) - this node is a cross-community bridge._
- **Should `Validated Gaia fetch and failure handling` be split into smaller, more focused modules?**
  _Cohesion score 0.07111756168359942 - nodes in this community are weakly interconnected._
- **Why does `math (external import)` connect `Centroid covariance and saturated-wing fits` to `Coordinate audit and sparse joint-fit coverage`, `Validated Gaia fetch and failure handling`, `OUTLIER promotion and moving-object linking`, `Forced photometry and light curves`, `Exact-TAN display stacks and differences`, `Pass grouping`, `Sliding-window display and frame roles`, `Contamination vetoes and crowded-field guard`, `Pixel-phase bias`?**
  _High betweenness centrality (0.152) - this node is a cross-community bridge._
- **Should `Epoch propagation and D5 calibration checks` be split into smaller, more focused modules?**
  _Cohesion score 0.08414634146341464 - nodes in this community are weakly interconnected._

## Memory scope and audit limits

Targeted snapshot of Behlül's project memory, handoff, task/protocol documents and new astrometry code. Archived plans/research/Stage 0 reports and other teams' implementation directories were excluded; linked sources outside this scope were not independently indexed. D5 (03-02) and saturated-core wing-fit (03-05) prototypes are indexed; real-data acceptance remains blocked by human inputs documented in HUMAN_ACTIONS.md.

External dependency nodes are materialized only from explicit AST imports; their package implementations were not indexed.

Semantic extraction token usage was **not exposed by the host collaboration tools**. Zero placeholders in extraction internals are not zero-cost measurements. Cost is unavailable, not measured as zero.

`graphify-out/` shareable outputs are graph.json, GRAPH_REPORT.md, graph.html, health.json, and manifest.json. Interpreter paths, extraction caches, temporary chunks, and the build helper are local working files, not portable source artifacts.

## Graph integrity

- Missing/dangling endpoints: 0/0
- Exact duplicate edges: 0
- Same-endpoint edges collapsed by the simple graph: 8
- Collapse example: `b_astrometri_centroid_joint_coverage_run` → `b_astrometri_centroid_joint_coverage_run_snapshot`; contexts: , call.
- Collapse example: `b_astrometri_centroid_joint_fit_fit_joint_pass` → `b_astrometri_centroid_joint_fit_fit_joint_pass_to_radec`; contexts: , call.
- Collapse example: `b_astrometri_centroid_joint_fit_fit_joint_pass` → `b_astrometri_centroid_joint_fit_fit_joint_pass_residuals`; contexts: , argument.
- Collapse example: `b_astrometri_centroid_phase_bias_write_phase_bias_csv` → `b_astrometri_centroid_phase_bias_py_path`; contexts: parameter_type, return_type.
- Collapse example: `b_astrometri_centroid_wing_fit_fit_epsf_wing` → `b_astrometri_centroid_wing_fit_fit_epsf_wing_residuals`; contexts: , argument.
