# Kullanıcıya Sorular

> Kaynak: PLAN_spherex_v3.md §7, DECISIONS_AND_TASK.md  
> Son güncelleme: 2026-11-15 (görev 00-13)

## Yanıtlananlar

| # | Soru | Yanıt | Kaynak |
|---|---|---|---|
| Q2 | Aylık bütçe üst sınırı? | Bütçe şimdilik kısıt değil; demo için saatlik kiralama yeterli (birkaç saat) | DECISIONS_AND_TASK.md — "Budget is not a constraint for now" |
| Q4 | Beklenen trafik? | Jüri/demo (günde birkaç kullanıcı); 7/24 barındırma yok, genel trafik yok | DECISIONS_AND_TASK.md — "no 24/7 hosting, no public traffic" |
| Q5 | İlk 2 demo hedefi? | **Tüm 5 hedef** [V]: Barnard's Star, ε Indi B, WISE 0855, RW Aurigae, R Draconis (v3 varsayılanı değiştirildi) | DECISIONS_AND_TASK.md — kullanıcı kararı 2026-11-14 |
| Q6 | Drizzle (seviye 2): bir gün harca? | **HAYIR** — "sonraya" listede bırak | DECISIONS_AND_TASK.md — "user said NO" |
| Q-GPU | GPU stratejisi? | CPU-first; demo için vast.ai on-demand (yalnızca B.5 tetikleyicisi devreye girerse) | DECISIONS_AND_TASK.md — kullanıcı kararı |
| Q-ZODI | Zodi çıkarma gösterimi? | Açma/kapama düğmesi (ham / zodi / düz), varsayılan AÇIK + rozet; ölçümler etkilenmez | DECISIONS_AND_TASK.md — kullanıcı yorumlanmış cevap, **[NV] onay bekleniyor** |
| Q-ALADIN | Aladin Lite paneli? | Demo'da YOK (kullanıcı kararsız; önerilen varsayılan uygulandı) | DECISIONS_AND_TASK.md — 2026-11-14 |
| Q-ML | Küçük ML modeli (gerçek/bogus)? | Sonraya; şimdi yalnızca veri-toplama kancası (candidates_log) | DECISIONS_AND_TASK.md — görevler 04-18, 04-19 → "sonra" |

## Hâlâ cevaplanmadı

| # | Soru | Varsayılan | Öncelik |
|---|---|---|---|
| Q1 | **Hackathon son tarihi (tarih ve saat dilimi)?** | 7 gün → MCD + dilimler 1–2 | **YÜKSEK** — build sırasını ve acil durum planını belirler |
| Q3 | **Sağlayıcı / bölge?** | D9 testine göre; AWS us-east-1 veya Hetzner Ashburn; emin değilse AWS | ORTA — D9 (in-region zamanlama testi) sonucuna göre karar verilecek [NV] |

> **Q1 notu:** Kullanıcı henüz son tarihi bildirmedi; plan 7 günlük varsayımla ilerliyor.  
> **Q3 notu:** Hetzner Ashburn'ün varlığı ve fiyatı doğrulanmamış [ASSUMPTION]. D9 testi (EC2 us-east-1 + Hetzner, 50 çerçeve, koalesced okuma) yapılana kadar sağlayıcı açık.

## Ekran görüntüsü soruları (Q-H serisi)

PLAN_spherex_v3.md §7'den Q-H1, Q-H2, Q-H3 — kullanıcıya build ilerledikçe sorulacak.

| Soru | Ne zaman | Hedef |
|---|---|---|
| **Q-H1:** "Bu checkerboard görüntülerinde (zoom 3, 7 ve 16,5) gri, bulanık veya eşit olmayan genişlikte kare görüyor musunuz? (her görüntü için evet/hayır)" | Gün 2 — D1 checkerboard koşumundan sonra | Piksel-tam ızgara hizalamasını doğrula; Canvas2D ve WebGL2 çıktılarını karşılaştır |
| **Q-H2:** "Barnard pass blink: yıldızın adım attığını, saha yıldızları sabit kalırken görüyor musunuz? 'θ_res / offset' rozeti ve 'yeniden örneklenmiş R-k' etiketi anlaşılır mı?" | Gün 4 — Gaia eşleşmesi + WCS düzeltmesi + R-k raster tamamlandıktan sonra | Viewer çekirdek kullanılabilirliği; blink ve rozet tasarımı onayı |
| **Q-H3:** "Bu 6 görüntüden streç (asinh / doğrusal / zscale) ve koyu veya açık temayı seçin." | Gün 5 — Dağıtım + iki hedef render edildiğinde | Sunum görünümü kararı; kullanıcı tercihini yakalamak |
