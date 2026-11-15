# D9 VM Zamanlama Testi Runbook

> Görev 01-06 — AWS us-east-1 bölge-içi S3 gecikme ölçümü  
> Son güncelleme: 2026-11-15

---

## Genel Bakış

D9 testi, AWS us-east-1 bölgesinde çalışan küçük bir VM'den NASA-IRSA
SPHEREx L2 S3 kovasına bölge-içi S3 getirme sürelerini ölçer.  
Sonuç p50 ve p95 istatistiklerini döndürür; `p50 > 2.0 s` ise vast.ai GPU
tetikleyicisi etkinleşir.

---

## 1. Ön Koşullar

| Gereklilik | Değer |
|---|---|
| AWS bölge | us-east-1 |
| EC2 örnek türü | t3.medium (2 vCPU, 4 GB RAM) — yeterli; t3.large isteğe bağlı |
| İşletim sistemi | Ubuntu 22.04 LTS (ami-0c7217cdde317cfec) veya eşdeğeri |
| Python | ≥ 3.11 |
| Bağımlılıklar | `httpx` (d9_test.py tek bağımlılığı) |
| Ağ | S3 anonim erişim — kimlik bilgisi gerekmez |
| SSH anahtarı | Mevcut EC2 key pair |

---

## 2. EC2 VM Başlatma

```bash
# 2.1 Örneği başlat (AWS CLI)
aws ec2 run-instances \
  --region us-east-1 \
  --image-id ami-0c7217cdde317cfec \
  --instance-type t3.medium \
  --key-name <KEY_PAIR_ADI> \
  --security-group-ids <SG_ID> \
  --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=d9-test-runner}]" \
  --query "Instances[0].InstanceId" \
  --output text
# → i-0abcdef1234567890 (kaydet)

# 2.2 Örnek IP'sini al
aws ec2 describe-instances \
  --region us-east-1 \
  --instance-ids <INSTANCE_ID> \
  --query "Reservations[0].Instances[0].PublicIpAddress" \
  --output text
# → 1.2.3.4

# 2.3 SSH bağlantısı (hazır olana kadar ~60 s bekle)
ssh -i ~/.ssh/<KEY_PAIR_ADI>.pem ubuntu@<VM_IP>
```

---

## 3. VM Kurulumu

```bash
# 3.1 Sistemi güncelle ve Python 3.11 kur
sudo apt-get update -y
sudo apt-get install -y python3.11 python3.11-venv git

# 3.2 Repoyu klonla
git clone https://github.com/Bhllcoder1/planet-x-sphere.git
cd planet-x-sphere

# 3.3 Sanal ortam ve bağımlılıklar
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install httpx
```

---

## 4. D9 Testini Çalıştırma

```bash
# 4.1 Standart çalıştırma (50 kare, Barnard hedefi, seed=42)
python -m c_sunucu.ops.d9_test --target barnard --n 50 --seed 42

# 4.2 Warm-up ile çalıştırma (önce 3 kare ısıtma, sonra ölçüm)
python -m c_sunucu.ops.d9_test --target barnard --n 50 --seed 42 --warm

# 4.3 Sonuçları belirli bir dizine kaydet
python -m c_sunucu.ops.d9_test --target barnard --n 50 --out-dir /tmp/d9out
```

> [!NOTE]
> `--seed 42` tekrarlanabilirlik için standarttır. Farklı tohumlar farklı
> kare sıraları seçer; karşılaştırmalar için sabit seed kullan.

---

## 5. Beklenen Çıktı Formatı

### 5.1 Terminal Çıktısı

```
D9 Zamanlama Testi başlıyor — hedef=barnard n=50 seed=42
Makine: ip-10-0-1-42 | Python 3.11.x | Linux
S3 kova: nasa-irsa-spherex (us-east-1, anonim erişim)

Ölçüm: 50 kare...
  [  1/50] 2025W34_2B_042_I03_map_11.fits          0.312s
  [  2/50] 2025W34_2B_117_I01_map_11.fits          0.287s
  ...
  [ 50/50] 2025W34_2B_088_I05_map_11.fits          0.445s

============================================================
D9 Zamanlama Testi — barnard (n=50)
Makine: ip-10-0-1-42, bölge: AWS us-east-1 (doğrulanmamış)
------------------------------------------------------------
p50: 0.350s  p95: 0.890s
min: 0.210s  max: 1.230s
GPU tetikleyicisi: p50 > 2.0s → HAYIR
------------------------------------------------------------
Hedef p50 < 1.0s: ✓  (0.350s)
Hedef p95 < 3.0s: ✓  (0.890s)
============================================================
Sonuç JSON: d9_result_20261115_082500Z.json
```

**us-east-1 VM'den başarı senaryosu:** p50 < 1.0 s, p95 < 3.0 s, GPU tetikleyicisi HAYIR.  
**Ankara'dan ölçülen değerler (referans):** p50 ≈ 3.9 s, p95 ≈ 12.73 s, GPU tetikleyicisi EVET.

### 5.2 JSON Çıktı Formatı

