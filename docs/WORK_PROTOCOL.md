# Çalışma protokolü — 00-05

Ekip büyüklüğünden bağımsız görev seçimi, üstlenme ve kapanış kuralları. Görev açıklamalarına kişi adı veya tarih eklenmez; çalışma kayıtları açıklamadan ayrı tutulur.

## Yedi kural

1. **Hazır işi seç.** İş 0,5–6 saatlik ve tek başına yapılabilir olmalı; `ÖNCE` alanındaki bütün görevler kapalı olmalı. Yerel dosyanın bulunması veya eski rapor, önkoşulun kapandığını kanıtlamaz. Açık önkoşul varsa işi beklet; bağımsız araştırmayı uygulama/tamamlama olarak sunma.
2. **Sırayı koru.** Hazır işler arasında önce öncelik 1, sonra `demo-5-gün` etiketi, sonra liste numarası gelir. Eşitlikte görev kimliğini kullan. Beceri etiketi işin gereksinimidir; mevcut hesap ataması korunur ve yalnız yetkili olunan alandan iş alınır.
3. **Çakışmayı önle.** Başlamadan hemen önce durumu ve mevcut üstlenme kaydını yeniden oku. Görevde yalnız oturum kimliği/zaman damgası içeren `üstlenildi` kaydı tut; çalışan oturumun işini ikinci kez alma. Harici yorum yetkisi yoksa yazma: yerel üstlenmeyi kaydet, bunu ekip çapında kilit sayma ve mevcut eşgüdümcü üzerinden tek sahibi belirle.
4. **Küçük ve tek çıktılı çalış.** Bir ajana tek kısa görev, tek çıktı dosyası ve açık KABUL/KANIT ver; sonuç gelince işi gözden geçir. Aynı dosyaya iki ajan yazmaz. Bir ClickUp görevi birden çok dosya gerektiriyorsa ayrı dosya sahipliği olan kısa alt briflere ayır; model kademeleri 00-06'nın konusudur.
5. **Altı saati aşanı böl.** İş 6 saati aşacaksa durumu kaydet; bağımsız kabul ölçütleri ve önkoşulları olan yeni görev kimlikleriyle böl. Harici görev oluşturma yetkisi yoksa önce yerel taslak çıkar; açılmış görev gibi gösterme. Eski görev yeni kimlikleri referanslamadan tamamlanmaz.
6. **Kanıtla kapat.** KABUL sayıları sağlanır, test/log/çıktı yolu KANIT olarak kaydedilir ve kapatılan bilinmeyenin `[V]`/`[NV]` etiketi güncellenir. Varsayım `[ASSUMPTION]` kalır. Eksik, başarısız veya çalıştırılmamış kontrol açıkça yazılır; yerel bitiş ile ClickUp kapanışı ayrı kaydedilir.
7. **Devri açık bırak.** Sonuç, değişen dosya, doğrulama ve sonraki adım kalıcı kayda yazılır. Kullanıcı kararı, hesap erişimi veya elle etiketleme gerekiyorsa ilgili adım durdurulur ve yanıt beklenir; bağımsız işler sürer. Üstlenme bırakılıyorsa nedenini ve kalan işi kaydet; sessizce başka işe geçme.

## Üç adayla seçim denemesi

Kaynak: API'den alınan yerel görev anlık görüntüsü; aşağıdakiler prova değerlendirmesidir, gerçek üstlenme veya kapanış değildir. Okunan görevlerin tamamı `to do` olduğundan açık önkoşul kapalı varsayılmadı.

| Aday | Kontrol | Prova sonucu ve tek çıktı |
|---|---|---|
| [00-05](https://app.clickup.com/t/z8qu5ddjv6) | Öncelik 1; demo; ÖNCE: yok; rapor/karar becerisi | Hazır; ilk seçim. Tek sahip/oturum, `docs/WORK_PROTOCOL.md`. |
| [08-01](https://app.clickup.com/t/z8qu5ddjz8) | Öncelik 2; demo; ÖNCE: yok; rapor becerisi | Hazır; 00-05 ile dosyası farklı olduğundan ayrı sahipte çakışmadan yürüyebilir. Tek çıktı: `b_astrometri/reports/hedefler_sablon.md` (ürün deposundaki yer önerisi; görevin eski çıktı yoluyla eşleme kaydı gerekir). |
| [01-03](https://app.clickup.com/t/z8qu5ddjvj) | ÖNCE: 01-01; bu önkoşul anlık görüntüde `to do` | Uygulama seçimi bekler. Yerel ortam doğrulaması kanıtı hazırlanabilir; önkoşul kapanışı teyit edilmeden görev hazır sayılmaz. Karar notu: `docs/GAIA_FETCH.md`; indirme/test işleri ayrı dosya brifleri olur. |

Sonuç: iki bağımsız adayın dosya sahipliği ayrıldı; üçüncü aday açık önkoşulda durduruldu. Aynı görev veya çıktı iki oturuma verilmedi. Harici üstlenme/kapanış işlemi bu prova ile yapılmadı.

Kaynaklar: yerel `spherex-kb/clickup/BRIEF.md` (Task format, Rules), [plan v3 §4.3](plan/PLAN_spherex_v3.md), [görev dizini](second-brain/TASKS.md). Asıl 00-05 kabulü yedi kural ve üç adaylık seçim notudur; bu sayfa görevlerin bilimsel kabul koşullarını değiştirmez.
