# Shift-and-Stack Benchmark ve GPU Kılavuzu

> Görev 04-14 — CPU Referans Benchmark ve vast.ai GPU Entegrasyonu  
> Son güncelleme: 2026-11-15

---

## Genel Bakış

SPHEREx Level-2 görüntülerinde Barnard ve diğer yüksek özdevinimli (high proper motion) hedeflerin tespitinde SNR artırımı için **shift-and-stack** (ötele ve yığ) algoritması kullanılır:
- **SNR kazanımı:** $\text{SNR}_{\text{stack}} \approx \sqrt{N} \times \text{SNR}_{\text{single}}$
- 358 kare için teorik SNR kazanımı $\approx \sqrt{358} \approx 18.9\times$.

Bu işlem varsayılan olarak **CPU NumPy** ile gerçekleştirilir. Eğer p50 gecikme süresi **> 2.0 s** olursa veya çoklu grid araması gerekiyorsa **vast.ai kiralık GPU (CuPy)** yoluna geçilir.

---

## 1. B.5 GPU Tetikleyici Kuralı

| Metrik | Eşik | Karar |
|---|---|---|
| p50 işlem süresi | $\le 2.0\text{ s}$ | **CPU yeterli** — GPU kiralanmaz |
| p50 işlem süresi | $> 2.0\text{ s}$ | **GPU tetiklenir** — vast.ai A4000/A5000 kiralanır |
| Tek kare SNR | $> 5.0$ | **Doğrudan tespit** — yığma zorunlu değil |

---

## 2. CPU Benchmark'ı Çalıştırma

CPU referans uygulamasını test etmek ve p50/p95 sürelerini ölçmek için:

```bash
# 50 kare, 10 tekrarlı test
python -m c_sunucu.ops.shift_stack_demo --frames 50 --runs 10

# Özel boyut veya SNR tahminiyle
python -m c_sunucu.ops.shift_stack_demo --frames 100 --runs 5 --snr 1.2
```

Program çıktısı JSON formatında rapor ve GPU tetikleyicisinin durumunu (exit code 2 = GPU gerek, exit code 0 = CPU yeterli) döner.

---

## 3. GPU (CuPy) Yolu

Eğer GPU tetikleyicisi aktifse:
1. `ops/VASTAI_RUNBOOK.md` adımlarını takip ederek vast.ai üzerinden GPU kiralayın (NVIDIA RTX A4000/A5000, 16GB VRAM, ~$0.40/saat).
2. Makineye bağlanın ve CuPy ortamını kurun:
   ```bash
   pip install cupy-cuda12x
   ```
3. `c_sunucu/ops/gpu_stack.py` betiğini çalıştırın:
   ```bash
   python c_sunucu/ops/gpu_stack.py --frames 358 --shifts shifts.json --out stacked.fits
   ```

---

## 4. Sorun Giderme ve Performans İpuçları

- **Bellek yetersizliği (OOM):** Çok sayıda tam boyutlu kare için bellek yetmezse, kareler 64x64 tespit pencerelerine (sub-crop) bölünerek yığılmalıdır.
- **CPU performansı:** NumPy median yerine float32 NaN-omitted mean kullanılması CPU süresini %40-60 azaltır.
