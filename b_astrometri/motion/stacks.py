"""04-02: exact-reprojected, display-only pass stacks and channel-safe differences.

Noise after reprojection is nominal: interpolated pixels are correlated, and
reprojecting a variance plane does not propagate squared overlap coefficients.
Only aligned-grid noise is validated by the independent-noise formula below.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from a_veri_isleme.process.masks import PROFILE_CENTROID_MASK, build_pixel_mask

BADGE = "Yeniden örneklendi — astrometri yok"
DEFAULT_BAD_FLAGS = PROFILE_CENTROID_MASK


def _labels():
    return {"mode": "S", "view_only": True, "astrometry_allowed": False,
            "measurement_allowed": False, "badge": BADGE, "psf_matched": False}


def inverse_variance_stack(images, variances, *, masks=None):
    """Combine >=2 aligned surface-brightness planes without modifying inputs.

    Pixels with fewer than two valid contributors remain NaN. Variance and noise
    assume independent input samples; callers must disclose resampling effects.
    """
    images = np.asarray(images, dtype=float)
    variances = np.asarray(variances, dtype=float)
    if images.ndim != 3 or images.shape[0] < 2 or images.shape != variances.shape:
        raise ValueError("Need >=2 images and matching variance planes [frame,y,x]")
    valid = np.isfinite(images) & np.isfinite(variances) & (variances > 0)
    if masks is not None:
        masks = np.asarray(masks)
        if masks.dtype.kind != "b" or masks.shape != images.shape:
            raise ValueError("Masks must be boolean and match image shape")
        valid &= ~masks
    weights = np.divide(1.0, variances, out=np.zeros_like(variances), where=valid)
    total_weight = weights.sum(axis=0)
    coverage = valid.sum(axis=0)
    usable = (coverage >= 2) & (total_weight > 0) & np.isfinite(total_weight)
    numerator = (np.where(valid, images, 0.0) * weights).sum(axis=0)
    image = np.divide(numerator, total_weight, out=np.full(images.shape[1:], np.nan), where=usable)
    variance = np.divide(1.0, total_weight, out=np.full(images.shape[1:], np.nan), where=usable)
    return {"image": image, "variance": variance, "noise": np.sqrt(variance),
            "coverage": coverage, **_labels()}


def _same_grid(left, right):
    return left.to_header(relax=True).tostring() == right.to_header(relax=True).tostring()


def stack_pass(frames, *, target_wcs, shape_out):
    """Stack one detector/pass/release onto a caller-supplied TAN WCS grid.

    Frame keys: frame_id, detector, pass_id, release, wavelength_um, image,
    variance, wcs; optional boolean mask and uint32 flags. IMAGE/VARIANCE inputs
    are surface brightness and squared surface brightness in matching units.
    Masking uses A's conservative centroid profile, never replaces native data.
    """
    if len(frames) < 2:
        raise ValueError("At least two frames are required for a pass stack")
    shape_out = tuple(shape_out)
    if len(shape_out) != 2 or any(int(v) != v or v <= 0 for v in shape_out):
        raise ValueError("Output shape must be two positive integers")
    if not target_wcs.has_celestial or list(target_wcs.wcs.ctype) != ["RA---TAN", "DEC--TAN"]:
        raise ValueError("Target must be a two-dimensional celestial TAN WCS")
    ids = [str(f["frame_id"]) for f in frames]
    if any(not fid for fid in ids) or len(set(ids)) != len(ids):
        raise ValueError("Frame identities must be nonempty and unique")
    for field in ("detector", "pass_id", "release"):
        if len({f[field] for f in frames}) != 1:
            raise ValueError(f"Cannot mix {field} values in one pass stack")
    detector, release = frames[0]["detector"], frames[0]["release"]
    if detector not in range(1, 7) or release not in {"DR1", "QR3"}:
        raise ValueError("Require detector 1..6 and explicitly identified DR1 or QR3 release")
    wavelengths = [float(f["wavelength_um"]) for f in frames]
    if not all(math.isfinite(v) and v > 0 for v in wavelengths):
        raise ValueError("Wavelengths must be finite positive micrometres")
    images, variances, resampled, frame_valid_pixels = [], [], False, {}
    for frame in frames:
        image, variance = np.asarray(frame["image"], dtype=float), np.asarray(frame["variance"], dtype=float)
        if image.ndim != 2 or image.shape != variance.shape:
            raise ValueError("Image and variance must be matching two-dimensional arrays")
        mask = np.asarray(frame.get("mask", np.zeros(image.shape, dtype=bool)))
        if mask.dtype.kind != "b" or mask.shape != image.shape:
            raise ValueError("Frame mask must be boolean with image shape")
        flags = np.asarray(frame.get("flags", np.zeros(image.shape, dtype=np.uint32)))
        if flags.shape != image.shape or flags.dtype.kind not in "iu":
            raise ValueError("Flags must be an integer array with image shape")
        mask = mask | build_pixel_mask(flags, image=image, variance=variance, profile="centroid")
        clean_image, clean_variance = np.where(mask, np.nan, image), np.where(mask, np.nan, variance)
        if image.shape == shape_out and _same_grid(frame["wcs"], target_wcs):
            projected, projected_variance = clean_image, clean_variance
        else:
            from reproject import reproject_exact
            projected, footprint = reproject_exact((clean_image, frame["wcs"]), target_wcs,
                                                   shape_out=shape_out)
            projected_variance, var_footprint = reproject_exact((clean_variance, frame["wcs"]),
                                                               target_wcs, shape_out=shape_out)
            absent = (footprint <= 0) | (var_footprint <= 0)
            projected = np.where(absent, np.nan, projected)
            projected_variance = np.where(absent, np.nan, projected_variance)
            resampled = True
        images.append(projected)
        variances.append(projected_variance)
        frame_valid_pixels[str(frame["frame_id"])] = int(np.count_nonzero(
            np.isfinite(projected) & np.isfinite(projected_variance) & (projected_variance > 0)))
    result = inverse_variance_stack(images, variances)
    result.update({"frame_ids": ids, "wavelengths_um": wavelengths, "detector": detector,
                   "pass_id": frames[0]["pass_id"], "release": release,
                   "frame_valid_pixels": frame_valid_pixels,
                   "target_wcs": target_wcs, "resampled": resampled,
                   "noise_model": "nominal diagonal variance; resampling covariance unpropagated"
                       if resampled else "independent aligned input variances",
                   "noise_validation": "pending real-data empty-sky test",
                   "units": "MJy/sr", "variance_units": "(MJy/sr)^2"})
    return result


def difference_stacks(left, right, *, channel_width_um):
    """Subtract same-detector/release stacks only within one wavelength channel."""
    if not math.isfinite(channel_width_um) or channel_width_um <= 0:
        raise ValueError("Channel width must be finite and positive")
    for field in ("detector", "release"):
        if left[field] != right[field]:
            raise ValueError(f"Cannot difference different {field} values")
    if (left["image"].shape != right["image"].shape
            or not _same_grid(left["target_wcs"], right["target_wcs"])):
        raise ValueError("Difference requires identical target WCS and shape")
    wavelengths = left["wavelengths_um"] + right["wavelengths_um"]
    if not wavelengths or max(wavelengths) - min(wavelengths) > channel_width_um:
        raise ValueError("All contributing wavelengths must fit within one channel width")
    if set(left["frame_ids"]) & set(right["frame_ids"]):
        raise ValueError("Difference stacks must not share input frames")
    image = left["image"] - right["image"]
    variance = left["variance"] + right["variance"]
    return {"image": image, "variance": variance, "noise": np.sqrt(variance),
            "coverage": np.minimum(left["coverage"], right["coverage"]),
            "detector": left["detector"], "release": left["release"],
            "target_wcs": left["target_wcs"], "wavelengths_um": wavelengths,
            "frame_ids": left["frame_ids"] + right["frame_ids"],
            "pass_ids": [left["pass_id"], right["pass_id"]],
            "noise_model": "sum of independent stack diagonal variances; covariance ignored",
            "units": "MJy/sr", **_labels()}


def validation_metrics(stack, difference, *, empty_sky_mask, static_star_mask):
    """D10 ingredients, not a claim of acceptance without supplied valid regions."""
    def selected(product, mask):
        mask = np.asarray(mask)
        if mask.dtype.kind != "b" or mask.shape != product["image"].shape:
            raise ValueError("Validation region masks must match product shape")
        valid = mask & np.isfinite(product["image"]) & np.isfinite(product["noise"]) & (product["noise"] > 0)
        if np.count_nonzero(valid) < 2:
            raise ValueError("Need at least two finite validation pixels")
        return valid
    sky, stars = selected(stack, empty_sky_mask), selected(difference, static_star_mask)
    ratio = float(np.std(stack["image"][sky], ddof=1) / np.sqrt(np.mean(stack["variance"][sky])))
    residual = float(np.median(np.abs(difference["image"][stars]) / difference["noise"][stars]))
    return {"noise_ratio": ratio, "noise_within_20_percent": 0.8 <= ratio <= 1.2,
            "static_residual_median_sigma": residual, "static_residual_below_3_sigma": residual < 3,
            "sky_pixels": int(sky.sum()), "static_pixels": int(stars.sum()),
            "scope": "supplied regions only; resampled covariance and PSF differences not corrected"}


def write_stack_products(product, directory, *, stem):
    """Write little-endian float32 view planes plus JSON provenance, never native measurement products."""
    directory = Path(directory)
    if Path(stem).name != stem or not stem:
        raise ValueError("Product stem must be a plain nonempty filename")
    directory.mkdir(parents=True, exist_ok=True)
    paths = {}
    for name in ("image", "noise"):
        path = directory / f"{stem if name == 'image' else 'noise_' + stem}.f32"
        np.asarray(product[name], dtype="<f4").tofile(path)
        paths[name] = str(path)
    metadata = {k: v for k, v in product.items() if k not in {"image", "variance", "noise", "coverage", "target_wcs"}}
    metadata.update({"shape": list(product["image"].shape), "dtype": "<f4", "files": paths,
                     "wcs_header": product["target_wcs"].to_header(relax=True).tostring(sep="\n")})
    path = directory / f"{stem}.json"
    path.write_text(json.dumps(metadata, indent=2, allow_nan=False), encoding="utf-8")
    return {**paths, "metadata": str(path)}
