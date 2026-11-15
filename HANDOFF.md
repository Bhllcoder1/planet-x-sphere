# Planet XSphere — oturum devri

Son güncelleme: 2026-11-15 (oturum 3). Kalıcı proje hafızası [Second Brain](docs/second-brain/README.md).

## Git durumu

- Depo: `C:/Users/behlu/planet-x-sphere`
- Dal: `b/01-03-gaia-fetch` (PR #1 açık/draft)
- Son commit: `68a4010` — 04-08 veto guard raporu + TASKS.md güncellemesi
- Stage 0 Python: `C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe`
- Depo dışı kanıtlar/FITS: `C:/Users/behlu/reports/`

## Verification commands

```powershell
$py='C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe'
& $py -I -m unittest discover -s b_astrometri/centroid -p 'test_*.py'
& $py -I -m unittest discover -s b_astrometri/gaia     -p 'test_*.py'
& $py -I -m unittest discover -s b_astrometri/movers   -p 'test_*.py'
& $py -I -m unittest discover -s b_astrometri/motion   -p 'test_*.py'
```

**Son çalışma:** centroid 28, gaia 35, movers 11, motion 15 = **89 test OK**

## Tamamlanan işler (commit'e giren)

| Görev | Dosya | Durum |
|---|---|---|
| 00-05 çalışma protokolü | `docs/WORK_PROTOCOL.md` | ClickUp in-progress |
| 08-01 result template | `b_astrometri/reports/hedefler_sablon.md` | ClickUp complete ✓ |
| 01-03 Gaia istemcisi | `b_astrometri/gaia/fetch.py` + 13 test | WCS piksel ölçeği + stream deadline fix |
| 03-07 epoch | `b_astrometri/gaia/epoch.py` + 11 test | Kutup hatası vektörel yöntemle düzeltildi |
| 03-15 WiseView epoch testi | `b_astrometri/gaia/test_epoch_wiseview.py` + 6 test | Barnard 2010 MJD doğrulandı |
| 03-01 ePSF | `b_astrometri/centroid/epsf.py` + 7 test | NaN fix dahil; fiziksel normalizasyon açık |
| 03-02 D5 normalizasyon | `b_astrometri/centroid/` | 600 sentetik fit, max hata ≤0.000514 px |
| 03-04 hata elipsi | `b_astrometri/centroid/` | Prototip; üretim H-04 bekliyor |
| 03-05 kanat uyumu | `b_astrometri/centroid/` | Sentetik test; gerçek FITS yok |
| 03-06 ortak uyum | `b_astrometri/centroid/joint_fit.py` | Jacobian düzeltmesi dahil |
| 03-12 enjeksiyon/kurtarma | `b_astrometri/` | Harness spec; gerçek veri H-01/H-05 |
| 04-01 geçiş gruplama | `b_astrometri/` | Barnard 358/3, ε Indi B 458/4 sentetik |
| 04-02 geçiş yığını | `b_astrometri/motion/stacks.py` | 9 test; H-03/H-08 bekleniyor |
| 04-03 zorlanmış fotometri | `b_astrometri/motion/forced_phot.py` | Sentetik; gerçek WCS/ePSF H-08 bekliyor |
| 04-06 hareketli bağlama | `b_astrometri/movers/linker.py` | Çift-destekli seyrek ızgara; H-10 bekliyor |
| 04-07 OUTLIER terfi | `b_astrometri/movers/outlier_candidates.py` | TRANSIENT bit0/HALO bit28 fix |
| 04-08 veto guard | `b_astrometri/movers/veto_guard.py` | STREAK/GHOST/CROSSTALK veto; H-10 bekliyor |
| 04-12 RW Aur/R Dra | `b_astrometri/reports/` | TAP başarısız; `UNKNOWN` çıktısı |
| 04-15 kayan pencere | `b_astrometri/motion/lightcurves.py` | 8 test; H-03 bekleniyor |
| 07-04 T1/T4 | `b_astrometri/` | Δx=0.998404 px sentetik; H-11 bekleniyor |
| 09-06 sınırlılıklar | `b_astrometri/reports/09-06-sinirliliklar.md` | Taslak; 09-04/08-14 bekleniyor |

## Uygulama raporları (b_astrometri/reports/)

Tüm yerel ✓ görevlerin raporları mevcut:
01-03, 03-01, 03-02, 03-04, 03-05, 03-06, 03-07, 03-12, 03-13, 03-14, 03-15,
04-01, 04-02, 04-03, 04-06, 04-07, 04-08, 04-10, 04-12, 04-15, 09-06

## İnsan girdisi bekleyenler (H-xx)

| ID | Konu | Bloke eden görevler |
|---|---|---|
| H-01 | Akif'in 02-03/02-12 dal/klasör yolu | 03-01/03-07 üretim entegrasyonu, 03-12/03-14 |
| H-03 | Liste 02 kare manifesti + `SPS_EPA` şeması | 04-01 prod, 04-06, 04-15 |
| H-04 | 02-07 gerçek izole yıldız kesitlerinin yolu | 03-02 prod, 03-05 |
| H-05 | 02-08/03-03 çıktı yolu | 03-05 gerçek görüntü doğrulaması |
| H-08 | Liste 03 ePSF/WCS + Liste 02 maskeler yolu | 04-03 gerçek akı ölçümü |
| H-09 | WISE 0855 List 01 kapsam sonucu | 04-04 |
| H-10 | Gerçek asteroid kataloğu + WCS (≥3 kare) | 04-06/04-08 gerçek doğrulama |
| H-11 | 07-04 D3 gerçek 100 WCS penceresi + Playwright | 07-04 T1 ekran |
| H-12 | RW Aur/R Dra List 01 + 04-03 flux çıktısı | 04-12 prod |

## Önkoşulsuz yapılabilecekler

Tüm önkoşulsuz yerel işler tamamlandı. Kalan eylem maddeleri yalnızca H-xx insan
girdisi gerektirir. Yeni oturum H-xx yanıtlarından birini alırsa o blok açılır.

Graphify çıktısı: `graphify-out/.graphify_labels.json` + `graphify-out/GRAPH_REPORT.md` ✓

## Önemli notlar

- ClickUp kişisel token: `C:\Users\behlu\Desktop\tokeeeeen.txt` (pk_ ile başlar; commit etme)
- Graphify çıktısı `graphify-out/` depoda değil, yerel türetilmiş — commit etme.
- TypeSafe Jev skill: `.agents/skills/typesafe-ai/` kurulu; kodda LLM yok.
- Yerel `reports/` ve FITS dosyaları depoya eklenmez (CONTRIBUTING.md kural 5).
- coord_audit.py: `round()`, `math.floor/ceil/trunc`, `np.rint()`, `origin=1` WCS yasak.
- `a_veri_isleme` modülü Akif'in (H-01); forced_phot.py'de try/except fallback var.
