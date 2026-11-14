# Otonom Ajan Döngüsü (Agentic Loop)

Kullanıcı çıktısı veya ara onay beklemeden Behlül Anik'e atanan bağımsız görevleri sırayla eriten sürekli çalışma döngüsü.

## Döngü Adımları

1. **Durum ve Görev Oku**
   - `HANDOFF.md` ve `docs/second-brain/TASKS.md` dosyalarını oku.
   - Canlı ClickUp bağlantısı varsa `Behlül Anik` görevlerini oku; yoksa snapshot'ı yalnızca tarihli tarihsel kayıt olarak kullan. Snapshot'tan güncel durum çıkarma.
   - Bu iş döngüsü görev/yorum/mesaj durumunu ClickUp'ta değiştirmez; kullanıcı açıkça isterse ayrı işlem olarak ele al.
   - `H-01` (Akif 02-03/02-12) veya kullanıcı kararı/hesap erişimi bekleyen görevleri atla.
   - `WORK_PROTOCOL.md` sırasıyla (öncelik, bağımlılık yok, tek dosya sahipliği) sıradaki bağımsız görevi seç.

2. **Uygula ve Test Yaz**
   - Yalnız ilgili alan klasöründe (`b_astrometri/`, `docs/`, vb.) küçük, tek sorumluluklu kod ve birim testleri yaz.
   - Token/parola veya büyük bilimsel veri (FITS/önbellek) depoya ekleme.
   - Doğrulanmamış entegrasyonları `[NV]`, varsayımları `[ASSUMPTION]` olarak işaretle.

3. **Doğrula**
   - `C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe -I -m unittest discover -s b_astrometri/centroid -p 'test_*.py' -v`
   - `C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe -I -m unittest discover -s b_astrometri/gaia -p 'test_*.py' -v`
   - `git diff --check`
   - Tüm testler geçmeden bir sonraki adıma geçme.

4. **Kaydet ve GitHub'a Gönder**
   - `HANDOFF.md` dosyasına tamamlanan işi, test sayısını, sınırları ve sıradaki görevi ekle.
   - `git add` → `git commit` → `git push origin b/01-03-gaia-fetch`.

5. **Devam / Durma Koşulu**
   - Kullanıcı çıktısı beklemeden Adım 1'e dön.
   - Yalnız şu durumlarda dur ve kullanıcıya bildir:
     - Bağımsız görev kalmadı (kalanların tümü `H-01` veya dış ekip çıktısı bekliyor).
     - Test/ortam hatası iki denemede çözülemedi.
     - Yeni bir insan kararı/erişim gereksinimi (`HUMAN_ACTIONS.md`) ortaya çıktı.
