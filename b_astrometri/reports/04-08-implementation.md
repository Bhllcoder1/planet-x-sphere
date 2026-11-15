# 04-08 Uygulama Raporu: STREAK/GHOST/CROSSTALK Vetoları ve Kalabalık-Alan Koruması

**Durum:** Yerel prototip tamamlandı; gerçek FLAGS maskeli görüntü H-10 bekleniyor.

---

## Uygulanan İşlevler

### `b_astrometri/movers/veto_guard.py`

#### Flag Bit Tanımları (SPHEREx Explanatory Supplement Tablo 16)

| Bit | Sembol | Değer |
|-----|--------|-------|
| 0 | TRANSIENT | `1 << 0` |
| 20 | CROSSTALK | `1 << 20` |
| 22–24 | GHOST | `(1<<22)|(1<<23)|(1<<24)` |
| 25 | STREAK | `1 << 25` |
| 28 | HALO | `1 << 28` |

**Önceki versiyon hatası:** TRANSIENT bit 0 (tablo doğru) idi; HALO bit 15 olarak kodlanmıştı (eski `a_veri_isleme` sabitlerinden). Düzeltildi: bit 28.

#### `evaluate_candidate_flags(flags, x_px, y_px, *, radius_px=3.0)`

Adayın `(x_px, y_px)` merkezinden `radius_px` (varsayılan 3 piksel) içindeki tüm FLAGS piksellerini OR'layarak veto ve uyarı kategorisi üretir:

- **Veto (linking devre dışı bırakır):** STREAK, GHOST (bit 22–24 herhangi biri), CROSSTALK
- **Caution (uyarı, veto değil):** TRANSIENT, HALO

Çıktı: `{"veto_reason": [...], "caution": [...]}` — her zaman liste, boş olabilir.

#### `tag_candidates(candidates, flags_by_frame, *, radius_px=3.0)`

Tüm aday listesini gezer; her adayın `observations` listesindeki frame bazlı FLAGS dizisinde `evaluate_candidate_flags` çağırır. Birden fazla frame'den gelen veto nedenlerini birleştirir. **Hiçbir aday silinmez** — `vetoed=True` olarak etiketlenir ve `candidates_log`'da tutulur.

```python
out["veto_reason"] = sorted(vetos)   # ["CROSSTALK", "STREAK"] gibi
out["caution"]     = sorted(cautions)
out["vetoed"]      = bool(out["veto_reason"])
```

#### `crowded_field_guard(source_fraction, local_noise, sparse_median_noise, ...)`

Kalabalık alan eşikleri **[ASSUMPTION]** — gerçek SPHEREx s0_D gc1..gc5 / sp1..sp6 parametrelerine göre kalibre edilmedi:

- `source_fraction > 0.50` → `SOURCE_GT_50PCT`
- `local_noise / sparse_median_noise > 5.0` → `NOISE_GT_5X_SPARSE`

Herhangi biri tetiklenirse `linking_enabled=False` ve `banner="kalabalik_alan"` döner; linking tamamen atlanır.

---

## `b_astrometri/movers/outlier_candidates.py` ile Entegrasyon (04-07)

`promote_outliers` OUTLIER bileşenlerini katalog konumlarıyla karşılaştırır; eşleşmeyenleri `detections` listesine `det_id="outlier:N"` ile ekler. `score_linked_candidates` bunları `04-06` link sonuçlarına `outlier_score_bonus` alanıyla enjekte eder.

**Not:** `outlier_candidates.py` doğrudan `a_veri_isleme.process.masks` modülünü içe aktarır (H-01 bağımlılığı); forced_phot.py'deki try/except fallback bu dosyaya uygulanmadı — `a_veri_isleme` kurulu olmadan import hatası verir [NV].

---

## Doğrulama

Yerel test koşusu (04-07 kapsamında):

```
b_astrometri/movers/: 11–12 test geçti
```

`veto_guard.py` için ayrı birim testleri yazılmadı. `tag_candidates` ve `crowded_field_guard` sentetik FLAGS dizileriyle kapsanmamış [NV].

---

## Açık Maddeler

| ID | Konu |
|----|------|
| H-10 | Gerçek asteroid kataloğu + WCS ile ≥3 kare üzerinde veto testleri |
| — | `crowded_field_guard` eşikleri (`0.50`, `5.0`) SPHEREx tasarım belgesine göre kalibre edilmedi [ASSUMPTION] |
| H-01 | `outlier_candidates.py`'deki `a_veri_isleme` import'u için try/except fallback eklenmedi |
