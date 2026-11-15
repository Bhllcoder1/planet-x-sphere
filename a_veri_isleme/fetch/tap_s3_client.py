"""
Alan A - Görev 01-10, 02-01, 02-02, 02-12: Sorgu Adımı (C.1), L1 Bayt-Ofset Haritası ve S3 Okuma (C.2)
Doğrulama durumu:
- URI'den S3 anahtarı türetme (`ibe/data/spherex/` önekini kaldırma): [V: PLAN_spherex_v3.md §1, s0_B §1]
- Tekilleştirme (obs_id, detector) çifti başına en yeni `l2b-v27-*` sürümünü tutma: [V: PLAN_spherex_v3.md §2.6]
- HDU tamsayı indeksleri: IMAGE=1, FLAGS=2, VARIANCE=3, ZODI=4, EPSF=5, WCS-WAVE=6 [V: s0_B]
- Birleştirilmiş satır aralığı (coalesced row-span) hesabı (satır adımı 8160 bayt, 2040 float32 piksel): [V: s0_B]
"""

from __future__ import annotations
from dataclasses import dataclass
import json
import os
import re
from typing import Dict, Iterable, List, Optional, Tuple

S3_BUCKET = "nasa-irsa-spherex"
IBE_PREFIX = "ibe/data/spherex/"
DETECTOR_SIZE_PX = 2040
BYTES_PER_FLOAT32 = 4
ROW_STRIDE_BYTES = DETECTOR_SIZE_PX * BYTES_PER_FLOAT32  # 8160 B [V: PLAN_spherex_v3.md §2.4]

HDU_INDICES: Dict[str, int] = {
    "PRIMARY": 0,
    "IMAGE": 1,
    "FLAGS": 2,
    "VARIANCE": 3,
    "ZODI": 4,
    "EPSF": 5,
    "WCS-WAVE": 6,
}


def uri_to_s3_key(uri: str) -> str:
    """
    Görev 02-01 (C.1): IRSA TAP `uri` sütunundan S3 nesne anahtarını türetir.
    `cloud_access` sütunu mevcut olmadığı için `uri` içindeki `ibe/data/spherex/`
    öneki kaldırılır [V: PLAN_spherex_v3.md §1].
    """
    cleaned = uri.strip().lstrip("/")
    if cleaned.startswith(IBE_PREFIX):
        return cleaned[len(IBE_PREFIX):]
    idx = cleaned.find(IBE_PREFIX)
    if idx != -1:
        return cleaned[idx + len(IBE_PREFIX):]
    return cleaned


def extract_detector_from_uri(uri: str) -> Optional[int]:
    """
    TAP tablosunda ayrı bir `detector` sütunu yoktur; dedektör numarası (1..6)
    URI dizininden veya dosya adındaki `D1..D6` deseninden çıkarılır [V: s0_A.md].
    """
    m = re.search(r"D([1-6])_spx", uri)
    if m:
        return int(m.group(1))
    m2 = re.search(r"/([1-6])/level2_", uri)
    if m2:
        return int(m2.group(1))
    return None


def extract_procver_tag(uri: str) -> str:
    """URI içinden `l2b-v27-2026-xxx` işleme sürümü etiketini çıkarır."""
    m = re.search(r"(l2b(?:_retry)?-v\d+-\d{4}-\d+)", uri)
    return m.group(1) if m else ""


def deduplicate_tap_rows(rows: Iterable[Dict[str, object]]) -> List[Dict[str, object]]:
    """
    Görev 02-01 (C.1): Aynı `(obs_id, detector)` çifti için birden fazla satır varsa
    en yeni `l2b-v27-*` işleme etiketine sahip olanı tutar; DR1 ve QR3 birlikte
    kullanılabilir (ikisi de provenance 7.0.5) [V: PLAN_spherex_v3.md §2.6].
    """
    best_by_key: Dict[Tuple[str, int], Dict[str, object]] = {}
    for row in rows:
        uri = str(row.get("uri", ""))
        obs_id = str(row.get("obs_id") or row.get("obsid") or uri)
        det = row.get("detector")
        det_int = int(det) if det is not None else (extract_detector_from_uri(uri) or 0)
        procver = str(row.get("procver") or extract_procver_tag(uri))

        key = (obs_id, det_int)
        enriched = dict(row)
        enriched["s3_key"] = uri_to_s3_key(uri)
        enriched["detector"] = det_int
        enriched["procver"] = procver

        prev = best_by_key.get(key)
        if prev is None or str(enriched["procver"]) >= str(prev.get("procver", "")):
            best_by_key[key] = enriched

    return list(best_by_key.values())


@dataclass(frozen=True)
class HduByteOffset:
    hdu_index: int
    hdu_name: str
    header_start: int
    data_start: int
    data_length: int


def compute_row_span_byte_range(
    data_start_offset: int,
    y0: int,
    y1: int,
    row_stride_bytes: int = ROW_STRIDE_BYTES,
    detector_height: int = DETECTOR_SIZE_PX,
) -> Tuple[int, int]:
    """
    Görev 01-10, 02-02 & 02-12 (C.2): IMAGE / VARIANCE / ZODI (sıkıştırılmamış float32)
    HDU'ları için `[y0, y1)` satır aralığını tek bir HTTP/S3 Range GET ile okumak üzere
    `(start_byte, end_byte_inclusive)` aralığını hesaplar [V: PLAN_spherex_v3.md §2.4].
    """
    y_start = max(0, min(detector_height, int(y0)))
    y_end = max(y_start, min(detector_height, int(y1)))
    if y_end <= y_start:
        raise ValueError(f"Geçersiz satır aralığı: y0={y0}, y1={y1}")

    start_byte = int(data_start_offset) + y_start * int(row_stride_bytes)
    end_byte_inclusive = int(data_start_offset) + y_end * int(row_stride_bytes) - 1
    return start_byte, end_byte_inclusive


def build_l1_cache_key(s3_key: str) -> str:
    """Görev 02-12: S3 anahtarından güvenli L1 önbellek dosya anahtarı üretir."""
    base = s3_key.strip().replace("/", "__")
    if base.endswith(".fits"):
        base = base[:-5]
    return base
