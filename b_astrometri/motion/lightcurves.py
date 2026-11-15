"""04-12: Degisen yildizlar (RW Aur, R Dra) icin lambda-kutulu isik egrileri.

Farkli dalga boylari (CWAVE/CBAND) asla etiketsiz birlestirilmez.
Kapsam bos ise 'unknown' (TAP basarisiz) ile 'no_coverage' ayri raporlanir.
Gecisten gecise degisim delta_F / sqrt(sig1^2 + sig2^2) ile sigma cinsinden
hesaplanir.
"""
from __future__ import annotations

import math
import html
import json
import re
from pathlib import Path
from typing import Any

if __package__:
    from .forced_phot import combine_forced_flux, forced_phot
else:
    from forced_phot import combine_forced_flux, forced_phot


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
    empty_reason: str | None = None,
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
            "coverage_status": empty_status,
            "photometry_status": "not_run",
            "reason": empty_reason or "No measurements supplied",
            "bin_width_um": float(bin_width_um),
            "bins": [],
        }

    grouped = {}
    for m in measurements:
        if m.get("status") != "ok" or m.get("flux") is None or m.get("sigma_flux") is None:
            continue
        cw = float(m["cwave_um"])
        if (not math.isfinite(cw) or cw <= 0
                or not math.isfinite(float(m["flux"]))
                or not math.isfinite(float(m["sigma_flux"])) or float(m["sigma_flux"]) <= 0):
            continue
        idx, label = _bin_label(cw, bin_width_um)
        key = (str(m.get("detector", "unspecified")), str(m.get("release", "unspecified")), idx, label)
        grouped.setdefault(key, []).append(m)

    bins_out: list[dict[str, Any]] = []
    for (detector, release, idx, label), items in sorted(grouped.items()):
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
            "detector": None if detector == "unspecified" else detector,
            "release": None if release == "unspecified" else release,
            "lambda_label": label if detector == "unspecified" else f"D{detector} {release}: {label}",
            "lambda_min_um": float(idx * bin_width_um),
            "lambda_max_um": float((idx + 1) * bin_width_um),
            "n_points": len(items_sorted),
            "any_saturated": any(bool(r.get("saturated_fit")) for r in items_sorted),
            "max_delta_sigma": float(max_delta_sigma),
            "variable_gt_3sigma": bool(max_delta_sigma > 3.0),
            "variability_status": "measured" if len(valid_passes) >= 2 else "insufficient_passes",
            "n_comparable_passes": len(valid_passes),
            "passes": pass_summary,
            "points": [
                {
                    "frame_id": r.get("frame_id"),
                    "pass_id": int(r["pass_id"]),
                    "mjd": float(r["mjd"]),
                    "cwave_um": float(r["cwave_um"]),
                    "cband_um": r.get("cband_um"),
                    "flux": float(r["flux"]),
                    "sigma_flux": float(r["sigma_flux"]),
                    "saturated_fit": bool(r.get("saturated_fit", False)),
                }
                for r in items_sorted
            ],
        })

    if not bins_out:
        return {
            "target": target_name,
            "status": "no_valid_measurements",
            "coverage_status": "covered",
            "photometry_status": "no_valid_measurements",
            "bin_width_um": float(bin_width_um),
            "n_bins": 0,
            "bins": [],
        }
    return {
        "target": target_name,
        "status": "ok",
        "coverage_status": "covered",
        "photometry_status": "measured",
        "bin_width_um": float(bin_width_um),
        "n_bins": len(bins_out),
        "bins": bins_out,
    }


