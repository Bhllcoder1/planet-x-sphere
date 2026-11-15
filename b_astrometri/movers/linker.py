"""04-06: Hareketli cisim bulucu — statik eleme, hiz izgarasi ve dogrusal RANSAC baglama.

< 3 farkli kare iceren geciste 'baglama kapali' ('linking_closed') doner.
Statik kaynaklar (Gaia/2MASS eslesmesi veya >=2 karede <=1.0 px tekrar) elenir.
Hiz ust siniri 10.6 px/saat (~65"/h ana kusak; NEO hizlari denenmedi [ASSUMPTION]).
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
            if i == j or d["frame_id"] == other["frame_id"]:
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


def link_movers(
    detections: list[dict[str, Any]],
    *,
    v_min_px_hr: float = 0.05,
    v_max_px_hr: float = DEFAULT_V_MAX_PX_HR,
    residual_tol_px: float = 1.0,
    static_radius_px: float = 1.0,
) -> dict[str, Any]:
    """Kare tespitlerinden dogrusal hareketli aday izleri (tracks) bagla."""
    unique_frames = {d["frame_id"]: float(d["mjd"]) for d in detections}
    if len(unique_frames) < 3:
        return {
            "status": "linking_closed",
            "reason": "fewer_than_3_frames",
            "n_frames": len(unique_frames),
            "tracks": [],
            "candidates_log": [],
        }

    moving = filter_static_detections(detections, static_radius_px=static_radius_px)
    t_ref = min(unique_frames.values())
    by_frame: dict[str, list[dict[str, Any]]] = {}
    for d in moving:
        by_frame.setdefault(str(d["frame_id"]), []).append(d)

    # Ciftlerden hiz hipotezleri uret (RANSAC 2-nokta ornekleme)
    candidates: list[dict[str, Any]] = []
    seen_sets: set[tuple[str, ...]] = set()
    n = len(moving)
    for i in range(n):
        di = moving[i]
        ti = (float(di["mjd"]) - t_ref) * 24.0
        for j in range(i + 1, n):
            dj = moving[j]
            if di["frame_id"] == dj["frame_id"]:
                continue
            dt = (float(dj["mjd"]) - float(di["mjd"])) * 24.0
            if abs(dt) < 1e-6:
                continue
            vx = (float(dj["x"]) - float(di["x"])) / dt
            vy = (float(dj["y"]) - float(di["y"])) / dt
            speed = math.hypot(vx, vy)
            if not (v_min_px_hr <= speed <= v_max_px_hr):
                continue

            inliers = []
            for fid, frame_dets in by_frame.items():
                t_f = (float(frame_dets[0]["mjd"]) - t_ref) * 24.0
                xp = float(di["x"]) + vx * (t_f - ti)
                yp = float(di["y"]) + vy * (t_f - ti)
                best_d, best_r = None, residual_tol_px
                for cand in frame_dets:
                    r = math.hypot(float(cand["x"]) - xp, float(cand["y"]) - yp)
                    if r < best_r:
                        best_d, best_r = cand, r
                if best_d is not None:
                    inliers.append(best_d)

            if len(inliers) < 2:
                continue
            key = tuple(sorted(f"{d['frame_id']}:{d['det_id']}" for d in inliers))
            if key in seen_sets:
                continue
            seen_sets.add(key)

            x0, y0, vx_f, vy_f, rms_px, max_res_px = _fit_line(inliers, t_ref)
            if len(inliers) >= 3 and max_res_px < residual_tol_px:
                kind = "track"
            elif len(inliers) == 2:
                kind = "low_confidence_track"
            else:
                continue

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
                "veto_reason": [],
                "detection_ids": [d["det_id"] for d in inliers],
                "detection_refs": [
                    {"frame_id": d["frame_id"], "det_id": d["det_id"]}
                    for d in inliers
                ],
            })

    candidates.sort(key=lambda c: (-c["n_detections"], c["rms_px"]))
    tracks = [c for c in candidates if c["kind"] == "track"]
    return {
        "status": "ok",
        "n_frames": len(unique_frames),
        "n_static_filtered": len(detections) - len(moving),
        "tracks": tracks,
        "candidates_log": candidates,
    }
