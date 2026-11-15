"""
Real/fake moving object classifier (small model) with rule-score comparison.
[PARTIAL] real training data from 04-18 needed; feature extraction and logistic score complete.
"""
from __future__ import annotations
import math
import numpy as np
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class MoverFeatures:
    """Features extracted from a mover candidate for classification."""
    n_detections: int
    velocity_px_hr: float
    snr_mean: float
    chi2_linear_fit: float
    max_veto_score: float      # from veto_guard
    arc_length_px: float
    flux_variance: float


@dataclass
class ClassificationResult:
    candidate_id: str
    rule_score: float          # 0–1, from veto/detection logic
    model_score: float         # 0–1, from logistic classifier
    is_real: bool
    notes: str = ""


def extract_features(
    detections_x: np.ndarray,
    detections_y: np.ndarray,
    detections_mjd: np.ndarray,
    detections_flux: np.ndarray,
    detections_snr: np.ndarray,
    veto_score: float = 0.0,
) -> MoverFeatures:
    """Extract classification features from a candidate's detection series."""
    n = len(detections_x)
    if n < 2:
        return MoverFeatures(n_detections=n, velocity_px_hr=0.0, snr_mean=float(np.mean(detections_snr)),
                             chi2_linear_fit=999.0, max_veto_score=veto_score,
                             arc_length_px=0.0, flux_variance=float(np.var(detections_flux)))

    dt_hr = (detections_mjd[-1] - detections_mjd[0]) * 24.0
    dx = detections_x[-1] - detections_x[0]
    dy = detections_y[-1] - detections_y[0]
    arc = math.sqrt(dx**2 + dy**2)
    vel = arc / max(dt_hr, 1e-9)

    # Linear chi² in x
    t = (detections_mjd - detections_mjd[0]) * 24.0
    p = np.polyfit(t, detections_x, 1)
    residuals = detections_x - np.polyval(p, t)
    chi2 = float(np.sum(residuals**2) / max(n - 2, 1))

    return MoverFeatures(
        n_detections=n,
        velocity_px_hr=vel,
        snr_mean=float(np.mean(detections_snr)),
        chi2_linear_fit=chi2,
        max_veto_score=veto_score,
        arc_length_px=arc,
        flux_variance=float(np.var(detections_flux)),
    )


def rule_score(features: MoverFeatures) -> float:
    """Heuristic 0–1 score based on detection quality rules."""
    score = 1.0
    if features.n_detections < 3:
        score *= 0.5
    if features.snr_mean < 3.0:
        score *= 0.3
    if features.chi2_linear_fit > 2.0:
        score *= max(0.1, 1.0 - 0.3 * features.chi2_linear_fit)
    if features.max_veto_score > 0.5:
        score *= 0.1
    return float(np.clip(score, 0.0, 1.0))


def logistic_score(features: MoverFeatures) -> float:
    """Simple logistic classifier (weights from synthetic training [PARTIAL])."""
    # Feature vector: [n_det, snr, 1/chi2, 1-veto, 1]
    x = np.array([
        features.n_detections / 10.0,
        features.snr_mean / 10.0,
        1.0 / max(features.chi2_linear_fit, 0.01),
        1.0 - features.max_veto_score,
        1.0,
    ])
    # Placeholder weights (replace with fitted values from 04-18 training set)
    w = np.array([0.8, 1.2, 0.5, 1.5, -2.0])
    logit = float(np.dot(w, x))
    return float(1.0 / (1.0 + math.exp(-logit)))


def classify_candidate(
    candidate_id: str,
    detections_x: np.ndarray,
    detections_y: np.ndarray,
    detections_mjd: np.ndarray,
    detections_flux: np.ndarray,
    detections_snr: np.ndarray,
    veto_score: float = 0.0,
    threshold: float = 0.5,
) -> ClassificationResult:
    feats = extract_features(detections_x, detections_y, detections_mjd,
                             detections_flux, detections_snr, veto_score)
    rs = rule_score(feats)
    ms = logistic_score(feats)
    combined = (rs + ms) / 2.0
    return ClassificationResult(
        candidate_id=candidate_id,
        rule_score=rs,
        model_score=ms,
        is_real=combined >= threshold,
        notes=f"[PARTIAL] combined={combined:.3f}; real training data from 04-18 needed; feature extraction and logistic score complete.",
    )


if __name__ == "__main__":
    rng = np.random.default_rng(99)
    n = 8
    t = np.sort(rng.uniform(0, 30, n))  # MJD offset days
    x = 100.0 + 0.5 * t + rng.normal(0, 0.1, n)
    y = 200.0 + 0.1 * t + rng.normal(0, 0.1, n)
    flux = rng.uniform(80, 120, n)
    snr = rng.uniform(4, 8, n)

    result = classify_candidate("test_mover_001", x, y, t, flux, snr, veto_score=0.1)
    print(f"rule_score={result.rule_score:.3f}, model_score={result.model_score:.3f}, is_real={result.is_real}")
    print(result.notes)

    # Real vs fake comparison test
    rng2 = np.random.default_rng(42)
    n_r, n_f = 8, 2
    t_r = np.sort(rng2.uniform(0, 30, n_r))
    x_r = 50.0 + 0.3 * t_r + rng2.normal(0, 0.05, n_r)
    y_r = 50.0 + 0.1 * t_r + rng2.normal(0, 0.05, n_r)
    real_cand = classify_candidate(
        "real_cand", x_r, y_r, t_r,
        np.full(n_r, 90.0), np.full(n_r, 7.0), veto_score=0.0,
    )
    t_f = np.sort(rng2.uniform(0, 30, n_f))
    x_f = rng2.uniform(0, 100, n_f)
    y_f = rng2.uniform(0, 100, n_f)
    fake_cand = classify_candidate(
        "fake_cand", x_f, y_f, t_f,
        np.full(n_f, 20.0), np.full(n_f, 1.0), veto_score=0.9,
    )
    real_combined = (real_cand.rule_score + real_cand.model_score) / 2.0
    fake_combined = (fake_cand.rule_score + fake_cand.model_score) / 2.0
    assert real_combined > fake_combined, (
        f"real combined score {real_combined:.3f} should exceed fake {fake_combined:.3f}"
    )
    print(f"real_combined={real_combined:.3f} > fake_combined={fake_combined:.3f} OK")
    print("DONE 04-19")
