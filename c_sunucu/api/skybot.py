"""
skybot.py — IMCCE SkyBoT etiketleme modülü (Görev 04-09).

SPHEREx karelerindeki tespit edilen aday izleri IMCCE SkyBoT servisiyle
çapraz eşler (-objFilter=100 formatı).

Kurallar:
- Sorgu URL: https://ssp.imcce.fr/webservices/skybot/api/conesearch.php
- Parametreler: -ep={JD}&-ra={ra}&-dec={dec}&-rs={radius}&-mime=json&-output=all&-observer=500&-filter=0&-objFilter=100&-refsys=EQJ2000
- JD = MJD_AVG + 2400000.5
- -objFilter=100: yalnız asteroitler (110 sunucu hatası vermektedir [V: s0_D §3]).
- Eşleme yarıçapı: max(3 piksel * 6.2 arcsec/px, 3 * sigma_ephemeris) [V: PLAN_v3 §2.1].
- SkyBoT erişilemezse veya zaman aşımına uğrarsa: 'untagged' etiketi verilir; işlem ASLA engellenmez [V: PLAN_v2 §C.13].
"""
from __future__ import annotations

import json
import logging
import math
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

SKYBOT_API_URL = "https://ssp.imcce.fr/webservices/skybot/api/conesearch.php"
SPHEREX_PIXEL_SCALE_ARCSEC = 6.2  # arcsec/piksel
MIN_MATCH_RADIUS_PIXELS = 3.0     # 3 piksel


def mjd_to_jd(mjd: float) -> float:
    """Modified Julian Date'i Julian Date'e dönüştürür."""
    return mjd + 2400000.5


def parse_skybot_ra(ra_str: str) -> float:
    """'12 34 56.78' hms formatındaki RA dizesini dereceye dönüştürür."""
    parts = ra_str.strip().split()
    if len(parts) != 3:
        return float(ra_str)
    h, m, s = float(parts[0]), float(parts[1]), float(parts[2])
    return (h + m / 60.0 + s / 3600.0) * 15.0


def parse_skybot_dec(dec_str: str) -> float:
    """'+12 34 56.7' veya '-12 34 56.7' dms formatındaki Dec dizesini dereceye dönüştürür."""
    s = dec_str.strip()
    sign = -1.0 if s.startswith("-") else 1.0
    s_clean = s.lstrip("+-")
    parts = s_clean.split()
    if len(parts) != 3:
        return float(dec_str)
    d, m, sec = float(parts[0]), float(parts[1]), float(parts[2])
    return sign * (d + m / 60.0 + sec / 3600.0)


def angular_distance_arcsec(ra1: float, dec1: float, ra2: float, dec2: float) -> float:
    """İki (RA, Dec) gökyüzü koordinatı arasındaki açısal mesafeyi yay-saniyesi olarak hesaplar."""
    r1, d1 = math.radians(ra1), math.radians(dec1)
    r2, d2 = math.radians(ra2), math.radians(dec2)
    # Haversine
    dlat = d2 - d1
    dlon = r2 - r1
    a = math.sin(dlat / 2.0) ** 2 + math.cos(d1) * math.cos(d2) * math.sin(dlon / 2.0) ** 2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return math.degrees(c) * 3600.0


def query_skybot_conesearch(
    ra_deg: float,
    dec_deg: float,
    epoch_mjd: float,
    radius_arcsec: float = 10800.0,
    timeout_sec: float = 8.0,
) -> Optional[List[Dict[str, Any]]]:
    """
    IMCCE SkyBoT conesearch API'sini -objFilter=100 parametresiyle sorgular.

    Returns:
        Asteroit listesi veya ağ/zaman aşımı durumunda None.
    """
    jd = mjd_to_jd(epoch_mjd)
    params = {
        "-ep": f"{jd:.6f}",
        "-ra": f"{ra_deg:.6f}",
        "-dec": f"{dec_deg:.6f}",
        "-rs": f"{radius_arcsec:.1f}",
        "-mime": "json",
        "-output": "all",
        "-observer": "500",
        "-filter": "0",
        "-objFilter": "100",  # Yalnız asteroitler
        "-refsys": "EQJ2000",
        "-from": "Antigravity_planet_x_sphere",
    }
    url = f"{SKYBOT_API_URL}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "SPHEREx-Viewer-Pipeline/0.1"})

    try:
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("data", [])
    except Exception as exc:
        logger.warning("SkyBoT sorgusu başarısız (%s); 'untagged' etiketi verilecek.", exc)
        return None


