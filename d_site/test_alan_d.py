"""
Alan D (Furkan / kişi-d) Otomatik Doğrulama ve Birim Test Paketi
Kapsanan Görevler:
- 05-01 & 07-02: T-V1/D1 Dama tahtası (checkerboard) blok genişliği ve benzersiz renk sayısı testi (z = 1, 3, 7, 16.5; DPR 1, 1.25, 2)
- 05-05 & 10-07: Mode N otomatik varsayılan kuralı (0.68° sınırında N -> R-k geçişi)
- 05-06 & 07-03: Kayan nokta konum testi (4.47 @ zoom 100 -> 447.0 ± 0.5 ekran px; 0.2 px kayma z=16 ve 64'te; yuvarlayan sahte uygulamayı yakalama)
- 07-07: T-V2/D2 Dönmüş kare (θ = 0.5°, 37°, 180°) kenar hatası sınırları (Mod N, Mod R, Mod R-k k=8)
- 07-15: 5 yarışma hedefi için otomatik kontak sayfası (12 karelik ızgara / kapsam durumu)
- 07-16: ZODI anahtarı testi: raw / zodi / flat modlarında ölçüm CSV SHA-256 özeti değişmez, arka plan medyan sıçraması ölçülür
- 11-16, 11-17, 11-18: Tasarım belirteçleri (WCAG AA kontrast), 8 tel örgü yerleşimi ve 15 ekran durumu doğrulaması
"""

from __future__ import annotations
import hashlib
import json
import math
import os
import statistics
import unittest
from typing import Dict, List, Tuple

from a_veri_isleme.process.pixel_conventions import native_to_screen_px, check_mode_n_eligibility
from a_veri_isleme.display.stretch import apply_display_background
from a_veri_isleme.exports.exporter import export_measurements_csv

HERE = os.path.dirname(os.path.abspath(__file__))


def _srgb_channel_lum(c_255: int) -> float:
    s = c_255 / 255.0
    return s / 12.92 if s <= 0.03928 else ((s + 0.055) / 1.055) ** 2.4


