# Ekip bölüşümü: 4 alan (2026-11-14)

ClickUp'ta her görevde `kişi-a`, `kişi-b`, `kişi-c` veya `kişi-d` etiketi var. **Kimseye atama yapılmadı:** hangi harfi kimin alacağını ekip belirler. Harfler beceri alanıdır, kişi değil.

**Önemli:** tüm görevlerin tahmini toplamı **679 saat**, 'demo-5-gün' etiketli olanlar **449 saat**. Dört kişi için 5 gün yaklaşık 160 iş saati eder. Saat tahminleri ajanların yapay zekâsız bir kişi için verdiği kaba değerlerdir [ASSUMPTION]. Yapay zekâ yardımıyla kısalır ama kapsamı kesme sırasına göre yönetmek gerekir (bkz. DECISIONS_AND_TASK.md).

## Alan A: Veri entegrasyonu, görüntü işleme ve veri analizi (`kişi-a`)

NASA/IRSA'dan veriyi almak (TAP sorgusu, S3 okuma), pencere kesmek, maskelemek, arka planı çıkarmak, yıldızları bulmak, kare ürünlerini ve gösterim işlevlerini (gerdirme, PNG, ZODI) yazmak; ayrıca hedef raporlarının veri tarafı ve dışa aktarma biçimleri (CSV, FITS).

53 görev, tahmini 170 saat (demo etiketli 100, 'sonra' 20).

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

## Alan B: Astrometri ve hareketli cisim bilimi (`kişi-b`)

Konum bilimi: ePSF ile merkezleme, Gaia eşleme ve epoğa taşıma, WCS düzeltmesi, hareket uydurma, hareketli cisim bulucu, değişen yıldız ışık eğrileri, bilimsel testler ve 5 hedefin sonuç raporları.

46 görev, tahmini 170 saat (demo etiketli 100, 'sonra' 20).