def tag_candidates(
    candidates: List[Dict[str, Any]],
    skybot_data: Optional[List[Dict[str, Any]]],
    pixel_scale_arcsec: float = SPHEREX_PIXEL_SCALE_ARCSEC,
) -> List[Dict[str, Any]]:
    """
    Aday tespit listesini SkyBoT asteroit verisiyle eşleştirir ve etiketler.

    Her adaya şu alanlar eklenir:
    - 'skybot_tag': 'olası: {ad}' | 'aday' | 'untagged'
    - 'skybot_matched': bool
    - 'skybot_distance_arcsec': Optional[float]
    - 'skybot_object_name': Optional[str]
    - 'skybot_vmag': Optional[float]
    """
    tagged = []

    # SkyBoT servisi erişilemediyse
    if skybot_data is None:
        for c in candidates:
            item = dict(c)
            item["skybot_tag"] = "untagged"
            item["skybot_matched"] = False
            item["skybot_distance_arcsec"] = None
            item["skybot_object_name"] = None
            item["skybot_vmag"] = None
            tagged.append(item)
        return tagged

    # SkyBoT objelerini ayrıştır
    parsed_objects = []
    for obj in skybot_data:
        try:
            name = str(obj.get("Name", "Bilinmeyen"))
            ra_s = str(obj.get("RA (hms)", ""))
            dec_s = str(obj.get("DEC (dms)", ""))
            vmag = float(obj.get("VMag", 99.0))
            err_arcsec = float(obj.get("Err", 0.05))
            ra_d = parse_skybot_ra(ra_s) if ra_s else float(obj.get("RA", 0.0))
            dec_d = parse_skybot_dec(dec_s) if dec_s else float(obj.get("DEC", 0.0))
            parsed_objects.append({
                "name": name,
                "ra": ra_d,
                "dec": dec_d,
                "vmag": vmag,
                "err_arcsec": err_arcsec,
            })
        except Exception as e:
            logger.debug("SkyBoT satırı ayrıştırılamadı: %s", e)

    min_match_dist_arcsec = MIN_MATCH_RADIUS_PIXELS * pixel_scale_arcsec  # 3 px * 6.2 = 18.6"

    for c in candidates:
        item = dict(c)
        c_ra = float(item.get("ra", 0.0))
        c_dec = float(item.get("dec", 0.0))

        best_match = None
        best_dist = float("inf")

        for obj in parsed_objects:
            dist = angular_distance_arcsec(c_ra, c_dec, obj["ra"], obj["dec"])
            match_radius = max(min_match_dist_arcsec, 3.0 * obj["err_arcsec"])
            if dist <= match_radius and dist < best_dist:
                best_dist = dist
                best_match = obj

        if best_match is not None:
            item["skybot_tag"] = f"olası: {best_match['name']}"
            item["skybot_matched"] = True
            item["skybot_distance_arcsec"] = round(best_dist, 3)
            item["skybot_object_name"] = best_match["name"]
            item["skybot_vmag"] = best_match["vmag"]
        else:
            item["skybot_tag"] = "aday"
            item["skybot_matched"] = False
            item["skybot_distance_arcsec"] = None
            item["skybot_object_name"] = None
            item["skybot_vmag"] = None

        tagged.append(item)

    return tagged
