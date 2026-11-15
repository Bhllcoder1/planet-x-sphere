# 08-09 RW Aurigae — Kapsam Tablosu: Durum

**Durum:** Engellenmiş — H-09/Liste 01 ve H-08 bekleniyor

## Yapılanlar

- 08-01 sonuç notu şablonu mevcut (hedefler_sablon.md)
- Liste 01 TAP sorgusu denendi; başarısız oldu → kapsam (kare sayısı, geçiş sayısı) **bilinmiyor**
- Zorlanmış fotometri modülü (04-03/forced_phot.py) prototip olarak hazır

## Engelleyenler

| Bloke | Açıklama |
|---|---|
| H-09 / Liste 01 | SPHEREx kapsam sorgusu başarısız; RW Aur kaç karede var bilinmiyor |
| H-08 / Liste 03 | Gerçek ePSF grid ve WCS düzeltmesi olmadan akı ölçümü yapılamaz |

## Sonraki adım

H-09 (Liste 01 kapsam) ve H-08 (Liste 03 ePSF/WCS) teslim edildiğinde:
1. Kapsam tablosunu doldur (kare, geçiş, detektor)
2. 04-03 forced_phot ile per-frame akı ölç
3. 08-10 değişken yıldız uyarısını yaz
