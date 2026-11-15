"""08-02: Barnard Yildizi kapsam tablosu uretici.

Bir JSON kare manifesti (passes.json bicimi) kabul eder ya da sentetik yedege duser.
[PARTIAL] Gercek S/N ve aki degerleri H-08 (Liste 03 ePSF/WCS) bekliyor.
Doygun cekirdek bayragi: Barnard cok parlak, cekirdek doygun [ASSUMPTION].
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


BARNARD_RA_DEG = 269.452
BARNARD_DEC_DEG = 4.693
SATURATION_THRESHOLD_MJYSR = 1e4  # [ASSUMPTION] placeholder

# Sentetik yedek: 358 kare / 3 gecis
_SYNTHETIC_PASSES = [
    {"pass_id": "P01", "mjd_start": 60000.0, "mjd_end": 60014.9, "n_frames": 120,
     "mean_cwave_um": 1.05, "frames": []},
    {"pass_id": "P02", "mjd_start": 60030.0, "mjd_end": 60044.9, "n_frames": 119,
     "mean_cwave_um": 1.05, "frames": []},
    {"pass_id": "P03", "mjd_start": 60060.0, "mjd_end": 60074.9, "n_frames": 119,
     "mean_cwave_um": 1.05, "frames": []},
]


def build_coverage_table(passes: list[dict[str, Any]]) -> dict[str, Any]:
    """Passes listesinden kapsam tablosu olustur.

    Returns dict with 'rows' (list of row dicts) and 'markdown' (str).
    [PARTIAL] mean_flux ve snr alanlari H-08 olmadan None kalir.
    """
    rows = []
    total_frames = 0
    for p in passes:
        n = int(p.get("n_frames", len(p.get("frames", []))))
        total_frames += n
        # Doygun cekirdek: Barnard cok parlak [ASSUMPTION]
        mean_flux = p.get("mean_flux_mjysr", None)
        saturated = True if mean_flux is None else (mean_flux > SATURATION_THRESHOLD_MJYSR)
        rows.append({
            "pass_id": p["pass_id"],
            "mjd_start": float(p["mjd_start"]),
            "mjd_end": float(p["mjd_end"]),
            "n_frames": n,
            "mean_cwave_um": float(p.get("mean_cwave_um", float("nan"))),
            "saturated_core_flag": saturated,
            "mean_flux_mjysr": mean_flux,
            "snr": p.get("snr", None),
        })
    md_lines = [
        "| pass_id | mjd_start | mjd_end | n_frames | mean_cwave_um | saturated_core |",
        "|---|---|---|---|---|---|",
    ]
    for r in rows:
        sat = "YES [ASSUMPTION]" if r["saturated_core_flag"] else "no"
        cwave = f"{r['mean_cwave_um']:.3f}" if math.isfinite(r["mean_cwave_um"]) else "unknown"
        md_lines.append(
            f"| {r['pass_id']} | {r['mjd_start']:.1f} | {r['mjd_end']:.1f} "
            f"| {r['n_frames']} | {cwave} | {sat} |"
        )
    md_lines.append(f"\nToplam kare: {total_frames} / {len(rows)} gecis")
    return {"target": "Barnard's Star", "ra_deg": BARNARD_RA_DEG, "dec_deg": BARNARD_DEC_DEG,
            "total_frames": total_frames, "n_passes": len(rows), "rows": rows,
            "markdown": "\n".join(md_lines), "data_source": "synthetic_fallback"}


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
    print(f"# Barnard Yildizi Kapsam Tablosu\n")
    print(result["markdown"])
    print(f"\nVeri kaynagi: {source}")
    print("NOT: Gercek S/N ve aki degerleri H-08 bekleniyor.")
