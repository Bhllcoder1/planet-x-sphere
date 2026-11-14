# Graph Report - planet-x-sphere  (2026-11-15)

## Corpus Check
- Corpus is ~13,084 words - fits in a single context window. You may not need a graph.

## Summary
- 211 nodes · 371 edges · 14 communities (9 shown, 5 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 2 edges (avg confidence: 0.85)
- Token cost: unavailable; host agent tools did not expose token usage

## Community Hubs (Navigation)
- Project Workflow and Memory
- ePSF Model and Centroid Tests
- Gaia Access Tests
- Gaia Catalogue Fetch
- Centroid Error Ellipse
- Astrometry and Epoch Propagation
- Coordinate Rules Audit
- Epoch Propagation Tests
- WiseView Epoch Validation
- ePSF Model
- ePSF Unit Tests
- Project Decisions and Target Reports
- Centroid Harness Specification
- Unresolved Project Decisions

## God Nodes (most connected - your core abstractions)
1. `document()` - 15 edges
2. `FetchTests` - 15 edges
3. `numpy (external import)` - 15 edges
4. `EpochTests` - 12 edges
5. `Session` - 12 edges
6. `error_ellipse()` - 10 edges
7. `H-01 pending: location or readiness of Akif 02-03 and 02-12 outputs` - 10 edges
8. `EPSFTests` - 9 edges
9. `catalogue()` - 9 edges
10. `WiseViewEpochTests` - 9 edges

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

## Communities (14 total, 5 thin omitted)

### Community 0 - "Project Workflow and Memory"
Cohesion: 0.08
Nodes (31): Behl?l astrometry and moving-object science: 46 tasks, Contribution and ownership rules, Human decisions block only dependent tasks, 01-03 Gaia DR3 access decision and validation, Gaia required 11-column schema and G<18 download, ESA large tiles: 2/4 validated; third timed out; no partial output, Provider trials: ESA first, MAST overflow; other mirrors and US machine unverified, Gaia live evidence: reports/gaia-B-small-live-result.json and validated FITS (+23 more)

### Community 1 - "ePSF Model and Centroid Tests"
Cohesion: 0.11
Nodes (10): astropy_io (external import), astropy_table (external import), astropy_wcs (external import), ErrorResponse, http_error(), Response, importlib_util (external import), pathlib (external import) (+2 more)

### Community 2 - "Gaia Access Tests"
Cohesion: 0.19
Nodes (3): document(), FetchTests, Session

### Community 3 - "Gaia Catalogue Fetch"
Cohesion: 0.22
Nodes (17): argparse (external import), astropy_io_votable (external import), atomic_write(), fetch_frame(), fetch_tile(), frame_tiles(), main(), parse_catalogue() (+9 more)

### Community 4 - "Centroid Error Ellipse"
Cohesion: 0.19
Nodes (5): catalog_fields(), coverage_probability(), error_ellipse(), EllipseTests, unittest (external import)

### Community 5 - "Astrometry and Epoch Propagation"
Cohesion: 0.25
Nodes (9): astropy_coordinates (external import), astropy_time (external import), astropy_units (external import), _finite(), parallax_offsets(), propagate_catalogue(), _sky(), space_motion() (+1 more)

### Community 6 - "Coordinate Rules Audit"
Cohesion: 0.20
Nodes (4): audit_directory(), audit_source(), _is_timing_expr(), CoordAuditTests

### Community 9 - "ePSF Model"
Cohesion: 0.18
Nodes (4): astropy_nddata (external import), EPSFGrid, recovery_check(), photutils_psf (external import)

### Community 11 - "Project Decisions and Target Reports"
Cohesion: 0.22
Nodes (5): Historical Barnard example: 358 frames, 3 passes, 08-01 six-section target result template, Fixed scope: Barnard, Epsilon Indi B, WISE 0855, RW Aur, R Dra, 08-01 target result template, Planet XSphere five-target pixel-precision viewer

## Knowledge Gaps
- **15 isolated node(s):** `astropy_nddata (external import)`, `photutils_psf (external import)`, `astropy_io_votable (external import)`, `unittest_mock (external import)`, `Historical Barnard example: 358 frames, 3 passes` (+10 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 69 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Claude Code Codex session handoff` connect `Project Workflow and Memory` to `ePSF Model`, `Gaia Catalogue Fetch`, `Astrometry and Epoch Propagation`?**
  _High betweenness centrality (0.214) - this node is a cross-community bridge._
- **What connects `astropy_nddata (external import)`, `photutils_psf (external import)`, `astropy_io_votable (external import)` to the rest of the system?**
  _15 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Project Workflow and Memory` be split into smaller, more focused modules?**
  _Cohesion score 0.07682926829268293 - nodes in this community are weakly interconnected._
- **Why does `pathlib (external import)` connect `ePSF Model and Centroid Tests` to `ePSF Model`, `Gaia Catalogue Fetch`, `Astrometry and Epoch Propagation`, `Coordinate Rules Audit`?**
  _High betweenness centrality (0.188) - this node is a cross-community bridge._
- **Should `ePSF Model and Centroid Tests` be split into smaller, more focused modules?**
  _Cohesion score 0.10822510822510822 - nodes in this community are weakly interconnected._
- **Why does `numpy (external import)` connect `Astrometry and Epoch Propagation` to `ePSF Model`, `ePSF Unit Tests`, `Centroid Error Ellipse`, `ePSF Model and Centroid Tests`?**
  _High betweenness centrality (0.163) - this node is a cross-community bridge._

## Memory scope and audit limits

Targeted snapshot of Behlül's project memory, handoff, task/protocol documents and new astrometry code. Archived plans/research/Stage 0 reports and other teams' implementation directories were excluded; linked sources outside this scope were not independently indexed.

External dependency nodes are materialized only from explicit AST imports; their package implementations were not indexed.

Semantic extraction token usage was **not exposed by the host collaboration tools**. Zero placeholders in extraction internals are not zero-cost measurements. Cost is unavailable, not measured as zero.

`graphify-out/` was written into the working tree and is currently visible in git status. Commit only outputs the team wants to share, or ignore local generated files.
