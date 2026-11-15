"""
c_sunucu/api/main.py — SPHEREx Blink Backend (FastAPI)
CORS proxy: tarayıcı IRSA TAP/S3'e doğrudan erişemez, bu sunucu aracılık eder.

Çalıştırmak için:
  pip install fastapi uvicorn httpx astropy numpy
  uvicorn main:app --host 0.0.0.0 --port 8000 --reload
"""

import asyncio
import io
import json
import logging
import math
import os
import struct
import xml.etree.ElementTree as ET
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


@app.get("/api/s3-status")
async def s3_status():
    """S3 spatial index durumunu göster."""
    sample = {k: v for k, v in list(_S3_FIELD_INDEX.items())[:5]}
    return {
        "index_ready": _S3_INDEX_READY,
        "field_count": len(_S3_FIELD_INDEX),
        "sample_fields": sample,
    }


@app.get("/api/s3-test")
async def s3_test():
    """S3 erişim testi — prefix listesi ve ilk dosya header'ı."""
    async with httpx.AsyncClient(timeout=20) as client:
        prefixes = await _s3_list_prefixes(client, "dr1/level2/")
        result = {"prefix_count": len(prefixes), "first_5": prefixes[:5]}
        if prefixes:
            keys = await _s3_list_keys(client, prefixes[0], max_keys=2)
            result["sample_keys"] = keys
            if keys:
                hb = await _fits_header_range(client, keys[0], num_blocks=10)
                wcs = _parse_fits_wcs_from_bytes(hb)
                result["sample_wcs"] = wcs
    return result


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


# ─────────────────────────────────────────────────────────────
# DOĞRUDAN S3 ERIŞIMI (IRSA TAP olmadan)
# ─────────────────────────────────────────────────────────────

# In-memory spatial index: prefix → (ra_c, dec_c, ra_half, dec_half)
_S3_FIELD_INDEX: dict = {}
_S3_INDEX_LOCK = asyncio.Lock()
_S3_INDEX_READY = False

S3_LIST_URL = "https://nasa-irsa-spherex.s3.amazonaws.com"
S3_NS = "http://s3.amazonaws.com/doc/2006-03-01/"

# Bilinen hedeflerin doğrulanmış S3 key'leri (real_spherex_data.js'den)
# Her entry: (ra, dec, [s3_keys])
KNOWN_TARGET_KEYS: list[tuple] = [
    # Barnard's Star — 5 gerçek SPHEREx L2 gözlemi
    (269.45, 4.69, [
        "dr1/level2/2025W34_2B/l2b-v27-2026-229/2/level2_2025W34_2B_0557_2D2_spx_l2b-v27-2026-229.fits",
        "dr1/level2/2025W35_2A/l2b-v27-2026-231/1/level2_2025W35_2A_0233_1D1_spx_l2b-v27-2026-231.fits",
        "dr1/level2/2025W40_1A/l2b-v27-2026-239/1/level2_2025W40_1A_0353_1D1_spx_l2b-v27-2026-239.fits",
        "dr1/level2/2026W11_1A/l2b-v27-2026-232/1/level2_2026W11_1A_0444_1D1_spx_l2b-v27-2026-232.fits",
        "dr1/level2/2026W11_1A/l2b-v27-2026-232/1/level2_2026W11_1A_0430_2D1_spx_l2b-v27-2026-232.fits",
    ]),
]


def _angdist_deg(ra1, dec1, ra2, dec2) -> float:
    """İki koordinat arasındaki açısal mesafe (derece)."""
    r = math.pi / 180
    c1 = math.cos(dec1 * r); c2 = math.cos(dec2 * r)
    return math.degrees(math.acos(min(1.0, c1 * c2 * math.cos((ra1 - ra2) * r) + math.sin(dec1 * r) * math.sin(dec2 * r))))


