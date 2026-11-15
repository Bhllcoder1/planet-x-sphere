# 03-05 Doymuş Çekirdek Kanat Uyumu — Uygulama Raporu

**Durum:** Yerel prototip tamamlandı; H-05 (02-08/03-03 gerçek görüntü yolu) bekleniyor.

**Dosya:** `b_astrometri/centroid/wing_fit.py`

---

## Uygulanan Şeyler

### `valid_pixel_mask()`

Üç koşulu birleştiren piksel maskesi:
- `IMAGE` ve `VARIANCE` sonlu (`np.isfinite`)
- `VARIANCE > 0`
- Flags verilmişse: `(flags & bad_flags) == 0`

`DEFAULT_BAD_FLAGS = 0x3C028E44 | OVERFLOW(bit1) | DICHROIC(bit7) | GHOST(bit22-24) | STREAK(bit25)` — `forced_phot.py`'deki tanımla uyumlu.

### `fit_epsf_wing()`

**Girdiler:** ePSF grid, piksel koordinat ızgaraları (xx, yy), görüntü, varyans, başlangıç konumu (x_init, y_init), isteğe bağlı flags ve bad_flags.

**Çekirdek maskesi:** `r² ≤ core_radius_px²` (varsayılan 1.5 px). Bu bölgede geçersiz piksel varsa `saturated_fit = True` rozeti verilir; uyum yine de kanat pikselleriyle devam edebilir.

**Erken çıkış koşulları:**
- Maskelenmiş piksel oranı > 0.5
- Geçerli piksel sayısı < 6

Her iki durumda `status = "unmeasurable"` döner.

**Uyum:** `scipy.optimize.least_squares` ile 4 parametre: (x, y, flux, background). Ağırlıklar `1/√var`. Sınırlar: (x,y) piksel ızgarasına kenetlendi, flux ≥ 0.

**Kovaryans:** `(JᵀJ)⁻¹` tersinden 2×2 xy bloğu alınır, `catalog_fields()` ile hata elipsine çevrilir (03-04 ile aynı rutin).

**Çıktı sözlüğü:**
```
status, saturated_fit, x, y, flux, background, chi2_nu,
n_valid, masked_fraction, sigma_x, sigma_y, rho_xy,
ellipse_a, ellipse_b, ellipse_pa_deg
```

---

## Doğrulama

Sentetik testler (`b_astrometri/centroid/test_wing_fit.py` — ayrı dosya):

| Test | Açıklama | Sonuç |
|------|----------|-------|
| Çekirdeksiz Gauss | Tüm pikseller geçerli, merkez kurtarımı | ≤0.05 px [NV gerçek FITS'te] |
| Doymuş çekirdek | 1.5 px içi NaN, kanatla uyum | `saturated_fit=True`, konum yakınsadı |
| Aşırı maskeleme | masked_fraction > 0.5 | `unmeasurable` döndü |
| Az piksel | n_valid < 6 | `unmeasurable` döndü |

[ASSUMPTION] Merkez kurtarım doğruluğu gerçek SPHEREx FITS görüntüleriyle doğrulanmadı.

---

## Açık Kalan İşler

| ID | Konu |
|----|------|
| H-04 | 02-07 gerçek izole yıldız kesitlerinin yolu → 03-02 ve 03-05 üretim testi |
| H-05 | 02-08/03-03 çıktı yolu → gerçek doymuş çekirdekli görüntü doğrulaması |

Gerçek FITS olmadan:
- `core_radius_px = 1.5` eşiği kalibre edilmedi
- Parlak yıldızlarda kanat/çekirdek sınırı gözlemsel olarak belirlenmedi
- `chi2_nu` eşiği (bad_fit kritik değeri) test edilmedi

---

## Teknik Notlar

- Koordinatlar hiçbir zaman yuvarlanmıyor; `int(x+0.5)` veya `round()` yok — coord-audit uyumlu.
- `flags` None geçilebilir (flags-sız mod); bu durumda yalnızca NaN/inf maskeleme uygulanır.
- `least_squares` başarısızlığı (tekil Jacobian) `unmeasurable` olarak yakalanır — çökmez.
- `catalog_fields()` doğrudan 03-04 hata elipsi rutinini çağırır; iki modül arasında senkronizasyon gerekmiyor.
