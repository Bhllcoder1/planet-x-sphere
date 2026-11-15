# Planet XSphere — oturum devri

Son güncelleme: 2026-11-15. Kalıcı proje hafızası [Second Brain](docs/second-brain/README.md), insan adımları [HUMAN_ACTIONS.md](docs/second-brain/HUMAN_ACTIONS.md) içinde. Yerel prototip/test başarısı ClickUp kabulü anlamına gelmez.

## Çalışma ve Git durumu

- Depo: `C:/Users/behlu/planet-x-sphere`; dal: `b/01-03-gaia-fetch`; `main` başlangıç tabanı `449567a556001f758a74dc1c8d5f622569c57b51`.
- Proje dışı kanıtlar ve FITS: `C:/Users/behlu/reports/`; Stage 0 Python: `C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe`.
- GitHub feature branch `b/01-03-gaia-fetch`; PR #1 is open/draft. The exact head is verified from GitHub before each push.
- ClickUp kişisel token ile salt-okunur `GET /user` HTTP 401 verdi; token yazdırılmadı, ClickUp'a değişiklik/yorum yapılmadı. 2026-11-14 tarihli yerel snapshot'ta Behlül'e atanan 46 görev `to do` görünüyordu; snapshot geçmiş veridir, canlı durum değildir.

## Kod kanıtı ve sınırlar

| İş | Doğrulanan yerel sonuç | Açık sınır / ClickUp durumu |
|---|---|---|
| 01-03 Gaia | `b_astrometri/gaia/fetch.py`; 35 Gaia tests; 128 px default live setting 16/16, 49,176 sources; all 16 required by regression | Original 256 px four queries were 2/4. 01-01 prerequisite and ClickUp acceptance remain unverified. |
| 03-01 ePSF | `b_astrometri/centroid/epsf.py`; test paketi ve yerel D2 smoke | Fiziksel akı normalizasyonu/yönelimi doğrulanmadı; H-01 girdileri bekliyor. |
| 03-07 epoch | `epoch.py`; 14 epoch tests; quality filter 49,176 -> 46,770 sources, 2,406 rejected; A/B/C propagation smoke preserves IDs and finite coordinates; JSON evidence outside repo | Target 3px exclusion, 02-03 production query/cache, uncertainty and RV remain open/assumed. |
| 03-04 elips / 03-14 koordinat denetimi | Centroid paketinde testli prototipler | ClickUp önkoşulları ve kabulü doğrulanmadı. |
| 03-02 D5 | 100 synthetic phase pairs; 600 noiseless recovery fits on real EPSF templates D2/D3/D6, max error <=0.000514 px; 25x amplitude behavior test | Zero real stars tested; 200-star orientation and physical flux calibration still need H-04. |
| 03-05 kanat uyumu | NaN/OVERFLOW maskeleme, `saturated_fit`, >%50 maskede `unmeasurable`, hata elipsi alanları; 2 sentetik test | Gerçek görüntü doğrulaması yok; 02-08/03-03 girdileri için H-05. Prototip, görev kabulü değil. |
| 04-03 zorlanmış fotometri | Sabit pikselde (F,b), sigma_flux, chi2_nu, maske/uyarı bayrakları ve ters-varyans coadd; sentetik testler | RA/Dec-WCS kare akışı ve CSV/parquet API'si yok; gerçek ePSF/WCS/maskeler ve D13 enjeksiyonu H-08 bekliyor. Prototip, görev kabulü değil. |
| 04-06 hareketli bağlama | `b_astrometri/movers/linker.py`; 2 sentetik test; `detection_refs` frame_id/det_id korur | Gerçek asteroid doğrulaması yok; Stage 0 D için ortak WCS/FITS/katalog H-10 bekliyor. Hız ızgarası henüz yok. Görev açık. |
| 04-04 WISE 0855 | `b_astrometri/reports/04-04-wise0855/wise0855_detect.json`: coverage `unknown`; TAP/SIA unsuccessful, photometry not run | Canonical List 01 result missing; H-09. Query failure is not zero coverage; 04-04 remains open. |
| 04-12 RW Aur/R Dra | λ-kutu/pass özetleyici ve JSON/SVG yazıcısı; gerçek girdisiz iki “UNKNOWN / photometry not run” çıktısı | Stage 0 TAP sorguları başarısız; frame listesi, 04-03 ölçümü ve sabit kontrol yıldızı yok. H-12; kabul yapılmadı. |
| 04-01 geçiş gruplama | 4 test; Barnard 358 kare/3 geçiş, ε Indi B 458 kare/4 geçiş; boşluk listesi | Liste 02 manifesti ve `SPS_EPA` alanı bulunamadı; H-03. Kabul açık. |
| 07-04 T1/T4 | T1: sentetik birim testleri ve gerçek görüntü/variance/flag piksellerine enjeksiyonda `Δx=0.998404 px`, `np.roll Δx=1.000000 px`; T4: 9 gerçek SIP-3 kesitte 7.569 piksel, max dönüş hatası `4.47e-11 px` | T1 ekran/Playwright ve D3'te gerekli 100 geniş gerçek pencere eksik; H-11. 07-04 kısmi. |

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
- H-11: 07-04 D3 için 50/100/200 px boyutlarında 100 gerçek WCS penceresi; T1 ekran testi için 07-03/07-02 görüntüleyici Playwright testi veya sahibi.
- H-12: RW Aur/R Dra List 01 frame/coverage verisi, aynı karelerde sabit kontrol yıldızı ve 04-03 flux/σ/CWAVE/CBAND/pass çıktısı.