async def _s3_list_prefixes(client: httpx.AsyncClient, prefix: str) -> list[str]:
    """S3 ListObjectsV2 ile delimiter='/' kullanarak alt prefix'leri listele."""
    prefixes = []
    token = None
    while True:
        params = {"list-type": "2", "prefix": prefix, "delimiter": "/", "max-keys": "500"}
        if token:
            params["continuation-token"] = token
        try:
            r = await client.get(S3_LIST_URL + "/", params=params, timeout=15)
            if r.status_code != 200:
                break
            root = ET.fromstring(r.text)
            for cp in root.findall(f"{{{S3_NS}}}CommonPrefixes"):
                p = cp.findtext(f"{{{S3_NS}}}Prefix")
                if p:
                    prefixes.append(p)
            is_trunc = root.findtext(f"{{{S3_NS}}}IsTruncated", "false").lower() == "true"
            if not is_trunc:
                break
            token = root.findtext(f"{{{S3_NS}}}NextContinuationToken")
        except Exception as e:
            log.warning("S3 prefix listesi hatası: %s", e)
            break
    return prefixes


async def _s3_list_keys(client: httpx.AsyncClient, prefix: str, max_keys: int = 20) -> list[str]:
    """Belirli bir prefix altındaki nesne anahtarlarını listele."""
    keys = []
    token = None
    while len(keys) < max_keys:
        params = {"list-type": "2", "prefix": prefix, "max-keys": str(min(max_keys - len(keys), 100))}
        if token:
            params["continuation-token"] = token
        try:
            r = await client.get(S3_LIST_URL + "/", params=params, timeout=15)
            if r.status_code != 200:
                break
            root = ET.fromstring(r.text)
            for obj in root.findall(f"{{{S3_NS}}}Contents"):
                k = obj.findtext(f"{{{S3_NS}}}Key")
                if k and k.endswith(".fits"):
                    keys.append(k)
            is_trunc = root.findtext(f"{{{S3_NS}}}IsTruncated", "false").lower() == "true"
            if not is_trunc:
                break
            token = root.findtext(f"{{{S3_NS}}}NextContinuationToken")
        except Exception as e:
            log.warning("S3 key listesi hatası: %s", e)
            break
    return keys


async def _fits_header_range(client: httpx.AsyncClient, s3_key: str, num_blocks: int = 20) -> Optional[bytes]:
    """FITS dosyasının ilk num_blocks×2880 baytını Range request ile çek.
    SPHEREx L2: WCS 2. HDU'da (~5760 byte), 20 blok = 57600 byte yeterli."""
    url = f"{S3_BASE}/{s3_key}"
    byte_end = num_blocks * 2880 - 1
    try:
        r = await client.get(url, headers={"Range": f"bytes=0-{byte_end}"}, timeout=20)
        if r.status_code in (200, 206):
            return r.content
    except Exception as e:
        log.debug("FITS header range hatası %s: %s", s3_key, e)
    return None


def _parse_fits_wcs_from_bytes(header_bytes: bytes) -> Optional[dict]:
    """
    Ham FITS baytlarından WCS bilgisini çöz.
    SPHEREx L2: CRVAL1/CRVAL2 ve NAXIS1/NAXIS2 farklı HDU'lara dağılmış.
    Tüm baytları HDU sınırlarını umursamadan tara ve ilk bulunan değerleri al.
    """
    if not header_bytes:
        return None
    try:
        cards: dict = {}
        target = {"CRVAL1","CRVAL2","NAXIS1","NAXIS2","CDELT1","CDELT2",
                  "CD1_1","CD2_2","PC1_1","PC2_2"}
        for i in range(0, len(header_bytes) - 79, 80):
            card = header_bytes[i:i+80].decode("ascii", errors="replace")
            if len(card) > 9 and card[8] == "=":
                key = card[:8].strip()
                if key in target and key not in cards:
                    val = card[9:].split("/")[0].strip().strip("'").strip()
                    try:
                        cards[key] = float(val)
                    except ValueError:
                        pass

        if "CRVAL1" not in cards or "CRVAL2" not in cards:
            return None

        # Gerçek piksel ölçeği: CDELT * PC diyagonal (SPHEREx L2 konvansiyonu)
        cdelt1 = abs(cards.get("CDELT1", 1.0))
        cdelt2 = abs(cards.get("CDELT2", 1.0))
        pc11   = abs(cards.get("PC1_1",  cards.get("CD1_1", 0.00167)))
        pc22   = abs(cards.get("PC2_2",  cards.get("CD2_2", 0.00167)))
        scale1 = cdelt1 * pc11 if cdelt1 != 1.0 or pc11 != 0.00167 else pc11
        scale2 = cdelt2 * pc22 if cdelt2 != 1.0 or pc22 != 0.00167 else pc22
        # cdelt=1.0 → ölçek doğrudan PC matrisinden gelir
        if cdelt1 == 1.0:
            scale1 = abs(cards.get("PC1_1", cards.get("CD1_1", 0.00167)))
        if cdelt2 == 1.0:
            scale2 = abs(cards.get("PC2_2", cards.get("CD2_2", 0.00167)))

        return {
            "ra":     float(cards["CRVAL1"]),
            "dec":    float(cards["CRVAL2"]),
            "naxis1": int(cards.get("NAXIS1", 2040)),
            "naxis2": int(cards.get("NAXIS2", 2040)),
            "cdelt1": scale1 if scale1 > 0 else 0.00167,
            "cdelt2": scale2 if scale2 > 0 else 0.00167,
        }
    except Exception as e:
        log.debug("WCS ayrıştırma hatası: %s", e)
        return None


