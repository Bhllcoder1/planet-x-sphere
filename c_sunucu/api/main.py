"""
c_sunucu/api/main.py — SPHEREx Blink Backend (FastAPI)
CORS proxy: tarayıcı IRSA TAP/S3'e doğrudan erişemez, bu sunucu aracılık eder.

Çalıştırmak için:
  pip install fastapi uvicorn httpx astropy numpy
  uvicorn main:app --host 0.0.0.0 --port 8000 --reload
"""

import io
import json
import logging
import os
from typing import Optional

import httpx
import numpy as np
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# astropy opsiyonel — yoksa WCS devre dışı
try:
    from astropy.io import fits
    from astropy.wcs import WCS
    ASTROPY_OK = True
except ImportError:
    ASTROPY_OK = False

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("spherex-api")

app = FastAPI(title="SPHEREx Blink API", version="1.0.0")

# CORS — geliştirme ve demo için tüm origin'e izin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

IRSA_TAP    = "https://irsa.ipac.caltech.edu/TAP/sync"
IRSA_GATOR  = "https://irsa.ipac.caltech.edu/cgi-bin/Gator/nph-query"
IRSA_SIA    = "https://irsa.ipac.caltech.edu/SIA"
S3_BASE     = "https://nasa-irsa-spherex.s3.amazonaws.com"
# SpaceApps / NASA Open Data Portal SPHEREx prefix
S3_DR1_BASE = "https://nasa-irsa-spherex.s3.amazonaws.com/dr1/level2"

# Bilinen SPHEREx IRSA tablo adları (öncelik sırasıyla dene)
SPHEREX_TABLES = ["spherex.sph_l2", "spherex_dr1.sph_l2", "spherex.level2"]
SPHEREX_TABLE  = os.getenv("SPHEREX_TABLE", SPHEREX_TABLES[0])


@app.get("/api/health")
async def health():
    status = {"status": "ok", "astropy": ASTROPY_OK, "table": SPHEREX_TABLE}
    # IRSA erişilebilirlik hızlı testi
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(IRSA_TAP, params={"QUERY": "SELECT TOP 1 * FROM TAP_SCHEMA.tables", "FORMAT": "json"})
            status["irsa_tap"] = r.status_code
    except Exception as e:
        status["irsa_tap"] = f"err:{e}"
    return status


async def _query_irsa(ra: float, dec: float, radius_deg: float, max_frames: int):
    """IRSA'yı TAP → Gator CGI → SIA sırasıyla dener. (rows, cols) ya da (None, None) döner."""
    # -- Yöntem 1: TAP (tüm bilinen tablo adlarını dene) --
    for table in SPHEREX_TABLES:
        adql = (
            f"SELECT file_name, ra, dec, mjd_obs, spat_lam, detector, orient "
            f"FROM {table} "
            f"WHERE CONTAINS(POINT('ICRS',ra,dec),CIRCLE('ICRS',{ra},{dec},{radius_deg:.6f}))=1 "
            f"ORDER BY mjd_obs "
            f"LIMIT {max_frames}"
        )
        try:
            async with httpx.AsyncClient(timeout=12) as client:
                r = await client.get(IRSA_TAP, params={"QUERY": adql, "FORMAT": "json"})
            if r.status_code == 200:
                data = r.json()
                rows = data.get("data", [])
                cols = [m["name"] for m in data.get("metadata", [])]
                log.info("IRSA TAP OK — tablo: %s, %d satır", table, len(rows))
                return rows, cols
            log.warning("IRSA TAP %s → HTTP %s", table, r.status_code)
        except Exception as e:
            log.warning("IRSA TAP %s hata: %s", table, e)

    # -- Yöntem 2: Gator CGI (catalog=spherex_dr1 veya spherex_l2) --
    for catalog in ["spherex_l2", "spherex_dr1", "sph_l2"]:
        try:
            params = {
                "catalog": catalog,
                "spatial": "cone", "ra": ra, "dec": dec,
                "radius": radius_deg * 3600,  # arcsec
                "outfmt": "1",  # IPAC table
                "selcols": "fname,ra,dec,mjd_obs,spat_lam,detector",
                "maxrec": max_frames,
            }
            async with httpx.AsyncClient(timeout=15) as client:
                r = await client.get(IRSA_GATOR, params=params)
            if r.status_code == 200 and "\\char" in r.text:
                rows, cols = _parse_ipac_table(r.text, max_frames)
                if rows:
                    log.info("IRSA Gator OK — katalog: %s, %d satır", catalog, len(rows))
                    return rows, cols
        except Exception as e:
            log.warning("IRSA Gator %s hata: %s", catalog, e)

    # -- Yöntem 3: SIA v2 (görüntü envanteri) --
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(
                f"{IRSA_SIA}/SPHEREx",
                params={"POS": f"CIRCLE {ra} {dec} {radius_deg}", "MAXREC": max_frames, "FORMAT": "json"},
            )
        if r.status_code == 200:
            sia_data = r.json()
            rows, cols = _parse_sia_response(sia_data, max_frames)
            if rows:
                log.info("IRSA SIA OK — %d satır", len(rows))
                return rows, cols
    except Exception as e:
        log.warning("IRSA SIA hata: %s", e)

    log.error("Tüm IRSA erişim yöntemleri başarısız — ra=%.4f dec=%.4f", ra, dec)
    return None, None


