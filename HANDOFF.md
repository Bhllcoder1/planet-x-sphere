# Planet XSphere — oturum devri

Son güncelleme: 2026-11-15, aktif geliştirme oturumu. Bu dosya Claude Code/Codex için kısa devir notudur; çalışma sonunda yenilenir. Ana hafıza: [Second Brain](docs/second-brain/README.md).

## Kullanıcının istediği çalışma biçimi

- Yalnız **Behlül Anik'e atanan 46 görev** üzerinde çalış. Tüm ekip işlerini üstlenme.
- Paralel ajanlarla bağımsız dosyalarda ilerle; sonuçları gözden geçir.
- Gerçek kullanıcı kararı/hesap erişimi/elle işlem gereken adımda dur, kullanıcıya sor, yanıt gelmeden bağımlı işi yapma. Bağımsız işler devam edebilir.
- İnsan işlerini [HUMAN_ACTIONS.md](docs/second-brain/HUMAN_ACTIONS.md) içine somut talimat ve beklenen çıktıyla yaz. CVAT/etiketlemeyi ihtiyaç ortaya çıkmadan kurma.
- Bu HANDOFF.md'yi her önemli iş grubundan sonra ve oturum sonunda güncelle.

## Depo ve veri

- Ürün: `C:/Users/behlu/planet-x-sphere`
- Dal: `b/01-03-gaia-fetch`; değişiklikler henüz commit edilmedi, push/PR yok.
- Kaynak deneyler: `C:/Users/behlu/spherex-kb/stage0`
- Python: `C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe`; `-I` kullan.
- Yeni çalışma kanıtları/veri: `C:/Users/behlu/reports/`; FITS/önbellek depoya eklenmez.
- Önce `AGENTS.md`, `CONTRIBUTING.md`, `docs/second-brain/NOW.md` oku. Dizin sahipliğine uy.

## Tamamlanan yerel çıktılar

| İş | Dosya / doğrulama | Sınır |
|---|---|---|
| Kalıcı hafıza | `docs/second-brain/` ve README bağlantısı | Görevler, kararlar, kaynaklar, insan adımları ayrı. |
| 00-05 çalışma protokolü | `docs/WORK_PROTOCOL.md`; 7 kural, 3 seçim provası | ClickUp'ta kapatılmadı. |
| 08-01 sonuç şablonu | `b_astrometri/reports/hedefler_sablon.md`; 6 bölüm ve tarihsel örnekler | Yeni bilimsel ölçüm yapılmadı; ClickUp'ta kapatılmadı. |
| 01-03 Gaia istemcisi | `b_astrometri/gaia/fetch.py`, `test_fetch.py`; 11 test geçti | Küçük karo alternatifi 16/16 başarılı; 49.176 tekil kaynak/67,364 sn. Önkoşul ve ClickUp kapanışı ayrı. |

## Aktif işler — aynı dosyaya tekrar ajan verme

1. **Gaia erişim ajanı tamamladı:** küçük koniler 16/16 başarılı. Sonuç `reports/gaia-B-small-live-result.json`, birleşik katalog `reports/gaia-B-small-validated.fits`. Yeniden ağ sorgusu gerekmiyor.
2. **03-01 ePSF prototipi tamamlandı:** `b_astrometri/centroid/epsf.py` ve `test_epsf.py`; 6 test ana ajan tarafından doğrulandı, gerçek D2 smoke/görüntü kanıtı alındı. `PSF_NORM=1`; fiziksel akı normalizasyonu açıkça doğrulanmamış. 02-03/02-12 üretim entegrasyonu ve 03-02 bağımsız normalizasyon/yönelim denetimi bekliyor.
3. **03-07 epoch prototipi tamamlandı:** `b_astrometri/gaia/epoch.py` ve `test_epoch.py`; kutup hatası vektörel yöntemle düzeltildi. Son 11 epoch ve 11 erişim testi ana ajan doğruladı (ePSF ile toplam 28). Barnard tahmin tablosu yenilendi: `reports/gaia-epoch-barnard.json`, docs/second-brain/IMPLEMENTATION.md. RV açık, belirsizlik uydurulmuyor; tam görev entegrasyonu açık.
4. **Graphify:** ayrı ajan `graphify-out/` çıktıları ve grafik yapılandırmasının sahibi. Bilim venv'inden ayrı uv ortamına kuruldu. Hedef yeni kod/proje hafızası; eski büyük plan/araştırma arşivleri kapsam dışı. Kalıcı graph.json, GRAPH_REPORT.md ve graph.html hazırlanıyor.