| Görev | Süre | Etiket | Ad |
|---|---|---|---|
| 00-05 | 2 h | demo | Çalışma protokolü: ekip büyüklüğünden bağımsız görev seçimi |
| 01-03 | 3 h | demo | Gaia indirme sorunu: ESA TAP güvenilmez, yedek seçenekleri sırayla dene |
| 01-12 | 2 h | sonra | OUTLIER bayrağı nedeni (R27): aynı alanda hafta ve işleme etiketi karşılaştırması |
| 03-01 | 5 h | demo | ePSF modeli: EPSF HDU'dan GriddedPSFModel (örnekleme 5, 33x33) ve bölge seçimi |
| 03-02 | 3 h | demo | D5: ePSF normalizasyon ve yönelim kontrolü (×1/×25, x/y, dosya içi vs kalibrasyon) |
| 03-04 | 2 h | demo | Hata elipsi: kovaryanstan 1σ/2σ elips parametreleri ve JSON alanları |
| 03-05 | 4 h | demo | Doymuş çekirdek kanat uyumu: NaN/OVERFLOW pikselleri maskeleyerek |
| 03-06 | 5 h |  | Geçiş başına ortak uyum (C.7b): tek (α,δ) ile kareler boyunca |
| 03-07 | 5 h | demo | Gaia DR3 sorgusu ve epoğa taşıma formülleri (uzay hareketi + paralaks) |
| 03-12 | 4 h | demo | Enjeksiyon/kurtarma düzeneği tanımı: T1-T4 ve ölçütleri |
| 03-13 | 4 h | demo | Piksel-faz sapma eğrisi: sapma(faz) ölçümü ve tablo |
| 03-14 | 3 h | demo | Koordinat kuralları denetimi: 0 tabanlı, float konum asla yuvarlanmaz |
| 03-15 | 2 h | demo | WiseView'in Gaia yer değiştirmesiyle karşılaştırma testi (epoch hatasını bizim kodda önlem |
| 04-01 | 2 h | demo | Geçiş (pass) gruplama: 30 gün boşluk kuralı ve passes.json |
| 04-02 | 5 h |  | Geçiş yığını ve fark görüntüsü: yalnızca-görüntüleme (S modu), 'astrometri yok' etiketli |
| 04-03 | 4 h | demo | Zorlanmış (forced) ePSF fotometri modülü: sabit konumda kare başı akı |
| 04-04 | 5 h | demo | WISE 0855 saptanabilirlik testi: zorlanmış fotometri ve geçiş başına ters-varyans toplamı |
| 04-06 | 6 h |  | Hareketli cisim bulucu: katalog bağlama (hız ızgarası + RANSAC) |
| 04-07 | 4 h |  | OUTLIER kümelerini aday olarak terfi ettirme (hareketli arama maske profili) |
| 04-08 | 4 h |  | STREAK/GHOST/CROSSTALK vetoları (neden kodlu) ve kalabalık-alan koruması |
| 04-10 | 5 h |  | R24: asteroit konum sapması (1-3 px) araştırması: piksel nicemleme, LEO paralaksı, zamanla |
| 04-12 | 5 h |  | Değişen yıldızlar: RW Aur ve R Dra için λ-kutulu ışık eğrileri |
| 04-15 | 4 h | sonra | Kayan pencere toplama ve fark görünümü (yalnız görüntüleme, S modu) |
| 04-16 | 4 h | sonra | Sonra: 'kaydır ve topla' (shift-and-add) görünümü: kullanıcı hız girer, kareler izlenen ci |
| 04-17 | 4 h | sonra | Sonra: sentetik cisim ekleme (görüntüleme kopyasına, 'SENTETİK' etiketli) |
| 04-19 | 6 h | sonra | Sonra: gerçek/sahte hareketli sınıflandırıcı (küçük model) ve kural skoruyla karşılaştırma |
| 07-04 | 5 h | demo | T1 tam sayı kayma testi (sayısal + ekran z = 1, 4, 16, 64) ve T4 WCS gidiş-dönüş, D3 afin  |
| 07-05 | 6 h | demo | T2 alt-piksel merdiveni ve T3 enjeksiyon/kurtarma (D4 merkezleme yöntemi seçimi) |
| 07-08 | 6 h |  | T5 Gaia astrometri testi ve D6 WCS düzeltme modeli, D7 astrometri penceresi |
| 07-09 | 4 h |  | T6 bilinen hareket testi: Barnard μ (Gaia ile ±3σ ve %10), doygun çekirdek notu |
| 08-01 | 2 h | demo | Hedef sonuç notu şablonunu yazmak (kapsam, tespit, S/N, hareket, uyarılar, demo görünümü) |
| 08-02 | 3 h | demo | Barnard Yıldızı: kapsam tablosu ve zorlanmış fotometri/S-N sonucu (doygun çekirdek) |
| 08-04 | 2 h | demo | Barnard Yıldızı: uyarılar ve demo görünümünün tanımı (tıklama yolu, rozetler) |
| 08-05 | 3 h | demo | Epsilon Indi B: kapsam tablosu (458 kare, 4 geçiş) ve tespit/S-N sonucu |
| 08-06 | 3 h |  | Epsilon Indi B: hareket (literatür/Gaia), uyarılar ve demo görünümü |
| 08-07 | 3 h | demo | WISE 0855: kapsam tablosu (TAP şimdilik başarısız, bilinmiyor) ve tespit/zorlanmış fotomet |
| 08-09 | 3 h | demo | RW Aurigae: kapsam tablosu (TAP başarısız, bilinmiyor) ve tespit/zorlanmış fotometri |
| 08-10 | 3 h |  | RW Aurigae: değişken yıldız uyarısı (parlaklık ve dalgaboyu karışıklığı) ve demo görünümü |
| 08-11 | 3 h | demo | R Draconis: kapsam tablosu (TAP başarısız, bilinmiyor) ve tespit/zorlanmış fotometri |
| 08-13 | 2 h | demo | Beş hedefin karşılaştırma tablosunu yazmak (kapsam, S/N, hareket, durum) |
| 09-01 | 2 h | demo | README.md yazmak: ne yapar, nasıl çalıştırılır, hangi hedefler, hangi sınırlar |
| 09-06 | 2 h | demo | Sınırlılıklar sayfası: neyin doğrulanmadığını yazmak |
| 09-07 | 2 h | demo | Kullanıcı soruları için ekran görüntüsü setini hazırlamak (Q-H1, Q-H2, Q-H3) |
| 09-11 | 2 h | demo | Birinci prova: demo betiğini kronometreyle baştan sona yapmak |
| 10-11 | 6 h | demo | Okuma paneli, WCS-düzeltme rozeti ve geçişler arası hareket ölçüm paneli |
| 10-12 | 5 h | demo | Spektrum / ışık eğrisi paneli: RW Aur ve R Dra için zorunlu minimum |

## Alan C: Sunucu (backend), hesaplar, kiralama (`kişi-c`)

FastAPI sunucusu, önbellek, hız ve nezaket sınırları, kiralık makine kurulumu ve kapatma, dağıtım (Docker, Caddy), hesaplar/giriş/geçmiş/profil API'si, yedekleme, URL durumu ve hata/durum bilgileri, sunucu hız testi.

50 görev, tahmini 170 saat (demo etiketli 124, 'sonra' 23).

