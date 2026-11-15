# Kiralık Makine Kılavuzu

> Görevler 06-07 (koşullar) ve 06-08 (başlatma)
> Son güncelleme: 2026-11-15

## 1. Kiralama Koşulları

### 1.1 CPU VM (temel, her zaman) [V]

Demo günü birkaç saat önce kirala.

| Parametre | Değer |
|---|---|
| Bölge | AWS us-east-1 veya Hetzner Ashburn [V] |
| Minimum CPU | 4 vCPU |
| Minimum RAM | 8 GB |
| Disk | 50 GB SSD (önbellek için ~12 GB + işletim sistemi) |
| Önerilen tür | AWS t3.medium veya eşdeğeri |
| Kiralama süresi | Demo + hazırlık: ~3 saat |

Bölge seçimi için D9 test sonuçları (görev 01-06) esas alınır. D9 testi
us-east-1 üzerinden çalıştırıldıysa aynı bölgeyi kullan.

### 1.2 GPU Tetikleyicisi (isteğe bağlı) [NV]

D9 testi (görev 01-06) `p50 > 2.0 s` döndürürse ve yalnızca o zaman
vast.ai'dan GPU kirala.

| Parametre | Değer |
|---|---|
| Platform | vast.ai |
| Tür | 1× NVIDIA A5000 veya eşdeğeri |
| Kullanım amacı | Yalnızca shift-and-stack görevi (04-14) |
| Maksimum süre | 2 saat |
| Tetikleyici eşiği | p50 > 2.0 s |

GPU kilalama kararı D9 testi bitmeden verilmez.

---

## 2. D9 Testi: Sıra [NV]

D9 testi hangi donanımın yeterli olduğunu ölçer; kiralama kararı bu
sonuca göre verilir.

```bash
# 1. Küçük bir AWS us-east-1 VM kirala (t3.medium, 1 saat)
#    ve SSH ile bağlan
ssh ubuntu@<VM_IP>

# 2. Repoyu kopyala
git clone https://github.com/Bhllcoder1/planet-x-sphere
cd planet-x-sphere

# 3. D9 testini çalıştır (50 kare, Barnard hedefi)
python -m c_sunucu.ops.d9_test --target barnard --n 50

# 4. Çıktıdan p50 ve p95 değerlerini kaydet
```

Karar tablosu:

| p50 sonucu | Karar |
|---|---|
| < 1.0 s | CPU-only yeterli; GPU kiralama yok |
| 1.0 – 2.0 s | CPU-only muhtemelen yeterli; tekrar ölç |
| > 2.0 s | GPU tetikleyici devreye girer (bkz. §1.2) |

---

## 3. Demo VM Başlatma

### 3.1 Ön koşullar

- SSH anahtarı VM'e yüklenmiş olmalı.
- `.env.example` dosyası repoda mevcut: `c_sunucu/.env.example`.
- Docker ve Docker Compose VM'de kurulu olmalı.

### 3.2 Adım adım komutlar [V]

```bash
# 1. VM'e SSH
ssh ubuntu@<VM_IP>

# 2. Repoyu kopyala
git clone https://github.com/Bhllcoder1/planet-x-sphere
cd planet-x-sphere

# 3. .env oluştur ve doldur
cp c_sunucu/.env.example c_sunucu/.env
nano c_sunucu/.env
# Doldurulması gereken alanlar:
#   APP_SECRET_KEY=<rastgele güçlü değer>
#   CADDY_DOMAIN=<IP veya alan adı>

# 4. Docker Compose ile başlat
cd c_sunucu/deploy
docker compose up -d

# 5. Önbelleği doldur (tüm demo hedefleri)
python -m c_sunucu.ops.prefetch \
    --targets barnard eps_indi_b wise0855 rwaur rdra

# 6. Sağlık kontrolü
curl http://localhost:8000/health
```

Beklenen yanıt: `{"status": "ok"}` veya eşdeğeri.

### 3.3 Önbellek boyutu tahmini [ASSUMPTION]

| Hedef | Tahmini boyut |
|---|---|
| Barnard | ~4.2 GB (ölçülmüş, arith) |
| Diğer 4 hedef | ~7.8 GB (toplam tahmin) [ASSUMPTION] |
| Tüm 5 hedef | ~12 GB [ASSUMPTION] |

---

## 4. Demo Sonrası Temizlik

```bash
# Docker'ı durdur
cd planet-x-sphere/c_sunucu/deploy
docker compose down

# AWS üzerinde VM'i terminate et
aws ec2 terminate-instances --instance-ids <i-xxxxxxxxxxxxx>

# vast.ai GPU kiraladıysan: panelden "Destroy" tıkla
# veya CLI ile:
#   vastai destroy instance <INSTANCE_ID>
```

Boşta geçen her saat gereksiz maliyet üretir; demo biter bitmez VM silinir.

---

## 5. Maliyet Tahmini [ASSUMPTION]

| Bileşen | Süre | Birim fiyat | Tahmini toplam |
|---|---|---|---|
| AWS t3.medium (D9 testi) | 1 saat | ~$0.09/saat | ~$0.09 |
| AWS t3.medium (demo) | 2 saat | ~$0.09/saat | ~$0.18 |
| vast.ai A5000 (koşullu) | 2 saat | ~$0.40/saat | ~$0.80 |
| **Toplam (CPU-only)** | 3 saat | — | **~$0.27 [ASSUMPTION]** |
| **Toplam (GPU tetikleyici)** | 5 saat | — | **~$1.07 [ASSUMPTION]** |

> Not: Tüm fiyatlar tahminidir [ASSUMPTION]. Gerçek fiyatlar için
> [AWS fiyatlandırma](https://aws.amazon.com/ec2/pricing/) ve
> [vast.ai](https://vast.ai/) sayfalarını kontrol edin.

---

## 6. Şimdi Kiralama

**Kiralama zamanı değil.** Kod hazır olmadan VM kiralamak boşa para harcar.

Kiralama için tüm aşağıdaki görevler tamamlanmış olmalı:

- [ ] Görev 01-06: D9 testi geçiyor
- [ ] Görevler 06-01 – 06-09: Sunucu kodu tamamlandı
- [ ] `c_sunucu/.env.example` dolduruldu ve test edildi
- [ ] `docker compose up` yerel ortamda başarılı

---

## Referanslar

| Görev | Konu |
|---|---|
| 01-05 / 01-06 | D9 testi tanımı ve çalıştırma |
| 04-14 | Shift-and-stack (GPU gerektiren adım) |
| 06-01 – 06-09 | Sunucu kurulum görevleri |
