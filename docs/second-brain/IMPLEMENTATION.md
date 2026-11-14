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