def _parse_ipac_table(text: str, max_rows: int) -> tuple:
    """Basit IPAC tablo ayrıştırıcı → (rows, cols)."""
    lines = [l for l in text.splitlines() if not l.startswith("\\") and not l.startswith("|")]
    header_lines = [l for l in text.splitlines() if l.startswith("|")]
    if not header_lines:
        return [], []
    col_names = [c.strip() for c in header_lines[0].split("|") if c.strip()]
    rows = []
    for line in lines[:max_rows]:
        parts = line.split()
        if len(parts) >= len(col_names):
            rows.append(parts[:len(col_names)])
    return rows, col_names


def _parse_sia_response(data: dict, max_rows: int) -> tuple:
    """VOTable/JSON SIA yanıtını (rows, cols) biçimine çevir."""
    try:
        table = data.get("resultsets", [{}])[0]
        cols = [f["name"] for f in table.get("fields", [])]
        rows = table.get("data", [])[:max_rows]
        return rows, cols
    except Exception:
        return [], []


@app.get("/api/cutout")
async def get_cutout(
    ra: float = Query(..., description="Sağ Yükseliş (derece, 0–360)"),
    dec: float = Query(..., description="Diklik (derece, -90 – +90)"),
    radius: float = Query(3.0, description="Arama yarıçapı (arcmin, 0.5–10)"),
    max_frames: int = Query(20, description="Maks. kare sayısı"),
):
    """
    Verilen (RA, Dec) koordinatına en yakın SPHEREx L2 karelerini döndürür.
    1. IRSA TAP'ı sorgula → s3_key listesi al
    2. Her FITS dosyasını S3'ten çek → 31x31 kesit çıkar
    3. Frontend'in beklediği JSON formatında döndür
    """
    if not (0 <= ra <= 360):
        raise HTTPException(422, "RA 0–360 aralığında olmalı")
    if not (-90 <= dec <= 90):
        raise HTTPException(422, "Dec -90 – +90 aralığında olmalı")
    radius = max(0.5, min(10.0, radius))
    radius_deg = radius / 60.0

    # --- 1. IRSA'yı üç farklı yöntemle dene ---
    rows, cols = await _query_irsa(ra, dec, radius_deg, max_frames)

    if rows is None:
        raise HTTPException(502, "IRSA TAP/Gator/SIA servisleri erişilemiyor. Lütfen tekrar deneyin.")

    def col(row, *names):
        for name in names:
            try:
                v = row[cols.index(name)]
                if v is not None and v != "null":
                    return v
            except (ValueError, IndexError):
                pass
        return None

    if not rows:
        return JSONResponse({"frames": [], "message": "Bu koordinatta SPHEREx karesi bulunamadı."})

    # 2. Her kare için FITS çek ve 31x31 kesit al
    frames = []
    async with httpx.AsyncClient(timeout=30) as client:
        for i, row in enumerate(rows[:max_frames]):
            fname = col(row, "file_name", "fname", "filename") or ""
            ra_frame = float(col(row, "ra", "ra_j2000") or ra)
            dec_frame = float(col(row, "dec", "dec_j2000") or dec)
            mjd = col(row, "mjd_obs", "mjd")
            cwave = float(col(row, "spat_lam", "wavelength", "lambda") or 0)
            detector = str(col(row, "detector", "det_id") or "?")

            frame = {
                "frame_id": f"tap_{i}",
                "pass_id": i,
                "detector": detector,
                "cwave_um": cwave,
                "utc_date": f"MJD {mjd}" if mjd else "?",
                "target_x": 15,
                "target_y": 15,
                "raw_record": {
                    "s3_key": fname,
                    "measured_centroid": {
                        "ra_deg": ra_frame,
                        "dec_deg": dec_frame,
                        "x_cutout": 15,
                        "y_cutout": 15,
                        "sigma_x_px": 0.5,
                        "sigma_y_px": 0.5,
                    },
                    "image_mjy_sr": None,
                    "variance_mjy_sr2": None,
                    "zodi_mjy_sr": None,
                    "flags_bitmask": None,
                    "provenance_type": "IRSA_TAP_L2",
                },
            }

            # FITS dosyasını S3'ten çekmeyi dene
            if fname and ASTROPY_OK:
                s3_url = f"{S3_BASE}/{fname}"
                try:
                    r = await client.get(s3_url)
                    if r.status_code == 200:
                        cutout = _extract_cutout(r.content, ra, dec)
                        if cutout:
                            frame["raw_record"].update(cutout)
                            frame["target_x"] = cutout.get("target_x", 15)
                            frame["target_y"] = cutout.get("target_y", 15)
                except Exception as e:
                    log.debug("S3 çekme hatası %s: %s", fname, e)

            frames.append(frame)

    return JSONResponse({"frames": frames, "count": len(frames), "query": {"ra": ra, "dec": dec, "radius_arcmin": radius}})


