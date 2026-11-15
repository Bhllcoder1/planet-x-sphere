# 04-12 — Hedef/kontrol yıldızı fotometri bağlantısı

Uygulama: `b_astrometri/motion/lightcurves.py` içindeki `produce_target_control_lightcurves`.

API:

```python
result = produce_target_control_lightcurves(
    target_name, target_ra_deg, target_dec_deg,
    control_name, control_ra_deg, control_dec_deg, frames,
    bin_width_um=channel_width_um,
    coverage_status="covered",  # unknown / no_coverage / partial da açıkça seçilebilir
    coverage_reason=coverage_evidence,
    output_dir=output_directory,
)
```

`frames`, yeni `forced_phot(ra, dec, frames)` fonksiyonunun gerçek EPSF, düzeltilmiş kesit WCS, native görüntü/varyans/bayrak, MJD, pass, normalize etme ve birim sözleşmesini taşır. Hedef ve kontrol koordinatları çağırandan gelir; hedef kendisinin kontrolü olarak kabul edilmez. Her iki kaynak **aynı kare listesinde** ayrı ölçülür.

Hedef ve kontrolün tam geçerli eğrileri ayrı tutulur. Karşılaştırma yalnız her iki ölçümün başarılı olduğu **aynı frame/pass/dedektör/release/λ kutusu** çiftlerinden yapılır. Farklı dedektör/release ölçümleri aynı eğride karıştırılmaz; aynı dedektör/release içinde farklı görüntü birimi veya EPSF normuyla gelen veri reddedilir. Kontrol farklı bir LVF kutusuna düşerse o kare karşılaştırmaya alınmaz ve nedeni kaydedilir; geçerli hedef noktası kendi eğrisinde korunur.

İki karşılaştırılabilir geçiş yoksa kontrol için `control_within_3sigma=None`, `control_assessment=not_measured` yazılır. Ölçülmemiş bir kontrol sabit ilan edilmez. Ölçülen kontrolün sonucu yalnız `consistent_with_constant_at_3sigma` veya `change_exceeds_3sigma` olabilir; bu sonuç kontrolün fiziksel olarak kesin sabit olduğunu kanıtlamaz. Doygun-fit rozetleri ve kareye özgü CWAVE/CBAND bilgisi korunur.

Boş `unknown` kapsam, arşiv hatası/bilinmiyor olarak kalır; `no_coverage` yalnız çağıranın doğrulanmış kapsam kararıyla kullanılır. Kapsam yokken kare verilmesi veya kapsam var denirken kare listesinin verilmemesi hata sayılır. Eksik veya başarısız fotometri hiçbir yerde sıfır akıya çevrilmez.

`output_dir` verilirse mevcut JSON/SVG yazıcısı `target/` ve `control/` altında iki eğriyi, ek `target_control_comparison.json` da ortak değerlendirme ve kare eşlemesini yazar. Akılar mevcut modülün **uncalibrated_model_amplitude** birimindedir; fiziksel akı kalibrasyonu doğrulanmış sayılmaz.

## Kabul durumu

Kullanıcı yeni test istemedi; **bu dilimde yeni test eklenmedi veya test çalıştırılmadı**. Kaynak akışı statik olarak incelendi; bu dilimin runtime/compile doğrulaması da yapılmadı. Bu, kullanıcının üretim veri işlemesini yasakladığı anlamına gelmez. Gerçek RW Aur/R Dra kareleri ve uygun kontrol yıldızı sağlanmadığı için gerçek ışık eğrisi, R Dra değişimi ve 3σ kontrol kabulü üretilmedi. 04-03/04-01, kanonik kapsam ve gerçek WCS/EPSF doğrulaması bekleyen önkoşullardır. Bu bağlantı 04-12 tamamlandı anlamına gelmez.
