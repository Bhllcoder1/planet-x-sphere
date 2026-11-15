# Uygulama kanıtları — 2026-11-15

## Gaia erişimi — 01-03

[Karar ve çalıştırma notu](../GAIA_FETCH.md). ESA küçük karo alternatifi canlı 16/16 sorguda aynı B penceresini kapsadı; 49.176 tekil kaynak, 67,364 sn. Büyük karolar 2/4 kaldı; küçük sorguyla çözüm bulundu. 11 erişim testi geçti. Kaynak: `b_astrometri/gaia/fetch.py`.

Tüm seçeneklerin [V]/[NV] tablosu notta var. ABD makinesi denenmedi. Önkoşul 01-01'in temiz kurulum/kilit dosyası kabulü ve ClickUp kapanışı açık; yerel mevcut ortam çalışıyor.

## ePSF prototipi — 03-01

Kaynak: `b_astrometri/centroid/epsf.py`, altı çevrimdışı test ana oturumda geçti. Gerçek D2 FITS: 441×33×33 örnek, 5×5 oversampling, ham toplam 0,9999999999999998–1,0000000000000002. Üç konumda noiseless self-recovery maksimum 0 px; model genliği bağıl hatası 2,09×10⁻¹⁴. Bu fiziksel akı normalizasyonunu kanıtlamaz.

Kanıtlar depo dışında:

- `C:/Users/behlu/reports/epsf-real-smoke.json`
- `C:/Users/behlu/reports/epsf-detector2-region220.png`

Ajan ayrıca dokuz gerçek FITS'te D2/D3/D6 okudu; D3'te 451 bölgeyi doğruladı. Bağımsız 03-02 normalizasyon/yönelim ve 02-03/02-12 üretim entegrasyonu bekliyor. PSF_NORM=1; sonuç fiziksel akı diye kullanılmaz.

## Epoch prototipi — 03-07

Kaynak: `b_astrometri/gaia/epoch.py`. Son **11 epoch testi ana oturumda geçti**: astropy uzay hareketi, pmra cos(dec), farklı referans epokları, paralaks işareti, bağımsız gözlemci geometrisi, RA sarımı ve iki kutup. İncelemenin bulduğu kutup hatası normalize edilmiş Kartezyen gözlemci çıkarımıyla düzeltildi; birinci derece tangent farkları yalnız tanı alanlarıdır. Erişim testleriyle toplam 22 Gaia testi, ayrıca 6 ePSF testi geçti.

RV açık parametre; sessiz sıfır yok. Distance floor yalnız uzay hareketinde; imzalı paralaks gözlemci teriminde korunur. Kovaryans belirsizliği hesaplanmıyor; çıktı bunu açıkça belirtir. HEALPix/sorgu seçimi ve 02-03 entegrasyonu bekliyor.

### Barnard tarihsel katalogdan tahmin provası

Gaia source_id 4472832130942575872; gerçek `stage0/data/C/gaia_A.fits` girdisi ve `stage0/data/C/hdr_A.txt`, `hdr_B.txt`, `hdr_C.txt` başlıkları. RV=0 km/s `[ASSUMPTION: eski deney tercihi]`; gözlemci Dünya merkezi, uzay aracı değil. Aşağıdakiler **ölçülen konumlar değil**, son vektörel yöntemle hesaplanan tahminlerdir. Kesin girdi/sürüm/meta ve değerler `C:/Users/behlu/reports/gaia-epoch-barnard.json` içinde.

| Kare | MJD UTC | RA tahmin (deg) | Dec tahmin (deg) | Paralaks ΔRA* (mas) | Paralaks ΔDec (mas) |
|---|---|---|---|---|---|
| A | 60916,722636004 | 269,4462033966172 | 4,767254520097566 | −505,4488843 | 105,9716879 |
| B | 60948,58600568 | 269,446174104526 | 4,767467288067585 | −540,6082282 | −32,0488435 |
| C | 61110,1584034 | 269,44637580436864 | 4,768737874953876 | 537,5883462 | −41,8540291 |

Kare isimleri `data/C/hdr_?.txt` başlıklarından gelir. Tam arşiv listesinin ilk/son tarihi, seçilmiş bu üç karenin tarihleri değildir.

## Bağımsız kapsam denetimi

Ana ajan, B penceresindeki **1.048.576 native piksel merkezinin tamamını** WCS ile göğe dönüştürüp başarılı 16 koniden en az birine düştüğünü doğruladı. FITS kaynak kimlikleri tekil, satır sayısı 49.176 ve epoch değerleri 2016.0. Kanıt: `reports/gaia-B-coverage-audit.json`. Bu geometrik kapsam testidir; kataloğun bilimsel tamlık oranını ölçmez.

## Geçiş gruplama prototipi — 04-01

Kaynak: `b_astrometri/motion/passes.py`. 30 günden **büyük** ardışık-kare boşluklarında yeni pass açar; `passes.json` içinde pass aralıkları, dedektör sayıları ve açık `gaps` listesi, `pass_of_frame.json` içinde kare eşlemesi üretir. Centroid-motion çevrimdışı test klasöründe 4 test vardır.

