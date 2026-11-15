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
| **T1 — Tam sayı kayma** | `07-04` | Gerçek yerel kesitte ePSF yıldızı `(x,y)` ve `(x+1,y)` konumlarına enjekte edilir; ayrıca kesit `np.roll` ile 1 px kaydırılır. Ekran kontrolü yakınlaştırma `z = 1, 4, 16, 64` değerlerinde yapılır. | Sayısal: ölçülen `Δx` ve `|Δx−1|`. Ekran: görünen yer değiştirme eksi `z` ekran pikseli. | Parlak kaynakta `Δx = 1,000 ± 0,005 px`; ekran sapması her `z` için tam `0 px`. `z` büyütmedir, fiziksel enjeksiyon kayması değildir. |
| **T2 — Alt-piksel merdiveni** | `07-05` | `0,1, 0,2, …, 0,9` px konum kaymaları; yalnız `SNR > 50` sonuçları kabul hesabına girer. | Her faz ve eksen için ortalama konum yanlılığı `bias(faz)`; grafik ve tablo (`03-13`). | Her fazda ve eksende `|bias| < 0,02 px`, yalnız `SNR > 50` için. `SNR = 50` eşiği karşılamaz. |
| **T3 — Enjeksiyon / kurtarma** | `07-05` | Aynı gerçek `VARIANCE` gürültüsü üstüne rastgele faz ve akılı `N = 2000` ePSF yıldızı; gerçek varyans gürültüsü kullanılır. | Her SNR diliminde ortalama yanlılık/faz, `RMS`, `σ_tahmin`, `RMS / σ_tahmin` ve SNR’a göre tamlık eğrisi. | Her raporlanan SNR diliminde `RMS / σ_tahmin ∈ [0,80, 1,25]`; T2 yanlılık sınırı `SNR > 50` dilimlerinde uygulanır. |
| **T4 — WCS gidiş-dönüş** | `07-04` | Rastgele ve köşe 0-tabanlı piksel koordinatları `(x, y)` | `piksel → gök → piksel` geri dönüş hatası `dr` | `max(dr) < 1e-4 px` |

## 3. Zorunlu Çıktı Şeması (Özet Tablo)

Her test koşusu aşağıdaki alanları içeren bir JSON raporu üretir. Uygulanmayan metrikler `null` yazılır; T1/T4 için enjeksiyon veya SNR dilimi yoktur. T2 kayıtları faz ve eksen, T3 kayıtları SNR dilimi bazında ayrılır:
- `test_id` (`"T1"`..`"T4"`), `n_injected`, `snr_bin`, `phase_px`, `axis`, `mean_bias_px`, `rms_px`, `sigma_pred_px`, `rms_over_sigma`, `max_error_px`, `passed` (`bool`).
- T1 `max_error_px` alanı `|Δx−1|`; T2 `mean_bias_px` alanı faz ve eksen başına ortalama bias; T3 `rms_over_sigma` alanı SNR dilimi başına orandır; T4 `max_error_px` alanı en büyük piksel dönüş hatasıdır. `passed`, ilgili satırın kendi eşiğini karşılamasını belirtir.
- Karşılaştırma notu: Anderson & King (2000) HST için `0,002 px` en iyi durumu bildirir; SPHEREx ePSF için bu sayı önsel hedef alınmaz, ölçülerek raporlanır.
