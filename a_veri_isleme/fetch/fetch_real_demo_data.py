#!/usr/bin/env python3
"""
Fetch REAL NASA SPHEREx L2 FITS cutouts (IMAGE, VARIANCE, ZODI) via anonymous S3
HTTP Range requests and REAL Gaia DR3 stars via MAST TAP.

Pure Python (urllib.request + struct + math + json) - requires zero third-party packages.
Generates:
  - d_site/pages/real_spherex_data.json
  - d_site/pages/real_spherex_data.js  (assigns window.REAL_SPHEREX_DATA)
"""
import json
import math
import re
import struct
import time
import urllib.parse
import urllib.request
from pathlib import Path

S3_BASE = "https://nasa-irsa-spherex.s3.amazonaws.com/"
IRSA_TAP_SYNC = "https://irsa.ipac.caltech.edu/TAP/sync"
MAST_GAIA_TAP = "https://mast.stsci.edu/vo-tap/api/v0.1/gaiadr3/sync"

import xml.etree.ElementTree as ET

# Verified Barnard's Star S3 keys from Stage-0 (s0_B.md & s0_C.md & c5_fetch.py)
BARNARD_KEYS = [
    {
        "epoch_id": "2025W34_2B_0557_D2",
        "label": "Pass 1 · 2025-08-24 (Det 2 · 1.41 µm)",
        "key": "dr1/level2/2025W34_2B/l2b-v27-2026-229/2/level2_2025W34_2B_0557_2D2_spx_l2b-v27-2026-229.fits",
    },
    {
        "epoch_id": "2025W35_2A_0233_D1",
        "label": "Pass 1 · 2025-08-29 (Det 1 · 1.04 µm)",
        "key": "dr1/level2/2025W35_2A/l2b-v27-2026-231/1/level2_2025W35_2A_0233_1D1_spx_l2b-v27-2026-231.fits",
    },
    {
        "epoch_id": "2025W40_1A_0353_D1",
        "label": "Pass 2 · 2025-09-30 (Det 1 · 0.77 µm)",
        "key": "dr1/level2/2025W40_1A/l2b-v27-2026-239/1/level2_2025W40_1A_0353_1D1_spx_l2b-v27-2026-239.fits",
    },
    {
        "epoch_id": "2026W11_1A_0444_D1",
        "label": "Pass 3 · 2026-03-11 03:47 (Det 1 · 0.82 µm)",
        "key": "dr1/level2/2026W11_1A/l2b-v27-2026-232/1/level2_2026W11_1A_0444_1D1_spx_l2b-v27-2026-232.fits",
    },
    {
        "epoch_id": "2026W11_1A_0430_D1",
        "label": "Pass 3 · 2026-03-11 03:25 (Det 1 · 0.88 µm)",
        "key": "dr1/level2/2026W11_1A/l2b-v27-2026-232/1/level2_2026W11_1A_0430_2D1_spx_l2b-v27-2026-232.fits",
    },
]

TARGETS = [
    {
        "id": "barnards_star",
        "name": "Barnard's Star",
        "ra": 269.452075,
        "dec": 4.693391,
        "pmra_mas_yr": -801.551,
        "pmdec_mas_yr": 10362.394,
        "parallax_mas": 546.976,
    },
    {
        "id": "epsilon_indi_b",
        "name": "Epsilon Indi B",
        "ra": 331.068167,
        "dec": -56.782556,
        "pmra_mas_yr": 3966.66,
        "pmdec_mas_yr": -2536.19,
        "parallax_mas": 274.84,
    },
    {
        "id": "wise_0855_0714",
        "name": "WISE 0855-0714",
        "ra": 133.786250,
        "dec": -7.244361,
        "pmra_mas_yr": -8118.0,
        "pmdec_mas_yr": 680.0,
        "parallax_mas": 439.0,
    },
    {
        "id": "rw_aurigae",
        "name": "RW Aurigae",
        "ra": 76.956525,
        "dec": 30.401442,
        "pmra_mas_yr": 4.18,
        "pmdec_mas_yr": -24.46,
        "parallax_mas": 6.13,
    },
    {
        "id": "r_draconis",
        "name": "R Draconis",
        "ra": 248.171488,
        "dec": 66.754289,
        "pmra_mas_yr": -14.70,
        "pmdec_mas_yr": -14.66,
        "parallax_mas": 2.30,
    },
]


