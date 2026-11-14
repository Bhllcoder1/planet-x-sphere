# 03-02 (D5) — ePSF Normalizasyon ve Yönelim Kontrolü (`d5_result.md`)

## Özet Durum

- `[V]` **Kendi-kurtarma ve 25× akı ölçeği (`d5_check.py`):** Hem `norm=1.0` hem `norm=25.0` için 36 alt-piksel kaymada (`{0.0, 0.1, 0.3, 0.5, 0.7, 0.9}` px) konum kurtarma hatası `< 0.001 px` doğrulandı; sabit görüntüye `×25` model uyarlandığında akı genliğinin `1/25` ölçeklendiği doğrulandı.
- `[V]` **Sentetik yönelim ayrımı (`compare_orientation`):** Asimetrik ePSF üzerinde 12 gürültülü sentetik kesitte normal yönelim (`PSF_TRANSPOSE=False`) devrik yönelime (`x <-> y`) göre açıkça düşük `χ²_ν` verdi.
- `[NV]` **200 gerçek yıldız (`02-07`) yönelim ve mutlak akı kalibrasyonu:** Akif'in `02-07` izole gerçek yıldız seçimi (`H-01`) henüz gelmediği için gerçek veri `χ²_ν` dağılımı çalıştırılmadı. Bu nedenle `03-02` ClickUp görevi **açık** bırakılır; `epsf.py` içindeki `PSF_NORM = 1.0` ve `PSF_TRANSPOSE = False` [ASSUMPTION] olarak korunur.
- `[NV]` **Dosya içi vs kalibrasyon ePSF bayt-bayt karşılaştırması:** Liste `01` sonucu gelene kadar L1b paylaşımı yapılmaz.
