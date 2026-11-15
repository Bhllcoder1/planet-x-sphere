# 03-07 Uygulama Raporu: Gaia DR3 Sorgusu ve Epoğa Taşıma

**Durum:** Yerel prototip tamamlandı; 02-03 entegrasyonu ve 3 px dışlama bölgesi H-01 bekleniyor.

Tarih: 2026-11-15

---

## Görev Tanımı

Gaia DR3 kaynaklarını seçmek ve konumları referans epoğundan (2016.0 TCB) gözlem çerçevesi MJD'sine taşımak. Taşıma iki aşamadan oluşur: (1) baryosentrik uzay hareketi (öz hareket + paralaks mesafe + radyal hız), (2) gözlemcinin yerinden gelen geometrik paralaks kayması.

---

## Uygulanan Fonksiyonlar

### `select_calibrators(catalogue)`

Gaia DR3 kalibrasyon yıldızı seçimi:

- **RUWE ≤ 1.4** — çift/ayrılmamış yıldız reddi
- **G ≥ 9** — doymuş çekirdek reddi
- **pmra, pmdec, parallax** sonlu olmak zorunda
- Belirsiz/maskelenmiş değerler kalite kontrolden **geçmiş gibi** değil, reddedilmiş olarak işlenir
- Dönüş: (seçilmiş_tablo, özet_sözlük) — reddedilme nedeni sayımları çakışabilir
- **[AÇIK]** 3 px hedef-dışlama bölgesi uygulanmadı; hedef WCS ve koordinat sözleşmesi (H-01) bekleniyor

### `space_motion(ra_deg, dec_deg, pmra, pmdec, parallax, ref_epoch, mjd_utc, *, radial_velocity_kms)`

Baryosentrik konum taşıması:

- Astropy `SkyCoord.apply_space_motion()` kullanır
- Referans epoğu: Julian yıl TCB (`format="jyear", scale="tcb"`)
- Çerçeve zamanı: MJD UTC (`format="mjd", scale="utc"`)
- Paralaks mesafesi: `1000 / max(parallax_mas, 0.05)` pc — 0.05 mas taban (Stage 0'dan miras, açık bırakıldı)
- Girdi doğrulama: maskelenmiş veya sonlu olmayan herhangi bir değer `ValueError` fırlatır

### `parallax_offsets(ra_deg, dec_deg, parallax_mas, observer_au)`

Birinci-mertebe tanjant-düzlemi gözlemci paralaksı:

```
dra*cos(dec) = π * (X*sin(α) - Y*cos(α))
ddec        = π * (X*cos(α)*sin(δ) + Y*sin(α)*sin(δ) - Z*cos(δ))
```

- `observer_au`: ICRS XYZ AU (yer varsayılanı: Astropy builtin efemeris)
- Sapma değerleri mas cinsinden döner (tabloya yazılır, koordinata eklenmez)

### `propagate_catalogue(catalogue, mjd_utc, *, radial_velocity_kms, observer_au=None)`

Tam boru hattı (katalog → taşınmış tablo):

1. `space_motion()` → baryosentrik RA/Dec
2. Kartezyen yön vektörü hesabı — **vektörel yöntem** (her iki kutup yakınında koşullu olarak iyi)
3. Gözlemci konumu çıkarma → normalize edilmiş yön → `arctan2`/`arcsin` ile geri-dönüşüm
4. Çıktı tablosu alanları:

| Alan | Açıklama |
|------|----------|
| `ra_bary_deg` | Baryosentrik RA (gözlemci paralaksı yok) |
| `dec_bary_deg` | Baryosentrik Dec |
| `ra_deg` | Son konum (baryosentrik + gözlemci kayması) |
| `dec_deg` | Son konum |
| `parallax_dra_cosdec_mas` | RA paralaks kaydırması (kayıt için) |
| `parallax_ddec_mas` | Dec paralaks kaydırması |
| `distance_parallax_mas` | Mesafe hesabında kullanılan paralaks (taban uygulandı) |
| `radial_velocity_kms` | Girdi yayılımı |

---

## Doğrulama

### Birim Testleri: 35 test OK

Test modülleri:
- `b_astrometri/gaia/test_epoch.py` — temel birim testleri
- `b_astrometri/gaia/test_epoch_wiseview.py` — 03-15 WiseView karşılaştırma testleri

### 03-15 WiseView Epoğ Testi (6 test)

Barnard Yıldızı (Gaia DR3: source_id 4472832130942575872) üzerinde:

| Test | Sonuç |
|------|-------|
| 2010 MJD'de konum sonlu ve geçerli | ✓ |
| WiseView (2016.0 katalog) konumundan >10″ uzakta | ✓ (gerçek kayma ~50″) |
| Doğrusal PM yaklaşımıyla uyum < 0.600″ | ✓ |
| 2010'da Barnard güneyde ve doğuda (pmra<0, pmdec>0) | ✓ |
| Baryosentrik RA/Dec alanları dolu | ✓ |
| Meta kayıtta MJD kaydedildi | ✓ |

**Kutup hatası düzeltmesi:** Orijinal skaler arcsin/arccos yaklaşımı kutup bölgelerinde kararsızlaşıyordu. `np.linalg.norm` + vektör normalizasyonu + `arctan2`/`arctan2(z, hypot(x,y))` yöntemiyle ikinci türden kutup tekilliği giderildi.

---

## Açık Maddeler

| Madde | Önkoşul |
|-------|---------|
| 3 px hedef-dışlama bölgesi (`select_calibrators` içinde) | H-01: Akif'in 02-03 dal/klasör yolu |
| `fetch.py` / `epoch.py` üretim entegrasyonu | H-01 |
| Öz hareketi bilinmeyen kaynaklar için NaN politikası belgelenmeli | — |
| Paralaks taban değeri (0.05 mas) Stage 0'dan miras; gözden geçirilmeli | — |

---

## Dosyalar

| Dosya | Değişiklik |
|-------|-----------|
| `b_astrometri/gaia/epoch.py` | Yeni modül — tüm fonksiyonlar |
| `b_astrometri/gaia/test_epoch.py` | Birim testler |
| `b_astrometri/gaia/test_epoch_wiseview.py` | 03-15 WiseView doğrulama testleri |