Stage 0 yerel kare listesiyle doğrulama: Barnard 358/358 kare, 3 pass (46/55/37 gün), iki boşluk; ε Indi B 458/458 kare, 4 pass (46/45/15/10 gün), üç boşluk. Çıktılar depo dışı `C:/Users/behlu/reports/04-01-passes/{Barnard,EpsInd_B}/` altında. Bu, mevcut liste verisiyle modül kontrolüdür.

**Sınır / kabul açık:** depo ve Stage 0 taramasında Liste 02 üretim manifesti bulunmadı. Kaydedilmiş `frames_*.json` girdilerinde `SPS_EPA` alanı yok; bu nedenle üretilen pass yönelim kümeleri boş ve görevdeki yönelim çıktısı kanıtlanmadı. Release/provenance tekilleştirmesi de bu fonksiyonda yapılmaz; Liste 02 girdisinin sözleşmesi beklenir. ClickUp 04-01'i tamamlandı saymayın. İnsan girdisi [HUMAN_ACTIONS.md](HUMAN_ACTIONS.md) H-03'te tutulur.

## ePSF D5 kontrol prototipi — 03-02

`b_astrometri/centroid/d5_check.py` ve testleri sentetik/öz-kurtarma kontrolü sağlar. 36 alt-piksel kaymada `norm=1` ve `norm=25` için konum hatası `<0.001 px`; `×25` modelin aynı görüntüde akı genliğinin `1/25` ölçeklenmesi kontrol edildi. 12 gürültülü sentetik kesitte normal PSF yönelimi devrik varyanttan daha düşük `χ²_ν` verdi. Çift keşif düzeltildikten sonra centroid dizini **21/21** geçti.

**Sınır / kabul açık:** bu sonuç gerçek ePSF kalibrasyonunu veya yönelimi kanıtlamaz. 02-07'den 200 gerçek izole yıldız/kesit yok; `PSF_NORM=1` ve `PSF_TRANSPOSE=False` hâlâ `[ASSUMPTION]`. `d5_result.md` ve insan girdisi [HUMAN_ACTIONS.md](HUMAN_ACTIONS.md) H-04'te tutulur. ClickUp 03-02'yi kapatmayın.

## Doymuş çekirdek kanat uyumu prototipi — 03-05

`b_astrometri/centroid/wing_fit.py` geçersiz/NaN/OVERFLOW piksellerini maskeler; maskeli piksel oranı `%50` üzerindeyse `unmeasurable`, çekirdek maskelenmişse `saturated_fit` döndürür. Sentetik kesitlerde konum belirsizliğinin genişlemesi ve üç-sigma konum sınırı ile iki test geçti; elips alanları `ellipse.catalog_fields` üzerinden üretilir.

**Sınır / kabul açık:** gerçek doymuş gözlem kareleriyle tarama yapılmadı. 02-08 ve 03-03 veri/önkoşulları H-05'te bekliyor. Bu prototip ClickUp 03-05 kabulü değildir.

## Piksel-faz sapma sweep'i — 03-13 sentetik kanıtı

`b_astrometri/centroid/phase_bias.py` ile 0..0,95 px fazlarında 0,05 adım ve her faz/SNR için 200 deneme çalıştırıldı (SNR 20/50/100; sabit seed 2026). CSV ve iki ayrı grafik `b_astrometri/reports/03-13-synthetic/` altındadır. SNR 50'de maksimum |bias| x/y = 0,00435/0,00281 px, RMS/σ = 0,895..1,100; SNR 100'de 0,00287/0,00202 px, RMS/σ = 0,924..1,136. SNR 20 ve 50 için `passed_t2_t3` uygulanmaz; görev ölçütü SNR > 50'dir.

**Sınır / kabul açık:** bunlar `test_epsf.fixture(detector=2)` sentetik sonuçlarıdır; 03-12 şartnamesi ile 07-05 kapsamındaki üretim T2/T3 test kodu veya 03-03 üretim uyum entegrasyonu değildir. Sayısal sentetik ölçütler geçti; ClickUp canlı durumu 401 nedeniyle doğrulanamadı. H-06 03-03 arayüzünü, H-07 kullanıcının “eğri düz mü?” görsel kararını bekletir. 03-13 görevi tamamlandı sayılmaz.

## 07-04 T1/T4 — gerçek Stage 0 kanıtı

T1: aynı OBSID'li gerçek 100×100 Stage 0 B penceresi ve gerçek ePSF kesiti kullanılarak 15×15 gerçek piksel damgasına yıldız enjekte edildi. `(x,y)`→`(x+1,y)` ölçümü `Δx=0.998404`, `Δy=0.000487 px`; damgada `np.roll` ölçümü `Δx=1.000000 px`. Her iki sonuç `0.005 px` toleransını geçti. ePSF'nin enjeksiyon ve uyumda aynı olması nedeniyle bu bağımsız PSF doğrulaması değildir. Ayrıntı [T1 raporunda](../../b_astrometri/reports/07-04-t1-real/README.md).

