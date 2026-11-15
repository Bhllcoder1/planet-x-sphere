# Alan A Karar Kayıtları ve Protokoller (00-01, 00-07, 00-09, 01-13, 08-14)

## 1. Karar Kaydı: Drizzle KAPALI (Görev 00-01)
- **Karar:** Drizzle (seviye 2 alt-piksel yeniden örnekleme / birleştirme) **KAPALIDIR** (`[V: DECISIONS_AND_TASK.md]`).
- **Gerekçe:**
  1. Yeniden örnekleme (interpolation / drizzle) gürültüyü komşu pikseller arasında korele eder, PSF çekirdeğini bulanıklaştırır ve ePSF merkezleme (centroid) ölçümlerinde sistematik piksel-faz yanlılığı (bias) üretir.
  2. Ölçüm verisi (`IMAGE`, `VARIANCE`, `FLAGS`) her zaman doğal dedektör ızgarasında (0-tabanlı float koordinatlar) tutulur; kesirli konumlar asla tam sayıya yuvarlanmaz (ör. `x = 4.47`, `zoom = 100` iken ekran koordinatı `447.0 ± 0.5 px` olarak çizilir).
  3. Parlaklık yayılımı ("smooth shift") yalnızca **etiketli salt-görüntüleme (view-only)** modunda sunulabilir; astrometri ve fotometri bu görüntüler üzerinde asla çalıştırılmaz.

---

## 2. Dürüstlük Protokolü: Etiket Kuralları (Görev 00-07 & 08-14)
Tüm kod çıktılarında, raporlarda, JSON manifestlerinde ve CSV başlıklarında aşağıdaki üç etiket zorunludur:
- **`[V]` (Verified / Doğrulandı):** Gerçek SPHEREx / Gaia / SkyBoT verisi veya birim testi ile bizzat çalıştırılarak kanıtlanmış bulgu (ör. `[V: s0_B §4]`).
- **`[NV]` (Not Verified / Doğrulanmadı):** Henüz gerçek veriyle veya hedef ortamda ölçülmemiş durum (ör. `[NV: us-east-1 D9 gecikmesi]`). Doğrulanmamış hiçbir iddia yapılmış gibi gösterilmez.
- **`[ASSUMPTION]` (Varsayım):** Tasarım veya planlama amacıyla seçilmiş, doğrulama bekleyen eşik veya tahmin (ör. `[ASSUMPTION: fit-mask > %50 eşiği]`).
- **Dürüst Sonuç Kuralı (Görev 08-14):** Yarışmanın 5 test hedefinden (Barnard'ın Yıldızı, ε Indi B, WISE 0855, RW Aur, R Dra) herhangi biri SPHEREx verisinde düşük S/N veya arşiv kapsamı nedeniyle saptanamazsa, başka bir cisimle değiştirilmez; ölçülen üst sınır / S/N ve kapsam durumu dürüstçe raporlanır.

---

## 3. İnce Dilim (Thin-Slice) Kesme Sırası (Görev 00-09)
Zaman veya kaynak kısıtı durumunda özellikler aşağıdaki sırayla kesilir (`[V: DECISIONS_AND_TASK.md, PLAN_spherex_v3.md §4]`):
1. **İlk kesilecekler (MCD dışı):** Drizzle, yapay zekâ büyütme (AI upscaling), WISE/unWISE katmanı, kiralık GPU (`shift-and-stack`), Aladin Lite yan paneli, ML tabanlı real/bogus sınıflandırıcı.
2. **Koşullu kesilecekler:** Geçiş başına yığınlama (per-pass stacking) — yalnızca WISE 0855 tekil karelerde/zorlanmış fotometride saptanamazsa devreye alınır.
3. **Asla kesilmeyecek çekirdek (MCD):**
   - 5 yarışma hedefinin kapsam ve S/N durumu,
   - Aynı dedektör içinde Mode N (veya dönme > sınır ise R-k) blink,
   - Doğal float koordinatlarda ePSF merkezleme (Barnard için `saturated-fit` kanat uyumu) ve Gaia DR3 karşılaştırması,
   - Değişen yıldızlar (RW Aur, R Dra) için temel dönem/dalga boyu parlaklık paneli.

---

## 4. Stage 0 Kapanış ve Geçit Tablosu (Görev 01-13)

| Stage 0 Testi | Durum | Temel Sonuç | İlgili Görev / Liste |
|---|---|---|---|
| **s0_A** (Kapsam, Başlıklar, Roll) | Kısmen Tamamlandı `[V: s0_A.md]` | Barnard (358 kare, 3 geçiş) ve ε Indi A/B (460/458 kare, 4 geçiş) doğrulandı. Geçiş içi roll yayılımı 0.72°–3.84°; `SPS_EPA` yönelimi belirler. WISE 0855, RW Aur, R Dra senkron TAP zaman aşımına uğradı. | `01-02` (Async TAP), `01-09` (L0 donmuş listeler) |
| **s0_B** (S3 Okuma, Kesit, ePSF) | Tamamlandı `[V: s0_B.md]` | S3 anonim Range GET 0/30 hata ile çalıştı; HDU dizinleri `IMAGE=1, FLAGS=2, VARIANCE=3, ZODI=4, EPSF=5, WCS-WAVE=6`. Parent-piksel kuralı `< 1e-7 px` doğrulandı. Barnard çekirdeği 2×2 NaN. | `01-10`, `02-02`, `02-03`, `02-08` |
| **s0_C** (WCS vs Gaia ve Aberasyon) | Tamamlandı (A, B, C kareleri) `[V: s0_C.md]` | 3 farklı mevsimde başlık WCS'i Gaia DR3 konumlarını ~0.03 px (0.17") ortalama farkla veriyor; yıllık aberasyon (6–12") WCS çözümünün içine emilmiş durumda. Sabit kayma (shift-only) modeli yeterli. | `01-04` (Tamamlandı), `03-09`, `03-10` |
| **s0_D** (Maskeler ve Asteroitler) | Tamamlandı `[V: s0_D.md]` | 17/17 asteroit çekirdeği fit maskesinden sağ çıkıyor; 11/17'sinde `OUTLIER` (bit 19) var. `STREAK` (25) ve `GHOST` (22–24) merkezlemede maskelenir; `CROSSTALK` (20) ve `TRANSIENT` (0) uyarı bayrağı olarak kalır. | `02-04`, `02-09`, `04-07`, `04-08` |
