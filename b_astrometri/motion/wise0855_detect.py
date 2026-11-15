"""
WISE 0855 detectability: forced photometry + inverse-variance coadd over passes.
[PARTIAL] H-09 (WISE 0855 SPHEREx coverage) + H-08 (real FITS) needed.
Provides the detection framework; fill passes_snr with real values when data arrive.
"""
from __future__ import annotations
import math
import numpy as np
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class PassPhotometry:
    pass_id: str
    mjd_mid: float
    flux_adu: float
    flux_err_adu: float

    @property
    def snr(self) -> float:
        if self.flux_err_adu <= 0:
            return 0.0
        return self.flux_adu / self.flux_err_adu


@dataclass
class DetectabilityResult:
    target: str = "WISE_J085510.83-071442.5"
    n_passes: int = 0
    combined_snr: float = 0.0
    detection_flag: bool = False
    passes: List[PassPhotometry] = field(default_factory=list)
    notes: str = ""

    def summary(self) -> dict:
        return {
            "target": self.target,
            "n_passes": self.n_passes,
            "combined_snr": round(self.combined_snr, 3),
            "detected_5sigma": self.detection_flag,
            "notes": self.notes,
        }


def combine_passes_inverse_variance(passes: List[PassPhotometry]) -> float:
    """Inverse-variance weighted combination of per-pass S/N values."""
    total_w = 0.0
    total_wf = 0.0
    for p in passes:
        if p.flux_err_adu > 0:
            w = 1.0 / (p.flux_err_adu ** 2)
            total_w += w
            total_wf += w * p.flux_adu
    if total_w <= 0:
        return 0.0
    combined_flux = total_wf / total_w
    combined_err = math.sqrt(1.0 / total_w)
    return combined_flux / combined_err if combined_err > 0 else 0.0


def assess_detectability(passes: List[PassPhotometry], snr_threshold: float = 5.0) -> DetectabilityResult:
    """Assess if WISE 0855 is detectable across given forced-photometry passes."""
    combined = combine_passes_inverse_variance(passes)
    return DetectabilityResult(
        n_passes=len(passes),
        combined_snr=combined,
        detection_flag=combined >= snr_threshold,
        passes=passes,
        notes=f"[STUB] real data from H-09/H-08 needed; threshold={snr_threshold}σ",
    )


if __name__ == "__main__":
    # Synthetic smoke test: inject faint source
    rng = np.random.default_rng(7)
    # WISE 0855 expected ~ T=14.3 W2 → faint SPHEREx source, ~2–3σ per pass
    passes = [
        PassPhotometry(pass_id=f"pass_{i}", mjd_mid=60000.0 + i * 90,
                       flux_adu=rng.normal(10.0, 5.0), flux_err_adu=5.0)
        for i in range(6)
    ]
    result = assess_detectability(passes)
    print(result.summary())
    print(f"Per-pass SNR: {[f'{p.snr:.2f}' for p in passes]}")
    print("04-04 wise0855_detect: OK")
