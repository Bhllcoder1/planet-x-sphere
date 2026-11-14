"""
Alan A - Görev 02-03: Alma + Piksel Kuralları Modülü (C.3)
Doğrulama durumu:
- Parent-piksel dönüşümü: [V: s0_B §4] (< 1e-7 px SIP WCS uyumu)
- Mode N dönme eşiği: [V: PLAN_spherex_v3.md §2.2]
- Float konumların yuvarlanmaması kuralı: [V: DECISIONS_AND_TASK.md]
"""

from __future__ import annotations
import math
from dataclasses import dataclass
from typing import Tuple


def cutout_to_parent_pixel(
    x_cut: float,
    y_cut: float,
    crpix1a: float,
    crpix2a: float,
) -> Tuple[float, float]:
    """
    Kesit (cutout) 0-tabanlı piksel koordinatlarını ana (parent) dedektörün
    0-tabanlı piksel koordinatlarına dönüştürür [V: s0_B §4].

    Formül:
        x_orig = 1.0 + x_cut - CRPIX1A
        y_orig = 1.0 + y_cut - CRPIX2A
    """
    x_orig = 1.0 + float(x_cut) - float(crpix1a)
    y_orig = 1.0 + float(y_cut) - float(crpix2a)
    return x_orig, y_orig


def parent_to_cutout_pixel(
    x_orig: float,
    y_orig: float,
    crpix1a: float,
    crpix2a: float,
) -> Tuple[float, float]:
    """
    Ana dedektör 0-tabanlı piksel koordinatlarını kesit (cutout) 0-tabanlı
    koordinatlarına dönüştürür [V: s0_B §4].
    """
    x_cut = float(x_orig) - 1.0 + float(crpix1a)
    y_cut = float(y_orig) - 1.0 + float(crpix2a)
    return x_cut, y_cut


def native_to_screen_px(
    x_native: float,
    y_native: float,
    zoom: int,
    origin_x: int = 0,
    origin_y: int = 0,
    half_pixel_center: bool = False,
) -> Tuple[float, float]:
    """
    0-tabanlı doğal float piksel konumunu ekran pikseline dönüştürür.
    Kesirli konumlar ASLA tam sayıya yuvarlanmaz [V: DECISIONS_AND_TASK.md]:
    Örn: x_native = 4.47, zoom = 100, half_pixel_center = False -> 447.0 ekran pikseli.

    Tek yarım-piksel fonksiyonu (C.3):
    FITS/WCS piksel merkezi tam sayı indeksindedir (0.0, 1.0, ...).
    Canvas/WebGL doku (texture) sol-üst köşesi (0,0) ise piksel merkezi +0.5 kayar.
    Bu bayrak tüm boru hattında tek bir noktadan yönetilir.
    """
    if zoom <= 0 or int(zoom) != zoom:
        raise ValueError(f"Zoom pozitif tam sayı olmalıdır, verilen: {zoom}")
    offset = 0.5 if half_pixel_center else 0.0
    sx = (float(x_native) - float(origin_x) + offset) * float(zoom)
    sy = (float(y_native) - float(origin_y) + offset) * float(zoom)
    return sx, sy


@dataclass(frozen=True)
class ModeNCheckResult:
    allow_mode_n: bool
    mode: str
    theta_res_deg: float
    edge_displacement_px: float
    reason: str


def check_mode_n_eligibility(
    same_detector: bool,
    pa_ref_deg: float,
    pa_frame_deg: float,
    sps_epa_ref: float,
    sps_epa_frame: float,
    window_width: int = 31,
    window_height: int = 31,
    max_edge_disp_px: float = 0.25,
) -> ModeNCheckResult:
    """
    Mode N uygunluk kuralı [V: PLAN_spherex_v3.md §2.2]:
    - Yalnızca aynı dedektör olduğunda ve pencere köşesindeki artık dönme kayması
      r_edge * theta_res <= 0.25 px olduğunda Mode N varsayılan olur.
    - SPS_EPA farkı 180 derece ise tam 180 derece çevirme uygulanır ve kalan
      artık açı (theta_res) hesaplanır.
    - 31x31 pencere için r_edge = hypot(15, 15) ≈ 21.21 px -> theta_res <= ~0.675°.
    """
    if not same_detector:
        return ModeNCheckResult(
            allow_mode_n=False,
            mode="R-k",
            theta_res_deg=float("nan"),
            edge_displacement_px=float("nan"),
            reason="Farklı dedektör: doğal ızgaralar uyuşmuyor, sunucu R-k modu seçildi.",
        )

    expected_flip = 180.0 if abs(float(sps_epa_frame) - float(sps_epa_ref)) > 90.0 else 0.0
    raw_diff = (float(pa_frame_deg) - float(pa_ref_deg) - expected_flip) % 360.0
    if raw_diff > 180.0:
        raw_diff -= 360.0
    theta_res_deg = abs(raw_diff)
    theta_res_rad = math.radians(theta_res_deg)

    r_edge = math.hypot((window_width - 1) / 2.0, (window_height - 1) / 2.0)
    edge_disp = r_edge * theta_res_rad

    if edge_disp <= max_edge_disp_px:
        return ModeNCheckResult(
            allow_mode_n=True,
            mode="N",
            theta_res_deg=theta_res_deg,
            edge_displacement_px=edge_disp,
            reason=f"θ_res {theta_res_deg:.2f}° -> kenarda <= {edge_disp:.2f} px (Mode N uygun)",
        )
    return ModeNCheckResult(
        allow_mode_n=False,
        mode="R-k",
        theta_res_deg=theta_res_deg,
        edge_displacement_px=edge_disp,
        reason=(
            f"θ_res {theta_res_deg:.2f}° -> kenarda {edge_disp:.2f} px > {max_edge_disp_px} px sınırı; "
            "Mode R-k seçildi."
        ),
    )
