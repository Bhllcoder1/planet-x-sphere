# planet-x-sphere

NASA SPHEREx taramasının görüntülerinden, verilen bir gökyüzü bölgesinin zaman içindeki değişimini **piksel hassasiyetiyle** gösteren ve hareketli cisimleri öne çıkaran bir web aracı (NASA Space Apps). Kapsam: yarışmanın 5 test hedefi (Barnard'ın Yıldızı, ε Indi B, WISE 0855, RW Aur, R Dra).

## Nereden başlamalı
1. `docs/plan/DECISIONS_AND_TASK.md`: kararlar ve güncel durum.
2. `docs/plan/PLAN_spherex_v3.md`: son plan.
3. Kendi alanının klasöründeki `README.md` (görev listesi ve alt klasörler).
4. ClickUp'ta (Planet XSphere çalışma alanı) sana atanmış görevler. Her görevin en üstünde sade bir özet var.

## Yapı
```
planet-x-sphere/
├── README.md, CONTRIBUTING.md, .gitignore
├── .github/          CODEOWNERS ve PR şablonu
├── a_veri_isleme/    Akif    : fetch, process, products, display, exports
├── b_astrometri/     Behlül  : centroid, gaia, wcs, motion, movers, reports
├── c_sunucu/         Osman   : api, cache, accounts, deploy
├── d_site/           Furkan  : viewer, pages, design
├── contracts/        alanlar arası sözleşmeler (manifest, API, URL şeması)
├── ops/              kiralama, dağıtım, yedek (Osman)
├── tests/            test verisi ve regresyon betiği
└── docs/
    ├── plan/         planlar, kararlar, site şartnamesi, ekip bölüşümü
    ├── research/     araştırma notları ([V]/[NV] etiketli)
    ├── stage0/       gerçek veri testlerinin raporları
    └── TEAM.md       ekip ve alanlar
```

## Durum
Planlama ve Stage 0 testleri bitti; ürün kodu henüz yok, alt klasörler boş. Süre tahminleri ve bazı eşikler [ASSUMPTION] etiketlidir. Bilinmeyenler: yarışma son tarihi, WISE 0855 / RW Aur / R Dra kapsamı.

Kaynak sayfa kopyaları, görev dosyaları ve Stage 0 betikleri depoda değil; proje sahibinin yerel yedeğinde. Belgelerdeki `sources\` ve `stage0\` yolları o yedeğe işaret eder.

Veri: NASA/IPAC IRSA (SPHEREx), ESA Gaia, IMCCE SkyBoT.