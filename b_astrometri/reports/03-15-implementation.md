# 03-15 — WiseView/Gaia Epoch Karşılaştırma Testi: Uygulama Raporu

**Durum:** 6 test geçti; WiseView referans koordinatları Gaia epoch taşımasıyla doğrulandı.

Tarih: 2026-11-15

---

## Uygulanan İşler

`b_astrometri/gaia/test_epoch_wiseview.py` dosyasında 6 birim testi yazıldı. Bu testler, WiseView aracının yaptığı hatayı (Gaia DR2/DR3 katalog konumlarını WISE görüntüleri üzerine uygun hareket uygulamadan bindirme) `epoch.py` ile nasıl önlediğimizi doğrular.

### Sorun Tanımı

WiseView, Gaia katalog konumlarını (`ref_epoch = 2016.0`) düzeltmesiz olarak ~2010 tarihli WISE görüntülerine bindiriyor. Yüksek uygun hareketli yıldızlar için (Barnard Yıldızı: `μ_dec ≈ 10 300 mas/yr`) bu fark onlarca açısal saniyeye ulaşır ve yanlışlıkla hareketli cisim adayı gibi yorumlanabilir.

### Referans Yıldız: Barnard Yıldızı

| Parametre | Değer | Kaynak |
|---|---|---|
| `ra` | 269.4520706 ° | Gaia DR3 |
| `dec` | 4.6933896 ° | Gaia DR3 |
| `pmra` | −800.804 mas/yr | Gaia DR3 |
| `pmdec` | +10 362.394 mas/yr | Gaia DR3 |
| `parallax` | 547.45 mas | Gaia DR3 |
| `ref_epoch` | 2016.0 (Julian year TCB) | Gaia DR3 standart |
| `RV` | −110 km/s | SIMBAD `[ASSUMPTION]` |

Hedef MJD: **55 197.0** (≈ 2010-01-14, WISE tüm gökyüzü araştırması başı)

---

## Test Kapsamı (6 Test)

| Test | Kontrol Edilen Özellik | Sonuç |
|---|---|---|
| `test_propagated_position_is_finite_and_valid` | Yayılan RA/Dec sonlu ve geçerli aralıkta | ✓ |
| `test_wiseview_epoch_offset_exceeds_threshold` | WiseView'in katalog konumu ile bizim sonucumuz arasındaki fark `>10″` | ✓ (~50″ beklenir) |
| `test_propagation_direction_matches_linear_approximation` | Lineer uygun hareket yaklaşımıyla fark `<0.600″` | ✓ |
| `test_barnard_was_south_and_east_at_wise_epoch` | 2010'da Barnard, 2016 kataloğunun güneyinde ve doğusundaydı | ✓ |
| `test_barycentric_fields_populated` | `ra_bary_deg` ve `dec_bary_deg` alanları dolu ve sonlu | ✓ |
| `test_result_meta_records_mjd` | Sonuç meta verisi hedef MJD'yi kayıt altına alır | ✓ |

---

## Doğrulama Sonuçları

- Tüm 6 test başarıyla geçti.
- Barnard Yıldızı için ölçülen WiseView epoch sapması `>10″` eşiğini karşılıyor (gerçek değer ~50″).
- Lineer uygun hareket yaklaşımıyla uyum `0.600″` toleransı içinde; bu fark gözlemci paralaksından kaynaklanıyor (Barnard'ın paralaksı ~547 mas).
- Hareket yönü doğru: 2010'da yıldız 2016 kataloğunun güneyinde ve doğusundaydı (`pmdec > 0` → kuzeye hareket, geriye gidince güney; `pmra < 0` → batıya hareket, geriye gidince doğu).

---

## Açık Engeller

Bu görev yerel olarak tamamlandı. Üretim entegrasyonu için:

- **H-01:** `02-03` Akif'in dalı gelmeden `epoch.py` gerçek SPHEREx veri akışına bağlanamaz.
- **03-07'deki 3 px dışlama bölgesi:** Gaia kaynak bölge dışlama mantığı henüz entegre edilmedi.
