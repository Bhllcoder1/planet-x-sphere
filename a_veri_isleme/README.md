# Alan A: Veri entegrasyonu, görüntü işleme ve veri analizi

ClickUp etiketi: `kişi-a`. 53 görev, tahmini 170 saat [ASSUMPTION: ajan tahmini].

NASA/IRSA'dan veri almak (TAP sorgusu, S3 okuma), pencere kesmek, maskelemek, arka planı çıkarmak, yıldızları bulmak, kare ürünlerini ve gösterim işlevlerini yazmak; veri analizi ve çıktı biçimleri (CSV, FITS, PNG).

## Bu klasörün sahibi

`.github/CODEOWNERS` dosyasında bu klasöre bağlı GitHub kullanıcısı. Değişiklik bu kişinin onayıyla birleşir.

## Görevler

| Görev | Süre | Etiket | Ad |
|---|---|---|---|
| 00-01 | 1 h | demo | Karar kaydı: drizzle KAPALI (kullanıcı kararı) ve nedeni |
| 00-07 | 1 h | demo | Dürüstlük protokolü: [V] / [NV] / [ASSUMPTION] etiketleri |
| 00-09 | 1 h | demo | Karar kaydı: ince dilim (thin-slice) kesme sırası |
| 01-01 | 2 h | demo | Ortam: venv ve paketler (photutils; sep Python 3.14'te tekerlek yok) |
| 01-02 | 3 h | demo | Kapsam testi: WISE 0855, RW Aur, R Dra için async TAP (dedektör/geçiş) |
| 01-04 | 3 h |  | Sapma (aberration) kareleri B ve C: s0_C'yi tamamla |
| 01-07 | 2 h | sonra | Parent-piksel kuralı kenar testi: kenara kırpılmış kesit + başka dedektör |
| 01-08 | 2 h | sonra | Karşılaştırma: dosya-içi ePSF ile kalibrasyon dosyası baytlarını karşılaştır |
| 01-09 | 2 h | demo | Donmuş kare listeleri: 5 hedef için L0 dosyaları |
| 01-10 | 3 h | demo | Bayt-ofset haritası: HDU başlık ve veri başlangıçları (L1) |
| 01-11 | 4 h | demo | Barnard 358 kareyi önbelleğe al (prefetch betiği + koşu) |
| 01-13 | 2 h | demo | Stage 0 kapanış tablosu: kalan maddelerin hangi listeye gittiği ve geçit kontrolü |
| 02-01 | 4 h | demo | Sorgu adımı (C.1): async TAP, anahtar türetme, tekilleştirme, L0 önbelleği |
| 02-02 | 5 h | demo | Pencere getirme (C.2): birleştirilmiş satır aralığı okuması, 4 HDU paralel |
| 02-03 | 4 h | demo | Alma + piksel kuralları modülü (C.3): tek yarım-piksel fonksiyonu ve birim testleri |
| 02-04 | 3 h | demo | Maske profilleri (C.4): onaltılı değerlerle iki profil ve çalıştırılabilir tablo |
| 02-05 | 4 h | demo | Arka plan (C.5): sabit üst-piksel ızgarası döşemeleriyle, istek penceresinden bağımsız |
| 02-06 | 3 h |  | ZODI ve saçılan ışık denetimi: eğim testi ve 'stray-light şüpheli' bayrağı |
| 02-07 | 4 h | demo | Tüm-kare tespit (C.6): photutils ile astrometri yıldızı seçimi |
| 02-08 | 3 h | demo | Doymuş / NaN çekirdek işleme: zorlanmış konum ve maske ile ön-kontrol |
| 02-09 | 4 h |  | Aykırı değer / kozmik ışın / geçici olay işleme (C.10), neden kodlu liste |
| 02-12 | 3 h | demo | L1 önbelleği: bayt-ofset haritası ve anahtar şeması |
| 02-13 | 3 h |  | Kare kalite bayrakları: kullanılamaz kare, kalabalık alan ve kapsam rozeti |
| 02-14 | 3 h | sonra | astroscrappy ek maskesi (yalnızca D13 geçerse): hiçbir pikseli değiştirmeden |
| 02-15 | 2 h | demo | Gösterim işleme katmanı: tasarım kararları (kim neyi yapar, ölçüm verisi asla değişmez) |
| 02-16 | 4 h | demo | Germe ve kırpma modülü (Python referansı): fixed / percent / adapt / zscale + asinh + ters |
| 02-17 | 4 h | demo | Aynı germe işlevini tarayıcıda uygula ve Python ile 'altın test' yap |
| 02-18 | 3 h | sonra | Gösterim amaçlı sıcak/aykırı piksel işleme: varsayılan KAPALI, ölçümü etkilemeyen seçenek |
| 02-19 | 3 h | demo | ZODI/arka plan çıkarma (yalnız gösterim), renk çubuğu ve birim etiketi |
| 02-21 | 4 h | sonra | Sonra: dedektör/dalga boyundan renkli bileşik görünüm (yalnız görüntüleme) |
| 02-22 | 3 h | demo | display_defaults.json ve otomatik kalite geri dönüşü (zscale) |
| 03-03 | 6 h | demo | Merkezleme uyumu: (x, y, F, b) + kovaryans + VAR yeniden ölçekleme + kırpma |
| 03-08 | 3 h | demo | Gaia eşleştirme: KD-ağacı, belirsiz çiftler ve dışlama kuralları |
| 03-09 | 5 h | demo | Ölçülmüş WCS düzeltmesi: yalnız kayma, held-out RMS ve rozet |
| 03-10 | 3 h |  | Aberasyon alarmı: kayma > 0,5 px veya öngörülen vektörle korelasyon |
| 03-11 | 5 h | demo | Hareket uyumu: (α0, δ0, μα*, μδ, ϖ) geçişler arası ve Gaia ile karşılaştırma |
| 04-05 | 5 h |  | Çapraz-geçiş yavaş cisim eşleştirme: geçiş başına konumlardan μ uydurma |
| 04-11 | 5 h |  | Zaman karıştırmalı yanlış-iz oranı ve enjeksiyon testi (D11) |
| 04-13 | 4 h |  | Tıklanan kaynaktan spektrum: tüm karelerde zorlanmış fotometri, λ'ya göre akı |
| 04-18 | 4 h | sonra | Sonra: SkyBoT etiketli eğitim setini ~100 seyrek kareye genişletme |
| 07-06 | 5 h |  | D5 ePSF normalleştirme/yönelim ve D13 enjeksiyon testi (çekirdek kaybı, merkez yanlılığı) |
| 07-14 | 3 h | sonra | Sentetik cisimle kurtarma testi (kullanıcı özelliği ve hareketli bulucu ile ortak) |
| 08-03 | 3 h | demo | Barnard Yıldızı: geçişler arası hareketi Gaia ile karşılaştırmak (0->1 ve 0->2) |
| 08-08 | 2 h |  | WISE 0855: hareket (yaklaşık 0.66 px / 6 ay, aritmetik), uyarılar ve demo görünümü |
| 08-12 | 3 h |  | R Draconis: değişken yıldız uyarısı (parlaklık ve dalgaboyu karışıklığı) ve demo görünümü |
| 08-14 | 2 h |  | Dürüst sonuç kuralını yazmak: SPHEREx'in gösteremediği hedef olduğu gibi raporlanır |
| 10-17 | 3 h | demo | WiseView kaynak kodunu inceleyip not çıkar: işlev-satır tablosu, alınacaklar ve alınmayaca |
| 11-01 | 2 h | demo | IRSA çıktı belgesini scrapling ile okuyup tam sütun/birim/biçim listesini yazmak |
| 11-02 | 2 h |  | MJy/sr -> mJy dönüşümünün hangi piksel ölçeğini kullandığını doğrulamak |
| 11-03 | 3 h | demo | Boru hattı ürünlerini 'gösterime hazır' yapan dışa aktarım şemasını yazmak |
| 11-12 | 3 h | demo | Ölçüm tablosu CSV'si: şemaya uygun sütunlar ve kaynak başlığı |
| 11-14 | 5 h |  | Spektrum grafiği (hata çubuklu, dedektöre göre renkli) ve tablosu |
| 11-15 | 2 h | demo | Her çıktıya kaynak bloğu ve dürüst sınır notu eklemek |

Her görevin ayrıntısı ClickUp'ta (Planet XSphere çalışma alanı).

## Alt klasörler

- `fetch/     NASA/IRSA'dan kare listesi (TAP) ve piksel okuma (S3)
- `process/   maske, arka plan, yıldız bulma, doymuş çekirdek
- `products/  kare ürün dosyaları ve manifest
- `display/   gerdirme, PNG ve küçük resim üretimi
- `exports/   CSV, FITS kesit ve spektrum çıktıları
