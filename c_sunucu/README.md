# Alan C: Sunucu, hesaplar, kiralama

ClickUp etiketi: `kişi-c`. 50 görev, tahmini 170 saat [ASSUMPTION: ajan tahmini].

FastAPI sunucusu, önbellek, kiralık makine kurulumu ve kapatma, dağıtım (Docker, Caddy), hesaplar, giriş, geçmiş, profil, yedekleme, hız ve nezaket sınırları.

## Bu klasörün sahibi

`.github/CODEOWNERS` dosyasında bu klasöre bağlı GitHub kullanıcısı. Değişiklik bu kişinin onayıyla birleşir.

## Görevler

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

Her görevin ayrıntısı `docs/tasks/tasks_<liste>.json` dosyasında ve ClickUp'ta.