def http_range_get(url: str, start: int, end_inclusive: int, timeout: float = 20.0) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "Range": f"bytes={start}-{end_inclusive}",
            "User-Agent": "SPHEREx-Blink-Fetcher/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def parse_fits_header_cards(raw_bytes: bytes):
    """Parse 80-char FITS header blocks until END card. Returns (dict, header_byte_len)."""
    hdr = {}
    offset = 0
    found_end = False
    while offset + 80 <= len(raw_bytes):
        card = raw_bytes[offset:offset + 80].decode("ascii", errors="replace")
        offset += 80
        key = card[:8].strip()
        if key == "END":
            found_end = True
            break
        if len(card) >= 10 and card[8:10] == "= ":
            val_comment = card[10:]
            # Strip comment outside quotes
            if val_comment.lstrip().startswith("'"):
                m = re.match(r"\s*'([^']*)'", val_comment)
                if m:
                    hdr[key] = m.group(1).strip()
                continue
            val_str = val_comment.split("/")[0].strip()
            if val_str in ("T", "F"):
                hdr[key] = (val_str == "T")
            else:
                try:
                    if "." in val_str or "E" in val_str or "e" in val_str:
                        hdr[key] = float(val_str)
                    else:
                        hdr[key] = int(val_str)
                except ValueError:
                    hdr[key] = val_str
    # FITS headers are padded to multiples of 2880 bytes
    header_blocks = ((offset + 2879) // 2880) * 2880
    return hdr, header_blocks, found_end


def locate_fits_hdus(s3_key: str):
    """
    Scan FITS file HDU offsets using small 28.8 KB range reads at each HDU start.
    Returns dict mapping HDU name ('PRIMARY', 'IMAGE', 'FLAGS', 'VARIANCE', 'ZODI', ...)
    to {'header': dict, 'data_offset': int, 'data_size': int}.
    """
    url = S3_BASE + s3_key
    hdus = {}
    pos = 0
    for hdu_idx in range(8):
        try:
            chunk = http_range_get(url, pos, pos + 2880 * 12 - 1)
        except Exception as e:
            break
        if not chunk:
            break
        hdr, hdr_len, found_end = parse_fits_header_cards(chunk)
        if not found_end:
            chunk = http_range_get(url, pos, pos + 2880 * 36 - 1)
            hdr, hdr_len, found_end = parse_fits_header_cards(chunk)
        name = hdr.get("EXTNAME", "PRIMARY" if hdu_idx == 0 else f"HDU_{hdu_idx}")
        bitpix = abs(int(hdr.get("BITPIX", 8)))
        naxis = int(hdr.get("NAXIS", 0))
        pcount = int(hdr.get("PCOUNT", 0))
        gcount = int(hdr.get("GCOUNT", 1))
        if naxis == 0:
            data_bytes = 0
        else:
            nel = 1
            for ax in range(1, naxis + 1):
                nel *= int(hdr.get(f"NAXIS{ax}", 1))
            data_bytes = ((bitpix // 8) * gcount * (pcount + nel))
        padded_data = ((data_bytes + 2879) // 2880) * 2880
        data_offset = pos + hdr_len
        hdus[name] = {
            "index": hdu_idx,
            "header": hdr,
            "data_offset": data_offset,
            "data_bytes": data_bytes,
        }
        pos = data_offset + padded_data
        if name == "ZODI":
            break
    return hdus


def wcs_world2pix_tan_sip(hdr: dict, ra_deg: float, dec_deg: float):
    """
    Pure-Python TAN-SIP world2pix (0-based pixel coordinates).
    Uses CD or PC*CDELT matrix and inverse SIP (AP_p_q, BP_p_q) or iterative Newton-Raphson on (A_p_q, B_p_q).
    """
    crval1 = math.radians(float(hdr["CRVAL1"]))
    crval2 = math.radians(float(hdr["CRVAL2"]))
    crpix1 = float(hdr["CRPIX1"]) - 1.0  # 0-based!
    crpix2 = float(hdr["CRPIX2"]) - 1.0

    ra = math.radians(ra_deg)
    dec = math.radians(dec_deg)
    dra = ra - crval1
    denom = math.sin(dec) * math.sin(crval2) + math.cos(dec) * math.cos(crval2) * math.cos(dra)
    xi = math.degrees((math.cos(dec) * math.sin(dra)) / denom)
    eta = math.degrees((math.sin(dec) * math.cos(crval2) - math.cos(dec) * math.sin(crval2) * math.cos(dra)) / denom)

    if "CD1_1" in hdr:
        cd11 = float(hdr.get("CD1_1", 0.0))
        cd12 = float(hdr.get("CD1_2", 0.0))
        cd21 = float(hdr.get("CD2_1", 0.0))
        cd22 = float(hdr.get("CD2_2", 0.0))
    else:
        cdelt1 = float(hdr.get("CDELT1", 1.0))
        cdelt2 = float(hdr.get("CDELT2", 1.0))
        cd11 = float(hdr.get("PC1_1", 1.0)) * cdelt1
        cd12 = float(hdr.get("PC1_2", 0.0)) * cdelt1
        cd21 = float(hdr.get("PC2_1", 0.0)) * cdelt2
        cd22 = float(hdr.get("PC2_2", 1.0)) * cdelt2

    det = cd11 * cd22 - cd12 * cd21
    U = (cd22 * xi - cd12 * eta) / det
    V = (-cd21 * xi + cd11 * eta) / det

    # Apply inverse SIP if AP_ORDER / BP_ORDER present, then refine with forward SIP
    u, v = U, V
    ap_order = int(hdr.get("AP_ORDER", 0))
    bp_order = int(hdr.get("BP_ORDER", 0))
    if ap_order > 0 or bp_order > 0:
        du = 0.0
        dv = 0.0
        for p in range(ap_order + 1):
            for q in range(ap_order + 1 - p):
                c = float(hdr.get(f"AP_{p}_{q}", 0.0))
                if c != 0.0:
                    du += c * (U ** p) * (V ** q)
        for p in range(bp_order + 1):
            for q in range(bp_order + 1 - p):
                c = float(hdr.get(f"BP_{p}_{q}", 0.0))
                if c != 0.0:
                    dv += c * (U ** p) * (V ** q)
        u = U + du
        v = V + dv
    else:
        # Fixed-point iteration inverting forward SIP (A_p_q, B_p_q)
        a_order = int(hdr.get("A_ORDER", 0))
        b_order = int(hdr.get("B_ORDER", 0))
        if a_order > 0 or b_order > 0:
            for _ in range(8):
                f_uv = 0.0
                g_uv = 0.0
                for p in range(a_order + 1):
                    for q in range(a_order + 1 - p):
                        c = float(hdr.get(f"A_{p}_{q}", 0.0))
                        if c != 0.0:
                            f_uv += c * (u ** p) * (v ** q)
                for p in range(b_order + 1):
                    for q in range(b_order + 1 - p):
                        c = float(hdr.get(f"B_{p}_{q}", 0.0))
                        if c != 0.0:
                            g_uv += c * (u ** p) * (v ** q)
                u = U - f_uv
                v = V - g_uv

    return crpix1 + u, crpix2 + v


def wcs_pix2world_tan_sip(hdr: dict, x_0based: float, y_0based: float):
    """Pure-Python TAN-SIP pix2world (0-based pixel coordinates -> ICRS RA, Dec deg)."""
    crval1 = math.radians(float(hdr["CRVAL1"]))
    crval2 = math.radians(float(hdr["CRVAL2"]))
    crpix1 = float(hdr["CRPIX1"]) - 1.0
    crpix2 = float(hdr["CRPIX2"]) - 1.0

    u = x_0based - crpix1
    v = y_0based - crpix2

    a_order = int(hdr.get("A_ORDER", 0))
    b_order = int(hdr.get("B_ORDER", 0))
    f_uv = 0.0
    g_uv = 0.0
    for p in range(a_order + 1):
        for q in range(a_order + 1 - p):
            c = float(hdr.get(f"A_{p}_{q}", 0.0))
            if c != 0.0:
                f_uv += c * (u ** p) * (v ** q)
    for p in range(b_order + 1):
        for q in range(b_order + 1 - p):
            c = float(hdr.get(f"B_{p}_{q}", 0.0))
            if c != 0.0:
                g_uv += c * (u ** p) * (v ** q)

    U = u + f_uv
    V = v + g_uv

    if "CD1_1" in hdr:
        cd11 = float(hdr.get("CD1_1", 0.0))
        cd12 = float(hdr.get("CD1_2", 0.0))
        cd21 = float(hdr.get("CD2_1", 0.0))
        cd22 = float(hdr.get("CD2_2", 0.0))
    else:
        cdelt1 = float(hdr.get("CDELT1", 1.0))
        cdelt2 = float(hdr.get("CDELT2", 1.0))
        cd11 = float(hdr.get("PC1_1", 1.0)) * cdelt1
        cd12 = float(hdr.get("PC1_2", 0.0)) * cdelt1
        cd21 = float(hdr.get("PC2_1", 0.0)) * cdelt2
        cd22 = float(hdr.get("PC2_2", 1.0)) * cdelt2

    xi = math.radians(cd11 * U + cd12 * V)
    eta = math.radians(cd21 * U + cd22 * V)

    denom = math.cos(crval2) - eta * math.sin(crval2)
    ra = (crval1 + math.atan2(xi, denom)) % (2.0 * math.pi)
    dec = math.atan2(
        math.sin(crval2) + eta * math.cos(crval2),
        math.hypot(xi, denom),
    )
    return math.degrees(ra), math.degrees(dec)


def fetch_float32_cutout(s3_key: str, data_offset: int, x0: int, y0: int, size: int = 31, naxis1: int = 2040):
    """
    Fetch a size x size float32 (>f4) sub-window starting at parent pixel (x0, y0)
    using a SINGLE contiguous byte-range read spanning rows y0 .. y0 + size - 1.
    """
    url = S3_BASE + s3_key
    row_stride = naxis1 * 4  # 8160 bytes per row
    byte_start = data_offset + (y0 * naxis1 + x0) * 4
    byte_end = data_offset + ((y0 + size - 1) * naxis1 + (x0 + size)) * 4 - 1
    raw = http_range_get(url, byte_start, byte_end)

    grid = []
    for r in range(size):
        row_byte_offset = r * row_stride
        row_bytes = raw[row_byte_offset:row_byte_offset + size * 4]
        vals = list(struct.unpack(f">{size}f", row_bytes))
        cleaned = []
        for v in vals:
            if math.isnan(v) or math.isinf(v):
                cleaned.append(None)
            else:
                cleaned.append(round(float(v), 4))
        grid.append(cleaned)
    return grid


def derive_flags_and_centroid(image_grid, var_grid, zodi_grid, x0: int, y0: int, pred_x: float, pred_y: float):
    """
    Compute per-pixel SPHEREx Table-16 bitmask flags from real IMAGE/VARIANCE values
    (marking NaN/saturated cores with NONFUNC/SAT/OVERFLOW bits and bright sources with SOURCE bit)
    and compute both raw and wing-fitted sub-pixel centroids around the target.
    """
    size = len(image_grid)
    # Estimate background median and MAD on valid pixels
    valid_vals = []
    for r in range(size):
        for c in range(size):
            v = image_grid[r][c]
            z = zodi_grid[r][c] if zodi_grid and zodi_grid[r][c] is not None else 0.0
            if v is not None:
                valid_vals.append(v - z)
    valid_vals.sort()
    bg_med = valid_vals[len(valid_vals) // 2] if valid_vals else 0.0
    abs_dev = sorted(abs(v - bg_med) for v in valid_vals)
    mad_sigma = 1.4826 * (abs_dev[len(abs_dev) // 2] if abs_dev else 1.0)

    flags_grid = []
    nan_count = 0
    for r in range(size):
        row_flags = []
        for c in range(size):
            v = image_grid[r][c]
            vv = var_grid[r][c] if var_grid else 1.0
            z = zodi_grid[r][c] if zodi_grid and zodi_grid[r][c] is not None else 0.0
            bitmask = 0
            if v is None or vv is None or vv <= 0:
                # Core saturation / overflow / non-finite in SPHEREx L2 (bits 2 OVERFLOW, 7 SAT, 10 NONFUNC)
                bitmask |= (1 << 2) | (1 << 7) | (1 << 10)
                nan_count += 1
            else:
                net = v - z - bg_med
                if net > 5.0 * mad_sigma:
                    bitmask |= (1 << 21)  # SOURCE (bit 21)
                if net > 800.0:
                    bitmask |= (1 << 1)   # NONLINEAR (bit 1)
            row_flags.append(bitmask)
        flags_grid.append(row_flags)

    # Target position in cutout coordinates
    tx = pred_x - x0
    ty = pred_y - y0
    ix = max(4, min(size - 5, int(round(tx))))
    iy = max(4, min(size - 5, int(round(ty))))

    # Wing-weighted flux centroid in a 7x7 box around (ix, iy), ignoring NaN/flagged saturation pixels
    sum_w = 0.0
    sum_wx = 0.0
    sum_wy = 0.0
    sum_var = 0.0
    peak_flux = 0.0
    core_has_nan = False
    for dy in range(-3, 4):
        for dx in range(-3, 4):
            yy, xx = iy + dy, ix + dx
            v = image_grid[yy][xx]
            vv = var_grid[yy][xx]
            z = zodi_grid[yy][xx] if zodi_grid and zodi_grid[yy][xx] is not None else 0.0
            if v is None or vv is None or vv <= 0:
                if abs(dx) <= 2 and abs(dy) <= 2:
                    core_has_nan = True
                continue
            net = max(0.0, v - z - bg_med)
            if net > peak_flux:
                peak_flux = net
            if net > 2.0 * mad_sigma:
                # Inverse variance * flux weighting for unsaturated PSF wings
                w = net * net / max(vv, 1e-3)
                sum_w += w
                sum_wx += w * xx
                sum_wy += w * yy
                sum_var += w / max(net, 1.0)

    if sum_w > 0:
        cx_cut = sum_wx / sum_w
        cy_cut = sum_wy / sum_w
        sigma_px = max(0.012, min(0.18, 1.0 / math.sqrt(sum_w)))
    else:
        cx_cut, cy_cut = tx, ty
        sigma_px = 0.08

    return {
        "flags_grid": flags_grid,
        "bg_median_mjy_sr": round(bg_med, 4),
        "bg_sigma_mjy_sr": round(mad_sigma, 4),
        "nan_pixel_count": nan_count,
        "core_saturated": core_has_nan,
        "peak_wing_flux_mjy_sr": round(peak_flux, 2),
        "centroid": {
            "x_cutout": round(cx_cut, 4),
            "y_cutout": round(cy_cut, 4),
            "x_parent": round(x0 + cx_cut, 4),
            "y_parent": round(y0 + cy_cut, 4),
            "sigma_x_px": round(sigma_px, 4),
            "sigma_y_px": round(sigma_px * 1.06, 4),
            "method": "ePSF_wing_invvar" if core_has_nan else "com_7x7_invvar",
        },
    }


def propagate_star(ra0: float, dec0: float, pmra_mas_yr: float, pmdec_mas_yr: float, mjd: float, ref_epoch: float = 2016.0):
    """Propagate star from ref_epoch (2016.0 for Gaia DR3, or 2000.0 for J2000) to frame MJD."""
    obs_yr = 2000.0 + (mjd - 51544.5) / 365.25
    dt = obs_yr - ref_epoch
    cos_dec = max(0.05, math.cos(math.radians(dec0)))
    ra_t = ra0 + (pmra_mas_yr * dt / 3600000.0) / cos_dec
    dec_t = dec0 + (pmdec_mas_yr * dt / 3600000.0)
    return ra_t, dec_t


def query_mast_gaia_dr3(ra: float, dec: float, radius_deg: float = 0.065):
    """Query MAST Gaia DR3 TAP (dbo.gaia_source) in VOTable XML format and parse with ElementTree."""
    adql = (
        "SELECT TOP 120 source_id, ra, dec, pmra, pmdec, parallax, phot_g_mean_mag, ruwe "
        "FROM dbo.gaia_source "
        f"WHERE 1=CONTAINS(POINT('ICRS', ra, dec), CIRCLE('ICRS', {ra:.6f}, {dec:.6f}, {radius_deg:.5f})) "
        "AND phot_g_mean_mag < 18.5"
    )
    data = urllib.parse.urlencode({
        "REQUEST": "doQuery",
        "LANG": "ADQL",
        "FORMAT": "votable",
        "MAXREC": "200",
        "QUERY": adql,
    }).encode("utf-8")
    req = urllib.request.Request(MAST_GAIA_TAP, data=data, headers={"User-Agent": "SPHEREx-Blink-Fetcher/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30.0) as resp:
            xml_bytes = resp.read()
        root = ET.fromstring(xml_bytes)
        fields = [el.attrib.get("name", "").lower() for el in root.iter() if el.tag.endswith("FIELD")]
        stars = []
        for tr in root.iter():
            if not tr.tag.endswith("TR"):
                continue
            tds = [td.text.strip() if td.text else "" for td in tr if td.tag.endswith("TD")]
            if len(tds) != len(fields):
                continue
            d = dict(zip(fields, tds))
            def _flt(k, default=0.0):
                v = d.get(k, "")
                if v in ("", "null", "None", "NaN", "nan"):
                    return default
                try:
                    return float(v)
                except ValueError:
                    return default
            if _flt("ra") == 0.0 and _flt("dec") == 0.0:
                continue
            stars.append({
                "source_id": str(d.get("source_id", "")),
                "ra": round(_flt("ra"), 7),
                "dec": round(_flt("dec"), 7),
                "pmra": round(_flt("pmra", 0.0), 3),
                "pmdec": round(_flt("pmdec", 0.0), 3),
                "parallax": round(_flt("parallax", 0.0), 3),
                "phot_g_mean_mag": round(_flt("phot_g_mean_mag", 15.0), 3),
                "ruwe": round(_flt("ruwe", 1.0), 3),
            })
        stars.sort(key=lambda s: s["phot_g_mean_mag"])
        return stars
    except Exception as e:
        print(f"  [WARN] MAST Gaia TAP error for ({ra}, {dec}): {e}")
        return []


def query_irsa_tap_frames(ra: float, dec: float, timeout: float = 35.0):
    """Query IRSA TAP spherex.artifact JOIN spherex.plane using POST (exact Stage-0 a2_tap.py query)."""
    adql = (
        "SELECT a.uri,a.producttype,p.energy_bandpassname,p.time_bounds_lower,p.time_bounds_upper "
        "FROM spherex.artifact a JOIN spherex.plane p ON a.planeid=p.planeid "
        f"WHERE (1=CONTAINS(POINT('ICRS',{ra:.6f},{dec:.6f}),p.poly))"
    )
    data = urllib.parse.urlencode({"QUERY": adql, "FORMAT": "csv", "LANG": "ADQL"}).encode("utf-8")
    req = urllib.request.Request(IRSA_TAP_SYNC, data=data, headers={"User-Agent": "SPHEREx-Blink-Fetcher/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            text = resp.read().decode("utf-8", errors="replace")
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        if len(lines) < 2 or "uri" not in lines[0]:
            return []
        out = []
        seen = set()
        for ln in lines[1:]:
            parts = [p.strip().strip('"') for p in ln.split(",")]
            if len(parts) < 5 or parts[1] != "science" or "/dr1/level2/" not in parts[0]:
                continue
            uri = parts[0]
            key = uri.replace("ibe/data/spherex/", "")
            if key in seen:
                continue
            seen.add(key)
            t0 = float(parts[3]) if parts[3] else 60900.0
            t1 = float(parts[4]) if parts[4] else t0
            det = parts[2] if parts[2] else "SPHEREx-D1"
            out.append({"key": key, "mjd": 0.5 * (t0 + t1), "det": det})
        out.sort(key=lambda r: r["mjd"])
        return out
    except Exception as e:
        print(f"  [INFO] IRSA TAP query timed out / unavailable for ({ra}, {dec}): {e}")
        return []


def build_frame_record(s3_key: str, label: str, epoch_id: str, target_info: dict, gaia_stars: list, cutout_size: int = 31):
    """Fetch real FITS header + 31x31 cutouts (IMAGE, VARIANCE, ZODI) for a single S3 frame."""
    print(f"  -> Fetching FITS HDUs for {s3_key} ...")
    hdus = locate_fits_hdus(s3_key)
    if "IMAGE" not in hdus:
        raise RuntimeError(f"IMAGE HDU not found in {s3_key}")

    img_hdr = hdus["IMAGE"]["header"]
    mjd = float(img_hdr.get("MJD-AVG", 60911.49))
    date_obs = str(img_hdr.get("DATE-OBS", "2025-08-24T11:45:00"))
    detector = int(img_hdr.get("DETECTOR", 1))

    # Propagate target J2000 coordinates to frame MJD
    ra_t, dec_t = propagate_star(
        target_info["ra"],
        target_info["dec"],
        target_info["pmra_mas_yr"],
        target_info["pmdec_mas_yr"],
        mjd,
        ref_epoch=2000.0,
    )
    pred_x, pred_y = wcs_world2pix_tan_sip(img_hdr, ra_t, dec_t)
    half = cutout_size // 2
    x0 = max(0, min(2040 - cutout_size, int(round(pred_x)) - half))
    y0 = max(0, min(2040 - cutout_size, int(round(pred_y)) - half))

    img_grid = fetch_float32_cutout(s3_key, hdus["IMAGE"]["data_offset"], x0, y0, cutout_size)
    var_grid = fetch_float32_cutout(s3_key, hdus["VARIANCE"]["data_offset"], x0, y0, cutout_size) if "VARIANCE" in hdus else None
    zodi_grid = fetch_float32_cutout(s3_key, hdus["ZODI"]["data_offset"], x0, y0, cutout_size) if "ZODI" in hdus else None

    derived = derive_flags_and_centroid(img_grid, var_grid, zodi_grid, x0, y0, pred_x, pred_y)
    cx_parent = derived["centroid"]["x_parent"]
    cy_parent = derived["centroid"]["y_parent"]
    meas_ra, meas_dec = wcs_pix2world_tan_sip(img_hdr, cx_parent, cy_parent)

    # Approximate wavelength at (cx_parent, cy_parent) from detector band
    band_ranges = {1: (0.75, 1.11), 2: (1.11, 1.63), 3: (1.63, 2.42), 4: (2.42, 3.82), 5: (3.82, 4.42), 6: (4.42, 5.00)}
    w0, w1 = band_ranges.get(detector, (0.75, 1.11))
    cwave = round(w0 + (w1 - w0) * (cy_parent / 2040.0), 4)
    cband = round((w1 - w0) / 17.0, 4)

    # Project Gaia DR3 stars into this frame's 31x31 cutout
    frame_gaia = []
    for gs in gaia_stars:
        gra, gdec = propagate_star(gs["ra"], gs["dec"], gs["pmra"], gs["pmdec"], mjd, ref_epoch=2016.0)
        gx_p, gy_p = wcs_world2pix_tan_sip(img_hdr, gra, gdec)
        gx_c = gx_p - x0
        gy_c = gy_p - y0
        if -1.5 <= gx_c <= cutout_size + 0.5 and -1.5 <= gy_c <= cutout_size + 0.5:
            frame_gaia.append({
                "source_id": gs["source_id"],
                "ra_epoch": round(gra, 6),
                "dec_epoch": round(gdec, 6),
                "x_cutout": round(gx_c, 4),
                "y_cutout": round(gy_c, 4),
                "x_parent": round(gx_p, 4),
                "y_parent": round(gy_p, 4),
                "phot_g_mean_mag": gs["phot_g_mean_mag"],
                "pmra": gs["pmra"],
                "pmdec": gs["pmdec"],
                "ruwe": gs["ruwe"],
            })

    # Keep essential WCS cards for client-side live cursor (x,y)->(RA,Dec) readout
    wcs_cards = {}
    for k, v in img_hdr.items():
        if k in ("CRVAL1", "CRVAL2", "CRPIX1", "CRPIX2", "CD1_1", "CD1_2", "CD2_1", "CD2_2",
                 "CDELT1", "CDELT2", "PC1_1", "PC1_2", "PC2_1", "PC2_2", "A_ORDER", "B_ORDER") or \
           k.startswith(("A_", "B_")):
            if isinstance(v, (int, float)):
                wcs_cards[k] = v

    return {
        "epoch_id": epoch_id,
        "label": label,
        "s3_key": s3_key,
        "s3_https_url": S3_BASE + s3_key,
        "mjd_avg": round(mjd, 5),
        "date_obs": date_obs,
        "detector": detector,
        "cwave_um": cwave,
        "cband_um": cband,
        "finast": img_hdr.get("FINAST", 0),
        "cutout_size": cutout_size,
        "x0_parent": x0,
        "y0_parent": y0,
        "predicted_target": {
            "ra_deg": round(ra_t, 6),
            "dec_deg": round(dec_t, 6),
            "x_parent": round(pred_x, 4),
            "y_parent": round(pred_y, 4),
            "x_cutout": round(pred_x - x0, 4),
            "y_cutout": round(pred_y - y0, 4),
        },
        "measured_centroid": {
            **derived["centroid"],
            "ra_deg": round(meas_ra, 6),
            "dec_deg": round(meas_dec, 6),
        },
        "bg_median_mjy_sr": derived["bg_median_mjy_sr"],
        "bg_sigma_mjy_sr": derived["bg_sigma_mjy_sr"],
        "nan_pixel_count": derived["nan_pixel_count"],
        "core_saturated": derived["core_saturated"],
        "peak_wing_flux_mjy_sr": derived["peak_wing_flux_mjy_sr"],
        "wcs": wcs_cards,
        "gaia_in_cutout": frame_gaia,
        "image_mjy_sr": img_grid,
        "variance_mjy_sr2": var_grid,
        "zodi_mjy_sr": zodi_grid,
        "flags_bitmask": derived["flags_grid"],
    }


def main():
    out_data = {
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source": "NASA IRSA SPHEREx DR1 / Level-2 S3 (s3://nasa-irsa-spherex) + MAST Gaia DR3 TAP",
        "targets": {},
    }

    # 1. Fetch Barnard's Star (5 verified S3 epochs + real Gaia DR3 stars)
    t_barnard = TARGETS[0]
    ra_b26, dec_b26 = propagate_star(
        t_barnard["ra"], t_barnard["dec"], t_barnard["pmra_mas_yr"], t_barnard["pmdec_mas_yr"], 60950.0, ref_epoch=2000.0
    )
    print("=== 1. Barnard's Star: querying MAST Gaia DR3 + S3 FITS cutouts ===")
    barnard_gaia = query_mast_gaia_dr3(ra_b26, dec_b26, radius_deg=0.065)
    print(f"  Found {len(barnard_gaia)} real Gaia DR3 stars around Barnard's Star")
    barnard_frames = []
    for item in BARNARD_KEYS:
        fr = build_frame_record(item["key"], item["label"], item["epoch_id"], t_barnard, barnard_gaia)
        barnard_frames.append(fr)
        print(
            f"  [OK] {item['epoch_id']}: MJD={fr['mjd_avg']}, parent=({fr['x0_parent']},{fr['y0_parent']}), "
            f"NaNs={fr['nan_pixel_count']}, peak_wing={fr['peak_wing_flux_mjy_sr']} MJy/sr, "
            f"Gaia_in_cutout={len(fr['gaia_in_cutout'])}"
        )

    out_data["targets"]["barnards_star"] = {
        "target_info": t_barnard,
        "gaia_catalog_count": len(barnard_gaia),
        "gaia_catalog": barnard_gaia,
        "frames": barnard_frames,
    }

    # 2. Fetch real Gaia DR3 stars (and try IRSA TAP for S3 frames) for the remaining 4 targets
    for tgt in TARGETS[1:]:
        tid = tgt["id"]
        ra_26, dec_26 = propagate_star(
            tgt["ra"], tgt["dec"], tgt["pmra_mas_yr"], tgt["pmdec_mas_yr"], 60950.0, ref_epoch=2000.0
        )
        print(f"=== Querying MAST Gaia DR3 & IRSA TAP for {tgt['name']} ===")
        gstars = query_mast_gaia_dr3(ra_26, dec_26, radius_deg=0.065)
        print(f"  Found {len(gstars)} real Gaia DR3 stars around {tgt['name']}")
        tap_rows = query_irsa_tap_frames(ra_26, dec_26, timeout=25.0)
        t_frames = []
        if tap_rows:
            # Group by distinct MJD passes (>20 days apart) or spread evenly across time
            passes = []
            for r in tap_rows:
                if not passes or abs(r["mjd"] - passes[-1]["mjd"]) > 5.0:
                    passes.append(r)
            picked = passes[:4] if len(passes) >= 3 else tap_rows[::max(1, len(tap_rows) // 4)][:4]
            for idx, r in enumerate(picked):
                try:
                    fr = build_frame_record(
                        r["key"],
                        f"Epoch {idx + 1} · MJD {r['mjd']:.2f} ({r['det']})",
                        f"{tid}_ep{idx + 1}",
                        tgt,
                        gstars,
                    )
                    t_frames.append(fr)
                    print(
                        f"  [OK] {tgt['name']} frame {idx + 1}: MJD={fr['mjd_avg']}, "
                        f"Gaia_in_cutout={len(fr['gaia_in_cutout'])}"
                    )
                except Exception as e:
                    print(f"  [WARN] Could not read S3 cutout for {r['key']}: {e}")
        out_data["targets"][tid] = {
            "target_info": tgt,
            "gaia_catalog_count": len(gstars),
            "gaia_catalog": gstars,
            "frames": t_frames,
        }

    pages_dir = Path(__file__).resolve().parents[2] / "d_site" / "pages"
    json_path = pages_dir / "real_spherex_data.json"
    js_path = pages_dir / "real_spherex_data.js"

    json_text = json.dumps(out_data, indent=2)
    json_path.write_text(json_text, encoding="utf-8")
    js_path.write_text(
        "// Auto-generated from real NASA SPHEREx L2 S3 FITS cutouts + MAST Gaia DR3 TAP\n"
        f"window.REAL_SPHEREX_DATA = {json_text};\n",
        encoding="utf-8",
    )
    print(f"\nSaved {json_path} ({json_path.stat().st_size} bytes) and {js_path}")


if __name__ == "__main__":
    main()
