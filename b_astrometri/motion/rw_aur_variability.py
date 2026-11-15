"""08-10: RW Aurigae — variable star flux warning module.

variability_warning() flags when max/min flux ratio exceeds the threshold.
Threshold default 2.0× (~1 mag) is a conservative proxy for RW Aur's known
multi-magnitude optical outbursts; tune once real SPHEREx λ-binned light
curves (04-12) are available.
"""

VARIABILITY_THRESHOLD = 2.0  # max/min flux ratio


def variability_warning(flux_measurements: list) -> dict:
    """Return variability assessment for a sequence of flux values.

    Parameters
    ----------
    flux_measurements : per-frame flux values (arbitrary units, same band).

    Returns
    -------
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
            f"RW Aur flux varies by {flux_range:.2f}x across frames "
            f"(threshold {VARIABILITY_THRESHOLD}x). "
            "Brightness variations may bias forced-photometry astrometry; "
            "cross-check lambda-band light curves from 04-12."
        )
    else:
        warning_text = f"flux variation {flux_range:.2f}x -- below threshold."

    return {
        "flag": flagged,
        "flux_range": flux_range,
        "warning_text": warning_text,
    }


def main() -> None:
    # --- variable case: flux swings by 3x, should trigger warning ---
    variable_flux = [1.0, 1.4, 2.5, 3.0, 1.1]
    result_var = variability_warning(variable_flux)
    assert result_var["flag"] is True, f"expected flag=True, got {result_var}"
    assert result_var["flux_range"] is not None
    assert result_var["flux_range"] > VARIABILITY_THRESHOLD
    print(f"Variable case: flux_range={result_var['flux_range']:.2f}x, flag={result_var['flag']}")
    print(f"  Warning: {result_var['warning_text']}")

    # --- stable case: all measurements within 1.5x, should not trigger ---
    stable_flux = [100.0, 105.0, 98.0, 102.0, 107.0]
    result_stable = variability_warning(stable_flux)
    assert result_stable["flag"] is False, f"expected flag=False, got {result_stable}"
    print(f"Stable case:   flux_range={result_stable['flux_range']:.2f}x, flag={result_stable['flag']}")

    # --- edge: single measurement ---
    result_edge = variability_warning([50.0])
    assert result_edge["flag"] is False
    assert result_edge["flux_range"] is None

    print("08-10 rw_aur_variability: OK")


if __name__ == "__main__":
    main()
    print("DONE 08-10")
