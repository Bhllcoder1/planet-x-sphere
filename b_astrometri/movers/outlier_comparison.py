"""01-12/R27: descriptive OUTLIER/SOURCE fractions, never a causal diagnosis.

Caller provides ten FLAGS windows from the same declared sparse sky region,
detector and release. No remote reads or mutable source products are involved.
"""
from __future__ import annotations

import csv
from collections import defaultdict
import json
from pathlib import Path
import re

import numpy as np

from a_veri_isleme.process.masks import MASK_OUTLIER, MASK_SOURCE


def compare_outlier_frames(frames: list[dict]) -> dict:
    """Return per-frame and week/pipeline descriptive statistics for ten frames.

    Required metadata: frame_id, week (YYYYWww), procver, field_id, region_id,
    detector (1..6), release, sparse_field=True and flags (2D integer bitmap).
    Optional region_mask is boolean support on a common sky region, NOT a
    science-quality mask. The caller must establish that region_id has the same
    sky footprint across rotated WCS windows; array shape alone cannot do that.
    """
    if len(frames) != 10:
        raise ValueError("01-12 requires ten frames from one sparse field")
    rows = []
    control = None
    seen = set()
    for frame in frames:
        metadata = {}
        for key in ("frame_id", "week", "procver", "field_id", "region_id", "release"):
            value = frame.get(key)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{key} must be a nonempty metadata string")
            metadata[key] = value
        if metadata["frame_id"] in seen:
            raise ValueError("Duplicate frame_id would count the same frame twice")
        seen.add(metadata["frame_id"])
        if not re.fullmatch(r"\d{4}W(?:0[1-9]|[1-4][0-9]|5[0-3])", metadata["week"]):
            raise ValueError("week must use the archive YYYYWww label")
        detector = frame.get("detector")
        if isinstance(detector, bool) or not isinstance(detector, (int, np.integer)) or not 1 <= detector <= 6:
            raise ValueError("detector must be an integer from 1 through 6")
        if frame.get("sparse_field") is not True:
            raise ValueError("Caller must document sparse-field selection explicitly")
        flags = np.asarray(frame["flags"])
        if flags.ndim != 2 or flags.size == 0 or flags.dtype.kind not in "ui":
            raise ValueError("FLAGS must be a nonempty two-dimensional integer bitmap")
        if np.any(flags < 0) or np.any(flags > np.iinfo(np.uint32).max):
            raise ValueError("FLAGS values must fit an unsigned 32-bit bitmap")
        support = np.asarray(frame.get("region_mask", np.ones(flags.shape, dtype=bool)))
        if support.dtype.kind != "b" or support.shape != flags.shape:
            raise ValueError("region_mask must be boolean and match FLAGS shape")
        if np.any(np.ma.getmaskarray(frame.get("region_mask", False))):
            raise ValueError("region_mask cannot itself contain unknown mask values")
        if np.any(np.ma.getmaskarray(frame["flags"]) & support):
            raise ValueError("Masked FLAGS values cannot count as measured pixels")
        n_pixels = int(np.count_nonzero(support))
        if not n_pixels:
            raise ValueError("region_mask cannot select an empty region")
        current_control = (metadata["field_id"], metadata["region_id"], int(detector),
                           metadata["release"], flags.shape, n_pixels)
        if control is None:
            control = current_control
        elif current_control != control:
            raise ValueError("Use the same field, sky region, detector, release, shape and sample size")
        selected = flags[support]
        n_outlier = int(np.count_nonzero(selected & MASK_OUTLIER))
        n_source = int(np.count_nonzero(selected & MASK_SOURCE))
        rows.append({**metadata, "detector": int(detector), "n_pixels": n_pixels,
                     "n_outlier": n_outlier, "n_source": n_source,
                     "n_outlier_and_source": int(np.count_nonzero(((selected & MASK_OUTLIER) != 0) &
                                                                    ((selected & MASK_SOURCE) != 0))),
                     "outlier_fraction": n_outlier / n_pixels,
                     "source_fraction": n_source / n_pixels})
    if len({row["week"] for row in rows}) < 2:
        raise ValueError("The week comparison requires frames from different weeks")
    grouped = defaultdict(list)
    for row in rows:
        grouped[(row["week"], row["procver"])].append(row)
    groups = []
    for (week, procver), values in sorted(grouped.items()):
        pixels = sum(v["n_pixels"] for v in values)
        groups.append({"week": week, "procver": procver, "n_frames": len(values),
                       "n_pixels": pixels,
                       "outlier_fraction": sum(v["n_outlier"] for v in values) / pixels,
                       "source_fraction": sum(v["n_source"] for v in values) / pixels})
    weeks_by_procver, procvers_by_week = defaultdict(set), defaultdict(set)
    for row in rows:
        weeks_by_procver[row["procver"]].add(row["week"])
        procvers_by_week[row["week"]].add(row["procver"])
    return {"task": "01-12", "n_frames": len(rows), "frames": rows,
            "week_pipeline_groups": groups,
            "has_week_contrast_at_fixed_procver": any(len(v) > 1 for v in weeks_by_procver.values()),
            "has_procver_contrast_at_fixed_week": any(len(v) > 1 for v in procvers_by_week.values()),
            "fraction_denominator": "all pixels in caller-declared common sky support; no quality-mask exclusion",
            "control_note": "same field/region/detector/release/shape/sample size checked; sky-footprint identity and sparsity are caller assertions",
            "conclusion": "[NV] OUTLIER cause remains unknown; measured fractions are observational, not causal evidence",
            "risk_R27_closed": False}


def write_outlier_comparison(result: dict, output_directory: str | Path) -> None:
    """Write the task CSV and companion JSON; downloaded FLAGS stay external."""
    payload = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)
    directory = Path(output_directory)
    directory.mkdir(parents=True, exist_ok=True)
    columns = ("frame_id", "week", "procver", "field_id", "region_id", "detector", "release",
               "n_pixels", "n_outlier", "n_source", "n_outlier_and_source", "outlier_fraction", "source_fraction")
    with (directory / "outlier_by_week.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows(result["frames"])
    (directory / "outlier_by_week.json").write_text(payload + "\n", encoding="utf-8")
