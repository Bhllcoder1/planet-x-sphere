# 04-12 — RW Aur ve R Dra kapsam durumu

Stage 0 A, RW Aur ve R Dra için tekrarlanan IRSA TAP denemelerinin 400 s okumada zaman aşımına, HTTP 502'ye veya bağlantı sıfırlanmasına uğradığını; kapsamın **UNKNOWN** kaldığını kaydediyor (`docs/stage0/s0_A.md`, satır 385–389 ve 398–406). Bu, sıfır kare kanıtı değildir. Frame listesi ve 04-03 fotometri girdisi bulunmadığı için ölçüm yapılmadı.

İki hedef için JSON ve SVG durum çıktısı `lightcurves.py` yazıcısıyla üretildi:

- `lightcurves_rw-aur.json` / `.svg`
- `lightcurves_r-dra.json` / `.svg`

Çıktılarda `coverage_status=unknown`, `photometry_status=not_run`, boş λ kutuları ve sorgunun tamamlanmama nedeni yer alır. SVG panelleri açıkça “Coverage: UNKNOWN” ve “not a zero-flux measurement” der; sıfır akı noktası çizmez.

**04-12 kabulü tamamlanmadı:** kontrol yıldızı kararlılığı, R Dra'nın σ cinsinden değişimi, gerçek λ kutuları ve doygunluk değerlendirmesi için [H-12](../../../docs/second-brain/HUMAN_ACTIONS.md) girdileri gerekir. Şu anki JSON/SVG yalnız doğru bilinmeyen durumunu kaydeder.
