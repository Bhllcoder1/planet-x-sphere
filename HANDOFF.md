# HANDOFF — planet-x-sphere (Alan C / newernever)

> Bu dosyayı okuyarak kaldığın yerden devam et.
> Bağlam kesintisi olursa: `git log --oneline -10` + bu dosya yeter.

## Proje özeti
NASA Space Apps hackathonu: SPHEREx taramasından 5 hedef gökyüzü bölgesinin zaman serisi görüntüleyicisi.
- Repo: `Bhllcoder1/planet-x-sphere` (private)
- Yerel: `C:/Users/Tahir/source/planet-x-sphere`
- Alan: **C** (sunucu, hesaplar, kiralama) → `c_sunucu/` ve `ops/`
- ClickUp: Planet XSphere çalışma alanı, token `pk_314539962_TCGPHKBBWYVKAQ21LFITV81MIJU070P3`
- GitHub token: `C:/Users/Tahir/OneDrive/Desktop/tokenc.txt` satır 5 (ghp_…)
- Git remote auth: `git -c http.extraheader="Authorization: Basic <base64(newernever:ghp_...)>"` ile push

## Tamamlanan görevler
_henüz yok — ilk push sonrası güncellenecek_

## Sıradaki görev
Şu an Grup 1 işleniyor:
- [x] docs/RISKS.md (00-10 R1b/R22/R23, 00-11 R24, 00-12 R25/R26/R27)
- [ ] docs/QUESTIONS.md (00-13)
- [ ] c_sunucu/.env.example + ops/SECRET_MANAGEMENT.md (06-10)
- [ ] tests/ dizin kurulumu (07-01)
- [ ] docs/STATUS.md (09-04)
- [ ] contracts/api.yaml + c_sunucu/api/mock_server.py (06-14)
- [ ] c_sunucu/api/main.py (06-01 FastAPI skeleton)
- [ ] c_sunucu/cache/ (06-02)
- [ ] c_sunucu/api/tap_client.py (06-03)
- [ ] c_sunucu/api/s3_reader.py (06-04)
- Sonra: 06-05, 06-06, 06-07, 06-08, 06-09, 06-11, 06-12, 06-13
- Sonra: 05-04, 05-10, 05-18, 10-03, 10-04, 10-15
- Sonra: 11-04..11-13 (hesaplar, giriş, geçmiş, profil)
- Sonra: 09-05, 09-09, 09-10, 09-03 (sunum)
- Sonra: 01-05, 01-06 (D9 zamanlama testi — gerçek VM gerektirir)

## Kritik kararlar (PLAN_spherex_v3.md'den)
- S3 primer, cutout fallback (503 riski)
- TAP async zorunlu; demo frame listeleri dondurulmuş
- Mode N = kendi gridinde; R-k sunucu taraflı yeniden örnekleme MCD'de
- HDU indeksleme: IMAGE=1, FLAGS=2, VARIANCE=3, ZODI=4, EPSF=5, WCS-WAVE=6
- Arka plan sabit parent-grid tile'larında (window'a bağımlı değil)
- Hedefler: Barnard, ε Indi B, WISE 0855, RW Aur, R Dra

## Dal/commit kuralı
- Dal: `c/<görev-no>-kısa-ad`
- main'e doğrudan push (küçük değişiklikler OK; büyük kod PR açar)
- Commit mesajı: `feat: <görev-no> <kısa açıklama>`

## Context budget notu
15M token havuzu mevcut. %80'e yaklaşınca (12M kullanım) bu dosyayı güncelle ve `/compact` çalıştır.
