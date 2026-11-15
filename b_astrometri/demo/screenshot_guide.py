"""
Screenshot guide generator for Q-H1, Q-H2, Q-H3 demo questions.
Produces a JSON manifest of which viewer states to capture and annotate.
[PARTIAL] Live viewer (liste 05/07) needed for actual capture; guide logic complete.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List


@dataclass
class ScreenshotSpec:
    """Specification for a single demo screenshot."""
    id: str                   # e.g. "Q-H1-a"
    question: str             # demo question being illustrated
    viewer_state: str         # what the viewer should show
    highlight: List[str]      # UI elements to annotate
    caption: str
    file_name: str            # suggested output filename


SCREENSHOT_SPECS: List[ScreenshotSpec] = [
    # Q-H1: Barnard's Star
    ScreenshotSpec(
        id="Q-H1-a",
        question="Q-H1: Can we detect Barnard's Star moving?",
        viewer_state="Barnard blink panel, pass 1 vs pass 4",
        highlight=["motion_vector_overlay", "wcs_badge", "saturated_core_warning"],
        caption="Barnard blink: 4-pass position shift visible (~10 arcsec/yr). "
                "Orange badge: saturated core — wing-fit centroid used.",
        file_name="q-h1-barnard-blink.png",
    ),
    ScreenshotSpec(
        id="Q-H1-b",
        question="Q-H1: Proper motion measurement panel",
        viewer_state="Barnard motion measurement panel",
        highlight=["proper_motion_fit", "chi2_dof", "gaia_comparison"],
        caption="PM fit: vRA ~10890 mas/yr ±X, vDec ~-4697 mas/yr ±Y. "
                "Gaia DR3 reference shown for comparison.",
        file_name="q-h1-barnard-pm-fit.png",
    ),
    # Q-H2: Epsilon Indi B
    ScreenshotSpec(
        id="Q-H2-a",
        question="Q-H2: Is epsilon Indi B detectable?",
        viewer_state="eps Indi B forced-phot results, 4 passes",
        highlight=["snr_per_pass", "combined_snr", "brown_dwarf_badge"],
        caption="eps Indi B: combined S/N ~[TBD] from 4 passes. "
                "Brown dwarf companion badge; no variability flag.",
        file_name="q-h2-eps-indi-b-detect.png",
    ),
    ScreenshotSpec(
        id="Q-H2-b",
        question="Q-H2: Coverage table for epsilon Indi B",
        viewer_state="eps Indi B coverage table",
        highlight=["n_frames", "n_passes", "mjd_range"],
        caption="458 frames across 4 passes; baseline ~[TBD] days.",
        file_name="q-h2-eps-indi-b-coverage.png",
    ),
    # Q-H3: WISE 0855
    ScreenshotSpec(
        id="Q-H3-a",
        question="Q-H3: Can SPHEREx detect WISE 0855?",
        viewer_state="WISE 0855 forced-phot upper limit panel",
        highlight=["coverage_unknown_badge", "upper_limit_arrow", "tap_failed_note"],
        caption="WISE 0855 coverage: unknown (TAP query failed). "
                "Forced phot upper limit shown; real data needed.",
        file_name="q-h3-wise0855-upper-limit.png",
    ),
]


def generate_manifest(out_path: Path) -> Dict:
    """Write screenshot manifest JSON and return it."""
    manifest = {
        "version": "1.0",
        "total_screenshots": len(SCREENSHOT_SPECS),
        "screenshots": [
            {
                "id": s.id,
                "question": s.question,
                "viewer_state": s.viewer_state,
                "highlight": s.highlight,
                "caption": s.caption,
                "file_name": s.file_name,
            }
            for s in SCREENSHOT_SPECS
        ],
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


if __name__ == "__main__":
    out = Path("b_astrometri/demo/screenshot_manifest.json")
    manifest = generate_manifest(out)
    print(f"Screenshot manifest: {manifest['total_screenshots']} specs")
    for s in SCREENSHOT_SPECS:
        print(f"  [{s.id}] {s.file_name} — {s.question[:55]}")
    print(f"Manifest written to {out}")
    print("09-07 screenshot_guide: OK")
