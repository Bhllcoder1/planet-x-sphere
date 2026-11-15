# Şu an

## Aktif kapsam

Active area: B (confirmed by user). ClickUp access is restored using the pk_ value extracted from the local token file. Live read verified 46 Behlul-assigned tasks. Earlier whole-line parsing caused the 401 error; it was not evidence of an invalid personal token.

İnsan girdisi gereken bağımlılıklar [HUMAN_ACTIONS.md](HUMAN_ACTIONS.md) içinde. H-01 (Akif'in 02-03/02-12 çıktılarının yeri/hazır oluşu) yanıtlanana kadar bağlı üretim entegrasyonu bekler. Bağımsız işlerde yalnız görev önkoşulları sağlananlar yürütülür. Yerel kod/test geçmesi tek başına ClickUp kabulü değildir.

## Doğrulanan durum — 2026-11-15

- [V] ClickUp API hesabı Behlül Anik; Planet XSphere çalışma alanında 199 görevden 46'sı bu hesaba atanmış. Okunan anlık görüntüde 46'sı da `to do`.
- [V] Ürün deposu `C:/Users/behlu/planet-x-sphere`; o tarihteki başlangıç incelemesinde ürün alanları iskelet halindeydi.
- [V] Deney betikleri/veriler `C:/Users/behlu/spherex-kb/stage0` altında; ürün deposunda değiller.
- [V] Eski ESA betiği `c6_gaia.py` başarısız karolara rağmen kısmi birleştirilmiş çıktı yazabiliyor.
- [V] Eski MAST betiği `c9_vizier.py` OVERFLOW sonucunu yalnızca uyarıp kabul ediyor. Yeni çözüm eksik/kesilmiş kataloğu tam gibi sunmamalı.
- [V] Gaia küçük koni canlı denemesi ESA üzerinden 16/16 başarılı sorgu ve 49.176 tekil kaynak verdi; B penceresinin dört büyük karo denemesi 2/4 kaldı. Ayrıntı ve kapsam sınırı [GAIA_FETCH.md](../GAIA_FETCH.md) içinde.

## Şu anki yerel doğrulama

- `[V]` 2026-11-15 latest focused runs: centroid 32/32, Gaia 35/35, D5 3/3; `git diff --check` clean.
- `[V]` 2026-11-15: `d93e952` 04-01 pass gruplama prototipini özellik dalına ekledi; `main` değiştirilmedi.
- `[NV]` 03-14 kabulü açık: ClickUp önkoşulları 02-03 ve 03-03'ün tamamlandığı doğrulanmadı. Koordinat denetimi prototipi var; görevi kapatmayın.
- `[V]` 03-12 T1–T4 girdi/çıktı/eşik şartnamesi `b_astrometri/centroid/harness_spec.md` içinde; ClickUp açıklamasına göre bu görev test kodu yazmaz. Test uygulaması 07-04/07-05 kapsamındadır. Canlı ClickUp durumu 401 nedeniyle doğrulanamadı.
- `[V]` ClickUp snapshot'ı 2026-11-14 22:23 UTC'de yazılmış; o anda Behlül'e atanmış 46 görevin hepsi `to do` idi. Canlı GET /user HTTP 401 olduğu için bu durum bugün için doğrulanmış sayılmaz.
- `[V]` H-02 resolved: GET /user returned 200 for Behlul Anik. Token stays outside the repository.
- `[V]` 04-01 yerel pass gruplaması 4/4 testte geçti; Barnard 358 kare/3 pass, ε Indi B 458/4 ve gap listeleri yazıldı. Çıktı kanıtı depo dışı `C:/Users/behlu/reports/04-01-passes/`.
- `[NV]` 04-01 tam kabulü açık: Liste 02 manifesti yok, yerel frame JSON'larında `SPS_EPA` alanı yok ve release tekilleştirmesi modülde değil. H-03 girdisi bekleniyor.
- `[V]` 03-02 D5: 100 exact phase pairs (0.0..0.9 by 0.1), x1/x25 self-recovery; 3 focused tests pass. Real template smoke: 600 fits on D2/D3/D6, max error 0.000514 px; zero real stars. Evidence outside repo at `C:/Users/behlu/reports/d5-real-templates-100phase.json`.
- `[V]` 01-03 implementation: 128 px is now the default after the explicit 128-px live run returned 16/16; regression requires all 16 tiles and preserves output on failure. Gaia suite: 35 tests. 01-01 prerequisite / ClickUp closure remain unverified.
- `[V]` 03-07: quality filter and A/B/C batch propagation smoke verified on the local Gaia catalogue: 49,176 -> 46,770, 2,406 rejected; IDs preserved, finite coordinates, zero warnings. Target 3px exclusion and 02-03 query/cache integration remain pending.
- `[NV]` D5 real-star/orientation acceptance still needs 200 isolated 02-07 stars (H-04); the 100-phase/template checks do not replace that sample.
- `[V]` GitHub PR #1 is open and draft; on 2026-11-15 the branch is pushed and PR #1 remains open/draft. No review, merge, or ClickUp closure has happened.
- [HUMAN_ACTIONS.md](HUMAN_ACTIONS.md) içindeki H-01 çözülmeden 02-03/02-12'ye bağlı üretim entegrasyonuna geçme.

## Sonraki adımlar

1. PR #1 remains a draft; wait for human review before merge. Do not close ClickUp tasks without live acceptance.
2. Continue live ClickUp task updates using the local token; do not ask the user to renew a working token.
3. H-01 ve H-03 yanıtlarına göre bağlı üretim işlerini sürdür; hazır olmayan önkoşulları tamamlanmış sayma.

## Oturum kaydı

- Second brain oluşturuldu; sadece görev/karar/kaynak bilgileri kaydedildi.
- Gaia denetimi ajanı mevcut betiklerdeki kısmi sonuç ve OVERFLOW risklerini bağımsız olarak bildirdi.
- [V] Ajanın yerel önbellek okuması: B'nin dört MAST karosu 15.734 / 16.515 / 17.514 / 18.761 satır; birleşik dosya 55.137 kaynak, 11 sütun ve ref_epoch=2016.0. Bu, tarihsel kesilmenin olmadığını veya canlı erişimi kanıtlamaz.
- Kullanıcı 2026-11-15: paralel ajanlarla ilerle; karar/hesap/elle işlem için gerçekten kullanıcı bilgisi gerekiyorsa ilgili adımı durdur ve yanıtını bekle. Etiketleme gerekirse CVAT vb. araçları ve uygun becerileri değerlendir; henüz etiketleme gereksinimi saptanmadı.
- [V] İlk küçük koni denemesinde ESA HTTP 200 ve QUERY_STATUS=OK (2,77 sn); MAST HTTP 200 fakat OK ardından OVERFLOW (1,32 sn). Kanıt: depo dışında `reports/gaia-live-probes.json`. Bu ilk denemeden sonra küçük ESA koni setiyle B penceresi başarıyla tarandı; aşağıdaki sonraki kayıt o sonucu verir.
- [V] Ortam denetimi: mevcut Stage 0 venv Python 3.14.0, astropy 8.0.2, photutils 3.1.1, numpy 2.5.4, scipy 1.18.1, requests 2.34.2. SEP yok. Bu temiz kurulum/bağımlılık kilidi doğrulaması değildir.
- 00-05 yerel çıktısı hazır: [çalışma protokolü](../WORK_PROTOCOL.md), yedi kural ve üç görevle seçim provası. ClickUp kapanışı yapılmadı.
- 08-01 yerel çıktısı hazır: [hedef raporu şablonu](../../b_astrometri/reports/hedefler_sablon.md), altı bölüm ve tarihsel Barnard/bilinmeyen WISE 0855 doldurma provası. Yeni bilimsel ölçüm yapılmadı; ClickUp kapanışı yapılmadı.
- Gaia small-tile live evidence: 16/16 ESA responses, 49,176 unique sources, 67.364 s; 128px setting is now the code default and all-16 completion is regression-tested. The original four large tiles were 2/4; ClickUp acceptance and prerequisite 01-01 remain open.
- ePSF prototipi: 6 test ana oturumda geçti; gerçek D2 441×33×33/5×5, üç konum self-recovery 0 px. Görüntü/JSON kanıtları [IMPLEMENTATION.md](IMPLEMENTATION.md) içinde. Fiziksel normalizasyon ve üretim entegrasyonu açık.
- Epoch prototype: 14 tests now cover propagation, pole/RA edge cases, and the task quality filter; 49,176 catalogue entries -> 46,770 selected and propagated at A/B/C. User-target 3px exclusion, upstream query/cache integration and uncertainty propagation remain open.
- Kullanıcı Jev TypeSafe v1.14 görüntü desteğini incelemeyi ve TypeSafe becerisini projeye kurmayı istedi. Tek npx yöntemiyle `.agents/skills/typesafe-ai/` kuruldu, SKILL.md okundu. Görüntüler/Box resmi belgede halen dreamer-ready; canlı API denemesi yapılmadı. Bilimsel doğruluk veya güven puanı hakkında test edilmemiş iddia yok.
- Graphify kalıcı grafiği kuruluyor: hedef kapsam yeni kod + proje hafızası; eski araştırma/plan arşivleri kapsam dışında. Dosya notları asıl hafıza, grafik anlık türetilmiş dizindir.

## Sonraki işlerin bağımlılıkları

- 03-01: 02-03 koordinat ve 02-12 L1 önbellek arayüzlerini bekler; sentetik/yerel FITS prototipi bağımsız hazırlanabilir.
- 03-02: 03-01 ve 02-07 gerçek yıldız seçimini bekler. Kabulde konum kadar akı da doğrulanmalı (×1/×25 ölçeği).
- 03-07: 02-03 koordinat sözleşmesine bağlanır; saf epoch/paralaks testleri bağımsız hazırlanabilir.
- 04-03: ePSF, maskeler ve WCS düzeltmesiyle gerçek veri bütünleştirmesi gerekir.
- 03-12: T1–T4 şartnamesi güncellendi; fiziksel 1 px T1 kayması ekran yakınlaştırmalarından ayrıldı, T2 strict SNR>50 ve faz/eksen raporu, T3 SNR-dilimi oranı ve JSON alan uygulanabilirliği açıklandı.
- 03-13: Sentetik faz taraması ve iki grafik hazır; 07-05 üretim T2/T3 testleri ile 03-03 merkezleme uyum arayüzü H-06, grafiklerin görsel kabulü H-07 bekliyor.
- 07-04: T1 gerçek Stage 0 penceresinde ePSF enjeksiyonu `Δx=0.998404 px`, `np.roll Δx=1.000000 px`; T4 dokuz gerçek SIP-3 kesitte 7.569 piksel, max hata 4.47e-11 px. T1 ekran/Playwright ve 100 gerçek penceredeki D3 için H-11 girdisi eksik; görev kısmi.
- 04-12: RW Aur/R Dra için yalnız UNKNOWN/photometry-not-run JSON+SVG yazıldı. Stage 0 TAP hataları sıfır kare kanıtı değil; gerçek λ eğrisi, kontrol yıldızı ve 3σ değerlendirmesi H-12 girdileri olmadan yapılamaz.
- 04-04: WISE 0855 kapsamı `unknown`; TAP/SIA sorgu başarısızlığı sıfır kare demek değildir. Kanonik Liste 01 kare/geçiş çıktısı H-09 gelene kadar zorlanmış fotometriyi başlatma.
- 04-03: piksel düzeyindeki sentetik fotometri/coadd prototipi hazır; RA/Dec→WCS kare akışı ve çıktı dosyası gerçek veri entegrasyonu H-08 bekliyor.
- 04-06: sentetik hareketli iz bağlama kodu hazır; gerçek asteroid için ortak tangent düzlemi WCS/FITS ve üç karelik kaynak kataloğu H-10 bekliyor. İki noktalı hız hipotezleri mevcut; planlanan hız ızgarası henüz yok.
- Gaia, ePSF ve sentetik kaynak testleri için CVAT/elle etiketleme gereksinimi saptanmadı.

## Current parallel batch

- Live updates: 08-01 complete; 00-05, 01-03, 03-02, 03-07, 03-06, 04-02, 04-07 and 04-15 in progress. Status updates explicitly authorized by user.
- Four agents own disjoint files: 04-02 stacks, 04-07 OUTLIER candidates, 04-15 rolling window and 03-06 joint-fit outputs. No final scientific acceptance claimed yet.
- Merged origin/main 449567a into feature branch; A pixel/mask modules are now available. Earlier blanket H-01 missing-code claim needs integration-level review.
- Corrected veto flag mapping: TRANSIENT bit0, HALO bit28 (OUTLIER remains bit19).
- Installed reproject0.21.0 in Stage0 venv for task-required exact TAN reprojection.

## Parallel code delivered

-04-02:stack_pass,difference_stacks,validation_metrics,compare_stack_modes,write_stack_products; exactTAN reprojection and same-channel restrictions.9 focused tests.
-04-07:promote_outliers+score_linked_candidates+JSON; SOURCE/OUTLIER retained; raw8connected compact<=40pixel components.7 focused tests; movers12/12.
-04-15:rolling_window+frame role list,inside/outside references through04-02.8 focused tests.
-03-06:full2x2covariance,framechi2,JSON output,block sparse numericalJacobian;4 focused tests.1000trialcoverage not yet finished.
-RealBarnard/Gaia/2026 acceptance is pending task-specific reports; no new real detection/measurement invented.
