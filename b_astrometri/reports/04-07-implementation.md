# 04-07 — OUTLIER terfisi: uygulama ve kabul sınırı

`movers/outlier_candidates.py`, gerçek Alan A `process/masks.py` sabitlerini ve
`build_pixel_mask(..., profile="mover_search")` işlevini kullanır. Maske yalnız
`0x3C028E44`; OUTLIER (19) ve SOURCE (21) bu bitler nedeniyle silinmez.

## İşlem

`promote_outliers` FLAGS üzerinde 8-bağlantılı bileşenleri bulur. Ham bileşenin
boyutu **≤40 piksel** olmalıdır; fit-mask uygulanmadan önce boyut sayılır.
Kullanılabilir piksel kalmadığında veya konum Gaia/katalog konumuna eşleştiğinde
terfi edilmez ve nedeni `component_log` içinde kalır. SOURCE içindeki kümeler
korunur. Mevcut kare tespitiyle eşleşen küme yeni mükerrer tespit yaratmaz;
eşleşmeyen küme geometrik merkezli ek aday olur. Bu merkez hassas astrometri değildir.

`outlier_score_bonus=1` **[ASSUMPTION]**, 04-11 kalibrasyonu bekler.
`score_linked_candidates` mevcut 04-06 `detection_refs` kimliklerini kullanarak
bu ek kanıtı skora ekler; iz yaratmaz veya silmez. OUTLIER olmayan karelerde
normal katalog tespitleri aynen korunur. Farklı karelerden adaylar bağlanmadan
önce tüm x/y konumlarını ortak tangent düzlemine dönüştürmek çağıranın görevidir;
yerel pencere piksellerini doğrudan çapraz-kare bağlamak geçerli değildir.

`static_positions` verilirse gerçek terfi edilen adaylara uzaklıkla pay/payda
ve oran ölçülür. Verilmezse `not_measured`; boş referans havuzu oranı `null`.
Gaia/katalog sonucu açık girdi olarak zorunludur. `write_candidates` adayları,
tespitleri, reddetme nedenlerini ve istatistikleri JSON'a yazar.

## Doğrulama

```powershell
& C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe -I -m unittest discover -s b_astrometri/movers -p test_outlier_candidates.py -v
```

Testler: 8-bağlantı; 40 dahil / 42 hariç; fit-mask; SOURCE korunması;
katalog eşleşmesi; mükerrer tespitin önlenmesi; ölçülen sentetik referans oranı;
OUTLIER'sız üç sentetik karede gerçek 04-06 bağlayıcısının çalışması; ek skor;
FLAGS/girdi doğrulaması ve JSON yazımı.

## Gerçek veri kabulü açık

- **[NV]** Üç seyrek karede 17 asteroidin OUTLIER taşıyan 11'inin yeniden bulunması.
- **[NV]** Gerçek sabit yıldız terfi oranının yeniden ölçümü ve tarihsel %2,6–3,7 ile karşılaştırma.
- **[NV]** 2026W12/13 gerçek karelerinde OUTLIER-adayı sayısı ve bağımsız bağlama.

`docs/stage0/s0_D.md` içindeki 11/17 ve %2,6–3,7 tarihsel rapor sonuçlarıdır;
bu uygulamanın yeni ölçümleri değildir. 2026 koruması şu anda sentetik sıfır-OUTLIER
testiyle sınırlıdır. Gerçek FLAGS/kare katalogları ve ortak WCS girdileriyle kabul
koşulları çalıştırılmadan görev tamamlandı sayılmaz. CVAT/elle etiketleme ihtiyacı
saptanmadı; katalog ve bilinen asteroid karşılaştırması gerekir.
