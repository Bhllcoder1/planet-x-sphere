# 04-17 — Sentetik Cisim Ekleme (Sonra): Durum

**Durum:** Gelecek görev — 02-16 bekleniyor.

## Engelleyen koşullar

| Önkoşul | Açıklama | Sahip |
|---|---|---|
| 03-01 | ePSF modeli | Bu dal — yerel ✓ |
| 02-16 | Viewer görüntüleme kopyası altyapısı | Atanmamış |

## Yerel durum

ePSF modeli (`03-01`, `epsf.py`) ve GriddedPSFModel hazır. Sentetik cisim ekleme
için:

- Görüntüleme kopyasına (viewer çıktısına) `SENTETİK` etiketli overlay gerekiyor.
- Bu overlay 02-16 viewer altyapısı kapsamında.

## Sonraki adım

02-16 görüntüleme kopyası hazır olduğunda `inject_synthetic(image, x, y, flux, epsf)`
fonksiyonu eklenebilir.
