# HANDOFF — planet-x-sphere (Alan A, B, C Ortak Durum)

> Bu dosyayı okuyarak projenin güncel durumunu görebilirsiniz.
> Tüm alanların (A, B, C) kodları entegre edilmiştir.

## Proje Özeti
NASA Space Apps hackathonu: SPHEREx taramasından 5 hedef gökyüzü bölgesinin zaman serisi görüntüleyicisi.
- Repo: `Bhllcoder1/planet-x-sphere`
- Yerel: `C:/Users/Tahir/source/planet-x-sphere`
- Alanlar:
  - **Alan A (Akif)**: Veri işleme boru hattı (`a_veri_isleme/`), maskeler, germe, L0/L1, TAP async.
  - **Alan B (Berk / Furkan)**: Astrometri ve hareket (`b_astrometri/`), Gaia, centroid, ePSF, mover classifier, ışık eğrileri.
  - **Alan C (Osman / newernever)**: Sunucu backend (`c_sunucu/`), önbellek ürünleri, manifest v2, render motoru, Aladin Lite, operasyon/runbook'lar.

---

## Alan C (Sunucu & Altyapı) Tamamlananlar
- 00-10 .. 00-13: Riskler ve sorular dokümanları ✓
- 01-05: c_sunucu/ops/d9_test.py ✓
- 01-06: ops/D9_VM_RUNBOOK.md + c_sunucu/ops/d9_simulate.py + tests/test_d9_simulate.py ✓
- 02-10: c_sunucu/cache/frame_products.py (img/var/flg/cat/geom little-endian binary ürünler) ✓
- 02-11: contracts/manifest.schema.json + contracts/manifest_example.json (Draft 2020-12 v2) ✓
- 02-20: c_sunucu/api/image_renderer.py (tam sayı NN zoom, asinh germe, Okabe-Ito NaN, thumb_64) ✓
- 04-09: c_sunucu/api/skybot.py (IMCCE SkyBoT etiketleme ve çevrimdışı fallback) ✓
- 04-14: c_sunucu/ops/shift_stack_demo.py + ops/SHIFT_STACK_RUNBOOK.md (CPU benchmark & CuPy vast.ai) ✓
- 05-04 / 05-18: raster ve wiseview uyumluluk modülleri ✓
- 05-14: d_site/pages/aladin_panel.html + c_sunucu/api/routes/aladin.py (Aladin Lite v3 context panel) ✓
- 06-01 .. 06-14: FastAPI iskeleti, önbellek katmanı, TAP client, S3 reader, runbook'lar, Docker/Caddy ✓
- 07-01, 07-10, 07-11, 07-12: Test altyapısı, hız testi, yığma testi, regresyon testi ✓
- 11-04 .. 11-13: Hesaplar, session, geçmiş, profil ekranı (/profile/view), share, export, fits_export ✓
- Alan C birim testleri: 45/45 geçti (%100) ✓
- ClickUp: Alan C'ye ait 50/50 görev tamamlandı ✓

---

## Alan B (Astrometri & Hareket) Tamamlananlar
- 00-05: docs/WORK_PROTOCOL.md ✓
- 01-03: b_astrometri/gaia/fetch.py + 13 test ✓
- 03-01: b_astrometri/centroid/epsf.py + 7 test ✓
- 03-02: b_astrometri/centroid/d5_check.py (600 sentetik fit) ✓
- 03-04: b_astrometri/centroid/error_ellipse.py ✓
- 03-05: b_astrometri/centroid/wing_fit.py ✓
- 03-06: b_astrometri/centroid/joint_fit.py (Jacobian düzeltmesi) ✓
- 03-07: b_astrometri/gaia/epoch.py + 11 test ✓
- 03-12 .. 03-15: enjeksiyon/kurtarma, sentetik testler, WiseView epoch doğrulaması ✓
- 04-01 .. 04-03: geçiş gruplama, geçiş yığını (`stacks.py`), zorlanmış fotometri (`forced_phot.py`) ✓
- 04-06 .. 04-08: hareketli bağlama (`linker.py`), OUTLIER terfi (`outlier_candidates.py`), veto guard (`veto_guard.py`) ✓
- 04-10: R24 asteroit sapma analizi raporu ✓
- 04-12: lambda-binli ışık eğrisi modülü ve raporu ✓
- 04-15: kayan pencere ışık eğrisi analizi (`rolling.py`) ✓
- 07-04: T1 tam sayı kayma + T4 WCS gidiş-dönüş testleri (`tests/test_T1.py`, `tests/test_T4.py`) ✓
- 08-01 .. 08-13: Hedef sonuç raporları ve karşılaştırma matrisleri ✓
- 09-06 .. 09-11: Sınırlılıklar ve demo prova modülleri ✓
- 10-11 .. 10-12: Hareket ve spektrum okuma panelleri ✓
- Alan B birim testleri: 89 test OK ✓

---

## Alan A (Veri İşleme) Tamamlananlar
- `a_veri_isleme/` modülleri `main` dalında mevcut ve testleri geçmektedir:
  - `a_veri_isleme/process/pixel.py`
  - `a_veri_isleme/process/masks.py`
  - `a_veri_isleme/process/stretch.py`
  - `a_veri_isleme/fetch/` ve `export/` modülleri
  - 8/8 birim testi yerelde doğrulanmıştır.

---

## Doğrulama Komutları
- Python pytest: `pytest tests/ -v`
- Alan B unittest:
  - `python -m unittest discover -s b_astrometri/centroid -p "test_*.py"`
  - `python -m unittest discover -s b_astrometri/gaia -p "test_*.py"`
  - `python -m unittest discover -s b_astrometri/movers -p "test_*.py"`
  - `python -m unittest discover -s b_astrometri/motion -p "test_*.py"`
