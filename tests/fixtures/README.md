# Test Fixtures

Bu dizin, `planet-x-sphere` test paketinin kullandığı tüm veri dosyalarını barındırır.

## Dizin Yapısı

```
tests/fixtures/
├── README.md                  — Bu dosya
├── manifest_example.json      — Örnek manifest (sürüm 2, Barnard hedefi, 1 kare)
├── real/                      — Gerçek FITS dosyaları (git'e eklenmez)
└── synthetic/                 — Sentetik test verileri (git'e eklenir, küçük boyutlu)
```

### `real/`

NASA IRSA SPHEREx S3 kovasından (`nasa-irsa-spherex`, us-east-1, anonim erişim)
indirilen gerçek Level-2 FITS dosyaları bu dizine konur.

**Bu dizin `.gitignore` kapsamındadır** — dosya boyutları 61–65 MB/kare arasında
olduğundan depoya dahil edilmezler. Yerel geliştirme ortamında gerçek veriyle çalışmak
için dosyaları manuel olarak indirip bu dizine yerleştirin.

Örnek bir kare S3 anahtarı:

```
dr1/level2/2025W34_2B/l2b-v27-2026-229/2/level2_2025W34_2B_0557_2D2_spx_l2b-v27-2026-229.fits
```

### `synthetic/`

Belirleyici (deterministik) biçimde üretilen küçük boyutlu test verileri bu dizinde
tutulur. Bu dosyalar git'e eklenir çünkü boyutları küçüktür ve test koşularını
tekrarlanabilir kılar.

Sentetik veriler `conftest.py` fixture'ları aracılığıyla üretilir; sabit tohum
(SEED = 42) sayesinde her çalıştırmada özdeş sonuçlar elde edilir.

## Sentetik Veri Üretimi

`conftest.py` iki temel fixture sağlar:

| Fixture | Açıklama |
|---------|----------|
| `fixed_seed` | `random` ve `numpy.random` modüllerini SEED=42 ile başlatır; `autouse=True` sayesinde tüm testlere otomatik uygulanır. |
| `synthetic_window` | 100×100 boyutunda, float32 tipinde, SEED=42 ile üretilmiş sentetik bir görüntü penceresi döndürür. |
| `manifest_example` | `manifest_example.json` dosyasını okuyarak bir Python sözlüğü olarak döndürür. |

Kullanım örneği:

```python
def test_window_shape(synthetic_window):
    assert synthetic_window.shape == (100, 100)
    assert synthetic_window.dtype == np.float32
```

## Sabit Tohum Kuralı (SEED = 42)

Tüm testlerde `SEED = 42` kullanılır. Bu kural:

- **Tekrarlanabilirlik** sağlar: aynı test, farklı makinelerde veya farklı zamanlarda
  çalıştırıldığında özdeş sonuç üretir.
- **Hata ayıklamayı** kolaylaştırır: rastgele veri nedeniyle intermittent (aralıklı)
  başarısızlıklar oluşmaz.
- **CI/CD uyumluluğu**: seed sabitlendiği için CI ortamında da yerel ortamla birebir
  aynı davranış gözlemlenir.

Yeni bir fixture yazarken her zaman `np.random.default_rng(SEED)` veya
`np.random.seed(SEED)` kullanın; `autouse=True` olan `fixed_seed` fixture'ı
modül düzeyindeki global durumu sıfırlamak için yeterli olmayabilir.

## HDU Düzeni (Referans)

SPHEREx Level-2 FITS dosyalarının HDU sıralaması:

| HDU | İsim | İçerik |
|-----|------|--------|
| 1 | IMAGE | Bilim görüntüsü (2040×2040, float32) |
| 2 | FLAGS | Kalite bayrakları |
| 3 | VARIANCE | Varyans haritası |
| 4 | ZODI | Zodyakal ışık katkısı |
| 5 | EPSF | Efektif nokta yayılma fonksiyonu |
| 6 | WCS-WAVE | Dalga boyu–uzamsal WCS |
