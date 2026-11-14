# Senden beklenenler

Gaia erişimi, ePSF prototipi ve sentetik testler otomatik yürütülüyor; CVAT kurulumu/elle etiketleme şu aşamada gerekli değil. Aşağıdaki bilgi yalnız üretim entegrasyonunu etkiliyor; bağımsız prototipleri durdurmuyor.

Bir insan adımı gerçekten gerektiğinde aşağıdaki kayıt doldurulur; ilgili otomasyon yanıt gelene kadar durur, bağımsız işler devam eder.

| Kimlik | Yapacağın işlem | Neden otomatik yapılamıyor | Beklenen çıktı | Açılacak görev | Durum |
|---|---|---|---|---|---|
| H-01 | Akif'in 02-03 koordinat/piksel kuralları ve 02-12 önbellek çıktıları başka yerdeyse dal/klasör yolunu belirt; hazır değillerse bunu söylemen yeterli. | Mevcut depoda yalnız iskelet var; başka yerin varlığı bilinmiyor. | Dal adı/yerel yol veya “hazır değil” yanıtı. | 03-01, 03-07 ve ardından fotometri üretim entegrasyonu. | Kullanıcıya soruldu; yanıt bekleniyor. |

## Nasıl hazırlanacak?

- Karar gerekiyorsa kısa seçenekler, etkileri ve öneri sunulur; yanıt gelmeden karar verilmez.
- Hesap/erişim gerekiyorsa yerel kurulum yolu gösterilir; şifre veya anahtar sohbetten istenmez.
- Etiketleme gerekiyorsa önce örnek veri, etiket sözlüğü, kalite ölçütü ve küçük pilot hazırlanır; sonra uygun araç/skill araştırılır. Kurulumdan önce gerçek ihtiyacı doğrula.
- Ücretli makine veya harcama gerektiğinde maliyet ve amaç sunulur; onay olmadan kiralama yapılmaz.
- Dışarıya mesaj gönderme veya ekip üyesinden bilgi isteme gerekiyorsa kullanıcıya iletilebilir kısa taslak hazırlanır; kendiliğinden gönderilmez.

Henüz gerekmeyen olası işler gerçek bekleyen adım gibi listelenmez. Ekip arayüzü eksikleri [NOW.md](NOW.md) içinde teknik bağımlılık olarak tutulur.
