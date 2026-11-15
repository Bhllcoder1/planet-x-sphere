"""
frame_products.py — Kare başına ürün dosyaları yazma ve okuma modülü (Görev 02-10).

Sözleşme:
- cache/{release}/{pipever}/{fieldkey}/{frame_id}/
    ├── img.f32   (float32, little-endian, C-order, hedef penceresi)
    ├── var.f32   (float32, little-endian, C-order)
    ├── flg.u32   (uint32, little-endian, C-order)
    ├── cat.json  (tespit kataloğu; x, y float koordinatları yuvarlanmaz)
    ├── geom.json (ham WCS, T dönüşümü, roll, N/R parametreleri)
    └── meta.json (MJD-AVG, dedektör, dalgaboyu, bayraklar)

Tüm yazımlar atomiktir (geçici dosya + os.replace).
[V: PLAN_v2 C.11, s0_B §4]
"""
from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np


@dataclass
class CatalogSource:
    """Tekil tespit kaynağı (cat.json içindeki eleman)."""
    x: float
    y: float
    sigma_x: float
    sigma_y: float
    rho: float
    flux: float
    snr: float
    flags: int
    gaia_id: Optional[str] = None
    residual: Optional[float] = None
    reject_reason: Optional[str] = None
    saturated_core: bool = False


@dataclass
class FrameProductSet:
    """Bir kareye ait ürün seti."""
    img: np.ndarray          # float32 (H, W)
    var: np.ndarray          # float32 (H, W)
    flg: np.ndarray          # uint32 (H, W)
    catalog: List[Dict[str, Any]]
    geom: Dict[str, Any]
    meta: Dict[str, Any]


def get_product_dir(
    base_dir: Path | str,
    release: str,
    pipever: str,
    fieldkey: str,
    frame_id: str
) -> Path:
    """Ürün dosyalarının hedef dizin yolunu döndürür."""
    return Path(base_dir) / release / pipever / fieldkey / frame_id


def write_frame_products(
    base_dir: Path | str,
    release: str,
    pipever: str,
    fieldkey: str,
    frame_id: str,
    products: FrameProductSet,
) -> Dict[str, str]:
    """
    Ürün setini belirtilen önbellek yoluna atomik olarak yazar.

    Diziler küçük-endian (little-endian) olarak yazılır:
    - img.f32: '<f4'
    - var.f32: '<f4'
    - flg.u32: '<u4'

    Returns:
        Üretilen dosyaların göreli yolları sözlüğü.
    """
    target_dir = get_product_dir(base_dir, release, pipever, fieldkey, frame_id)
    target_dir.mkdir(parents=True, exist_ok=True)

    rel_base = f"cache/{release}/{pipever}/{fieldkey}/{frame_id}"
    out_paths: Dict[str, str] = {}

    def _write_atomic_binary(filename: str, array: np.ndarray, dtype_str: str) -> Path:
        arr_conv = np.ascontiguousarray(array.astype(dtype_str))
        final_path = target_dir / filename
        tmp_path = target_dir / f"{filename}.tmp_{os.getpid()}"
        with open(tmp_path, "wb") as f:
            f.write(arr_conv.tobytes())
        os.replace(tmp_path, final_path)
        return final_path

    def _write_atomic_json(filename: str, data: Any) -> Path:
        final_path = target_dir / filename
        tmp_path = target_dir / f"{filename}.tmp_{os.getpid()}"
        # float konumların tam hassasiyetle korunması için varsayılan json.dumps kullanılır
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp_path, final_path)
        return final_path

    # 1. Binary arrayler (little-endian)
    _write_atomic_binary("img.f32", products.img, "<f4")
    out_paths["img"] = f"{rel_base}/img.f32"

    _write_atomic_binary("var.f32", products.var, "<f4")
    out_paths["var"] = f"{rel_base}/var.f32"

    _write_atomic_binary("flg.u32", products.flg, "<u4")
    out_paths["flg"] = f"{rel_base}/flg.u32"

    # 2. JSON meta dosyaları
    _write_atomic_json("cat.json", products.catalog)
    out_paths["cat"] = f"{rel_base}/cat.json"

    _write_atomic_json("geom.json", products.geom)
    out_paths["geom"] = f"{rel_base}/geom.json"

    _write_atomic_json("meta.json", products.meta)
    out_paths["meta"] = f"{rel_base}/meta.json"

    return out_paths


def read_frame_products(
    base_dir: Path | str,
    release: str,
    pipever: str,
    fieldkey: str,
    frame_id: str,
    shape: Tuple[int, int] = (64, 64),
) -> FrameProductSet:
    """
    Yazılmış ürün dosyalarını diskten okur ve doğrular.
    """
    target_dir = get_product_dir(base_dir, release, pipever, fieldkey, frame_id)

    # 1. Binary okuma
    with open(target_dir / "img.f32", "rb") as f:
        img = np.frombuffer(f.read(), dtype="<f4").reshape(shape)

    with open(target_dir / "var.f32", "rb") as f:
        var = np.frombuffer(f.read(), dtype="<f4").reshape(shape)

    with open(target_dir / "flg.u32", "rb") as f:
        flg = np.frombuffer(f.read(), dtype="<u4").reshape(shape)

    # 2. JSON okuma
    with open(target_dir / "cat.json", "r", encoding="utf-8") as f:
        catalog = json.load(f)

    with open(target_dir / "geom.json", "r", encoding="utf-8") as f:
        geom = json.load(f)

    with open(target_dir / "meta.json", "r", encoding="utf-8") as f:
        meta = json.load(f)

    return FrameProductSet(
        img=img,
        var=var,
        flg=flg,
        catalog=catalog,
        geom=geom,
        meta=meta,
    )


def estimate_barnard_storage(
    n_frames: int = 358,
    window_shape: Tuple[int, int] = (64, 64),
    avg_cat_sources: int = 15,
) -> Dict[str, Any]:
    """
    Barnard'ın Yıldızı 358 kare için toplam disk alanı tahminini hesaplar [V: 02-10 kabul].
    """
    h, w = window_shape
    px = h * w
    img_bytes = px * 4
    var_bytes = px * 4
    flg_bytes = px * 4
    # cat ~ 1.5 KB, geom ~ 1.0 KB, meta ~ 0.5 KB
    json_bytes = avg_cat_sources * 100 + 1500
    per_frame_bytes = img_bytes + var_bytes + flg_bytes + json_bytes
    total_bytes = per_frame_bytes * n_frames

    return {
        "n_frames": n_frames,
        "window_shape": f"{h}x{w}",
        "per_frame_kb": round(per_frame_bytes / 1024, 2),
        "total_mb": round(total_bytes / (1024 * 1024), 2),
        "breakdown": {
            "img.f32_total_kb": round((img_bytes * n_frames) / 1024, 2),
            "var.f32_total_kb": round((var_bytes * n_frames) / 1024, 2),
            "flg.u32_total_kb": round((flg_bytes * n_frames) / 1024, 2),
            "json_total_kb": round((json_bytes * n_frames) / 1024, 2),
        }
    }
