# Alan D (Furkan / `kişi-d`): Karar Kayıtları, Politikalar ve Riskler
**Kapsanan Görevler:** `00-02`, `00-03`, `00-04`, `00-06`, `00-08`, `00-14`, `10-01`

---

## 1. [00-02] Karar Kaydı: Yapay Zekâ ile Görüntü Büyütme (AI Upscaling) Bırakıldı
- **Karar:** Görüntüleyici ve veri işleme hattında yapay zekâ tabanlı üst-çözünürlük (AI super-resolution / GAN / diffusion upscaling) **kesin olarak kullanılmayacaktır** `[V: DECISIONS_AND_TASK.md, PLAN_spherex_v3.md §1]`.
- **Bilimsel ve Teknik Gerekçe:**
  1. Üretken veya öğrenilmiş üst-çözünürlük modelleri, gürültülü arka planda gerçekte var olmayan nokta kaynaklar (halüsinasyon yıldız/asteroit) üretebilir ve zaman serisi blink'te sahte hareketli cisim adaylarına yol açar.
  2. Piksel değerlerini doğrusal olmayan biçimde değiştirdiği için alt-piksel astrometri (`ePSF` merkezleme) ve akı (`MJy/sr`) korunumu bozulur.
  3. Projede yakınlaştırma yalnızca **tam sayı çarpanlarla (`z = 8..32`) ve en yakın komşu (`NEAREST`)** örneklemesiyle yapılır.
- **Doğrulama Kanıtı:** `a_veri_isleme/requirements.txt` ve proje bağımlılıklarında hiçbir üst-çözünürlük, GAN veya difüzyon paketi bulunmamaktadır `[V]`.

---

## 2. [00-03] Karar Kaydı: Kapsam = Yarışmanın 5 Test Hedefi
- **Karar:** Projenin taahhüt edilen kapsamı, yarışma metninde adı geçen **5 test hedefidir** `[V: DECISIONS_AND_TASK.md]`. Gösterilemeyen veya arşivde kapsamı/S/N oranı yetersiz çıkan hiçbir hedef sessizce başka bir gök cismiyle **değiştirilmez**; sonuç olduğu gibi dürüstçe raporlanır.

| # | Hedef Adı | ICRS RA (J2000 / 2026) | ICRS Dec (J2000 / 2026) | Öz Hareket (μα*, μδ) | SPHEREx Durumu & Özel Not |
|---|---|---|---|---|---|
| 1 | **Barnard's Star** | `269.452075°` (`17h57m48.50s`) | `+04.693391°` (`+04°41'36.2"`) | `-801.55, +10362.39 mas/yr` `[V: s0_A]` | **358 kare, 3 geçiş** `[V: s0_A]`. Çekirdekte 2×2 `NaN` doygunluk var `[V: s0_B]`; `saturated-fit` kanat uyumu ile ölçülür. |
| 2 | **Epsilon Indi B** | `330.872408°` (`22h03m29.38s`) | `-56.793797°` (`-56°47'37.7"`) | `+3966.67, -2536.19 mas/yr` `[V: s0_A]` | **458 kare, 4 geçiş** `[V: s0_A]`. Parlak ε Indi A'nın yanında çözülmemiş kahverengi cüce çifti (Ba+Bb); tek kaynaşmış kaynak ve uyarı rozetiyle gösterilir. |
| 3 | **WISE 0855−0714** | `133.795129°` (`08h55m10.83s`) | `-07.245147°` (`-07°14'42.5"`) | `-8118, +680 mas/yr` `[ASSUMPTION: lit]` | Senkron TAP zaman aşımına uğradı `[V: s0_A]`, kapsam asenkron TAP (`01-02`) ile doğrulanacak `[NV]`. Saptanabilirliği (`04-04`) yığın (stack) gereksinimini belirler. |
| 4 | **RW Aurigae** | `076.956525°` (`05h07m49.57s`) | `+30.401408°` (`+30°24'05.1"`) | `+3.4, -20.8 mas/yr` `[V: s0_A]` | Değişen yıldız (T Tauri); senkron TAP başarısız `[V: s0_A]`, kapsam `[NV]`. Dönem/dalga boyu parlaklık paneli (`W15`) zorunludur. |
| 5 | **R Draconis** | `248.172546°` (`16h32m41.41s`) | `+66.754983°` (`+66°45'17.9"`) | `-11.2, -33.1 mas/yr` `[V: s0_A]` | Mira tipi değişen yıldız; senkron TAP başarısız `[V: s0_A]`, kapsam `[NV]`. Parlaklık ve dalga boyu karışıklığı uyarısı ile ışık eğrisi paneli zorunludur. |

