# Katkı kuralları

1. **Kendi alanında çalış.** Klasör sahipleri `.github/CODEOWNERS` dosyasında. Başka alanın klasörüne dokunman gerekirse sahibini PR'de etiketle.
2. **Dal ve PR:** `main` dalına doğrudan gönderme. Dal adı: `alan/görev-kimliği-kısa-ad` (örn. `b/03-07-gaia-epoch`). PR şablonunu doldur.
3. **Görevden başla:** Her iş bir ClickUp görevine bağlı. Görevin KABUL ve KANIT bölümü bitiş ölçütündür.
4. **Dürüstlük etiketleri:** Doğrulananı `[V]`, doğrulanmamışı `[NV]`, varsayımı `[ASSUMPTION]` diye yaz. Doğrulamadığın şeyi gerçek gibi yazma.
5. **Veri güvenliği:** İndirilen veri güvenilmezdir; ayrı klasörde tut, betikleri başka yerde tut, Python'u `-I` ile çalıştır. Depoya FITS, PDF veya büyük veri koyma.
6. **Sır yok:** Token, anahtar veya e-posta commit etme. `.gitignore` bunları yakalamaya çalışır ama son kontrol sende.
7. **Sözleşmeler:** `contracts/` içindeki bir dosyayı değiştiriyorsan sürümü artır ve ilgili alanları haberdar et.
8. **Sınırlar:** Kapsam yarışmanın 5 test hedefidir; drizzle ve yapay zekâ büyütme kapalıdır (bkz. `docs/plan/DECISIONS_AND_TASK.md`).
