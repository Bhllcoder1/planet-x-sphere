# Graph Report - planet-x-sphere  (2026-11-15)

## Corpus Check
- Corpus is ~14,550 words - fits in a single context window. You may not need a graph.

## Summary
- 233 nodes · 416 edges · 15 communities (9 shown, 6 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS · INFERRED: 2 edges (avg confidence: 0.85)
- Token cost: unavailable; host agent tools did not expose token usage

## Community Hubs (Navigation)
- Project Workflow, Memory, and Human Gates
- Gaia Fetch Validation
- Astrometry and Epoch Propagation
- SPHEREx Pass Grouping
- Gaia Catalogue Fetch
- Centroid Error Ellipse
- Target Reports and Gaia Evidence
- Coordinate Rules Audit
- Epoch Propagation Tests
- WiseView Epoch Validation
- ePSF Model
- ePSF Unit Tests
- Gaia Fetch Error Tests
- Centroid Harness Specification
- Unresolved Project Decisions

## God Nodes (most connected - your core abstractions)
1. `document()` - 15 edges
2. `FetchTests` - 15 edges
3. `numpy (external import)` - 15 edges
4. `EpochTests` - 12 edges
5. `Session` - 12 edges
6. `group_passes()` - 12 edges
7. `error_ellipse()` - 10 edges
8. `pathlib (external import)` - 10 edges
9. `math (external import)` - 10 edges
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
- 1-file cycle: `b_astrometri/centroid/epsf.py -> b_astrometri/centroid/epsf.py`
- 1-file cycle: `b_astrometri/gaia/epoch.py -> b_astrometri/gaia/epoch.py`
- 1-file cycle: `b_astrometri/gaia/fetch.py -> b_astrometri/gaia/fetch.py`
- 1-file cycle: `b_astrometri/gaia/test_fetch.py -> b_astrometri/gaia/test_fetch.py`
- 1-file cycle: `b_astrometri/motion/passes.py -> b_astrometri/motion/passes.py`

## Communities (15 total, 6 thin omitted)

### Community 0 - "Project Workflow, Memory, and Human Gates"
Cohesion: 0.09
Nodes (26): 04-01 pass grouping prototype and measured gap output, Behl?l astrometry and moving-object science: 46 tasks, Contribution and ownership rules, Human decisions block only dependent tasks, H-01 pending: location or readiness of Akif 02-03 and 02-12 outputs, H-02 pending ClickUp token renewal after HTTP 401, H-03 pending canonical frame manifest and SPS_EPA source, Barnard epoch table is prediction with explicit RV=0 assumption (+18 more)

### Community 1 - "Gaia Fetch Validation"
Cohesion: 0.12
Nodes (8): astropy_wcs (external import), document(), FetchTests, http_error(), Response, Session, requests (external import), unittest_mock (external import)

### Community 2 - "Astrometry and Epoch Propagation"
Cohesion: 0.16
Nodes (12): astropy_coordinates (external import), astropy_io (external import), astropy_table (external import), astropy_time (external import), astropy_units (external import), _finite(), parallax_offsets(), propagate_catalogue() (+4 more)

### Community 3 - "SPHEREx Pass Grouping"
Cohesion: 0.18
Nodes (8): extract_detector(), extract_frame_id(), extract_mjd(), group_passes(), write_pass_outputs(), PassGroupingTests, pathlib (external import), typing (external import)

### Community 4 - "Gaia Catalogue Fetch"
Cohesion: 0.22
Nodes (16): argparse (external import), astropy_io_votable (external import), atomic_write(), fetch_frame(), fetch_tile(), frame_tiles(), main(), parse_catalogue() (+8 more)

### Community 5 - "Centroid Error Ellipse"
Cohesion: 0.21
Nodes (5): catalog_fields(), coverage_probability(), error_ellipse(), EllipseTests, math (external import)

### Community 6 - "Target Reports and Gaia Evidence"
Cohesion: 0.12
Nodes (13): Historical Barnard example: 358 frames, 3 passes, 08-01 six-section target result template, 01-03 Gaia DR3 access decision and validation, Gaia required 11-column schema and G<18 download, ESA large tiles: 2/4 validated; third timed out; no partial output, Provider trials: ESA first, MAST overflow; other mirrors and US machine unverified, Gaia live evidence: reports/gaia-B-small-live-result.json and validated FITS, ESA small tiles: 16/16 OK, 49176 sources, 67.364 seconds (+5 more)

### Community 7 - "Coordinate Rules Audit"
Cohesion: 0.18
Nodes (5): audit_directory(), audit_source(), _is_timing_expr(), CoordAuditTests, unittest (external import)

### Community 10 - "ePSF Model"
Cohesion: 0.18
Nodes (4): astropy_nddata (external import), EPSFGrid, recovery_check(), photutils_psf (external import)

## Knowledge Gaps
- **18 isolated node(s):** `astropy_nddata (external import)`, `photutils_psf (external import)`, `astropy_io_votable (external import)`, `unittest_mock (external import)`, `typing (external import)` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 77 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Claude Code Codex session handoff` connect `Project Workflow, Memory, and Human Gates` to `ePSF Model`, `Astrometry and Epoch Propagation`, `Gaia Catalogue Fetch`?**
  _High betweenness centrality (0.211) - this node is a cross-community bridge._
- **What connects `astropy_nddata (external import)`, `photutils_psf (external import)`, `astropy_io_votable (external import)` to the rest of the system?**
  _18 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Project Workflow, Memory, and Human Gates` be split into smaller, more focused modules?**
  _Cohesion score 0.08888888888888889 - nodes in this community are weakly interconnected._
- **Why does `pathlib (external import)` connect `SPHEREx Pass Grouping` to `Gaia Fetch Validation`, `Astrometry and Epoch Propagation`, `Gaia Catalogue Fetch`, `Coordinate Rules Audit`, `ePSF Model`?**
  _High betweenness centrality (0.206) - this node is a cross-community bridge._
- **Should `Gaia Fetch Validation` be split into smaller, more focused modules?**
  _Cohesion score 0.11827956989247312 - nodes in this community are weakly interconnected._
- **Why does `numpy (external import)` connect `Astrometry and Epoch Propagation` to `ePSF Model`, `ePSF Unit Tests`, `Centroid Error Ellipse`?**
  _High betweenness centrality (0.143) - this node is a cross-community bridge._
- **Should `Target Reports and Gaia Evidence` be split into smaller, more focused modules?**
  _Cohesion score 0.11764705882352941 - nodes in this community are weakly interconnected._

## Memory scope and audit limits

Targeted snapshot of Behlül's project memory, handoff, task/protocol documents and new astrometry code. Archived plans/research/Stage 0 reports and other teams' implementation directories were excluded; linked sources outside this scope were not independently indexed. Concurrent untracked D5 work-in-progress files were excluded pending collaborator review; remove their exact patterns in `.graphify_build.json` and rebuild after they are committed.

External dependency nodes are materialized only from explicit AST imports; their package implementations were not indexed.

Semantic extraction token usage was **not exposed by the host collaboration tools**. Zero placeholders in extraction internals are not zero-cost measurements. Cost is unavailable, not measured as zero.

`graphify-out/` shareable outputs are graph.json, GRAPH_REPORT.md, graph.html, health.json, and manifest.json. Interpreter paths, extraction caches, temporary chunks, and the build helper are local working files, not portable source artifacts.

## Graph integrity

- Missing/dangling endpoints: 0/0
- Exact duplicate edges: 0
- Same-endpoint edges collapsed by the simple graph: 1
- Collapse example: `b_astrometri_motion_passes_write_pass_outputs` → `b_astrometri_motion_passes_py_path`; contexts: generic_arg, parameter_type.