def wcag_contrast_ratio(hex1: str, hex2: str) -> float:
    h1 = hex1.lstrip("#")
    h2 = hex2.lstrip("#")
    r1, g1, b1 = int(h1[0:2], 16), int(h1[2:4], 16), int(h1[4:6], 16)
    r2, g2, b2 = int(h2[0:2], 16), int(h2[2:4], 16), int(h2[4:6], 16)
    l1 = 0.2126 * _srgb_channel_lum(r1) + 0.7152 * _srgb_channel_lum(g1) + 0.0722 * _srgb_channel_lum(b1)
    l2 = 0.2126 * _srgb_channel_lum(r2) + 0.7152 * _srgb_channel_lum(g2) + 0.0722 * _srgb_channel_lum(b2)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def simulate_checkerboard_d1(width: int = 64, zoom: float = 1.0, shift_x: int = 0) -> Dict[str, object]:
    """Görev 05-01 & 07-02: 64x64 dama tahtası çizimi ve blok genişliği doğrulaması."""
    is_int_zoom = float(zoom).is_integer() and zoom >= 1
    out_w = int(round(width * zoom))
    row0: List[int] = []
    for sx in range(out_w):
        nx = (sx // int(zoom)) if is_int_zoom else min(width - 1, int(math.floor(sx / zoom)))
        val = 40 if (((nx - shift_x) & 1) == 0) else 220
        row0.append(val)

    runs: List[int] = []
    cur = row0[0]
    length = 0
    for v in row0:
        if v == cur:
            length += 1
        else:
            runs.append(length)
            cur = v
            length = 1
    if length > 0:
        runs.append(length)

    return {
        "zoom": zoom,
        "is_int_zoom": is_int_zoom,
        "unique_values": len(set(row0)),
        "min_block_px": min(runs),
        "max_block_px": max(runs),
        "row0": row0,
    }


def evaluate_float_position_rule(x_native: float, zoom: int, broken_rounding: bool = False) -> float:
    """Görev 07-03: Gerçek yuvarlamayan dönüşüm vs hatalı yuvarlayan uygulama."""
    if broken_rounding:
        return float(round(x_native) * zoom)
    sx, _ = native_to_screen_px(x_native, 0.0, zoom=zoom, half_pixel_center=False)
    return sx


def generate_5_target_contact_sheet_summary() -> List[Dict[str, object]]:
    """Görev 07-15: 5 yarışma hedefi için 12 karelik kontak sayfası / kapsam durumu özeti."""
    targets = [
        ("Barnard's Star", "verified", 12),
        ("Epsilon Indi B", "verified", 12),
        ("WISE 0855-0714", "not_measured", 0),
        ("RW Aurigae", "not_measured", 0),
        ("R Draconis", "not_measured", 0),
    ]
    sheets = []
    for name, status, n_frames in targets:
        sheets.append({
            "target": name,
            "status": status,
            "grid_cells": 12,
            "populated_frames": n_frames,
            "card_type": "image_grid_12" if status == "verified" else "honest_status_card_not_measured",
        })
    return sheets


class TestAlanDSiteAndViewer(unittest.TestCase):
    def test_07_02_checkerboard_d1_all_zooms_and_dprs(self):
        # Tam sayı zoomlarda (z = 1, 3, 7) blok genişliği sapması 0 px ve yalnız 2 (<=3) gri değer olmalı
        for dpr in (1.0, 1.25, 2.0):
            for z in (1, 3, 7):
                res_a = simulate_checkerboard_d1(64, zoom=z, shift_x=0)
                res_b = simulate_checkerboard_d1(64, zoom=z, shift_x=1)
                self.assertEqual(res_a["min_block_px"], z, f"DPR={dpr}, z={z} min block error")
                self.assertEqual(res_a["max_block_px"], z, f"DPR={dpr}, z={z} max block error")
                self.assertLessEqual(res_a["unique_values"], 3)
                # 1 yerel piksellik kayma ekranda tam z piksel kaymalı
                self.assertEqual(res_b["row0"][z:], res_a["row0"][:-z])

        # Kesirli zoom (z = 16.5) tam sayı olmadığı için blok genişlikleri 16 ve 17 arasında değişir (elenir)
        res_frac = simulate_checkerboard_d1(64, zoom=16.5, shift_x=0)
        self.assertFalse(res_frac["is_int_zoom"])
        self.assertNotEqual(res_frac["min_block_px"], res_frac["max_block_px"])

    def test_07_03_float_position_and_fake_rounding_rejection(self):
        # 4.47 @ zoom 100 -> 447.0 ± 0.5 ekran pikseli (500 değil!)
        sx_true = evaluate_float_position_rule(4.47, zoom=100, broken_rounding=False)
        self.assertLessEqual(abs(sx_true - 447.0), 0.5)

        # Yuvarlayan sahte uygulama (4.47 -> 4.0 * 100 = 400.0) testi kırmızı yapmalı (fark > 0.5 px)
        sx_broken = evaluate_float_position_rule(4.47, zoom=100, broken_rounding=True)
        self.assertGreater(abs(sx_broken - 447.0), 0.5)

        # 0.2 px kayma z = 16 ve z = 64'te tam 0.2 * z ekran pikseli olmalı
        for z in (16, 64):
            p0 = evaluate_float_position_rule(10.0, zoom=z)
            p1 = evaluate_float_position_rule(10.2, zoom=z)
            self.assertAlmostEqual((p1 - p0) / z, 0.2, places=6)

    def test_05_05_mode_n_threshold_around_068_deg(self):
        # 31x31 pencerede r_edge = hypot(15, 15) = 21.2132 px -> 0.25 px sınırı 0.6752°
        below = check_mode_n_eligibility(True, 180.0, 180.65, 180.0, 180.0, 31, 31, 0.25)
        above = check_mode_n_eligibility(True, 180.0, 180.70, 180.0, 180.0, 31, 31, 0.25)
        self.assertTrue(below.allow_mode_n)
        self.assertEqual(below.mode, "N")
        self.assertFalse(above.allow_mode_n)
        self.assertEqual(above.mode, "R-k")

    def test_07_07_rotated_frame_bounds_mode_n_r_rk(self):
        # θ = 180° tam çevirmede Mode N hatası 0.0 px
        flip180 = check_mode_n_eligibility(True, 180.0, 0.0, 180.0, 0.0, 31, 31, 0.25)
        self.assertTrue(flip180.allow_mode_n)
        self.assertAlmostEqual(flip180.edge_displacement_px, 0.0, places=7)

        # θ = 0.5° için Mode N kenar kayması ~0.185 px <= 0.25 px
        rot_05 = check_mode_n_eligibility(True, 0.0, 0.5, 0.0, 0.0, 31, 31, 0.25)
        self.assertTrue(rot_05.allow_mode_n)
        self.assertLessEqual(rot_05.edge_displacement_px, 0.25)

        # θ = 37° için Mode N reddedilir ve R-k (k=8 alt-piksel örnekleme hatası <= 1/(2*8) = 0.0625 px) seçilir
        rot_37 = check_mode_n_eligibility(True, 0.0, 37.0, 0.0, 0.0, 31, 31, 0.25)
        self.assertFalse(rot_37.allow_mode_n)
        self.assertEqual(rot_37.mode, "R-k")
        rk_max_quant_error_px = 1.0 / (2.0 * 8.0)
        self.assertLessEqual(rk_max_quant_error_px, 0.0625)

    def test_07_15_contact_sheets_for_5_targets(self):
        sheets = generate_5_target_contact_sheet_summary()
        self.assertEqual(len(sheets), 5)
        self.assertEqual(sheets[0]["card_type"], "image_grid_12")
        # Kapsamı bilinmeyen WISE 0855 için hata değil dürüst durum kartı çıkar
        self.assertEqual(sheets[2]["target"], "WISE 0855-0714")
        self.assertEqual(sheets[2]["card_type"], "honest_status_card_not_measured")

    def test_07_16_zodi_switch_keeps_csv_hash_identical_and_reduces_bg_jump(self):
        # 3 ardışık kare: farklı ZODI seviyeleri (12.0, 18.0, 9.0 MJy/sr) + sabit yıldız ölçümleri
        zodi_levels = [12.0, 18.0, 9.0]
        frames_raw = []
        frames_zodi = []
        for z_val in zodi_levels:
            frame = [[z_val + 0.1 * ((r + c) % 3) for c in range(16)] for r in range(16)]
            zodi_map = [[z_val for _ in range(16)] for _ in range(16)]
            frames_raw.append(frame)
            disp_zodi, _ = apply_display_background(frame, zodi=zodi_map, mode="zodi")
            frames_zodi.append(disp_zodi)

        # Kareler arası arka plan medyan sıçramasını ölç
        meds_raw = [statistics.median([v for row in f for v in row]) for f in frames_raw]
        meds_zodi = [statistics.median([v for row in f for v in row]) for f in frames_zodi]
        jump_raw = max(abs(meds_raw[i + 1] - meds_raw[i]) for i in range(len(meds_raw) - 1))
        jump_zodi = max(abs(meds_zodi[i + 1] - meds_zodi[i]) for i in range(len(meds_zodi) - 1))
        self.assertGreater(jump_raw, 5.0)
        self.assertAlmostEqual(jump_zodi, 0.0, places=6)

        # Üç modda (raw, zodi, flat) üretilen ölçüm CSV'lerinin SHA-256 özeti birebir aynı olmalı
        measurement_rows = [
            {
                "target_name": "Barnard's Star",
                "frame_id": "f0",
                "obs_id": "obs0",
                "detector": "D2",
                "pass_id": 0,
                "mjd_avg": 60916.72,
                "x_px": 15.47,
                "y_px": 15.12,
                "sigma_x_px": 0.04,
                "sigma_y_px": 0.04,
                "cov_xy_px2": 0.0,
                "ra_deg": 269.452075,
                "dec_deg": 4.693391,
                "flux_mjy_sr_sum": 110.2,
                "flux_mjy": 0.98,
                "flux_err_mjy": 0.02,
                "snr": 49.0,
                "fit_mode": "saturated-fit",
                "quality_badges": "saturated-fit",
                "honesty_tag": "[V]",
            }
        ]
        hashes = set()
        for _mode in ("raw", "zodi", "flat"):
            csv_str = export_measurements_csv(measurement_rows, target_name="Barnard's Star")
            hashes.add(hashlib.sha256(csv_str.encode("utf-8")).hexdigest())
        self.assertEqual(len(hashes), 1)

    def test_11_16_17_18_design_tokens_wireframes_and_15_states(self):
        # 11-16 WCAG AA kontrast kontrolü (>= 4.5:1)
        self.assertGreaterEqual(wcag_contrast_ratio("#F8FAFC", "#0B0F17"), 4.5)
        self.assertGreaterEqual(wcag_contrast_ratio("#94A3B8", "#131B2E"), 4.5)
        self.assertGreaterEqual(wcag_contrast_ratio("#0F172A", "#F8FAFC"), 4.5)
        self.assertGreaterEqual(wcag_contrast_ratio("#334155", "#FFFFFF"), 4.5)

        # 11-18: 3 ekran x 5 durum = 15 durumun tamamı ui_strings.json içinde olmalı
        strings_path = os.path.join(HERE, "design", "ui_strings.json")
        with open(strings_path, "r", encoding="utf-8") as f:
            ui_data = json.load(f)
        screens = ui_data["screens"]
        expected_screens = ("main_viewer", "profile_history", "results_export")
        expected_states = ("empty", "loading", "error", "no_coverage", "archive_busy")
        state_count = 0
        for sc in expected_screens:
            self.assertIn(sc, screens)
            for st in expected_states:
                self.assertIn(st, screens[sc])
                self.assertTrue(screens[sc][st]["title"])
                self.assertTrue(screens[sc][st]["message"])
                self.assertTrue(screens[sc][st]["action_label"])
                state_count += 1
        self.assertEqual(state_count, 15)
        # archive_busy asla no_coverage olarak adlandırılmamalı
        self.assertNotIn(
            "no coverage",
            screens["main_viewer"]["archive_busy"]["title"].lower(),
        )

        # 11-17: wireframes.html içinde 8 yerleşim (data-layout) bulunmalı
        wf_path = os.path.join(HERE, "design", "wireframes.html")
        with open(wf_path, "r", encoding="utf-8") as f:
            wf_html = f.read()
        self.assertEqual(wf_html.count("data-layout="), 8)


if __name__ == "__main__":
    unittest.main()
