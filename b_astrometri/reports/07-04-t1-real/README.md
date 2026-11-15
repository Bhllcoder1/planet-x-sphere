# 07-04 T1 — real cutout üzerinde sayısal 1 px kayma

Stage 0 B'deki gerçek `100×100` IMAGE/VARIANCE/FLAGS penceresine, aynı OBSID'li `f0_A.fits` ePSF modeliyle yapay parlak yıldız enjekte edildi. WCS başlığındaki `OBSID` ve ePSF kesitinin OBSID değeri `2025W34_2B_0557_2` olarak eşleşiyor. Test aynı gerçek 15×15 yerel piksel damgasını arka plan olarak kullandı; FITS/NPZ verileri depoya kopyalanmadı.

Komut:

```powershell
& C:/Users/behlu/spherex-kb/stage0/venv/Scripts/python.exe tests/test_T1.py `
  --real-window C:/Users/behlu/spherex-kb/stage0/data/B/s3win.npz `
  --epsf-fits C:/Users/behlu/spherex-kb/stage0/data/B/cut/f0_A.fits `
  --frame-header C:/Users/behlu/spherex-kb/stage0/data/B/full_image_header.txt
```

Enjeksiyon ebeveyn pikseli `(1193,1705)`, model genliği `5000`:

| Deney | Ölçülen kayma | Hata | Kabul |
|---|---:|---:|---|
| Aynı gerçek piksel damgasına `(x,y)` ve `(x+1,y)` enjeksiyonu | `Δx=0.998403719`, `Δy=0.000486581` px | `x`: 0.001596281 px; `y`: 0.000486581 px | Geçti (`≤0.005 px`) |
| Enjekte edilmiş 15×15 damgada `np.roll(..., 1, axis=1)` | `Δx=0.9999999996` px | `4.35e-10 px` | Geçti (`≤0.005 px`) |

**Sınır:** ePSF aynı gözlemden alındı ve hem enjeksiyonda hem uyumda kullanıldı; bu, gerçek PSF doğruluğundan bağımsız bir test değildir. Gerçek gürültü/variance/flag pikselleri üzerinde sayısal tam-piksel kaymasını doğrular. T1 ekran/Playwright kabulü ve 07-04 D3 hâlâ açık; [H-11](../../../docs/second-brain/HUMAN_ACTIONS.md) gerekli girdileri listeler.
