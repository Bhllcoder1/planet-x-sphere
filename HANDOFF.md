# Planet XSphere — oturum devri

Son güncelleme: 2026-11-15. Ana proje hafızası: [Second Brain](docs/second-brain/README.md). Bu devir notundaki yerel uygulama/test durumunu ClickUp kabulü veya görev kapanışıyla karıştırma.

## Çalışma biçimi

- Yalnız Behlül Anik'e atanan görevler; `main` dalına doğrudan yazma.
- İnsan kararı/erişimi/elle inceleme gerekiyorsa bağlı adımı durdur, [HUMAN_ACTIONS.md](docs/second-brain/HUMAN_ACTIONS.md)'ye beklenen yanıtı yaz; bağımsız işleri sürdürebilirsin.
- FITS, büyük veri, API tokenı ve sırları depoya/sohbete koyma. Python'ı `-I` ile çalıştır.
- Yerel prototip, görev önkoşulları ve ClickUp kapanışını ayrı raporla.

## Depo ve uzak dal

- Depo: `C:/Users/behlu/planet-x-sphere`
- Etkin dal: `b/01-03-gaia-fetch`; başlangıç uzak ucu 2026-11-15'te `f0b34ac922a6235b9f959488cb93472b8c80afa8` olarak doğrulandı.
- Ana dal o kontrolde `449567a556001f758a74dc1c8d5f622569c57b51` idi.
- Kanıt ve FITS: depo dışı `C:/Users/behlu/reports/`; mevcut Stage 0 Python: `C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe`.

## Yerel çıktılar ve sınırlar

| İş | Yerel çıktı / kanıt | Açık sınır |
|---|---|---|
| 01-03 Gaia | `b_astrometri/gaia/fetch.py`; 11 erişim testi; küçük ESA konileri 16/16, 49.176 tekil kaynak | 4 büyük karonun 2'si kaldı; küçük koni kapsamı aynı kare penceresi için denetlendi. Önkoşul ve ClickUp kabulü ayrı. |
| 03-01 ePSF | `b_astrometri/centroid/epsf.py`; daha önce 6 test ve gerçek D2 smoke | Fiziksel akı normalizasyonu/yönelimi doğrulanmadı; 02-03/02-12 entegrasyonu bekliyor. |
| 03-07 epoch | `b_astrometri/gaia/epoch.py`; 11 epoch testi; kutup geometrisi vektörel yöntemle düzeltildi | 02-03 entegrasyonu, HEALPix/sorgu seçimi ve kovaryans belirsizliği açık. Barnard örneği RV=0 varsayımlı tahmindir. |
| 03-04 elips | `b_astrometri/centroid/ellipse.py`, `test_ellipse.py`; centroid test paketinde yer alıyor | ClickUp önkoşulu 03-03 doğrulanmadı; yerel modül ClickUp kapanışı demek değil. |
| 03-14 koordinat denetimi | `coord_audit.py`, `test_coord_audit.py`; statik denetim alt-piksel float/origin=1 kalıplarını arıyor | Kod/test prototipi var; 02-03 ve 03-03 önkoşulları doğrulanmadı. Görev kabulü açık. |
| 04-01 geçiş gruplama | `b_astrometri/motion/passes.py`, 4 test; Barnard 358 kare/3 pass, ε Indi B 458 kare/4 pass; gap listesi eklendi | Liste 02 manifesti bulunamadı; iki yerel kare listesinde `SPS_EPA` alanı yok. H-03 bekliyor, görev kabulü açık. Çıktılar `C:/Users/behlu/reports/04-01-passes/` altında. |
| Proje hafızası | `docs/second-brain/`, `HANDOFF.md`, `docs/AGENT_LOOP.md`, `graphify-out/` | ClickUp GET /user HTTP 401; 2026-11-14 tarihli snapshot güncel durum değildir. H-02 yerel token yenilemesi bekliyor. |

## İnsan girdisi bekleyen adım

H-01: Akif'in 02-03 koordinat/piksel kuralları ile 02-12 L1 cache çıktılarının dal/klasör yolunu veya hazır olmadıkları bilgisini kullanıcıdan bekle. Yanıt gelene kadar üretim entegrasyonunu yapma. Bağımsız test/prototipler sürebilir.

## Son test (2026-11-15)

- **Döngü tur 2 (04-01):** `b_astrometri/motion/passes.py` + `test_passes.py` (4 test OK; Barnard 358 kare → 3 geçiş [46/55/37 gün], ε Indi B → 4 geçiş [46/45/15/10 gün]).
- **Döngü tur 3 (03-02 kısmi/prototip):** `b_astrometri/centroid/d5_check.py`, `test_d5_check.py` (3 test OK) ve `d5_result.md` eklendi. `×1`/`×25` kendi-kurtarma (`< 0.001 px`) + `25×` akı ölçeği ve sentetik yönelim `χ²_ν` ayrımı doğrulandı; 200 gerçek yıldız (`02-07` / `H-01`) `[NV]` açık bırakıldı.

```powershell
& 'C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe' -I -m unittest discover -s b_astrometri/motion -p 'test_*.py' -v
# 4 test OK
& 'C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe' -I -m unittest discover -s b_astrometri/centroid -p 'test_*.py' -v
# 26 test OK
& 'C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe' -I -m unittest discover -s b_astrometri/gaia -p 'test_*.py' -v
# 30 test OK
git diff --check
```

ClickUp API canlı okuma denemesi yerel tokenla HTTP 401 döndürdü. Görev durumu değiştirilmedi, yorum/mesaj gönderilmedi. 2026-11-14 tarihli anlık görüntüde Behlül'e atanan 46 görevin tamamı `to do` idi; bunu güncel durum varsayma. Erişim için H-02'yi tamamlat; 04-01 üretim girdisi için H-03'ü yanıtla.
