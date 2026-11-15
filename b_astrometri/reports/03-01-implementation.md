# 03-01 ePSF Model Uygulaması

Tarih: 2026-11-15
Durum: Sentezik self-recovery doğrulandı; fiziksel normalizasyon H-01 bekliyor.

## Ne Yapıldı

`b_astrometri/centroid/epsf.py` içinde `EPSFGrid` sınıfı ile SPHEREx ePSF modellerini
yükleyip bölgeye göre sorgulayan bir arayüz oluşturuldu.

### EPSFGrid Sınıfı

FITS HDU'dan ePSF örneklerini okur:

- **Desteklenen sürümler:** Yalnızca açıkça belirtilmiş QR3 ve DR1 ürünleri.
- **Sürüm kontrolü:** Pipeline 6.5.6 öncesi reddet (eksen sırası düzeltmesi öncesi).
- **DETCOORD/ORDERING doğrulaması:** `sky` ve `x-fast then y` zorunlu.
- **Örnekleme:** 5×5 (OVSMPY/OVSMPX header çifti); diğerleri hata.
- **Izgara şekli:** 33×33 piksel örnekleri;
  - Dedektör 3: 451 bölge (11×41 ızgara)
  - Diğer dedektörler (1,2,4,5,6): 441 bölge (21×21 ızgara)
- **NaN koruması:** Örnekler ve bölge merkezleri için `np.isfinite` kontrolü;
  negatif/sıfır toplam reddet.
- **Normalizasyon:** `PSF_NORM=1.0` örneklerin saklanan değerlerini korur;
  fiziksel akı normalizasyonu 03-02'ye açık bırakıldı.

### Bölge Sorgulama

`zone_at(x_parent, y_parent)`:
- 0-tabanlı ebeveyn koordinatlar, 2040×2040 sınır içi zorunlu.
- En yakın bölge: Öklid uzaklığı minimum (`np.argmin`), ızgara enterpolasyonu yok.

`model_at(x_parent, y_parent, interpolation=...)`:
- `nearest`: Tek bölge `ImagePSF` döner.
- `bilinear`: `GriddedPSFModel.copy()` tüm ızgarayı destekler.

### FITS Ekseni Notu

`fits.open` Astropy aracılığıyla FITS x-hızlı örnekleri `[y, x]` olarak sunar;
`GriddedPSFModel(NDData(self.samples))` bu düzeni doğrudan kabul eder.
Eksen takası yapılmaz.

## Self-Recovery Testi

`recovery_check(grid)` gürültüsüz kendi kendini test eder:

- 3 ayrı kesir ofset çifti dener: (0.0, 0.0), (0.1, 0.9), (0.7, 0.3).
- `least_squares` ile (x, y, F) uyum, xtol/ftol/gtol=1e-12.
- Referans: 123.0 birim model genliği.

| Metrik | Sonuç |
|--------|-------|
| Maksimum konum hatası | < 0.001 px (eşik) |
| Maksimum göreli genlik hatası | < 0.001 (eşik değil, bilgi) |
| Fiziksel akı doğrulanmış | Hayır — `physical_flux_validated: false` |

Gerçek FITS olmadan bağımsız yönelim/akı doğrulaması yapılmadı.

## Açık Noktalar

| ID | Konu |
|----|------|
| H-01 | 02-03/02-12 dal yolu; üretim entegrasyonu için gerekli |
| — | Fiziksel normalizasyon (topam=1 veya piksele dönüştürme) 03-02'de ele alınacak |
| — | Bilinear enterpolasyonun sınır bölgelerde tutarlılığı test edilmedi |
| — | Gerçek kare/FITS olmadan D3 (11×41) ızgara doğrulaması yapılamaz |

## Kullanılan Dosyalar

- `b_astrometri/centroid/epsf.py` — sınıf ve self-recovery
- `b_astrometri/centroid/test_epsf.py` — 7 birim test (NaN fix dahil)
