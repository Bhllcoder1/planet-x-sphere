"""04-06: Hareketli cisim bulucu — statik eleme, hiz izgarasi ve dogrusal RANSAC baglama.

< 3 farkli kare iceren geciste 'baglama kapali' ('linking_closed') doner.
Statik kaynaklar (Gaia/2MASS eslesmesi veya >=2 karede <=1.0 px tekrar) elenir.
Hiz ust siniri 10.6 px/saat (~65"/h ana kusak; NEO hizlari denenmedi [ASSUMPTION]).
Girdi x/y tum karelerde AYNI tangent-duzlemi piksel sisteminde olmali; bu modul
kare-yerel koordinatlari WCS ile donusturmez. Izgara yalnizca tespit ciftlerinin
destekledigi hiz hucrelerini degerlendirir; tum hiz uzayini taradigini iddia etmez.
"""
from __future__ import annotations

import math
from typing import Any

import numpy as np

DEFAULT_V_MAX_PX_HR = 10.6  # ~65"/h / 6.15"/px [ASSUMPTION]


def filter_static_detections(
    detections: list[dict[str, Any]],
    *,
    static_radius_px: float = 1.0,
) -> list[dict[str, Any]]:
    """Gaia/2MASS eslesmelerini ve >=2 farkli karede <=1 px tekrarlayanlari ele."""
    non_cat = [d for d in detections if not d.get("catalog_match", False)]
    keep: list[dict[str, Any]] = []
    r2_lim = static_radius_px ** 2
    for i, d in enumerate(non_cat):
        repeated = False
        for j, other in enumerate(non_cat):
            if i == j or str(d["frame_id"]) == str(other["frame_id"]):
                continue
            dx = float(d["x"]) - float(other["x"])
            dy = float(d["y"]) - float(other["y"])
            if dx * dx + dy * dy <= r2_lim:
                repeated = True
                break
        if not repeated:
            keep.append(d)
    return keep


def _fit_line(inliers: list[dict[str, Any]], t_ref: float) -> tuple[float, float, float, float, float, float]:
    t = np.array([(float(d["mjd"]) - t_ref) * 24.0 for d in inliers], dtype=float)
    x = np.array([float(d["x"]) for d in inliers], dtype=float)
    y = np.array([float(d["y"]) for d in inliers], dtype=float)
    a = np.column_stack([np.ones_like(t), t])
    cx, _, _, _ = np.linalg.lstsq(a, x, rcond=None)
    cy, _, _, _ = np.linalg.lstsq(a, y, rcond=None)
    rx = x - (cx[0] + cx[1] * t)
    ry = y - (cy[0] + cy[1] * t)
    r = np.hypot(rx, ry)
    return (
        float(cx[0]), float(cy[0]),
        float(cx[1]), float(cy[1]),
        float(np.sqrt(np.mean(r * r))), float(np.max(r)),
    )


def _consensus(by_frame, t_ref, x0, y0, vx, vy, tolerance):
    inliers = []
    for frame_dets in by_frame.values():
        t = (float(frame_dets[0]["mjd"]) - t_ref) * 24.0
        best, best_r = None, tolerance
        for detection in frame_dets:
            r = math.hypot(float(detection["x"]) - (x0 + vx * t),
                           float(detection["y"]) - (y0 + vy * t))
            if r < best_r:
                best, best_r = detection, r
        if best is not None:
            inliers.append(best)
    return inliers


