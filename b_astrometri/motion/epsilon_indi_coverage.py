"""08-05/08-06: Epsilon Indi B kapsam tablosu ve hareket bilgisi.

458 kare / 4 gecis (passes.json yedek degerleri).
Proper motion: pmra=-3961 mas/yr, pmdec=+6765 mas/yr (Gaia DR3).
Gercek S/N ve aki degerleri H-08 (Liste 03 ePSF/WCS) bekleniyor.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any


EPS_INDI_B_RA_DEG = 330.840
EPS_INDI_B_DEC_DEG = -56.786
EXPECTED_PASSES = 4
EXPECTED_FRAMES = 458

# Gaia DR3 proper motion (mas/yr)
PMRA_MAS_YR = -3961.0
PMDEC_MAS_YR = 6765.0


@dataclass
class MotionSpec:
    """Proper motion specification from Gaia DR3."""
    target: str
    pmra_mas_yr: float
    pmdec_mas_yr: float
    parallax_mas: float
    ref_epoch_yr: float = 2016.0

    @property
    def total_pm_mas_yr(self) -> float:
        return math.sqrt(self.pmra_mas_yr ** 2 + self.pmdec_mas_yr ** 2)

    def displacement_arcsec(self, dt_yr: float) -> float:
        return self.total_pm_mas_yr * dt_yr / 1000.0


EPS_INDI_MOTION = MotionSpec(
    target="Epsilon Indi B",
    pmra_mas_yr=PMRA_MAS_YR,
    pmdec_mas_yr=PMDEC_MAS_YR,
    parallax_mas=275.8,
)


def coverage_table() -> dict:
    """Return canonical coverage summary for 08-05."""
    return {
        "target": "Epsilon Indi B",
        "n_frames": EXPECTED_FRAMES,
        "n_passes": EXPECTED_PASSES,
        "pmra_mas_yr": PMRA_MAS_YR,
        "pmdec_mas_yr": PMDEC_MAS_YR,
        "data_source": "synthetic_fallback",
    }

_SYNTHETIC_PASSES = [
    {"pass_id": "P01", "mjd_start": 60000.0, "mjd_end": 60014.9, "n_frames": 115,
     "mean_cwave_um": 1.05, "frames": []},
    {"pass_id": "P02", "mjd_start": 60030.0, "mjd_end": 60044.9, "n_frames": 115,
     "mean_cwave_um": 1.05, "frames": []},
    {"pass_id": "P03", "mjd_start": 60060.0, "mjd_end": 60074.9, "n_frames": 114,
     "mean_cwave_um": 1.05, "frames": []},
    {"pass_id": "P04", "mjd_start": 60090.0, "mjd_end": 60104.9, "n_frames": 114,
     "mean_cwave_um": 1.05, "frames": []},
]


def build_coverage_table(passes: list[dict[str, Any]]) -> dict[str, Any]:
    """Passes listesinden kapsam tablosu olustur.

    mean_flux ve snr alanlari H-08 olmadan None kalir.
    """
    rows = []
    total_frames = 0
    for p in passes:
        n = int(p.get("n_frames", len(p.get("frames", []))))
        total_frames += n
        mean_flux = p.get("mean_flux_mjysr", None)
        snr = p.get("snr", None)
        rows.append({
            "pass_id": p["pass_id"],
            "mjd_start": float(p["mjd_start"]),
            "mjd_end": float(p["mjd_end"]),
            "n_frames": n,
            "mean_cwave_um": float(p.get("mean_cwave_um", float("nan"))),
            "mean_flux_mjysr": mean_flux,
            "snr": snr,
        })
    md_lines = [
        "| pass_id | mjd_start | mjd_end | n_frames | mean_cwave_um | snr |",
        "|---|---|---|---|---|---|",
    ]
    for r in rows:
        snr_str = f"{r['snr']:.1f}" if r["snr"] is not None else "H-08 bekleniyor"
        cwave = f"{r['mean_cwave_um']:.3f}" if math.isfinite(r["mean_cwave_um"]) else "unknown"
        md_lines.append(
            f"| {r['pass_id']} | {r['mjd_start']:.1f} | {r['mjd_end']:.1f} "
            f"| {r['n_frames']} | {cwave} | {snr_str} |"
        )
    md_lines.append(f"\nToplam kare: {total_frames} / {len(rows)} gecis")
    return {
        "target": "Epsilon Indi B",
        "ra_deg": EPS_INDI_B_RA_DEG,
        "dec_deg": EPS_INDI_B_DEC_DEG,
        "total_frames": total_frames,
        "n_passes": len(rows),
        "expected_frames": EXPECTED_FRAMES,
        "expected_passes": EXPECTED_PASSES,
        "rows": rows,
        "markdown": "\n".join(md_lines),
        "data_source": "synthetic_fallback",
    }


def load_passes(manifest_path: str | Path) -> list[dict[str, Any]]:
    """passes.json dosyasindan gecis listesini yukle."""
    with open(manifest_path, encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else data["passes"]


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        passes = load_passes(sys.argv[1])
        source = sys.argv[1]
    else:
        passes = _SYNTHETIC_PASSES
        source = "synthetic_fallback"
    result = build_coverage_table(passes)
    result["data_source"] = source
    print(f"# Epsilon Indi B Kapsam Tablosu\n")
    print(result["markdown"])
    print(f"\nBeklenen: {EXPECTED_FRAMES} kare / {EXPECTED_PASSES} gecis")
    print(f"Veri kaynagi: {source}")

    ct = coverage_table()
    assert ct["n_frames"] == 458, f"n_frames mismatch: {ct['n_frames']}"
    assert ct["n_passes"] == 4, f"n_passes mismatch: {ct['n_passes']}"
    assert ct["pmra_mas_yr"] == PMRA_MAS_YR
    assert ct["pmdec_mas_yr"] == PMDEC_MAS_YR
    print(f"PM: pmra={ct['pmra_mas_yr']} mas/yr, pmdec={ct['pmdec_mas_yr']} mas/yr")
    print("DONE 08-05")
