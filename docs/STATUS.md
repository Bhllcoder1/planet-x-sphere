# Proje Durumu

> Son güncelleme: 2026-11-15
> Etiketler: **[V]** = bu çalışmada doğrulandı · **[NV]** = doğrulanmadı · **[ASSUMPTION]** = planda varsayılan olarak belirlendi

---

## Stage 0: Veri Araştırması

| Alan | Durum | Notlar |
|---|---|---|
| Barnard TAP (async + sync) | ✅ | 358 kare, 3 geçiş (pass 0/1/2), tüm 6 dedektör [V: s0_A] |
| ε Indi A TAP | ✅ | 460 kare, 4 geçiş, tüm 6 dedektör [V: s0_A] |
| ε Indi B TAP | ✅ | 458 kare, 4 geçiş, tüm 6 dedektör [V: s0_A] |
| WISE 0855 TAP | ❌ | Sync zaman aşımı 400 s, HTTP 502; async iş kuyruğa girdi, 10+ dk QUEUED kaldı; SIA qr3 boş döndü; kare sayısı bilinmiyor [V: s0_A §Retry] |
| RW Aur TAP | ❌ | Sync zaman aşımı, HTTP 502; async denenmedi (süre aşıldı); kare sayısı bilinmiyor [V: s0_A §Retry] |
| R Dra TAP | ❌ | Sync zaman aşımı, HTTP 502; async denenmedi (süre aşıldı); kare sayısı bilinmiyor [V: s0_A §Retry] |
| S3 anonim byte-range okuma | ✅ | 30/30 pencere başarılı; p50 3.9 s, p95 12.7 s (4 HDU, 1 MiB readahead) — Ankara'dan ölçüm [V: s0_B] |
| S3 FLAGS .section sıkıştırılmış okuma | ✅ | 100×100 int32 dizisi döndü, tam olarak cutout çıktısına eşit [V: s0_B] |
| Kesit (cutout) servisi | 🔶 | 503: 5/14 istek (servis meşgul); başarılı istekler p50 12.4 s; fallback olarak tutuldu [V: s0_B] |
| Parent-piksel kuralı (merkez) | ✅ | Barnard D2, 1 kare; cutout A ve B, S3 100×100 penceresi — centroid farkı < 2.3×10⁻¹³ px [V: s0_B §4] |
| Parent-piksel kuralı (kenar/diğer dedektörler) | ❌ | Yalnızca bir kare, bir dedektör, merkez bölge; kenar ve D1/D3-D6 test edilmedi [NV] |
| Mask profilleri: s0_D doğrulaması | ✅ | Fit mask 0x3C028E44; centroid ve mover-search profilleri veriyle sabitlendi [V: s0_D] |
| Mask profilleri: kalabalık alan (gc) | 🔶 | gc3'te PERSIST %66.5 → kullanılamaz; SOURCE gc karelerinde %100 → arka plan maskesi çöküyor [V: s0_D] |
| Mover tespiti (seyrek kareler) | 🔶 | 17/25 bilinenin 3 seyrek karede tespit edildi; kalabalık (gc) karede 0/4 tespit [V: s0_D §3] |
| Mover'da OUTLIER bayrağı davranışı | ✅ | 11/17'si OUTLIER'lı, 6/17'si yalnızca SOURCE; fit mask hiçbir mover çekirdeğini yok etmedi [V: s0_D §3] |
| WCS-Gaia astrometri (aberasyon testi) | ✅ | 3 kare (A, B, C, dedektör 1); Gaia'ya medyan kayma 0.025–0.03 px; aberasyon vektörü WCS'e emilmiş [V: s0_C] |
| ESA Gaia TAP (kare B, C) | 🔶 | HTTP 500 ve bağlantı sıfırlamaları; B ve C için MAST TAP'a geçildi; ESA ile karşılaştırma kare A'da doğrulandı [V: s0_C §2] |
| HDU düzeni ve anahtar türetme | ✅ | uri'den `ibe/data/spherex/` çıkarılır → S3 anahtarı; HDU sırası: IMAGE=1, FLAGS=2, VARIANCE=3, ZODI=4, EPSF=5, WCS-WAVE=6 [V: s0_B §1] |
| Roll / SPS_EPA tarama | ✅ | Barnard D2: pass içi yayılma 0.72–1.42°; ε Indi D3: 1.08–3.84°; ters geçiş farkı 180°'den 0–7.8° sapıyor [V: s0_A] |
| Bölge-içi (us-east-1) zamanlama D9 | ❌ | Henüz test edilmedi; Türkiye'den ölçüm yukarı sınırdır [NV] |

