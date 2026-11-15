import json
import unittest
from pathlib import Path

from coord_audit import audit_directory, audit_source
from ellipse import catalog_fields


class CoordAuditTests(unittest.TestCase):
    def test_b_astrometri_has_no_coordinate_rounding_or_origin_1(self):
        root = Path(__file__).resolve().parents[1]
        issues = audit_directory(root)
        self.assertEqual(issues, {}, f"Koordinat kurali ihlalleri: {issues}")

    def test_detects_forbidden_rounding_and_origin_1(self):
        bad = (
            "x_px = round(x)\n"
            "y_px = np.floor(y)\n"
            "sky = wcs.pixel_to_world(x, y, origin=1)\n"
        )
        issues = audit_source(bad, "sample.py")
        self.assertEqual(len(issues), 3)

    def test_ellipse_outputs_preserve_subpixel_native_floats(self):
        fields = catalog_fields([[0.04123456789, 0.00321], [0.00321, 0.01987654321]])
        for k, v in fields.items():
            self.assertIs(type(v), float, f"{k} native float olmali")
        encoded = json.dumps(fields)
        decoded = json.loads(encoded)
        self.assertAlmostEqual(decoded["a1"], fields["a1"], places=12)


if __name__ == "__main__":
    unittest.main()
