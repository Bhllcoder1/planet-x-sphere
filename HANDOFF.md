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
| Proje hafızası | `docs/second-brain/`, `HANDOFF.md`, `docs/AGENT_LOOP.md` | Güncel ClickUp bağlantısı yok; son snapshot 2026-11-15 ve yalnız o anın kaydıdır. |

## İnsan girdisi bekleyen adım

H-01: Akif'in 02-03 koordinat/piksel kuralları ile 02-12 L1 cache çıktılarının dal/klasör yolunu veya hazır olmadıkları bilgisini kullanıcıdan bekle. Yanıt gelene kadar üretim entegrasyonunu yapma. Bağımsız test/prototipler sürebilir.

## Son test (2026-11-15)

- **Döngü tur 2 (04-01):** `b_astrometri/motion/passes.py` + `test_passes.py` (4 test OK; Barnard 358 kare → 3 geçiş [46/55/37 gün], ε Indi B → 4 geçiş [46/45/15/10 gün]).

```powershell
& 'C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe' -I -m unittest discover -s b_astrometri/motion -p 'test_*.py' -v
# 4 test OK
& 'C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe' -I -m unittest discover -s b_astrometri/centroid -p 'test_*.py' -v
# 16 test OK
& 'C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe' -I -m unittest discover -s b_astrometri/gaia -p 'test_*.py' -v
# 30 test OK
git diff --check
```

ClickUp API aracı bu çalışma oturumunda mevcut değil. Görev durumu değiştirilmedi, yorum/mesaj gönderilmedi. Önceki anlık görüntüde bütün ilgili işler `to do` idi; güncel durumu ayrıca doğrulamadan aynı sonucu varsayma.
