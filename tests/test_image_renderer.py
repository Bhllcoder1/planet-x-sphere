"""
test_image_renderer.py — PNG ve küçük resim üretimi testleri (Görev 02-20).
"""
import io
import sys
from pathlib import Path
import numpy as np
from PIL import Image
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT / "c_sunucu") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "c_sunucu"))

from api.image_renderer import render_thumbnail_64, render_to_png


@pytest.fixture
def sample_image_64():
    np.random.seed(42)
    img = np.random.uniform(10.0, 100.0, size=(64, 64)).astype(np.float32)
    # Birkaç NaN piksel ekle (sözleşme gereği test etmek için)
    img[10, 10] = np.nan
    img[10, 11] = np.nan
    return img


def test_png_signature_and_dimensions(sample_image_64):
    """Üretilen baytların geçerli bir PNG dosyası olduğunu ve boyutunu doğrular."""
    png_bytes = render_to_png(sample_image_64, zoom=1)
    assert png_bytes.startswith(b"\x89PNG\r\n\x1a\n")

    img = Image.open(io.BytesIO(png_bytes))
    assert img.size == (64, 64)
    assert img.mode == "RGBA"


def test_integer_zoom_nearest_neighbor(sample_image_64):
    """zoom=4 verildiğinde boyutun 256×256 olduğunu doğrular."""
    png_bytes = render_to_png(sample_image_64, zoom=4)
    img = Image.open(io.BytesIO(png_bytes))
    assert img.size == (256, 256)


def test_nan_pixels_colored_okabe_ito_blue(sample_image_64):
    """NaN piksellerin Okabe-Ito mavisi (0, 114, 178) ile boyandığını doğrular."""
    png_bytes = render_to_png(sample_image_64, zoom=1)
    img = Image.open(io.BytesIO(png_bytes))
    rgba = np.array(img)

    # (10, 10) NaN idi
    nan_pixel = rgba[10, 10]
    assert nan_pixel[0] == 0
    assert nan_pixel[1] == 114
    assert nan_pixel[2] == 178
    assert nan_pixel[3] == 255


def test_grid_and_markers(sample_image_64):
    """Izgara ve işaretçilerin görüntüyü bozmadan başarıyla eklendiğini doğrular."""
    markers = [{"x": 32.5, "y": 32.5, "label": "Barnard"}]
    png_bytes = render_to_png(sample_image_64, zoom=2, draw_grid=True, markers=markers)
    img = Image.open(io.BytesIO(png_bytes))
    assert img.size == (128, 128)


def test_thumbnail_64(sample_image_64):
    """Thumbnail fonksiyonunun tam 64×64 PNG ürettiğini doğrular."""
    thumb_bytes = render_thumbnail_64(sample_image_64)
    assert thumb_bytes.startswith(b"\x89PNG\r\n\x1a\n")
    img = Image.open(io.BytesIO(thumb_bytes))
    assert img.size == (64, 64)
