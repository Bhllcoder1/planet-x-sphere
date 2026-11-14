# planet-x-sphere

NASA SPHEREx taramasının görüntülerinden, verilen bir gökyüzü bölgesinin zaman içindeki değişimini **piksel hassasiyetiyle** gösteren ve hareketli cisimleri öne çıkaran bir web aracı (NASA Space Apps yarışması). Kapsam: yarışmanın 5 test hedefi (Barnard'ın Yıldızı, ε Indi B, WISE 0855, RW Aur, R Dra).

## Nereden başlamalı
1. `docs/plan/DECISIONS_AND_TASK.md`: kararlar ve güncel görev durumu.
2. `docs/plan/PLAN_spherex_v3.md`: son plan (v2'nin farkı ve ince dilim sırası).
3. `docs/plan/TEAM_SPLIT.md`: dört alanın görev listeleri ve alanlar arası teslimatlar.
4. Kendi alanının klasöründeki `README.md`.
5. ClickUp'ta kendi `kişi-x` etiketli görevlerin.

## Yapı
```
planet-x-sphere/
├── README.md
├── CONTRIBUTING.md
├── .github/            CODEOWNERS ve PR şablonu
├── a_veri_isleme/      alan A: veri entegrasyonu, görüntü işleme, veri analizi
├── b_astrometri/       alan B: astrometri ve hareketli cisim bilimi
├── c_sunucu/           alan C: sunucu, hesaplar
├── d_site/             alan D: site ve arayüz
├── contracts/          alanlar arası sözleşmeler (manifest, API, URL şeması)
├── ops/                kiralama, dağıtım, yedek (alan C)
├── tests/              test verisi ve regresyon betiği
├── tools/              ClickUp betikleri, kazıma aracı, Stage 0 betikleri
└── docs/
    ├── plan/           plan v1-v3, kararlar, site şartnamesi, gösterim katmanı, ekip bölüşümü
    ├── research/       araştırma notları ([V]/[NV] etiketli)
    ├── stage0/         gerçek veri testlerinin raporları (A, B, C, D)
    ├── sources/        okunan sayfaların kopyaları ve kaynak haritası
    └── tasks/          199 görevin kaynak dosyaları ve yazım yönergeleri
```

## Durum
Planlama ve Stage 0 testleri bitti; ürün kodu yazılmaya başlanmadı. Birçok sayı (süre tahmini, bazı eşikler) [ASSUMPTION] etiketlidir. Önemli bilinmeyenler: yarışma son tarihi, WISE 0855 / RW Aur / R Dra kapsamı.

Veri: NASA/IPAC IRSA (SPHEREx), ESA Gaia, IMCCE SkyBoT. WiseView kodunun ilgili dosyaları (kamu malı lisansı) yalnızca referans olarak `docs/sources/wiseview/` içinde.

## Yol notu
Belgelerdeki `sources\...`, `sources_xxx\...`, `research\...`, `research2\...` ve `stage0\...` yolları eski çalışma klasöründen kalmadır. Bu depodaki karşılıkları: `sources\` -> `docs/sources/genel/`, `sources_viewer`, `sources_astrometry`, `sources_moving`, `sources_server`, `sources_wiseview` -> `docs/sources/viewer` vb., `research` ve `research2` -> `docs/research/`, `stage0\s0_*.md` -> `docs/stage0/`.