---

## Alan A: Veri Entegrasyonu ve Görüntü İşleme

| Bileşen | Durum | Görev |
|---|---|---|
| Ortam (venv, photutils, sep) | ❌ | 01-01 |
| Async TAP istemcisi (WISE 0855 / RW Aur / R Dra) | ❌ | 01-02 |
| Donmuş kare listeleri (5 hedef L0) | ❌ | 01-09 |
| Bayt-ofset haritası (HDU başlık/veri, L1) | ❌ | 01-10 |
| Barnard 358 kare prefetch betiği | ❌ | 01-11 |
| Sorgu adımı (async TAP + L0 önbelleği) | ❌ | 02-01 |
| Pencere getirme (birleştirilmiş row-range, 4 HDU paralel) | ❌ | 02-02 |
| Piksel kuralları modülü (C.3) | ❌ | 02-03 |
| Mask profilleri (C.4, iki profil) | ❌ | 02-04 |
| Arka plan (C.5, sabit üst-piksel ızgarası) | ❌ | 02-05 |
| Tüm-kare tespit (C.6, DAOStarFinder) | ❌ | 02-07 |
| Doymuş/NaN çekirdek işleme | ❌ | 02-08 |
| L1 önbelleği (bayt-ofset haritası + anahtar şeması) | ❌ | 02-12 |
| Gösterim işleme katmanı tasarımı | ❌ | 02-15 |
| Germe ve kırpma modülü (Python ref: fixed/percent/adapt/zscale+asinh) | ❌ | 02-16 |
| Aynı germe tarayıcıda + altın test | ❌ | 02-17 |
| ZODI/arka plan çıkarma (yalnız gösterim) | ❌ | 02-19 |
| display_defaults.json ve otomatik kalite geri dönüşü | ❌ | 02-22 |
| Kare başı ürün dosyaları (img/var/flg/cat/geom) | ❌ | 02-10 |
| Manifest şeması v2 | ❌ | 02-11 |
| PNG ve küçük resim üretimi (tam sayı yakınlık + NN) | ❌ | 02-20 |
| Ölçüm tablosu CSV şeması | ❌ | 11-12 |
| Dışa aktarım şeması (gösterime hazır ürünler) | ❌ | 11-03 |

---

## Alan B: Astrometri ve Hareketli Cisim Bilimi