def link_movers(
    detections: list[dict[str, Any]],
    *,
    v_min_px_hr: float = 0.05,
    v_max_px_hr: float = DEFAULT_V_MAX_PX_HR,
    residual_tol_px: float = 1.0,
    static_radius_px: float = 1.0,
    max_hypotheses: int = 100_000,
) -> dict[str, Any]:
    """Sparse velocity-lattice seeds plus deterministic two-point consensus/refit.

    Lattice component spacing is min(1px, tolerance)/(sqrt(2)*total hours).
    Only pair-supported cells are searched, anchored at the pair's first point.
    Pairs in the same cell/anchor are merged; the first pair's identity is kept.
    A seed quantized outside the speed annulus retains its original pair velocity
    instead of silently losing a boundary-speed candidate. Final fitted speeds
    must still satisfy the requested bounds.

    max_hypotheses also caps the conservative pair-check count before the
    quadratic static filter. Exceeding it returns an explicit incomplete status;
    it never coarsens the lattice or truncates a detection list.
    """
    if (not all(math.isfinite(v) for v in (v_min_px_hr, v_max_px_hr, residual_tol_px, static_radius_px))
            or not 0 <= v_min_px_hr <= v_max_px_hr or v_max_px_hr <= 0
            or residual_tol_px <= 0 or static_radius_px < 0):
        raise ValueError("Require finite speed bounds, positive residual tolerance and nonnegative static radius")
    if isinstance(max_hypotheses, bool) or not isinstance(max_hypotheses, int) or max_hypotheses <= 0:
        raise ValueError("max_hypotheses must be a positive integer computational budget")
    unique_frames, identities = {}, set()
    for detection in detections:
        if not all(math.isfinite(float(detection[name])) for name in ("x", "y", "mjd")):
            raise ValueError("Detection x, y and mjd must be finite")
        fid, did = str(detection["frame_id"]), str(detection["det_id"])
        if not fid or not did or (fid, did) in identities:
            raise ValueError("Detection frame_id/det_id pairs must be nonempty and unique")
        identities.add((fid, did))
        mjd = float(detection["mjd"])
        if fid in unique_frames and unique_frames[fid] != mjd:
            raise ValueError("All detections in a frame must have the same MJD")
        unique_frames[fid] = mjd
    refs = lambda rows: [{"frame_id": d["frame_id"], "det_id": d["det_id"]} for d in rows]
    diagnostics = {"method": "pair_supported_sparse_velocity_lattice",
                   "full_velocity_grid_searched": False, "max_hypotheses": max_hypotheses,
                   "coordinate_contract": "caller supplies one common tangent-plane pixel system"}
    if len(unique_frames) < 3:
        return {
            "status": "linking_closed",
            "reason": "fewer_than_3_frames",
            "n_frames": len(unique_frames),
            "tracks": [],
            "candidates_log": [],
            "unlinked_detections": refs(detections),
            "search_diagnostics": diagnostics,
        }

    non_catalogue = [d for d in detections if not d.get("catalog_match", False)]
    pair_bound = len(non_catalogue) * (len(non_catalogue) - 1) // 2
    diagnostics["pair_checks_upper_bound"] = pair_bound
    if pair_bound > max_hypotheses:
        return {"status": "search_budget_exceeded", "reason": "pair_check_budget",
                "search_complete": False, "n_frames": len(unique_frames),
                "tracks": [], "candidates_log": [], "unlinked_detections": refs(detections),
                "search_diagnostics": diagnostics}
    span_hours = (max(unique_frames.values()) - min(unique_frames.values())) * 24.0
    if span_hours <= 0:
        return {"status": "linking_closed", "reason": "no_time_baseline",
                "n_frames": len(unique_frames), "tracks": [], "candidates_log": [],
                "unlinked_detections": refs(detections), "search_diagnostics": diagnostics}
    grid_step = min(1.0, residual_tol_px) / (math.sqrt(2) * span_hours)
    if not math.isfinite(grid_step) or grid_step <= 0:
        raise ValueError("Time span cannot represent a finite positive velocity grid step")
    diagnostics.update({"span_hours": span_hours, "component_step_px_hr": grid_step,
                        "diagonal_spacing_times_span_px": math.sqrt(2) * grid_step * span_hours})
    moving = filter_static_detections(detections, static_radius_px=static_radius_px)
    moving = sorted(moving, key=lambda d: (float(d["mjd"]), str(d["frame_id"]), str(d["det_id"])))
    moving_ids = {(str(d["frame_id"]), str(d["det_id"])) for d in moving}
    static_log = [{**refs([d])[0], "reason": "catalogue_match" if d.get("catalog_match", False)
                   else "repeated_static_position"} for d in detections
                  if (str(d["frame_id"]), str(d["det_id"])) not in moving_ids]
    t_ref = min(unique_frames.values())
    by_frame: dict[str, list[dict[str, Any]]] = {}
    for d in moving:
        by_frame.setdefault(str(d["frame_id"]), []).append(d)

    # Deterministic pair votes populate a sparse lattice, not an exhaustive grid.
    candidates: list[dict[str, Any]] = []
    seen_sets: set[tuple[tuple[str, str], ...]] = set()
    seen_grid_anchors = set()
    evaluated, pair_votes, boundary_seeds = 0, 0, 0
    n = len(moving)
    for i in range(n):
        di = moving[i]
        ti = (float(di["mjd"]) - t_ref) * 24.0
        for j in range(i + 1, n):
            dj = moving[j]
            if str(di["frame_id"]) == str(dj["frame_id"]):
                continue
            dt = (float(dj["mjd"]) - float(di["mjd"])) * 24.0
            if abs(dt) < 1e-6:
                continue
            vx = (float(dj["x"]) - float(di["x"])) / dt
            vy = (float(dj["y"]) - float(di["y"])) / dt
            speed = math.hypot(vx, vy)
            if not (v_min_px_hr <= speed <= v_max_px_hr):
                continue
            pair_votes += 1
            cell = (round(vx / grid_step), round(vy / grid_step))
            grid_vx, grid_vy = cell[0] * grid_step, cell[1] * grid_step
            boundary = not v_min_px_hr <= math.hypot(grid_vx, grid_vy) <= v_max_px_hr
            # Boundary seeds retain the exact pair, so do not merge distinct pairs.
            seed_key = (i, cell, j if boundary else None)
            if seed_key in seen_grid_anchors:
                continue
            seen_grid_anchors.add(seed_key)
            evaluated += 1
            boundary_seeds += int(boundary)
            seed_vx, seed_vy = (vx, vy) if boundary else (grid_vx, grid_vy)
            x_seed, y_seed = float(di["x"]) - seed_vx * ti, float(di["y"]) - seed_vy * ti
            inliers = _consensus(by_frame, t_ref, x_seed, y_seed, seed_vx, seed_vy, residual_tol_px)
            if len(inliers) < 2:
                continue
            # Consensus/refit iterations reject outliers and can recover other frame matches.
            for _ in range(5):
                x0, y0, vx_f, vy_f, _, _ = _fit_line(inliers, t_ref)
                refined = _consensus(by_frame, t_ref, x0, y0, vx_f, vy_f, residual_tol_px)
                if len(refined) < 2:
                    inliers = []
                    break
                old_ids = [(str(d["frame_id"]), str(d["det_id"])) for d in inliers]
                new_ids = [(str(d["frame_id"]), str(d["det_id"])) for d in refined]
                inliers = refined
                if old_ids == new_ids:
                    break
            if len(inliers) < 2:
                continue
            x0, y0, vx_f, vy_f, rms_px, max_res_px = _fit_line(inliers, t_ref)
            if not (v_min_px_hr <= math.hypot(vx_f, vy_f) <= v_max_px_hr):
                continue
            if len(inliers) >= 3 and max_res_px < residual_tol_px:
                kind = "track"
            elif len(inliers) == 2:
                kind = "low_confidence_track"
            else:
                continue
            key = tuple(sorted((str(d["frame_id"]), str(d["det_id"])) for d in inliers))
            if key in seen_sets:
                continue
            seen_sets.add(key)
            score = float(len(inliers)) - 0.1 * rms_px
            candidates.append({
                "kind": kind,
                "n_detections": len(inliers),
                "x0": x0,
                "y0": y0,
                "t_ref_mjd": t_ref,
                "vx_px_hr": vx_f,
                "vy_px_hr": vy_f,
                "speed_px_hr": math.hypot(vx_f, vy_f),
                "rms_px": rms_px,
                "max_residual_px": max_res_px,
                "score": score,
                "score_interpretation": "uncalibrated ordering only; not a probability",
                "velocity_cell": list(cell),
                "velocity_seed_kind": "exact_boundary_pair" if boundary else "occupied_grid_cell",
                "seed_pair_refs": refs([di, dj]),
                "seed_pair_velocity_px_hr": [vx, vy],
                "veto_reason": [],
                "detection_ids": [d["det_id"] for d in inliers],
                "detection_refs": [
                    {"frame_id": d["frame_id"], "det_id": d["det_id"]}
                    for d in inliers
                ],
            })

    candidates.sort(key=lambda c: (-c["n_detections"], c["rms_px"]))
    tracks = [c for c in candidates if c["kind"] == "track"]
    linked_ids = {(str(r["frame_id"]), str(r["det_id"])) for c in candidates for r in c["detection_refs"]}
    diagnostics.update({"eligible_pair_votes": pair_votes, "evaluated_hypotheses": evaluated,
                        "exact_boundary_pair_seeds": boundary_seeds,
                        "consensus_refit_iterations_max": 5})
    return {
        "status": "ok",
        "search_complete": True,
        "n_frames": len(unique_frames),
        "n_static_filtered": len(detections) - len(moving),
        "static_filter_log": static_log,
        "unlinked_detections": refs([d for d in moving if (str(d["frame_id"]), str(d["det_id"])) not in linked_ids]),
        "search_diagnostics": diagnostics,
        "tracks": tracks,
        "candidates_log": candidates,
    }
