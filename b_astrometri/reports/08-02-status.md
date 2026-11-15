# 08-02 Barnard Yıldızı — Kapsam Tablosu ve Zorlanmış Fotometri

**Durum:** Engellenmiş — H-01 ve H-08 bekleniyor.

## Yerel Tamamlanan

- 04-01 sentetik geçiş gruplama: Barnard 358 kare / 3 geçiş doğrulandı
- 03-05 kanat uyumu prototipi: NaN/OVERFLOW çekirdek sığdırma hazır
- 04-03 zorlanmış fotometri prototipi: sentetik piksel testleri geçiyor
- 03-01 ePSF GriddedPSFModel: 33×33, 5× örnekleme, NaN fix dahil

## Bloklar

| ID | Konu |
|----|------|
| H-01 | Akif'in `a_veri_isleme` / 02-03 dal yolu — üretim ePSF yüklemesi için gerekli |
| H-08 | Liste 03 ePSF HDU yolu + Liste 02 maskeler — gerçek akı ölçümü için gerekli |

## Sonraki Adım

H-01 ve H-08 yanıtlandıktan sonra:
1. Barnard kapsam sorgusunu Liste 01 TAP üzerinden çalıştır
2. `forced_phot()` ile gerçek kare başı akı ölç
3. Doygun çekirdek uyarısını (`saturated_fit`) kapsam tablosuna ekle
