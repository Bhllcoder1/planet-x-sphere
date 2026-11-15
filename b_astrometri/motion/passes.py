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
import re
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


def pass_summary(passes: list[dict[str, Any]]) -> dict[str, Any]:
    """Summarise a list of pass dicts (as returned in group_passes result['passes']).

    Returns {n_passes, total_frames, mjd_range_days}.
    mjd_range_days is the span from the earliest mjd_min to the latest mjd_max
    across all passes; 0.0 for an empty list.
    """
    if not passes:
        return {"n_passes": 0, "total_frames": 0, "mjd_range_days": 0.0}
    total_frames = sum(p.get("n_frames", 0) for p in passes)
    mjd_min = min(p["mjd_min"] for p in passes)
    mjd_max = max(p["mjd_max"] for p in passes)
    return {
        "n_passes": len(passes),
        "total_frames": total_frames,
        "mjd_range_days": float(mjd_max - mjd_min),
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


def _required_text(record: dict[str, Any], field: str) -> str:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Manifest requires nonempty string {field}")
    return value.strip()


def _required_number(record: dict[str, Any], field: str) -> float:
    value = record.get(field)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"Manifest requires finite numeric {field}")
    return float(value)


def _processing_order(procver: str) -> tuple[int, int, int]:
    match = re.fullmatch(r"l2b(?:_retry)?-v(\d+)-(\d{4})-(\d+)", procver)
    if match is None:
        raise ValueError("procver must identify l2b-v<version>-<year>-<build> or l2b_retry-v...")
    return tuple(int(part) for part in match.groups())


def load_pass_manifest(path: str | Path) -> dict[str, Any]:
    """Read a JSON manifest object for ``group_manifest_passes``.

    This is B's explicit input boundary, not a replacement for the pending
    shared 02-11 schema. No array-only legacy catalogue is silently promoted
    into a canonical manifest with guessed metadata.
    """
    manifest = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(manifest, dict):
        raise ValueError("Pass manifest must be a JSON object")
    return manifest


def group_manifest_passes(
    manifest: dict[str, Any], *, gap_days: float = 30.0,
) -> dict[str, Any]:
    """Validate/deduplicate an explicitly identified target manifest, then group.

    Required envelope: target_id (stable string), release (DR1 or QR3), status
    (ok/unknown/no_coverage), frames (list). Every frame requires frame_id,
    obs_id, detector (integer 1..6), mjd_avg (IMAGE MJD-AVG), sps_epa (actual
    header value), procver (l2b-v<version>-<year>-<build>). Optional per-frame
    release must agree with the envelope. Times/orientation must already come
    from upstream IMAGE metadata; this function cannot prove their provenance.

    Only newest numeric processing version per (obs_id,detector) is retained.
    Ambiguous tied versions and reused frame identities are rejected rather
    than resolved from row order. Legacy group_passes remains permissive.
    """
    if not isinstance(manifest, dict):
        raise ValueError("Pass manifest must be an object")
    target_id = _required_text(manifest, "target_id")
    release = _required_text(manifest, "release")
    if release not in {"DR1", "QR3"}:
        raise ValueError("Pass manifest requires one explicitly identified DR1 or QR3 release")
    status = manifest.get("status")
    if status not in {"ok", "unknown", "no_coverage"}:
        raise ValueError("Manifest status must be ok, unknown or no_coverage")
    frames = manifest.get("frames")
    if not isinstance(frames, list):
        raise ValueError("Manifest frames must be an explicit list")
    if (frames and status != "ok") or (not frames and status == "ok"):
        raise ValueError("Nonempty frames require status=ok; empty frames require unknown or no_coverage")
    by_identity: dict[str, tuple[Any, ...]] = {}
    best: dict[tuple[str, int], dict[str, Any]] = {}
    dropped = []
    for row in frames:
        if not isinstance(row, dict):
            raise ValueError("Every manifest frame must be an object")
        frame_id = _required_text(row, "frame_id")
        obs_id = _required_text(row, "obs_id")
        detector = row.get("detector")
        if isinstance(detector, bool) or not isinstance(detector, int) or detector not in range(1, 7):
            raise ValueError("Manifest detector must be an integer from 1 to 6")
        if "release" in row and row["release"] != release:
            raise ValueError("Mixed or conflicting releases are not accepted")
        if "target_id" in row and row["target_id"] != target_id:
            raise ValueError("Frame target_id conflicts with the manifest target")
        mjd = _required_number(row, "mjd_avg")
        epa = _required_number(row, "sps_epa")
        procver = _required_text(row, "procver")
        order = _processing_order(procver)
        identity = (obs_id, detector, mjd, epa, release, procver)
        if frame_id in by_identity and by_identity[frame_id] != identity:
            raise ValueError(f"Stable frame_id reused for conflicting metadata: {frame_id}")
        by_identity[frame_id] = identity
        normalized = dict(row, frame_id=frame_id, obs_id=obs_id, detector=detector,
                          mjd_avg=mjd, sps_epa=epa, procver=procver, release=release)
        # Remove permissive aliases so group_passes cannot prefer stale values.
        for alias, canonical in (("MJD-AVG", mjd), ("SPS_EPA", epa)):
            if alias in row and _required_number(row, alias) != canonical:
                raise ValueError(f"Conflicting manifest coordinate/time alias: {alias}")
            normalized.pop(alias, None)
        key = (obs_id, detector)
        previous = best.get(key)
        if previous is None:
            best[key] = normalized
            continue
        previous_order = _processing_order(previous["procver"])
        if order == previous_order:
            if (previous["mjd_avg"], previous["sps_epa"], previous["procver"]) != (mjd, epa, procver):
                raise ValueError(f"Conflicting equal processing versions for observation {obs_id}, detector {detector}")
            kept, discarded = sorted((previous, normalized), key=lambda item: item["frame_id"])
        elif order > previous_order:
            kept, discarded = normalized, previous
        else:
            kept, discarded = previous, normalized
        best[key] = kept
        dropped.append({"frame_id": discarded["frame_id"], "obs_id": obs_id,
                        "detector": detector, "procver": discarded["procver"],
                        "reason": "duplicate observation/detector; newest numeric version retained"})
    retained = sorted(best.values(), key=lambda row: (row["mjd_avg"], row["frame_id"]))
    result = group_passes(retained, gap_days=gap_days,
                          empty_status=status if status != "ok" else "unknown")
    result.update({"target_id": target_id, "release": release,
                   "input_frame_count": len(frames), "duplicates_removed": len(dropped),
                   "discarded_frames": dropped, "frames": retained,
                   "manifest_boundary": "explicit B pass input; shared 02-11 schema pending",
                   "time_source_required": "IMAGE MJD-AVG; supplied upstream, not independently verified",
                   "orientation_source_required": "actual SPS_EPA; supplied upstream, not independently verified"})
    return result