def _extract_cutout(fits_bytes: bytes, ra: float, dec: float, size: int = 31) -> Optional[dict]:
    """FITS dosyasından (ra,dec) merkezli size×size kesit çıkar."""
    if not ASTROPY_OK:
        return None
    try:
        with fits.open(io.BytesIO(fits_bytes)) as hdul:
            # SPHEREx L2: IMAGE, VARIANCE, ZODI, FLAGS uzantıları
            img_hdu  = hdul["IMAGE"]   if "IMAGE"    in [h.name for h in hdul] else hdul[1]
            var_hdu  = hdul["VARIANCE"] if "VARIANCE" in [h.name for h in hdul] else None
            zodi_hdu = hdul["ZODI"]     if "ZODI"     in [h.name for h in hdul] else None
            flag_hdu = hdul["FLAGS"]    if "FLAGS"    in [h.name for h in hdul] else None

            wcs = WCS(img_hdu.header, naxis=2)
            px, py = wcs.all_world2pix([[ra, dec]], 0)[0]
            px, py = int(round(px)), int(round(py))

            half = size // 2
            img_data = img_hdu.data
            h, w = img_data.shape
            x0, y0 = max(0, px - half), max(0, py - half)
            x1, y1 = min(w, px + half + 1), min(h, py + half + 1)

            def to_list(arr):
                if arr is None:
                    return None
                patch = arr[y0:y1, x0:x1]
                # NaN → None
                return [[None if np.isnan(v) else float(v) for v in row] for row in patch]

            img_patch = to_list(img_data)
            if img_patch is None or len(img_patch) == 0:
                return None

            # WCS sözlüğü
            hdr = img_hdu.header
            wcs_dict = {k: hdr.get(k) for k in
                ["CTYPE1","CTYPE2","CRVAL1","CRVAL2","CRPIX1","CRPIX2",
                 "CD1_1","CD1_2","CD2_1","CD2_2","NAXIS1","NAXIS2",
                 "A_ORDER","B_ORDER","AP_ORDER","BP_ORDER"] if hdr.get(k) is not None}
            # SIP katsayıları
            for prefix in ["A","B","AP","BP"]:
                order = hdr.get(f"{prefix}_ORDER", 0)
                for p in range(order + 1):
                    for q in range(order + 1 - p):
                        key = f"{prefix}_{p}_{q}"
                        if hdr.get(key) is not None:
                            wcs_dict[key] = float(hdr[key])

            return {
                "image_mjy_sr": img_patch,
                "variance_mjy_sr2": to_list(var_hdu.data if var_hdu else None),
                "zodi_mjy_sr": to_list(zodi_hdu.data if zodi_hdu else None),
                "flags_bitmask": to_list(flag_hdu.data if flag_hdu else None),
                "wcs": wcs_dict,
                "cutout_size": size,
                "target_x": float(px - x0),
                "target_y": float(py - y0),
                "s3_https_url": None,
                "provenance_type": "S3_FITS_L2_DIRECT",
            }
    except Exception as e:
        log.debug("Kesit çıkarma hatası: %s", e)
        return None
