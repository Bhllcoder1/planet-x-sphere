"""04-08: STREAK/GHOST/CROSSTALK vetolari (neden kodlu) ve kalabalik-alan korumasi.

Adaylar hicbir zaman sessizce silinmez; 3 px yakininda veto biti varsa
'veto_reason' alaniyla etiketlenir ve candidates_log icinde tutulur.
TRANSIENT/HALO yalnizca 'caution' uyarisi uretir, veto sayilmaz.
Kalabalik alan esikleri (SOURCE > 0.50 veya gurultu > 5x seyrek medyan) [ASSUMPTION].
"""
from __future__ import annotations

import math
from typing import Any

import numpy as np

BIT_TRANSIENT = 1 << 10
BIT_HALO = 1 << 19
BIT_CROSSTALK = 1 << 20
MASK_GHOST = (1 << 22) | (1 << 23) | (1 << 24)
BIT_STREAK = 1 << 25


def evaluate_candidate_flags(
    flags,
    x_px: float,
    y_px: float,
    *,
    radius_px: float = 3.0,
) -> dict[str, list[str]]:
    """Adayin 3 px yakinindaki FLAGS bitlerinden veto_reason ve caution uret."""
    flg = np.asarray(flags, dtype=np.int64)
    ny, nx = flg.shape
    yy, xx = np.mgrid[0:ny, 0:nx]
    patch = flg[((xx - float(x_px)) ** 2 + (yy - float(y_px)) ** 2) <= (radius_px ** 2)]
    combined = int(np.bitwise_or.reduce(patch)) if patch.size else 0

    veto_reason: list[str] = []
    if combined & BIT_STREAK:
        veto_reason.append("STREAK")
    if combined & MASK_GHOST:
        veto_reason.append("GHOST")
    if combined & BIT_CROSSTALK:
        veto_reason.append("CROSSTALK")

    caution: list[str] = []
    if combined & BIT_TRANSIENT:
        caution.append("TRANSIENT")
    if combined & BIT_HALO:
        caution.append("HALO")

    return {"veto_reason": sorted(veto_reason), "caution": sorted(caution)}


def tag_candidates(
    candidates: list[dict[str, Any]],
    flags_by_frame: dict[str, Any],
    *,
    radius_px: float = 3.0,
) -> list[dict[str, Any]]:
    """Tum adaylari kopyalayip veto_reason / caution ekle; hicbirini silme."""
    tagged: list[dict[str, Any]] = []
    for cand in candidates:
        out = dict(cand)
        vetos = set(out.get("veto_reason", []))
        cautions = set(out.get("caution", []))
        for obs in out.get("observations", []):
            flg = flags_by_frame.get(obs.get("frame_id"))
            if flg is None:
                continue
            res = evaluate_candidate_flags(flg, obs["x"], obs["y"], radius_px=radius_px)
            vetos.update(res["veto_reason"])
            cautions.update(res["caution"])
        out["veto_reason"] = sorted(vetos)
        out["caution"] = sorted(cautions)
        out["vetoed"] = bool(out["veto_reason"])
        tagged.append(out)
    return tagged


def crowded_field_guard(
    source_fraction: float,
    local_noise: float,
    sparse_median_noise: float,
    *,
    max_source_fraction: float = 0.50,
    max_noise_ratio: float = 5.0,
) -> dict[str, Any]:
    """Kalabalik-alan korumasi: esikler [ASSUMPTION] (s0_D gc1..gc5 vs sp1..sp6)."""
    if not (math.isfinite(source_fraction) and math.isfinite(local_noise) and math.isfinite(sparse_median_noise)):
        raise ValueError("Girdi metrikleri sonlu olmali")
    if sparse_median_noise <= 0:
        raise ValueError("sparse_median_noise > 0 olmali")
    noise_ratio = float(local_noise / sparse_median_noise)
    high_source = source_fraction > max_source_fraction
    high_noise = noise_ratio > max_noise_ratio
    triggered = bool(high_source or high_noise)
    reasons = []
    if high_source:
        reasons.append("SOURCE_GT_50PCT")
    if high_noise:
        reasons.append("NOISE_GT_5X_SPARSE")
    return {
        "linking_enabled": not triggered,
        "guard_triggered": triggered,
        "banner": "kalabalik_alan" if triggered else None,
        "reasons": reasons,
        "source_fraction": float(source_fraction),
        "noise_ratio": noise_ratio,
    }
