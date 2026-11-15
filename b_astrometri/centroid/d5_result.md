# 03-02 (D5) — ePSF Normalizasyon ve Yönelim Kontrolü (`d5_result.md`)

## Özet Durum

- `[V]` **Self-recovery:** 100 phase pairs (x,y = 0.0..0.9 by 0.1) for norm=1 and norm=25 pass `<0.001 px` in the synthetic fixture. The same-image amplitude scaling test remains consistent with the 25x normalization difference.
- `[V]` **Template self-consistency on real EPSFs:** 600 noiseless recovery fits across detectors 2/3/6, two normalizations, and 100 phase pairs; maximum position errors are 0.000226, 0.000135, and 0.000514 px respectively. Evidence: `C:/Users/behlu/reports/d5-real-templates-100phase.json`. This uses real templates, not real stars.
- `[NV]` **200 real stars (`02-07`) and real orientation/physical-flux calibration:** H-04 sample is still missing; zero real stars were tested. Synthetic orientation evidence does not determine physical constants. Keep `PSF_NORM=1` / non-transposed orientation as assumptions; 03-02 remains open.
- `[NV]` **Dosya içi vs kalibrasyon ePSF bayt-bayt karşılaştırması:** Liste `01` sonucu gelene kadar L1b paylaşımı yapılmaz.
