# Hedef sonuç notu şablonu — 08-01

Her hedef için aşağıdaki altı bölümü kopyala; notu tek sayfalık tut. Her sonuç sayı, birim, belirsizlik veya neden verilmediği ve kanıt yoluyla birlikte yazılır. `[V: dosya/bölüm]` doğrulanmış kanıtı, `[NV]` doğrulanmamışı, `[ASSUMPTION]` varsayımı, `(arit)` yalnız hesaplanan beklentiyi belirtir. Tarihsel rapor değeri yeni ölçüm değildir. Boş alan bırakma; bilinmeyene `BİLİNMİYOR [NV]`, ölçülmeyene `ÖLÇÜLMEDİ [NV]: neden` yaz.

## 1. Kimlik ve veri kökeni

- Hedef: `<Barnard / Epsilon Indi B / WISE 0855 / RW Aur / R Dra>`; başka hedefle değiştirilmez.
- RA/Dec (deg, ICRS): `<değer ± belirsizlik; koordinat epoğu ve kaynak>`.
- Sorguda kullanılan konum/epok: `<değer; öz hareket/paralaks uygulaması ve kanıt>`.
- Release/koleksiyon ve veri yayım tarihi: `<ad; tarih veya BİLİNMİYOR [NV]>`.
- Pipeline/işleme sürümü; manifest/kare listesi; maske profili; analiz kodu sürümü: `<değerler ve yollar>`.

## 2. Kapsam

Geçiş = MJD kümeleri; ardışık kareler arasındaki boşluk **>30 gün** ise yeni geçiş. D1–D6 ayrı dedektörlerdir. Kapsanan kare sayısı ile ölçümde kullanılan kare sayısını ayır.

| Geçiş | Kapsanan / kullanılan kare | D1,D2,D3,D4,D5,D6 dağılımı | MJD min–max (gün) | Süre (gün) | SPS_EPA (deg), başlık örneklemi n | Durum / kanıt |
|---|---|---|---|---|---|---|
| `<no veya BİLİNMİYOR>` | `<n / n>` | `<altı sayı>` | `<min–max>` | `<değer>` | `<0/180; n>` | `<etiket; dosya>` |

Toplam kare/geçiş: `<n / n; kanıt>`. Sorgu deneme geçmişi: `<hizmet, sonuç/hata, log yolu>`. TAP başarısızsa kapsam hücreleri **BİLİNMİYOR [NV]** olur; `0 kare` sonucu çıkarılmaz. Sıfır yalnız tamamlanmış, sınırları belirtilmiş boş sorgu sonucuyla yazılır.

## 3. Tespit ve zorlanmış fotometri

| Dedektör / dalga boyu (µm) / geçiş | Kullanılan / reddedilen kare | Yöntem ve akı birimi | Akı ± σ | S/N ve tespit eşiği | Sonuç / kanıt |
|---|---|---|---|---|---|
| `<D, λ aralığı, geçiş>` | `<n / n; ret nedeni>` | `<tespit veya sabit konumda ePSF; birim>` | `<değer ± σ>` | `<ölçülen; Nσ eşiği ve kaynağı>` | `<tespit / eşik altında / ÖLÇÜLMEDİ>` |

Üst sınır varsa `<Nσ, birim, hesap yöntemi ve kanıt>` yaz; zorlanmış fotometri sonucunu kendiliğinden tespit sayma. Birim dönüşümü doğrulanmadıysa dönüştürülmüş akı yerine `[NV]` yaz.

## 4. Hareket ve karşılaştırma

- Geçiş çifti ve Δt (gün/yıl): `<değer; aynı dedektör/λ seçimi>`.
- Ölçülen Δx, Δy (px) ve göksel Δα*, Δδ (arcsec): `<değer ± σ; kovaryans/uyum kanıtı>`.
- Ölçülen μα*, μδ (mas/yıl), paralaks (mas): `<değer ± σ veya ÖLÇÜLMEDİ>`.
- Gaia/literatür beklentisi: `<değer ± σ; epok, kaynak ve dönüşüm>`; yalnız hesap ise `(arit)` etiketi.
- Ölçüm–beklenti farkı ve uyum kararı: `<belirsizlikle karşılaştırma; ölçüt kaynağı veya NV>`.

## 5. Uyarılar ve sınırlar

Her biri için `var / yok (kanıt) / bilinmiyor` seç: doygun/NaN çekirdek; çözülmemiş çift; değişken yıldız; kalabalık alan; kullanılan maske ve reddedilen bayraklar; küçük örneklem (n); arşiv hatası/kısmi veri. Epsilon Indi B için parlak Epsilon Indi A yanındaki **tek karışık, çözülmemiş kaynak** uyarısını değerlendir. RW Aur/R Dra'da farklı zaman ve dalga boylarının parlaklık farkına etkisini ayır.