`tests/test_T4.py --real-dir <Stage0 B/cut>` dokuz gerçek FITS kesitinin SIP-3 `IMAGE` WCS başlıklarını doğrular ve her 29×29 piksel merkezini 0 tabanlı piksel→gök→piksel dönüşünden geçirir. 7.569 pikselde en büyük hata `4.47e-11 px`; `1e-4 px` eşiğinin altında. Kesitler depoya eklenmedi. Komut ve kesit bazlı sayılar [T4 doğrulama raporunda](../../b_astrometri/reports/07-04-t4-real/README.md).

**Sınır / kabul açık:** bu, yalnız eldeki dokuz küçük kesitte T4 kanıtıdır. 07-04 D3 için gerekli 50/100/200 px boyutlarında 100 gerçek pencere yok; T1 ekran kontrolü 07-03 görüntüleyici testine bağlı. H-11 bekliyor; 07-04 bütünüyle tamamlanmadı.

## Sabit konumlu zorlanmış ePSF fotometrisi — 04-03 prototipi

`b_astrometri/motion/forced_phot.py` sabit piksel konumunda `(F, b)` ağırlıklı doğrusal uyumunu, `sigma_flux`, `chi2_nu`, hatalı-uyum eşiğini (`>5`), maske/uyarı bayraklarını ve ters-varyanslı kare birleştirmeyi sağlar. Sentetik enjeksiyon-kurtarma, doymuş NaN çekirdek, hata eşiği, meta veri önceliği, bayrak/variance doğrulaması ve geçersiz coadd örnekleri için testler var.

**Sınır / kabul açık:** canlı görev durumu ClickUp 401 nedeniyle doğrulanmadı. Görev tarifindeki RA/Dec→WCS dönüşümü, `forced_phot(ra, dec, frames)` kare akışı ve parquet/CSV satır çıktısı bu prototipte yok; gerçek ePSF/WCS/maskeler ve D13 enjeksiyon verisi de çalıştırılmadı. H-08 girdileri gelene kadar 04-03'ü tamamlandı saymayın.

## Değişen yıldız ışık eğrileri — 04-12 prototipi

`b_astrometri/motion/lightcurves.py` λ-kutulu per-frame flux girdilerini MJD ve pass ile gruplar; geçişler arası farkı `|ΔF|/hypot(σ1,σ2)` olarak verir ve >3σ değişimi işaretler. Sabit kontrol yıldızı, R Dra değişimi, boş geçişler ve λ etiketli SVG çıktısı için prototip testleri var. `write_lightcurve_outputs` JSON+SVG yazar; boş girdide bilinmeyen kapsamı “not a zero-flux measurement” diye açıkça gösterir.

RW Aur ve R Dra için yalnız **UNKNOWN / photometry not run** JSON+SVG üretildi; Stage 0 A TAP hataları sıfır kare kanıtı değildir. Gerçek fotometri, 3σ kontrol yıldızı ve değişkenlik sonucu yok. Liste 01 frame listesi, 04-03 ölçümleri ve kontrol yıldızı H-12'de bekliyor. Çıktı [durum raporunda](../../b_astrometri/reports/04-12-status/README.md); 04-12 kabulü açık.

## WISE 0855 tespit edilebilirlik kapsam kapısı — 04-04

`b_astrometri/reports/04-04-wise0855/wise0855_detect.json` sonucu **unknown**. Stage 0 kanıtı (`docs/stage0/s0_A.md` satır 383/404/405) TAP zaman aşımı/502 ve tamamlanmayan SIA yedeği kaydediyor; QR3-only boş probe DR1/QR2/TAP'te kapsam yokluğunu kanıtlamaz. Bu nedenle fotometri ve geçiş başına SNR çalıştırılmadı; başka hedefe geçilmedi.

**Sınır / kabul açık:** 04-04'ün ilk kapsam kapısı kanonik Liste 01 sonucunu bekliyor (H-09). “Bilinmiyor” veriden “kapsam yok” çıkarmak değildir; gerçek kare/geçiş listesi gelmeden ölçüm yoktur.

## Hareketli cisim bağlama prototipi — 04-06

`b_astrometri/movers/linker.py` Gaia/2MASS eşleşmelerini ve farklı karelerde 1 px içinde tekrarlanan kaynakları eler; iki noktalı hız hipotezleriyle kareler arası doğrusal iz adayları arar. Üçten az karede `linking_closed` döner. Çıktıdaki `detection_refs` her tespitin frame_id ve det_id'sini korur. İki sentetik test statik eleme, hız kurtarma, artık ve kısa-geçiş davranışını kapsar.

**Sınır / kabul açık:** burada hız-ızgarası yerine tespit çiftlerinden hipotez örnekleniyor. Stage 0 D'de Bellerophon üç karede aday görünse de koordinatlar farklı kare-yerel piksel sistemlerinde; Stage 0 D FITS/WCS dosyaları bu bilgisayarda yok. Ortak tangent düzlemi koordinatları olmadan gerçek asteroidin `<1 px` izi doğrulanamaz. H-10 bekleniyor; 04-06 tamamlandı sayılmamalı.
