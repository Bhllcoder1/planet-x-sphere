# 01-03 Gaia DR3 Karo İndirme İstemcisi

Tarih: 2026-11-15
Durum: Yerel prototip tamamlandı; piksel ölçeği WCS'ten okunuyor, timeout deadline zorunlu.

## Ne Yapıldı

`b_astrometri/gaia/fetch.py` — ESA ve MAST TAP uç noktaları üzerinden Gaia DR3
yıldız katalogunu karo karo indirir, önbelleğe alır ve FITS'e yazar.

## Temel Bileşenler

### `parse_catalogue(content)`

VOTable XML'ini ayrıştırır:
- Harici `STREAM` referansları yasaktır (güvenlik).
- `QUERY_STATUS = OK` zorunlu; eksik veya "OVERFLOW" ise `ValueError`.
- `source_id`, `ra`, `dec` için maske ve sonlu değer kontrolü.
- RA ∈ [0,360) ve Dec ∈ [-90,90] aralık doğrulaması.

### `fetch_tile(provider, query, cache, ...)`

Önbellek stratejisi:
- SHA-256 ile anahtar; `identity + sha256` meta-JSON ile doğrulama.
- Bozuk veya eksik önbellek sessizce yeniden indirilir.

Zaman aşımı:
- `timeout=(connect=min(10,t), read=t)` per-chunk boşta-kalma sınırı.
- `stream=True` + deadline döngüsü toplam aktarım süresini zorlar:
  monotonic clock `> started + timeout` ise `response.close()` + `Timeout`.

Yeniden deneme:
- 4xx (429 hariç) kalıcı hata → yeniden denemez.
- Diğer ağ/HTTP hataları: üstel bekleme (max 8s), `attempts` kadar.

### `frame_tiles(header, x0, y0, tile_half=128)`

WCS'ten piksel ölçeği:
- `proj_plane_pixel_scales(WCS(header))` → derece/piksel.
- Herhangi bir hata veya sıfır/negatif ölçek → geri dön 6.2″/px.
- `radius = tile_half × √2 × (px_scale / 3600) + 0.01°` güvenlik marjı.

Çerçeve 1024×1024 px; 128 px yarı ile 4×4 = 16 karo, 256 px ile 2×2 = 4 karo.

### `fetch_frame(header, x0, y0, cache, output, ...)`

- Tüm karolar başarılı olmalı; herhangi biri başarısızsa mevcut çıktı değişmez.
- `source_id` tekrarlanan girişleri `unique()` ile temizler.
- Atomik yazma (`os.replace`) — kesilmiş çalışma eski çıktıyı korur.

## Sütunlar

`source_id, ra, dec, parallax, parallax_error, pmra, pmdec,`
`phot_g_mean_mag, ruwe, ref_epoch, astrometric_params_solved`

## Test Kapsamı

35 birim test (`b_astrometri/gaia/test_fetch.py`):
- `iter_content()` ve `close()` akış davranışı mock'ları.
- coord-audit uyumlu: yarıçap hesabında `round()` yok.
- 4xx (429 dahil) yeniden deneme mantığı.
- Atomik yazma başarısızlık senaryoları.

## Açık Noktalar

| ID | Konu |
|----|------|
| H-01 | 02-03/02-12 dal yolu; üretim WCS'i ile entegrasyon |
| — | Gerçek SPHEREx karesinde 3px dışlama (04-10 araştırması) henüz çözülmedi |
| — | ESA TAP büyük sorgularda OVERFLOW verebilir; MAST yedek çalışıyor |

## Kullanılan Dosyalar

- `b_astrometri/gaia/fetch.py` — istemci
- `b_astrometri/gaia/test_fetch.py` — 35 test
