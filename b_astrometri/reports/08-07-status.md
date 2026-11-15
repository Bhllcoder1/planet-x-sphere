# 08-07 WISE 0855 — Kapsam Tablosu ve Tespit/Zorlanmış Fotometri

**Durum:** Engellenmiş — H-09 ve H-08 bekleniyor.

## Yerel Tamamlanan

- TAP sorgusu denendi: ESA ve MAST uç noktaları başarısız; `UNKNOWN` kapsamı [NV]
- 04-03 zorlanmış fotometri prototipi hazır; gerçek FITS bekliyor
- WISE 0855 parametreleri: T_efektif ~ 250 K, W2 ~ 14 mag, hareket ~ 8200 mas/yr

## Bloklar

| ID | Konu |
|----|------|
| H-09 | Liste 01 kapsam sorgusu sonucu — WISE 0855'in SPHEREx çerçevelerinde olup olmadığı |
| H-08 | Liste 03 ePSF/WCS — gerçek akı ölçümü için gerekli |

## Sonraki Adım

H-09 yanıtlandıktan sonra:
1. Kapsam tablosunu Liste 01 sonucuyla doldur
2. H-08 geldiğinde `forced_phot()` ile kare başı akı ölç
3. Çok soğuk (T < 300 K) hedef için S/N tahmini yap
