"""
test_d9_simulate.py — D9 simülasyon modülü birim testleri (Görev 01-06).
"""
import json
import pathlib
import tempfile
import pytest

from c_sunucu.ops.d9_simulate import simulate_d9, _write_simulated_json
from c_sunucu.ops.d9_test import D9Result


def test_simulate_d9_basic():
    """simulate_d9 temel parametrelerle doğru D9Result ve JSON dosyası üretir."""
    with tempfile.TemporaryDirectory() as tmpdir:
        out_dir = pathlib.Path(tmpdir)
        result, json_path = simulate_d9(n=20, seed=42, target="barnard", out_dir=out_dir)

        assert isinstance(result, D9Result)
        assert result.n == 20
        assert result.target == "barnard"
        assert len(result.times) == 20
        assert result.p50 > 0.0
        assert result.p95 >= result.p50
        assert result.p_min <= result.p50 <= result.p_max
        assert result.gpu_trigger is True  # Ankara profili p50 ~ 3.9s > 2.0s
        assert "sim" in result.hostname

        # JSON çıktısını doğrula
        assert json_path.exists()
        data = json.loads(json_path.read_text(encoding="utf-8"))
        assert data["simulated"] is True
        assert data["sim_profile"] == "ankara_reference"
        assert data["n"] == 20
        assert data["target"] == "barnard"
        assert len(data["times"]) == 20
        assert data["gpu_trigger"] is True


def test_simulate_d9_reproducibility():
    """Aynı seed ile çalıştırılan simülasyon özdeş sonuçlar üretir."""
    with tempfile.TemporaryDirectory() as tmpdir:
        out_dir = pathlib.Path(tmpdir)
        r1, _ = simulate_d9(n=15, seed=123, out_dir=out_dir)
        r2, _ = simulate_d9(n=15, seed=123, out_dir=out_dir)

        assert r1.p50 == r2.p50
        assert r1.p95 == r2.p95
        assert r1.times == r2.times


def test_simulate_d9_frame_keys():
    """Üretilen test kare anahtarları doğru formatta ve n adettir."""
    with tempfile.TemporaryDirectory() as tmpdir:
        out_dir = pathlib.Path(tmpdir)
        result, _ = simulate_d9(n=10, seed=99, out_dir=out_dir)

        assert len(result.frames_tested) == 10
        for key in result.frames_tested:
            assert "level2" in key
            assert key.endswith(".fits")
