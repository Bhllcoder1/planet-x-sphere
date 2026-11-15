"""
test_shift_stack_demo.py — Shift-and-stack CPU benchmark testleri (Görev 04-14).
"""
import pytest
import numpy as np

from c_sunucu.ops.shift_stack_demo import (
    _uret_sentetik_kareler,
    _cpu_shift_and_stack,
    snr_kazanim_tahmini,
    shift_and_stack_cpu_benchmark,
    GPU_TRIGGER_THRESHOLD_S,
)


def test_uret_sentetik_kareler():
    """Sentetik kareler doğru boyutta ve float32 türünde üretilir."""
    kareler = _uret_sentetik_kareler(5, yukseklik=32, genislik=32, seed=42)
    assert len(kareler) == 5
    for k in kareler:
        assert k.shape == (32, 32)
        assert k.dtype == np.float32


def test_cpu_shift_and_stack():
    """Medyan yığma doğru boyut ve değer üretir."""
    # 3 adet sabit değerli matris
    f1 = np.ones((16, 16), dtype=np.float32) * 1.0
    f2 = np.ones((16, 16), dtype=np.float32) * 2.0
    f3 = np.ones((16, 16), dtype=np.float32) * 10.0
    
    yigim = _cpu_shift_and_stack([f1, f2, f3])
    assert yigim.shape == (16, 16)
    assert yigim.dtype == np.float32
    # [1, 2, 10] medyanı 2.0'dır
    assert np.allclose(yigim, 2.0)


def test_cpu_shift_and_stack_empty_error():
    """Boş liste verilince ValueError yükseltir."""
    with pytest.raises(ValueError, match="boş olamaz"):
        _cpu_shift_and_stack([])


def test_snr_kazanim_tahmini():
    """SNR kazanım hesabı sqrt(N) * single_snr formülüne uyar."""
    # N=100 -> sqrt(100) = 10, single_snr=1.5 -> stack_snr=15.0
    sonuc = snr_kazanim_tahmini(100, single_snr=1.5, threshold=5.0)
    assert pytest.approx(sonuc["gain_factor"]) == 10.0
    assert pytest.approx(sonuc["stack_snr"]) == 15.0
    assert sonuc["gpu_unnecessary"] is False

    # single_snr > 5.0 ise gpu_unnecessary True olmalı
    sonuc_yuksek = snr_kazanim_tahmini(100, single_snr=6.0, threshold=5.0)
    assert sonuc_yuksek["gpu_unnecessary"] is True


def test_shift_and_stack_cpu_benchmark():
    """Benchmark p50, p95 ve trigger_gpu alanlarını doğru döner."""
    res = shift_and_stack_cpu_benchmark(
        n_frames=5,
        n_runs=3,
        frame_height=32,
        frame_width=32,
        seed=42,
        single_snr=1.5,
    )
    assert "p50_s" in res
    assert "p95_s" in res
    assert "trigger_gpu" in res
    assert res["n_frames"] == 5
    assert res["n_runs"] == 3
    assert len(res["times_s"]) == 3
    assert res["p50_s"] > 0.0
    assert res["p95_s"] >= res["p50_s"]
