"""03-13: Piksel-faz sapma egrisi — sapma(faz) olcumu ve CSV tablosu.

03-12 T2 duzenegini uygular: alt-piksel fazinda (0..1 px) bilinen yildiz
enjeksiyonu ve wing_fit/ePSF merkezleme ile ortalama sapma, RMS, sigma_tahmin
ve RMS/sigma_tahmin oranini olcer.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np

from wing_fit import fit_epsf_wing


def run_phase_sweep(
    grid,
    *,
    phases=None,
    snr_levels=(20.0, 50.0, 100.0),
    n_trials: int = 200,
    seed: int = 2026,
    noise_sigma: float = 1.0,
) -> list[dict]:
    """Her (SNR, faz) cifti icin x ve y sapma + RMS/sigma_tahmin olcumu."""
    if phases is None:
        phases = [i * 0.05 for i in range(20)]
    rng = np.random.default_rng(seed)
    cx0, cy0 = grid.positions[len(grid.positions) // 2]
    # Birim akida tepe degeri uzerinden yaklasik SNR -> akı olcegi
    yy0, xx0 = np.mgrid[-4:5, -4:5] + np.array([[[cy0]], [[cx0]]])
    unit_stamp = grid.model_at(cx0, cy0).evaluate(xx0, yy0, 1.0, cx0, cy0)
    unit_norm = float(np.sqrt(np.sum(unit_stamp ** 2)))
    var = np.full_like(unit_stamp, noise_sigma ** 2, dtype=float)

    rows: list[dict] = []
    for snr in snr_levels:
        flux = float(snr * noise_sigma / unit_norm)
        for phase in phases:
            dx_err, dy_err, sig_x_pred, sig_y_pred = [], [], [], []
            x_true = float(cx0 + phase)
            y_true = float(cy0 + phase)
            yy, xx = np.mgrid[-4:5, -4:5] + np.array([[[cy0]], [[cx0]]])
            clean = grid.model_at(x_true, y_true).evaluate(xx, yy, flux, x_true, y_true)
            for _ in range(n_trials):
                noisy = clean + rng.normal(0.0, noise_sigma, size=clean.shape)
                fit = fit_epsf_wing(grid, xx, yy, noisy, var, x_true, y_true)
                if fit["status"] == "ok":
                    dx_err.append(fit["x"] - x_true)
                    dy_err.append(fit["y"] - y_true)
                    sig_x_pred.append(fit["sig_x"])
                    sig_y_pred.append(fit["sig_y"])
            dx_a = np.asarray(dx_err, dtype=float)
            dy_a = np.asarray(dy_err, dtype=float)
            sx_a = np.asarray(sig_x_pred, dtype=float)
            sy_a = np.asarray(sig_y_pred, dtype=float)
            rms_x = float(np.sqrt(np.mean(dx_a ** 2)))
            rms_y = float(np.sqrt(np.mean(dy_a ** 2)))
            sig_x_m = float(np.mean(sx_a))
            sig_y_m = float(np.mean(sy_a))
            bias_x = float(np.mean(dx_a))
            bias_y = float(np.mean(dy_a))
            ros_x = float(rms_x / sig_x_m) if sig_x_m > 0 else math.nan
            ros_y = float(rms_y / sig_y_m) if sig_y_m > 0 else math.nan
            passed = (
                abs(bias_x) < 0.02
                and abs(bias_y) < 0.02
                and 0.8 <= ros_x <= 1.25
                and 0.8 <= ros_y <= 1.25
            )
            rows.append({
                "snr": float(snr),
                "phase": float(phase),
                "n_ok": len(dx_a),
                "bias_x_px": bias_x,
                "bias_y_px": bias_y,
                "rms_x_px": rms_x,
                "rms_y_px": rms_y,
                "sigma_pred_x_px": sig_x_m,
                "sigma_pred_y_px": sig_y_m,
                "rms_over_sigma_x": ros_x,
                "rms_over_sigma_y": ros_y,
                "passed_t2_t3": bool(passed),
            })
    return rows


def write_phase_bias_csv(rows: list[dict], path: str | Path) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        out.write_text("", encoding="utf-8")
        return out
    fields = list(rows[0].keys())
    with out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return out
