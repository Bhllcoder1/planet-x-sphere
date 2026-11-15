# 09-06 Sınırlılıklar sayfası — taslak

**Durum:** Taslak (09-04 ve 08-14 tamamlandığında güncellenir). Doğrulanmamış iddialar `[NV]`, varsayımlar `[ASSUMPTION]` etiketlidir.

---

## Astrometri ve katalog

| Alan | Ne doğrulandı | Ne doğrulanamadı | Neden |
|---|---|---|---|
| Gaia DR3 karoları | ESA TAP ile 16/16 karo başarılı (49 176 kaynak) | Dört büyük karo için tam kapsam (2/4 başarılı); MAST taşma riski | H-03 bekleniyor; MAST probes OVERFLOW döndürdü |
| Piksel ölçeği | 128 px karo koni yarıçapı hesaplandı | WCS'ten gerçek ölçek okunmuyor; 6.2″/px sabit kodlu | H-04 bekleniyor; fetch.py düzeltmesi açık |
| Epoch taşıma | Barnard 2010 MJD doğrulandı (6 test); 49 176 → 46 770 seçim | 02-03 koordinat sözleşmesine bağlama; 3 px hedef dışlama | H-01 bekleniyor |
| Koordinat kuralı | 0 tabanlı float konum prototipi var | 02-03/02-12 üretim sözleşmesi doğrulanmadı | H-01 bekleniyor |

## ePSF ve merkezleme

| Alan | Ne doğrulandı | Ne doğrulanamadı | Neden |
|---|---|---|---|
| ePSF modeli | 03-02: 600 sentetik fit, max hata ≤0.000514 px | 02-07 gerçek izole yıldız kesitleriyle yönelim/akı | H-04 bekleniyor |
| Fiziksel normalizasyon | D5 sentetik × 1/×25 self-recovery | Gerçek FITS üzerinde flux birimi tutarlılığı | H-04 bekleniyor |
| Ortak uyum (03-06) | 4 test; Jacobian düzeltmesi dahil | 1000-trial hata kapsamı henüz tamamlanmadı | 03-06 kovaryans doğrulaması açık |
| Hata elipsi (03-04) | Prototip var | Üretim H-04 bekleniyor | — |

## Geçiş gruplama ve yığınlar

| Alan | Ne doğrulandı | Ne doğrulanamadı | Neden |
|---|---|---|---|
| Pass gruplama | Barnard 358/3, ε Indi B 458/4 sentetik | Liste 02 manifesti; `SPS_EPA` alanı | H-03 bekleniyor |
| Exact-TAN yığın | 04-02: 9 test, f32/noise/JSON | Gerçek manifest/maskeler | H-03/H-08 bekleniyor |
| Kayan pencere | 04-15: 8 test | Gerçek kare sırası | H-03 bekleniyor |

## Zorlanmış fotometri ve hedefler

| Alan | Ne doğrulandı | Ne doğrulanamadı | Neden |
|---|---|---|---|
| Zorlanmış fotometri (04-03) | Piksel düzeyinde sentetik prototip | RA/Dec→WCS kare akışı; gerçek ePSF/WCS/maskeler | H-08 bekleniyor |
| WISE 0855 | TAP/SIA denendi | Kapsam bilinmiyor (TAP başarısız = sıfır kare değil) | H-09 bekleniyor |
| Barnard Yıldızı fotometri | — | Doygun çekirdek NaN sığdırma; gerçek kare listesi | H-08 bekleniyor |
| ε Indi B fotometri | — | 458 kare gerçek kapsamı | H-08 bekleniyor |
| RW Aur / R Dra ışık eğrileri | UNKNOWN JSON+SVG yazıldı | Gerçek kare/kontrol yıldızı/akı | H-12 bekleniyor |

## Hareketli cisim bulucu

| Alan | Ne doğrulandı | Ne doğrulanamadı | Neden |
|---|---|---|---|
| Katalog bağlama | Sentetik iz bağlama (iki noktalı hız) | Gerçek asteroid; ortak tangent düzlemi WCS | H-10 bekleniyor |
| OUTLIER terfi | 7 test, TRANSIENT bit0/HALO bit28 düzeltildi | Gerçek FLAGS verisi | H-03 bekleniyor |
| Hız ızgarası | Prototip yok | — | — |

## Görüntüleyici ve arayüz

| Alan | Ne doğrulandı | Ne doğrulanamadı | Neden |
|---|---|---|---|
| T1 tam sayı kayma | Δx=0.998404 px sentetik | T1 ekran/Playwright; 100 gerçek WCS penceresi | H-11 bekleniyor |
| T4 WCS gidiş-dönüş | 9 gerçek SIP-3 kesit; max hata 4.47e-11 px | — | — |
| T2/T3 alt-piksel | — | 07-05 bekleniyor | — |

## Genel uyarılar

- **Sentetik test başarısı üretim kabulü değildir.** Tablodaki tüm "yerel ✓" kayıtları gerçek FITS, gerçek kare manifesti veya ekip çıktılarıyla doğrulanmayı bekliyor.
- **TAP başarısızlığı sıfır kare demek değildir.** WISE 0855, RW Aur, R Dra için kapsam bilinmiyor; Stage 0 A arama sorguları tamamlanmadı.
- **ClickUp kapanışı yapılmadı.** `in progress` görevler yerel prototipi yansıtır; ClickUp kabulü ekip kararı gerektirir.
- **Resampled variance nominaldır.** 03-06 interpolasyon kovaryansı yayılmıyor; bu aşamada ihmal edilebilir kabul edildi.
- [NV] Dört büyük Gaia karosundan iki tanesi için tam kapsam doğrulaması yapılmadı.
- [ASSUMPTION] 6.2″/px piksel ölçeği; gerçek WCS'ten okunmadı (fetch.py açık madde).
