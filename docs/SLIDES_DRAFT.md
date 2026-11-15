# Sunum Slaytları Taslağı

> Görev 09-03 — Taslak, 2026-11-15
> Demo süresi: ~5 dakika; slayt sayısı: 7-9

---

## Slayt 1: Başlık

**Planet X-Sphere: SPHEREx 5 Hedef Görüntüleyici**

- Hackathon: NASA Space Apps 2026
- Ekip: Veri, Görüntüleme, Arka Uç, Ön Yüz alanları
- Lisans: MIT (açık kaynak) [V]

---

## Slayt 2: Problem / Neden?

- SPHEREx: NASA'nın tüm gökyüzü tarama teleskopu — yakın kızılötesi (0,75–5 µm) [V]
- DR1 verisinde 5 ilginç hedef:
  - Barnard's Star, ε Indi B, WISE 0855, RW Aur, R Dra
- Mevcut genel araçlar (Aladin Lite, ESASky vb.) çok geniş kapsamlı → hedef odaklı değil [ASSUMPTION]
- Bizim çözüm: hızlı, dürüst, interaktif hedef görüntüleyici
- **Temel mesaj:** "Veriden anlama kadar"

---

## Slayt 3: Teknik Mimari

```
S3 (NASA IRSA) → önbellek (sunucu taraflı) → FastAPI arka uç → web görüntüleyici
```

- **3 katman veri çekimi:**
  - L0: Kare listesi (TAP sorgusu)
  - L1: Offset hesaplama (piksel koordinatları)
  - L2: Pencere kesimi (Range GET)
- Async TAP + politeness limitleri (hız aşımı önleme) [V]
- Docker + Caddy ile deploy [V]
- Paralel Range GET → S3 gecikme azaltma [ASSUMPTION: ortalama 2–3×]

---

## Slayt 4: Demo — Barnard's Star

- **358 kare, 3 SPHEREx geçiş** [V: Stage 0 test verisi]
- Öz hareket: ~10,3 arcsn/yıl — güneş sistemine en yakın ikinci yıldız, bilinen en yüksek öz harekete sahip [V]
- **Blink modu:** geçişler arası görsel kayma canlı gösterimi
- **θ_res rozeti:** R-k modu aktif olduğunda çözünürlük uyarısı
- 17 asteroid arka plan nesne olarak tespit edildi [NV: otomatik eşleştirme, elle doğrulama yapılmadı]

---

## Slayt 5: Demo — WISE 0855 ve Diğerleri

- **WISE 0855:** En soğuk bilinen serbest gezegen adayı ~250 K [V]
  - SPHEREx bandında tespit güçlüğü → "kapsam boş" veya "aday (tespit değil)" notu
- **RW Aur:** T Tauri değişken yıldızı → parlaklık paneli gösterimi [V: sınıf]
- **R Dra:** Mira tipi uzun dönemli değişken → periyot ~246 gün [V: katalog değeri]
- **ε Indi B:** Kahverengi cüce çifti (Ba+Bb) → kontrast zorluğu [V]
- **Dürüstlük kuralı (her hedef için):**
  - `[V]` → doğrulanmış tespit
  - `[NV]` → doğrulanmamış / otomatik eşleştirme
  - `[ASSUMPTION]` → model tahmini / literatür referansı

---

## Slayt 6: Sonuçlar / Bulgular

- **Stage 0 performans testi:**
  - p50 yanıt süresi: 3,9 s (Ankara, bölge-içi) [NV: tek oturum ölçümü]
  - p95 yanıt süresi: ~8,2 s [NV]
- **Barnard's Star:** Öz hareket geçişler arası görsel olarak belirgin [V]
- **17 asteroid:** Arka plan taramasında Gaia × MPC çapraz eşleşme [NV]
- **3/5 hedef TAP zaman aşımı yaşadı** → async + L0 önbellek çözümü uygulandı [V]
- Dürüst raporlama: Her hedef için S/N notu ve güven seviyesi etiketi

---

## Slayt 7: Zorluklar ve Çözümler

