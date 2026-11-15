# Planet XSphere — oturum devri

Son güncelleme: 2026-11-15. Kalıcı proje hafızası [Second Brain](docs/second-brain/README.md), insan adımları [HUMAN_ACTIONS.md](docs/second-brain/HUMAN_ACTIONS.md) içinde. Yerel prototip/test başarısı ClickUp kabulü anlamına gelmez.

## Çalışma ve Git durumu

- Depo: `C:/Users/behlu/planet-x-sphere`; dal: `b/01-03-gaia-fetch`; `main` başlangıç tabanı `449567a556001f758a74dc1c8d5f622569c57b51`.
- Proje dışı kanıtlar ve FITS: `C:/Users/behlu/reports/`; Stage 0 Python: `C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe`.
- GitHub dalında 03-02 sentetik D5 ve 03-05 doymuş çekirdek prototipi commitlidir. Bu oturumda test keşif düzeltmesi, D5 sonuç/H-04 referansı, Second Brain ve Graphify çıktıları yenileniyor.
- ClickUp kişisel token ile salt-okunur `GET /user` HTTP 401 verdi; token yazdırılmadı, ClickUp'a değişiklik/yorum yapılmadı. 2026-11-14 tarihli yerel snapshot'ta Behlül'e atanan 46 görev `to do` görünüyordu; snapshot geçmiş veridir, canlı durum değildir.

## Kod kanıtı ve sınırlar

| İş | Doğrulanan yerel sonuç | Açık sınır / ClickUp durumu |
|---|---|---|
| 01-03 Gaia | `b_astrometri/gaia/fetch.py`; 11 test; küçük ESA konileri 16/16, 49.176 tekil kaynak | Dört büyük karonun ikisi kaldı; görev kabulü/önkoşul ayrıca doğrulanmalı. |
| 03-01 ePSF | `b_astrometri/centroid/epsf.py`; test paketi ve yerel D2 smoke | Fiziksel akı normalizasyonu/yönelimi doğrulanmadı; H-01 girdileri bekliyor. |
| 03-07 epoch | `b_astrometri/gaia/epoch.py`; 11 epoch testi, kutup geometrisi vektörel düzeltildi | 02-03 entegrasyonu, sorgu seçimi ve kovaryans belirsizliği açık; Barnard RV=0 varsayımlı. |
| 03-04 elips / 03-14 koordinat denetimi | Centroid paketinde testli prototipler | ClickUp önkoşulları ve kabulü doğrulanmadı. |
| 03-02 D5 | 36 sentetik alt-piksel kaymada norm 1/25 konum hatası <0.001 px; sabit görüntüde 25x akı ölçeği; 12 sentetik kesitte yönelim ayrımı | 200 gerçek yıldız/02-07 yok; `PSF_NORM=1`, `PSF_TRANSPOSE=False` varsayım. H-04. Görev açık. |
| 03-05 kanat uyumu | NaN/OVERFLOW maskeleme, `saturated_fit`, >%50 maskede `unmeasurable`, hata elipsi alanları; 2 sentetik test | Gerçek görüntü doğrulaması yok; 02-08/03-03 girdileri için H-05. Prototip, görev kabulü değil. |
| 04-03 zorlanmış fotometri | Sabit pikselde (F,b), sigma_flux, chi2_nu, maske/uyarı bayrakları ve ters-varyans coadd; sentetik testler | RA/Dec-WCS kare akışı ve CSV/parquet API'si yok; gerçek ePSF/WCS/maskeler ve D13 enjeksiyonu H-08 bekliyor. Prototip, görev kabulü değil. |
| 04-06 hareketli bağlama | `b_astrometri/movers/linker.py`; 2 sentetik test; `detection_refs` frame_id/det_id korur | Gerçek asteroid doğrulaması yok; Stage 0 D için ortak WCS/FITS/katalog H-10 bekliyor. Hız ızgarası henüz yok. Görev açık. |
| 04-04 WISE 0855 | `b_astrometri/reports/04-04-wise0855/wise0855_detect.json`: coverage `unknown`; TAP/SIA unsuccessful, photometry not run | Canonical List 01 result missing; H-09. Query failure is not zero coverage; 04-04 remains open. |
| 04-01 geçiş gruplama | 4 test; Barnard 358 kare/3 geçiş, ε Indi B 458 kare/4 geçiş; boşluk listesi | Liste 02 manifesti ve `SPS_EPA` alanı bulunamadı; H-03. Kabul açık. |

