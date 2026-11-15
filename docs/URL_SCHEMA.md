# URL Parametre Şeması

> Görev 05-10 çıktısı.  
> Tüm görüntüleyici durumu URL parametrelerinde saklanır; bu sayede bağlantı paylaşımı tam yeniden oluşturma sağlar.

---

## 1. Temel URL Yapısı

```
https://{domain}/?{parametreler}
```

Örnek:

```
https://spherex-viewer.example.com/?target=barnard&view=rk&clip=zscale&blink=true&blink_ms=500&zodi=true
```

Tüm parametreler isteğe bağlıdır; belirtilmeyenler kendi varsayılan değerlerini kullanır. `[V]`

---

## 2. Parametreler Tablosu

| Parametre | Tipi | Varsayılan | Açıklama |
|---|---|---|---|
| `target` | string | `"barnard"` | Hedef kimliği: `barnard`, `eps_indi_b`, `wise0855`, `rwaur`, `rdra` |
| `frame` | string | — | Kare kimliği; boşsa ilk kullanılabilir kare gösterilir |
| `x` | int | `0` | Görüntü penceresinin sol üst köşesinin x konumu (piksel) |
| `y` | int | `0` | Görüntü penceresinin sol üst köşesinin y konumu (piksel) |
| `w` | int | `100` | Pencere genişliği (piksel) |
| `h` | int | `100` | Pencere yüksekliği (piksel) |
| `view` | enum | `"n"` | Görüntü modu: `n` = N-shift, `rk` = R-k raster, `s` = Stack |
| `clip` | enum | `"zscale"` | Kırpma modu: `fixed`, `percent`, `adapt`, `zscale` |
| `clip_lo` | float | — | Alt kırpma sınırı; yalnızca `clip=fixed` ile geçerlidir |
| `clip_hi` | float | — | Üst kırpma sınırı; yalnızca `clip=fixed` ile geçerlidir |
| `stretch` | enum | `"linear"` | Renk germe: `linear`, `log`, `asinh` |
| `blink` | bool | `false` | Blink modunu açar (`true`) veya kapatır (`false`) |
| `blink_ms` | int | `500` | Blink hızı (milisaniye); `blink=true` olmadan görmezden gelinir |
| `zodi` | bool | `true` | ZODI çıkarma; `true` = çıkarma açık, `false` = ham veri `[V]` |
| `hdu` | enum | `"image"` | Gösterilen HDU katmanı: `image`, `flags`, `variance`, `zodi` |
| `pass` | int | — | Geçiş filtresi; boşsa tüm geçişler dahil edilir |
| `det` | string | — | Dedektör filtresi: `D1`–`D6`; boşsa tüm dedektörler dahil edilir |

### Parametre Notları

- **`view`** `[V]` — Üç mod DECISIONS_AND_TASK.md'de onaylanmıştır: `n` (N-shift),
  `rk` (R-k raster), `s` (Stack). `rk`, WCS uyumu zayıf olduğunda `n`'ye tercih edilir.
- **`clip`** `[V]` — `zscale` varsayılan olarak seçilmiştir; `fixed` modunda `clip_lo` ve
  `clip_hi` birlikte sağlanmalıdır.
- **`clip_lo` / `clip_hi`** `[ASSUMPTION]` — Değer birimi FITS data-unit'tir
  (MJy/sr veya instrüman sayım birimi); görev 05-10 kapsamı dışında kesinleştirilmedi.
- **`stretch`** `[ASSUMPTION]` — `linear`, `log`, `asinh` seçenekleri yaygın astronomi
  görüntüleyici geleneğine dayanmaktadır; DECISIONS_AND_TASK.md'de açıkça listelenmemiştir.
- **`blink_ms`** `[V]` — Varsayılan değer 500 ms, DECISIONS_AND_TASK.md'deki blink modu
  tartışmasından alınmıştır.
- **`zodi`** `[V]` — ZODI çıkarma varsayılan olarak açıktır; durum arayüzde rozet ile
  gösterilir. Ham/zodi/flat ayrımı tam olarak belirtilmemiş olduğundan tek bool olarak
  şematize edilmiştir. `[ASSUMPTION]`
- **`hdu`** `[ASSUMPTION]` — FITS dosyasının standart uzantılarından türetilmiştir;
  kesin HDU adları veri pipeline görevlerine bağlıdır.