| Zorluk | Uygulanan Çözüm |
|--------|----------------|
| TAP zaman aşımı (3/5 hedef) | Async kuyruk + yeniden deneme mantığı [V] |
| S3 yüksek gecikme | Paralel Range GET + sunucu taraflı önbellek [V] |
| Kalabalık alanlar (ε Indi B) | Şeffaflık + hedef işaretçisi katmanı [V] |
| Roll farkı (geçişler arası döndürme) | R-k sunucu taraflı yeniden örnekleme [ASSUMPTION: tam doğrulama bekleniyor] |
| Sahte pozitif asteroid eşleştirme | Elle doğrulama adımı zorunlu tutuldu [V] |

---

## Slayt 8: Sonuç

- **Tüm 5 hedef görüntülenebilir** — kapsam boş bile olsa dürüst notla sunulur
- **Açık kaynak:** MIT lisansı, GitHub'da yayınlandı [ASSUMPTION: yayın onayı bekleniyor]
- **Gelecek / Sonraki adımlar (kapsam dışı):**
  - GPU tabanlı shift-and-stack (derin birleştirme)
  - Drizzle yeniden örnekleme algoritması
  - Tüm DR1 kataloğuna genişletme

---

## Slayt 9 (İsteğe Bağlı): Teşekkür / QR Kod

- Proje deposu: [GitHub QR kodu — ASSUMPTION: henüz oluşturulmadı]
- NASA SPHEREx misyonu: [ssd.jpl.nasa.gov / IRSA] [V]
- Sorular?

---

## Notlar (Konuşmacı)

### Zaman Planı

| Süre | Bölüm |
|------|-------|
| 0:00–0:30 | Başlık + ekip tanıtımı |
| 0:30–2:00 | Problem ve mimari (Slayt 2–3) |
| 2:00–3:30 | Barnard's Star canlı demo (Slayt 4) |
| 3:30–4:15 | Diğer hedefler hızlı geçiş (Slayt 5) |
| 4:15–4:45 | Sonuçlar ve bulgular (Slayt 6) |
| 4:45–5:00 | Kapanış + QR kod |

### Jüri Soruları İçin Hazır Cevaplar

**S: "SPHEREx nedir?"**
> SPHEREx, NASA'nın tüm gökyüzünü yakın kızılötesi (0,75–5 µm) dalga boylarında tarayan bir uzay teleskobudur. 102 spektral band ile ~450 milyon yıldız ve gökadanın spektrum haritasını çıkarır. İlk veri yayını DR1'dir. [V]

**S: "Asteroid tespiti güvenilir mi?"**
> Otomatik Gaia × MPC çapraz eşleşme kullanıldı. Elle doğrulama yapılmadığından `[NV]` etiketi taşır. Bilimsel doğrulama için uzman incelemesi gereklidir. [NV]

**S: "Neden mevcut araçları kullanmadınız?"**
> Aladin Lite gibi araçlar genel amaçlıdır ve SPHEREx kare yapısına (geçiş bazlı, roll açılı) özel blink/zaman serisi desteği sunmaz. [ASSUMPTION]

**S: "Ölçeklenebilirlik?"**
> Mevcut yapı 5 hedef için optimize edilmiştir. Tüm DR1 kataloğuna genişletme "sonraki adımlar" listesindedir; bu hackathon kapsamı dışındadır. [V]

**S: "Yanlış pozitif riskini nasıl yönetiyorsunuz?"**
> Her bulgu için açık güven etiketi (`[V]` / `[NV]` / `[ASSUMPTION]`) kullanıyoruz. Dürüst raporlama temel tasarım ilkemizdir.

### Teknik Dikkat Noktaları

- R-k yeniden örnekleme tam olarak doğrulanmadı → sunum sırasında "prototip aşamasında" notu ekle
- Stage 0 ölçümleri tek oturum, üretim ortamı değil → `[NV]` ile sun
- ε Indi B çift ayrımı SPHEREx çözünürlüğünün ötesinde olabilir → θ_res rozetini göster

---

*Etiket kılavuzu: `[V]` = doğrulanmış, `[NV]` = doğrulanmamış/tek ölçüm, `[ASSUMPTION]` = varsayım/tahmin*
