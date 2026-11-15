# 04-19 — Gerçek/Sahte Hareketli Sınıflandırıcı (Sonra): Durum

**Durum:** Gelecek görev — 04-18 bekleniyor.

## Engelleyen koşullar

| Önkoşul | Açıklama | Sahip |
|---|---|---|
| 04-18 | Etiketlenmiş gerçek/sahte pozitif veri seti | Atanmamış |

## Yerel durum

Yerel olarak tamamlanmış hiçbir sınıflandırıcı bileşeni yok. Hareketli cisim
bağlama (`04-06`, `linker.py`) ve OUTLIER terfi (`04-07`) hazır — bunlar
sınıflandırıcı için özellik kaynağı olacak.

Planlanan: kural tabanlı skor (`04-07` çıktısından) ile küçük ML modeli karşılaştırması.

## Sonraki adım

04-18 etiketlenmiş veri seti hazır olduğunda kural skoru baseline ve küçük
sınıflandırıcı (örn. Random Forest, ~10 özellik) karşılaştırılabilir.
