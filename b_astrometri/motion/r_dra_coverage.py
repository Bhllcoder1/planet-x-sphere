"""08-11: R Draconis — SPHEREx coverage table generator.

Mira-type long-period variable; period ~346 days.
[BLOCKED] H-12: real TAP/IRSA queries failed; coverage unknown.
Real data needed: R Dra RA/Dec → SPHEREx footprint TAP query.
"""


TARGET_NAME = "R Draconis"
TARGET_RA_DEG = 173.3542   # J2000, literature (11h 33m 25s)
TARGET_DEC_DEG = 68.0394   # +68° 02' 22"
MIRA_PERIOD_DAYS = 346.0   # Mira-type period, literature


def coverage_summary() -> dict:
    """Return coverage status dict. Real TAP query blocked (H-12)."""
    return {
        "target": TARGET_NAME,
        "ra_deg": TARGET_RA_DEG,
        "dec_deg": TARGET_DEC_DEG,
        "mira_period_days": MIRA_PERIOD_DAYS,
        "coverage_status": "unknown_tap_failed",
        "n_frames": None,
        "n_passes": None,
        "note": (
            "[H-12] SPHEREx TAP/IRSA query failed; re-run when service available. "
            f"Mira period {MIRA_PERIOD_DAYS} d — SPHEREx cadence may sample "
            "multiple variability phases."
        ),
    }


if __name__ == "__main__":
    import json
    summary = coverage_summary()
    print(json.dumps(summary, indent=2))
