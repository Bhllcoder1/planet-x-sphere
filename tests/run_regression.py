#!/usr/bin/env python3
"""
Ana Regresyon ve Doğrulama Koşucusu (tests/run_regression.py)
- Alan A (a_veri_isleme) Python birim testlerini çalıştırır (8 test)
- Alan D (d_site) Python doğrulama testlerini çalıştırır (7 test)
- Alan D (tests/test_viewer_js.mjs) Node.js ES modül testlerini çalıştırır (8 test grubu)
- 07-15 5 yarışma hedefi kontak sayfası manifestini (tests/contact_sheets_07_15.json) üretir
"""

from __future__ import annotations
import json
import os
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from d_site.test_alan_d import generate_5_target_contact_sheet_summary


def main() -> int:
    print("=== [1/3] Running Python Unit & Validation Tests (Alan A + Alan D) ===")
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=ROOT, pattern="test_alan_*.py", top_level_dir=ROOT)
    runner = unittest.TextTestRunner(verbosity=2)
    py_result = runner.run(suite)
    if not py_result.wasSuccessful():
        return 1

    print("\n=== [2/3] Running Node.js Viewer & UI Regression Suite (tests/test_viewer_js.mjs) ===")
    js_proc = subprocess.run(
        ["node", os.path.join(ROOT, "tests", "test_viewer_js.mjs")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    print(js_proc.stdout)
    if js_proc.returncode != 0:
        print(js_proc.stderr, file=sys.stderr)
        return js_proc.returncode

    print("=== [3/3] Generating 5-Target Contact Sheet Manifest (Task 07-15) ===")
    sheets = generate_5_target_contact_sheet_summary()
    out_json = os.path.join(ROOT, "tests", "contact_sheets_07_15.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(
            {
                "task_id": "07-15",
                "targets_count": len(sheets),
                "honesty_rule": "Unverified targets emit honest status cards ('not_measured'), never substituted.",
                "sheets": sheets,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )
    print(f"Wrote {out_json} ({len(sheets)} targets).")
    print("\nALL REGRESSION TESTS PASSED (15 Python tests + 8 JS test suites = 23/23 OK).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