---

## 3. [00-04] Karar Kaydı: Son Teslim Tarihi (Deadline) Sorusu ve Varsayılan
- **Kullanıcıya Sorulan Soru:** *"Hackathon son teslim tarihi (gün, saat ve saat dilimi) nedir?"*
- **Kayıtlı Durum:** Kullanıcıdan kesin saat gelene kadar planlama varsayılanı **7 gün** (`5 iş günü MCD + 2 gün tampon`) olarak sabitlenmiştir `[ASSUMPTION: DECISIONS_AND_TASK.md]`. Süre daralırsa `PLAN_spherex_v3.md §4.1` içindeki **3 günlük acil durum planı** devreye girer.

---

## 4. [00-06] Çalışma ve Model Kademesi Protokolü (`WORK_PROTOCOL`)
1. **Üç Model Kademesi:**
   - **Opus (`model-opus`):** Mimari kararlar, matematiksel formül ve koordinat/kovaryans denetimi (yalnız diff incelemesi), tasarım gözden geçirme kapısı (`11-22`).
   - **Sonnet (`model-sonnet`):** Çekirdek boru hattı modülleri, WebGL2/Canvas2D görüntüleyici, FastAPI uç noktaları, entegrasyon ve birim testleri.
   - **Haiku (`model-haiku`):** Şablon doldurma, kontak sayfası üretimi (`07-15`), dış bağlantı kontrolü (`05-19`), ekran görüntüsü toplama.
2. **Bir Brif = Bir Dosya Kuralı:** Her görev tek bir sorumluluk alanına ve açıkça tanımlanmış çıktı dosyalarına bağlanır; başka alanın (`a_veri_isleme`, `b_astrometri`, `c_sunucu`, `d_site`) dosyaları o alanın sorumlusundan habersiz değiştirilmez.

---

## 5. [00-08] Veri İşleme Güvenliği Politikası (`DATA_POLICY`)
İndirilen tüm astronomik arşiv verileri (FITS, CSV, JSON, VOTable, PDF) **güvenilmez girdi (untrusted input)** kabul edilir:
1. **Klasör Ayrımı:** İndirilen ham veriler yalnızca `data/` altında tutulur (`.gitignore` ile depodan dışlanmıştır). Çalıştırılabilir betikler asla `data/` içine konmaz ve `data/` çalışma dizini (`CWD`) yapılarak Python başlatılmaz.
2. **İzole Python (`-I`):** Tüm veri işleme ve test komutları `python3 -I` (isolated mode) ile çalıştırılır; böylece geçerli dizindeki veya kullanıcı ortamındaki sahte bir modülün (`astropy.py` vb.) yüklenmesi engellenir.
3. **Güvenli Serileştirme:** `pickle`, `shelve`, `marshal`, `eval()`, `exec()` ve `yaml.load()` kullanımı **kesinlikle yasaktır**; yalnızca `json`, `csv`, `astropy.io.fits` (standart başlık/veri okuma) ve ham ikili `float32`/`uint32` dizileri kullanılır.
4. **Ağ ve TLS:** Arşiv sorgularında (`IRSA`, `Gaia`, `MAST`) HTTPS ve TLS sertifika doğrulaması her zaman açıktır (`verify=True`).
5. **Yol Geçişi (Path Traversal) Koruması:** S3 veya kullanıcı girdisinden türetilen önbellek anahtarlarında `..` ve `/` karakterleri temizlenir (`build_l1_cache_key`).
6. **Sırların Korunması:** API anahtarları ve parola özetleri kaynak koduna veya Git geçmişine asla yazılmaz.
- **Stage 0 Betik Denetimi (`c7_analyze.py`, `c5_fetch.py`):** `docs/stage0/s0_C.md` kapsamındaki betikler incelenmiş; TLS doğrulamasının açık olduğu, verinin `stage0/data/` altında ayrı tutulduğu ve Python'un `-I` bayrağıyla çalıştırıldığı doğrulanmıştır `[V: s0_C.md §1]`.

---

## 6. [00-14] Risk Kaydı: R3/R4 Kapsam ve WISE 0855 Görünürlüğü, R17 Sağlayıcı

