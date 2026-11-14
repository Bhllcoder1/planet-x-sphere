# Alan B: Astrometri ve hareketli cisim bilimi

ClickUp etiketi: `kişi-b`. 46 görev, tahmini 170 saat [ASSUMPTION: ajan tahmini].

Konum bilimi: ePSF ile merkezleme, Gaia eşleme, WCS düzeltmesi, hareket uydurma, hareketli cisim bulucu, bilimsel testler ve 5 hedefin sonuç raporları.

## Bu klasörün sahibi

`.github/CODEOWNERS` dosyasında bu klasöre bağlı GitHub kullanıcısı. Değişiklik bu kişinin onayıyla birleşir.

## Görevler

| Görev | Süre | Etiket | Ad |
|---|---|---|---|
| 00-05 | 2 h | demo | Çalışma protokolü: ekip büyüklüğünden bağımsız görev seçimi |
| 01-03 | 3 h | demo | Gaia indirme sorunu: ESA TAP güvenilmez, yedek seçenekleri sırayla dene |
| 01-12 | 2 h | sonra | OUTLIER bayrağı nedeni (R27): aynı alanda hafta ve işleme etiketi karşılaştırması |
| 03-01 | 5 h | demo | ePSF modeli: EPSF HDU'dan GriddedPSFModel (örnekleme 5, 33x33) ve bölge seçimi |
| 03-02 | 3 h | demo | D5: ePSF normalizasyon ve yönelim kontrolü (×1/×25, x/y, dosya içi vs kalibrasyon) |
| 03-04 | 2 h | demo | Hata elipsi: kovaryanstan 1σ/2σ elips parametreleri ve JSON alanları |
| 03-05 | 4 h | demo | Doymuş çekirdek kanat uyumu: NaN/OVERFLOW pikselleri maskeleyerek |
| 03-06 | 5 h |  | Geçiş başına ortak uyum (C.7b): tek (α,δ) ile kareler boyunca |
| 03-07 | 5 h | demo | Gaia DR3 sorgusu ve epoğa taşıma formülleri (uzay hareketi + paralaks) |
| 03-12 | 4 h | demo | Enjeksiyon/kurtarma düzeneği tanımı: T1-T4 ve ölçütleri |
| 03-13 | 4 h | demo | Piksel-faz sapma eğrisi: sapma(faz) ölçümü ve tablo |
| 03-14 | 3 h | demo | Koordinat kuralları denetimi: 0 tabanlı, float konum asla yuvarlanmaz |
| 03-15 | 2 h | demo | WiseView'in Gaia yer değiştirmesiyle karşılaştırma testi (epoch hatasını bizim kodda önlem |
| 04-01 | 2 h | demo | Geçiş (pass) gruplama: 30 gün boşluk kuralı ve passes.json |
| 04-02 | 5 h |  | Geçiş yığını ve fark görüntüsü: yalnızca-görüntüleme (S modu), 'astrometri yok' etiketli |
| 04-03 | 4 h | demo | Zorlanmış (forced) ePSF fotometri modülü: sabit konumda kare başı akı |
| 04-04 | 5 h | demo | WISE 0855 saptanabilirlik testi: zorlanmış fotometri ve geçiş başına ters-varyans toplamı |
| 04-06 | 6 h |  | Hareketli cisim bulucu: katalog bağlama (hız ızgarası + RANSAC) |
| 04-07 | 4 h |  | OUTLIER kümelerini aday olarak terfi ettirme (hareketli arama maske profili) |
| 04-08 | 4 h |  | STREAK/GHOST/CROSSTALK vetoları (neden kodlu) ve kalabalık-alan koruması |
| 04-10 | 5 h |  | R24: asteroit konum sapması (1-3 px) araştırması: piksel nicemleme, LEO paralaksı, zamanla |
| 04-12 | 5 h |  | Değişen yıldızlar: RW Aur ve R Dra için λ-kutulu ışık eğrileri |
| 04-15 | 4 h | sonra | Kayan pencere toplama ve fark görünümü (yalnız görüntüleme, S modu) |
| 04-16 | 4 h | sonra | Sonra: 'kaydır ve topla' (shift-and-add) görünümü: kullanıcı hız girer, kareler izlenen ci |
| 04-17 | 4 h | sonra | Sonra: sentetik cisim ekleme (görüntüleme kopyasına, 'SENTETİK' etiketli) |
| 04-19 | 6 h | sonra | Sonra: gerçek/sahte hareketli sınıflandırıcı (küçük model) ve kural skoruyla karşılaştırma |
| 07-04 | 5 h | demo | T1 tam sayı kayma testi (sayısal + ekran z = 1, 4, 16, 64) ve T4 WCS gidiş-dönüş, D3 afin  |
| 07-05 | 6 h | demo | T2 alt-piksel merdiveni ve T3 enjeksiyon/kurtarma (D4 merkezleme yöntemi seçimi) |
| 07-08 | 6 h |  | T5 Gaia astrometri testi ve D6 WCS düzeltme modeli, D7 astrometri penceresi |
| 07-09 | 4 h |  | T6 bilinen hareket testi: Barnard μ (Gaia ile ±3σ ve %10), doygun çekirdek notu |
| 08-01 | 2 h | demo | Hedef sonuç notu şablonunu yazmak (kapsam, tespit, S/N, hareket, uyarılar, demo görünümü) |
| 08-02 | 3 h | demo | Barnard Yıldızı: kapsam tablosu ve zorlanmış fotometri/S-N sonucu (doygun çekirdek) |
| 08-04 | 2 h | demo | Barnard Yıldızı: uyarılar ve demo görünümünün tanımı (tıklama yolu, rozetler) |
| 08-05 | 3 h | demo | Epsilon Indi B: kapsam tablosu (458 kare, 4 geçiş) ve tespit/S-N sonucu |
| 08-06 | 3 h |  | Epsilon Indi B: hareket (literatür/Gaia), uyarılar ve demo görünümü |
| 08-07 | 3 h | demo | WISE 0855: kapsam tablosu (TAP şimdilik başarısız, bilinmiyor) ve tespit/zorlanmış fotomet |
| 08-09 | 3 h | demo | RW Aurigae: kapsam tablosu (TAP başarısız, bilinmiyor) ve tespit/zorlanmış fotometri |
| 08-10 | 3 h |  | RW Aurigae: değişken yıldız uyarısı (parlaklık ve dalgaboyu karışıklığı) ve demo görünümü |
| 08-11 | 3 h | demo | R Draconis: kapsam tablosu (TAP başarısız, bilinmiyor) ve tespit/zorlanmış fotometri |
| 08-13 | 2 h | demo | Beş hedefin karşılaştırma tablosunu yazmak (kapsam, S/N, hareket, durum) |
| 09-01 | 2 h | demo | README.md yazmak: ne yapar, nasıl çalıştırılır, hangi hedefler, hangi sınırlar |
| 09-06 | 2 h | demo | Sınırlılıklar sayfası: neyin doğrulanmadığını yazmak |
| 09-07 | 2 h | demo | Kullanıcı soruları için ekran görüntüsü setini hazırlamak (Q-H1, Q-H2, Q-H3) |
| 09-11 | 2 h | demo | Birinci prova: demo betiğini kronometreyle baştan sona yapmak |
| 10-11 | 6 h | demo | Okuma paneli, WCS-düzeltme rozeti ve geçişler arası hareket ölçüm paneli |
| 10-12 | 5 h | demo | Spektrum / ışık eğrisi paneli: RW Aur ve R Dra için zorunlu minimum |

Her görevin ayrıntısı ClickUp'ta (Planet XSphere çalışma alanı).

## Alt klasörler

- `centroid/  ePSF ile merkezleme ve hata elipsi
- `gaia/      Gaia sorgusu, epoğa taşıma, eşleme
- `wcs/       WCS düzeltmesi ve aberasyon alarmı
- `motion/    hareket uydurma
- `movers/    hareketli cisim bulucu ve SkyBoT etiketleme
- `reports/   5 hedefin sonuç raporları