def produce_target_control_lightcurves(
    target_name, target_ra_deg, target_dec_deg,
    control_name, control_ra_deg, control_dec_deg, frames, *,
    bin_width_um, coverage_status, output_dir=None, coverage_reason=None,
):
    """Measure caller-supplied target/control positions on exactly the same frames.

    Frames follow ``forced_phot``'s corrected-WCS/EPSF contract. bin_width_um is
    the caller's channel width, not a calibrated default. Each detector/release
    is kept separate. Control comparisons use only matching frame/pass/channel
    measurements that succeeded for BOTH objects; their independent curves keep
    all valid points. A single pass never establishes a stable control star.
    Empty unknown coverage is not converted to zero flux or no coverage.
    """
    frames = list(frames)
    if coverage_status not in {"covered", "partial", "unknown", "no_coverage"}:
        raise ValueError("coverage_status must be covered, partial, unknown or no_coverage")
    if not math.isfinite(bin_width_um) or bin_width_um <= 0:
        raise ValueError("bin_width_um must be a finite positive channel width")
    if (not isinstance(target_name, str) or not isinstance(control_name, str)
            or not target_name.strip() or not control_name.strip()):
        raise ValueError("Target and control names are required")
    if str(target_name).strip() == str(control_name).strip():
        raise ValueError("The control must be identified separately from the target")
    for ra, dec in ((target_ra_deg, target_dec_deg), (control_ra_deg, control_dec_deg)):
        if (not math.isfinite(float(ra)) or not math.isfinite(float(dec))
                or not 0 <= float(ra) < 360 or not -90 <= float(dec) <= 90):
            raise ValueError("Target/control coordinates must be finite degrees in the supplied WCS celestial frame")
    if (float(target_ra_deg) == float(control_ra_deg)
            and float(target_dec_deg) == float(control_dec_deg)):
        raise ValueError("The target cannot be used as its own control")
    if frames and coverage_status == "no_coverage":
        raise ValueError("Frames contradict an explicit no_coverage result")
    if not frames and coverage_status in {"covered", "partial"}:
        raise ValueError("Covered/partial workflow requires the actual frame list")
    ids = [str(frame["frame_id"]) for frame in frames]
    if any(not fid for fid in ids) or len(ids) != len(set(ids)):
        raise ValueError("Photometry frame IDs must be nonempty and unique")
    target_rows = forced_phot(target_ra_deg, target_dec_deg, frames) if frames else []
    control_rows = forced_phot(control_ra_deg, control_dec_deg, frames) if frames else []
    all_passes = sorted({int(frame["pass_id"]) for frame in frames})
    empty_status = coverage_status if not frames else "unknown"

    def curve(name, rows):
        result = build_lambda_lightcurves(name, rows, bin_width_um=bin_width_um,
            empty_status=empty_status, all_pass_ids=all_passes, empty_reason=coverage_reason)
        result.update(coverage_status=coverage_status,
                      flux_unit="uncalibrated_model_amplitude", physical_flux_validated=False)
        return result

    target_curve, control_curve = curve(target_name, target_rows), curve(control_name, control_rows)
    paired_target, paired_control, pairing = [], [], []
    units_by_group = {}
    for target, control in zip(target_rows, control_rows):
        if any(target[field] != control[field] for field in ("frame_id", "pass_id", "mjd", "detector", "release")):
            raise ValueError("Target/control photometry must use identical frame/pass metadata")
        for row in (target, control):
            group = (row["detector"], row["release"])
            units = (row["image_unit"], row["epsf_norm_multiplier"])
            if group in units_by_group and units_by_group[group] != units:
                raise ValueError("Cannot combine differing image units/EPSF normalization within one detector/release")
            units_by_group[group] = units
        usable = all(row["status"] == "ok" and row.get("flux") is not None
            and row.get("sigma_flux") is not None and math.isfinite(float(row["flux"]))
            and math.isfinite(float(row["sigma_flux"])) and float(row["sigma_flux"]) > 0
            and row.get("cwave_um") is not None and math.isfinite(float(row["cwave_um"]))
            and float(row["cwave_um"]) > 0 for row in (target, control))
        same_channel = usable and _bin_label(target["cwave_um"], bin_width_um)[0] == _bin_label(control["cwave_um"], bin_width_um)[0]
        if same_channel:
            paired_target.append(target)
            paired_control.append(control)
        pairing.append({"frame_id": target["frame_id"], "pass_id": target["pass_id"],
                        "target_status": target["status"], "control_status": control["status"],
                        "paired": bool(same_channel),
                        "reason": "same_frame_pass_channel" if same_channel else
                            "different_wavelength_channels" if usable else "missing_or_failed_photometry"})
    paired_target_curve = curve(target_name, paired_target)
    paired_control_curve = curve(control_name, paired_control)
    key = lambda item: (item["detector"], item["release"], item["bin_index"])
    target_bins = {key(item): item for item in paired_target_curve["bins"]}
    control_bins = {key(item): item for item in paired_control_curve["bins"]}
    channels = {key(item): item for item in target_curve["bins"] + control_curve["bins"]}
    comparisons = []
    for channel, channel_info in channels.items():
        target_bin, control_bin = target_bins.get(channel), control_bins.get(channel)
        measured = bool(target_bin and control_bin and target_bin["n_comparable_passes"] >= 2
                        and control_bin["n_comparable_passes"] >= 2)
        comparisons.append({"detector": channel_info["detector"], "release": channel_info["release"],
            "lambda_label": channel_info["lambda_label"], "paired_frames": target_bin["n_points"] if target_bin else 0,
            "paired_passes": target_bin["n_comparable_passes"] if target_bin else 0,
            "status": "measured" if measured else "insufficient_passes" if target_bin else "no_paired_measurements",
            "target_max_delta_sigma": target_bin["max_delta_sigma"] if measured else None,
            "control_max_delta_sigma": control_bin["max_delta_sigma"] if measured else None,
            "control_within_3sigma": control_bin["max_delta_sigma"] <= 3 if measured else None})
    complete_control = bool(comparisons) and all(item["status"] == "measured" for item in comparisons)
    control_within = all(item["control_within_3sigma"] for item in comparisons) if complete_control else None
    result = {"target": str(target_name), "control": str(control_name),
        "target_coordinates_deg": [float(target_ra_deg), float(target_dec_deg)],
        "control_coordinates_deg": [float(control_ra_deg), float(control_dec_deg)],
        "status": coverage_status if not frames else "measured" if complete_control and coverage_status == "covered" else "partial",
        "coverage_status": coverage_status, "coverage_reason": coverage_reason,
        "control_within_3sigma": control_within,
        "control_assessment": "not_measured" if not complete_control else
            "consistent_with_constant_at_3sigma" if control_within else "change_exceeds_3sigma",
        "target_curve": target_curve, "control_curve": control_curve,
        "paired_comparisons": comparisons, "frame_pairing": pairing,
        "frame_ids": ids, "bin_width_um": float(bin_width_um),
        "physical_flux_validated": False,
        "acceptance_status": "not_claimed; requires real-data/control/WCS validation"}
    if output_dir is not None:
        directory = Path(output_dir)
        result["outputs"] = {
            "target": write_lightcurve_outputs(target_curve, directory / "target"),
            "control": write_lightcurve_outputs(control_curve, directory / "control")}
        summary = directory / "target_control_comparison.json"
        result["outputs"]["comparison"] = str(summary)
        summary.write_text(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    return result


def write_lightcurve_outputs(result: dict[str, Any], output_dir: str | Path) -> dict[str, str]:
    """Write a JSON result and SVG plot; empty coverage is explicitly annotated."""
    target = str(result.get("target", "")).strip()
    slug = re.sub(r"[^a-z0-9-]+", "-", target.lower()).strip("-")
    if not slug:
        raise ValueError("A target name is required for output filenames")
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / f"lightcurves_{slug}.json"
    svg_path = out / f"lightcurves_{slug}.svg"
    json_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    svg_path.write_text(_lightcurve_svg(result), encoding="utf-8")
    return {"json": str(json_path), "svg": str(svg_path)}


def _lightcurve_svg(result: dict[str, Any]) -> str:
    bins = result.get("bins", [])
    target = html.escape(str(result.get("target", "Target")))
    if not bins:
        coverage = html.escape(str(result.get("coverage_status", result.get("status", "unknown"))).upper())
        photometry = html.escape(str(result.get("photometry_status", "not_run")).replace("_", " ").upper())
        reason = html.escape(str(result.get("reason", "No valid measurements")))
        return (
            '<svg xmlns="http://www.w3.org/2000/svg" width="900" height="360" viewBox="0 0 900 360">'
            '<rect width="100%" height="100%" fill="white"/>'
            f'<text x="40" y="48" font-size="24" font-family="sans-serif">{target} — λ-binned light curve</text>'
            f'<text x="450" y="145" text-anchor="middle" font-size="22" font-family="sans-serif">Coverage: {coverage}</text>'
            f'<text x="450" y="185" text-anchor="middle" font-size="18" font-family="sans-serif">Photometry: {photometry}</text>'
            f'<text x="450" y="225" text-anchor="middle" font-size="14" font-family="sans-serif">{reason}</text>'
            '<text x="450" y="275" text-anchor="middle" font-size="13" fill="#555" font-family="sans-serif">'
            'An empty panel is not a zero-flux measurement.</text></svg>'
        )

    width, panel_h, left, right = 900, 300, 80, 850
    height = 80 + panel_h * len(bins)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
             '<rect width="100%" height="100%" fill="white"/>',
             f'<text x="40" y="38" font-size="23" font-family="sans-serif">{target} — λ-binned light curve</text>']
    palette = ["#1769aa", "#c43c39", "#248232", "#8a50a4", "#c77d00"]
    for i, item in enumerate(bins):
        ytop = 65 + i * panel_h
        plot_top, plot_bottom = ytop + 40, ytop + 230
        points = item.get("points", [])
        mjds = [float(p["mjd"]) for p in points]
        lows = [float(p["flux"]) - float(p["sigma_flux"]) for p in points]
        highs = [float(p["flux"]) + float(p["sigma_flux"]) for p in points]
        xmin, xmax = min(mjds), max(mjds)
        ymin, ymax = min(lows), max(highs)
        if xmax == xmin:
            xmin, xmax = xmin - 0.5, xmax + 0.5
        if ymax == ymin:
            ymin, ymax = ymin - 0.5, ymax + 0.5
        ypad = (ymax - ymin) * 0.08
        ymin, ymax = ymin - ypad, ymax + ypad
        color = palette[i % len(palette)]
        label = html.escape(str(item.get("lambda_label", "λ bin")))
        parts.extend([
            f'<text x="{left}" y="{ytop + 24}" font-size="17" font-family="sans-serif">{label}</text>',
            f'<line x1="{left}" y1="{plot_top}" x2="{left}" y2="{plot_bottom}" stroke="#333"/>',
            f'<line x1="{left}" y1="{plot_bottom}" x2="{right}" y2="{plot_bottom}" stroke="#333"/>',
            f'<text x="18" y="{(plot_top + plot_bottom) / 2}" transform="rotate(-90 18 {(plot_top + plot_bottom) / 2})" font-size="12" font-family="sans-serif">Flux</text>',
            f'<text x="{(left + right) / 2}" y="{plot_bottom + 32}" text-anchor="middle" font-size="12" font-family="sans-serif">MJD</text>',
        ])
        for p in points:
            x = left + (float(p["mjd"]) - xmin) / (xmax - xmin) * (right - left)
            fy, sig = float(p["flux"]), float(p["sigma_flux"])
            y = plot_bottom - (fy - ymin) / (ymax - ymin) * (plot_bottom - plot_top)
            y1 = plot_bottom - (fy - sig - ymin) / (ymax - ymin) * (plot_bottom - plot_top)
            y2 = plot_bottom - (fy + sig - ymin) / (ymax - ymin) * (plot_bottom - plot_top)
            parts.extend([
                f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{color}"/>',
                f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4" fill="{color}"/>',
            ])
        variable = ("insufficient passes for change" if item.get("variability_status") == "insufficient_passes"
                    else "variable >3σ" if item.get("variable_gt_3sigma") else "no >3σ change")
        sat = "; saturated-fit present" if item.get("any_saturated") else ""
        parts.append(f'<text x="{right}" y="{ytop + 24}" text-anchor="end" font-size="12" fill="{color}" font-family="sans-serif">{variable}{sat}</text>')
    parts.append('</svg>')
    return "".join(parts)
