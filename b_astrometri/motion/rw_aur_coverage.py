"""08-09: RW Aurigae — SPHEREx coverage table generator.

TAP/IRSA queries failed during development; coverage is unknown.
Framework is complete: plug in real n_frames/n_passes when TAP is available (H-12).
"""


TARGET_NAME = "RW Aurigae"
TARGET_RA_DEG = 75.4817   # J2000, literature
TARGET_DEC_DEG = 30.4028


def coverage_summary() -> dict:
    """Return coverage status dict.

    Returns a dict with coverage_status='unknown_tap_failed' until real
    SPHEREx footprint data is available (H-12).
    """
    return {
        "target": TARGET_NAME,
        "ra_deg": TARGET_RA_DEG,
        "dec_deg": TARGET_DEC_DEG,
        "coverage_status": "unknown_tap_failed",
        "n_frames": None,
        "n_passes": None,
        "note": "SPHEREx TAP/IRSA query failed; re-run when service available.",
    }


def main() -> None:
    summary = coverage_summary()
    assert summary["coverage_status"] == "unknown_tap_failed", (
        f"Unexpected coverage_status: {summary['coverage_status']!r}"
    )
    print(f"RW Aur coverage_status: {summary['coverage_status']}")
    print(f"  target: {summary['target']}")
    print(f"  ra={summary['ra_deg']}, dec={summary['dec_deg']}")
    print(f"  note: {summary['note']}")
    print("DONE 08-09")


if __name__ == "__main__":
    main()
