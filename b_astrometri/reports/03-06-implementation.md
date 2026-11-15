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
- Sayısal Jacobian blok-seyrektir: bütün pikseller ortak iki gök konumuna, her kare yalnız kendi akı/arka planına bağlıdır. `least_squares(jac_sparsity=...)` kullanılır; kovaryans için tam `JᵀJ` yoğunlaştırılıp terslenir, yalnız köşegen bloklar alınmaz.

## Doğrulama

Komut:

```powershell
& 'C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe' -I -m unittest discover -s 'C:/Users/behlu/planet-x-sphere/b_astrometri/centroid' -p test_joint_fit.py -v
```

`test_joint_fit.py` dört kontrol içerir:

Son koşu: **[V] 4 test geçti, 1.165 s**; aşağıdaki kontroller bu komutla çalıştırıldı. Aynı dört testin önceki yoğun Jacobian koşusu 9.127 s idi; gözlenen test süresi yaklaşık 7,8 kat azaldı (tekil koşular, kararlı performans garantisi değil).

1. Sabit tohumlu, 20 sentetik kare ve iki açık dışlama: değişen roll, akı ve arka planla ortak uyum; her eksende ortak σ tek kare σ/3'ten küçük, konum hatası 3σ'dan küçük. Tam kovaryans pozitif, elipsle tutarlı; kare χ² toplamı genel χ² ile aynı; JSON gidiş-dönüşü kayıpsızdır.
2. Bütün karelerin reddedildiği durumda açık `unmeasurable` ve üç gerekçeli dışlama.
3. Boyut uyuşmazlığı ve geçersiz başlangıç koordinatlarının reddi.
4. Geçersiz JSON sayısının mevcut ürün dosyasını değiştirmemesi.

Bu 20 kare testi **1000 denemeli 1σ kapsama testi değildir**. 3σ eksen kontrolünü görevin %39,3'lük iki boyutlu 1σ kapsaması gibi sunma.

## Kapanışı engelleyenler — [NV]

- 1000 bağımsız 20-kare denemesi başlatıldı; tamamlanmış sonuç henüz okunmadı. İlerleme kanıtındaki `complete` ve `completed_trials` alanlarını kontrol et; kısmi sonuç tam koşu değildir.
- Gerçek Barnard geçişi, düzeltilmiş WCS girdileri ve gerçek ePSF ile tek-kare/ortak σ karşılaştırması yapılmadı. Görevin 03-03/03-09 önkoşulları kanıtlanmadan gerçek veri kabulü ileri sürülmez.
- Başlangıç için tek-kare konumlarının ağırlıklı ortalamasını hazırlayan entegrasyon yok; çağıran başlangıcı veriyor.
- χ² aykırı kareleri otomatik sınıflayan, kalibre edilmiş eşik/karar politikası yok; kare tanıları sunuluyor.
- Kovaryans yalnız verilen görüntü varyansının biçimsel belirsizliğidir; WCS sistematikleri, kareler arası korelasyon ve geçiş içi öz hareket dahil değildir.
- Barnard'ın geçiş boyunca hareketi sabit konum varsayımını bozabilir. Orta epoğu yazmak bu hareketi düzeltmez; gerçek sonuçta artıklar ve model yeterliliği ayrıca incelenmelidir.

Sonuç: dosyaya aktarılabilir konum/kovaryans/χ² çıktısı ve hata kontrolleri mevcut; **03-06 bütünü tamamlanmış değildir**. ClickUp değiştirilmedi.

## Tekrarlanabilir kapsama deneyi

`b_astrometri/centroid/joint_coverage.py`, deterministik 20-kare testinin değişen roll/akı/arka plan düzenini kullanır. Her deneme bağımsız `SeedSequence([55, deneme_no])` gürültüsüyle üretilir; ortak konum hatası tam 2×2 kovaryans üzerinden Mahalanobis² ≤1 ile sayılır. Beklenen 2B Gauss kapsaması `1-exp(-1/2)` = yaklaşık %39,3469'dur. Tabloda biçimsel kovaryans, tek-kare/ortak σ oranları, başarısızlıklar ve süre tutulur. Üretim ve uyum aynı sentetik ePSF'i kullanır; bu gerçek veri sistematiklerini sınamaz.

```powershell
& 'C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe' -I 'C:/Users/behlu/planet-x-sphere/b_astrometri/centroid/joint_coverage.py' --trials 1000 --seed 55 --output 'C:/Users/behlu/reports/03-06-coverage.json'
```

Ön kontrol `[V]`: `--trials 2` ile 2/2 uyum başarılı, 2.459 s; kanıt `C:/Users/behlu/reports/03-06-coverage-smoke.json`. İki örnek kapsama kararı için yeterli değildir. 1000 denemelik koşu başlatıldı; her 25 denemede kanıt atomik yenilenir. Sonuç bitmeden başarı veya kapsama uyumu iddia edilmez. Smoke hızından kaba süre 20,5 dakika `(arit) [ASSUMPTION]`; koşu sırasında değişebilir.
