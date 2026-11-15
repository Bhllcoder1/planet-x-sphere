"""04-07: compact OUTLIER evidence, preserving ordinary detections and SOURCE.

Input/output x,y are window-local native pixels. Convert all detections to a
common tangent plane before calling linker.link_movers across different frames.
Flag-component centers are geometric candidates, not precision centroids.
"""
from copy import deepcopy
import json
import math
from pathlib import Path

import numpy as np
from scipy.ndimage import find_objects, label
from scipy.spatial import cKDTree

from a_veri_isleme.process.masks import (
    MASK_OUTLIER, MASK_SOURCE, PROFILE_MOVER_MASK, build_pixel_mask,
)


def _positions(values):
    points = np.asarray(values, dtype=float)
    if points.size == 0:
        return np.empty((0, 2))
    if points.ndim != 2 or points.shape[1] != 2 or not np.isfinite(points).all():
        raise ValueError("Positions must be finite (x,y) pairs in this FLAGS window")
    return points


def promote_outliers(flags, detections, *, frame_id, mjd, catalog_positions,
                     match_radius_px=3.0, detection_radius_px=1.5,
                     score_bonus=1.0, static_positions=None):
    """Return merged detections, component log and measured promotion statistics.

catalog_positions is required: supply the actual Gaia/catalogue query result,
including an explicitly empty result. score_bonus is uncalibrated [ASSUMPTION].
Existing detections are retained even when this frame has no OUTLIER pixels.
"""
    array = np.asarray(flags)
    if (array.ndim != 2 or not array.size or array.dtype.kind not in "iu"
            or np.any(array < 0) or np.any(array > np.iinfo(np.uint32).max)):
        raise ValueError("FLAGS must be a nonempty 2D uint32-compatible integer array")
    if not all(math.isfinite(v) for v in (mjd, match_radius_px, detection_radius_px, score_bonus)):
        raise ValueError("MJD, radii and bonus must be finite")
    if match_radius_px < 0 or detection_radius_px < 0 or score_bonus < 0:
        raise ValueError("Radii and bonus must be nonnegative")
    array = array.astype(np.uint32, copy=False)
    merged = deepcopy(detections)
    for detection in merged:
        if detection["frame_id"] != frame_id or float(detection["mjd"]) != float(mjd):
            raise ValueError("All detections must belong to the supplied frame and MJD")
        if not np.isfinite([detection["x"], detection["y"]]).all():
            raise ValueError("Non-finite detection coordinates")
    ids = [d["det_id"] for d in merged]
    used_ids = set(ids)
    if len(used_ids) != len(ids):
        raise ValueError("Duplicate detection IDs within frame")
    catalogs = _positions(catalog_positions)
    matched_positions = _positions([(d["x"], d["y"]) for d in merged if d.get("catalog_match", False)])
    catalogs = np.concatenate((catalogs, matched_positions))
    catalog_tree = cKDTree(catalogs) if len(catalogs) else None
    detection_points = _positions([(d["x"], d["y"]) for d in merged])
    detection_tree = cKDTree(detection_points) if len(detection_points) else None
    masked = build_pixel_mask(array, profile="mover_search")
    components, count = label((array & MASK_OUTLIER) != 0, structure=np.ones((3, 3)))
    records, candidates = [], []
    for number, bounds in enumerate(find_objects(components), start=1):
        pixels = components[bounds] == number
        size = int(pixels.sum())
        record = {"component": number, "size_px": size}
        # Count raw component size before removing fit-mask pixels; a large
        # component must not become several false compact sources after masking.
        usable = pixels & ~masked[bounds]
        if size > 40:
            record["reason"] = "noncompact_gt40"
        elif not usable.any():
            record["reason"] = "fit_masked"
        else:
            yy, xx = np.nonzero(usable)
            x, y = float(xx.mean() + bounds[1].start), float(yy.mean() + bounds[0].start)
            record.update(x=x, y=y, usable_pixels=int(usable.sum()),
                          source_overlap=bool(np.any(array[bounds][usable] & MASK_SOURCE)))
            distance = catalog_tree.query([x, y])[0] if catalog_tree is not None else math.inf
            if distance <= match_radius_px:
                record["reason"] = "catalog_match"
            else:
                record["reason"] = "promoted"
                distance, index = (detection_tree.query([x, y]) if detection_tree is not None
                                   else (math.inf, None))
                if distance <= detection_radius_px:
                    detection = merged[int(index)]
                else:
                    det_id = f"outlier:{number}"
                    while det_id in used_ids:
                        det_id = "outlier:" + det_id
                    used_ids.add(det_id)
                    detection = {"frame_id": frame_id, "mjd": float(mjd), "det_id": det_id,
                                 "x": x, "y": y, "catalog_match": False,
                                 "position_method": "flag_component_geometric_center"}
                    merged.append(detection)
                detection.setdefault("outlier_components", []).append(number)
                detection["outlier_score_bonus"] = float(score_bonus)
                record["det_id"] = detection["det_id"]
                candidates.append(dict(record))
        records.append(record)
    stats = {"n_components": int(count), "n_promoted_components": len(candidates),
             "n_original_detections": len(detections), "n_output_detections": len(merged),
             "n_outlier_pixels": int(np.count_nonzero(array & MASK_OUTLIER)),
             "static_promotion_status": "not_measured"}
    if static_positions is not None:
        static = _positions(static_positions)
        candidate_points = _positions([(c["x"], c["y"]) for c in candidates])
        tree = cKDTree(candidate_points) if len(candidate_points) else None
        promoted = int(np.count_nonzero(tree.query(static)[0] <= match_radius_px)) if tree is not None and len(static) else 0
        stats.update(static_promotion_status="measured" if len(static) else "empty_reference_pool",
                     n_static_reference=len(static), n_static_promoted=promoted,
                     static_promotion_fraction=promoted / len(static) if len(static) else None)
    return {"frame_id": frame_id, "mjd": float(mjd), "coordinate_system": "window_local_native_pixel",
            "mask": f"0x{PROFILE_MOVER_MASK:08X}", "score_bonus_assumption": float(score_bonus),
            "detections": merged, "outlier_candidates": candidates,
            "component_log": records, "statistics": stats}


