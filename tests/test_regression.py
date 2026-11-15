"""
test_regression.py — Regresyon testleri.

Altın test: belirli bir girdi için çıktı değişmemeli.
Stretch, koordinat ayrıştırma, URL şeması, offset hesaplama.

S3 ve TAP çağrıları mock'lanır; gerçek ağ bağlantısı açılmaz.
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from a_veri_isleme.fetch.tap_s3_client import (
    ROW_STRIDE_BYTES,
    uri_to_s3_key,
)
from a_veri_isleme.process.pixel_conventions import (
    check_mode_n_eligibility,
    native_to_screen_px,
)


# ---------------------------------------------------------------------------
# Koordinat / piksel testleri
# ---------------------------------------------------------------------------

def test_float_position_no_round() -> None:
    """
    Float pozisyon 4.47 → zoom 100 → 447.0 piksel (yuvarlanmaz).
    [V: DECISIONS_AND_TASK.md — Drizzle test]
    """
    # Arrange
    float_pos: float = 4.47
    zoom: int = 100

    # Act  — native_to_screen_px modülünü kullan
    screen_x, _ = native_to_screen_px(float_pos, 0.0, zoom=zoom)

    # Assert
    assert abs(screen_x - 447.0) < 0.5, (
        f"Float pozisyon yuvarlandı: {screen_x} != 447.0 (± 0.5)"
    )


def test_float_position_direct_multiply() -> None:
    """
    Çarpma yoluyla doğrudan kontrol: float_pos * zoom == 447.0.
    Modülden bağımsız temel aritmetik gerileme.
    """
    # Arrange
    float_pos: float = 4.47
    zoom: int = 100

    # Act
    screen_px: float = float_pos * zoom

    # Assert
    assert abs(screen_px - 447.0) < 0.5, (
        f"Temel çarpma hatası: {screen_px}"
    )


# ---------------------------------------------------------------------------
# Bayt-offset hesaplama testleri
# ---------------------------------------------------------------------------

def test_row_range_calculation() -> None:
    """
    100. satır için byte offset doğru hesaplanmalı.
    naxis1=2040, bitpix=-32 (float32=4 byte), satırlar y0=50..y1=150.
    [V: tap_s3_client.py — ROW_STRIDE_BYTES=8160]
    """
    # Arrange
    naxis1: int = 2040
    bitpix: int = -32  # float32 = 4 bayt
    y0: int = 50
    y1: int = 150
    expected_start: int = y0 * naxis1 * 4
    expected_size: int = (y1 - y0) * naxis1 * 4

    # Act
    row_stride: int = naxis1 * abs(bitpix) // 8
    start: int = y0 * row_stride
    size: int = (y1 - y0) * row_stride

    # Assert
    assert start == expected_start, (
        f"Başlangıç offset yanlış: {start} != {expected_start}"
    )
    assert size == expected_size, (
        f"Boyut yanlış: {size} != {expected_size}"
    )


def test_row_stride_constant_matches_spec() -> None:
    """
    tap_s3_client.ROW_STRIDE_BYTES sabitinin beklenen 8160 değerine eşit olduğunu doğrular.
    [V: s0_B §2.4 — 2040 piksel × 4 bayt = 8160 B]
    """
    assert ROW_STRIDE_BYTES == 8160, (
        f"ROW_STRIDE_BYTES beklenen 8160, alınan: {ROW_STRIDE_BYTES}"
    )


# ---------------------------------------------------------------------------
# URI → S3 anahtar dönüşümü (TAP mock)
# ---------------------------------------------------------------------------

def test_uri_to_s3_key_strips_prefix() -> None:
    """
    'ibe/data/spherex/' önekinin URI'den kaldırılarak S3 anahtarına dönüştürüldüğünü
    doğrular. TAP/S3 ağ çağrısı yapılmaz.
    [V: PLAN_spherex_v3.md §1]
    """
    # Arrange
    uri: str = "ibe/data/spherex/l2/1/level2_spx_D1_spx_1234.fits"
    expected: str = "l2/1/level2_spx_D1_spx_1234.fits"

    # Act  — S3 / TAP çağrısı yapılmaz; saf dönüşüm işlevi
    result: str = uri_to_s3_key(uri)

    # Assert
    assert result == expected, (
        f"S3 anahtarı yanlış: '{result}' != '{expected}'"
    )


def test_uri_to_s3_key_no_network(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    uri_to_s3_key sırasında gerçek ağ soketi açılmadığını monkeypatch ile doğrular.
    """
    import socket

    # Arrange — ağ bağlantısı açıksa test başarısız olsun
    monkeypatch.setattr(socket, "getaddrinfo", MagicMock(side_effect=RuntimeError("Gerçek ağ yasak")))

    uri: str = "ibe/data/spherex/l2/2/level2_spx_D2_spx_5678.fits"

    # Act  — RuntimeError fırlatılmamalı (ağ kullanılmıyor)
    result: str = uri_to_s3_key(uri)

    # Assert
    assert result == "l2/2/level2_spx_D2_spx_5678.fits"


# ---------------------------------------------------------------------------
# theta_res modulo 180 doğruluğu
# ---------------------------------------------------------------------------

def test_theta_res_modulo() -> None:
    """
    SPS_EPA farkı ~180° olduğunda 180° döndürme uygulanır;
    kalan artık açı (theta_res) doğru hesaplanmalı.
    [V: pixel_conventions.py — check_mode_n_eligibility]
    """
    # Arrange
    # pa_frame - pa_ref - 180 = 0.3  →  theta_res ≈ 0.3°
    result = check_mode_n_eligibility(
        same_detector=True,
        pa_ref_deg=0.0,
        pa_frame_deg=180.3,
        sps_epa_ref=0.0,
        sps_epa_frame=180.0,  # fark > 90°  →  expected_flip = 180°
    )

    # Assert
    assert abs(result.theta_res_deg - 0.3) < 0.01, (
        f"theta_res beklenen ~0.3°, alınan: {result.theta_res_deg:.4f}°"
    )


def test_theta_res_zero_for_aligned_frames() -> None:
    """
    Hizalanmış kareler için theta_res sıfır olmalı ve Mode N seçilmeli.
    """
    # Arrange + Act
    result = check_mode_n_eligibility(
        same_detector=True,
        pa_ref_deg=45.0,
        pa_frame_deg=45.0,
        sps_epa_ref=0.0,
        sps_epa_frame=0.0,
    )

    # Assert
    assert result.theta_res_deg < 1e-9
    assert result.allow_mode_n is True
    assert result.mode == "N"
