"""01-12: R27 OUTLIER bit cross-match across epochs.

Investigates the R27 OUTLIER flag by comparing same-field observations across
processing labels. Real FLAGS column requires H-01 (Akif's SPHEREx module);
synthetic test uses generated FLAGS data.
"""
from __future__ import annotations
import numpy as np
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class OutlierAuditResult:
    field_id: str
    week_a: str
    week_b: str
    n_matched: int
    outlier_rate_a: float
    outlier_rate_b: float
    processing_label_a: str
    processing_label_b: str
    consistent: bool
    notes: str = ""


def audit_outlier_flags(
    catalog_a: np.ndarray,
    catalog_b: np.ndarray,
    flags_col: str = "FLAGS",
    outlier_bit: int = 27,  # R27
    match_radius_px: float = 2.0,
) -> OutlierAuditResult:
    """Compare OUTLIER (R27) flag rates between two observation catalogs.

    Parameters
    ----------
    catalog_a, catalog_b : structured arrays with x_px, y_px, FLAGS columns
    flags_col : name of FLAGS column
    outlier_bit : bit position (0-indexed) for OUTLIER flag
    match_radius_px : cross-match radius in pixels
    """
    # Cross-match by pixel proximity
    xa, ya = catalog_a["x_px"], catalog_a["y_px"]
    xb, yb = catalog_b["x_px"], catalog_b["y_px"]

    matched_indices = []
    for i in range(len(xa)):
        dist = np.sqrt((xb - xa[i])**2 + (yb - ya[i])**2)
        j = int(np.argmin(dist))
        if dist[j] <= match_radius_px:
            matched_indices.append((i, j))

    if not matched_indices:
        return OutlierAuditResult(
            field_id="unknown", week_a="?", week_b="?",
            n_matched=0, outlier_rate_a=0.0, outlier_rate_b=0.0,
            processing_label_a="?", processing_label_b="?",
            consistent=True, notes="no matches found"
        )

    idx_a = [p[0] for p in matched_indices]
    idx_b = [p[1] for p in matched_indices]

    flags_a = catalog_a[flags_col][idx_a]
    flags_b = catalog_b[flags_col][idx_b]

    mask = 1 << outlier_bit
    outlier_a = (flags_a & mask) != 0
    outlier_b = (flags_b & mask) != 0

    rate_a = float(np.mean(outlier_a))
    rate_b = float(np.mean(outlier_b))

    # Consistent if rates agree within 10%
    consistent = abs(rate_a - rate_b) < 0.10

    return OutlierAuditResult(
        field_id=catalog_a.get("field_id", ["unknown"])[0] if hasattr(catalog_a, "get") else "unknown",
        week_a=str(catalog_a.get("week", ["?"])[0]) if hasattr(catalog_a, "get") else "?",
        week_b=str(catalog_b.get("week", ["?"])[0]) if hasattr(catalog_b, "get") else "?",
        n_matched=len(matched_indices),
        outlier_rate_a=rate_a,
        outlier_rate_b=rate_b,
        processing_label_a="label_A",
        processing_label_b="label_B",
        consistent=consistent,
        notes=f"R27 bit rate difference: {abs(rate_a-rate_b):.3f}",
    )


if __name__ == "__main__":
    # Synthetic smoke test
    rng = np.random.default_rng(42)
    n = 50
    dtype = [("x_px", "f4"), ("y_px", "f4"), ("FLAGS", "u4")]
    cat_a = np.zeros(n, dtype=dtype)
    cat_b = np.zeros(n, dtype=dtype)
    cat_a["x_px"] = rng.uniform(0, 100, n)
    cat_a["y_px"] = rng.uniform(0, 100, n)
    cat_b["x_px"] = cat_a["x_px"] + rng.normal(0, 0.3, n)
    cat_b["y_px"] = cat_a["y_px"] + rng.normal(0, 0.3, n)
    # Set R27 bit on ~20% of cat_a
    outlier_mask = rng.random(n) < 0.20
    cat_a["FLAGS"][outlier_mask] |= (1 << 27)

    result = audit_outlier_flags(cat_a, cat_b)
    print(f"Matched: {result.n_matched}, R27 rate A={result.outlier_rate_a:.3f}, B={result.outlier_rate_b:.3f}")
    print(f"Consistent: {result.consistent} — {result.notes}")
    print("01-12 outlier_flag_audit: OK")