| Bileşen | Durum | Görev |
|---|---|---|
| ePSF modeli (GriddedPSFModel, örnekleme 5, 33×33) | ❌ | 03-01 |
| ePSF normalleştirme ve yönelim kontrolü | ❌ | 03-02 |
| Merkezleme uyumu (x, y, F, b + kovaryans) | ❌ | 03-03 |
| Hata elipsi (1σ/2σ, JSON alanları) | ❌ | 03-04 |
| Doymuş çekirdek kanat uyumu | ❌ | 03-05 |
| Gaia DR3 sorgusu ve epoğa taşıma | ❌ | 03-07 |
| Gaia eşleştirme (KD-ağacı, belirsiz çiftler) | ❌ | 03-08 |
| WCS kayma düzeltmesi (held-out RMS, rozet) | ❌ | 03-09 |
| Hareket uyumu (α0, δ0, μα*, μδ, ϖ; geçişler arası) | ❌ | 03-11 |
| Geçiş gruplama (30 gün boşluk, passes.json) | ❌ | 04-01 |
| Zorlanmış ePSF fotometri modülü | ❌ | 04-03 |
| WISE 0855 saptanabilirlik testi | ❌ | 04-04 |
| Hareketli cisim bulucu (hız ızgarası + RANSAC) | ❌ | 04-06 |
| OUTLIER aday terfisi (mover arama profili) | ❌ | 04-07 |
| Piksel-faz sapma eğrisi | ❌ | 03-13 |
| T1 tam sayı kayma testi (sayısal + ekran) | ❌ | 07-04 |
| T2 alt-piksel merdiveni ve T3 enjeksiyon/kurtarma | ❌ | 07-05 |
| Barnard hareketi Gaia ile karşılaştırma | ❌ | 08-03 |
| ε Indi B kapsam tablosu ve tespit sonucu | ❌ | 08-05 |
| WISE 0855 kapsam tablosu ve zorlanmış fotometri | ❌ | 08-07 |
| RW Aur kapsam tablosu ve zorlanmış fotometri | ❌ | 08-09 |
| R Dra kapsam tablosu ve zorlanmış fotometri | ❌ | 08-11 |
| 5 hedef karşılaştırma tablosu | ❌ | 08-13 |
| Okuma paneli ve hareket ölçüm paneli | ❌ | 10-11 |
| Spektrum / ışık eğrisi paneli (RW Aur, R Dra) | ❌ | 10-12 |

---

## Alan C: Sunucu (Backend), Hesaplar, Kiralama

| Bileşen | Durum | Görev |
|---|---|---|
| Bölge-içi zamanlama testi (D9) betiği ve şeması | ❌ | 01-05 |
| D9: kiralanan makinede zamanlama testi | ❌ | 01-06 |
| FastAPI iskeleti (manifest uç noktası) | ❌ | 06-01 |
| L0/L1/L2 önbellek katmanları + byte-offset haritası | ❌ | 06-02 |
| Async TAP istemcisi (async iş, 15 dk tavan, retry/backoff) | ❌ | 06-03 |
| Birleştirilmiş paralel S3 okuyucu (row-block Range GET, 4 HDU) | ❌ | 06-04 |
| Nezaket sınırları (IRSA 4 eşzamanlı, cutout 45 s backoff) | ❌ | 06-05 |
| Saatlik kiralama runbook (bölüm 1: boyut, bölge, güvenlik) | ❌ | 06-07 |
| Kiralama runbook (bölüm 2: D9, prefetch, otomatik kapanış) | ❌ | 06-08 |
| Docker + Caddy dağıtımı (compose, TLS, sıkıştırma) | ❌ | 06-09 |
| Sır yönetimi (.env düzeni, tarama) | ❌ | 06-10 |
| Çevrimdışı yedek (video + ekran görüntüleri) | ❌ | 06-11 |
| API sözleşmesi (OpenAPI) ve sahte sunucu | ❌ | 06-14 |
| Regresyon paketi koşu betiği (tek komut, tek tablo) | ❌ | 07-12 |
| R-k sunucu raster modu (k=4–8 NN, farklı dönüşlü kareler) | ❌ | 05-04 |
| URL parametre şeması (adres çubuğuna durum yazma) | ❌ | 05-10 |
| WiseView uyumlu URL takma adları | ❌ | 05-18 |
| Kullanıcı deposu (≤10 hesap, seed dosyası, parola özeti) | ❌ | 11-04 |
| Giriş, oturum çerezi, HTTPS, hız sınırı | ❌ | 11-05 |
| Arama geçmişi şeması ve otomatik kayıt uç noktası | ❌ | 11-06 |
| Geçmişten URL şemasıyla ayar geri yükleme | ❌ | 11-07 |
| Profil API'si (sayaçlar, son ziyaret, veri izolasyonu) | ❌ | 11-08 |
| Profil ve geçmiş ekranı | ❌ | 11-09 |
| Veritabanı yedekleme ve geri yükleme betiği | ❌ | 11-10 |
| PNG çıktısı (ızgara, işaretçi, rozet gömülü) | ❌ | 11-11 |

