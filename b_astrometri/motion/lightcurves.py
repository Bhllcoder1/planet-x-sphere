"""04-12: Degisen yildizlar (RW Aur, R Dra) icin lambda-kutulu isik egrileri.

Farkli dalga boylari (CWAVE/CBAND) asla etiketsiz birlestirilmez.
Kapsam bos ise 'unknown' (TAP basarisiz) ile 'no_coverage' ayri raporlanir.
Gecisten gecise degisim delta_F / sqrt(sig1^2 + sig2^2) ile sigma cinsinden
hesaplanir.
"""
from __future__ import annotations

import math
from typing import Any

from forced_phot import combine_forced_flux


def _bin_label(cwave_um: float, bin_width_um: float) -> tuple[int, str]:
    idx = int(cwave_um / bin_width_um)
    lo = idx * bin_width_um
    hi = (idx + 1) * bin_width_um
    return idx, f"{lo:.3f}-{hi:.3f}_um"


def build_lambda_lightcurves(
    target_name: str,
    measurements: list[dict[str, Any]],
    *,
    bin_width_um: float = 0.05,
    empty_status: str = "unknown",
    all_pass_ids: list[int] | None = None,
) -> dict[str, Any]:
    """Zorlanmis fotometri olcumlerinden lambda-kutulu isik egrisi ve gecis degisimi."""
    if bin_width_um <= 0 or not math.isfinite(bin_width_um):
        raise ValueError("bin_width_um pozitif sonlu olmali")
    if empty_status not in {"unknown", "no_coverage"}:
        raise ValueError("empty_status 'unknown' veya 'no_coverage' olmali")
    if not measurements:
        return {
            "target": target_name,
            "status": empty_status,
            "bin_width_um": float(bin_width_um),
            "bins": [],
        }

    grouped: dict[tuple[int, str], list[dict[str, Any]]] = {}
    for m in measurements:
        if m.get("status") != "ok" or m.get("flux") is None or m.get("sigma_flux") is None:
            continue
        cw = float(m["cwave_um"])
        if not math.isfinite(cw):
            continue
        key = _bin_label(cw, bin_width_um)
        grouped.setdefault(key, []).append(m)

    bins_out: list[dict[str, Any]] = []
    for (idx, label), items in sorted(grouped.items()):
        items_sorted = sorted(items, key=lambda r: float(r["mjd"]))
        by_pass: dict[int, list[dict[str, Any]]] = {}
        for r in items_sorted:
            by_pass.setdefault(int(r["pass_id"]), []).append(r)

        pass_ids = sorted(set(all_pass_ids or []) | set(by_pass.keys()))
        pass_summary: list[dict[str, Any]] = []
        valid_passes: list[dict[str, Any]] = []
        for pid in pass_ids:
            p_items = by_pass.get(pid, [])
            if not p_items:
                pass_summary.append({"pass_id": pid, "status": "no_data", "flux": None, "sigma_flux": None})
                continue
            comb = combine_forced_flux(p_items)
            entry = {
                "pass_id": pid,
                "status": comb["status"],
                "n_frames": len(p_items),
                "mjd_min": float(min(r["mjd"] for r in p_items)),
                "mjd_max": float(max(r["mjd"] for r in p_items)),
                "flux": comb["flux"],
                "sigma_flux": comb["sigma_flux"],
                "any_saturated": any(bool(r.get("saturated_fit")) for r in p_items),
            }
            pass_summary.append(entry)
            if comb["status"] == "ok":
                valid_passes.append(entry)

        max_delta_sigma = 0.0
        for i in range(len(valid_passes)):
            for j in range(i + 1, len(valid_passes)):
                p1, p2 = valid_passes[i], valid_passes[j]
                denom = math.hypot(p1["sigma_flux"], p2["sigma_flux"])
                if denom > 0:
                    ds = abs(p2["flux"] - p1["flux"]) / denom
                    if ds > max_delta_sigma:
                        max_delta_sigma = ds

        bins_out.append({
            "bin_index": idx,
            "lambda_label": label,
            "lambda_min_um": float(idx * bin_width_um),
            "lambda_max_um": float((idx + 1) * bin_width_um),
            "n_points": len(items_sorted),
            "any_saturated": any(bool(r.get("saturated_fit")) for r in items_sorted),
            "max_delta_sigma": float(max_delta_sigma),
            "variable_gt_3sigma": bool(max_delta_sigma > 3.0),
            "passes": pass_summary,
            "points": [
                {
                    "frame_id": r.get("frame_id"),
                    "pass_id": int(r["pass_id"]),
                    "mjd": float(r["mjd"]),
                    "cwave_um": float(r["cwave_um"]),
                    "flux": float(r["flux"]),
                    "sigma_flux": float(r["sigma_flux"]),
                    "saturated_fit": bool(r.get("saturated_fit", False)),
                }
                for r in items_sorted
            ],
        })

    return {
        "target": target_name,
        "status": "ok",
        "bin_width_um": float(bin_width_um),
        "n_bins": len(bins_out),
        "bins": bins_out,
    }
