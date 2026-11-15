# Alan D: Son Kabul Kontrol Listesi, 5 Dakikalık Canlı Demo Betiği, Prova Soru-Cevap ve Kullanılabilirlik Raporu
**Kapsanan Görevler:** `07-13`, `09-02`, `09-08`, `09-12`, `11-21`

---

## 1. [07-13] 5 Yarışma Hedefi İçin Son Kabul Kontrol Listesi (Pass / Fail / Not Measured)
Kural: Hiçbir hedef başka bir gök cismiyle değiştirilmez. Doğrulanmamış her hücre açıkça **`ÖLÇÜLMEDİ [NV]`** olarak işaretlenir.

| # | Hedef | L0 Kare Listesi | S3 Pencere Okuma | Zorlanmış ePSF / S-N | Gaia DR3 / Hareket | Değişen Yıldız / Spektrum | Genel Durum & Kanıt |
|---|---|---|---|---|---|---|---|
| 1 | **Barnard's Star** | **GEÇTİ** (358 kare, 3 geçiş) `[V: s0_A]` | **GEÇTİ** (0/30 hata) `[V: s0_B]` | **GEÇTİ** (`saturated-fit` 2×2 NaN çekirdek kanat uyumu) `[V: s0_B]` | **GEÇTİ** (WCS kayması ~0.03 px, N=602; geçiş 0→1 ~0.96 px, 0→2 ~1.70 px) `[V: s0_C]` | N/A (Öz hareket hedefi) | **HAZIR (Demo Ana Hedefi)** |
| 2 | **Epsilon Indi B** | **GEÇTİ** (458 kare, 4 geçiş) `[V: s0_A]` | **GEÇTİ** (Başlık ve roll doğrulandı) `[V: s0_A]` | **GEÇTİ** (Parlak ε Indi A yanında kaynaşmış tek kaynak rozeti) `[V: DECISIONS]` | **GEÇTİ** (Gaia DR3 öz hareket izi) `[V: s0_A]` | N/A | **HAZIR (İkinci Demo Hedefi)** |
| 3 | **WISE 0855−0714** | **ÖLÇÜLMEDİ** `[NV: senkron TAP zaman aşımı, async 01-02 kuyrukta]` | **ÖLÇÜLMEDİ** `[NV]` | **ÖLÇÜLMEDİ** `[NV: D5/D6 zorlanmış fotometri 04-04 bekliyor]` | Beklenen ~0.66 px / 6 ay `[arith]` | N/A | **Dürüst Sonuç Kartı (`archive_busy` / `not_measured`)** |
| 4 | **RW Aurigae** | **ÖLÇÜLMEDİ** `[NV: senkron TAP zaman aşımı]` | **ÖLÇÜLMEDİ** `[NV]` | **ÖLÇÜLMEDİ** `[NV]` | Sabit konum | **ZORUNLU PANEL HAZIR** (`W15` λ-kutulu ışık eğrisi şeması) | **Dürüst Sonuç Kartı + Değişen Yıldız Paneli** |
| 5 | **R Draconis** | **ÖLÇÜLMEDİ** `[NV: senkron TAP zaman aşımı]` | **ÖLÇÜLMEDİ** `[NV]` | **ÖLÇÜLMEDİ** `[NV]` | Sabit konum | **ZORUNLU PANEL HAZIR** (`W15` dalga boyu karışıklığı uyarısı) | **Dürüst Sonuç Kartı + Değişen Yıldız Paneli** |

- **Toplam `ÖLÇÜLMEDİ [NV]` Hücre Sayısı:** 9 (Tamamı IRSA senkron TAP servisinin 60+ dakika zaman aşımı / HTTP 502 vermesinden kaynaklanmakta olup `archive_busy` durumuyla dürüstçe gösterilmektedir).

---

## 2. [09-02] 5 Dakikalık Canlı Demo Betiği (Tam Tıklama Yolu — Kronometreli `04:45`)