---

## Alan D: Site ve Arayüz

| Bileşen | Durum | Görev |
|---|---|---|
| Checkerboard test donanımı D1/T-V1 ve Q-H1 görüntüleri | ❌ | 05-01 |
| Görüntüleyici Mod N (tam sayı yakınlık, NN, piksel ızgarası) | ❌ | 05-02 |
| Blink kontrolleri (oynat/duraklat, hız, adım, yeniden başlat) | ❌ | 05-03 |
| θ_res / ofset rozeti ve Mod N otomatik varsayılan kuralı | ❌ | 05-05 |
| Float konum işaretçileri ve hata elipsleri (4.47 → 447 kuralı) | ❌ | 05-06 |
| Gaia katmanı (MJD'ye taşınmış konumlar) | ❌ | 05-07 |
| Epoch göstergesi (+ − .) ve döngü başı kenarlığı | ❌ | 05-15 |
| Germe arayüzü (kırpma modları, doğrusallık) | ❌ | 05-17 |
| ZODI arka plan anahtarı arayüzde | ❌ | 05-20 |
| T-V1/D1: checkerboard Playwright testi (DPR 1/1.25/2, Chrome+Firefox) | ❌ | 07-02 |
| Kayan nokta konum testi (4.47 zoom 100 → 447 ± 0.5 ekran px) | ❌ | 07-03 |
| Hedef başına son kabul kontrol listesi (5 hedef) | ❌ | 07-13 |
| 5 hedef otomatik kontak sayfası (regresyon ekran görüntüleri) | ❌ | 07-15 |
| ZODI anahtarı testi (ölçüm değişmez, arka plan sıçraması ölçülür) | ❌ | 07-16 |
| Açılış sayfası ve hedef seçici (5 kart + kapsam durumu) | ❌ | 10-02 |
| Koordinat girişi (ondalık + sexagesimal, ad çözümleme) | ❌ | 10-03 |
| FOV seçici ve pencere yeniden isteği | ❌ | 10-04 |
| Blink oynatıcı (kare sayacı dahil) | ❌ | 10-05 |
| Kare başı metadata şeridi (tarih, dedektör, λ, geçiş, sürüm) | ❌ | 10-06 |
| Mod rozeti (N/R-k/S), piksel ızgarası, kesin-piksel modu | ❌ | 10-07 |
| Kontrast ayarı ve tema (asinh/lineer/zscale, koyu/açık) | ❌ | 10-08 |
| Bayrak katmanı (Table 16 bitleri, iki maske profili) | ❌ | 10-09 |
| Gaia katmanı (öz hareket izi) ve centroid işaretleri | ❌ | 10-10 |
| Hedef sonuç kartı ve kapsam/hata durumları | ❌ | 10-14 |
| URL şeması, gömme modu, paylaş/dışa aktar (PNG, CSV) | ❌ | 10-15 |
| Hakkında ve sınırlılıklar sayfası, erişilebilirlik, mobil | ❌ | 10-16 |
| Tasarım belirteçleri (renk, tipografi, boşluk, koyu/açık) | ❌ | 11-16 |
| Tel örgüler (ana ekran, giriş, profil, sonuç; masaüstü + telefon) | ❌ | 11-17 |
| Boş/yükleniyor/hata/kaplama-yok durumları ve metin dosyası | ❌ | 11-18 |

---

## Sunum ve Demo Hazırlığı

| Alan | Durum | Not |
|---|---|---|
| Risk kaydı (R1b, R22, R23) | ✅ | docs/RISKS.md [V: dosya var] |
| Risk kaydı (R24 asteroid 1-3 px) | ❌ | 00-11 |
| Risk kaydı (R25 kalabalık alan, R26 roll, R27 OUTLIER) | ❌ | 00-12 |
| Dürüstlük protokolü ([V]/[NV]/[ASSUMPTION] etiketleri) | ✅ | Tüm Stage 0 raporlarında uygulandı [V] |
| Kesme sırası kararı (ince dilim) | ✅ | DECISIONS_AND_TASK.md'de belgelendi [V] |
| Hedef kapsamı: yarışmanın 5 hedefi | ✅ | Barnard + ε Indi A/B + WISE 0855 + RW Aur + R Dra [V: kullanıcı kararı] |
| Drizzle KAPALI kararı | ✅ | 00-01; kullanıcı onayladı [V] |
| Ekip bölüşümü (4 alan A/B/C/D) | ✅ | TEAM_SPLIT.md; saatler kaba tahmindir [ASSUMPTION] |
| README.md | ❌ | 09-01 |
| Sunum slayt taslağı (8-10 slayt) | ❌ | 09-03 |
| STATUS.md (bu dosya) | ✅ | 09-04 — 2026-11-15 |
| Yarışma kuralları ve gönderim gereksinimleri | ❌ | 09-05 — henüz okunmadı [NV] |
| Sınırlılıklar sayfası | ❌ | 09-06 |
| Teşekkür ve atıf (NASA/IRSA, SPHEREx, Gaia, astropy, photutils) | ❌ | 09-09 |
| Yarışma teslim kontrol listesi | ❌ | 09-10 — 09-05'e bağımlı |
| Birinci prova (kronometreyle) | ❌ | 09-11 |
| 5 dakikalık demo betiği (tıklama yolu) | ❌ | 09-02 |
| Yedek kayıtlı video (canlı demo çökerse) | ❌ | 09-08 |
| İkinci prova + soru-cevap hazırlığı | ❌ | 09-12 |

---

## Özet Sayılar

| Kategori | Toplam görev | ✅ Tamam | 🔶 Kısmi | ❌ Yapılmadı | ⏸ Sonraya |
|---|---|---|---|---|---|
| Stage 0 araştırması | 20 | 12 | 4 | 4 | 0 |
| Alan A (veri + görüntü işleme) | 23 | 0 | 0 | 23 | 0 |
| Alan B (astrometri + bilim) | 25 | 0 | 0 | 25 | 0 |
| Alan C (sunucu + hesaplar) | 24 | 0 | 0 | 24 | 0 |
| Alan D (site + arayüz) | 29 | 0 | 0 | 29 | 0 |
| Sunum + demo hazırlığı | 19 | 7 | 0 | 12 | 0 |
| **Genel toplam** | **140** | **19** | **4** | **117** | **0** |

Genel ilerleme: **19/140 (%14) tamamlandı** — tümü Stage 0 araştırması ve karar kayıtları.
Ürün kodu henüz yazılmadı; demo hazırlığının yalnızca belgeleme adımları bitti [ASSUMPTION: görev sayısı tamlığı].

---

## Kritik Riskler (açık)

| Risk | Önem | Durum |
|---|---|---|
| WISE 0855, RW Aur, R Dra TAP kalıcı başarısız | YÜKSEK | Async TAP yeniden denenmeli; kapsam bilinmiyor [NV] |
| D9 bölge-içi zamanlama: p50 < 1 s / çerçeve hedefi | YÜKSEK | Hiç test edilmedi; Türkiye'den ölçüm 3.9 s [V: s0_B] |
| Kesit servisi %503 oranı (%36) | ORTA | S3 birincil yol; kesit yalnızca fallback [V: s0_B] |
| OUTLIER bayrağı davranışı 2026 karelerinde | ORTA | 2025W51/52'de %1.7-2.1; 2026W12/13'te ~0 [V: s0_D]; neden bilinmiyor [NV] |
| Barnard Yıldızı doymuş çekirdek → centroid zorlanmış | ORTA | Plan: NaN maskeli kanat uyumu; henüz test edilmedi [NV] |
| Son teslim tarihi bilinmiyor | YÜKSEK | Varsayılan: 7 gün [ASSUMPTION: DECISIONS_AND_TASK.md] |
