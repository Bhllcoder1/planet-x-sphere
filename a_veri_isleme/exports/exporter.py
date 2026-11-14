"""
Alan A - Görev 11-02, 11-03, 11-12, 11-15: Dışa Aktarım Şeması, Birim Dönüşümü ve CSV Üretimi
Doğrulama durumu:
- SPHEREx yüzey parlaklığı birimi: MJy/sr [V: s0_B]
- Piksel ölçeği: ~6.15 arcsec/px [V: s0_C §3] -> katı açı Ω_px ve MJy/sr -> mJy dönüşümü
- Her çıktıya kaynak bloğu (provenance) ve dürüst sınır notu eklenmesi [Görev 11-15]
"""

from __future__ import annotations
import csv
import io
import math
from typing import Dict, Iterable, List

ARCSEC_PER_RAD = 206264.80624709636
DEFAULT_PIXEL_SCALE_ARCSEC = 6.15  # [V: s0_C §3]

CSV_COLUMNS: List[str] = [
    "target_name",
    "frame_id",
    "obs_id",
    "detector",
    "pass_id",
    "mjd_avg",
    "x_px",
    "y_px",
    "sigma_x_px",
    "sigma_y_px",
    "cov_xy_px2",
    "ra_deg",
    "dec_deg",
    "flux_mjy_sr_sum",
    "flux_mjy",
    "flux_err_mjy",
    "snr",
    "fit_mode",
    "quality_badges",
    "honesty_tag",
]


def mjy_sr_to_mjy(
    surface_brightness_mjy_sr: float,
    pixel_scale_arcsec: float = DEFAULT_PIXEL_SCALE_ARCSEC,
) -> float:
    """
    Görev 11-02: MJy/sr yüzey parlaklığını piksel başına nokta kaynak akısına (mJy) dönüştürür.
    1 MJy = 10^9 Jy = 10^12 mJy
    Ω_px (sr) = (pixel_scale_arcsec / 206264.806247)^2
    F (mJy) = I (MJy/sr) * Ω_px (sr) * 10^9
    """
    omega_sr = (float(pixel_scale_arcsec) / ARCSEC_PER_RAD) ** 2
    return float(surface_brightness_mjy_sr) * omega_sr * 1e9


def build_provenance_header(
    target_name: str,
    pipeline_version: str = "planet-x-sphere-a-0.1.0",
    honesty_note: str = (
        "[V: s0_B, s0_C] Başlık WCS ve S3 piksel okuma doğrulandı; "
        "[NV] us-east-1 canlı gecikme ve 3 hedefin (WISE 0855, RW Aur, R Dra) tam TAP kapsamı doğrulanmadı."
    ),
) -> List[str]:
    """
    Görev 11-15: Her dışa aktarılan çıktıya eklenecek kaynak (provenance) bloğu ve
    dürüst sınır notu.
    """
    return [
        f"# Kaynak (Provenance): NASA/IPAC IRSA SPHEREx (dr1/qr3, provenance 7.0.5), ESA/MAST Gaia DR3",
        f"# Boru Hattı: {pipeline_version} | Hedef: {target_name}",
        f"# Piksel Kuralları: 0-tabanlı float koordinatlar (yuvarlanmamış); Drizzle KAPALI [V: 00-01]",
        f"# Dürüst Sınır Notu: {honesty_note}",
    ]


def export_measurements_csv(
    rows: Iterable[Dict[str, object]],
    target_name: str,
    honesty_note: str | None = None,
) -> str:
    """
    Görev 11-03 & 11-12: Ölçüm tablosunu kaynak başlığı ve şemaya uygun sütunlarla
    CSV metnine dönüştürür. Gösterim ayarlarından hiçbir girdi almaz.
    """
    buf = io.StringIO()
    header_lines = (
        build_provenance_header(target_name, honesty_note=honesty_note)
        if honesty_note
        else build_provenance_header(target_name)
    )
    for line in header_lines:
        buf.write(line + "\n")

    writer = csv.DictWriter(buf, fieldnames=CSV_COLUMNS, extrasaction="ignore")
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    return buf.getvalue()
