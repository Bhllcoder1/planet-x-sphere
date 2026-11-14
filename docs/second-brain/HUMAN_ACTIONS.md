# Senden beklenenler

Gaia erişimi, ePSF prototipi ve sentetik testler otomatik yürütülüyor; CVAT kurulumu/elle etiketleme şu aşamada gerekli değil. Aşağıdaki bilgi yalnız üretim entegrasyonunu etkiliyor; bağımsız prototipleri durdurmuyor.

Bir insan adımı gerçekten gerektiğinde aşağıdaki kayıt doldurulur; ilgili otomasyon yanıt gelene kadar durur, bağımsız işler devam eder.

| Kimlik | Yapacağın işlem | Neden otomatik yapılamıyor | Beklenen çıktı | Açılacak görev | Durum |
|---|---|---|---|---|---|
| H-01 | Akif'in 02-03 koordinat/piksel kuralları ve 02-12 önbellek çıktıları başka yerdeyse dal/klasör yolunu belirt; hazır değillerse bunu söylemen yeterli. | Mevcut depoda yalnız iskelet var; başka yerin varlığı bilinmiyor. | Dal adı/yerel yol veya “hazır değil” yanıtı. | 03-01, 03-07 ve ardından fotometri üretim entegrasyonu. | Kullanıcıya soruldu; yanıt bekleniyor. |
| H-02 | ClickUp ayarlarından yeni kişisel API tokenı üretip yalnızca bu bilgisayardaki mevcut yerel token dosyasını güncelle; tokenı sohbete veya depoya gönderme. Sonra “hazır” de, ben salt-okunur `/user` ve görev sorgusuyla sınayayım. | Mevcut yerel tokenla canlı `GET /user` HTTP 401 döndü; güncel görev durumu doğrulanamıyor. | API 200 ile Behlül hesabı doğrulanır; atanan görevler ve güncel ClickUp durumları tazelenir. | Tüm ClickUp görev denetimi ve sıradaki bağımsız işin seçimi. | Kullanıcı işlemi gerekiyor. |
| H-03 | Liste 02'nin kanonik kare-listesi/manifest çıktısının dalını veya yerel yolunu ver; henüz hazır değilse bunu söyle. Varsa `SPS_EPA` alanının nereden geldiğini de belirt. | 04-01'in önkoşulu olan Liste 02 manifesti depoda ve Stage 0 çalışma klasöründe bulunamadı; mevcut `frames_*.json` örneklerinde `SPS_EPA` alanı yok. | Manifest yolu/şeması veya hazır olmadığı bilgisi. | 04-01 kabulü; sonra 04-02/04-03 entegrasyonu. | Kullanıcı/ekip girdisi bekleniyor. |
| H-04 | Akif'in 02-07 gerçek astrometri-yıldızı listesinin/kesit örneklerinin dalını veya yerel yolunu ver; hazır değilse bunu belirt. | 03-02'nin gerçek yönelim sınaması ve 200 yıldız örneklemi için 02-07 çıktısı gerekiyor; mevcut snapshot'ta 02-07 Akif'e atanmış ve `to do`. | Kaynak kare kimliği, alt-piksel konumu, kesit/gürültü verisi olan gerçek-yıldız örneklemi veya hazır değil yanıtı. | 03-02 yönelim/akı doğrulaması. | Kullanıcı/ekip girdisi bekleniyor. |

## Nasıl hazırlanacak?

- Karar gerekiyorsa kısa seçenekler, etkileri ve öneri sunulur; yanıt gelmeden karar verilmez.
- Hesap/erişim gerekiyorsa yerel kurulum yolu gösterilir; şifre veya anahtar sohbetten istenmez.
- Etiketleme gerekiyorsa önce örnek veri, etiket sözlüğü, kalite ölçütü ve küçük pilot hazırlanır; sonra uygun araç/skill araştırılır. Kurulumdan önce gerçek ihtiyacı doğrula.
- Ücretli makine veya harcama gerektiğinde maliyet ve amaç sunulur; onay olmadan kiralama yapılmaz.
- Dışarıya mesaj gönderme veya ekip üyesinden bilgi isteme gerekiyorsa kullanıcıya iletilebilir kısa taslak hazırlanır; kendiliğinden gönderilmez.

Henüz gerekmeyen olası işler gerçek bekleyen adım gibi listelenmez. Ekip arayüzü eksikleri [NOW.md](NOW.md) içinde teknik bağımlılık olarak tutulur.
