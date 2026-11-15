# 01-03 — Gaia DR3 erişimi

Görev: https://app.clickup.com/t/z8qu5ddjvj

## Güncel durum

**Doğrulanmış varsayılan: 128 px yarı-boy.** B’nin aynı 1024×1024 penceresi 16 küçük ESA konisiyle tamamen sorgulandı: **16/16 OK**, 49.176 tekil kaynak, 67,364 saniye, sıfır yeniden deneme/yedek/cache hit. Dört eski ana bölge, her biri dört küçük koniyle kaplanır. Kod varsayılanı da 128’dir; 256 açıkça seçilebilir.

Kanıt: `C:/Users/behlu/reports/gaia-B-small-live-result.json`, birleşik `reports/gaia-B-small-validated.fits`. 11 sütun, ref_epoch=2016.0 ve 16 başarılı karo meta bilgisi kontrol edildi. Canlı koşu 128 ayarını açıkça verdi; birim testleri bu ayarın artık varsayılan olduğunu ve 16/16 gerekmesini doğrular. Büyük dört sorgu hâlâ 2/4. Konilerin pencere dışı ayak izleri farklı olduğundan katalog toplamları doğrudan karşılaştırılmaz.

Önceki büyük karo denemesinde iki karo doğrulandı (15.828 ve 16.604 kaynak); üçüncü karo 1×30, 2×45 ve 1×60 sn okuma sınırlarında zaman aşımına uğradı, dördüncü denenmedi. Eksik birleşik çıktı yayımlanmadı. Eski başarısızlık kanıtı `reports/gaia-B-live-result.json`.

ESA VOTable alanında `ID=SOURCE_ID`, `name=source_id` ayrımı gerçek yanıtla doğrulandı. Gaia paketi **35 birim testini** geçti; `test_fetch.py` 16 varsayılan karo ve son karo başarısızlığında yeni/eski çıktının korunmasını denetler.

## Çalıştırma

Depo kökünden (önbellek ve çıktı depo dışında kalmalı):

```powershell
& 'C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe' -I -m unittest discover -s b_astrometri/gaia -p 'test_*.py' -v
& 'C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe' -I b_astrometri/gaia/fetch.py --stage0-data 'C:/Users/behlu/spherex-kb/stage0/data/C' --frame B --providers esa --cache 'C:/Users/behlu/reports/gaia-fetch-small-cache' --output 'C:/Users/behlu/reports/gaia-B-small-validated.fits' --attempts 1 --timeout 15
```

Varsayılan sağlayıcı sırası ESA → MAST. Başarısız/kesilmiş yanıt önbelleğe alınmaz; yeniden çalıştırma yalnız yeni istemcinin doğrulanmış karolarını kullanır. `--timeout` bağlantı/okuma bekleme sınırıdır, bütün koşunun kesin toplam süre sınırı değildir. G<18 indirme seçimi korunur. Yeni paket yüklenmedi.

## Denemeler

| Seçenek | Durum | Kanıt / sınır |
|---|---|---|
| ESA 128 px small tiles | [V] B window 16/16, 49,176 unique sources, 67.364 s | Proven live response; now the default; one run only. |
| ESA yeniden deneme / async | [V] Tarihsel betikte var; [NV] yeni async karşılaştırma | Stage 0 C raporu eski B denemesinde 2/4 ve HTTP 500/reset kaydediyor. |
| MAST alternatif ayna | [V] Canlı HTTP 200 ama OK ardından OVERFLOW, 1,32 sn | Aynı küçük koni; bu yanıt tam katalog olarak kabul edilmez. |
| CDS VizieR | [V] Tarihsel bağlantı zaman aşımı; [NV] güncel erişim | Stage 0 C §2; bu oturumda tekrar denenmedi. |
| ARI Heidelberg / GAVO | [NV] | Güncel erişim ve sütun uyumu henüz denenmedi. |
| ABD makinesinden sorgu | [NV] | Erişim yok, makine kiralanmadı. Gerekirse kullanıcı kararı beklenir. |

Küçük sorgu: RA=269,452, Dec=4,693, yarıçap=0,01 derece, G<18; MAXREC=100. Süreler birer ölçümdür; başarı oranı tahmini değildir. Kanıt depo dışında `C:/Users/behlu/reports/gaia-live-probes.json`.

## Doğruluk kuralları

- Kaynak indirme G<18 komşuları korur; astrometri seçimi daha sonra 11<G<17, RUWE<1,4 ve izolasyon kuralları uygular.
- Sütunlar: source_id, ra, dec, parallax, parallax_error, pmra, pmdec, phot_g_mean_mag, ruwe, ref_epoch, astrometric_params_solved.
- Başta OK bulunması yeterli değildir: tablonun arkasındaki QUERY_STATUS=OVERFLOW/ERROR da sorguyu geçersiz kılar.
- Eksik karo varsa birleşik tam katalog yayımlanmaz. Eski Stage 0 FITS dosyaları doğrulanmış yeni önbellek diye kullanılmaz.
- Bilimsel veri ve önbellek kaynak deposunun dışında tutulur. Epoch/paralaks düzeltmesi bu erişim görevinin çıktısı değildir.

## Kaynaklar

- [Stage 0 C](stage0/s0_C.md): tarihsel deneyler ve MAST/ESA karşılaştırması.
- [MAST Gaia DR3 TAP](https://mast.stsci.edu/vo-tap/api/v0.1/gaiadr3/): resmi hizmet adresi.
- [IVOA TAP 1.1](https://www.ivoa.net/documents/TAP/20190927/REC-TAP-1.1.html): QUERY_STATUS ve sonuç kesilmesi sözleşmesi.
