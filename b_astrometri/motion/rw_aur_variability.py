"""08-10: RW Aurigae — variable star flux warning module.

[PARTIAL] Real λ-binned light curves from 04-12/H-12 needed for
production use. variability_warning() works on any flux list.

Threshold: flux_range = max/min > 2.0 triggers warning.
[ASSUMPTION] 2.0× factor chosen as 1 mag variability proxy; may need
tuning once real SPHEREx light curves (04-12) are available.
"""


VARIABILITY_THRESHOLD = 2.0  # max/min flux ratio; [ASSUMPTION]


def variability_warning(flux_measurements: list) -> dict:
    """Return variability assessment for a sequence of flux values.

    Args:
        flux_measurements: Per-frame flux values (arbitrary units, same band).

    Returns:
        dict with keys: flag (bool), flux_range (float|None), warning_text (str).
    """
    if not flux_measurements or len(flux_measurements) < 2:
        return {
            "flag": False,
            "flux_range": None,
            "warning_text": "insufficient data (< 2 measurements)",
        }

    positive = [f for f in flux_measurements if f > 0]
    if len(positive) < 2:
        return {
            "flag": False,
            "flux_range": None,
            "warning_text": "insufficient positive flux values",
        }

    flux_range = max(positive) / min(positive)
    flagged = flux_range > VARIABILITY_THRESHOLD

    if flagged:
        warning_text = (
            f"RW Aur flux varies by {flux_range:.2f}× across frames "
            f"(threshold {VARIABILITY_THRESHOLD}×). "
            "Brightness variations may bias forced-photometry astrometry; "
            "cross-check λ-band light curves from 04-12."
        )
    else:
        warning_text = f"flux variation {flux_range:.2f}× — below threshold."

    return {
        "flag": flagged,
        "flux_range": flux_range,
        "warning_text": warning_text,
    }


if __name__ == "__main__":
    import json
    # Synthetic demo: 3 frames with 2.5× range
    demo = [1.0, 1.4, 2.5]
    result = variability_warning(demo)
    print(json.dumps(result, indent=2))