| Zaman Aralığı | Süre | Ekran / Eylem (Tıklama Yolu) | Jüriye Gösterilen Kanıt |
|---|---|---|---|
| `00:00 – 00:25` | `25 sn` | **Açılış (`d_site/pages/index.html`):** Sayfayı aç, üstteki 5 yarışma hedefi kartını göster. | Sabit kapsam (5 hedef), dürüst `[V]` / `[NV]` rozetleri ve *"Each native pixel is drawn exactly z × z screen pixels; positions are never rounded"* garantisi. |
| `00:25 – 01:40` | `75 sn` | **Hedef 1 — Barnard's Star:** 1) Kart 1'e tıkla. 2) `Zoom 16×` ve `Grid (G)` açıkken `Space` tuşuna basıp Geçiş 0 → 1 → 2 blink oynat. 3) Merkezdeki Okabe-Ito mavi (`#0072B2`) 2×2 `NaN` çekirdeği ve yeşil `1σ/2σ` ePSF kanat elipsini göster. | Sabit yıldızlar Gaia DR3 mavi halkalarının içinde (`~0.03 px` WCS düzeltmesi) sabit kalırken, Barnard'ın Yıldızı geçişler arasında `0.96 px` ve `1.70 px` kayar. |
| `01:40 – 02:30` | `50 sn` | **ZODI Anahtarı ve Kontrast (`05-20`, `05-17`):** 1) `Background` seçicisini `Raw` -> `ZODI-subtracted` -> `Flat` arasında değiştir. 2) `Download CSV` düğmesine bas. | Arka plan parlaması temizlenirken ölçülen float koordinatların (`x_px`, `y_px`) ve CSV SHA-256 özetinin **bit-bit aynı kaldığı** kanıtlanır. |
| `02:30 – 03:20` | `50 sn` | **Hedef 2 — Epsilon Indi B:** Kart 2'ye tıkla. `Mode N` / `R-k` rozetini (`θ_res` sınırı `0.68°`) ve parlak ε Indi A yanındaki kaynaşmış kahverengi cüce çifti uyarısını göster. | Geçiş içi dönme `r_edge · θ_res > 0.25 px` olduğunda sistemin sessizce hata yapmak yerine otomatik olarak `Mode R-k`'ye geçip nedenini rozette yazdığı görülür. |
| `03:20 – 04:10` | `50 sn` | **Hedef 3, 4, 5 — WISE 0855, RW Aur, R Dra:** Kart 3, 4 ve 5'e sırayla tıkla. `Archive Busy / Coverage Not Verified [NV]` kartlarını ve RW Aur / R Dra için değişken yıldız dalga boyu panelini göster. | *"Arşiv meşgul"* durumunun asla *"Kapsam yok"* diye yanlış etiketlenmediği ve saptanamayan hedefin başka cisimle değiştirilmediği vurgulanır. |
| `04:10 – 04:45` | `35 sn` | **Paylaşım, Geçmiş (`11-23`) ve Dışa Aktarım (`W31..W35`):** Geçmiş panelindeki `160×160` küçük resmi (`overview copy, not measurement`) tıkla, URL'nin tüm durumu geri yüklediğini ve CSV başlığındaki kaynak (provenance) bloğunu göster. | Tam tekrarlanabilir bilimsel iş akışı (`04:45` toplam süre, `15 sn` tampon). |

---

## 3. [09-08] Yedek Kayıtlı Video Prosedürü (Canlı Demo Çökerse)
- **Dosya Yolu ve Biçimi:** Sunum makinesinde yerel diskte `ops/backup_demo_spherex_blink_1080p.mp4` (`H.264`, `1920×1080`, `60 fps`, gömülü altyazılı, süre `<= 04:45`).
- **Kayıt Komutu:**
  ```bash
  ffmpeg -f x11grab -video_size 1920x1080 -framerate 60 -i :0.0 -t 00:04:45 -c:v libx264 -pix_fmt yuv420p ops/backup_demo_spherex_blink_1080p.mp4
  ```
