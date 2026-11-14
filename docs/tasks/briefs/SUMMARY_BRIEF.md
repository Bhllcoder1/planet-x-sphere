# Brief: add a plain-language SUMMARY block at the top of every ClickUp task

Problem (user feedback): "I read the task and did not understand what it is." The descriptions start with technical sections (ARKA PLAN, AMAÇ, NASIL...). Add a short block at the very top that a first-year student who does not know astronomy could follow.

## What to do
For every task in your assigned files clickup\tasks_<LL>.json:
1. First copy the file to tasks_<LL>.pre_summary.json (only if it does not exist yet).
2. Read the whole task (name, tags, est_hours, description). Then PREPEND this block (Turkish) to "description", followed by a line with `---` and a blank line, and leave the rest of the description exactly as it is:

**ÖZET (sade dille)**
- **Ne yapıyoruz:** one sentence, at most 25 words, everyday words. Say what is produced or checked.
- **Neden:** one sentence: what goes wrong or what we cannot do without it.
- **Sana ne düşüyor:** 2-4 very short concrete steps (open / write / run / check), in order, in the imperative ("Gaia'dan çevredeki yıldızları sorgula").
- **Bitti sayılır:** one sentence with the measurable finish line (take it from KABUL; keep the numbers).
- **Alan ve süre:** the area letter from the tags (kişi-a..kişi-d: A veri ve görüntü işleme, B astrometri ve hareketli cisim, C sunucu ve hesaplar, D site ve arayüz), est_hours in hours, and 'demo' or 'sonra' if tagged.

## Fidelity rules (added after user feedback: the summary must not drift from the task's purpose or be misread)
- The first bullet ("Ne yapıyoruz") must restate the task's own purpose: take it from the AMAÇ section (and the task name), keep its key nouns and numbers. Do not generalise it, do not add goals the task does not have, do not change scope.
- Add a sixth bullet **Kapsam dışı:** one short sentence saying what this task does NOT include or what it must not be confused with (take neighbours from ÖNCE, from other task ids named in the text, or from the task's own DİKKAT section). Example: "Bu görev konum ölçmez; ölçüm 03-03'tedir." If nothing can be confused, write "Kapsam dışı: yok (görev tek başına anlaşılır)."
- Every statement in the block must be traceable to the task text. If you cannot support a statement from the task, leave it out.
- Self-check pass (mandatory): after writing all blocks, print for each task the pair (AMAÇ sentence | your 'Ne yapıyoruz' line | your 'Bitti sayılır' line) and compare them yourself. Fix every block where the meaning differs, where a number differs from KABUL, or where a reader could take the task to mean something else. Report how many blocks you had to fix.

## Style rules
- Everyday Turkish. Every technical word that must stay is explained in a few words in brackets on first use inside the block, e.g. "WCS (görüntüdeki pikselin gökyüzündeki yerini söyleyen harita)", "TAP (arşive soru sorma servisi)", "ePSF (yıldızın görüntüdeki beklenen biçimi)", "flag/bayrak (kötü pikselleri işaretleyen etiket)", "pass/geçiş (aynı gökyüzü bölgesinin bir taramada görülmesi)".
- Do not invent facts. Use only what the task already says. Keep [NV]/[ASSUMPTION] marks where they matter ("henüz doğrulanmadı").
- Do not change id, name, priority, tags, est_hours, or any text below the new block. Do not add requirements. Drizzle and AI upscaling stay off.
- If the block already exists (marker "**ÖZET (sade dille)**"), skip that task (idempotent).
- Example for task 03-07:
**ÖZET (sade dille)**
- **Ne yapıyoruz:** Gaia kataloğundaki yıldızların bilinen yerlerini alıp, her fotoğrafın çekildiği tarihe kadar nereye kaydıklarını hesaplıyoruz.
- **Neden:** Yıldızlar yavaşça yer değiştirir; hesaplamazsak kendi ölçümümüzü kataloğa bakarak kontrol edemeyiz.
- **Sana ne düşüyor:** 1) Gaia'dan çevredeki yıldızları sorgula. 2) Her karenin tarihine taşı (hazır astropy işlevi). 3) İki birim test yaz.
- **Bitti sayılır:** Barnard için hesaplanan yer, astropy'nin sonucuyla 1e-9 derece içinde uyuşuyor.
- **Alan ve süre:** B, yaklaşık 5 saat, demo.
---

## Output and checks
Write the JSON with Python (json.dump, ensure_ascii=False, indent=1) using stage0\venv\Scripts\python.exe -I -X utf8 (helper scripts into clickup\_gen\). Then reload and print: task count (must equal the original), how many tasks now start with the marker, any task whose block is longer than 120 words (shorten it), and any task where id/name/priority/tags/est_hours changed (must be none). Do not call ClickUp. Final reply <=80 words.
