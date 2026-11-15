# Risk Kaydı

> Kaynak: PLAN_spherex_v3.md §3, stage0/s0_A.md, stage0/s0_B.md, stage0/s0_D.md  
> Etiket kuralı: **[V: kaynak]** = doğrulandı; **[NV]** = doğrulanmadı; **[ASSUMPTION]** = varsayım; **[arith]** = aritmetik  
> Son güncelleme: 2026-11-15 (görevler 00-10, 00-11, 00-12)

---

## R1b — Getirme gecikmesi (S3 bölge dışı)

| Alan | Değer |
|---|---|
| **Durum** | Açık |
| **Etiket** | performans, veri-erişimi |
| **Kanıt** | S3 frame-window (4 HDU, 100×100, 1 MiB readahead): p50 **3.90 s**, p95 **12.73 s**, min 1.56 s, max 17.56 s, n=30 [V: s0_B §3]. Dosya açma p50 **5.1 s** (soğuk kare = açma + pencere) [V: s0_B §3]. Ölçüm **Ankara, konut bağlantısı** — us-east-1 bölgesi değil; bölge-içi gecikme [NV] (D9 ile test edilecek). |
| **Azaltma** | (1) Birleştirilmiş paralel Range GET: her HDU için tek istek ~0.8 MB; 4 HDU paralel → hedef p50 < 1 s (arith, [NV]). (2) Demo hedeflerini önceden çek (Barnard 358 kare, ~4.2 GB [arith]); demo canlı arşiv çağrısına bağımlı değil. (3) D9 testi (görevler 01-05, 01-06): bölge-içi VM'den 50 kare, koalesan okuma. |
| **Kapanış koşulu** | 01-06 (D9 testi) p50 < 1 s / frame-window kanıtlayınca **veya** tüm demo hedefleri önbellekte olunca kapanır. |

---

## R22 — TAP gecikmesi ve başarısızlıkları

| Alan | Değer |
|---|---|
| **Durum** | Açık |
| **Etiket** | veri-erişimi, güvenilirlik |
| **Kanıt** | Barnard TAP sync sorgusunda **202 s** (5 dakika sınırına yakın) [V: s0_B §1]. WISE 0855, RW Aur, R Dra TAP sorgularının hepsi başarısız: >60 dk deneme, HTTP 502 Proxy Error, zaman aşımı, bağlantı sıfırlama; async submit de 502 [V: s0_A §WISE0855/RWAur/RDra]. 6 hedeften 3'ünde kapsam bilinmiyor [NV]. |
| **Azaltma** | (1) Async TAP (`/async` uç noktası, poll, 15 dk tavan) + yeniden deneme/backoff zorunlu (görev 06-03). (2) L0 önbelleği: frame listesi bir kez indirilip dondurulur; demo TAP'a bağımlı değil. (3) UI: "arşiv meşgul, yeniden deneniyor" mesajı gösterir; sessiz hata asla. |
| **Kapanış koşulu** | Async TAP istemcisi (06-03) devreye alınınca ve L0 önbelleği (06-02) demo frame listlerini barındırınca kapanır. |

---

## R23 — Kesit servisi HTTP 503

| Alan | Değer |
|---|---|
| **Durum** | Açık |
| **Etiket** | veri-erişimi, güvenilirlik |
| **Kanıt** | 1 eşzamanlı istek sınırında 14 istekte **5 kez HTTP 503** "Server busy, retry later" [V: s0_B §3]. Başarılı isteklerde p50 **12.4 s**, p95 **15.9 s**; yanıt ~4 MB (boyuttan bağımsız) [V: s0_B §3]. 503 nedeni (hız sınırı mı, eşzamanlılık üst sınırı mı?) [NV]. |
| **Azaltma** | (1) S3 primer; kesit yalnızca S3 başarısız olursa son çare. (2) Demo yolunda asla kesit servisi kullanılmaz. (3) 1 eşzamanlı istek; 503 → 45 s bekle (görev 06-05). |
| **Kapanış koşulu** | Nezaket sınırları (06-05) uygulanınca ve hiçbir demo frame'inde kesit servisi kullanılmayınca kapanır. |

---

## R24 — Asteroit 1–3 piksel sapması

