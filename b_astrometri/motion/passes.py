"""04-01: Gecis (pass) gruplama — 30 gun bosluk kurali, passes.json ve pass_of_frame.json.

Kare listesi MJD-AVG (veya mjd) alanina gore siralanir; ardisik iki kare arasi
fark > gap_days (varsayilan 30.0 gun) oldugunda yeni gecis baslar.
Bos liste cokmez: TAP basarisizligi ('unknown') ile kapsam yoklugu
('no_coverage') ayri raporlanir.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


def extract_mjd(frame: dict[str, Any]) -> float:
    """Kareden sonlu MJD degerini (float) cikar."""
    for key in ("MJD-AVG", "mjd_avg", "mjd"):
        if key in frame and frame[key] is not None:
            val = float(frame[key])
            if not math.isfinite(val):
                raise ValueError(f"{key} sonlu olmali")
            return val
    if "time_bounds_lower" in frame and "time_bounds_upper" in frame:
        lo = float(frame["time_bounds_lower"])
        hi = float(frame["time_bounds_upper"])
        mid = 0.5 * (lo + hi)
        if math.isfinite(mid):
            return mid
    raise ValueError("Karede gecerli MJD-AVG / mjd alani yok")


def extract_frame_id(frame: dict[str, Any], index: int) -> str:
    for key in ("frame_id", "uri", "planeid"):
        val = frame.get(key)
        if val:
            return str(val)
    return f"frame_{index}"


def extract_detector(frame: dict[str, Any]) -> str:
    for key in ("detector", "det", "productid"):
        val = frame.get(key)
        if val is not None and str(val) != "":
            return str(val)
    return "unknown"


def group_passes(
    frames: list[dict[str, Any]],
    *,
    gap_days: float = 30.0,
    empty_status: str = "unknown",
) -> dict[str, Any]:
    """Kareleri MJD-AVG'ye gore siralayip > gap_days bosluklarda gecislere bol."""
    if gap_days <= 0 or not math.isfinite(gap_days):
        raise ValueError("gap_days pozitif sonlu olmali")
    if empty_status not in {"unknown", "no_coverage"}:
        raise ValueError("empty_status 'unknown' veya 'no_coverage' olmali")
    if not frames:
        return {"status": empty_status, "gap_days": float(gap_days),
                "n_frames": 0, "n_passes": 0, "passes": [], "gaps": [],
                "pass_of_frame": {}}

    enriched = []
    for idx, f in enumerate(frames):
        enriched.append((extract_mjd(f), extract_frame_id(f, idx),
                         extract_detector(f), f.get("sps_epa", f.get("SPS_EPA"))))
    enriched.sort(key=lambda item: (item[0], item[1]))

    groups: list[list[tuple[float, str, str, Any]]] = []
    gaps: list[dict[str, Any]] = []
    for item in enriched:
        if not groups:
            groups.append([item])
        else:
            previous = groups[-1][-1]
            gap = item[0] - previous[0]
            if gap > gap_days:
                gaps.append({"from_frame": previous[1], "to_frame": item[1],
                             "gap_days": float(gap), "new_pass_id": len(groups) + 1})
                groups.append([item])
            else:
                groups[-1].append(item)

    passes: list[dict[str, Any]] = []
    pass_of_frame: dict[str, int] = {}
    for pid, grp in enumerate(groups, start=1):
        mjds = [x[0] for x in grp]
        det_counts: dict[str, int] = {}
        epas = set()
        for _, fid, det, epa in grp:
            det_counts[det] = det_counts.get(det, 0) + 1
            pass_of_frame[fid] = pid
            if epa is not None and math.isfinite(float(epa)):
                epas.add(float(epa))
        stack_ok_by_det = {d: (c >= 2) for d, c in sorted(det_counts.items())}
        passes.append({
            "id": pid,
            "mjd_min": float(min(mjds)),
            "mjd_max": float(max(mjds)),
            "duration_days": float(max(mjds) - min(mjds)),
            "n_frames": len(grp),
            "detectors": dict(sorted(det_counts.items())),
            "stack_ok_by_detector": stack_ok_by_det,
            "stack_ok": any(stack_ok_by_det.values()),
            "sps_epa": sorted(epas),
        })

    return {
        "status": "ok",
        "gap_days": float(gap_days),
        "n_frames": len(enriched),
        "n_passes": len(passes),
        "passes": passes,
        "gaps": gaps,
        "pass_of_frame": pass_of_frame,
    }


def write_pass_outputs(result: dict[str, Any], out_dir: str | Path) -> tuple[Path, Path]:
    """passes.json ve pass_of_frame.json dosyalarini yaz."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    p_path = out / "passes.json"
    f_path = out / "pass_of_frame.json"
    passes_payload = {k: v for k, v in result.items() if k != "pass_of_frame"}
    p_path.write_text(json.dumps(passes_payload, indent=2), encoding="utf-8")
    f_path.write_text(json.dumps(result.get("pass_of_frame", {}), indent=2), encoding="utf-8")
    return p_path, f_path