Betik çalışma dizinine `d9_result_{timestamp}.json` dosyası yazar:

```json
{
  "target": "barnard",
  "n": 50,
  "warm": false,
  "p50": 0.3502,
  "p95": 0.8913,
  "p_min": 0.2103,
  "p_max": 1.2301,
  "gpu_trigger": false,
  "times": [0.312, 0.287, ...],
  "hostname": "ip-10-0-1-42",
  "timestamp": "2026-11-15T08:25:00Z",
  "frames_tested": ["dr1/level2/2025W34_2B_042_I03_map_11.fits", ...],
  "errors": []
}
```

**Alanlar:**

| Alan | Tür | Açıklama |
|---|---|---|
| `target` | str | Test hedefi (`"barnard"`) |
| `n` | int | Başarıyla ölçülen kare sayısı |
| `warm` | bool | Ön ısıtma yapıldıysa `true` |
| `p50` | float | Medyan getirme süresi (s) |
| `p95` | float | 95. yüzdelik getirme süresi (s) |
| `p_min` | float | Minimum getirme süresi (s) |
| `p_max` | float | Maksimum getirme süresi (s) |
| `gpu_trigger` | bool | `p50 > 2.0 s` ise `true` → vast.ai GPU kirala |
| `times` | list[float] | Her kare için ölçüm (s) |
| `hostname` | str | VM hostname'i |
| `timestamp` | str | ISO 8601 UTC zaman damgası |
| `frames_tested` | list[str] | Test edilen S3 key listesi |
| `errors` | list[str] | Başarısız kareler ve hata mesajları |

---

## 6. GPU Tetikleyici Kararı

```
p50 > 2.0 s  →  gpu_trigger: true  →  vast.ai GPU kirala (bkz. VASTAI_RUNBOOK.md)
p50 ≤ 2.0 s  →  gpu_trigger: false →  GPU gerekmez, CPU VM ile devam et
```

> [!IMPORTANT]
> GPU kiralama kararı D9 testi tamamlanmadan verilmez.  
> Ankara'dan çalıştırılan simülasyon (d9_simulate.py) referans değerdir; gerçek karar
> us-east-1 VM çıktısına dayanır.

---

## 7. Sonuç Kaydetme ve Raporlama

```bash
# JSON çıktısını yerel makineye kopyala
scp -i ~/.ssh/<KEY_PAIR_ADI>.pem ubuntu@<VM_IP>:~/planet-x-sphere/d9_result_*.json .

# Sonucu insan-okunabilir şekilde görüntüle
cat d9_result_*.json | python3 -m json.tool
```

Sonuç JSON'unu `ops/` dizinine ekleyerek git'e commit et:

```bash
cp d9_result_*.json ops/
git add ops/d9_result_*.json
git commit -m "ops: D9 test sonucu eklendi (us-east-1)"
```

---

## 8. VM Kapatma

> [!CAUTION]
> Testi tamamladıktan sonra VM'i **hemen** kapat. Çalışır halde bırakmak
> gereksiz maliyet doğurur.

```bash
# 8.1 SSH oturumunu kapat
exit

# 8.2 EC2 örneğini durdur (stop — silinmez, yeniden başlatılabilir)
aws ec2 stop-instances \
  --region us-east-1 \
  --instance-ids <INSTANCE_ID>

# 8.3 Örneği tamamen sil (terminate — geri dönüşü yok)
aws ec2 terminate-instances \
  --region us-east-1 \
  --instance-ids <INSTANCE_ID>
```

Yalnızca test amacıyla kullanıldıysa ve sonuçlar kaydedildiyse `terminate` tercih edilir.

---

## 9. Maliyet Notu

| Kaynak | Tür | Maliyet (tahmini) |
|---|---|---|
| EC2 t3.medium | us-east-1, on-demand | ~$0.0416/saat |
| S3 GET isteği | anonim, 50 kare × 4 HDU = 200 istek | ~$0.0001 |
| S3 veri transferi | bölge-içi, ücretsiz | $0.00 |
| **Toplam (1 saat)** | | **~$0.042** |

> [!TIP]
> Test genellikle 5–10 dakika içinde tamamlanır. `stop` yerine `terminate`
> kullanırsanız EBS depolama maliyeti de sıfırlanır.

---

## 10. Sorun Giderme

| Belirti | Olası Neden | Çözüm |
|---|---|---|
| `httpx.ConnectTimeout` | VM'nin internet erişimi yok | Security group outbound 443 açık mı kontrol et |
| HTTP 403 | S3 kova politikası değişmiş | `nasa-irsa-spherex` kova anonim erişim sağlıyor mu doğrula |
| `RuntimeError: Hiçbir kare ölçülmedi` | Tüm kareler hata döndürdü | `--log-level DEBUG` ile tekrar çalıştır |
| p50 beklenenden yüksek | VM farklı AZ'da | `ec2:DescribeInstances` ile AZ kontrol et; S3 ve VM aynı AZ'da mı? |

---

*Bu runbook `c_sunucu/ops/d9_test.py` v1.0 ile uyumludur.*