def _coord_in_footprint(ra: float, dec: float, wcs: dict, margin: float = 1.5) -> bool:
    """Koordinatın FITS dosyasının footprint'i içinde olup olmadığını kontrol et."""
    ra_half  = wcs["naxis1"] * wcs["cdelt1"] / 2 * margin
    dec_half = wcs["naxis2"] * wcs["cdelt2"] / 2 * margin
    # RA wraparound
    dra = abs(ra - wcs["ra"])
    if dra > 180:
        dra = 360 - dra
    ddec = abs(dec - wcs["dec"])
    return dra <= ra_half and ddec <= dec_half


async def _build_s3_field_index():
    """S3'teki tüm week/field prefix'leri örnekleyerek spatial index oluştur."""
    global _S3_FIELD_INDEX, _S3_INDEX_READY
    async with _S3_INDEX_LOCK:
        if _S3_INDEX_READY:
            return
        log.info("S3 spatial index oluşturuluyor…")
        async with httpx.AsyncClient(timeout=20) as client:
            # Tüm week/field prefix'lerini listele
            field_prefixes = await _s3_list_prefixes(client, "dr1/level2/")
            log.info("Bulunan %d field prefix", len(field_prefixes))

            # Her prefix'ten tek bir dosya alıp header oku (paralel, max 30)
            sem = asyncio.Semaphore(8)

            async def _index_one(prefix):
                async with sem:
                    keys = await _s3_list_keys(client, prefix, max_keys=1)
                    if not keys:
                        return
                    hbytes = await _fits_header_range(client, keys[0], num_blocks=10)
                    wcs = _parse_fits_wcs_from_bytes(hbytes)
                    if wcs:
                        _S3_FIELD_INDEX[prefix] = wcs
                        log.debug("Index: %s → RA=%.2f Dec=%.2f", prefix, wcs["ra"], wcs["dec"])

            await asyncio.gather(*[_index_one(p) for p in field_prefixes[:60]])

        _S3_INDEX_READY = True
        log.info("S3 spatial index hazır — %d field", len(_S3_FIELD_INDEX))


async def _build_frames_from_keys(client: httpx.AsyncClient, keys: list[str], ra: float, dec: float) -> list[dict]:
    """Verilen S3 key listesinden frame dict'leri oluşturur (WCS + opsiyonel FITS kesit)."""
    frames = []
    for k in keys:
        hb = await _fits_header_range(client, k)
        wcs = _parse_fits_wcs_from_bytes(hb) or {}
        fname = k.split("/")[-1]
        parts = fname.replace("level2_", "").split("_")
        detector   = parts[3] if len(parts) > 3 else "?"
        week_field = f"{parts[0]}_{parts[1]}" if len(parts) > 1 else "?"

        frame = {
            "frame_id": f"s3_{len(frames)}",
            "pass_id": len(frames),
            "detector": detector,
            "cwave_um": 0.0,
            "utc_date": week_field,
            "target_x": 15, "target_y": 15,
            "raw_record": {
                "s3_key": k,
                "s3_https_url": f"{S3_BASE}/{k}",
                "measured_centroid": {
                    "ra_deg": wcs.get("ra", ra),
                    "dec_deg": wcs.get("dec", dec),
                    "x_cutout": 15, "y_cutout": 15,
                    "sigma_x_px": 0.5, "sigma_y_px": 0.5,
                },
                "image_mjy_sr": None,
                "provenance_type": "S3_DIRECT_L2",
            },
        }
        if ASTROPY_OK:
            try:
                full_r = await client.get(f"{S3_BASE}/{k}", timeout=90)
                if full_r.status_code == 200:
                    cutout = _extract_cutout(full_r.content, ra, dec)
                    if cutout:
                        frame["raw_record"].update(cutout)
                        frame["target_x"] = cutout.get("target_x", 15)
                        frame["target_y"] = cutout.get("target_y", 15)
                        frame["raw_record"]["provenance_type"] = "S3_DIRECT_L2_CUTOUT"
            except Exception as e:
                log.debug("S3 tam dosya hatası %s: %s", k, e)
        frames.append(frame)
    return frames


