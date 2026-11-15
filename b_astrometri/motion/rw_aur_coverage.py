"""08-09: RW Aurigae — SPHEREx coverage table generator.

[BLOCKED] H-12: real TAP/IRSA queries failed; coverage unknown.
Real data needed: RW Aur RA/Dec → SPHEREx footprint TAP query.
"""


TARGET_NAME = "RW Aurigae"
TARGET_RA_DEG = 75.4817   # J2000, literature
TARGET_DEC_DEG = 30.4028


def coverage_summary() -> dict:
    """Return coverage status dict. Real TAP query blocked (H-12)."""
    return {
        "target": TARGET_NAME,
        "ra_deg": TARGET_RA_DEG,
        "dec_deg": TARGET_DEC_DEG,
        "coverage_status": "unknown_tap_failed",
        "n_frames": None,
        "n_passes": None,
        "note": "[H-12] SPHEREx TAP/IRSA query failed; re-run when service available.",
    }


if __name__ == "__main__":
    import json
    summary = coverage_summary()
    print(json.dumps(summary, indent=2))
