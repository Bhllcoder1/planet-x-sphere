# 03-12 — Enjeksiyon/Kurtarma Düzeneği: Uygulama Raporu

**Durum:** Harness taslağı tamamlandı; gerçek FITS T1-T4 koşusu H-01/H-05 bekleniyor.

Tarih: 2026-11-15

---

## Uygulanan İşler

Enjeksiyon/kurtarma doğrulama çerçevesinin spesifikasyonu `b_astrometri/centroid/harness_spec.md` olarak tamamlandı. Bu belge dört test katmanının (T1–T4) girdi sözleşmesini, kabul ölçütlerini ve JSON çıktı şemasını dondurur. Test kodu **07 listesi** (`07-04`, `07-05`) altında yazılır; bu rapor yalnızca tasarım kararlarını belgeler.

### T1–T4 Test Matrisi

| Test | 07 Görevi | Temel Girdi | Kabul Ölçütü |
|---|---|---|---|
| **T1 — Tam sayı kayma** | 07-04 | Gerçek kesitte ePSF yıldızı `(x,y)` ve `(x+1,y)` konumlarına enjekte | `Δx = 1.000 ± 0.005 px`; ekran sapması z=1,4,16,64 için `0 px` |
| **T2 — Alt-piksel merdiveni** | 07-05 | `0.1, 0.2, …, 0.9` px faz adımları, `SNR > 50` sonuçları | Her fazda `\|bias\| < 0.02 px` (SNR > 50) |
| **T3 — Enjeksiyon/kurtarma** | 07-05 | Rastgele faz/akı, `N = 2000` sentetik yıldız, gerçek VARIANCE gürültüsü | Her SNR diliminde `RMS/σ_tahmin ∈ [0.80, 1.25]` |
| **T4 — WCS gidiş-dönüş** | 07-04 | Rastgele ve köşe piksel koordinatları | `max(dr) < 1e-4 px` |

### PSF Üretim Kuralları

- **PSF kaynağı:** `EPSFGrid` (`03-01`), 5× örneklenmiş 33×33 damga.
- **Koordinat sistemi:** 0-tabanlı `float` ebeveyn piksel; konum asla yuvarlanmaz (`03-14`).
- **Gürültü modeli:** Poisson (kaynak + arka plan) + `VARIANCE` HDU gürültüsü.
- **Maske profili:** Gerçek `FLAGS` bit maskesi; `02-04` sözleşmesi gelene kadar `FLAGS = 0` varsayılır `[ASSUMPTION]`.
- **Döngüsellik uyarısı:** Aynı ePSF ile üretip aynı ePSF ile uydurmak iyimser sonuç verir; `03-02` kapsamındaki 200 gerçek yıldız testi bağımsız doğrulama olarak koşulur `[ASSUMPTION]`.

### JSON Çıktı Şeması

Her test satırı şu alanları içerir: `test_id`, `n_injected`, `snr_bin`, `phase_px`, `axis`, `mean_bias_px`, `rms_px`, `sigma_pred_px`, `rms_over_sigma`, `max_error_px`, `passed`.

Referans: Anderson & King (2000) HST için `0.002 px` en iyi durumu bildirir; SPHEREx ePSF için bu sayı önsel hedef alınmaz, ölçülerek raporlanır.

---

## Doğrulama

| Adım | Durum |
|---|---|
| Spesifikasyon belgesi (`harness_spec.md`) | ✓ Tamamlandı |
| T1 sayısal test kodu (07-04) | ✓ `Δx = 0.998404 px` sentetik doğrulandı |
| T4 WCS gidiş-dönüş testi (07-04) | ✓ Sentetik doğrulandı |
| T2/T3 test kodu (07-05) | — H-05 bekleniyor |
| Gerçek FITS üzerinde T1–T4 | — H-01 (ePSF) ve H-05 (kesit yolu) bekleniyor |

---

## Açık Engeller

- **H-01:** Akif'in `a_veri_isleme` modülü / `02-03` dal yolu gelmeden ePSF gerçek görüntüye uygulanamaz.
- **H-05:** `02-08` / `03-03` çıktı yolu gelmeden T2/T3 gerçek varyans gürültüsüyle koşulamaz.
- **H-11:** 07-04 T1 Playwright ekran kontrolü için D3 100 WCS penceresi bekleniyor.
