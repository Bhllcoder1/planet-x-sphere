# 03-12 — Enjeksiyon / Kurtarma Düzeneği Tanımı (`harness_spec.md`)

Bu belge, astrometri ve merkezleme doğruluğunu ölçen **T1–T4** enjeksiyon/kurtarma testlerinin girdi, çıktı ve sayısal kabul ölçütlerini dondurur. Test kodları **07 listesi** (`07-04`, `07-05`) altında yazılır; bu dosya yalnızca spesifikasyondur.

## 1. Sahte Yıldız Üretim Kuralı

- **PSF Kaynağı:** `b_astrometri/centroid/epsf.py` (`EPSFGrid`, `03-01`, 5× örneklenmiş 33×33 damga).
- **Koordinat Sistemi:** 0-tabanlı `float` ebeveyn piksel koordinatı (`0 <= x, y < 2040`); konum asla yuvarlanmaz (`03-14`).
- **Gürültü Modeli:** Poisson (kaynak + arka plan) + `VARIANCE` HDU gürültüsü.
  - Not: `VARIANCE` gerçek saçılımı bir miktar hafife alabildiğinden, T3'te `RMS / σ_tahmin > 1` yönünde hafif sapma beklenebilir.
- **Maske Profili:** Gerçek karelerden alınan `FLAGS` bit maskesi; karşılaştırılabilirlik için `02-04` ile birebir aynı maske profili kullanılır (`[ASSUMPTION]`: `02-04` sözleşmesi gelene kadar sentetik testlerde `FLAGS = 0` temiz piksel varsayılır).
- **Döngüsellik Uyarısı:** Aynı `ePSF` ile üretip aynı `ePSF` ile uydurmak iyimser sonuç verir; bu nedenle bağımsız doğrulama olarak `03-02` kapsamındaki **200 gerçek yıldız** testi ayrıca koşulur (`[ASSUMPTION]`).

## 2. Test Matrisi (T1–T4) ve 07 Listesi Eşleşmesi

| Test | 07 Görevi | Girdi | Çıktı Metrikleri | Sayısal Kabul Ölçütü |
|---|---|---|---|---|
| **T1 — Tam sayı kayma** | `07-04` | Tek parlak yıldız; bilinen `Δ = 1,000` px kaydırma (`z = 1, 4, 16, 64` kontrolü) | Ölçülen kayma `Δ_ölç`, hata `\|Δ_ölç - 1,000\|` | `Δ = 1,000 ± 0,005 px` (parlak kaynak) |
| **T2 — Alt-piksel merdiveni** | `07-05` | `0,1, 0,2, …, 0,9` px faz adımları, `SNR > 50` | Piksel-faz sapma eğrisi `sapma(faz)` (bkz. `03-13`) | `\|sapma(faz)\| < 0,02 px` (tüm fazlarda) |
| **T3 — Enjeksiyon / kurtarma** | `07-05` | Gerçek gürültü (Poisson + VAR) üstüne `N = 2000` enjekte yıldız | Ortalama sapma, `RMS`, `σ_tahmin`, `RMS / σ_tahmin`, `SNR` başına tablo | `RMS / σ_tahmin ∈ [0,80, 1,25]` |
| **T4 — WCS gidiş-dönüş** | `07-04` | Rastgele ve köşe 0-tabanlı piksel koordinatları `(x, y)` | `piksel → gök → piksel` geri dönüş hatası `dr` | `max(dr) < 1e-4 px` |

## 3. Zorunlu Çıktı Şeması (Özet Tablo)

Her test koşusu aşağıdaki alanları içeren bir JSON raporu üretir:
- `test_id` (`"T1"`..`"T4"`), `n_injected`, `snr_bin`, `mean_bias_px`, `rms_px`, `sigma_pred_px`, `rms_over_sigma`, `max_error_px`, `passed` (`bool`).
- Karşılaştırma notu: Anderson & King (2000) HST için `0,002 px` en iyi durumu bildirir; SPHEREx ePSF için bu sayı önsel hedef alınmaz, ölçülerek raporlanır.
