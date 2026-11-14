# Şu an

## Aktif kapsam

Behlül Anik'e atanan işleri bağımlılık sırasıyla uygulamak. İlk somut hedef: **01-03 Gaia erişimi**. Kullanıcı ajanlarla çalışmayı istedi. Dış sistemde görev kapatma, yorum veya mesaj gönderme henüz yapılmadı.

İkinci paralel dalga: 03-01 bağımsız ePSF prototipi ve 03-07 epoch dönüşümü. Üretim entegrasyon önkoşulları açık; prototipler görev kapanışı değildir. İnsan gerektiren işler [HUMAN_ACTIONS.md](HUMAN_ACTIONS.md) içinde tutulur; H-01 diğer dal/klasördeki Akif çıktılarının yerini soruyor. Yanıt gelene kadar üretim entegrasyonu bekler, bağımsız testler sürer.

## Doğrulanan durum — 2026-11-15

- [V] ClickUp API hesabı Behlül Anik; Planet XSphere çalışma alanında 199 görevden 46'sı bu hesaba atanmış. Okunan anlık görüntüde 46'sı da `to do`.
- [V] Ürün deposu `C:/Users/behlu/planet-x-sphere`; başlangıçta çalışma ağacı temiz ve ürün alanları iskelet halinde.
- [V] Deney betikleri/veriler `C:/Users/behlu/spherex-kb/stage0` altında; ürün deposunda değiller.
- [V] Eski ESA betiği `c6_gaia.py` başarısız karolara rağmen kısmi birleştirilmiş çıktı yazabiliyor.
- [V] Eski MAST betiği `c9_vizier.py` OVERFLOW sonucunu yalnızca uyarıp kabul ediyor. Yeni çözüm eksik/kesilmiş kataloğu tam gibi sunmamalı.
- [NV] Bu oturumda Gaia sağlayıcılarının canlı performansı ve B karesinin 4/4 karo sonucu henüz ölçülmedi.

## Devam et

1. 01-01 ortam önkoşulunu paket sürümleriyle doğrula; ClickUp'ta `to do` görünmesi yerel ortamın eksik olduğunu kanıtlamaz.
2. 01-03 kabulü: ESA küçük karo/yeniden deneme, alternatif ayna ve ABD makinesi seçeneklerinin her biri için [V]/[NV] satırı; B için 4/4 tam karo veya açık başarısızlık kaydı.
3. `b_astrometri/gaia/` altında en küçük yeniden kullanılabilir çözümü kur. Önbellek, sütun denetimi ve QUERY_STATUS denetimi ekle.
4. Anlamlı çevrimdışı testler ve ayrı canlı denemeyle doğrula; `docs/GAIA_FETCH.md` içine süre/başarı/kanıt yaz.
5. Sonra 03-01 → 03-02 → 04-03; her birinin açıklamasındaki diğer kişilere bağlı önkoşullarını başlamadan kontrol et.

## Oturum kaydı

- Second brain oluşturuldu; sadece görev/karar/kaynak bilgileri kaydedildi.
- Gaia denetimi ajanı mevcut betiklerdeki kısmi sonuç ve OVERFLOW risklerini bağımsız olarak bildirdi.
- [V] Ajanın yerel önbellek okuması: B'nin dört MAST karosu 15.734 / 16.515 / 17.514 / 18.761 satır; birleşik dosya 55.137 kaynak, 11 sütun ve ref_epoch=2016.0. Bu, tarihsel kesilmenin olmadığını veya canlı erişimi kanıtlamaz.
- Kullanıcı 2026-11-15: paralel ajanlarla ilerle; karar/hesap/elle işlem için gerçekten kullanıcı bilgisi gerekiyorsa ilgili adımı durdur ve yanıtını bekle. Etiketleme gerekirse CVAT vb. araçları ve uygun becerileri değerlendir; henüz etiketleme gereksinimi saptanmadı.
- [V] Canlı küçük koni denemesi: ESA HTTP 200 ve QUERY_STATUS=OK (2,77 sn); MAST HTTP 200 fakat OK ardından OVERFLOW (1,32 sn). Kanıt: depo dışında `reports/gaia-live-probes.json`. B'nin dört karosu henüz denenmedi.
- [V] Ortam denetimi: mevcut Stage 0 venv Python 3.14.0, astropy 8.0.2, photutils 3.1.1, numpy 2.5.4, scipy 1.18.1, requests 2.34.2. SEP yok. Bu temiz kurulum/bağımlılık kilidi doğrulaması değildir.
- 00-05 yerel çıktısı hazır: [çalışma protokolü](../WORK_PROTOCOL.md), yedi kural ve üç görevle seçim provası. ClickUp kapanışı yapılmadı.
- 08-01 yerel çıktısı hazır: [hedef raporu şablonu](../../b_astrometri/reports/hedefler_sablon.md), altı bölüm ve tarihsel Barnard/bilinmeyen WISE 0855 doldurma provası. Yeni bilimsel ölçüm yapılmadı; ClickUp kapanışı yapılmadı.
- Gaia küçük karo alternatifi başarılı: 16/16 canlı sorgu, 49.176 tekil kaynak, 67,364 sn; 11 çevrimdışı erişim testi geçti. Büyük dört karo 2/4 kaldı; küçük koniler aynı pencereyi kapsıyor. Kanıt `reports/gaia-B-small-live-result.json` (depo dışında). Önkoşul/ClickUp kapanışı ayrı ve açık.
- ePSF prototipi: 6 test ana oturumda geçti; gerçek D2 441×33×33/5×5, üç konum self-recovery 0 px. Görüntü/JSON kanıtları [IMPLEMENTATION.md](IMPLEMENTATION.md) içinde. Fiziksel normalizasyon ve üretim entegrasyonu açık.
- Epoch prototipi: kutup hatası düzeltildi; son 11 epoch + 11 erişim testi ana oturumda geçti. 6 ePSF testiyle toplam 28 test. Barnard tahmin tablosu son yöntem ve kesin kaynak yollarıyla IMPLEMENTATION.md içinde. Üretim entegrasyonu açık.
- Kullanıcı Jev TypeSafe v1.14 görüntü desteğini incelemeyi ve TypeSafe becerisini projeye kurmayı istedi. Tek npx yöntemiyle `.agents/skills/typesafe-ai/` kuruldu, SKILL.md okundu. Görüntüler/Box resmi belgede halen dreamer-ready; canlı API denemesi yapılmadı. Bilimsel doğruluk veya güven puanı hakkında test edilmemiş iddia yok.
- Graphify kalıcı grafiği kuruluyor: hedef kapsam yeni kod + proje hafızası; eski araştırma/plan arşivleri kapsam dışında. Dosya notları asıl hafıza, grafik anlık türetilmiş dizindir.

## Sonraki işlerin bağımlılıkları

- 03-01: 02-03 koordinat ve 02-12 L1 önbellek arayüzlerini bekler; sentetik/yerel FITS prototipi bağımsız hazırlanabilir.
- 03-02: 03-01 ve 02-07 gerçek yıldız seçimini bekler. Kabulde konum kadar akı da doğrulanmalı (×1/×25 ölçeği).
- 03-07: 02-03 koordinat sözleşmesine bağlanır; saf epoch/paralaks testleri bağımsız hazırlanabilir.
- 04-03: ePSF, maskeler ve WCS düzeltmesiyle gerçek veri bütünleştirmesi gerekir.
- Gaia, ePSF ve sentetik kaynak testleri için CVAT/elle etiketleme gereksinimi saptanmadı.