Araçtaki ajan oturumları başka uygulamaya taşınmaz. Devir sırasında çalışan süreç varsa önce durumunu kontrol et; dosyaları silme veya aynı işe ikinci süreç başlatma.

## Gaia bulguları ve tuzaklar

- ESA küçük koni HTTP200/OK; MAST aynı sorguda OK ardından OVERFLOW verdi. Varsayılan sıra ESA→MAST.
- VOTable'da `ID=SOURCE_ID`, `name=source_id`: Astropy `use_names_over_ids=True` gerekiyor; regresyon eklendi.
- Sondaki OVERFLOW/ERROR da reddedilir. Dış STREAM href reddedilir. RA/Dec sonlu ve geçerli aralıkta olmalı.
- Yeni B büyük karo önbelleği: 15.828 ve 16.604 satır. Üçüncü karo 30/45/60 sn sınırlarında zaman aşımı; dördüncü denenmedi. Eksik birleşik çıktı yayımlanmadı.
- Kanıt `reports/gaia-B-live-result.json`; doğrulanmış XML `reports/gaia-fetch-cache/`.
- Eski MAST B önbelleğinde 4 dosya var ama tarihsel OVERFLOW nedeniyle eksiksizlik kanıtı değildir.
- `--timeout` istek okuma bekleme sınırıdır; tüm komut için kesin toplam süre sınırı değildir.

## Kullanıcıdan beklenen tek bilgi

**H-01:** Akif'in 02-03 koordinat/piksel kuralları ve 02-12 önbellek çıktıları başka dal/klasörde var mı? Kullanıcıya soruldu, henüz yanıt yok. Üretim entegrasyonu beklesin; sentetik/yerel veri prototipleri devam edebilir. Hesap/etiketleme isteği yok.

## Sonraki somut adımlar

1. Graphify çıktısını ve örnek sorgusunu doğrula; grafiğin kapsamını ve son anlık görüntü tarihini kaydet.
2. Kullanıcının istediği TypeSafe skill `.agents/skills/typesafe-ai/` içine tek npx yöntemiyle kuruldu. İlgili işlerde SKILL.md oku. Görüntü/Box deneysel; canlı API denemesi yapılmadı. Skill canlı testten önce veri kapsamı/bütçe/onay ister; henüz test isteği yok.
3. EPSF kanıtı `reports/epsf-real-smoke.json` ve `reports/epsf-detector2-region220.png` içinde. Konum self-recovery fiziksel akı doğruluğu demek değildir.
4. Eksik önkoşullara bağlı görevleri tamamlanmış gösterme. 01-01 ortam mevcut ve çalışıyor; temiz kurulum/lockfile kabulü ayrı ve açık.
5. Kullanıcı H-01 yanıtı gelirse ilgili kodu inceleyip entegrasyon sözleşmesini netleştir. Sonrasında 03-02/04-03 sırasına geç.

## Test komutları

Depo kökünden PowerShell:

```powershell
& 'C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe' -I -m unittest discover -s b_astrometri/gaia -p 'test_*.py' -v
& 'C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe' -I -m unittest discover -s b_astrometri/centroid -p 'test_*.py' -v
git diff --check
git status --short
```

## ClickUp

API hesabı Behlül Anik doğrulandı; çalışma alanı ID `1100330000031287`. Anlık görüntü `reports/planet-xsphere-clickup-snapshot.json` (depo dışında; kişisel bilgiler içerebilir). Görev bağlantıları [TASKS.md](docs/second-brain/TASKS.md) içinde. Bu oturumda sadece API okundu: görev durumu/ataması/yorum değiştirilmedi, kimseye mesaj gönderilmedi. Anahtar kişisel yerel dosyada; içeriğini çıktı veya kaynak koduna yazma.
