# 07-04 T4 — gerçek WCS kesit doğrulaması

Stage 0 B veri kümesindeki dokuz gerçek 29×29 FITS kesitinin `IMAGE` uzantıları doğrulandı. Her dosyada SIP A/B düzeni 3 ve `RA---TAN-SIP` / `DEC--TAN-SIP` WCS vardır.

Komut:

```powershell
& C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe tests/test_T4.py --real-dir C:/Users/behlu/spherex-kb/stage0/data/B/cut
```

Komut her kesitteki 841 piksel merkezini 0 tabanlı `all_pix2world` → `all_world2pix` dönüşümünden geçirdi. Toplam 7.569 pikselde ölçülen en büyük dönüş hatası **4.47e-11 px** oldu; T4 eşiği **1e-4 px**.

| Kesit | En büyük hata (px) |
|---|---:|
| `f0_A.fits` | 1.94e-11 |
| `f0_B.fits` | 2.34e-11 |
| `f1_A.fits` | 2.88e-11 |
| `f1_B.fits` | 2.74e-11 |
| `f2_A.fits` | 2.34e-11 |
| `f2_B.fits` | 3.23e-11 |
| `f3_B.fits` | 4.47e-11 |
| `f4_A.fits` | 2.65e-11 |
| `f4_B.fits` | 2.65e-11 |

FITS verileri Stage 0 dizininde kaldı; depoya kopyalanmadı. Bu kanıt yalnızca mevcut dokuz dar kesit için T4'ü doğrular. 07-04'ün D3 kabulü için gereken 100 gerçek 50/100/200 px pencere ve T1 ekran kabulü için 07-03 görüntüleyici/Playwright çıktısı mevcut değildir. 07-04 bu nedenle bütünüyle tamamlanmış sayılmaz.