def score_linked_candidates(link_result, detections):
    """Add OUTLIER evidence to existing 04-06 results; do not create/remove tracks.

The caller must have transformed window-native candidates and ordinary catalogue
detections into the same tangent-pixel coordinate system before linking.
"""
    bonuses = {}
    for detection in detections:
        key = (detection["frame_id"], detection["det_id"])
        if key in bonuses:
            raise ValueError("Duplicate frame/detection identity")
        bonus = float(detection.get("outlier_score_bonus", 0.0))
        if not math.isfinite(bonus) or bonus < 0:
            raise ValueError("OUTLIER score bonus must be finite and nonnegative")
        bonuses[key] = bonus
    output = deepcopy(link_result)
    for field in ("tracks", "candidates_log"):
        # The linker shares candidate objects between these lists; score each
        # independent output record once rather than incrementing shared aliases.
        output[field] = deepcopy(link_result.get(field, []))
        for candidate in output.get(field, []):
            refs = {(ref["frame_id"], ref["det_id"]) for ref in candidate["detection_refs"]}
            bonus = sum(bonuses.get(key, 0.0) for key in refs)
            candidate["base_score"] = candidate["score"]
            candidate["outlier_score_bonus"] = bonus
            candidate["score"] += bonus
        output.get(field, []).sort(key=lambda candidate: -candidate["score"])
    return output


def write_candidates(path, result):
    """Serialize the complete per-frame result, including rejected component reasons."""
    Path(path).write_text(json.dumps(result, indent=2, allow_nan=False), encoding="utf-8")
