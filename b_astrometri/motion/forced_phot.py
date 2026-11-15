"""04-03: Zorlanmis (forced) ePSF fotometri modulu — sabit konumda kare basi aki.

Konum (x, y) 0-tabanli ebeveyn pikselde sabittir. forced_phot, acikca verilen
duzeltilmis kesit WCS'ini parent koordinatlarina baglar. Yalnizca (F, b) uydurulur;
agirlik 1 / (VAR * s^2), s >= 1.0. chi2_nu > 5.0 ise 'bad_fit' doner ve aki
degeri verilmez. NaN/OVERFLOW cekirdek 'saturated_fit' ile isaretlenir.
"""
from __future__ import annotations

import math
import csv
from pathlib import Path

import numpy as np

from a_veri_isleme.process.masks import PROFILE_CENTROID_MASK, MASK_TRANSIENT, MASK_CROSSTALK

# 0x3C028E44 + OVERFLOW(1) + DICHROIC(7) + GHOST(22-24) + STREAK(25)
DEFAULT_BAD_FLAGS = PROFILE_CENTROID_MASK
# TRANSIENT / CROSSTALK / HALO / PERSIST uyari bitleri (3 px icinde uyari)
# Table16: HALO28/PERSIST17; A's legacy BIT_PERSIST15 is NONLINEAR, not PERSIST.
WARN_FLAGS = MASK_TRANSIENT | MASK_CROSSTALK | (1 << 28) | (1 << 17)


def forced_phot_frame(
    grid,
    xx,
    yy,
    image,
    variance,
    x_px: float,
    y_px: float,
    *,
    flags=None,
    bad_flags: int = DEFAULT_BAD_FLAGS,
    warn_flags: int = WARN_FLAGS,
    var_scale: float = 1.0,
    frame_meta: dict | None = None,
) -> dict:
    """Sabit (x_px, y_px) konumunda agirlikli dogrusal en kucuk kareler (F, b)."""
    img = np.asarray(image, dtype=float)
    var_scale = float(var_scale)
    var = np.asarray(variance, dtype=float) * (var_scale ** 2)
    xx_a = np.asarray(xx, dtype=float)
    yy_a = np.asarray(yy, dtype=float)
    if not (img.shape == var.shape == xx_a.shape == yy_a.shape):
        raise ValueError("xx, yy, image ve variance ayni sekilde olmali")
    if var_scale < 1.0 or not math.isfinite(var_scale):
        raise ValueError("var_scale >= 1.0 ve sonlu olmali")
    if not (math.isfinite(float(x_px)) and math.isfinite(float(y_px))):
        raise ValueError("x_px ve y_px sonlu olmali")

    valid = np.isfinite(img) & np.isfinite(var) & (var > 0.0) & np.isfinite(xx_a) & np.isfinite(yy_a)
    warn_within_3px = False
    saturated_pixels = ~np.isfinite(img)
    if flags is not None:
        raw_flags = np.asarray(flags)
        if (raw_flags.dtype.kind not in "iu" or np.any(raw_flags < 0)
                or np.any(raw_flags > np.iinfo(np.uint32).max)):
            raise ValueError("flags must contain uint32-compatible integers")
        flg = raw_flags.astype(np.uint32, copy=False)
        if flg.shape != img.shape:
            raise ValueError("flags, image ile ayni sekilde olmali")
        valid &= (flg & bad_flags) == 0
        saturated_pixels |= (flg & (1 << 1)) != 0
        r2_warn = (xx_a - float(x_px)) ** 2 + (yy_a - float(y_px)) ** 2
        warn_within_3px = bool(np.any((flg[r2_warn <= 9.0] & warn_flags) != 0))

    r2_core = (xx_a - float(x_px)) ** 2 + (yy_a - float(y_px)) ** 2
    saturated_fit = bool(np.any(saturated_pixels & (r2_core <= 2.25)))

    n_valid = int(np.sum(valid))
    if n_valid < 4:
        return {
            **(frame_meta or {}),
            "status": "unmeasurable",
            "flux": None,
            "sigma_flux": None,
            "background": None,
            "chi2_nu": None,
            "bad_fit": False,
            "saturated_fit": saturated_fit,
            "warn_within_3px": warn_within_3px,
            "n_valid": n_valid,
        }

    model = grid.model_at(float(x_px), float(y_px))
    xv, yv = xx_a[valid], yy_a[valid]
    iv, wv = img[valid], 1.0 / var[valid]
    pv = model.evaluate(xv, yv, 1.0, float(x_px), float(y_px))

    # Agirlikli 2x2 normal denklem: I = F * p + b
    sw = float(np.sum(wv))
    sp = float(np.sum(wv * pv))
    sp2 = float(np.sum(wv * pv * pv))
    si = float(np.sum(wv * iv))
    spi = float(np.sum(wv * pv * iv))
    det = sp2 * sw - sp * sp
    if det <= 0.0 or not math.isfinite(det):
        return {
            **(frame_meta or {}),
            "status": "unmeasurable",
            "flux": None,
            "sigma_flux": None,
            "background": None,
            "chi2_nu": None,
            "bad_fit": False,
            "saturated_fit": saturated_fit,
            "warn_within_3px": warn_within_3px,
            "n_valid": n_valid,
        }

    flux = (spi * sw - sp * si) / det
    bg = (sp2 * si - sp * spi) / det
    sigma_flux = math.sqrt(sw / det)
    resid = iv - (flux * pv + bg)
    chi2_nu = float(np.sum(wv * resid * resid) / max(n_valid - 2, 1))
    bad_fit = chi2_nu > 5.0

    return {
        **(frame_meta or {}),
        "status": "bad_fit" if bad_fit else "ok",
        "flux": None if bad_fit else float(flux),
        "sigma_flux": None if bad_fit else float(sigma_flux),
        "background": None if bad_fit else float(bg),
        "chi2_nu": chi2_nu,
        "bad_fit": bad_fit,
        "saturated_fit": saturated_fit,
        "warn_within_3px": warn_within_3px,
        "n_valid": n_valid,
    }