**Bu notta ölçülmemiş olanlar:** `<zorunlu liste ve neden; hiç yoksa “yok” ve kapsanan ölçümlerin kanıtı>`.

## 6. Demo görünümü ve dürüst sonuç

- Paylaşılabilir URL ve ayarlar: `<hedef, FOV, dedektör, geçiş/kare, germe, arka plan, katmanlar>`.
- Tıklama yolu / ekran görüntüsü: `<adımlar ve dosya>`.
- Mod ve rozetler: `<N / R-k / S; WCS düzeltmesi, ofset, θ_res, release>`; S/yığın görünümü **yalnız görüntüleme, astrometri yok** olarak etiketlenir.
- Sonuç cümlesi: `<hangi release, kaç kare ve hangi Nσ eşiğiyle ne gösterildi/ölçülemedi>`; arşiv hatasını kapsam yok diye yazma.

## Doldurma provası — tarihsel kanıt, yeni analiz değil

**Barnard:** kimlik: Barnard Yıldızı; koordinat ve belirsizliği bu provada aktarılmadı `[NV]`. Stage 0 A raporunda 358 bilim karesi ve 3 geçiş var `[V: docs/stage0/s0_A.md, Barnard]`; koleksiyonlar dr1/qr3, pipeline 7.0.5; veri yayım tarihi `[NV]`.

| Geçiş | Kapsanan / kullanılan | D1,D2,D3,D4,D5,D6 | MJD min–max (gün) | Süre (gün) | SPS_EPA (deg); n | Kanıt |
|---|---|---|---|---|---|---|
| 0 | 118 / ÖLÇÜLMEDİ | 24,18,18,23,18,17 | 60902.87–60949.27 | 46.4 | 180; 8 | `[V: s0_A, kapsam/20 başlık örneklemi]` |
| 1 | 121 / ÖLÇÜLMEDİ | 18,18,24,18,19,24 | 61110.09–61165.08 | 55.0 | 0; 6 | `[V: s0_A, aynı bölümler]` |
| 2 | 119 / ÖLÇÜLMEDİ | 18,25,17,18,24,17 | 61268.63–61305.63 | 37.0 | 180; 6 | `[V: s0_A, aynı bölümler]` |

Tespit/S/N ve hareket ±σ: **ÖLÇÜLMEDİ [NV]**; bu görev ölçüm yapmaz (08-02/08-03). Uyarı: doygun/NaN çekirdek `[V: docs/stage0/s0_C.md §1]`; diğer uyarılar `[NV]`. Demo URL/rozetler **HAZIR DEĞİL [NV]** (08-04). Ölçülmemiş olanlar: fotometri, S/N, hareket, güncel kapsam ve demo. Başlık örneklemi bütün kareleri temsil eden ölçüm olarak sunulmaz.

**WISE 0855:** kimlik: WISE 0855; koordinat/öz hareket doğrulaması bu provada yapılmadı `[NV]`. Kapsam/geçiş/dedektör/MJD/SPS_EPA: **BİLİNMİYOR [NV]**. Tarihsel TAP denemeleri timeout/502/reset ile tamamlanamamış `[V: docs/stage0/s0_A.md, WISE0855 ve Completeness notes]`; bu **0 kare değildir**. Tespit/S/N, hareket ±σ ve görünürlük **ÖLÇÜLMEDİ [NV]**; üst sınır uydurulmaz. Uyarı: arşiv hatası, bilinmeyen kapsam; demo hazır değil `[NV]`. Ölçülmemiş olanlar: kapsam, fotometri/S/N, hareket ve demo. Sonuç: “Arşiv sorgusu tamamlanmadığından bu hedefin kapsamı ve tespiti henüz belirlenmedi.”

Kaynaklar (depo köküne göre): `docs/plan/SITE_SPEC.md` W17/W18; `docs/stage0/s0_A.md`; `docs/stage0/s0_C.md`; ClickUp [08-01](https://app.clickup.com/t/z8qu5ddjz8). Bu dosya, görevdeki eski `hedefler/_sablon.md` / `spherex-kb/hedefler_sablon.md` çıktı yollarının ürün deposundaki karşılığıdır.

## Doğrulama Kontrol Listesi

- [ ] Kapsam tablosu tamamlandı
- [ ] Zorlanmış fotometri S/N hesaplandı
- [ ] Hareket vektörü görüntülendi
- [ ] Uyarılar belgelendi