## Son doğrulama

Latest focused verification: centroid 32/32, Gaia 35/35, D5 3/3; `git diff --check` clean. D5 real-template smoke ran 600 noiseless fits, maximum error 0.000514 px. Earlier whole-repo suites below were not rerun in this pass. Graphify: 52 files, 365 nodes, 701 edges, 18 communities; no dangling endpoints.

```powershell
& 'C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe' -I -m unittest discover -s b_astrometri/centroid -p 'test_*.py' -v
& 'C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe' -I -m unittest discover -s b_astrometri/motion -p 'test_*.py' -v
& 'C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe' -I -m unittest discover -s b_astrometri/gaia -p 'test_*.py' -v
& 'C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe' -I -m unittest discover -s tests -p 'test_T*.py' -v
```
- **Döngü tur 5 (03-13 sentetik prototip):** `b_astrometri/centroid/phase_bias.py` + `test_phase_bias.py` (3 test; centroid 24/24). 20 faz × SNR 20/50/100 × 200 denemeden CSV ve iki ayrı grafik `b_astrometri/reports/03-13-synthetic/` altına yazıldı. SNR 100 sentetik ölçütleri geçti; 07-05 üretim T2/T3 testleri ve 03-03 üretim entegrasyonu ile insanın “eğri düz mü?” incelemesi bekliyor (`H-06`, `H-07`). Gerçek FITS kullanılmadı.

Aktif Claude Code süreci aynı çalışma ağacını kullanabiliyor; sonraki oturumda commit/çalışma ağacı kontrolü yapmadan dosya üzerine yazma. İnsan girdisi bekleyen işleri kapatma veya ClickUp durumunu varsayma.

## Bu tur: 03-12 şartname düzeltmesi

- [V] ClickUp snapshot 03-12 kapsamı yalnız T1–T4 girdileri/çıktıları/eşikleri tanımlamak; test kodu 07 listesinde. Şartname güncellendi: T1 fiziksel 1 px kayma ile z=1/4/16/64 ekran yakınlaştırması ayrıldı; T2 faz/eksen ve strict SNR>50 açıklandı; T3 oranı SNR dilimi başına raporlanacak; JSON metrik nullability ve satır kabulü belirtildi.
- [NV] Canlı ClickUp token hâlâ 401; şartname işi ClickUp’ta kapatılmadı. Üretim verisi/kod önkoşulları 03-01/03-03 ve diğer görevler için ayrıca doğrulanmalı.


## Active parallel batch

Area B confirmed. ClickUp access restored (pk_ extraction from local file); H-02 resolved. User authorized task-status updates: 08-01 complete; 00-05/01-03/03-02/03-07/03-06/04-02/04-07/04-15 in progress. Merged main commit449567a into feature branch. Four agents implement stacks, rolling view, OUTLIER promotion and joint-fit output in disjoint files. reproject0.21.0 installed. Root corrected TRANSIENT bit0 / HALO bit28; old OUTLIER-as-HALO bug fixed. Real dataset acceptance remains separate from unit tests.