| Alan | Değer |
|---|---|
| **Durum** | Açık |
| **Etiket** | astrometri, hareket |
| **Kanıt** | 17 tespit edilen asteroidin gözlem konumu, SkyBoT efemeris tahmininden **1–3 piksel** sapıyor [V: s0_D]. Efemeris σ yalnızca 0.004–0.02" [V]. Olası nedenler (doğrulanmadı, [arith]): (a) s0_D en parlak piksel kullandı → ±0.5 px kuantizasyon; (b) gözlemci 500 (geocenter) vs LEO uzay aracı → ~7 000 km / 1.5 AU ≈ 6.4" ≈ 1.0 px ana kuşak nesne için; (c) zamanlama: 65"/h hızda 1 px ≈ 340 s. WCS tek kare ile doğrulandı [INTERIM: s0_C çerçeve A]. |
| **Azaltma** | (1) Eşleşme yarıçapını max(3 px, 3σ_eph) olarak genişlet; açıklanamayan sapmaları raporla. (2) 04-09: ePSF centroid ile yeniden ölçüm ve nedenin tanımlanması. |
| **Kapanış koşulu** | 04-09 ePSF centroid ile sapmayı yeniden ölçünce ve temel neden tanımlanınca (ya da "açıklanamaz, genişletilmiş yarıçap kullanılıyor" yazılınca) kapanır. |

---

## R25 — Kalabalık alanlar

| Alan | Değer |
|---|---|
| **Durum** | Doğrulandı |
| **Etiket** | kapsam, maske |
| **Kanıt** | Galaksi merkezi karelerinde SOURCE bayrağı piksel alanının **%100'ünde** [V: s0_D §2]. CROSSTALK %14–21 (Galaksi alanı) [V: s0_D §2]. PERSIST %66.5'e kadar (bazı kareler) [V: s0_D §2]. Mover bulucu 0/4 buldu (kalabalık test alanı) [V: s0_D]. |
| **Azaltma** | (1) SOURCE > kare piksellerinin %50'sinde → "kalabalık alan, astrometri güvenilmez" afişi. (2) SOURCE frame maskesi kullanılmaz; mover bağlaması kapalı. (3) CROSSTALK/TRANSIENT: nedenli veto (kaldırılmaz, bayrak eklenir). Eşik [ASSUMPTION]. |
| **Kapanış koşulu** | Kalabalık alan algılama ve afişi uygulanınca (02-04 / 02-13) kapanır. |

---

## R26 — Geçiş içi roll farkı

| Alan | Değer |
|---|---|
| **Durum** | Doğrulandı |
| **Etiket** | görüntüleyici, astrometri |
| **Kanıt** | Barnard D2 aynı geçiş içi roll açısı yayılımı: **0.72° / 0.72° / 1.42°** (3 geçiş) [V: s0_A roll tabloları]. ε Indi A D3: 1.08–3.84° (4 geçiş) [V: s0_A]. Karşı yönlü geçişler: Barnard D2/D5 180°'den 0.0–0.3° sapma; D1/D3/D4/D6 3.5–4.3°; ε Indi D3 6.7–7.8° (n=6/hücre) [V: s0_A]. SPS_EPA (0/180) yönü etiketler [V: s0_A başlıkları]. |
| **Azaltma** | (1) Mode N kuralı (PLAN v3 §2.2): otomatik yalnızca aynı dedektör **ve** θ_res·r_kenar ≤ 0.25 px iken. 31×31 pencere → θ_res ≤ 0.68°; bu eşiği çoğu Barnard D2 geçiş çifti geçer → R-k tetiklenir. (2) **R-k sunucu taraflı raster** MCD'de (görev 05-04). (3) θ_res / kayma rozeti her karede görünür. |
| **Kapanış koşulu** | R-k modu (05-04) devreye alınınca ve θ_res rozeti gösterilince kapanır. |

---

## R27 — OUTLIER bayrağı bazı yayınlarda sıfıra yakın

| Alan | Değer |
|---|---|
| **Durum** | Açık |
| **Etiket** | veri-kalitesi, hareket |
| **Kanıt** | 2025W51/52 karelerinde OUTLIER yaklaşık **%2**; 2026W12/13 karelerinde yaklaşık **%0** [V: s0_D]. Neden: alan farkı mı, dönem farkı mı, işleme versiyonu mu? [NV]. |
| **Azaltma** | OUTLIER promosyonuna (kompakt küme → aday) tek başına güvenilmez; destekleyici kanıt gerektir (komşu piksel, PSF uyumu). |
| **Kapanış koşulu** | 01-12 (OUTLIER nedeni) araştırması tamamlanınca ve sonuç mover bulucu parametrelerine yansıtılınca kapanır. |
