# Çevrimdışı Yedekleme Planı

Etiketler: **[V]** doğrulanmış, **[NV]** doğrulanmamış, **[ASSUMPTION]** varsayım.

## 1. Amaç ve senaryo

Demo sırasında IRSA TAP veya S3 erişilemezse sistem **L0 (kare listesi) ve L2 (pencere .npz) önbelleğinden** çalışmaya devam eder. Bunun için demo öncesi önbellek `c_sunucu/ops/prefetch.py` ile doldurulur.

Dayanak:
- TAP, 6 hedeften 3'ünde başarısız oldu (HTTP 502, zaman aşımı) [V: s0_A, s0_B].
- Barnard TAP sorgusu ~202 s sürdü; 5 dk sınırına yakın [V: s0_A].
- S3 anonim erişim çalışıyor [V: s0_B]; demo ağında kesinti olasılığı [ASSUMPTION].

## 2. Önbellek katmanları ve düşüş sırası

| Katman | İçerik | Dizin | Çevrimdışı rolü |
|---|---|---|---|
| L0 | Hedef başına kare listesi | `L0_CACHE_DIR/{target}/frames.json` | TAP yerine geçer |
| L1 | HDU byte-offset haritası | `L1_CACHE_DIR/{frame_id}.json` | Pencere indirme ön koşulu |
| L2 | Pencere verisi (.npz) | `L2_CACHE_DIR/{frame_id}/{x0}_{y0}_{w}_{h}.npz` | S3 yerine geçer |

Düşüş: canlı TAP/S3 -> TAP hatasında L0 -> S3 hatasında L2. L2'de olmayan pencere çevrimdışıyken sunulamaz (kullanıcıya "önbellekte yok" denmeli) [ASSUMPTION].

## 3. Önceden çekme sırası

Sıra sabittir; zaman biterse en önemli hedefler hazır olur:

1. **barnard** (269.4521, 4.6933) - ana demo hedefi
2. eps_indi_b (330.84, -56.79)
3. wise0855 (133.79, -7.24)
4. rwaur (75.495, 30.40)
5. rdra (274.06, 68.13)

```bash
# Önce yalnızca Barnard
python -m c_sunucu.ops.prefetch --targets barnard
# Tümü (Barnard önce)
python -m c_sunucu.ops.prefetch --all --max-frames 200
```

Notlar:
- TAP başarısız olursa betik mevcut L0'dan devam eder; ilk kez çalışırken L0 yoksa hedef atlanır.
- Pencere indirmek için L1 offset haritası gerekir; yoksa kare atlanır ve uyarı loglanır. L1'i önceden üretmek gerekir [NV: L1 üretim betiği ayrıca doğrulanmadı].
- Varsayılan pencere görüntü merkezidir (970,970,100,100). Hedefin gerçek piksel konumu WCS ile hesaplanmalıdır; `--window x0,y0,w,h` ile verilir [ASSUMPTION].
- Betik idempotenttir: L2'de olan pencere yeniden indirilmez; kesilirse tekrar çalıştırmak yeterlidir.
- TAP için 15 dk poll sınırı ve 30/60/120 sn backoff vardır [V: tap_client.py]; Barnard için ~4 dk beklenmeli.

## 4. Depolama tahmini

| Kapsam | Tahmin | Etiket |
|---|---|---|
| Barnard | ~4,2 GB | [ASSUMPTION] |
| 5 hedef toplamı | ~12 GB | [ASSUMPTION] |
| Önerilen boş alan (yedeklerle birlikte, x3) | >= 40 GB | [ASSUMPTION] |

Referans: 100x100 pencere ~0,8 MB/HDU ham veri [V: s0_B]; .npz sıkıştırılmış olduğundan gerçek boyut daha küçük olabilir [NV]. İlk Barnard çalışmasından sonra `du -sh` ile gerçek boyut ölçülüp bu tablo güncellenmeli.

## 5. Yedekleme (rsync / USB)

```bash
# Ana makineden USB'ye (silme yok, ilerleme göster)
rsync -avh --progress "$L0_CACHE_DIR/" /mnt/usb/spherex/l0/
rsync -avh --progress "$L1_CACHE_DIR/" /mnt/usb/spherex/l1/
rsync -avh --progress "$L2_CACHE_DIR/" /mnt/usb/spherex/l2/

# Yedek makineye (ağ)
rsync -avh --partial -e ssh "$L2_CACHE_DIR/" yedek:/data/spherex/l2/

# Doğrulama (sadece fark raporu)
rsync -avhn --checksum "$L2_CACHE_DIR/" /mnt/usb/spherex/l2/
```

- Windows'ta rsync yoksa WSL veya `robocopy <kaynak> <hedef> /MIR /R:2 /W:2` kullanılır [ASSUMPTION].
- En az **iki bağımsız kopya**: ana disk + USB, ayrıca ikinci USB veya yedek dizüstü [ASSUMPTION].
- Geçmiş/kullanıcı verisi için `python -m c_sunucu.ops.db_backup backup --out spherex_backup.tar.gz` [V: db_backup.py].
- Geri yükleme: aynı rsync komutları ters yönde; ardından `L0/L1/L2_CACHE_DIR` ortam değişkenleri geri yüklenen dizine yönlendirilir.

## 6. Demo günü kontrol listesi

T-1 gün:
- [ ] `prefetch --all` tamamlandı; her hedefin `frames.json` dosyası var
- [ ] L2'de her hedef için en az bir pencere var; thumbnail'lar açılıyor
- [ ] Yedek kopya (USB) rsync `--checksum` farksız
- [ ] Yedek USB ve kablolar çantada

T-2 saat:
- [ ] Sunucu önbellek dizinleri ortam değişkenleriyle doğru yere bakıyor
- [ ] Barnard akışı baştan sona denendi (canlı)
- [ ] **Ağ kapalı/uçak modu ile Barnard akışı denendi** (L0+L2'den geliyor mu?)
- [ ] TAP/S3 erişimi test edildi; hatalıysa önbellek moduna geçmeye karar verildi
- [ ] Disk doluluğu < %80, şarj/güç kablosu bağlı
- [ ] Hesap/seed verisi (`users_seed.json`) yerinde

Demo sırasında:
- [ ] TAP/S3 hatasında panik yok: önbellek hedeflerine (Barnard önce) geç
- [ ] Önbellekte olmayan hedef istenmesin; anlatı L2'de olan hedefler üzerinden yürüsün
- [ ] Sonuçlar "aday" olarak sunulur, "tespit" denmez (ePSF doğrulaması bitmeden) [V: COMPETITION_RULES]

## 7. Açık riskler

- L1 offset haritalarının ön üretimi için doğrulanmış bir betik yok [NV].
- Boyut tahminleri ölçülmedi [ASSUMPTION].
- TapFrame'de `mjd_avg` şu an `lastmodified` değeridir, `sps_epa` 0.0'dır; L0'a bu haliyle yazılır [V: tap_client.py].
