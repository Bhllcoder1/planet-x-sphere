import unittest

from linker import link_movers


class MoverLinkerTests(unittest.TestCase):
    def test_fewer_than_3_frames_closes_linking(self):
        dets = [
            {"frame_id": "f1", "mjd": 60100.0, "det_id": "d1", "x": 100.0, "y": 200.0},
            {"frame_id": "f2", "mjd": 60100.2, "det_id": "d2", "x": 102.0, "y": 201.0},
        ]
        res = link_movers(dets)
        self.assertEqual(res["status"], "linking_closed")
        self.assertEqual(res["tracks"], [])

    def test_recovers_moving_asteroid_amid_static_stars_and_noise(self):
        # 4 kare, aralarinda 6 saat; gercek asteroit vx=1.2, vy=-0.8 px/saat
        vx_true, vy_true = 1.2, -0.8
        x0, y0, mjd0 = 500.0, 600.0, 60100.0
        dets = []
        for k in range(4):
            mjd = mjd0 + k * 0.25  # +6 saat
            dt_hr = k * 6.0
            fid = f"f{k}"
            # Asteroit (+0.15 px kucuk olcum gurultusu)
            dets.append({
                "frame_id": fid, "mjd": mjd, "det_id": f"ast_{k}",
                "x": x0 + vx_true * dt_hr + (0.1 if k % 2 else -0.1),
                "y": y0 + vy_true * dt_hr + (-0.05 if k % 2 else 0.05),
            })
            # Sabit yildiz (tum karelerde ayni piksel)
            dets.append({
                "frame_id": fid, "mjd": mjd, "det_id": f"star_{k}",
                "x": 300.2, "y": 400.4,
            })
            # Gaia eslesmeli sabit yildiz
            dets.append({
                "frame_id": fid, "mjd": mjd, "det_id": f"gaia_{k}",
                "x": 800.0, "y": 900.0, "catalog_match": True,
            })

        res = link_movers(dets)
        self.assertEqual(res["status"], "ok")
        self.assertEqual(len(res["tracks"]), 1)
        tr = res["tracks"][0]
        self.assertEqual(tr["n_detections"], 4)
        self.assertLess(tr["max_residual_px"], 1.0)
        self.assertAlmostEqual(tr["vx_px_hr"], vx_true, places=1)
        self.assertAlmostEqual(tr["vy_px_hr"], vy_true, places=1)
        self.assertEqual(tr["veto_reason"], [])
        self.assertEqual(
            {d["frame_id"] for d in tr["detection_refs"]},
            {"f0", "f1", "f2", "f3"},
        )
        self.assertGreaterEqual(len(res["candidates_log"]), 1)


if __name__ == "__main__":
    unittest.main()
