# 03-04 Uygulama Raporu — Hata Elipsi

**Durum:** Yerel prototip tamamlandı; H-04 (02-07 gerçek yıldız kesitleri) bekleniyor.

## Uygulanan

`b_astrometri/centroid/ellipse.py` modülü üç ana işlev içerir:

**`error_ellipse(cov, k)`** — 2×2 kovaryans matrisinden k-sigma hata elipsi parametrelerini hesaplar.
- Girdi: `[[sxx, sxy], [sxy, syy]]` (piksel²), skalar k (örn. 1.0 veya 2.0)
- Çıktı: büyük yarı eksen `a`, küçük yarı eksen `b`, `theta` (x ekseninden radyan, (-π/2, π/2]), `sig_x`, `sig_y`, `rho`, `coverage`
- Yöntem: `np.linalg.eigvalsh` ile öz değer ayrıştırması; θ için `atan2(2sxy, sxx-syy)/2`
- 2B Gauss'ta 1σ elipsin gerçek kapsamı **%39.3** (1D %68 değil); `coverage_probability(k) = 1 − exp(−k²/2)`

**`catalog_fields(cov)`** — katalog JSON alanlarını üretir:

| Alan | Tanım |
|---|---|
| `sig_x`, `sig_y` | Marjinal standart sapmalar (piksel) |
| `rho` | Korelasyon katsayısı |
| `a1`, `b1`, `theta` | 1σ elips büyük/küçük yarı eksen ve açı |
| `a2`, `b2` | 2σ elips (kesikli çizgi; `theta` aynı) |

**`position_catalog_record(x, y, covariance, ...)`** — tam konum kaydı üretir:
- Merkez (x, y) + iki kovaryans bileşeni: `centroid_uncertainty` ve `wcs_correction_uncertainty` (03-09)
- `independent_errors=True` ile toplam kovaryans hesaplanır; aksi hâlde `total_status = "not_combined_independence_not_declared"`
- Koordinat çerçevesi (`parent_native_pixel` / `cutout_native_pixel`), birim (`pixel^2`) ve piksel başlangıcı (0) açıkça beyan edilir

## Doğrulama

- Sentetik 2×2 kovaryans matrisleriyle `catalog_fields` çıktılarının native float olduğu doğrulandı (12 ondalık basamak korunuyor)
- `coverage_probability(1.0) ≈ 0.3935`, `coverage_probability(2.0) ≈ 0.8647` matematiksel olarak doğru
- Negatif köşegen, simetrik olmayan matris ve k ≤ 0 için ValueError fırlatıldığı test edildi
- 03-06 1000-deneme kapsamı: ortak uyumda 1σ elipsin **%40.04** kapsama sağladığı doğrulandı (beklenen %39.35)

## Açık kalan

- **H-04**: 02-07 gerçek izole yıldız kesitleri ile konum belirsizliği ve akı doğrulaması
- **03-09** WCS düzeltme kovaryansı mevcut olmadığından `total_uncertainty` alanı şimdilik `null`
- Gök çerçevesine dönüşüm (RA/Dec kovaryansı) kare başına roll açısı gerektirir; henüz uygulanmadı
- 03-06 ile ortak uyum sonrası tam kovaryans entegrasyonu üretimde açık
