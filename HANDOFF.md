# Planet XSphere — oturum devri

Son güncelleme: 2026-11-15. Kalıcı proje hafızası [Second Brain](docs/second-brain/README.md).

## Git durumu

- Depo: `C:/Users/behlu/planet-x-sphere`
- Dal: `b/01-03-gaia-fetch` (PR #1 açık/draft)
- Latest feature-branch/PR head must be read from GitHub; commit IDs in historical notes may be older.
- Stage 0 Python: `C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe`
- Depo dışı kanıtlar/FITS: `C:/Users/behlu/reports/`

## Verification commands (not run in current batch)

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
| 00-05 çalışma protokolü | `docs/WORK_PROTOCOL.md` | ClickUp kapalı değil |
| 08-01 result template | `b_astrometri/reports/hedefler_sablon.md` | ClickUp complete; live status verified |
| 01-03 Gaia istemcisi | `b_astrometri/gaia/fetch.py` + 13 test | 4xx fix dahil; ClickUp kapalı değil |
| 03-07 epoch | `b_astrometri/gaia/epoch.py` + 11 test | Kutup hatası vektörel yöntemle düzeltildi |
| 03-15 WiseView epoch testi | `b_astrometri/gaia/test_epoch_wiseview.py` + 6 test | Barnard 2010 MJD doğrulandı |
| 03-01 ePSF | `b_astrometri/centroid/epsf.py` + 7 test | NaN fix dahil; fiziksel normalizasyon açık |
| 03-02 D5 normalizasyon | `b_astrometri/centroid/` | 600 sentetik fit, max hata ≤0.000514 px |
| 03-04 hata elipsi | `b_astrometri/centroid/` | Protip; üretim H-04 bekliyor |
| 03-05 kanat uyumu | `b_astrometri/centroid/` | Sentetik test; gerçek FITS yok |
| 03-06 ortak uyum | `b_astrometri/centroid/joint_fit.py` | Jacobian düzeltmesi dahil |
| 04-01 geçiş gruplama | `b_astrometri/` | Barnard 358/3, ε Indi B 458/4 sentetik |
| 04-03 zorlanmış fotometri | `b_astrometri/centroid/` | Sentetik; gerçek WCS/ePSF H-08 bekliyor |
| 04-06 hareketli bağlama | `b_astrometri/movers/linker.py` | Sentetik; gerçek asteroid H-10 bekliyor |
| 04-07 OUTLIER terfi | `b_astrometri/movers/outlier_candidates.py` | TRANSIENT bit0/HALO bit28 fix |
| 04-12 RW Aur/R Dra | `b_astrometri/reports/` | TAP başarısız; `UNKNOWN` çıktısı |
| 07-04 T1/T4 | `b_astrometri/` | Δx=0.998404 px sentetik; T1 ekran H-11 bekliyor |
| stacks/kayan pencere | `b_astrometri/motion/stacks.py` | Yeni modül; test var |
| veto-guard düzeltme | `b_astrometri/movers/veto_guard.py` | TRANSIENT/HALO bit düzeltmesi |

## İnsan girdisi bekleyenler (H-xx)

| ID | Konu | Bloke eden görevler |
|---|---|---|
| H-01 | Akif'in 02-03/02-12 dal/klasör yolu (ya da "hazır değil") | 03-01/03-07 üretim entegrasyonu |
| H-03 | Liste 02 kare manifesti + `SPS_EPA` şeması | 04-01 prod, 04-06 |
| H-04 | 02-07 gerçek izole yıldız kesitlerinin yolu | 03-02 prod, 03-05 |
| H-05 | 02-08/03-03 çıktı yolu | 03-05 gerçek görüntü doğrulaması |
| H-08 | Liste 03 ePSF/WCS + Liste 02 maskeler yolu | 04-03 gerçek akı ölçümü |
| H-09 | WISE 0855 List 01 kapsam sonucu | 04-04 |
| H-10 | Gerçek asteroid kataloğu + WCS (≥3 kare) | 04-06 gerçek doğrulama |
| H-11 | 07-04 D3 gerçek 100 WCS penceresi + Playwright | 07-04 T1 ekran |
| H-12 | RW Aur/R Dra List 01 + 04-03 flux çıktısı | 04-12 prod |

## Önkoşulsuz yapılabilecekler (bir sonraki oturumda)

1. ~~`fetch.py` piksel ölçeği varsayımı (6.2″/px → WCS'ten oku)~~ ✓ 2026-11-15
2. ~~`fetch.py` toplam süre sınırı (stream=True + deadline)~~ ✓ 2026-11-15
3. Graphify `finalize()` → `.graphify_labels.json` + `GRAPH_REPORT.md`
4. ~~09-06 sınırlılıklar sayfası taslağı~~ ✓ `b_astrometri/reports/09-06-sinirliliklar.md`
5. ~~`docs/second-brain/TASKS.md` güncelleme: yerel tamamlananları işaretle~~ ✓ 2026-11-15

## Önemli notlar

- ClickUp kişisel token 2026-11-15'te H-02 ile çözüldü; görev durumları güncellendi (08-01 complete; diğerleri in-progress).
- Graphify çıktısı `graphify-out/` depoda değil, yerel türetilmiş — commit etme.
- TypeSafe Jev skill: `.agents/skills/typesafe-ai/` kurulu; kodda LLM yok, cookbook uygulanabilir değil. Canlı API denemesi yapılmadı.
- Yerel `reports/` ve FITS dosyaları depoya eklenmez (CONTRIBUTING.md kural 5).

## Parallel implementation results

04-02 exact-TAN stacks and channel-safe differences:9 focused tests; f32/noise/JSON writer and D10 metrics.04-07 OUTLIER promotion:7 focused tests, movers12/12.04-15 rolling-window inside/outside views and +/-/. roles:8 focused tests.03-06 full covariances, per-frame chi2, strict JSON output and block-sparse Jacobian:4 tests. Real target acceptance remains pending in each task report under b_astrometri/reports/. Resampled variance is explicitly nominal; interpolation covariance is not propagated. The1000trial03-06 coverage runner is being prepared; never claim its results until finished.

## Current ordered integration batch

- Work order:03-14 shared coordinate bridge ->04-03 sky-coordinate forced photometry and CSV ->04-06 velocity lattice and robust linking.
- No new tests added or run, by explicit user instruction. Static source review only; do not claim runtime verification.
- Other-session changes to Gaia fetch/tests and09-06 report may coexist in this shared worktree; do not stage or overwrite them blindly.
- Existing03-06 thousand-trial experiment remains a prior background process, evidence outside repo at reports/03-06-coverage.json; read complete flag before using results.

Ordered batch delivered:03-14 coordinates.py and04-03 forced_phot+CSV pushed in3b02704.04-06 now uses a pair-supported sparse velocity lattice, bounded search and consensus refinement; complete-grid coverage is not claimed. All three task slices were source-reviewed only; user requested no new tests. Real-data/acceptance gates remain open.