- **`pass`** `[ASSUMPTION]` — Tamsayı geçiş indeksi; birden fazla geçiş filtrelemek
  için virgülle ayrılmış liste sözdizimi kabul edilebilir (görev 05-10 dışında).
- **`det`** `[ASSUMPTION]` — `D1`–`D6` aralığı SPHEREx dedektör mimarisine dayanmaktadır;
  görsel adlar görev 05-10 kapsamı dışında kesinleşmemiştir.

---

## 3. Hedef Kimlik Referansı

| `target` Değeri | Resmi Hedef Adı |
|---|---|
| `barnard` | Barnard's Star |
| `eps_indi_b` | Epsilon Indi B |
| `wise0855` | WISE 0855−0714 |
| `rwaur` | RW Aurigae |
| `rdra` | R Draconis |

Varsayılan hedef `barnard`'dır. `[V]` — Beş hedef DECISIONS_AND_TASK.md'de rekabet
kapsamı olarak onaylanmıştır.

---

## 4. WiseView Alias'ları (Görev 05-18)

WiseView kaynaklı URL'ler bu şemada karşılık bulan parametrelere çevrilir. `[NV]` —
WiseView'ın canlı Lambda'sı mevcut değildir; alias eşleşmeleri kamuya açık WiseView
kaynak kodundan çıkarılmıştır (`sources_wiseview/`).

| WiseView Parametresi | Bu Şemadaki Karşılık | Notlar |
|---|---|---|
| `ra` | `x`, `y` ile birlikte hesaplanır | WCS → piksel dönüşümü gerektirir |
| `dec` | `x`, `y` ile birlikte hesaplanır | WCS → piksel dönüşümü gerektirir |
| `size` | `w`, `h` | WiseView boyut birimi onaylanmamış `[ASSUMPTION]` |
| `band` | `hdu` | WiseView band numarası → HDU adına çevrilir |
| `speed` | `blink_ms` | WiseView hız birimi → ms çevirisi kesinleşmedi `[ASSUMPTION]` |
| `minbright` | `clip_lo` | `clip=fixed` olarak ayarlanır |
| `maxbright` | `clip_hi` | `clip=fixed` olarak ayarlanır |

> Alias çevirisi, bir WiseView URL'si tespit edildiğinde otomatik olarak uygulanır.
> Çevrilemeyen WiseView parametreleri yoksayılır ve bir konsol uyarısı üretilir.
> `[ASSUMPTION]`

---

## 5. Örnek URL'ler

### Barnard's Star — R-k modu, blink açık, zscale kırpma

```
?target=barnard&view=rk&clip=zscale&blink=true&blink_ms=500&zodi=true
```

### WISE 0855 — Stack modu, sabit kırpma, ZODI kapalı

```
?target=wise0855&view=s&clip=fixed&clip_lo=-0.5&clip_hi=5.0&zodi=false
```

### Epsilon Indi B — N-shift modu, logaritmik germe, D3 dedektörü

```
?target=eps_indi_b&view=n&clip=zscale&stretch=log&det=D3
```

### RW Aurigae — Belirli geçiş, asinh germe, blink kapalı

```
?target=rwaur&view=rk&clip=percent&stretch=asinh&pass=2&blink=false
```

### R Draconis — Varsayılan ayarlarla minimum URL

```
?target=rdra
```

---

## 6. Durum Kodlama Kuralları

- Boolean parametreler `true` / `false` dizesi olarak kodlanır (büyük/küçük harf
  duyarsız ayrıştırılır). `[ASSUMPTION]`
- Float parametreler standart noktalı gösterimde iletilir; virgüllü yerel biçimler
  reddedilir.
- Bilinmeyen parametre adları yoksayılır; bu sayede WiseView alias'ları güvenle geçebilir.
- Parametre değerleri standart URL yüzde-kodlaması ile kodlanmalıdır.
- Fragment (`#`) bu şema tarafından kullanılmaz; varsa yoksayılır. `[ASSUMPTION]`

---

## 7. Etiket Sözlüğü

| Etiket | Anlamı |
|---|---|
| `[V]` | Doğrulanmış — DECISIONS_AND_TASK.md veya başka bir birincil kaynak tarafından desteklenmektedir |
| `[NV]` | Doğrulanmamış — Dış kaynaktan alınmıştır; bağımsız doğrulama yapılmamıştır |
| `[ASSUMPTION]` | Varsayım — Görüntüleyici geleneklerinden veya bağlamdan çıkarılmıştır; kesinleştirilmesi gerekebilir |