async def _query_s3_direct(ra: float, dec: float, radius_deg: float, max_frames: int) -> list[dict]:
    """
    IRSA TAP olmadan S3'ü doğrudan sorgula.
    Tüm 110 field prefix'ini paralel tara: her field'dan eşit aralıklı
    8 tile örnekle, WCS eşleşince o field'ı detaylı ara.
    """
    log.info("S3 doğrudan arama — ra=%.3f dec=%.3f", ra, dec)

    # --- Bilinen hedef key'lerini önce kontrol et ---
    for (tgt_ra, tgt_dec, s3_keys) in KNOWN_TARGET_KEYS:
        if _angdist_deg(ra, dec, tgt_ra, tgt_dec) < radius_deg + 0.5:
            log.info("Bilinen hedef eşleşti (%.2f,%.2f), %d key servis ediliyor", tgt_ra, tgt_dec, len(s3_keys))
            keys_to_use = s3_keys[:max_frames]
            async with httpx.AsyncClient(timeout=60) as client2:
                return await _build_frames_from_keys(client2, keys_to_use, ra, dec)

    async with httpx.AsyncClient(timeout=25) as client:
        all_prefixes = await _s3_list_prefixes(client, "dr1/level2/")
        if not all_prefixes:
            return []
        log.info("%d field prefix taranıyor", len(all_prefixes))

        matched_keys: list[str] = []
        sem = asyncio.Semaphore(10)

        async def _scan_prefix(prefix: str):
            async with sem:
                keys = await _s3_list_keys(client, prefix, max_keys=600)
                if not keys:
                    return
                # Eşit aralıklı 8 tile örnekle
                step = max(1, len(keys) // 8)
                sample = keys[::step][:8]
                hit = False
                for k in sample:
                    hb = await _fits_header_range(client, k)
                    wcs = _parse_fits_wcs_from_bytes(hb)
                    if wcs and _coord_in_footprint(ra, dec, wcs, margin=1.2):
                        hit = True
                        break
                if not hit:
                    return
                # Eşleşme var — tüm tile'ları ince tara
                log.info("Eşleşme: %s — tüm tile'lar taranıyor", prefix)
                for kk in keys:
                    if len(matched_keys) >= max_frames * 3:
                        return
                    h2 = await _fits_header_range(client, kk)
                    w2 = _parse_fits_wcs_from_bytes(h2)
                    if w2 and _coord_in_footprint(ra, dec, w2, margin=1.0):
                        if kk not in matched_keys:
                            matched_keys.append(kk)

        await asyncio.gather(*[_scan_prefix(p) for p in all_prefixes])
        log.info("S3 arama bitti: %d eşleşen tile", len(matched_keys))

        if not matched_keys:
            return []

        return await _build_frames_from_keys(client, matched_keys[:max_frames], ra, dec)

    return []


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
        # --- 2. IRSA down → S3 doğrudan erişim ---
        log.info("IRSA başarısız, S3 doğrudan erişim deneniyor…")
        s3_frames = await _query_s3_direct(ra, dec, radius_deg, max_frames)
        if s3_frames:
            return JSONResponse({
                "frames": s3_frames,
                "count": len(s3_frames),
                "source": "s3_direct",
                "message": f"IRSA down, S3'ten doğrudan {len(s3_frames)} kare bulundu.",
                "query": {"ra": ra, "dec": dec, "radius_arcmin": radius},
            })
        return JSONResponse({
            "frames": [],
            "count": 0,
            "irsa_status": "unavailable",
            "source": "cache_fallback",
            "message": "IRSA ve S3 araması sonuç vermedi. Önbellek verisi kullanılıyor.",
            "query": {"ra": ra, "dec": dec, "radius_arcmin": radius},
        })

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
