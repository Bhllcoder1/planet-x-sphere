# 03-04 — konum merkezli cat.json elips kaydı

`centroid/ellipse.py` içindeki eski `error_ellipse` / `catalog_fields` API'leri
korunur. Yeni `position_catalog_record` tek gerçek float konumu, 1σ/2σ merkezli
elipsleri ve ayrı hata bütçelerini JSON uyumlu sözlükte toplar.

## Girdi sözleşmesi

```python
record = position_catalog_record(
    x_native, y_native, centroid_covariance_xy,
    frame_id=frame_id,
    coordinate_frame="parent_native_pixel",  # veya cutout_native_pixel
    covariance_unit="pixel^2",
)
```

Konum 0 tabanlı native float'tır; yuvarlanmaz, gök veya gösterim pikseline
çevrilmez. Kovaryans (x,y) sırasında sonlu, simetrik, pozitif yarı tanımlı 2×2
matristir. Kare kimliği ve koordinat/kovaryans birimi zorunludur. Gök (arcsec²)
veya farklı karedeki matris sessizce bu kayda eklenmez; dönüşüm upstream yapılır.

WCS belirsizliği varsa ayrı `wcs_correction` girdisi şunları taşır:
`covariance`, `frame_id`, `coordinate_frame`, `covariance_unit`. Kare/çerçeve/birim
centroid ile aynı olmalıdır. Sadece `independent_errors=True` açık beyanıyla
Σ_total=Σ_centroid+Σ_correction hesaplanır; aksi halde iki hata ayrı kalır ve
`total_status` neden toplam olmadığını açıklar. Çapraz kovaryans veya bağımsızlık
kanıtı bu işlev tarafından üretilmez.

## Çıktı

- `x/y`, kare ve birim/eksen metadata'sı.
- `centroid_uncertainty`, `wcs_correction_uncertainty`, `total_uncertainty`
  ayrı bloklar; bulunmayan WCS/total değeri `null` olur, sıfır uydurulmaz.
- Her mevcut blokta `covariance`, `sig_x`, `sig_y`, `rho`, `a1/b1/theta`,
  `a2/b2`, ayrıca merkezi x/y içeren `1sigma` ve `2sigma` elipsleri.
- θ radyan ve native +x'ten +y yönündedir. 1σ düz, 2σ kesikli çizgi metadatası
  vardır; roll/ekran dönüşümünü arayüz aynı koordinat dönüşümüyle uygulamalıdır.
- Tam-rank iki boyutlu Gauss varsayımındaki nominal kapsam 1σ için yaklaşık
  %39,3, 2σ için %86,5'tir; tek boyutlu %68 değildir. Dejenere kovaryansın
  nominal kapsamı `null` ve `degenerate_covariance=True` olur.

## Kabul durumu

Kullanıcının isteği gereği **yeni test eklenmedi, test/derleme/deneme
çalıştırılmadı**. Bu ek API sadece kaynak incelemesiyle hazırlandı; yeni
üretim entegrasyonunun çalıştığı iddia edilmez. Mevcut sentetik analitik/Monte
Carlo testleri bu oturumda yeniden koşturulmadı ve yeni kayıt API'sini doğrulamaz.
Gerçek 03-03 kovaryansı, varsa 03-09 WCS düzeltme kovaryansı ve gerçek cat.json
yazıcısına bağlanması bekler. Görev veya ClickUp kapanışı yapılmadı.
