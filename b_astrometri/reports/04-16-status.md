# 04-16 — Kaydır-ve-Topla Görünümü (Sonra): Durum

**Durum:** Gelecek görev — 02-16 bekleniyor.

## Engelleyen koşullar

| Önkoşul | Açıklama | Sahip |
|---|---|---|
| 04-15 | Kayan pencere toplama | Bu dal — yerel ✓ |
| 02-16 | Viewer altyapısı (hız girişi + kare kaydırma) | Atanmamış |

## Yerel durum

04-15 kayan pencere toplama yerel olarak tamamlandı (8 test, `lightcurves.py`).
Shift-and-add için kullanıcının hız girmesi ve viewer'ın kareler boyunca kaydırması
gerekiyor — bu 02-16 kapsamında.

## Sonraki adım

02-16 viewer hız girişi hazır olduğunda `shift_and_add(frames, vx, vy)` arayüzü
04-15 üzerine eklenebilir.