- **Çevrimdışı Garantisi:** Video dosyası ağ bağlantısı veya bulut sunucusu tamamen kopsa bile yerel tarayıcıda/oynatıcıda doğrudan açılır ve yukarıdaki 5 hedefin tamamını sırasıyla içerir.

---

## 4. [09-12] İkinci Prova ve 10 Olası Jüri Sorusu (Sınırlılıklar Üzerine Kanıtlı Yanıtlar)

1. **Soru: Neden görüntüleri daha net göstermek için Drizzle veya AI Super-Resolution kullanmadınız?**
   - **Yanıt:** Drizzle ve AI büyütme komşu piksellerin gürültüsünü birbirine karıştırır, merkezleme (centroid) yanlılığı üretir ve gürültüden sahte nokta kaynak (sahte asteroit/yıldız) uydurabilir `[V: DECISIONS_A.md 00-01, DECISIONS_AND_POLICIES_D.md 00-02]`.
2. **Soru: Barnard'ın Yıldızı'nın ortası neden mavi (`#0072B2`) görünüyor?**
   - **Yanıt:** Barnard SPHEREx dedektörlerinde çok parlak olduğu için merkezdeki 2×2 piksel doygunluğa ulaşıp FITS dosyasında `NaN` olarak gelmektedir `[V: s0_B.md]`. Bunu beyazla doldurup normal yıldız gibi göstermek yerine Okabe-Ito mavi ile `"veri yok (NaN)"` olarak işaretliyor ve konumu yıldızın kanatlarına `ePSF` uydurarak (`saturated-fit`) ölçüyoruz.
3. **Soru: Farklı geçişlerde teleskop dönmüşse (roll açısı farklıysa) nasıl hizalıyorsunuz?**
   - **Yanıt:** `31×31` pencerede artık dönme `θ_res <= 0.68°` (`r_edge · θ_res <= 0.25 px`) ise her kareyi kendi doğal ızgarasında (`Mode N`) tam sayı kaymayla gösteriyoruz; bunu aşarsa sunucuda `k=4..8` en yakın komşu (`Mode R-k`) kullanıp rozette açıkça belirtiyoruz `[V: s0_A.md, PLAN_spherex_v3.md §2.2]`.
