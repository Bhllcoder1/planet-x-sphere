"""
Alan A Birim Testleri (02-03, 02-04, 02-13, 02-16, 02-19, 02-22, 11-02, 11-12, 11-15)
"""

import random
import unittest

from a_veri_isleme.process.pixel_conventions import (
    cutout_to_parent_pixel,
    parent_to_cutout_pixel,
    native_to_screen_px,
    check_mode_n_eligibility,
)
from a_veri_isleme.process.masks import (
    BASE_FIT_MASK,
    MASK_OUTLIER,
    MASK_SOURCE,
    MASK_STREAK,
    MASK_PROFILE_TABLE,
    build_pixel_mask,
    evaluate_frame_quality,
)
from a_veri_isleme.display.stretch import (
    array_sha256,
    apply_display_background,
    compute_clip_limits,
    stretch_array,
    render_rgba8,
    load_display_defaults,
)
from a_veri_isleme.exports.exporter import (
    mjy_sr_to_mjy,
    export_measurements_csv,
)
from a_veri_isleme.fetch.tap_s3_client import (
    uri_to_s3_key,
    extract_detector_from_uri,
    deduplicate_tap_rows,
    compute_row_span_byte_range,
    ROW_STRIDE_BYTES,
)


class TestAlanAModules(unittest.TestCase):
    def test_parent_pixel_roundtrip(self):
        # [V: s0_B §4] x_orig = 1 + x_cut - CRPIX1A
        x_orig, y_orig = cutout_to_parent_pixel(15.25, 20.75, crpix1a=-100.0, crpix2a=-200.0)
        self.assertAlmostEqual(x_orig, 116.25, places=7)
        self.assertAlmostEqual(y_orig, 221.75, places=7)
        xc, yc = parent_to_cutout_pixel(x_orig, y_orig, crpix1a=-100.0, crpix2a=-200.0)
        self.assertAlmostEqual(xc, 15.25, places=7)
        self.assertAlmostEqual(yc, 20.75, places=7)

    def test_float_position_never_rounded(self):
        # [V: DECISIONS_AND_TASK.md] float position 4.47 at zoom 100 -> 447.0 +/- 0.5 screen px
        sx, sy = native_to_screen_px(4.47, 10.12, zoom=100, half_pixel_center=False)
        self.assertAlmostEqual(sx, 447.0, places=5)
        self.assertAlmostEqual(sy, 1012.0, places=5)

    def test_mode_n_eligibility_31x31(self):
        # 31x31 pencerede r_edge = hypot(15, 15) = 21.213 px -> 0.25 px sınırı ~0.675 derece
        ok = check_mode_n_eligibility(
            same_detector=True,
            pa_ref_deg=181.0,
            pa_frame_deg=181.5,
            sps_epa_ref=180.0,
            sps_epa_frame=180.0,
        )
        self.assertTrue(ok.allow_mode_n)
        self.assertEqual(ok.mode, "N")

        not_ok = check_mode_n_eligibility(
            same_detector=True,
            pa_ref_deg=181.0,
            pa_frame_deg=182.2,
            sps_epa_ref=180.0,
            sps_epa_frame=180.0,
        )
        self.assertFalse(not_ok.allow_mode_n)
        self.assertEqual(not_ok.mode, "R-k")

    def test_mask_profiles_centroid_vs_mover(self):
        flags = [0, MASK_OUTLIER, MASK_SOURCE, MASK_STREAK, BASE_FIT_MASK]
        c_mask = build_pixel_mask(flags, profile="centroid")
        m_mask = build_pixel_mask(flags, profile="mover_search")

        # STREAK merkezlemede maskelenir, mover_search'te maskelenmez (veto/uyarı olarak kalır)
        self.assertTrue(c_mask[3])
        self.assertFalse(m_mask[3])

        # OUTLIER ve SOURCE mover_search'te ASLA maskelenmez
        self.assertFalse(m_mask[1])
        self.assertFalse(m_mask[2])
        self.assertEqual(MASK_PROFILE_TABLE["mover_search"].hex_mask, "0x3C028E44")

    def test_frame_quality_flags(self):
        flags = [[MASK_SOURCE for _ in range(10)] for _ in range(10)]
        q = evaluate_frame_quality(flags)
        self.assertTrue(q["crowded_field"])
        self.assertFalse(q["mover_linking_enabled"])
        self.assertIn("crowded-field", q["badges"])

    def test_display_never_modifies_measurement_data(self):
        rng = random.Random(42)
        img = [[rng.gauss(10.0, 2.0) for _ in range(31)] for _ in range(31)]
        img[15][15] = float("nan")  # Barnard NaN core
        zodi = [[8.0 for _ in range(31)] for _ in range(31)]
        flags = [[0 for _ in range(31)] for _ in range(31)]

        orig_hash = array_sha256(img)
        disp_bg, meta = apply_display_background(img, zodi=zodi, flags=flags, mode="flat")
        lo, hi = compute_clip_limits([disp_bg], [flags], clip_mode="percent")
        stretched = stretch_array(disp_bg, lo, hi, asinh_a=0.1, invert=False)
        rgba = render_rgba8(stretched)

        # Ölçüm verisi bit-bit aynı kalmalı
        self.assertEqual(array_sha256(img), orig_hash)
        # NaN çekirdek Okabe-Ito mavi (0, 114, 178, 255) olmalı
        self.assertEqual(tuple(rgba[15][15]), (0, 114, 178, 255))
        self.assertEqual(meta["units"], "MJy/sr")
        defaults = load_display_defaults()
        self.assertEqual(defaults["clip_mode"], "percent")

    def test_csv_export_and_unit_conversion(self):
        flux_mjy = mjy_sr_to_mjy(1.0, pixel_scale_arcsec=6.15)
        self.assertAlmostEqual(flux_mjy, (6.15 / 206264.80624709636) ** 2 * 1e9, places=6)

        csv_text = export_measurements_csv(
            [
                {
                    "target_name": "Barnard's Star",
                    "frame_id": "level2_2025W35_2A_0233_1D1",
                    "obs_id": "2025W35_2A_0233_1",
                    "detector": "D1",
                    "pass_id": 0,
                    "mjd_avg": 60916.72,
                    "x_px": 512.47,
                    "y_px": 512.12,
                    "sigma_x_px": 0.04,
                    "sigma_y_px": 0.04,
                    "cov_xy_px2": 0.0,
                    "ra_deg": 269.452,
                    "dec_deg": 4.693,
                    "flux_mjy_sr_sum": 120.5,
                    "flux_mjy": round(mjy_sr_to_mjy(120.5), 4),
                    "flux_err_mjy": 0.5,
                    "snr": 85.2,
                    "fit_mode": "saturated-fit",
                    "quality_badges": "saturated-fit",
                    "honesty_tag": "[V]",
                }
            ],
            target_name="Barnard's Star",
        )
        self.assertIn("# Kaynak (Provenance):", csv_text)
        self.assertIn("# Dürüst Sınır Notu:", csv_text)
        self.assertIn("Barnard's Star", csv_text)

    def test_tap_uri_dedup_and_coalesced_range(self):
        uri1 = "ibe/data/spherex/dr1/level2/2025W35_2A/l2b-v27-2026-230/1/level2_2025W35_2A_0233_1D1_spx_l2b-v27-2026-230.fits"
        uri2 = "ibe/data/spherex/dr1/level2/2025W35_2A/l2b-v27-2026-231/1/level2_2025W35_2A_0233_1D1_spx_l2b-v27-2026-231.fits"
        self.assertEqual(
            uri_to_s3_key(uri2),
            "dr1/level2/2025W35_2A/l2b-v27-2026-231/1/level2_2025W35_2A_0233_1D1_spx_l2b-v27-2026-231.fits",
        )
        self.assertEqual(extract_detector_from_uri(uri2), 1)
        deduped = deduplicate_tap_rows([
            {"obs_id": "2025W35_2A_0233_1", "uri": uri1},
            {"obs_id": "2025W35_2A_0233_1", "uri": uri2},
        ])
        self.assertEqual(len(deduped), 1)
        self.assertEqual(deduped[0]["procver"], "l2b-v27-2026-231")

        # 100 satırlık pencere Range GET bayt aralığı (100 * 8160 = 816,000 bayt)
        b_start, b_end = compute_row_span_byte_range(28800, 100, 200)
        self.assertEqual(b_end - b_start + 1, 100 * ROW_STRIDE_BYTES)


if __name__ == "__main__":
    unittest.main()
