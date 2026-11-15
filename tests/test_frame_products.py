"""
test_frame_products.py — Kare ürün dosyaları yazma, okuma, belirlenimlilik ve boyut testleri (Görev 02-10).
"""
import hashlib
import json
import sys
from pathlib import Path
import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT / "c_sunucu") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "c_sunucu"))

from cache.frame_products import (
    FrameProductSet,
    estimate_barnard_storage,
    read_frame_products,
    write_frame_products,
)


@pytest.fixture
def sample_products():
    shape = (64, 64)
    np.random.seed(42)
    img = np.random.randn(*shape).astype(np.float32)
    var = np.abs(np.random.randn(*shape)).astype(np.float32)
    flg = np.random.randint(0, 1000, size=shape, dtype=np.uint32)

    cat = [
        {
            "x": 4.47123456789,
            "y": 18.987654321,
            "sigma_x": 0.05,
            "sigma_y": 0.04,
            "rho": 0.01,
            "flux": 1250.75,
            "snr": 34.2,
            "flags": 0,
            "gaia_id": "Gaia DR3 44728321305274",
            "residual": 0.02,
            "reject_reason": None,
            "saturated_core": False,
        }
    ]
    geom = {
        "crpix1": 32.5,
        "crpix2": 32.5,
        "cd1_1": -0.0017,
        "cd1_2": 0.0,
        "cd2_1": 0.0,
        "cd2_2": 0.0017,
        "roll_deg": 180.25,
        "shift_px": [0.03, -0.02],
    }
    meta = {
        "mjd_avg": 60911.49,
        "detector": "D2",
        "sps_epa": 180.0,
        "wavelength_um": 1.42,
        "stray_light_suspect": False,
        "mask_fraction": 0.012,
        "unusable_for_astrometry": False,
    }
    return FrameProductSet(img=img, var=var, flg=flg, catalog=cat, geom=geom, meta=meta)


def test_write_and_read_roundtrip(tmp_path, sample_products):
    """Yazılan ürünlerin diskten birebir aynı değerlerle geri okunduğunu doğrular."""
    paths = write_frame_products(
        base_dir=tmp_path,
        release="dr1",
        pipever="l2b-v27",
        fieldkey="barnard",
        frame_id="frame_001",
        products=sample_products,
    )

    assert "img" in paths
    assert "var" in paths
    assert "flg" in paths
    assert "cat" in paths
    assert "geom" in paths
    assert "meta" in paths

    read_back = read_frame_products(
        base_dir=tmp_path,
        release="dr1",
        pipever="l2b-v27",
        fieldkey="barnard",
        frame_id="frame_001",
        shape=(64, 64),
    )

    np.testing.assert_array_equal(read_back.img, sample_products.img)
    np.testing.assert_array_equal(read_back.var, sample_products.var)
    np.testing.assert_array_equal(read_back.flg, sample_products.flg)
    assert read_back.catalog == sample_products.catalog
    assert read_back.geom == sample_products.geom
    assert read_back.meta == sample_products.meta


def test_determinism_bit_for_bit(tmp_path, sample_products):
    """Aynı kare iki kez işlenince dosyalar bit bit aynı olmalıdır [V: 02-10 kabul]."""
    dir1 = tmp_path / "run1"
    dir2 = tmp_path / "run2"

    write_frame_products(dir1, "dr1", "v1", "test", "f1", sample_products)
    write_frame_products(dir2, "dr1", "v1", "test", "f1", sample_products)

    for fname in ["img.f32", "var.f32", "flg.u32", "cat.json", "geom.json", "meta.json"]:
        p1 = dir1 / "dr1" / "v1" / "test" / "f1" / fname
        p2 = dir2 / "dr1" / "v1" / "test" / "f1" / fname
        assert p1.exists() and p2.exists()
        h1 = hashlib.sha256(p1.read_bytes()).hexdigest()
        h2 = hashlib.sha256(p2.read_bytes()).hexdigest()
        assert h1 == h2, f"Dosya {fname} belirlenimli değil!"


def test_float_positions_not_rounded(tmp_path, sample_products):
    """cat.json içindeki float koordinatların yuvarlanmadan tam hassasiyetle saklandığını doğrular."""
    write_frame_products(tmp_path, "dr1", "v1", "test", "f1", sample_products)
    cat_file = tmp_path / "dr1" / "v1" / "test" / "f1" / "cat.json"
    with open(cat_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data[0]["x"] == 4.47123456789
    assert data[0]["y"] == 18.987654321


def test_little_endian_storage(tmp_path, sample_products):
    """Binary dosyaların little-endian formatında yazıldığını doğrular."""
    write_frame_products(tmp_path, "dr1", "v1", "test", "f1", sample_products)
    img_file = tmp_path / "dr1" / "v1" / "test" / "f1" / "img.f32"
    raw_bytes = img_file.read_bytes()
    val_from_le = np.frombuffer(raw_bytes[:4], dtype="<f4")[0]
    expected_first = sample_products.img.ravel()[0]
    assert np.isclose(val_from_le, expected_first)


def test_barnard_storage_estimate():
    """Barnard 358 kare için depolama boyutunu raporlar."""
    est = estimate_barnard_storage(n_frames=358, window_shape=(64, 64))
    assert est["n_frames"] == 358
    assert est["total_mb"] > 0
    # 64x64 pencere: ~50 KB per frame * 358 ~ 18-20 MB
    assert 10.0 <= est["total_mb"] <= 30.0
