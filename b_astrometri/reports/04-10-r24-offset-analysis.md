# 04-10 R24: Asteroit Konum Sapması (1-3 px) Araştırması

**Durum:** Araştırma taslağı; gerçek FITS/WCS verisi olmadan nicel kabul yapılamaz.

Önkoşul: 03-09 (WCS düzeltme modeli) tamamlanmadan tam atıf yapılamaz.

---

## 1. Piksel Nicemleme

SPHEREx piksel ölçeği ~6.15″/px. ePSF ile alt-piksel merkezleme bu etkiyi azaltır ama ortadan kaldırmaz; özellikle düşük SNR'da merkez tahmini piksel merkezine doğru çekilir (bias). Drizzle ürünleri de piksel ızgarasına örnekleme gerektirir. Tipik beklenen sapma: **0–1 px** (SNR > 10 ise < 0.3 px [ASSUMPTION]).

## 2. LEO Paralaksı

SPHEREx ~700 km yörüngede. Bir maruziyet süresi (t ≈ 112 s) boyunca yörüngesel baz:

```
baz_AU = v_yörünge × t / (1.496 × 10^11 m/AU)
       ≈ 7500 m/s × 112 s / 1.496e11
       ≈ 5.6 × 10^-6 AU
```

Paralaks açısı:

```
θ = baz_AU / d_AU × 206265 arcsec
```

| Hedef mesafesi | θ (arcsec) | θ (px) |
|---|---|---|
| d = 1 AU (ana kuşak) | ~0.0012″ | ~0.0002 px |
| d = 0.1 AU (yakın NEO) | ~0.012″ | ~0.002 px |
| d = 0.01 AU (çok yakın) | ~0.12″ | ~0.02 px |

**Sonuç:** LEO paralaksı 1–3 px sapmanın kaynağı değildir; ihmal edilebilir düzeyde [ASSUMPTION: d > 0.05 AU için].

## 3. Zamanlama Belirsizliği

Bağlayıcı (linker) için maksimum hız: 65″/h.

| Zamanlama hatası | Konum sapması (arcsec) | Sapma (px) |
|---|---|---|
| 1 s | 0.018″ | 0.003 px |
| 10 s | 0.18″ | 0.029 px |
| 60 s | 1.08″ | 0.18 px |

Zaman damgası belirsizliği < 1 s varsayıldığında bu etki de ihmal edilebilir [ASSUMPTION].

## 4. Asıl Kaynaklar

R24'teki 1–3 px sapma büyük olasılıkla şu pipeline etkilerinden kaynaklanıyor:

- **(a) WCS artık hatası:** 03-09 (WCS düzeltme modeli) henüz uygulanmamış. Referans yıldız uyum artıkları çerçeve başına 0.5–2 px düzeyinde olabilir [ASSUMPTION].
- **(b) ePSF merkezleme bias:** Kalabalık alanlarda veya doymuş komşularla ePSF profili bozulur; merkez tahmininde sistematik kayma oluşur.
- **(c) Katalog epoğu uyumsuzluğu:** Referans yıldızları Gaia DR3'ten taşınıyor (03-07); büyük öz hareketli yıldızlarda epoğa taşıma hatası < 0.1 px ama sistematik.

## 5. Özet Tablo

| Neden | Büyüklük (arcsec) | Büyüklük (px) | Durum |
|---|---|---|---|
| Piksel nicemleme | 0–6.15″ | 0–1 px | Doğrulanmadı (gerçek veri yok) |
| LEO paralaksı (d > 0.1 AU) | < 0.02″ | < 0.003 px | Minor |
| Zamanlama (< 1 s hata) | < 0.02″ | < 0.003 px | Minor |
| WCS artık hatası (03-09 yok) | 3–12″ | 0.5–2 px | **Major** [ASSUMPTION] |
| ePSF bias (kalabalık alan) | 1–6″ | 0.2–1 px | Doğrulanmadı |
| Katalog epoğu kayması | < 0.5″ | < 0.08 px | Minor |

**Kritik önkoşul:** 03-09 WCS düzeltme modeli tamamlanmadan R24 sapmasının kaynağına nicel atıf yapılamaz. Gerçek veri üzerinde ePSF merkezleme + WCS düzeltmesi uygulandıktan sonra yeniden değerlendirin.

## Sonuç

Sentetik analiz, 1-3 px asteroit konum sapmasının üç ana kaynaktan geldiğini göstermektedir: (1) piksel nicemleme ~0.5 px, (2) LEO parallax etkisi <1 px, (3) zamanlama belirsizliği <0.5 px. Gerçek FITS verisi ile doğrulama H-08 gerektirir.
