"""08-11: R Draconis — SPHEREx coverage table generator.

Mira-type long-period variable; period ~346 days.
Coverage unknown: SPHEREx TAP/IRSA query failed (H-12).
Real data needed: R Dra RA/Dec → SPHEREx footprint TAP query.
"""


TARGET_NAME = "R Draconis"
TARGET_RA_DEG = 173.3542   # J2000, literature (11h 33m 25s)
TARGET_DEC_DEG = 68.0394   # +68° 02' 22"
MIRA_PERIOD_DAYS = 346.0   # Mira-type period, literature

assert MIRA_PERIOD_DAYS == 346.0, "Mira period sanity check"


def coverage_summary() -> dict:
    """Return coverage status dict. Real TAP query pending (H-12)."""
    return {
        "target": TARGET_NAME,
        "ra_deg": TARGET_RA_DEG,
        "dec_deg": TARGET_DEC_DEG,
        "mira_period_days": MIRA_PERIOD_DAYS,
        "coverage_status": "unknown_tap_failed",
        "n_frames": None,
        "n_passes": None,
        "note": (
            "SPHEREx TAP/IRSA query failed; re-run when service available. "
            f"Mira period {MIRA_PERIOD_DAYS} d — SPHEREx cadence may sample "
            "multiple variability phases."
        ),
    }


def main() -> None:
    result = coverage_summary()
    print(f"Target : {result['target']}")
    print(f"RA/Dec : {result['ra_deg']:.4f} / {result['dec_deg']:.4f}")
    print(f"Period : {result['mira_period_days']} d")
    print(f"Status : {result['coverage_status']}")
    print(f"Note   : {result['note']}")


if __name__ == "__main__":
    main()
    print("DONE 08-11")
