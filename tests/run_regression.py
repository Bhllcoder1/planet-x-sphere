"""
run_regression.py — Regresyon paketi koşucusu.

pytest'i programatik olarak çalıştırır; sonuçları raporlar.
Kullanım: python tests/run_regression.py

Çıkış kodları
-------------
0  — Tüm testler başarılı.
1  — En az bir test başarısız veya hata var.
"""
from __future__ import annotations

import pathlib
import sys
import time

import pytest


def main() -> None:
    """Regresyon test paketini çalıştır ve sonucu raporla."""
    # Bu betiğin bulunduğu dizin = tests/
    tests_dir: pathlib.Path = pathlib.Path(__file__).parent
    regression_file: pathlib.Path = tests_dir / "test_regression.py"

    if not regression_file.exists():
        print(f"[HATA] Regresyon test dosyası bulunamadı: {regression_file}")
        sys.exit(1)

    print("=" * 60)
    print("  Regresyon paketi başlatılıyor …")
    print(f"  Dosya : {regression_file}")
    print("=" * 60)

    baslangic: float = time.monotonic()

    ret: int | pytest.ExitCode = pytest.main(
        [
            str(regression_file),
            "--tb=short",   # kısa traceback
            "-v",           # her test ayrı satırda
            "--no-header",  # gereksiz pytest başlığını gizle
            "-p", "no:warnings",  # uyarıları bastır (daha temiz çıktı)
        ]
    )

    sure: float = time.monotonic() - baslangic

    print("=" * 60)
    if ret == pytest.ExitCode.OK or ret == 0:
        print(f"  SONUÇ : BAŞARILI  ({sure:.2f} s)")
    else:
        print(f"  SONUÇ : BAŞARISIZ (çıkış kodu: {int(ret)}, süre: {sure:.2f} s)")
        print("  Başarısız testler yukarıda listelendi.")
    print("=" * 60)

    if ret != pytest.ExitCode.OK and ret != 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
