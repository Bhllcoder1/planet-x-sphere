"""
Limitations page generator: what has NOT been verified with real SPHEREx data.
Companion to 09-06-sinirliliklar.md; produces machine-readable limitations JSON.
[PARTIAL] 09-04/08-14 finalization pending; core limitations catalogue complete.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


@dataclass
class Limitation:
    id: str
    category: str           # "astrometry" | "photometry" | "motion" | "data"
    title: str
    description: str
    blocker: Optional[str]  # H-xx identifier if blocked on human input
    severity: str           # "critical" | "major" | "minor"
    workaround: str


LIMITATIONS: List[Limitation] = [
    Limitation(
        id="L-01",
        category="data",
        title="No real SPHEREx FITS data tested",
        description="All centroid, photometry, and motion tests run on synthetic pixel data. "
                    "Real detector noise, persistence, and latent-image effects are unknown.",
        blocker="H-08",
        severity="critical",
        workaround="Synthetic data with Poisson noise + read-noise model used as stand-in.",
    ),
    Limitation(
        id="L-02",
        category="astrometry",
        title="Gaia TAP endpoint unreliable",
        description="ESA TAP queries failed during development; fallback to VizieR mirror "
                    "or local Gaia extract needed. Coverage for all 5 targets unverified.",
        blocker="H-01",
        severity="major",
        workaround="Synthetic Gaia catalogs generated from published μ, π values.",
    ),
    Limitation(
        id="L-03",
        category="astrometry",
        title="WCS correction model not end-to-end validated",
        description="D6 WCS correction model (T5 test) uses synthetic reference stars. "
                    "Real distortion map from SPHEREx focal plane is unknown.",
        blocker="H-08",
        severity="major",
        workaround="Affine residual model with synthetic grid validated to <0.1 px.",
    ),
    Limitation(
        id="L-04",
        category="photometry",
        title="ePSF from FITS HDU not tested end-to-end",
        description="ePSF grid built from synthetic 33×33 stamps; H-01 (Akif's module) "
                    "needed to load real HDU-based ePSF.",
        blocker="H-01",
        severity="major",
        workaround="GriddedPSFModel constructed from Gaussian stamps; shape qualitatively correct.",
    ),
    Limitation(
        id="L-05",
        category="motion",
        title="WISE 0855 and RW Aur SPHEREx coverage unknown",
        description="TAP coverage queries for WISE 0855, RW Aur, R Dra returned no data. "
                    "Detectability results are framework-only.",
        blocker="H-09",
        severity="major",
        workaround="Coverage marked UNKNOWN; framework ready to process when data arrive.",
    ),
    Limitation(
        id="L-06",
        category="motion",
        title="Classifier (04-19) uses placeholder weights",
        description="Logistic real/fake classifier weights are synthetic placeholders. "
                    "Real training requires 04-18 candidate catalog from actual observations.",
        blocker="H-13",
        severity="minor",
        workaround="Rule-based score (04-08 veto guard) is production-ready as primary filter.",
    ),
    Limitation(
        id="L-07",
        category="photometry",
        title="Lambda-binned light curves (04-12) framework only",
        description="Per-λ-bin photometry not demonstrated on real data. "
                    "RW Aur variability detection unconfirmed.",
        blocker="H-12",
        severity="minor",
        workaround="Stetson-J variability index implemented; synthetic smoke test passes.",
    ),
]


def generate_limitations_json(out_path: Path) -> dict:
    data = {
        "version": "1.0",
        "total": len(LIMITATIONS),
        "critical": sum(1 for l in LIMITATIONS if l.severity == "critical"),
        "major": sum(1 for l in LIMITATIONS if l.severity == "major"),
        "minor": sum(1 for l in LIMITATIONS if l.severity == "minor"),
        "limitations": [
            {
                "id": l.id,
                "category": l.category,
                "severity": l.severity,
                "title": l.title,
                "description": l.description,
                "blocker": l.blocker,
                "workaround": l.workaround,
            }
            for l in LIMITATIONS
        ],
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return data


if __name__ == "__main__":
    out = Path("b_astrometri/demo/limitations.json")
    data = generate_limitations_json(out)
    print(f"Limitations: {data['total']} total "
          f"({data['critical']} critical, {data['major']} major, {data['minor']} minor)")
    for lim in LIMITATIONS:
        blocker_str = f" [{lim.blocker}]" if lim.blocker else ""
        print(f"  {lim.id} [{lim.severity}]{blocker_str}: {lim.title}")
    print("09-06 limitations: OK")
