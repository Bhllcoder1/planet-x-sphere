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

## Tamamlanan görevler (2026-11-15)
- 00-10, 00-11, 00-12: docs/RISKS.md ✓
- 00-13: docs/QUESTIONS.md ✓
- 05-04: c_sunucu/api/raster.py ✓
- 05-10: docs/URL_SCHEMA.md ✓
- 05-18: c_sunucu/api/wiseview_compat.py ✓
- 06-01: FastAPI skeleton (api/main.py + routes/) ✓
- 06-02: cache/ (l0/l1/l2 + byte_offset_map) ✓
- 06-03: api/tap_client.py ✓
- 06-04: api/s3_reader.py ✓
- 06-05: api/politeness.py ✓
- 06-06: api/timing.py ✓
- 06-07/08: ops/RENTAL_RUNBOOK.md ✓
- 06-09: deploy/ (Dockerfile, docker-compose, Caddyfile) ✓
- 06-10: .env.example + ops/SECRET_MANAGEMENT.md ✓
- 06-12/13: ops/VASTAI_RUNBOOK.md + c_sunucu/ops/gpu_stack.py ✓
- 06-14: contracts/api.yaml + api/mock_server.py ✓
- 07-01: tests/ (conftest.py, fixtures/) ✓
- 07-11: tests/test_stack.py ✓
- 07-12: tests/test_regression.py + tests/run_regression.py ✓
- 09-03: docs/SLIDES_DRAFT.md ✓
- 09-04: docs/STATUS.md ✓
- 09-05: docs/COMPETITION_RULES.md ✓
- 09-09: docs/CREDITS.md ✓
- 09-10: docs/SUBMISSION_CHECKLIST.md ✓
- 10-03/04: c_sunucu/api/coord_parser.py ✓
- 11-04: c_sunucu/accounts/user_repo.py + __init__.py ✓
- 11-05: c_sunucu/accounts/session.py + api/routes/auth.py ✓
- 11-06: c_sunucu/accounts/history.py + api/routes/history.py ✓
- 11-07/08: c_sunucu/api/routes/profile.py ✓

## Üçüncü dalgada tamamlananlar
- 01-05: c_sunucu/ops/d9_test.py ✓
- 07-10: c_sunucu/ops/speed_test.py ✓
- 10-15: c_sunucu/api/routes/share.py ✓
- 11-10: c_sunucu/ops/db_backup.py ✓
- 11-11: c_sunucu/api/routes/export.py ✓
- 11-13: c_sunucu/api/routes/fits_export.py ✓
- Tüm yeni router'lar api/main.py'de kayıtlı ✓

## Dördüncü dalgada tamamlananlar (2026-11-15)
- 06-11: ops/OFFLINE_BACKUP_PLAN.md + c_sunucu/ops/prefetch.py ✓ (commit 1bd4192)
- 02-10: c_sunucu/cache/frame_products.py + tests/test_frame_products.py (img/var/flg/cat/geom atomik ve little-endian ürünler) ✓
- 02-11: contracts/manifest.schema.json + contracts/manifest_example.json + tests/test_manifest_schema.py (Draft 2020-12 v2 manifest sözleşmesi) ✓
- 02-20: c_sunucu/api/image_renderer.py + tests/test_image_renderer.py (tam sayı NN zoom, asinh germe, ızgara/işaretçi, Okabe-Ito NaN, thumb_64) ✓
- 04-09: c_sunucu/api/skybot.py + tests/test_skybot.py (-objFilter=100, max(3 px, 3σ) eşleme yarıçapı, çevrimdışı 'untagged' koruması) ✓
- 11-09: d_site/pages/profile.html + c_sunucu/api/routes/profile.py (/profile/view) (360 px uyumlu responsive profil/geçmiş UI) ✓
- a_veri_isleme/process/masks.py ve stretch.py: _flatten ve numpy dizi desteği düzeltildi, tüm modüller uyumlu hale getirildi ✓
- Alan A (Akif) GitHub durumu teyit edildi: ClickUp'ta 53 görev "to do" beklerken, GitHub `main` dalına commit `449567a` ile tüm temel modüller yüklenmiş; 8 testinin tümü geçiyor ✓
- ClickUp güncellendi: Alan C'nin 47 görevi "complete" işaretlendi (Kalan: 01-06 VM testi, 04-14 vast.ai tetikleyicisi, 05-14 sonra listesi) ✓
- Regresyon / Test paketi: 40/40 birim testi başarıyla geçti ✓

## Sıradaki (kalanlar / opsiyonel)
- 01-06: D9'u gerçek kiralık VM'de koşmak (fiziksel VM veya bulut örneği gerekir)
- 04-14, 05-14 ("sonra" listesi): GPU shift-and-stack (vast.ai), Aladin Lite paneli (MCD dışı / opsiyonel)

## GitHub push durumu
- Branch: c/00-10-to-11-05-alan-c-ilk-toplu
- Son commitler Alan C branch'ine push edilecek
- PR: tüm görevler tamamlandığında main'e açılacak

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
