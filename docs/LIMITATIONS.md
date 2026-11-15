# Sınırlılıklar ve Doğrulanmamış Noktalar (09-06 Taslak)

Bu sayfa, `b/01-03-gaia-fetch` dalındaki mevcut yerel prototiplerin **neyi doğruladığını** ve **neyin henüz doğrulanmadığını (`[NV]` / `[ASSUMPTION]`)** dürüstçe özetler.

## Doğrulanmamış (`[NV]`) Alanlar

1. **Üretim L1/L2 ve WCS Entegrasyonu (`H-01` / `02-03`, `02-12`, `03-03`, `03-09`):**
   - `02-03` koordinat/piksel sözleşmesi ve `02-12` L1 önbellek çıktıları Akif'ten bekleniyor.
   - Bu nedenle `epsf.py`, `wing_fit.py`, `joint_fit.py`, `forced_phot.py` ve `ellipse.py` henüz gerçek üretim kataloğu (`cat.json`) ve `03-09` WCS düzeltmesiyle uçtan uca bağlanmadı.
2. **200 Gerçek Yıldızda ePSF Yönelim ve Mutlak Akı (`03-02`):**
   - `×1` / `×25` kendi-kurtarma (`< 0.001 px`) ve sentetik yönelim `χ²_ν` ayrımı doğrulandı; ancak `02-07` izole yıldız seçimi gelmediği için `PSF_NORM = 1.0` ve `PSF_TRANSPOSE = False` gerçek veride doğrulanmadı (`[ASSUMPTION]`).
3. **Barnard Doygun Çekirdek Taraması (`03-05`) ve Ekran Testi (`07-04`):**
   - `T1` sayısal (`Δ = 1.000 ± 0.005 px`) ve `T4` SIP-3 WCS gidiş-dönüş (`< 1e-4 px`) testleri geçti; `z = 1, 4, 16, 64` Playwright ekran testi `d_site` arayüzünü bekliyor.
4. **Kapsam Bilinmezlikleri (`WISE 0855`, `RW Aur`, `R Dra`):**
   - Bu üç hedef için IRSA TAP sorguları zaman aşımı / 502 döndüğünden kare sayısı **"0"** değil **"bilinmiyor"** durumundadır (`passes.py` ve `lightcurves.py` ikisini ayrı raporlar).
5. **Hareketli Cisim Hız Sınırı (`04-06`) ve Kalabalık-Alan Eşikleri (`04-08`):**
   - `10.6 px/saat` (`65"/h`) üst sınırı ana kuşak asteroitleri içindir; hızlı NEO'lar denenmedi (`[ASSUMPTION]`).
   - Kalabalık-alan eşikleri (`SOURCE > %50`, `gürültü > 5× seyrek medyan`) yalnızca `s0_D` (`gc1..gc5`, `sp1..sp6`) sayılarına göre ayarlandı (`[ASSUMPTION]`).
6. **ClickUp Durumu:**
   - Tüm görevler yerel prototip/denetim aşamasında; ClickUp'ta henüz kapatılmadı.
