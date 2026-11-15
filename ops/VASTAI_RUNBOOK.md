# vast.ai GPU Kiralama Kılavuzu

**Durum:** Koşullu — yalnızca D9 tetikleyicisi devredeyse kullanılır  
**Tahmini maliyet:** ~$0.40/saat × 2 saat = ~$0.80 [ASSUMPTION]  
**Hedef kullanım süresi:** Demo (~2 saat)

---

## 1. Tetikleyici Koşulu

Bu kılavuz yalnızca aşağıdaki koşul gerçekleştiğinde uygulanır:

> **Görev 07-10 sonucu:** `fetch` işlemi p50 gecikme süresi **> 2.0 s**

Gecikme bu eşiğin altındaysa GPU gerekmez; CPU-first yolu yeterlidir.  
Tetikleyici ölçümü `c_sunucu/ops/gpu_stack.py` içindeki `D9_P50_THRESHOLD_S = 2.0`
sabitiyle senkronize edilmiştir.

---

## 2. Hesap Oluşturma ve SSH Anahtarı Ekleme

1. <https://vast.ai> adresine gidin ve üye olun.
2. Sol menüden **Account → SSH Keys** sayfasına gidin.
3. Yerel makinenizde anahtar üretin (zaten varsa atlayın):

   ```bash
   ssh-keygen -t ed25519 -C "vastai-planet-x"
   ```

4. `~/.ssh/id_ed25519.pub` içeriğini kopyalayın ve vast.ai SSH Keys formuna yapıştırın.
5. **vast.ai CLI** kurulumu:

   ```bash
   pip install vastai
   vastai set api-key <VASTAI_API_KEY>
   ```

   API anahtarını **Account → API Key** sayfasından alın.  
   Anahtarı kaynak koda yazmayın; ortam değişkeni olarak saklayın:

   ```bash
   export VASTAI_API_KEY="<anahtarınız>"
   ```

---

## 3. GPU Seçimi

Minimum gereksinim: **1× NVIDIA A5000 veya A4000 (12–16 GB VRAM)**

Kabul edilebilir alternatifler (VRAM ≥ 12 GB):
- RTX 3090 / 4090 (24 GB)
- A5000 (24 GB)
- A4000 (16 GB)

Daha düşük VRAM modelleri (örn. 3080 10 GB) `gpu_stack.py` için yeterli
olabilir; ancak ileriki görevlerde (Görev 04-14) gereksinim artabilir.

---

## 4. Uygun Instance Arama

```bash
# VRAM > 12 GB, saatlik fiyat < $0.60, güvenilirlik > 0.95
vastai search offers \
  'gpu_ram>12 num_gpus=1 reliability>0.95 dph<0.60 inet_down>200' \
  --order dph_total \
  -n 10
```

Parametrelerin anlamı:

| Parametre | Açıklama |
|-----------|----------|
| `gpu_ram>12` | En az 12 GB VRAM |
| `num_gpus=1` | Tek GPU (demo için yeterli) |
| `reliability>0.95` | Makine güvenilirliği > %95 |
| `dph<0.60` | Saatlik fiyat < $0.60 |
| `inet_down>200` | İndirme bant genişliği > 200 Mbps |

Çıktıdan **ID** sütunundaki değeri not alın.

---

## 5. Instance Başlatma

```bash
# <OFFER_ID> yerine yukarıdaki arama sonucundaki ID'yi yazın
vastai create instance <OFFER_ID> \
  --image pytorch/pytorch:2.3.0-cuda12.1-cudnn8-runtime \
  --disk 20 \
  --onstart-cmd "pip install cupy-cuda12x numpy"
```

Instance durumunu kontrol edin:

```bash
vastai show instances
```

`Status: running` olana kadar bekleyin (genellikle 1–3 dakika).

---

## 6. SSH Bağlantısı

```bash
# <SSH_HOST> ve <SSH_PORT> değerlerini 'vastai show instances' çıktısından alın
ssh -p <SSH_PORT> root@<SSH_HOST>
```

Bağlantı bilgilerini tek komutla alın:

```bash
vastai show instances --raw | python3 -c "
import sys, json
for inst in json.load(sys.stdin):
    if inst.get('actual_status') == 'running':
        print(f\"ssh -p {inst['ssh_port']} root@{inst['ssh_host']}\")
"
```

---

## 7. Önbellek Aktarımı (rsync)

GPU makinesine yerel önbellek ve proje dosyalarını aktarın:

```bash
# Önbellek dizini (varsayılan: ~/.cache/planet-x veya proje içi cache/)
REMOTE="root@<SSH_HOST> -p <SSH_PORT>"

rsync -avz --progress \
  --exclude '__pycache__' \
  --exclude '*.pyc' \
  ./cache/ \
  -e "ssh -p <SSH_PORT>" \
  root@<SSH_HOST>:/root/planet-x/cache/

# Proje kaynak kodunu da aktar
rsync -avz --progress \
  --exclude '.git' \
  --exclude '__pycache__' \
  ./ \
  -e "ssh -p <SSH_PORT>" \
  root@<SSH_HOST>:/root/planet-x/
```

---

## 8. gpu_stack.py Çalıştırma

GPU makinesinde:

```bash
cd /root/planet-x

# Bağımlılıkları yükle (henüz yapılmadıysa)
pip install cupy-cuda12x numpy

# GPU modunda çalıştır
python -m c_sunucu.ops.gpu_stack \
  --target barnard \
  --frames 50 \
  --gpu

# Çıktı dosyasını kontrol et
ls -lh outputs/
```

Yerel makinede sonuçları geri alın:

```bash
rsync -avz \
  -e "ssh -p <SSH_PORT>" \
  root@<SSH_HOST>:/root/planet-x/outputs/ \
  ./outputs/gpu_run/
```

---

## 9. Demo Sonrası Instance'ı Sonlandırma

**Önemli:** Instance çalışmaya devam ettiği sürece faturalandırılırsınız.
Demo bittikten hemen sonra sonlandırın.

```bash
# Çalışan instance ID'sini listele
vastai show instances

# Instance'ı durdur ve sil
vastai destroy instance <INSTANCE_ID>

# Silme işlemini doğrula
vastai show instances
```

---

## 10. Maliyet Özeti

| Kalem | Değer |
|-------|-------|
| GPU modeli hedefi | A5000 / A4000 (12–16 GB VRAM) |
| Tahmini saatlik fiyat | ~$0.40/saat [ASSUMPTION] |
| Demo süresi | ~2 saat |
| Toplam tahmini maliyet | **~$0.80** [ASSUMPTION] |

> [ASSUMPTION] Fiyatlar vast.ai piyasasına göre değişir. Kiralama öncesinde
> `vastai search offers` ile güncel fiyatı doğrulayın.

---

## 11. Sorun Giderme

| Sorun | Çözüm |
|-------|-------|
| SSH bağlanamıyor | `vastai show instances` ile port/host bilgisini teyit edin |
| CuPy yüklenmiyor | CUDA sürümünü kontrol edin: `nvidia-smi`; uygun `cupy-cudaXXX` paketini seçin |
| Instance başlamıyor | Farklı bir offer seçin; `reliability` filtresini artırın |
| Yüksek gecikme | `inet_down>500` filtresi ekleyin |
| Maliyet beklenenden yüksek | Instance'ın gereksiz yere çalışmadığını `vastai show instances` ile kontrol edin |

---

*Bu kılavuz Görev 06-12 kapsamında oluşturulmuştur.*  
*İlgili betik:* `c_sunucu/ops/gpu_stack.py` *(Görev 06-13)*
