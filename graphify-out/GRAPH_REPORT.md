# Graph Report - planet-x-sphere  (2026-11-15)

## Corpus Check
- Corpus is ~15,865 words - fits in a single context window. You may not need a graph.

## Summary
- 259 nodes · 468 edges · 14 communities (10 shown, 4 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 3 edges (avg confidence: 0.85)
- Token cost: unavailable; host agent tools did not expose token usage

## Community Hubs (Navigation)
- Project Workflow and Human Gates
- D5 ePSF Calibration Checks
- Gaia Catalogue Fetch
- Centroid Error Ellipse and Wing Fit
- Shared Request and Error Utilities
- SPHEREx Pass Grouping
- Target Reports and Pixel Viewer
- ePSF Grid and Unit Tests
- Coordinate Rules Audit
- Epoch and Parallax Tests
- WiseView Epoch Validation
- ePSF Grid Model
- Centroid Acceptance Contract
- Unresolved Project Decisions

## God Nodes (most connected - your core abstractions)
1. `numpy (external import)` - 24 edges
2. `document()` - 15 edges
3. `FetchTests` - 15 edges
4. `EpochTests` - 12 edges
5. `Session` - 12 edges
6. `group_passes()` - 12 edges
7. `math (external import)` - 11 edges
8. `error_ellipse()` - 10 edges
9. `pathlib (external import)` - 10 edges
10. `H-01 pending: location or readiness of Akif 02-03 and 02-12 outputs` - 10 edges

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
- 1-file cycle: `b_astrometri/motion/passes.py -> b_astrometri/motion/passes.py`

## Communities (14 total, 4 thin omitted)

### Community 0 - "Project Workflow and Human Gates"
Cohesion: 0.09
Nodes (27): 04-01 pass grouping prototype and measured gap output, Behl?l astrometry and moving-object science: 46 tasks, Contribution and ownership rules, Human decisions block only dependent tasks, H-01 pending: location or readiness of Akif 02-03 and 02-12 outputs, H-02 pending ClickUp token renewal after HTTP 401, H-03 pending canonical frame manifest and SPS_EPA source, H-05 pending: 03-05 real images and 02-08/03-03 outputs (+19 more)

### Community 1 - "D5 ePSF Calibration Checks"
Cohesion: 0.11
Nodes (17): astropy_coordinates (external import), astropy_table (external import), astropy_time (external import), astropy_units (external import), compare_orientation(), _fit_chi2_nu(), self_recovery_ladder(), D5CheckTests (+9 more)

### Community 2 - "Gaia Catalogue Fetch"
Cohesion: 0.11
Nodes (22): argparse (external import), astropy_io_votable (external import), astropy_wcs (external import), atomic_write(), fetch_frame(), fetch_tile(), frame_tiles(), main() (+14 more)

### Community 3 - "Centroid Error Ellipse and Wing Fit"
Cohesion: 0.11
Nodes (9): catalog_fields(), coverage_probability(), error_ellipse(), EllipseTests, WingFitTests, fit_epsf_wing(), valid_pixel_mask(), math (external import) (+1 more)

### Community 4 - "Shared Request and Error Utilities"
Cohesion: 0.19
Nodes (3): document(), FetchTests, Session

### Community 5 - "SPHEREx Pass Grouping"
Cohesion: 0.18
Nodes (8): extract_detector(), extract_frame_id(), extract_mjd(), group_passes(), write_pass_outputs(), PassGroupingTests, pathlib (external import), typing (external import)

### Community 6 - "Target Reports and Pixel Viewer"
Cohesion: 0.12
Nodes (13): Historical Barnard example: 358 frames, 3 passes, 08-01 six-section target result template, 01-03 Gaia DR3 access decision and validation, Gaia required 11-column schema and G<18 download, ESA large tiles: 2/4 validated; third timed out; no partial output, Provider trials: ESA first, MAST overflow; other mirrors and US machine unverified, Gaia live evidence: reports/gaia-B-small-live-result.json and validated FITS, ESA small tiles: 16/16 OK, 49176 sources, 67.364 seconds (+5 more)

### Community 7 - "ePSF Grid and Unit Tests"
Cohesion: 0.23
Nodes (4): astropy_io (external import), EPSFTests, fixture(), importlib_util (external import)

### Community 8 - "Coordinate Rules Audit"
Cohesion: 0.22
Nodes (4): audit_directory(), audit_source(), _is_timing_expr(), CoordAuditTests

### Community 11 - "ePSF Grid Model"
Cohesion: 0.20
Nodes (3): astropy_nddata (external import), EPSFGrid, recovery_check()

## Knowledge Gaps
- **18 isolated node(s):** `astropy_nddata (external import)`, `astropy_io_votable (external import)`, `unittest_mock (external import)`, `typing (external import)`, `Historical Barnard example: 358 frames, 3 passes` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 84 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `numpy (external import)` connect `D5 ePSF Calibration Checks` to `ePSF Grid Model`, `Centroid Error Ellipse and Wing Fit`, `ePSF Grid and Unit Tests`?**
  _High betweenness centrality (0.233) - this node is a cross-community bridge._
- **What connects `astropy_nddata (external import)`, `astropy_io_votable (external import)`, `unittest_mock (external import)` to the rest of the system?**
  _18 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Project Workflow and Human Gates` be split into smaller, more focused modules?**
  _Cohesion score 0.08558558558558559 - nodes in this community are weakly interconnected._
- **Why does `Claude Code Codex session handoff` connect `Project Workflow and Human Gates` to `D5 ePSF Calibration Checks`, `Gaia Catalogue Fetch`, `ePSF Grid Model`?**
  _High betweenness centrality (0.200) - this node is a cross-community bridge._
- **Should `D5 ePSF Calibration Checks` be split into smaller, more focused modules?**
  _Cohesion score 0.11051693404634581 - nodes in this community are weakly interconnected._
- **Why does `pathlib (external import)` connect `SPHEREx Pass Grouping` to `D5 ePSF Calibration Checks`, `Gaia Catalogue Fetch`, `ePSF Grid and Unit Tests`, `Coordinate Rules Audit`, `ePSF Grid Model`?**
  _High betweenness centrality (0.170) - this node is a cross-community bridge._
- **Should `Gaia Catalogue Fetch` be split into smaller, more focused modules?**
  _Cohesion score 0.10685483870967742 - nodes in this community are weakly interconnected._

## Memory scope and audit limits

Targeted snapshot of Behlül's project memory, handoff, task/protocol documents and new astrometry code. Archived plans/research/Stage 0 reports and other teams' implementation directories were excluded; linked sources outside this scope were not independently indexed. D5 (03-02) and saturated-core wing-fit (03-05) prototypes are indexed; real-data acceptance remains blocked by human inputs documented in HUMAN_ACTIONS.md.

External dependency nodes are materialized only from explicit AST imports; their package implementations were not indexed.

Semantic extraction token usage was **not exposed by the host collaboration tools**. Zero placeholders in extraction internals are not zero-cost measurements. Cost is unavailable, not measured as zero.

`graphify-out/` shareable outputs are graph.json, GRAPH_REPORT.md, graph.html, health.json, and manifest.json. Interpreter paths, extraction caches, temporary chunks, and the build helper are local working files, not portable source artifacts.

## Graph integrity

- Missing/dangling endpoints: 0/0
- Exact duplicate edges: 0
- Same-endpoint edges collapsed by the simple graph: 2
- Collapse example: `b_astrometri_centroid_wing_fit_fit_epsf_wing` → `b_astrometri_centroid_wing_fit_fit_epsf_wing_residuals`; contexts: , argument.
- Collapse example: `b_astrometri_motion_passes_write_pass_outputs` → `b_astrometri_motion_passes_py_path`; contexts: generic_arg, parameter_type.
