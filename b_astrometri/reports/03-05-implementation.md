# 03-05 Doymuş Çekirdek Kanat Uyumu Uygulaması

Tarih: 2026-11-15
Durum: Sentezik test geçiyor; gerçek FITS H-05 bekliyor.

## Ne Yapıldı

`b_astrometri/centroid/wing_fit.py` içinde `fit_epsf_wing` fonksiyonu ile
doymuş çekirdek pikseller maskelenirken kanat piksellerinden ePSF uyumu yapılır.

## Tasarım Kararları

### Çekirdek Doyma Algılama

Çekirdek tanımı: başlangıç konumuna ≤ `core_radius_px` (varsayılan 1.5 px) uzaklık.
Çekirdek içinde herhangi bir piksel geçersiz (NaN, OVERFLOW veya kötü bayrak) ise
`saturated_fit: true` rozeti verilir; uyum yine de yapılır, kanat piksellerinden.

### Ölçülemez Durum

İki koşuldan birinde `status: "unmeasurable"` döner:
- Tüm piksel setinde maskelenmiş oran > 0.5
- Geçerli piksel sayısı < 6

### Uyum Parametreleri

`least_squares` ile 4-parametre uyum: (x, y, flux, bg).

| Parametre | Açıklama |
|-----------|----------|
| x, y | Piksel konumu (başlangıç: x_init, y_init) |
| flux | Model genliği (≥0 sınır) |
| bg | Sabit arka plan |

Ağırlıklar: `inv_std = 1 / sqrt(var)` (χ² = Σ res² / (n-4)).
Yakınsama: xtol=ftol=gtol=1e-10, x_scale="jac".

### Kovaryans ve Hata Elipsi

J^T J tersinden 2×2 xy kovaryans alınır; `catalog_fields(cov_xy)` ile
1σ elips parametreleri elde edilir (03-04 modülünden).

Jacobian tekil (LinAlgError) ise `unmeasurable` döner.

## Çıktı Alanları

| Alan | Durum |
|------|-------|
| status | "ok" / "unmeasurable" |
| saturated_fit | Çekirdek içinde maskelenen piksel var mı |
| x, y | Uyulan konum |
| flux, background | Uyulan parametreler |
| chi2_nu | Normalize χ² |
| n_valid, masked_fraction | Piksel istatistikleri |
| + ellipse alanları | catalog_fields çıktısı (semi_a, semi_b, pa_deg, …) |

## Sınırlamalar

- Gerçek SPHEREx FITS olmadan bağımsız doğrulama yapılamaz (H-05).
- `x_scale="jac"` Levenberg-Marquardt benzeri yakınsama; ciddi doyma durumunda
  konverjans garantisi yoktur.
- Çekirdek yarıçapı (1.5 px) sabit; bant veya dedektöre göre optimizasyon henüz yapılmadı.
- bg sabit alındı; uzamsal gradyan modellenmedi.

## Açık Noktalar

| ID | Konu |
|----|------|
| H-05 | 02-08/03-03 çıktı yolu; gerçek görüntü doğrulaması için gerekli |
| — | Çekirdek yarıçapı bant/dedektöre göre parametre olabilir |

## Kullanılan Dosyalar

- `b_astrometri/centroid/wing_fit.py` — `fit_epsf_wing`, `valid_pixel_mask`
- `b_astrometri/centroid/ellipse.py` — `catalog_fields` (03-04)