## İnsan girdileri

- H-01: Akif'in 02-03 koordinat/piksel kuralları ve 02-12 L1 cache çıktılarının dal/yerel yolu veya hazır olmadıkları bilgisi.
- H-02: Bu bilgisayardaki ClickUp token dosyasını yeni kişisel tokenla güncelle; tokenı sohbete/depoya koyma. Ardından canlı salt-okunur denetim yapılabilir.
- H-03: Liste 02 kanonik kare manifesti ve `SPS_EPA` kaynağının yolu/şeması veya henüz hazır olmadığı bilgisi.
- H-04: 02-07 gerçek izole yıldız örneklemi/kesitlerinin yolu veya henüz hazır olmadığı bilgisi.
- H-05: 03-05 gerçek görüntü doğrulaması için 02-08/03-03 girdilerinin yolu veya hazır olmadığı bilgisi.
- H-06: 03-13 üretim entegrasyonu için 03-03 merkezleme uyum kodu ile giriş/çıkış şemasının yolu. 03-12 yalnız şartnamedir; test kodu 07-05 kapsamındadır.
- H-07: 03-13 sentetik bias ve RMS/sigma grafiklerinin görsel incelemesi (“eğri düz mü?”).
- H-08: 04-03 için Liste 03 ePSF/WCS, Liste 02 maskeleri ve D13 enjeksiyon verisinin yolu/şeması.
- H-09: WISE 0855 canonical List 01 coverage/frame/pass result path or `unknown/not ready`.
- H-10: 04-06 için en az üç karelik gerçek asteroid kataloğu ve ortak tangent düzlemi sağlayan WCS/FITS yolu.

## Son doğrulama

Bu oturumda: centroid **24/24**, motion **10/10**, movers **2/2**, Gaia **30/30** test geçti; toplam **66**. ERFA bir testte mesafe düzeltme uyarısı bastı, test yine geçti. `git diff --check` temiz. Graphify targeted corpus **42 dosya**, **305 düğüm**, **562 kenar**, **17 topluluk**; kayıp/eksik uç yok, 3 aynı-uçlu kenar sade grafikte birleşiyor. Token maliyeti host araçlarında sunulmadığı için bilinmiyor.

```powershell
& 'C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe' -I -m unittest discover -s b_astrometri/centroid -p 'test_*.py' -v
& 'C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe' -I -m unittest discover -s b_astrometri/motion -p 'test_*.py' -v
& 'C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe' -I -m unittest discover -s b_astrometri/gaia -p 'test_*.py' -v
```
- **Döngü tur 5 (03-13 sentetik prototip):** `b_astrometri/centroid/phase_bias.py` + `test_phase_bias.py` (3 test; centroid 24/24). 20 faz × SNR 20/50/100 × 200 denemeden CSV ve iki ayrı grafik `b_astrometri/reports/03-13-synthetic/` altına yazıldı. SNR 100 sentetik ölçütleri geçti; 07-05 üretim T2/T3 testleri ve 03-03 üretim entegrasyonu ile insanın “eğri düz mü?” incelemesi bekliyor (`H-06`, `H-07`). Gerçek FITS kullanılmadı.

Aktif Claude Code süreci aynı çalışma ağacını kullanabiliyor; sonraki oturumda commit/çalışma ağacı kontrolü yapmadan dosya üzerine yazma. İnsan girdisi bekleyen işleri kapatma veya ClickUp durumunu varsayma.

## Bu tur: 03-12 şartname düzeltmesi

- [V] ClickUp snapshot 03-12 kapsamı yalnız T1–T4 girdileri/çıktıları/eşikleri tanımlamak; test kodu 07 listesinde. Şartname güncellendi: T1 fiziksel 1 px kayma ile z=1/4/16/64 ekran yakınlaştırması ayrıldı; T2 faz/eksen ve strict SNR>50 açıklandı; T3 oranı SNR dilimi başına raporlanacak; JSON metrik nullability ve satır kabulü belirtildi.
- [NV] Canlı ClickUp token hâlâ 401; şartname işi ClickUp’ta kapatılmadı. Üretim verisi/kod önkoşulları 03-01/03-03 ve diğer görevler için ayrıca doğrulanmalı.
