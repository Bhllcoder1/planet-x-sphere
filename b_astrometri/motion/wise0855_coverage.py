"""08-07: WISE 0855 kapsam tablosu uretici.

TAP sorgulari su an basarisiz (H-09), bu nedenle sentetik yedege duser.
[PARTIAL] Gercek kapsam verileri H-09 (WISE 0855 kapsamı) cozulunce guncellenir.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


WISE0855_RA_DEG = 133.788
WISE0855_DEC_DEG = -7.245

_SYNTHETIC_PASSES: list[dict] = []  # TAP basarisiz: bos liste, durum notu


def build_coverage_table(passes: list[dict[str, Any]]) -> dict[str, Any]:
    """Passes listesinden kapsam tablosu olustur.

    TAP basarisiz oldugundan simdilik bos tablo donuluyor; H-09 bekliyor.
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
    if rows:
        md_lines = [
            "| pass_id | mjd_start | mjd_end | n_frames | mean_cwave_um | snr |",
            "|---|---|---|---|---|---|",
        ]
        for r in rows:
            snr_str = f"{r['snr']:.1f}" if r["snr"] is not None else "H-09 bekleniyor"
            cwave = f"{r['mean_cwave_um']:.3f}" if math.isfinite(r["mean_cwave_um"]) else "unknown"
            md_lines.append(
                f"| {r['pass_id']} | {r['mjd_start']:.1f} | {r['mjd_end']:.1f} "
                f"| {r['n_frames']} | {cwave} | {snr_str} |"
            )
        md_lines.append(f"\nToplam kare: {total_frames} / {len(rows)} gecis")
    else:
        md_lines = [
            "**Durum: TAP sorgulari basarisiz (H-09 bekleniyor)**",
            "",
            "WISE J085510.83-071442.5 kapsam verileri henuz alinamadi.",
            "H-09 (WISE 0855 kapsam gorevi) tamamlaninca bu tablo guncellenecek.",
        ]
    return {
        "target": "WISE 0855",
        "ra_deg": WISE0855_RA_DEG,
        "dec_deg": WISE0855_DEC_DEG,
        "total_frames": total_frames,
        "n_passes": len(rows),
        "tap_status": "FAILED" if not passes else "OK",
        "rows": rows,
        "markdown": "\n".join(md_lines),
        "data_source": "tap_failed_fallback" if not passes else "manifest",
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
        source = "tap_failed_fallback"
    result = build_coverage_table(passes)
    result["data_source"] = source
    print(f"# WISE 0855 Kapsam Tablosu\n")
    print(result["markdown"])
    print(f"\nVeri kaynagi: {source}")
    print("NOT: TAP basarisiz, H-09 bekleniyor.")
