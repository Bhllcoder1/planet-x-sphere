# Display layer design (gösterim katmanı) - 2026-11-14

Etiketler: [V] gerçek koşuyla doğrulandı, [NV] doğrulanmadı, [ASSUMPTION] varsayım.

## 1. Veri: "Veritabanımız ne? Aladin Lite mı?"

Kısa cevap: **Aladin Lite veritabanı değildir**; tarayıcıda gökyüzü haritası çizen bir kütüphanedir, bir şey saklamaz. Verimiz üç yerde durur: (1) NASA arşivi (asıl kaynak), (2) sunucudaki önbellek **dosyaları** (görüntüler), (3) küçük bir **SQLite** dosyası (yalnız hesaplar ve geçmiş). Pikseller SQL'e girmez.

```
[ARŞİV - bizim değil]
 IRSA TAP (kare listesi, ~200 s, bazen 502) [V s0_B]   IRSA S3 nasa-irsa-spherex (FITS, 61-65 MB/kare) [V]
 Gaia DR3 TAP (yıldız konumları)                       SkyBoT (asteroitler, sonra)
        |  yalnız sunucu çağırır; tarayıcı asla (SITE_SPEC §3 kural 5)
        v
[SUNUCU - kiralık VM]
 L0  kare listesi dosyaları (TAP satırları; demo için dondurulmuş)        [V: Barnard 357-358 kare]
 L1  ham pencere: IMAGE/VARIANCE/ZODI float32, FLAGS u32, byte-offset map  ~4.2 GB Barnard [arith v3]
 L2  ürünler: img.f32 var.f32 flg.u32 cat.json geom.json manifest.json      KB'lar/kare
 Pipeline (astropy, photutils): maske, WCS düzeltme, ePSF centroid, Gaia eşleme -> L2
 Gösterim fonksiyonu (Python): PNG + thumbnail üretir (dosya)
 SQLite (WAL): users, sessions, searches, examined  (+ thumbnail dosya yolu)  [ASSUMPTION, SITE_SPEC 2a]
        |  HTTPS (Caddy, zstd), JSON + ikili float32
        v
[TARAYICI]
 Kendi viewer'ımız: Canvas2D veya WebGL2 (05-01 dama tahtası testi seçer) = ANA YOL
 Shader: clip -> asinh -> invert -> renk; overlay'ler float koordinatta
 (Sonra, isteğe bağlı) Aladin Lite yan paneli: sadece geniş alan bağlamı (05-14)
        |
        v
[ÇIKTILAR] PNG (8 bit, gösterim kopyası) | CSV (ölçüm, L2'den) | FITS kesit (sonra) | paylaşım linki (URL)
```

| Şey | Nerede yaşar | Durum |
|---|---|---|
| Ham görüntü | IRSA S3; biz L1'e kopyalarız | S3 range okuma çalışıyor [V s0_B]; in-region hız [NV] (D9) |
| Kare listesi | L0 dosyası | TAP 3/6 hedefte başarısız [V s0_A] |
| Ölçüm (konum, akı) | L2 cat.json | henüz üretilmedi [NV] |
| Hesaplar, geçmiş | SQLite tek dosya | [ASSUMPTION]; yedek 11-10 |
| Ekran görüntüsü | tarayıcı belleği (texture) | — |
| Aladin Lite | tarayıcıda harita kütüphanesi | **veritabanı değil**; HiPS karolarını dış sunuculardan çeker [NV] -> kural 5 ile çelişir (soru 3) |

Aladin neden ana yol değil: SIP "not well tested" [V notes_viewer]; görüntüyü gök küresine yeniden izdüşürür, "1 px kayma = tam z ekran pikseli" garantisi yok.

## 2. Gösterim işleme (display processing)

**Temel kural:** ölçüm verisi (float32 MJy/sr, L2) asla değişmez; gösterim bir **kopya** üzerinde çalışır. CSV/centroid gösterim ayarından girdi almaz (hash testi, 02-18/02-19).

