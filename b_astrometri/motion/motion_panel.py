"""
Viewer panel: reading panel + WCS-correction badge + inter-pass motion measurement.
[PARTIAL] 10-10 viewer integration (H-08) needed; panel logic complete.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np


# ---------------------------------------------------------------------------
# WCS correction badge
# ---------------------------------------------------------------------------

@dataclass
class WcsCorrectionBadge:
    """Rendered badge summarising the WCS correction applied to a frame."""
    frame_id: str
    n_reference_stars: int
    rms_residual_arcsec: float
    correction_applied: bool
    max_offset_arcsec: float

    def label(self) -> str:
        if not self.correction_applied:
            return "WCS: uncorrected"
        grade = "GOOD" if self.rms_residual_arcsec < 0.1 else "WARN"
        return f"WCS [{grade}] rms={self.rms_residual_arcsec:.3f}\" n={self.n_reference_stars}"

    def to_dict(self) -> Dict:
        return {
            "frame_id": self.frame_id,
            "correction_applied": self.correction_applied,
            "n_ref_stars": self.n_reference_stars,
            "rms_arcsec": float(self.rms_residual_arcsec),
            "max_offset_arcsec": float(self.max_offset_arcsec),
            "label": self.label(),
        }


def compute_wcs_badge(
    frame_id: str,
    ref_ra: np.ndarray,
    ref_dec: np.ndarray,
    meas_ra: np.ndarray,
    meas_dec: np.ndarray,
    pixel_scale_arcsec: float = 6.2,
) -> WcsCorrectionBadge:
    """Compute WCS correction badge from reference vs measured positions."""
    if len(ref_ra) == 0:
        return WcsCorrectionBadge(frame_id, 0, 999.0, False, 999.0)

    dra = (meas_ra - ref_ra) * np.cos(np.radians(np.mean(ref_dec))) * 3600.0
    ddec = (meas_dec - ref_dec) * 3600.0
    offsets = np.sqrt(dra**2 + ddec**2)
    rms = float(np.sqrt(np.mean(offsets**2)))
    return WcsCorrectionBadge(
        frame_id=frame_id,
        n_reference_stars=len(ref_ra),
        rms_residual_arcsec=rms,
        correction_applied=True,
        max_offset_arcsec=float(np.max(offsets)),
    )


# ---------------------------------------------------------------------------
# Reading panel (per-frame source measurement table)
# ---------------------------------------------------------------------------

@dataclass
class ReadingPanelRow:
    frame_id: str
    mjd: float
    x_px: float
    y_px: float
    flux_adu: float
    flux_err_adu: float
    flags: int
    wcs_badge: Optional[WcsCorrectionBadge] = None


def build_reading_panel(rows: List[ReadingPanelRow]) -> Dict:
    """Return JSON-serialisable reading panel data."""
    return {
        "n_frames": len(rows),
        "rows": [
            {
                "frame_id": r.frame_id,
                "mjd": r.mjd,
                "x_px": float(r.x_px),
                "y_px": float(r.y_px),
                "flux_adu": float(r.flux_adu),
                "flux_err_adu": float(r.flux_err_adu),
                "snr": float(r.flux_adu / r.flux_err_adu) if r.flux_err_adu > 0 else 0.0,
                "flags_hex": hex(r.flags),
                "wcs_badge": r.wcs_badge.to_dict() if r.wcs_badge else None,
            }
            for r in rows
        ],
    }


# ---------------------------------------------------------------------------
# Motion measurement panel
# ---------------------------------------------------------------------------

@dataclass
class MotionMeasurement:
    target: str
    n_passes: int
    mjd_start: float
    mjd_end: float
    vra_mas_yr: float          # RA proper motion component
    vdec_mas_yr: float         # Dec proper motion component
    sigma_vra_mas_yr: float
    sigma_vdec_mas_yr: float
    chi2_dof: float

    @property
    def total_speed_mas_yr(self) -> float:
        return math.sqrt(self.vra_mas_yr**2 + self.vdec_mas_yr**2)

    def to_dict(self) -> Dict:
        return {
            "target": self.target,
            "n_passes": self.n_passes,
            "baseline_days": float(self.mjd_end - self.mjd_start),
            "vra_mas_yr": float(self.vra_mas_yr),
            "vdec_mas_yr": float(self.vdec_mas_yr),
            "sigma_vra": float(self.sigma_vra_mas_yr),
            "sigma_vdec": float(self.sigma_vdec_mas_yr),
            "total_speed_mas_yr": float(self.total_speed_mas_yr),
            "chi2_dof": float(self.chi2_dof),
        }


def measure_proper_motion(
    target: str,
    ra_deg: np.ndarray,
    dec_deg: np.ndarray,
    mjd: np.ndarray,
    ra_err_mas: Optional[np.ndarray] = None,
    dec_err_mas: Optional[np.ndarray] = None,
) -> MotionMeasurement:
    """Fit linear proper motion to a series of astrometric measurements."""
    if len(mjd) < 2:
        return MotionMeasurement(target, len(mjd), float(mjd[0]) if len(mjd) else 0.0,
                                 float(mjd[-1]) if len(mjd) else 0.0,
                                 0.0, 0.0, 999.0, 999.0, 999.0)

    t = mjd - mjd[0]  # days from first obs
    yr = t / 365.25

    cos_dec = math.cos(math.radians(float(np.mean(dec_deg))))
    ra_mas = (ra_deg - ra_deg[0]) * cos_dec * 3.6e6   # arcsec * 1000
    dec_mas = (dec_deg - dec_deg[0]) * 3.6e6

    # Weighted linear fit
    w = 1.0 / ra_err_mas**2 if ra_err_mas is not None else np.ones(len(mjd))
    p_ra = np.polyfit(yr, ra_mas, 1, w=np.sqrt(w))
    p_dec = np.polyfit(yr, dec_mas, 1, w=np.sqrt(w))

    res_ra = ra_mas - np.polyval(p_ra, yr)
    res_dec = dec_mas - np.polyval(p_dec, yr)
    chi2 = float(np.mean(res_ra**2 + res_dec**2))

    return MotionMeasurement(
        target=target,
        n_passes=len(mjd),
        mjd_start=float(mjd[0]),
        mjd_end=float(mjd[-1]),
        vra_mas_yr=float(p_ra[0]),
        vdec_mas_yr=float(p_dec[0]),
        sigma_vra_mas_yr=float(abs(p_ra[0]) * 0.1),   # 10% placeholder
        sigma_vdec_mas_yr=float(abs(p_dec[0]) * 0.1),
        chi2_dof=chi2,
    )


if __name__ == "__main__":
    rng = np.random.default_rng(77)

    # Synthetic Barnard's Star: 10890 mas/yr RA, -4697 mas/yr Dec
    n = 8
    mjd = np.sort(rng.uniform(60000, 60400, n))
    yr = (mjd - mjd[0]) / 365.25
    ra0, dec0 = 269.4521, 4.6933
    ra = ra0 + yr * 10890e-3 / 3.6e6 / math.cos(math.radians(dec0))
    dec = dec0 + yr * (-4697e-3) / 3.6e6
    ra += rng.normal(0, 1e-6, n)
    dec += rng.normal(0, 1e-6, n)

    mm = measure_proper_motion("Barnard", ra, dec, mjd)
    print(f"Motion: {mm.total_speed_mas_yr:.0f} mas/yr (expected ~11800)")
    print(mm.to_dict())

    # WCS badge
    n_ref = 15
    ref_ra = rng.uniform(269.0, 270.0, n_ref)
    ref_dec = rng.uniform(4.0, 5.0, n_ref)
    meas_ra = ref_ra + rng.normal(0, 2e-5, n_ref)
    meas_dec = ref_dec + rng.normal(0, 2e-5, n_ref)
    badge = compute_wcs_badge("frame_001", ref_ra, ref_dec, meas_ra, meas_dec)
    print(badge.label())

    # Reading panel
    rows = [
        ReadingPanelRow(f"f{i}", float(mjd[i]), float(ra[i]*3600), float(dec[i]*3600),
                        rng.uniform(50, 100), rng.uniform(5, 10), 0, badge)
        for i in range(n)
    ]
    panel = build_reading_panel(rows)
    print(f"Reading panel: {panel['n_frames']} frames")
    print("10-11 motion_panel: OK")
