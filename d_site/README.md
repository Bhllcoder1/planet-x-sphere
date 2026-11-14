# Alan D: Site ve arayüz

ClickUp etiketi: `kişi-d`. 50 görev, tahmini 170 saat [ASSUMPTION: ajan tahmini].

Tarayıcı görüntüleyicisi (Mod N, blink, işaretler, bayraklar, gerdirme arayüzü), site sayfaları, UI/UX ve görsel testler.

## Bu klasörün sahibi

`.github/CODEOWNERS` dosyasında bu klasöre bağlı GitHub kullanıcısı. Değişiklik bu kişinin onayıyla birleşir.

## Görevler

| Görev | Süre | Etiket | Ad |
|---|---|---|---|
| 00-02 | 0 h | demo | Karar kaydı: yapay zekâ ile büyütme (AI upscaling) bırakıldı |
| 00-03 | 1 h | demo | Karar kaydı: kapsam = yarışmanın 5 test hedefi |
| 00-04 | 0 h |  | Karar kaydı: son teslim tarihi (deadline) sorusu ve varsayılan |
| 00-06 | 0 h |  | Model kademesi kuralı yazılı hale getirilir (Opus/Sonnet/Haiku) |
| 00-08 | 2 h | demo | Veri işleme politikası: indirilen veri güvenilmezdir |
| 00-14 | 1 h | sonra | Risk kaydı: R3/R4 kapsam ve WISE 0855 görünürlüğü, R17 sağlayıcı |
| 05-01 | 5 h | demo | Dama tahtası (checkerboard) test donanımı D1/T-V1 ve Q-H1 ekran görüntüleri |
| 05-02 | 5 h | demo | Görüntüleyici Mod N: tam sayı yakınlık, en yakın komşu, piksel ızgarası |
| 05-03 | 4 h | demo | Blink kontrolleri: oynat/duraklat, hız, adım, yeniden başlat, aynı dedektör çiftleme |
| 05-05 | 4 h | demo | θ_res / ofset rozeti ve Mod N otomatik varsayılan kuralı; Q-H2 ekran görüntüleri |
| 05-06 | 5 h | demo | Float konum işaretçileri ve hata elipsleri; 4.47 -> 447 kuralı |
| 05-07 | 4 h | demo | Gaia katmanı: her karenin MJD'sine taşınmış konumlar |
| 05-08 | 4 h |  | Bayrak (flag) katmanı düğmeleri: Table 16 bitleri ve maske profilleri |
| 05-09 | 3 h | demo | İmleç okuması: native piksel, gök konumu, değer, λ, bayraklar |
| 05-11 | 3 h | demo | Germe ve tema seçici (asinh/linear/zscale, koyu/açık) ve Q-H3 ekran görüntüleri |
| 05-12 | 6 h | sonra | Sonra: GPU afin Mod R (WebGL2 kare başı afin + NN) ve T-V2 |
| 05-13 | 4 h | sonra | Sonra: yumuşak kayma (smooth-shift) görünümü, yalnızca-görüntüleme, etiketli |
| 05-15 | 3 h | demo | Epoch göstergesi (+ − .) ve döngü başı kenarlığı: hangi kareler eklendi, çıkarıldı, kullan |
| 05-16 | 3 h | sonra | Tıkla-ortala ve sürükle-yeni-görüş-alanı |
| 05-17 | 4 h | demo | Gerdirme arayüzü: kırpma modları (sabit/yüzdelik/otomatik), doğrusallık, 'dinamik aralığı  |
| 05-19 | 2 h | sonra | Bağlam bağlantıları: Simbad, VizieR, Legacy Survey, Pan-STARRS kesiti (koordinat dolu) |
| 05-20 | 3 h | demo | Arka plan (ZODI) anahtarı arayüzde: ham / ZODI çıkarılmış (varsayılan) / düzleştirilmiş; r |
| 07-02 | 6 h | demo | T-V1/D1: checkerboard Playwright testi, DPR 1/1.25/2, Chrome + Firefox, z = 1, 3, 7, 16.5 |
| 07-03 | 3 h | demo | Kayan nokta konum testi: 4.47 zoom 100'de 447.0 ± 0.5 ekran pikseli; 0.2 px kayma z = 16 v |
| 07-07 | 5 h |  | T-V2/D2: dönmüş kare çizim testi (θ = 0.5°, 37°, 180°) ve D1b kütüphane SIP doğruluğu |
| 07-13 | 4 h | demo | Hedef başına son kabul kontrol listesi: 5 yarışma hedefi için ölçülebilir geçti/geçmedi |
| 07-15 | 3 h | demo | 5 hedef için otomatik kontak sayfası (regresyon ekran görüntüleri) |
| 07-16 | 3 h | demo | ZODI anahtarı testi: ölçüm değişmez, arka plan sıçraması ölçülür |
| 09-02 | 3 h | demo | 5 dakikalık demo betiği: her hedef için tam tıklama yolu |
| 09-08 | 2 h | demo | Yedek kayıtlı video: canlı demo çökerse oynatılacak ekran kaydı |
| 09-12 | 2 h | demo | İkinci prova ve soru-cevap hazırlığı (sınırlılıklar üzerine olası sorular) |
| 10-01 | 2 h | demo | SITE_SPEC.md'yi kullanıcıyla kilitlemek: açık sorular ve UI dili kararı |
| 10-02 | 4 h | demo | Açılış sayfası ve hedef seçici: 5 hazır hedef kartı ve kapsam durumu |
| 10-05 | 4 h | demo | Blink oynatıcı: oynat/duraklat, hız, adım, yeniden başlat işareti, kare sayacı |
| 10-06 | 3 h | demo | Kare başına metadata şeridi: tarih, detektör, dalga boyu, geçiş, sürüm, işleme etiketi |
| 10-07 | 5 h | demo | Gösterim modu rozeti (N / R-k / S), θ_res-ofset rozeti, piksel ızgarası ve kesin-piksel me |
| 10-08 | 2 h | demo | Kontrast ayarı ve renk: asinh/lineer/zscale, ters çevir, koyu/açık tema |
| 10-09 | 4 h | demo | Bayrak katmanı: Table 16 bit adları ve iki maske profili, kalabalık alan uyarısı |
| 10-10 | 5 h | demo | Gaia katmanı (öz hareket izi) ve centroid işaretleri (hata elipsi) |
| 10-13 | 5 h | sonra | Yığın ve fark görünümü: detektör başına geçiş yığını, A−B farkı, görünüm-yalnız etiketi |
| 10-14 | 4 h | demo | Hedef sonuç kartı ve kapsam/hata durumları: kapsam yok, arşiv meşgul, işleniyor |
| 10-16 | 5 h | demo | Hakkında ve sınırlılıklar sayfası, erişilebilirlik ve mobil temel, UI dili |
| 11-16 | 3 h | demo | Tasarım belirteçleri: renk, tipografi ölçeği, boşluk, koyu/açık tema, 16 px mobil kenar |
| 11-17 | 5 h | demo | Tel örgüler: ana ekran, giriş, profil/geçmiş ve sonuç/dışa aktarım paneli (masaüstü + tele |
| 11-18 | 4 h | demo | Boş/yükleniyor/hata/kaplama-yok/arşiv-meşgul durumları ve tek dosyada metinler |
| 11-19 | 4 h |  | İlk kullanım yönlendirmesi, klavye kısayolları ve erişilebilirlik denetimi |
| 11-20 | 4 h |  | Algılanan hız: kareleri kademeli gösterme, iskelet ekran, yerleşim kayması yok |
| 11-21 | 3 h |  | En çok 10 kullanıcıyla kısa kullanılabilirlik testi (küçük alt küme yeterli) ve bulguların |
| 11-22 | 2 h |  | Tasarım gözden geçirme kapısı: erişilebilirlik, tutarlılık ve dürüstlük |
| 11-23 | 3 h | demo | Geçmiş kayıtlarında küçük resim (thumbnail) göstermek |

Her görevin ayrıntısı `docs/tasks/tasks_<liste>.json` dosyasında ve ClickUp'ta.
