# Brief: make every ClickUp task self-explanatory (NASA challenge style)

Goal: someone who does NOT know astronomy and was not in our discussions must be able to open ONE task and know what to do, why, with which data, with which sources, and when it is done. The NASA/IRSA texts we read explain things as: Background -> Objectives -> Potential considerations -> Resources. Mirror that.

## What you do
For every task in your assigned files clickup\tasks_<LL>.json:
1. First copy the original file to tasks_<LL>.orig.json (only if the .orig file does not exist yet).
2. Rewrite each task's "description" (keep id, name, priority, tags, est_hours unchanged unless a tag/estimate is clearly wrong; you may add the tag "model-..." never; do not change the model tag) so it has these sections in this order (markdown, Turkish, plain language):
   - **ARKA PLAN (sade dille):** 3-6 sentences for a newcomer. Define every jargon term used by the task the first time (WCS, SIP, ePSF, flag/bit, pass/geçiş, MJD, centroid, proper motion, forced photometry, CORS, TAP, S3 range read, Gaia, SkyBoT ...) in one clause each. Say what the problem is in SPHEREx terms. Only state facts that appear in our source pages / notes / test reports; otherwise mark [NV].
   - **AMAÇ:** (the original NE + NEDEN, tightened) plus one line saying which NASA challenge objective or "Potential consideration" the task serves, when one applies (the challenge text is summarized in plan/SITE_SPEC.md: blink series of an RA/Dec patch; easy updates with new releases; per-detector stacking; add/subtract images; selectable FOV; Gaia/WISE overlays; URL query params; metadata and contamination flags; Astropy/Aladin).
   - **NASIL (adım adım):** the original steps, kept concrete, with parameters, formulas and file names; add the first thing to open ("Nereden başlarım") if it is not obvious.
   - **GİRDİ / ÇIKTI**, **KABUL**, **KANIT**, **ÖNCE**, **MODEL** as in the original (keep the numbers; improve wording only).
   - **DİKKAT EDİLECEKLER (olası tuzaklar):** 2-4 bullets, each tied to a source: known pitfalls from our test reports (stage0/s0_A..D.md, e.g. 0/1-based pixels, SIP inverse tolerance, the QR1/QR2 ePSF x/y order bug, saturated NaN cores, TAP latency, 503s from the cutout service, OUTLIER set on real movers) or from the notes. Write the file after each bullet, for example "(stage0/s0_B.md)".
   - **KAYNAKLAR:** 1-4 items, each "URL - what to read there (section name or what you will find)". Use ONLY URLs from clickup\SOURCE_MAP.md. Open the local file listed next to the URL and check that the page really contains what you say (grep it). Also give the local copy path so nobody has to browse the web. If no verified source exists for a task, write "Doğrulanmış kaynak yok [NV]" instead of inventing one.
3. Keep every [V]/[NV]/[ASSUMPTION] tag and never turn an assumption into a fact. Do not add new requirements and do not add drizzle or AI upscaling work (both are off).
4. Length: descriptions may now be 1,500-4,500 characters. Quality over length: no filler.
5. Write the JSON with Python (json.dump(..., ensure_ascii=False, indent=1)) using stage0\venv\Scripts\python.exe -I -X utf8 (put your helper script in clickup\_gen\, never inline). Reload and print: task count (must equal the original), every task still has id/name/priority/tags/est_hours/description, and the list of ids whose KAYNAKLAR contain a URL that is not in SOURCE_MAP.md (must be empty). Do not call ClickUp.
6. Final reply <=100 words: counts and anything uncertain.
