# 03-13 Piksel-Faz Sapma Eğrisi

Tarih: 2026-11-15
Durum: Sentezik sweep kodu tamamlandı; gerçek FITS H-06/H-07 bekliyor.

## Ne Yapıldı

`b_astrometri/centroid/phase_bias.py` içinde `run_phase_sweep` ve
`write_phase_bias_csv` fonksiyonları.

03-12 T2 düzeneğini uygular: bilinen sub-piksel fazında yıldız enjekte et,
`fit_epsf_wing` ile geri kazan, ortalama sapma ve RMS/σ_tahmin oranını ölç.

## Sweep Parametreleri

| Parametre | Varsayılan | Açıklama |
|-----------|-----------|----------|
| phases | 0.0, 0.05, … 0.95 (20 nokta) | Sub-piksel faz değerleri |
| snr_levels | (20, 50, 100) | Her faz için SNR seviyeleri |
| n_trials | 200 | Gürültülü tekrar sayısı (her faz×SNR) |
| seed | 2026 | Tekrarlanabilirlik |
| noise_sigma | 1.0 | Piksel gürültü σ |

## Ölçülen Metrikler

Her (SNR, faz) çifti için:

| Alan | Açıklama |
|------|----------|
| bias_x_px, bias_y_px | Ortalama konum sapması (px) |
| rms_x_px, rms_y_px | RMS konum hatası (px) |
| sigma_pred_x/y_px | Kovaryans tahmini ortalaması |
| rms_over_sigma_x/y | Kalibrasyon oranı (ideal: 1.0) |
| passed_t2_t3 | SNR>50 için T2/T3 kriteri (bias<0.02 px, 0.8≤ROS≤1.25) |

## T2/T3 Geçiş Kriteri

SNR > 50 olduğunda değerlendirilir:
- `|bias_x| < 0.02 px` ve `|bias_y| < 0.02 px`
- `0.8 ≤ rms/sigma_pred ≤ 1.25` (her iki eksen için)

SNR ≤ 50 için `passed_t2_t3 = None` (bilgi; kriter uygulanmaz).

## Çıktı Formatı

`write_phase_bias_csv(rows, path)` ile CSV; sütunlar:
`snr, phase, n_ok, bias_x_px, bias_y_px, rms_x_px, rms_y_px,`
`sigma_pred_x_px, sigma_pred_y_px, rms_over_sigma_x, rms_over_sigma_y, passed_t2_t3`

## Mevcut Durum

Sentezik ızgara çalışacak biçimde tamamlandı; gerçek SPHEREx ePSF FITS
veya gerçek yıldız kesitleri olmadan üretim değerleri hesaplanamaz.

## Açık Noktalar

| ID | Konu |
|----|------|
| H-06 | Piksel-faz bias eğrisi için gerçek SPHEREx FITS ePSF (dedektör/bant başına) |
| H-07 | 03-13 gerçek veri çıktısı yolu |
| — | `unit_norm` normalizasyonu yaklaşık; bias eğrisi DR1 ePSF ile farklılaşabilir |

## Kullanılan Dosyalar

- `b_astrometri/centroid/phase_bias.py` — sweep ve CSV yazıcı
- `b_astrometri/centroid/wing_fit.py` — uyum motoru (03-05)
