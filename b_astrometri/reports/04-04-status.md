# 04-04 — WISE 0855 Saptanabilirlik Testi: Durum

**Durum:** Engellenmiş — H-09 ve H-08 bekleniyor.

## Engelleyen koşullar

| Önkoşul | Açıklama | ID |
|---|---|---|
| H-09 | Liste 01 — WISE 0855 kapsam sorgusu sonucu | Akif ekibi |
| H-08 | Liste 03 — ePSF ızgarası ve WCS düzeltmeli kesitler | Akif ekibi |

## Yerel durum

Zorlanmış fotometri modülü (`04-03`, `forced_phot.py`) hazır — sentetik piksel
testleri geçiyor. Ters-varyans ağırlıklı geçiş toplama (`combine_forced_flux`) da
hazır. WISE 0855 gerçek verisi için:

- Liste 01 TAP sorgusu önceki oturumda başarısız oldu (HTTP 500/503).
- Kapsam çerçeve sayısı bilinmiyor; H-09 yanıtı bekleniyor.
- S/N tahmini için H band bant genişliği ve ePSF ızgarası (H-08) gerekiyor.

## Sonraki adım

H-09 kapsam sonucu ve H-08 ePSF yolu alındığında `forced_phot` çalıştırılabilir.
