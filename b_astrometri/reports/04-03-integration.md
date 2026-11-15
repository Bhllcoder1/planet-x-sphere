# 04-03 — gerçek kare sözleşmesi ve RA/Dec fotometri akışı

`b_astrometri/motion/forced_phot.py` artık `forced_phot(ra, dec, frames)` ve
`write_forced_phot_csv(path, measurements)` sağlar. Önceki piksel-dizisi uyumu korunur.

## Açık kare girdisi

Her kare: `frame_id`, `mjd_avg` (UTC), `pass_id`, aynı boyutlu 2D `image`,
`variance`, `flags`, `image_unit`, `epsf_grid`, `corrected_cutout_wcs`,
`crpix1a`, `crpix2a`, `var_scale` gerektirir. Eksik alan sessiz varsayılmaz;
`ValueError` ile bildirilir. `var_scale` Liste 03'ten gelen s≥1 çarpanıdır.
QR3/DR1 ePSF grid'i release/dedektör/bölge metadatasını taşır; karede ayrıca
release veya dedektör verilmişse uyuşması gerekir.

Düzeltilmiş WCS seçimi açık girdidir; kod 03-09 düzeltmesini üretmez veya
ham WCS'i düzeltilmiş gibi seçmez. `coordinates.sky_to_frame_coordinates`
gök konumunu kesit float pikseline, Alan A parent-piksel kuralı da parent float
konumuna taşır. Kesit penceresi sınırları dışında ölçüm `outside_cutout` olur.
RA/Dec girdisi her verilen WCS'in göksel referans çerçevesinde önceden ifade
edilmiş olmalıdır; bu akış ICRS'e veya başka referans çerçevesine otomatik dönüşüm yapmaz.
Sadece damga dizi indeksleri tam sayıdır; kaynak konumu yuvarlanmaz. 9×9 yerel
damganın x/y örnekleri parent koordinatlarına taşınarak ePSF parent konumunda
değerlendirilir. Yalnız F ve b uydurulur; kötü uyumda akı/hata yazılmaz.

`wcs_corrected=True` çağıranın seçimini kaydeder; doğrulanmış düzeltme iddiası
değildir. Yanında `wcs_correction_status=caller_supplied_not_verified` yazılır.
FLAGS tam sayı, negatif olmayan ve uint32 aralığında; `var_scale` sonlu ve ≥1
olmalıdır. Bu kontroller hedef kesit dışında olsa da uygulanır.

CWAVE/CBAND varsayılanı gerçek ePSF bölgesinin **temsilî** değeridir ve kökeni
satırda açık yazılır; bu kaynak başına bilimsel spectral-WCS kalibrasyonu değildir.
Gerçek kalibre edilmiş değerler varsa `cwave_um`, `cband_um`, `spectral_source`
üçlüsüyle verilir. Fiziksel akı normalizasyonu 03-02'de açık olduğundan F çıktısı
`uncalibrated_model_amplitude`, `physical_flux_validated=False` olarak etiketlenir;
MJy/sr→mJy dönüşümü veya fiziksel kaynak akısı iddiası yapılmaz.

## Bayraklar

Uyum maskesi Alan A `PROFILE_CENTROID_MASK` sabitinden alınır. Uyarılar Table16'ya
göre TRANSIENT0, CROSSTALK20, HALO28 ve PERSIST17'dir. Eski HOT10/PHANMISS14/
OUTLIER19/SOURCE21 uyarı eşlemesi kaldırıldı. Alan A'nın eski BIT_PERSIST15
sabiti kullanılmaz; belgeye göre 15 NONLINEAR, 17 PERSIST'tir.

Sabit temel maskede HALO28/PERSIST17 zaten bulunmaktadır; uyarı eklemek bu
pikselleri uyumda yeniden kullanılabilir yapmaz. Görevdeki sabit maskeyi sessizce
değiştirmiyoruz. `saturated_fit`, çekirdekte NaN/OVERFLOW olduğunda konur;
yalnız başka bir maske biti veya geçersiz variance doygunluk diye sunulmaz.

CSV satırları kare/MJD/pass, dedektör/release, float konumlar, λ/bant genişliği,
F/σF/b/χ², durum ve bayraklar, maske, s, ePSF çarpanı ve birim durumunu taşır.

## Doğrulama ve kalanlar

Kullanıcının **şimdi test çalıştırmama** isteği doğrultusunda yeni test eklenmedi
ve hiçbir test/deneme çalıştırılmadı. Bu değişiklik çalıştırılarak doğrulanmış
veya ClickUp kabulünü geçmiş sayılmaz. Gerçek düzeltilmiş WCS/kare sözleşmesi,
03-02 fiziksel ePSF normalizasyonu, D13 akı enjeksiyonu RMS/σ kabulü ve Barnard
NaN çekirdek çıktısı gerçek verilerle hâlâ doğrulanmalıdır. Sahte ölçüm veya
başarı tablosu üretilmedi. CVAT/elle etiketleme gereksinimi saptanmadı.