def combine_forced_flux(measurements: list[dict]) -> dict:
    """Ters-varyans agirlikli aki birlestirme (04-04 / gecis toplami icin)."""
    good = [m for m in measurements if m.get("status") == "ok"
            and m.get("flux") is not None and m.get("sigma_flux") is not None
            and math.isfinite(float(m["flux"]))
            and math.isfinite(float(m["sigma_flux"]))
            and m["sigma_flux"] > 0]
    if not good:
        return {"status": "unmeasurable", "n_used": 0, "flux": None, "sigma_flux": None, "snr": None}
    f = np.array([m["flux"] for m in good], dtype=float)
    w = 1.0 / (np.array([m["sigma_flux"] for m in good], dtype=float) ** 2)
    w_sum = float(np.sum(w))
    flux_mean = float(np.sum(w * f) / w_sum)
    sigma_mean = math.sqrt(1.0 / w_sum)
    return {
        "status": "ok",
        "n_used": len(good),
        "flux": flux_mean,
        "sigma_flux": sigma_mean,
        "snr": float(flux_mean / sigma_mean) if sigma_mean > 0 else math.nan,
    }


def forced_phot(ra, dec, frames):
    """Measure a fixed position already expressed in each supplied WCS sky frame.

Each frame needs frame_id, mjd_avg, pass_id, image, variance, flags, image_unit,
epsf_grid, corrected_cutout_wcs, crpix1a, crpix2a and var_scale. EPSFGrid carries
the declared release/detector and representative spectral metadata. A supplied
CWAVE/CBAND pair overrides the region values only with explicit spectral_source.
Corrected WCS must be the cutout WCS; this function never estimates a correction
or transforms celestial reference frames. Convert RA/Dec upstream when needed.
"""
    from b_astrometri.centroid.coordinates import sky_to_frame_coordinates

    required = {"frame_id", "mjd_avg", "pass_id", "image", "variance", "flags",
                "image_unit", "epsf_grid", "corrected_cutout_wcs", "crpix1a", "crpix2a", "var_scale"}
    rows = []
    for frame in frames:
        missing = required - frame.keys()
        if missing:
            raise ValueError(f"Incomplete photometry frame contract: {sorted(missing)}")
        if not str(frame["image_unit"]).strip() or frame["image_unit"] is None:
            raise ValueError("Frame image_unit must be explicitly supplied")
        grid = frame["epsf_grid"]
        if getattr(grid, "release", "").upper() not in {"QR3", "DR1"}:
            raise ValueError("Photometry requires a QR3/DR1 EPSFGrid")
        if not math.isfinite(float(frame["mjd_avg"])):
            raise ValueError("mjd_avg must be finite")
        var_scale = float(frame["var_scale"])
        if not math.isfinite(var_scale) or var_scale < 1:
            raise ValueError("Frame var_scale must be finite and >=1")
        if "detector" in frame and int(frame["detector"]) != grid.detector:
            raise ValueError("Frame detector differs from EPSF detector")
        if "release" in frame and frame["release"].upper() != grid.release:
            raise ValueError("Frame release differs from EPSF release")
        coords = sky_to_frame_coordinates(ra, dec,
            corrected_cutout_wcs=frame["corrected_cutout_wcs"],
            crpix1a=frame["crpix1a"], crpix2a=frame["crpix2a"])
        img, var, flags = (np.asarray(frame[k]) for k in ("image", "variance", "flags"))
        if img.ndim != 2 or not img.size or img.shape != var.shape or img.shape != flags.shape:
            raise ValueError("Frame IMAGE/VARIANCE/FLAGS must be equal nonempty 2D arrays")
        if (flags.dtype.kind not in "iu" or np.any(flags < 0)
                or np.any(flags > np.iinfo(np.uint32).max)):
            raise ValueError("Frame FLAGS must contain uint32-compatible integers")
        metadata = {"frame_id": frame["frame_id"], "mjd": float(frame["mjd_avg"]),
                    "pass_id": frame["pass_id"], "detector": grid.detector, "release": grid.release,
                    "image_unit": str(frame["image_unit"]), "flux_unit": "uncalibrated_model_amplitude",
                    "physical_flux_validated": False, "epsf_norm_multiplier": float(grid.norm),
                    "var_scale": var_scale, "wcs_corrected": True,
                    "wcs_correction_status": "caller_supplied_not_verified",
                    "fit_mask": f"0x{DEFAULT_BAD_FLAGS:08X}", **coords}
        x, y = coords["x_cutout"], coords["y_cutout"]
        if not (-0.5 <= x < img.shape[1] - 0.5 and -0.5 <= y < img.shape[0] - 0.5):
            rows.append({**metadata, "status": "outside_cutout", "flux": None,
                         "sigma_flux": None, "background": None, "chi2_nu": None,
                         "cwave_um": None, "cband_um": None, "n_valid": 0,
                         "bad_fit": False, "saturated_fit": False, "warn_within_3px": False})
            continue
        zone = grid.zone_at(coords["x_parent"], coords["y_parent"])
        cwave, cband = zone["cwave_um"], zone["cband_um"]
        spectral_source = "EPSF region representative CWAVE/CBAND"
        if "cwave_um" in frame or "cband_um" in frame:
            if not {"cwave_um", "cband_um", "spectral_source"}.issubset(frame):
                raise ValueError("Spectral override needs cwave_um, cband_um and spectral_source")
            cwave, cband = float(frame["cwave_um"]), float(frame["cband_um"])
            spectral_source = str(frame["spectral_source"])
        if not all(math.isfinite(v) and v > 0 for v in (cwave, cband)):
            raise ValueError("CWAVE/CBAND must be positive and finite")
        metadata.update(cwave_um=float(cwave), cband_um=float(cband), spectral_source=spectral_source)
        # Only the stamp bounds are integer indices; source/model positions stay float.
        # 33 samples at 5x span ~6.4 native pixels; a 9x9 stamp also constrains b.
        cx, cy = int(math.floor(x + 0.5)), int(math.floor(y + 0.5))
        xs, ys = slice(max(0, cx - 4), min(img.shape[1], cx + 5)), slice(max(0, cy - 4), min(img.shape[0], cy + 5))
        yy, xx = np.mgrid[ys, xs]
        xx_parent = xx + (coords["x_parent"] - x)
        yy_parent = yy + (coords["y_parent"] - y)
        row = forced_phot_frame(grid, xx_parent, yy_parent, img[ys, xs], var[ys, xs],
            coords["x_parent"], coords["y_parent"], flags=flags[ys, xs],
            var_scale=frame["var_scale"], frame_meta=metadata)
        row["flags_or"] = int(np.bitwise_or.reduce(flags[ys, xs].astype(np.uint32).ravel()))
        rows.append(row)
    return rows


def write_forced_phot_csv(path, measurements):
    """Write per-frame measurements; None is blank, bad-fit flux stays absent."""
    fields = ["frame_id", "mjd", "pass_id", "detector", "release", "ra_deg", "dec_deg",
              "x_cutout", "y_cutout", "x_parent", "y_parent", "cwave_um", "cband_um",
              "spectral_source", "flux", "sigma_flux", "background", "chi2_nu", "status",
              "bad_fit", "saturated_fit", "warn_within_3px", "flags_or", "n_valid", "fit_mask",
              "var_scale", "epsf_norm_multiplier", "image_unit", "flux_unit", "physical_flux_validated",
              "wcs_corrected", "wcs_correction_status"]
    with Path(path).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(measurements)
