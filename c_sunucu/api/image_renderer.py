"""
image_renderer.py — PNG ve küçük resim üretimi (Görev 02-20).

Kullanıcı durumu / URL parametrelerinden sunucu tarafında birebir aynı görüntüyü
PNG ve küçük resim (thumbnail) olarak üretir.

Kurallar:
- Yakınlaştırma tam sayı (zoom = 1, 2, 4, 8) ve en yakın komşu (nearest neighbor) ile yapılır;
  PSF pikselleri ASLA bulanıklaştırılmaz / enterpole edilmez [V: PLAN_v2 §D].
- NaN pikseller Okabe-Ito mavi renk ile çizilir [V: DISPLAY_LAYER_DESIGN.md §2.1].
- İsteğe bağlı ızgara çizgileri ve hedef işaretçileri (+ reticle) yerel float koordinatlarına göre
  zoom ile ölçeklenerek çizilir.
- Çıktı geçerli PNG bayt dizisidir (Pillow ile kodlanır).
"""
from __future__ import annotations

import io
import math
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
from PIL import Image, ImageDraw

from a_veri_isleme.display.stretch import (
    apply_display_background,
    compute_clip_limits,
    render_rgba8,
    stretch_array,
)


def render_to_png(
    image: np.ndarray,
    zodi: Optional[np.ndarray] = None,
    flags: Optional[np.ndarray] = None,
    bg_mode: str = "zodi",
    clip_mode: str = "percent",
    low_pct: float = 0.5,
    high_pct: float = 99.5,
    asinh_a: float = 0.1,
    invert: bool = False,
    zoom: int = 1,
    draw_grid: bool = False,
    markers: Optional[List[Dict[str, Any]]] = None,
) -> bytes:
    """
    Kare veya pencere verisinden URL parametrelerine uygun PNG üretir.

    Args:
        image: 2B float32 dizi (H, W).
        zodi: İsteğe bağlı ZODI arka plan dizisi.
        flags: İsteğe bağlı bayrak dizisi.
        bg_mode: 'raw', 'zodi', veya 'flat'.
        clip_mode: 'percent', 'zscale', 'adapt', veya 'fixed'.
        zoom: Tam sayı büyütme katsayısı (1, 2, 4, 8 vb.).
        draw_grid: True ise piksel ızgarası çizgilerini çizer.
        markers: İsteğe bağlı işaretçi listesi [{'x': float, 'y': float, 'label': str}].

    Returns:
        PNG dosyasının ham baytları (bytes).
    """
    if zoom < 1:
        zoom = 1

    # 1. Arka plan gösterim modunu uygula (kopya üzerinde çalışır, orijinal değişmez)
    v_display, _ = apply_display_background(image, zodi=zodi, flags=flags, mode=bg_mode)

    # 2. Limit hesaplama
    lo, hi = compute_clip_limits(
        frames=[v_display],
        flags_list=[flags] if flags is not None else None,
        clip_mode=clip_mode,
        low_pct=low_pct,
        high_pct=high_pct,
    )

    # 3. Asinh germe
    stretched = stretch_array(v_display, lo=lo, hi=hi, asinh_a=asinh_a, invert=invert)

    # 4. RGBA8 matrisine dönüştür
    rgba = render_rgba8(stretched)

    # 5. PIL Image oluştur
    h, w, _ = rgba.shape
    base_img = Image.fromarray(rgba, mode="RGBA")

    # 6. Tam sayı yakınlaştırma (Nearest Neighbor)
    if zoom > 1:
        out_w = w * zoom
        out_h = h * zoom
        img = base_img.resize((out_w, out_h), resample=Image.NEAREST)
    else:
        img = base_img.copy()

    # 7. Çizim katmanı (Izgara ve işaretçiler)
    if draw_grid or markers:
        draw = ImageDraw.Draw(img)

        # Izgara çizgileri (zoom >= 4 iken belirgin, zoom < 4 iken her 10 pikselde bir)
        if draw_grid:
            grid_step = 1 if zoom >= 4 else 10
            grid_color = (200, 200, 200, 100)
            for col in range(0, w, grid_step):
                x = col * zoom
                draw.line([(x, 0), (x, h * zoom)], fill=grid_color, width=1)
            for row in range(0, h, grid_step):
                y = row * zoom
                draw.line([(0, y), (w * zoom, y)], fill=grid_color, width=1)

        # İşaretçiler (Crosshair / Reticle)
        if markers:
            marker_color = (255, 65, 54, 230)  # Kırmızı reticle
            for m in markers:
                mx = float(m.get("x", 0.0)) * zoom
                my = float(m.get("y", 0.0)) * zoom
                r = max(4, zoom * 2)
                # Artı işareti (+)
                draw.line([(mx - r, my), (mx + r, my)], fill=marker_color, width=max(1, zoom // 2))
                draw.line([(mx, my - r), (mx, my + r)], fill=marker_color, width=max(1, zoom // 2))
                # Daire
                draw.ellipse([(mx - r, my - r), (mx + r, my + r)], outline=marker_color, width=1)

    # 8. PNG olarak kodla
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def render_thumbnail_64(image: np.ndarray) -> bytes:
    """
    Hızlı liste ve önizleme için 64×64 thumbnail PNG üretir.
    En yakın komşu ile ölçekler; ölçüm verisini asla bozmaz.
    """
    lo, hi = compute_clip_limits(frames=[image], clip_mode="percent", low_pct=1.0, high_pct=99.0)
    stretched = stretch_array(image, lo=lo, hi=hi, asinh_a=0.1)
    rgba = render_rgba8(stretched)
    base_img = Image.fromarray(rgba, mode="RGBA")
    thumb = base_img.resize((64, 64), resample=Image.NEAREST)

    buf = io.BytesIO()
    thumb.save(buf, format="PNG")
    return buf.getvalue()