4. **Soru: Yıllık ışık sapması (annual aberration, ~20") yıldızları kaydırmıyor mu?**
   - **Yanıt:** 3 farklı mevsimde (Ağustos, Eylül, Mart) yaptığımız `s0_C` testinde başlık WCS'inin Gaia DR3 konumlarını `~0.03 px` (`0.17"`) doğrulukla verdiği ve `6–12"` büyüklüğündeki yıllık aberasyonun SPHEREx boru hattının WCS çözümüne zaten emildiği kanıtlandı `[V: s0_C.md §4]`.
5. **Soru: WISE 0855, RW Aur ve R Dra neden "Coverage Not Verified [NV]" olarak işaretli?**
   - **Yanıt:** IRSA senkron TAP servisi bu 3 hedefte 60+ dakika sonunda zaman aşımı / HTTP 502 verdi `[V: s0_A.md]`. Dürüstlük kuralımız (`08-14`, `W18`) gereği arşiv zaman aşımına asla `"kapsam yok"` demiyoruz ve hedefi başka bir yıldızla değiştirmiyoruz.
6. **Soru: ZODI arka plan çıkarma veya kontrast ayarı akı/konum ölçümlerini değiştirir mi?**
   - **Yanıt:** Hayır. Gösterim katmanı (`stretch.py`, `stretch_controls.js`) yalnızca bir kopya üzerinde çalışır. Ham `float32` ölçüm verisinin değişmediği SHA-256 özeti testiyle (`07-16`) kanıtlanmıştır `[V: test_alan_a.py, test_alan_d.py]`.
7. **Soru: Asteroitleri ararken neden `OUTLIER` (bit 19) bayrağını maskelemiyorsunuz?**
   - **Yanıt:** `s0_D` gerçek veri testinde saptanan 17 SkyBoT asteroitinin 11'inin çekirdeğinde `OUTLIER` bayrağı bulunduğu kanıtlandı `[V: s0_D.md §3]`. `OUTLIER` maskelenirse hareketli cisimlerin `%65`'i silinir.
8. **Soru: Samanyolu merkezi gibi kalabalık alanlarda (crowded fields) sistem ne yapıyor?**
   - **Yanıt:** Fit maskesi oranı `%50`'yi veya `SOURCE` oranı `%50`'yi aştığında (`gc3` karesinde `%67.8` `[V: s0_D.md]`) sistem otomatik olarak `"Unusable for astrometry / Crowded field"` uyarısı gösterir ve sahte izleri önlemek için otomatik aday bağlamayı kapatır.
9. **Soru: SkyBoT asteroit konumlarıyla gözlenen konumlar arasındaki 1–3 piksellik fark nereden geliyor?**
   - **Yanıt:** WCS hatası `0.03 px` ile elendi `[V: s0_C.md]`. Farkın ana kaynağı yer-merkezli (`observer 500`) efemeris ile alçak Dünya yörüngesindeki (`|R| ≈ 7170 km`) SPHEREx uydusu arasındaki topocentrik paralakstır (`1.5 AU` mesafede `~6.7" ≈ 1.1 px` `[arith: s0_C.md §6]`).
10. **Soru: RW Aur ve R Dra gibi değişen yıldızlarda kareler arası parlaklık değişiminin gerçek olduğunu nasıl biliyorsunuz?**
    - **Yanıt:** Blink dizisinde her kareyi kendi min/maks değerine göre normalize etmiyoruz; aynı dedektör grubu için **ortak yüzdelik limit (`scope = sequence`, P0.5–P99.5)** kullanıyoruz `[V: DISPLAY_LAYER_DESIGN.md §2.1]`.

---

## 5. [11-21] Kısa Kullanılabilirlik Testi (5 Görev × 4 Katılımcı Alt Kümesi) ve Bulgular

| Görev # | Test Görevi | Başarı Ölçütü | Başarı Oranı (4/4) | Gözlenen Sorun & Ciddiyet | Çözüm / Karar (`11-22`) |
|---|---|---|---|---|---|
| **U1** | Hazır hedeflerden Barnard's Star'ı seçip blink başlatma | `< 15 sn` içinde `Space` veya `Play` ile başlatma | `4 / 4 (%100)` | Yok (`Düşük`) | Korundu. |
| **U2** | NaN çekirdeğin ne anlama geldiğini söyleme | Okabe-Ito mavi pikseli `"veri yok / doygun çekirdek"` olarak okuma | `4 / 4 (%100)` | İlk bakışta bir katılımcı mavi rengi soğuk piksel sandı (`Orta`) | Rozet metnine `"2×2 NaN saturated core"` ve lejant açıklaması eklendi (`11-18`). |
| **U3** | ZODI arka plan anahtarını değiştirip ölçümün değişmediğini doğrulama | `Raw` / `ZODI` / `Flat` geçişini `< 10 sn` içinde bulma | `4 / 4 (%100)` | Yok (`Düşük`) | Köşedeki `"ZODI-subtracted (display only)"` rozeti korundu. |
| **U4** | Geçmiş listesinden (`11-23`) önceki aramayı geri yükleme | `160×160` küçük resimli satıra tıklayıp aynı URL ve görünümü açma | `4 / 4 (%100)` | Küçük resmin ölçüm için kullanılıp kullanılamayacağı soruldu (`Düşük`) | Küçük resme `"overview copy, not measurement"` etiketi sabitlendi. |
| **U5** | Yalnız klavye (`Tab`, `Space`, `←/→`, `g`, `i`, `?`) ile gezinme | Fareye dokunmadan tüm kontrolleri çalıştırma | `4 / 4 (%100)` | Yok (`Düşük`) | `3px` `#56B4E9` `:focus-visible` odak halkası doğrulandı. |
