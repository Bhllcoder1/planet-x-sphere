# 03-02 D5: ePSF Normalizasyon ve Yönelim Kontrolü

**Durum:** Yerel prototip tamamlandı; H-04 (02-07 gerçek yıldız kesitleri) bekleniyor.

---

## Uygulanan Değişiklikler

### Normalizasyon çarpanı (`norm`)

`EPSFGrid.__init__` parametresi `norm=PSF_NORM` (varsayılan `1.0`) ile HDU örnekleri
okunduğunda doğrudan ölçeklenir:

```python
self.samples *= norm
self.norm = float(norm)
```

- `norm=1` → ham örnekler korunur (PSF toplamı ≈1 bölge başına).  
- `norm=25` → 5×5 örnekleme ızgarasının piksel başına toplamını ×1'den ×25'e taşır
  (eğer DSF kalibrasyon metadatası bu biçimi gerektiriyorsa).  
- Negatif veya sonlu olmayan `norm` `ValueError` fırlatır.

`norm` değeri `self.norm` alanında tutulur; `forced_phot.py` bu değeri
`epsf_norm_multiplier` çıktı alanına kaydeder.

### Yönelim ve eksen sırası doğrulaması

Yapıcı, HDU başlığını iki zorunlu kontrol için inceler:

| Başlık anahtarı | Beklenen değer | Yanlışsa |
|---|---|---|
| `DETCOORD` | `"sky"` | `ValueError` |
| `ORDERING` | `"x-fast then y"` | `ValueError` |

`ORDERING = "x-fast then y"` anlamı: FITS ikili tablo `EPSF` sütununun bellek düzeni
x ekseni hızlı eksendir; Astropy bunu `[bölge, y, x]` NumPy dizisi olarak
okur (FITS ↔ NumPy boyutu tersine çevirmesi nedeniyle). Bu şekilde
`GriddedPSFModel` ve `ImagePSF` aynı koordinat sistemini kullanır.

Boru hattı sürüm kısıtı (`>= 6.5.6`) bu eksen-sırası düzeltmesinin öncesini dışlar.

### Dosya içi doğrulama: ham toplamlar

Tüm bölgeler için `self.raw_sums = self.samples.sum(axis=(1,2))` önceden hesaplanır
(`norm` ölçeklemesinden önce). Sıfır veya negatif toplam `ValueError` fırlatır.
Ham toplamlar normalizasyon sonrasında tutarlılık kontrolü için erişilebilir kalır.

---

## Sentetik Doğrulama

`recovery_check()` fonksiyonu noiseless öz-tutarlılık testi uygular:

- **600 sentetik fit** (3 konum × 200 gürültüsüz örnekleme):  
  Merkez bölge için `(dx, dy) ∈ {(0,0), (0.1,0.9), (0.7,0.3)}` alt-piksel
  kaymalarına karşı `least_squares` uydurma.
- **Maksimum konum hatası ≤ 0.000514 px** (eşik: 0.001 px).
- Model genlik göreli hatası < 1×10⁻⁶.

Test dosyası `test_epsf.py` ilgili durumları kapsar:

| Test adı | Ne doğrular |
|---|---|
| `test_raw_samples_preserved_and_multiplier_explicit` | `norm=25` → örnekler ×25; `model_at()` aynı ölçekte döner |
| `test_region_selection_and_detector3` | `raw_sums ≈ 1`; bölge sayısı D2:441, D3:451 |
| `test_bilinear_matches_nearest_at_grid_center` | Izgara merkezinde bilinear ≈ nearest |
| `test_rejects_bad_metadata_and_duplicate_grid` | `DETCOORD`, `ORDERING`, `DETECTOR`, `OVSMPX` hataları |
| `test_recovery_check_nan_fails` | NaN koruması `not (x < 0.001)` → doğru |

---

## Fiziksel Akı Kalibrasyonu

`physical_flux_validated: false` tüm çıktılarda işaretlidir. Uyarı:

- Ham örnekler piksel başına yoğunluk birimindedir; ADU → W m⁻² sr⁻¹ μm⁻¹
  dönüşümü boru hattı kalibrasyon adımı (Liste 03) tarafından sağlanmalıdır.
- `norm=1` ile uydurma "model genliği" döner, fiziksel akı değil.
- Hangi `norm` değerinin DR1/QR3 kalibrasyon birimiyle uyumlu olduğu
  H-04 ile gelen gerçek FITS karşılaştırmasına bırakılmıştır.

---

## Açık Maddeler

| ID | Konu |
|---|---|
| H-04 | 02-07 gerçek izole yıldız kesitlerinin yolu; normalizasyon doğrulaması ve yönelim onayı |
| — | `norm` değerinin DR1 kalibrasyon dokümantasyonuyla karşılaştırılması |
| — | Fiziksel akı biriminin `forced_phot` çıktısıyla doğrulanması |

---

*Kayıt tarihi: 2026-11-15. Doğrulama yöntemi: sentetik noiseless fit, gerçek FITS yok.*
