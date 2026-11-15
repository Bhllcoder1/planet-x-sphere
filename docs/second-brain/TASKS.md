# Behlül — görev dizini

Source: live ClickUp API, 2026-11-15. 46 assigned tasks. User authorized status updates; latest transitions recorded below.

| Görev | ClickUp durumu | Yerel durum | Önkoşul (açıklamadan) |
|---|---|---|---|
| [[00-05] Çalışma protokolü: ekip büyüklüğünden bağımsız görev seçimi](https://app.clickup.com/t/z8qu5ddjv6) | in progress | yerel ✓ | yok |
| [[01-03] Gaia indirme sorunu: ESA TAP güvenilmez, yedek seçenekleri sırayla dene](https://app.clickup.com/t/z8qu5ddjvj) | in progress | yerel ✓ (piksel ölçeği ve timeout açık) | 01-01 |
| [[01-12] OUTLIER bayrağı nedeni (R27): aynı alanda hafta ve işleme etiketi karşılaştırması](https://app.clickup.com/t/z8qu5ddjvv) | to do | — | 01-09 |
| [[03-01] ePSF modeli: EPSF HDU'dan GriddedPSFModel (örnekleme 5, 33x33) ve bölge seçimi](https://app.clickup.com/t/z8qu5ddjwm) | to do | yerel ✓ (sentetik; H-01 bekleniyor) | 02-03, 02-12 |
| [[03-02] D5: ePSF normalizasyon ve yönelim kontrolü (×1/×25, x/y, dosya içi vs kalibrasyon)](https://app.clickup.com/t/z8qu5ddjwn) | in progress | yerel ✓ (600 fit, max hata ≤0.000514 px; H-04 bekleniyor) | 03-01, 02-07 |
| [[03-04] Hata elipsi: kovaryanstan 1σ/2σ elips parametreleri ve JSON alanları](https://app.clickup.com/t/z8qu5ddjwq) | to do | — | 03-03 |
| [[03-05] Doymuş çekirdek kanat uyumu: NaN/OVERFLOW pikselleri maskeleyerek](https://app.clickup.com/t/z8qu5ddjwr) | to do | kısmi (sentetik; H-05 bekleniyor) | 03-03, 02-08 |
| [[03-06] Geçiş başına ortak uyum (C.7b): tek (α,δ) ile kareler boyunca](https://app.clickup.com/t/z8qu5ddjwt) | in progress | yerel ✓ (4 test; 1000-trial kapsamı henüz bitmedi) | 03-03, 03-09 |
| [[03-07] Gaia DR3 sorgusu ve epoğa taşıma formülleri (uzay hareketi + paralaks)](https://app.clickup.com/t/z8qu5ddjwu) | in progress | yerel ✓ (35 test; 02-03 entegrasyonu ve 3px dışlama açık) | 02-03 |
| [[03-12] Enjeksiyon/kurtarma düzeneği tanımı: T1-T4 ve ölçütleri](https://app.clickup.com/t/z8qu5ddjwz) | to do | yerel ✓ (harness_spec.md; test kodu 07-04/07-05 kapsamı) | 03-01, 03-03 |
| [[03-13] Piksel-faz sapma eğrisi: sapma(faz) ölçümü ve tablo](https://app.clickup.com/t/z8qu5ddjx0) | to do | kısmi (sentetik grafik; H-06/H-07 bekleniyor) | 03-12, 03-03 |
| [[03-14] Koordinat kuralları denetimi: 0 tabanlı, float konum asla yuvarlanmaz](https://app.clickup.com/t/z8qu5ddjx1) | in progress | kısmi (prototip; H-01 bekleniyor) | 02-03, 03-03 |
| [[03-15] WiseView'in Gaia yer değiştirmesiyle karşılaştırma testi (epoch hatasını bizim kodda önleme)](https://app.clickup.com/t/z8qu5ddjx2) | to do | yerel ✓ (6 test; Barnard 2010 MJD doğrulandı) | 03-07 |
| [[04-01] Geçiş (pass) gruplama: 30 gün boşluk kuralı ve passes.json](https://app.clickup.com/t/z8qu5ddjx3) | to do | kısmi (sentetik; H-03 bekleniyor) | liste 02 (kare listesi/manifest). |
| [[04-02] Geçiş yığını ve fark görüntüsü: yalnızca-görüntüleme (S modu), 'astrometri yok' etiketli](https://app.clickup.com/t/z8qu5ddjx4) | in progress | yerel ✓ (9 test; H-03/H-08 bekleniyor) | 04-01; liste 02 (maskeler, manifest). |
| [[04-03] Zorlanmış (forced) ePSF fotometri modülü: sabit konumda kare başı akı](https://app.clickup.com/t/z8qu5ddjx5) | in progress | kısmi (sentetik piksel; H-08 bekleniyor) | liste 03 (ePSF, WCS düzeltmesi), liste 02 (maskeler). |
| [[04-04] WISE 0855 saptanabilirlik testi: zorlanmış fotometri ve geçiş başına ters-varyans toplamı](https://app.clickup.com/t/z8qu5ddjx6) | to do | — (H-09 bekleniyor) | 04-03; liste 01 (WISE 0855 kapsamı); liste 03 (ePSF). |
| [[04-06] Hareketli cisim bulucu: katalog bağlama (hız ızgarası + RANSAC)](https://app.clickup.com/t/z8qu5ddjx8) | in progress | kısmi (sentetik; H-10 bekleniyor) | 04-01; liste 02 (tespit/katalog), liste 03 (WCS düzeltmesi). |
| [[04-07] OUTLIER kümelerini aday olarak terfi ettirme (hareketli arama maske profili)](https://app.clickup.com/t/z8qu5ddjx9) | in progress | yerel ✓ (7 test, movers 12/12; TRANSIENT/HALO bit düzeltildi) | 04-06 (arayüzü), liste 02 (FLAGS okuma). |
| [[04-08] STREAK/GHOST/CROSSTALK vetoları (neden kodlu) ve kalabalık-alan koruması](https://app.clickup.com/t/z8qu5ddjxa) | to do | — | 04-06, 04-07. |
| [[04-10] R24: asteroit konum sapması (1-3 px) araştırması: piksel nicemleme, LEO paralaksı, zamanlama](https://app.clickup.com/t/z8qu5ddjxc) | to do | — | liste 03 (ePSF merkezleme); 04-09 ile birlikte okunur. |
| [[04-12] Değişen yıldızlar: RW Aur ve R Dra için λ-kutulu ışık eğrileri](https://app.clickup.com/t/z8qu5ddjxe) | to do | kısmi (UNKNOWN JSON; H-12 bekleniyor) | 04-03, 04-01; liste 01 (kapsam). |
| [[04-15] Kayan pencere toplama ve fark görünümü (yalnız görüntüleme, S modu)](https://app.clickup.com/t/z8qu5ddjxh) | in progress | yerel ✓ (8 test; H-03 bekleniyor) | 04-01, 04-02, 02-16 |
| [[04-16] Sonra: 'kaydır ve topla' (shift-and-add) görünümü: kullanıcı hız girer, kareler izlenen cisme göre toplanır](https://app.clickup.com/t/z8qu5ddjxj) | to do | — | 04-15, 02-16 |
| [[04-17] Sonra: sentetik cisim ekleme (görüntüleme kopyasına, 'SENTETİK' etiketli)](https://app.clickup.com/t/z8qu5ddjxk) | to do | — | 03-01, 02-16 |
| [[04-19] Sonra: gerçek/sahte hareketli sınıflandırıcı (küçük model) ve kural skoruyla karşılaştırma](https://app.clickup.com/t/z8qu5ddjxn) | to do | — | 04-18 |
| [[07-04] T1 tam sayı kayma testi (sayısal + ekran z = 1, 4, 16, 64) ve T4 WCS gidiş-dönüş, D3 afin kalıntısı](https://app.clickup.com/t/z8qu5ddjyv) | to do | kısmi (Δx=0.998404 px; H-11 bekleniyor) | 07-01, 07-03 |
| [[07-05] T2 alt-piksel merdiveni ve T3 enjeksiyon/kurtarma (D4 merkezleme yöntemi seçimi)](https://app.clickup.com/t/z8qu5ddjyw) | to do | — | 07-01; liste 03 ePSF uyumu |
| [[07-08] T5 Gaia astrometri testi ve D6 WCS düzeltme modeli, D7 astrometri penceresi](https://app.clickup.com/t/z8qu5ddjyz) | to do | — | 07-01, 07-05; liste 03 Gaia eşleme/WCS düzeltme |
| [[07-09] T6 bilinen hareket testi: Barnard μ (Gaia ile ±3σ ve %10), doygun çekirdek notu](https://app.clickup.com/t/z8qu5ddjz0) | to do | — | 07-05, 07-08; liste 03/04 hareket uyumu |
| [[08-01] Hedef sonuç notu şablonunu yazmak (kapsam, tespit, S/N, hareket, uyarılar, demo görünümü)](https://app.clickup.com/t/z8qu5ddjz8) | complete | yerel ✓ | yok |
| [[08-02] Barnard Yıldızı: kapsam tablosu ve zorlanmış fotometri/S-N sonucu (doygun çekirdek)](https://app.clickup.com/t/z8qu5ddjz9) | to do | — | 08-01; liste 03 (ePSF, NaN çekirdek sığdırma) |
| [[08-04] Barnard Yıldızı: uyarılar ve demo görünümünün tanımı (tıklama yolu, rozetler)](https://app.clickup.com/t/z8qu5ddjzb) | to do | — | 08-03; liste 05 (rozetler, blink) |
| [[08-05] Epsilon Indi B: kapsam tablosu (458 kare, 4 geçiş) ve tespit/S-N sonucu](https://app.clickup.com/t/z8qu5ddjzc) | to do | — | 08-01; liste 03 |
| [[08-06] Epsilon Indi B: hareket (literatür/Gaia), uyarılar ve demo görünümü](https://app.clickup.com/t/z8qu5ddjzd) | to do | — | 08-05; liste 03, 05 |
| [[08-07] WISE 0855: kapsam tablosu (TAP şimdilik başarısız, bilinmiyor) ve tespit/zorlanmış fotometri](https://app.clickup.com/t/z8qu5ddjzf) | to do | — | 08-01; liste 01 (kapsam), liste 04 (tespit edilebilirlik) |
| [[08-09] RW Aurigae: kapsam tablosu (TAP başarısız, bilinmiyor) ve tespit/zorlanmış fotometri](https://app.clickup.com/t/z8qu5ddjzh) | to do | — | 08-01; liste 01, 03 |
| [[08-10] RW Aurigae: değişken yıldız uyarısı (parlaklık ve dalgaboyu karışıklığı) ve demo görünümü](https://app.clickup.com/t/z8qu5ddjzj) | to do | — | 08-09; liste 04, 05 |
| [[08-11] R Draconis: kapsam tablosu (TAP başarısız, bilinmiyor) ve tespit/zorlanmış fotometri](https://app.clickup.com/t/z8qu5ddjzk) | to do | — | 08-01; liste 01, 03 |
| [[08-13] Beş hedefin karşılaştırma tablosunu yazmak (kapsam, S/N, hareket, durum)](https://app.clickup.com/t/z8qu5ddjzn) | to do | — | 08-03, 08-06, 08-08, 08-10, 08-12 (hedef notları bitmiş olmalı) |
| [[09-01] README.md yazmak: ne yapar, nasıl çalıştırılır, hangi hedefler, hangi sınırlar](https://app.clickup.com/t/z8qu5ddjzq) | to do | — | liste 06 (dağıtım) |
| [[09-06] Sınırlılıklar sayfası: neyin doğrulanmadığını yazmak](https://app.clickup.com/t/z8qu5ddjzw) | to do | kısmi (taslak yazıldı) | 09-04, 08-14 |
| [[09-07] Kullanıcı soruları için ekran görüntüsü setini hazırlamak (Q-H1, Q-H2, Q-H3)](https://app.clickup.com/t/z8qu5ddjzx) | to do | — | liste 05, 07 |
| [[09-11] Birinci prova: demo betiğini kronometreyle baştan sona yapmak](https://app.clickup.com/t/z8qu5ddk01) | to do | — | 09-02, 09-08 |
| [[10-11] Okuma paneli, WCS-düzeltme rozeti ve geçişler arası hareket ölçüm paneli](https://app.clickup.com/t/z8qu5ddk0d) | to do | — | 10-10, liste 03 (C.9, hareket uyumu) |
| [[10-12] Spektrum / ışık eğrisi paneli: RW Aur ve R Dra için zorunlu minimum](https://app.clickup.com/t/z8qu5ddk0e) | to do | — | 10-05, liste 04 (λ-bin ışık eğrileri) |
