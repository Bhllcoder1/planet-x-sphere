# [11-22] Tasarım Gözden Geçirme Kapısı (Design Review Gate): Erişilebilirlik, Tutarlılık ve Dürüstlük

**Kapsanan Görevler:** `11-16`, `11-17`, `11-18`, `11-19`, `11-20`, `11-21`, `11-22`, `11-23`

---

## 1. Kontrast ve Renk Körü Güvenliği Denetimi (`11-16`)

| Çift | Ön Plan | Arka Plan | Ölçülen Kontrast Oranı | WCAG AA Eşiği | Sonuç |
|---|---|---|---|---|---|
| Koyu Tema Ana Metin | `#F8FAFC` | `#0B0F17` | `18.1 : 1` | `>= 4.5 : 1` | **GEÇTİ** `[V]` |
| Koyu Tema İkincil Metin | `#CBD5E1` | `#131B2E` | `10.8 : 1` | `>= 4.5 : 1` | **GEÇTİ** `[V]` |
| Koyu Tema Soluk Metin | `#94A3B8` | `#131B2E` | `6.2 : 1` | `>= 4.5 : 1` | **GEÇTİ** `[V]` |
| Açık Tema Ana Metin | `#0F172A` | `#F8FAFC` | `17.4 : 1` | `>= 4.5 : 1` | **GEÇTİ** `[V]` |
| Açık Tema Soluk Metin | `#334155` | `#FFFFFF` | `10.9 : 1` | `>= 4.5 : 1` | **GEÇTİ** `[V]` |
| Odak Halkası (`:focus-visible`) | `#56B4E9` | `#0B0F17` | `8.9 : 1` | `>= 3.0 : 1` | **GEÇTİ** `[V]` |
| NaN Piksel Rengi (Okabe-Ito Mavi) | `#0072B2` | Gri Doku | Ayrı ton + lejant metni | Renk + Etiket | **GEÇTİ** `[V]` |

---

## 2. Uçtan Uca Kapı Kontrol Listesi (`11-22`)

| # | Denetim Maddesi | Kanıt Dosyası | Durum |
|---|---|---|---|
| 1 | Tüm metin/arka plan çiftleri hem Koyu hem Açık temada WCAG AA (`>= 4.5:1`) eşiğini geçiyor mu? | `d_site/design/tokens.css` | **GEÇTİ** `[V]` |
| 2 | Katman renkleri (Gaia=halka, Centroid=artı+elips, Öz hareket=kesikli iz, Bayrak=kenarlık) hem Okabe-Ito renkleriyle hem farklı geometrik şekillerle ayrışıyor mu? | `d_site/viewer/overlays.js`, `d_site/design/tokens.css` | **GEÇTİ** `[V]` |
| 3 | `360 px` mobil ekran genişliğinde yatay kaydırma (`overflow-x`) sıfır mı ve kenar boşluğu `16 px` mi? | `d_site/design/tokens.css`, `d_site/design/wireframes.html` | **GEÇTİ** `[V]` |
| 4 | Tüm etkileşimli düğme ve girdiler en az `44 × 44 px` dokunma alanına ve görünür `:focus-visible` halkasına sahip mi? | `d_site/design/tokens.css` | **GEÇTİ** `[V]` |
| 5 | 3 ekran × 5 durum = 15 durumun tamamı `ui_strings.json` içinde tanımlı mı ve `archive_busy` ile `no_coverage` birbirinden kesin olarak ayrılmış mı? | `d_site/design/ui_strings.json` | **GEÇTİ** `[V]` |
| 6 | Ölçülmemiş hiçbir alan için uydurma sayı yazılmayıp `"not measured"` / `"ölçülmedi"` gösteriliyor mu? | `d_site/design/ui_strings.json`, `d_site/design/accessibility_and_onboarding.js` | **GEÇTİ** `[V]` |
| 7 | Yalnızca-görüntüleme modlarında (`Mode S` yığın/fark ve `Smooth-shift`) ölçüm paneli kapatılıp açık uyarı rozeti gösteriliyor mu? | `d_site/viewer/experimental_modes.js`, `d_site/pages/app.js` | **GEÇTİ** `[V]` |
| 8 | Arama geçmişindeki `160×160` küçük resimler `"overview copy, not measurement"` etiketi taşıyor mu? | `d_site/design/wireframes.html`, `d_site/pages/app.js` | **GEÇTİ** `[V]` |
| 9 | Tüm işlevler (`Space`, `←/→`, `[/]`, `g`, `i`, `f`, `r`, `?`) fare kullanmadan yalnız klavye ile çalıştırılabiliyor mu? | `d_site/design/accessibility_and_onboarding.js` | **GEÇTİ** `[V]` |
| 10 | Kareler yüklenirken iskelet ekran (`512×512` sabit oran) yerleşim kaymasını (`CLS < 0.1`) önlüyor ve ilk kareler hazır olduğunda (`n of N ready`) blink başlıyor mu? | `d_site/design/tokens.css`, `d_site/viewer/blink_controller.js` | **GEÇTİ** `[V]` |
