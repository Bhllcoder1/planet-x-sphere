# İnsan girdisi gerekenler

Sentetik prototipler bağımsız ilerleyebilir. Aşağıdaki girdiler ilgili gerçek veri entegrasyonu veya canlı ClickUp denetimi için gerekiyor; hazır değilse bunu belirtmek yeterli.

| Kimlik | Beklenen insan adımı | Neden gerekiyor | Beklenen yanıt | Etkilediği iş | Durum |
|---|---|---|---|---|---|
| H-01 | Akif'in 02-03 koordinat/piksel kuralları ve 02-12 L1 cache çıktılarının dalını/yerel yolunu ver veya hazır olmadığını belirt. | Depoda yalnızca prototip iskeleti var; üretim sözleşmesi ve cache çıktısı bulunamadı. | Dal/yol veya “hazır değil”. | 03-01, 03-07 üretim entegrasyonu. | Yanıt bekleniyor. |
| H-02 | Bu bilgisayardaki yerel ClickUp token dosyasını yeni kişisel tokenla güncelle; tokenı sohbete veya depoya koyma. Ardından “hazır” de. | Salt-okunur `GET /user` mevcut tokenla HTTP 401 döndürdü; canlı görev durumu doğrulanamıyor. | API 200 ile Behlül hesabı ve atanmış görevler doğrulanır. | Canlı ClickUp denetimi ve sıradaki görevin seçimi. | Kullanıcı işlemi gerekiyor. |
| H-03 | Liste 02 kanonik kare manifestinin dalını/yerel yolunu ve varsa `SPS_EPA` kaynağını ver veya henüz hazır olmadığını belirt. | Manifest depoda ve Stage 0 klasöründe bulunamadı; taranan `frames_*.json` örneklerinde `SPS_EPA` yok. | Manifest yolu/şeması ve `SPS_EPA` kaynağı veya “hazır değil”. | 04-01 kabulü; 04-02/04-03 entegrasyonu. | Yanıt bekleniyor. |
| H-04 | Akif'in 02-07 gerçek izole yıldız listesinin/kesitlerinin dalını veya yerel yolunu ver ya da hazır olmadığını belirt. | 03-02'nin gerçek yönelim/akı testi için gerçek yıldız örnekleri gerekiyor; geçmiş snapshot'ta 02-07 Akif'e atanmış ve `to do`. | Kare kimliği, alt-piksel konumu ve kesit/gürültü verisi olan örneklem veya “hazır değil”. | 03-02 gerçek veri doğrulaması. | Yanıt bekleniyor. |
| H-05 | 03-05 gerçek görüntü taraması için 02-08 ve 03-03 çıktı yollarını ver veya hazır olmadıklarını belirt. | Mevcut kanıt sentetik kesitlerle sınırlı; üretim görüntüleri ve önkoşul çıktıları doğrulanmadı. | Doymuş çekirdek içeren gerçek kare/kesitler ve ilgili çıktı yolları veya “hazır değil”. | 03-05 gerçek veri doğrulaması. | Yanıt bekleniyor. |

## Güvenli hazırlık

- Erişim anahtarı veya tokenı sohbete/depoya gönderme; yalnız yerel yapılandırmayı güncelle.
- Etiketleme gerekirse önce örnek veri, etiket sözlüğü ve kabul ölçütü netleştirilir; şu an CVAT/elle etiketleme gerekmiyor.
- Harcama veya dışarıya mesaj gönderme gerekirse önce kullanıcıya taslak ve maliyet sunulur; otomatik işlem yapılmaz.
- Görevlerin ClickUp durumunu canlı API doğrulanmadan değiştirme veya tamamlandı sayma.
