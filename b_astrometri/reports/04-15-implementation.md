# 04-15 — Kayan pencere ve pencere-dışı farkı

Yerel uygulama: `b_astrometri/motion/rolling.py`, `test_rolling.py`.
Görev: https://app.clickup.com/t/z8qu5ddjxh

## Davranış

- Girdi, 04-02 `stack_pass` kare sözleşmesi + sonlu UTC `mjd` alanıdır.
- Pencere `[başlangıç, başlangıç + gün)` biçiminde: sol sınır dahil, sağ sınır hariç.
- Uzunluk verilmezse sağlanan geçiş zaman aralığının üçte biri kullanılır `[ASSUMPTION]`. Sıfır zaman aralığında uzunluk açıkça verilmelidir.
- Aynı dedektör, geçiş, release ve tek kanal genişliği zorunludur. Dalga boyu farkı sessizce hareket gibi sunulmaz.
- İç ve dış kareler `stack_pass` üzerinden hedef TAN WCS ızgarasına aktarılır. Fark `iç yığın - dış yığın`dır; bu yığınlar ortak giriş karesi içermez.
- `+`: pencere katkısı, `-`: pencere-dışı referans katkısı, `.`: kullanılmayan kare. Bunlar bu pencerenin rolleridir; önceki pencereye göre ekleme/çıkarma animasyonu değildir.
- İki kareden az veya iki geçerli piksel katkısından az olan yerde ölçüm uydurulmaz: ürün yok ya da NaN olur. Boş/örtüşmeyen tarafların durumu ayrıca yazılır.
- Her ürün S modu, yalnız görüntüleme ve **“Yeniden örneklendi — astrometri yok”** rozeti taşır. Native ölçüm verisi değiştirilmez.

## Doğrulama ve sınırlar

Çevrimdışı testler pencere sınırlarını, varsayılan uzunluğu, iç-eksi-dış işaretini, rol listesini, maskeli/NaN/bayraklı pikselleri, geçersiz varyansı, değişmez girişleri ve farklı native WCS üzerinden gerçek `reproject_exact` yolunu kapsar. Sentetik sabit kaynaklar ve bağımsız gürültü denemesi ayrı testtir; bunlar gerçek Gaia/Barnard kabul kanıtı değildir.

8/8 odaklı test geçti. Sabit seed 20261115 ile hizalı 32×32 sentetik karelerde, 1021 boş-gök pikselinin gürültü oranı **1,01010**; üç sentetik sabit-kaynak pikselinde ortanca mutlak fark **0,21404σ** bulundu. Örtüşmeyen geçerli iç/dış kapsamlar `no_common_coverage` ve NaN fark verir. Bu sayılar yalnız bu sentetik denemenin kanıtıdır.

Ortak yeniden örnekleme modülü, varyans düzleminden gelen **nominal** diyagonal gürültüyü bildirir; yeniden örnekleme kovaryansı henüz yayılmaz. %20 gürültü sınaması yalnız hizalı sentetik bağımsız örnekler için geçerlidir. PSF eşleştirmesi yapılmaz.

Bekleyen önkoşullar: 04-01 kanonik geçiş listesi, 04-02 gerçek veri yığın kabulü ve 02-16 gösterim katmanı bağlantısı. Gerçek Gaia sabit yıldız kalıntı grafiği ve Barnard kayan pencere örneği henüz yoktur. Bu dosya görev kapanışı veya yarışma kabulü değildir.

```powershell
& 'C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe' -I -m unittest discover -s b_astrometri/motion -p test_rolling.py -v
```
