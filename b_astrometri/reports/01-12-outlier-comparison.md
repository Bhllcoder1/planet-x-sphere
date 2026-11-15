# 01-12 — R27 OUTLIER hafta/işleme karşılaştırması

**Durum: kaynak kod dilimi; çalıştırılmadı, bilimsel sonuç üretilmedi [NV].** Kullanıcının yeni testleri atlama talimatına uyuldu; test dosyası eklenmedi. Bu dilimin kaynak incelemesiyle sınırlandırılması çalışma kapsamı tercihidir; kullanıcı bütün üretim kodu/veri işlemeyi yasaklamadı. Önkoşul 01-09'un kapanışı bu çalışma ile ileri sürülmez.

## Hazırlanan

`b_astrometri/movers/outlier_comparison.py` içindeki `compare_outlier_frames(frames)` on karelik çağıran verisini kabul eder. Her karede şu alanlar zorunludur:

- `flags`: iki boyutlu tamsayı FLAGS penceresi; ham veri kopyalanmaz/değiştirilmez.
- `frame_id`, `week` (`YYYYWww` arşiv etiketi), `procver`, `field_id`, `region_id`, `release`.
- `detector`: 1–6; `sparse_field=True`: seyrek alan seçiminin çağıran tarafından açık beyanı.
- İsteğe bağlı `region_mask`: her karede aynı gök bölgesini seçen boolean örneklem desteği. Bu, kalite maskesi değildir.

Modül alan A'daki gerçek `a_veri_isleme.process.masks` sabitlerini kullanır: **OUTLIER bit 19**, **SOURCE bit 21** (Explanatory Supplement Tablo 16). Payda bölge desteğindeki bütün piksellerdir; OUTLIER/SOURCE veya fit-mask bitleri kalite gerekçesiyle paydadan çıkarılmaz. Her kare için piksel sayısı, OUTLIER/SOURCE/ikisinin birlikte sayısı ve 0–1 arası kesirler verilir. Yüzde gerekiyorsa kesir ×100'dür.

Karşılaştırma aynı alan/bölge/dedektör/release/pencere boyutu/örneklem sayısıyla sınırlandırılır; tekrar kare kimliği, boş örneklem ve bilinmeyen maskeli bayraklar reddedilir. En az iki farklı hafta gerekir. Her `(hafta, procver)` grubu için piksel ağırlıklı oranlar ve kare sayıları hazırlanır. Aynı procver'de birden fazla hafta ve aynı haftada birden fazla procver bulunup bulunmadığı ayrıca gösterilir; bunların bulunması nedenselliği kanıtlamaz.

**Kontrol sınırı:** metadata ve aynı dizi şekli tek başına gök ayak izinin aynı olduğunu kanıtlamaz. `region_id`, WCS dönüşleri boyunca aynı gök desteğini ve seyrek alanı gerçekten ifade etmelidir; bunu kare seçimi tarafı sağlamalıdır. Farklı piksellere karşılık gelen, aynı isimli bölgeleri bu modül kendiliğinden keşfedemez. NaN/eksik FLAGS değerleri sessizce 0 bayrak sayılamaz.

`write_outlier_comparison(result, output_directory)` görevdeki `outlier_by_week.csv` ve eşlik eden `outlier_by_week.json` dosyalarını çağıranın verdiği dizine yazar. Amaç dış veri dizini, örneğin `C:/Users/behlu/spherex-kb/stage0/data/D/` kullanmaktır; depoya bilimsel veri eklenmez. Yazma işlemi atomik bir iki-dosya işlemi değildir.

## Kanıt ve eksik kalanlar

Kaynaklar okundu: canlı 01-12 görev açıklaması (`reports/clickup-live-assigned.json`), `docs/research/notes_expsupp.md` Tablo 16 notları ve `a_veri_isleme/process/masks.py`. Bu, kaynak incelemesidir; yeni sayısal doğrulama değildir.

- Aynı seyrek alandan farklı haftalara/işleme etiketlerine ait on gerçek kare seçilmedi; gerçek FLAGS üzerinde çalıştırma yapılmadı.
- On gerçek satırlık CSV/JSON henüz üretilmedi; **2025/2026 oranları uydurulmadı**.
- `s0_D` ve 00-12 kayıtları değiştirilmedi; görev bunları gerçek veri sonucu oluşunca gerektirir.
- Çıktının hazır sonuç cümlesi bilerek “neden bilinmiyor [NV]” der ve `risk_R27_closed=False` döner. Gözlenen ilinti dahi veri incelenmeden ilan edilmez.
- Kod derlenmedi, yeni test yazılmadı/koşturulmadı. Sonraki üretim veri adımı gerçek on-kare seçimi ve çıktı kontrolüdür; bunun için kullanıcıdan genel çalışma yetkisini yeniden istemek gerekmez.

**01-12 tamamlandı sayılmaz:** kabul, on gerçek karelik tablo ve dürüst gözlemsel sonuç gerektirir. Bu dilim yalnız hesaplama/çıktı yolunu hazırlar; hareketli cisim adayı üretmez ve bayrakların fiziksel nedenini çözmüş gibi davranmaz.
