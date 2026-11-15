# 03-06 — Ortak geçiş uyumu: çıktı dilimi

## Uygulanan

`b_astrometri/centroid/joint_fit.py` aynı gök konumunu her karenin kendi WCS/ePSF'i üzerinden uydurur; akı ve sabit arka plan kare başına serbesttir. Görüntü yeniden örneklenmez. Başlangıç konumu çağırandan gelir.

Sonuç `pass_position` sözlüğüdür; `write_pass_position(result, path)` bunu katı JSON olarak yazar. `NaN`/`Infinity` yazılmadan reddedilir; bu durumda mevcut dosya değiştirilmez. Normal dosya sistemi yazma hatalarına karşı atomik/işlemsel kayıt vaat edilmez.

Eklenen çıktılar:

- `covariance_tangent_arcsec2`: doğu/kuzey teğet konumunun tam 2×2 kovaryansı; kare başına akı/arka plan dahil bütün parametrelerin ters normal matrisinden alınır.
- `covariance_radec_deg2`: aynı kovaryansın RA/Dec derece² karşılığı; RA dönüşümünde `cos(dec_init)` korunur. Elips doğu/kuzey yay saniyesindedir.
- Toplam `chi2`, `dof`, `chi2_nu`; `frame_diagnostics` içinde her karenin piksel sayısı, χ² ve χ²/piksel. Bunlar gözden geçirme tanılarıdır; keyfî eşikle otomatik dışlama yapılmaz. Kare başına paylaştırılmış serbestlik derecesi iddiası yoktur.
- Geçerli kare zamanlarının min/max orta noktası `epoch_mid_mjd`; bu çıktı sabit konum modelinin fiziksel olarak yeterli olduğunu kanıtlamaz.
- Biçimsiz veri boyutları/geçersiz başlangıç konumu reddedilir; yakınsama başarısızlığı `ok` sayılmaz. Kötü ve kullanılamaz kareler neden ve sayılarıyla korunur.

## Doğrulama

Komut:

```powershell
& 'C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe' -I -m unittest discover -s 'C:/Users/behlu/planet-x-sphere/b_astrometri/centroid' -p test_joint_fit.py -v
```

`test_joint_fit.py` dört kontrol içerir:

Son koşu: **[V] 4 test geçti, 9.127 s**; aşağıdaki kontroller bu komutla çalıştırıldı.

1. Sabit tohumlu, 20 sentetik kare ve iki açık dışlama: değişen roll, akı ve arka planla ortak uyum; her eksende ortak σ tek kare σ/3'ten küçük, konum hatası 3σ'dan küçük. Tam kovaryans pozitif, elipsle tutarlı; kare χ² toplamı genel χ² ile aynı; JSON gidiş-dönüşü kayıpsızdır.
2. Bütün karelerin reddedildiği durumda açık `unmeasurable` ve üç gerekçeli dışlama.
3. Boyut uyuşmazlığı ve geçersiz başlangıç koordinatlarının reddi.
4. Geçersiz JSON sayısının mevcut ürün dosyasını değiştirmemesi.

Bu 20 kare testi **1000 denemeli 1σ kapsama testi değildir**. 3σ eksen kontrolünü görevin %39,3'lük iki boyutlu 1σ kapsaması gibi sunma.

## Kapanışı engelleyenler — [NV]

- 1000 bağımsız 20-kare denemesinde iki boyutlu Mahalanobis mesafesi ≤1 kapsama sayımı ve tablosu yapılmadı.
- Gerçek Barnard geçişi, düzeltilmiş WCS girdileri ve gerçek ePSF ile tek-kare/ortak σ karşılaştırması yapılmadı. Görevin 03-03/03-09 önkoşulları kanıtlanmadan gerçek veri kabulü ileri sürülmez.
- Başlangıç için tek-kare konumlarının ağırlıklı ortalamasını hazırlayan entegrasyon yok; çağıran başlangıcı veriyor.
- Optimizasyon mevcut yoğun Jacobian'ı kullanıyor; görevdeki blok-seyrek çözücü henüz uygulanmadı.
- χ² aykırı kareleri otomatik sınıflayan, kalibre edilmiş eşik/karar politikası yok; kare tanıları sunuluyor.
- Kovaryans yalnız verilen görüntü varyansının biçimsel belirsizliğidir; WCS sistematikleri, kareler arası korelasyon ve geçiş içi öz hareket dahil değildir.
- Barnard'ın geçiş boyunca hareketi sabit konum varsayımını bozabilir. Orta epoğu yazmak bu hareketi düzeltmez; gerçek sonuçta artıklar ve model yeterliliği ayrıca incelenmelidir.

Sonuç: dosyaya aktarılabilir konum/kovaryans/χ² çıktısı ve hata kontrolleri mevcut; **03-06 bütünü tamamlanmış değildir**. ClickUp değiştirilmedi.