| Görev | Süre | Etiket | Ad |
|---|---|---|---|
| 00-10 | 2 h | demo | Risk kaydı: R1b getirme gecikmesi, R22 TAP, R23 kesit servisi |
| 00-11 | 2 h |  | Risk kaydı: R24 asteroit 1-3 piksel kayması |
| 00-12 | 2 h |  | Risk kaydı: R25 kalabalık alan, R26 kare içi roll farkı, R27 OUTLIER |
| 00-13 | 1 h | demo | Kullanıcıya sorular: sağlayıcı, hedef onayı, canlı gösterim |
| 01-05 | 3 h | demo | Bölge-içi zamanlama testi (D9) için betik ve ölçüm şeması |
| 01-06 | 3 h | demo | D9: kiralanan makinede bölge-içi zamanlama testini koştur |
| 02-10 | 4 h | demo | Kare başına ürün dosyaları (C.11): img/var/flg/cat/geom |
| 02-11 | 3 h | demo | Manifest şeması v2: alanlar, sürüm denetimi, JSON Schema dosyası |
| 02-20 | 4 h | demo | PNG ve küçük resim üretimi: tam sayı yakınlık + en yakın komşu; ızgara ve işaretleri gömme |
| 04-09 | 4 h |  | SkyBoT etiketleme: -objFilter=100 biçimi ve genişletilmiş eşleşme yarıçapı |
| 04-14 | 6 h | sonra | Sonra: kiralık GPU'da shift-and-stack (yalnızca B.5 tetikleyicisi çalışırsa) |
| 05-04 | 6 h | demo | R-k sunucu raster modu: farklı dönüşlü kareler için k=4-8 en yakın komşu |
| 05-10 | 4 h |  | URL parametre şeması: durumun adres çubuğuna yazılması ve yeniden yüklemede aynı görünüm |
| 05-14 | 4 h | sonra | Sonra: Aladin Lite yan paneli (bağlam haritası) ve dış bağlantılar |
| 05-18 | 3 h | demo | WiseView uyumlu URL takma adları ve `mode` isim çakışmasının çözümü |
| 06-01 | 4 h | demo | FastAPI iskeletini kurmak: önceden hesaplanmış dosyaları ve manifest uç noktasını sunmak |
| 06-02 | 5 h | demo | L0/L1/L2 önbellek katmanlarını ve dosya başına byte-offset haritasını gerçeklemek |
| 06-03 | 4 h |  | Asenkron TAP istemcisini yazmak: async iş, 15 dk tavan, yeniden deneme/backoff, L0 önbelle |
| 06-04 | 6 h | demo | Birleştirilmiş paralel S3 okuyucuyu yazmak: satır bloğu başına tek Range GET, 4 HDU parale |
| 06-05 | 3 h |  | Nezaket sınırlarını gerçeklemek: IRSA HTTP 4 eşzamanlı, cutout son çare 45 sn backoff |
| 06-06 | 3 h |  | Adım adım zamanlama loglarını yazmak (fetch/compute/serialize) ve GPU tetik raporunu çıkar |
| 06-07 | 4 h | demo | Saatlik kiralama runbook'u, bölüm 1: ne zaman kiralanır, boyut, güvenlik grubu, disk, bölg |
| 06-08 | 4 h | demo | Kiralama runbook'u, bölüm 2: D9 zamanlama testi, hedef ön-çekimi, önbelleği çıkarmak, otom |
| 06-09 | 4 h | demo | Docker + Caddy ile dağıtımı yazmak: compose, TLS, sıkıştırma, immutable dosya sunumu |
| 06-10 | 2 h | demo | Sır yönetimini kurmak: API anahtarları asla commit edilmez, tarama ve .env düzeni |
| 06-11 | 3 h | demo | Çevrimdışı yedeği hazırlamak: makine veya arşiv çökerse kayıtlı video ve ekran görüntüleri |
| 06-12 | 3 h | sonra | vast.ai GPU runbook'u (koşullu): shift-and-stack gösterimi için kiralama ve bırakma |
| 06-13 | 1 h | sonra | GPU tetik kapısı: zamanlama raporunu okuyup kirala / kiralama kararını vermek |
| 06-14 | 4 h | demo | API sözleşmesi (OpenAPI) ve sahte sunucu: ilk gün, D ve A beklemeden çalışsın |
| 07-01 | 2 h | demo | Test verisi yönetimini kurmak: sentetik/gerçek veri dizinleri, sabit tohum, ek kayıt (mani |
| 07-10 | 3 h |  | D8/D9 sunucu hızı testi: 50 kare koşturan betik ve sonuç yorumu (S3 okuyucu, sağlayıcı, bö |
| 07-11 | 4 h | sonra | D10 yığma birimi testi ve D14 aktarım formatı (float32+zstd, float16, 8-bit PNG) ölçümü |
| 07-12 | 4 h | demo | Regresyon paketi koşu betiği: tüm testleri tek komutla koşturup tek sonuç tablosu üretmek |
| 09-03 | 2 h | demo | Sunum slayt taslağını hazırlamak (8-10 slayt) |
| 09-04 | 3 h | demo | STATUS.md: tamam / kısmi / yapılmadı, rakamlarla |
| 09-05 | 2 h | demo | Yarışma sayfasını okuyup kuralları yazmak (gönderim gereksinimleri DOĞRULANMADI) |
| 09-09 | 2 h | demo | Teşekkür ve atıf sayfası: NASA/IPAC IRSA, SPHEREx, Gaia, astropy, photutils |
| 09-10 | 2 h | demo | Yarışma teslim kontrol listesi (kurallar 09-05 sonucuna göre) |
| 10-03 | 4 h | demo | Koordinat girişi: ondalık ve sexagesimal ayrıştırıcı, sunucu tarafı ad çözümleme |
| 10-04 | 3 h | demo | Görüş alanı (FOV) seçici ve pencere yeniden isteği |
| 10-15 | 6 h | demo | URL şeması, gömme modu, paylaş/dışa aktar (PNG, CSV) ve dış bağlantılar |
| 11-04 | 3 h | demo | En çok ~10 tanımlı hesabı seed dosyasından kuran kullanıcı deposu ve parola özeti |
| 11-05 | 4 h | demo | Giriş, oturum çerezi, HTTPS (Caddy) ve giriş hız sınırı |
| 11-06 | 4 h | demo | Arama geçmişi şeması ve her aramayı otomatik kaydeden uç nokta |
| 11-07 | 4 h | demo | Geçmiş kaydına tıklayınca tüm ayarları URL şeması ile geri yüklemek |
| 11-08 | 4 h | demo | Profil API'si: sayaçlar, son ziyaret, incelenen nesneler ve veri izolasyonu |
| 11-09 | 5 h | demo | Profil ve geçmiş ekranını yapmak (liste, süzme, sıralama, incelenen nesneler) |
| 11-10 | 3 h | demo | Veritabanı yedekleme ve yeni makineye geri yükleme betiği ve provası |
| 11-11 | 3 h | demo | PNG çıktısı: grid, işaretçi ve rozet metni gömülü görünüm kaydı |
| 11-13 | 5 h | sonra | Kesit FITS çıktısı: IRSA çok uzantılı düzen (IMAGE, FLAGS, VARIANCE, ZODI, EPSF, WCS-WAVE) |

## Alan D: Site ve arayüz (`kişi-d`)

Tarayıcı görüntüleyicisi (Mod N, blink, yakınlaştırma, işaretler, bayrak katmanı, gerdirme arayüzü), site sayfaları, UI/UX tasarımı ve görsel testler. Sunum ve belge görevleri (README, demo betiği, slaytlar, provalar) herkese dağıtıldı.

50 görev, tahmini 170 saat (demo etiketli 126, 'sonra' 21).

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

## Alanlar arası anlaşmalar (kim kime ne teslim eder)

| Kimden | Kime | Ne | Görev |
|---|---|---|---|
| A | B, C, D | Kare ürün dosyaları (img, var, flg, cat, geom) ve manifest şeması | 02-10, 02-11 |
| A | D, C | Gösterim işlevi (gerdirme) ve PNG/küçük resim | 02-16, 02-20 |
| B | A, D | WCS düzeltmesi, konum ve belirsizlik alanları (cat.json, geom.json) | 03-03, 03-04, 03-09 |
| C | D | API uç noktaları, URL durumu, hesap/geçmiş API'si, durum ve hata kodları | 06-01, 05-10, 11-04 → 11-08 |
| A | C | TAP istemcisi ve S3 okuyucu (sunucuya takılır) | 06-03, 06-04 |
| D | C | Arayüzün ihtiyaç duyduğu durumlar (kapsam yok, arşiv meşgul, işleniyor) | 10-14 |

Her anlaşma bir dosya şemasıdır (manifest, JSON Schema). Değişiklik olursa `02-11`'deki sürüm numarası artar, ilgili kişilere haber verilir.

## Dikkat
- Saatler tahmindir; yük dengesi de kabadır. **D alanı (site)** demo için en çok iş çıkaran alandır (demo etiketli saat en fazla).
- Bu bölüşüm 'beceri alanı' bölüşümüdür; istenirse iki kişi bir alanda birleştirilebilir, ya da bir kişi iki alan alabilir.
- Son tarih bilinmiyor. Ona göre kesilecek ilk işler: 'sonra' etiketliler, sonra yığınlar ve fark görünümleri, sonra spektrum.