| Risk Kodu | Tanım | Durum & Etiket | Kapanış Görevi | Kapanış Ölçütü |
|---|---|---|---|---|
| **R3** | WISE 0855, RW Aur ve R Dra için senkron IRSA TAP sorgusu zaman aşımı / HTTP 502 verdi; kare sayıları bilinmiyor. | Açık `[V: s0_A, NV: kapsam]` | `01-02`, `01-09` | Asenkron TAP (`/async`, 15 dk tavan) ile sorgulanıp L0 donmuş kare listelerinin (`frames_*.json`) üretilmesi. |
| **R4** | WISE 0855 tekil SPHEREx karelerinde (özellikle D1–D4 kısa dalga boylarında) gürültü altında kalabilir. | Açık `[NV]` | `04-04`, `08-08` | D5/D6 dedektörlerinde zorlanmış ePSF fotometrisi ve geçiş başına ters-varyans toplamı ile S/N ölçülmesi; S/N < 3 ise dürüst sonuç kartında üst sınır olarak raporlanması. |
| **R17** | Sunum için kiralanacak bulut sunucusunun (AWS `us-east-1` vs Hetzner Ashburn) gerçek S3 okuma gecikmesi ve saatlik maliyeti. | Açık `[ASSUMPTION]` | `01-05`, `01-06` | `D9` 50 kare birleştirilmiş paralel S3 okuma testinin kiralık makinede koşulup `p50 < 1 s` hedefinin ölçülmesi. |

---

## 7. [10-01] `SITE_SPEC.md` Açık Sorular ve Arayüz Dili Kararı
Kullanıcı yanıtları ve varsayılanlarla kilitlenen `SITE_SPEC.md` kararları:

| # | Soru | Karar / Varsayılan | Etiket | Etkilenen Görevler |
|---|---|---|---|---|
| 1 | Arayüz dili (W24) | Varsayılan **İngilizce (`en`)**, tek tıkla **Türkçe (`tr`)** dil desteği (`ui_strings.json` üzerinden). | `[ASSUMPTION: SITE_SPEC W24]` | `10-02`..`10-16`, `11-18` |
| 2 | Gösterimde ZODI çıkarma varsayılanı | **Açık (`zodi`)**, köşede rozet ile; `raw` ve `flat` seçenekleri anahtarda mevcut. Ölçüm verisi etkilenmez. | `[V: DECISIONS_AND_TASK.md]` | `02-19`, `05-20`, `07-16` |
| 3 | Germe (stretch) limit kapsamı | Aynı dedektör grubunda tüm blink dizisi için **ortak limit (`sequence`)** varsayılan; kare başına (`frame`) opsiyonel. | `[V: DECISIONS_AND_TASK.md]` | `02-16`, `05-17`, `10-08` |
| 4 | Aladin Lite yan paneli | 5 günlük ana demoda **kapalı** (sonra listesinde, `L1`); tarayıcı dış sunucuya doğrudan çıkmaz. | `[V: DECISIONS_AND_TASK.md]` | `05-14` |
| 5 | Küçük ML modeli (real/bogus) | Ana demoda **kapalı** (`L4`); şimdi yalnız veri toplama kancası (`candidates_log`). | `[V: DECISIONS_AND_TASK.md]` | `04-18`, `04-19` |
| 6 | Drizzle ve AI büyütme | **Kapalı**; kesirli konumlar float olarak korunur, yumuşak kayma yalnız etiketli görüntüleme modudur (`05-13`). | `[V: 00-01, 00-02]` | `05-02`, `05-06`, `05-13` |
| 7 | Canlı koordinat girişi vs 5 hazır hedef | 5 hazır hedef (`W1`) tam önbellekli çalışır; serbest koordinat kutusu (`W2`) parse edilir ve önbellekte yoksa durum mesajı gösterir. | `[V: SITE_SPEC W1, W2]` | `10-02`, `10-14` |
| 8 | Kullanıcı hesap sayısı | Ön tanımlı tohum dosyasından (`USERS_COUNT`, en çok ~10 hesap), açık kayıt bağlantısı yok (`W25`). | `[V: SITE_SPEC §2a]` | `11-17` |
| 9 | Varsayılan tema ve kontrast | Koyu tema (`dark`), `percent 0.5/99.5` + `asinh (a=0.1)`. | `[ASSUMPTION: 05-11, 11-16]` | `05-11`, `10-08`, `11-16` |