### 2.1 Adımlar

| # | Adım | Formül / kural | Varsayılan | Nerede |
|---|---|---|---|---|
| 1 | Ham veri | v = IMAGE (float32), NaN korunur | — | sunucu gönderir |
| 2 | Maske (yalnız limit hesabı için) | limit hesabından çıkar: NaN + fit mask `0x3C028E44` + OVERFLOW | açık | tarayıcı / sunucu |
| 3 | Arka plan görünümü | `raw` = v; `zodi` = v − ZODI; `flat` = v − ZODI − m_k (m_k = karenin background-mask'li sigma-clip medyanı) | `zodi`, rozetli (soru 1) | shader |
| 4 | Clip limitleri | `percent`: lo = P0.5, hi = P99.5; **tüm blink dizisinde aynı dedektör grubu için ortak** hesaplanır | percent 0.5/99.5, ortak | sunucu manifest'e yazar; tarayıcı özel değerde yeniden hesaplar |
| 5 | Normalize | x = clamp((v' − lo)/(hi − lo), 0, 1); hi = lo ise x = 0 | — | shader |
| 6 | asinh | y = asinh(x/a) / asinh(1/a) (astropy AsinhStretch) | a = 0.1 | shader |
| 7 | Invert | y = 1 − y | kapalı | shader |
| 8 | Renk | gri LUT (256 girişli doku); ikinci gamma yok (sRGB tuzağı, 02-17) | gri | shader |
| 9 | NaN | griden ayrı sabit renk (Okabe-Ito mavi), lejantta "veri yok (NaN)" | açık | shader |
| 10 | Çıkış | ekran; PNG = aynı Python fonksiyonu, tam sayı z, NEAREST; thumbnail 160x160 | — | ekran: tarayıcı; PNG/thumbnail: sunucu |

Neden **ortak limit**: kare başına limit blink'te sahte titreşim yaratır ve RW Aur / R Dra değişkenliğini gizler. "Kare başına" anahtar olarak kalır (05-17).

Barnard'ın NaN çekirdeği (2x2, IMAGE ve VARIANCE) [V s0_B]: limit hesabına girmez; NaN rengiyle çizilir (beyazla doldurmak "normal yıldız" izlenimi verir); "saturated-fit" rozeti; centroid ePSF kanat fitiyle (C.7).

### 2.2 5 hedef için varsayılanlar (hepsi aynı ayar; alan başına el ayarı yok)

| Hedef | Beklenen görünüm | Not |
|---|---|---|
| Barnard's Star | parlak, NaN çekirdek | ortak percent + a=0.1 yeterli [ASSUMPTION; Q-H3 ekran görüntüsü onaylar] |
| ε Indi B | parlak ε Indi A yanında | hi değerini A belirler; B soluk kalabilir; zscale anahtarı [NV] |
| WISE 0855 | soluk, belki görünmez | uzun λ dedektörleri (D5/D6); görünmüyorsa kart bunu söyler |
| RW Aur, R Dra | değişen yıldız | ortak limit zorunlu; çekirdek doygunluğu [NV] |

### 2.3 Tarayıcıya giden veri

Kare başına: img.f32 + zodi.f32 + flg.u32 (var.f32 okuma paneli için isteğe bağlı), little-endian, Caddy zstd.

| Pencere | Kare başına | Barnard 358 kare |
|---|---|---|
| 31x31 (SITE_SPEC varsayılanı) | 3 x 3.8 KB = 11.5 KB | ~4.1 MB [arith] |
| 64x64 (v3 Day 1) | 3 x 16 KB = 48 KB | ~17.6 MB [arith] |
| 8 bit PNG alternatifi (64², yalnız thumbnail/PNG) | 4 KB | ~1.5 MB |

zstd kazancı float gürültüde küçük olabilir [ASSUMPTION]; 07-11 (D14) ölçer. Float32 neden: slider anında tepki verir, veri yeniden inmez.

### 2.4 WiseView'den alınan / alınmayan (image_parsing.py, flash3.js)

| WiseView | Karar |
|---|---|
| fixed / percent / adapt clip modları, AsinhStretch, invert, min-max kutuları [V kod] | **Alınır** (isim ve UI); birim MJy/sr'a uyarlanır |
| `complex()`: lo = max(min(arr), −250) | **Alınmaz**: min aykırı piksele duyarlı; −250 WISE birimi |
| asinh sonrası `rescale_intensity(out_range)` yeniden normalize | **Alınmaz**: içerikle değişir, kareler arası tutarlılığı bozar |
| `find_outlier_pixels` / `simple()`: sıcak pikseli medyanla değiştirir | **Alınmaz** varsayılanda; 02-18 etiketli, varsayılan kapalı (11/17 asteroitte OUTLIER [V s0_D]) |
| `shrink()` (adapt, Scharr kenar ağırlıklı) | **Şimdi değil**; "auto" yerine zscale |
| Sunucuda 8 bit PNG üretip tarayıcıda drawImage (flash3.js ~930, ~721) [V] | Yalnız PNG/thumbnail için; etkileşim float32 + shader |
| unwise_cutout.py: `wcs_world2pix` (SIP yok), int() ile yuvarlama | **Alınmaz**: biz `all_world2pix`, float konum |

## 3. Otonomi ve küçük model

### 3.1 Kural ile otomatik olabilenler (model gerekmez)

| İş | Otomatik kural | Durum |
|---|---|---|
| Stretch limitleri | ortak percent 0.5/99.5, maskeli; sabit dosya `display_defaults.json` | tasarım [ASSUMPTION] |
| Maskeler | 2 profil (centroid / mover) sabit bitlerle | sayılar [V s0_D] |
| Mod seçimi | N sadece aynı dedektör ve r_edge·θ_res ≤ 0.25 px; değilse R-k + tek satır sebep | kural v3 §2.2; Barnard D2'de çoğu zaman R-k [V s0_A] |
| Hedef ölçümü | tahmini konumda forced-fit (tespit şart değil) | kural |
| Kare kalitesi | fit-mask > %50 -> "astrometri için kullanılmaz"; kalabalık alan -> linking kapalı | eşikler [ASSUMPTION] |
| Aday vetoları | STREAK/GHOST/CROSSTALK -> sebep kodu, silme yok | 04-08 |

### 3.2 Küçük ML modeli nerede değer katar

| Fikir | Etiketli veri gerçekte | Boyut | Hüküm |
|---|---|---|---|
| Real/bogus (mover adayı) | pozitif: **17** SkyBoT asteroiti, 3 kare [V s0_D]; negatif: binlerce statik yıldız, time-scrambled sahte izler (04-11), STREAK bileşenleri (2-16/kare); sentetik enjeksiyon (07-14) | ~20 özellikli gradient boosting (<1 MB) veya ~50k parametreli CNN (15x15 x 3 kare) | **Sonra.** 17 pozitif ile eğitim + dürüst test imkânsız. SkyBoT'u ~100 seyrek kareye genişletmek birkaç yüz pozitif verir [ASSUMPTION ~7-10 V<18/kare]; alan/tarih bazlı ayrık test seti; kural skorunu aynı yanlış-iz oranında geçemezse gönderilmez |
| Streak/ghost dedektörü | pipeline STREAK bayrağı var ama gürültü yakınında eksik [V s0_D p.18]; GHOST bu karelerde ~yok | — | **Model değil**, gerekirse Hough çizgi kuralı |
| Auto-contrast modeli | — | — | **Hiç**: deterministik percentile açıklanabilir; model kareler arası tutarsızlık = sahte blink |
| AI upscaling | — | — | **Düşürüldü** (sahte nokta en kötü hata) |

Riskler: (a) **dağılım kayması**: OUTLIER 2025 karelerinde %1.7-2.1, 2026'da ~0 [V s0_D]; bunu öğrenen model sessizce bozulur. (b) sahte güven: kalibre olmayan skor yanıltır. (c) sızıntı: aynı asteroit hem eğitimde hem testte. (d) kalabalık alan: 0/4 tespit [V]. Kural: model **sadece sıralar**, aday silmez; "ML skoru (deneysel)" etiketiyle.

Öneri: **şimdi** veri toplama kancası (aday stamp + özellik + etiket kaydı, 04-06..04-09); **sonra** model (mover finder slice 4 ve 04-11 yanlış-iz oranı çıktıktan sonra); auto-contrast ve upscaling **hiç**.

### 3.3 Otonomi merdiveni

| Seviye | Anlam | 5 gün |
|---|---|---|
| 0 manuel | her hedefte kullanıcı limit, mod, maske seçer | hayır |
| 1 kural varsayılanları | tek ayar dosyası, 5 hedef aynı; otomatik mod/maske/limit/forced-fit; kullanıcı yalnız isterse değiştirir | **evet, hedef bu** |
| 2 otomatik pipeline + QC | toplu koşu, kalite rozetleri, aday listesi + vetolar, otomatik kontak sayfası | kısmen: QC + kontak sayfası; mover adayları slice 4 (MCD dışı) |
| 3 tam otomatik | ML skorlu sınıflama, insan kontrolü yok | hayır (veri yok) |

## 4. ClickUp değişiklikleri

| Id | Değişiklik |
|---|---|
| 02-15 | Bu dokümandaki adım tablosu + "ortak limit" + NaN rengi + ZODI istisnası kararı eklenir |
| 02-16 | `scope=sequence|frame` parametresi (varsayılan sequence, dedektör grubu); WiseView son re-normalize yok; limitler maskeli pikselden |
| 02-17 | Altın teste ortak-limit ve NaN-renk girdisi; LUT dokusu |
| 02-19 | ZODI varsayılanı soru 1'e bağlanır; `flat` (kare medyanı) seçeneği eklenir |
| 02-20 | Thumbnail dosya olarak (SQLite'ta blob değil); tEXt'e `display_ver` |
| 05-14 | "Veritabanı değil" + HiPS dış çağrısı kural 5 istisnası/proxy kararı |
| 05-17 | "kare başına / ortak" anahtarı; "Varsayılan (auto)" düğmesi `display_defaults.json`'dan |
| 04-06..04-09 | Her aday için stamp + özellik + etiket kaydı (`candidates_log`); 04-07: OUTLIER özelliğine R27 uyarısı |
| 04-11 | Time-scrambled izler negatif etiket olarak saklanır |
| 11-06 | `searches` satırına çözülmüş lo/hi (MJy/sr), clip modu, `display_ver` |
| 11-23 | Thumbnail 02-20 yolundan |

Yeni görevler:
- N1 `display_defaults.json` + otomatik QC geri dönüşü (ör. zscale) - Sonnet
- N2 5 hedef için otomatik kontak sayfası (regresyon ekran görüntüleri) - Haiku
- N3 SkyBoT etiketli eğitim setini ~100 seyrek kareye genişletme (sonra) - Sonnet
- N4 Real/bogus GBDT temel modeli vs kural skoru, alan bazlı test (sonra) - Sonnet kod, Opus kapı kararı

## 5. Kullanıcıya sorular

1. **ZODI çıkarma gösterimde varsayılan açık olsun mu?** ("piksel değiştiren adım varsayılan kapalı" kuralına istisna.) Varsayılan: **evet**, rozetle; yoksa arka plan kareler arası zıplar.
2. **Stretch limitleri tüm dizi için ortak mı, kare başına mı?** Varsayılan: **ortak** (dedektör grubu başına).
3. **Aladin Lite paneli tarayıcının dış sunuculardan harita çekmesine izin verirse kabul mü?** Varsayılan: **demoda panel yok**; sonra proxy ile.
4. **Küçük ML modeli demoda olmasın, veri toplansın, sonra mı?** Varsayılan: **sonra**; demo seviye 1 + kısmi seviye 2.
