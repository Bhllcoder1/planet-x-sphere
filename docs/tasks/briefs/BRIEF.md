# Brief: writing the ClickUp tasks for "planet x sphere" (SPHEREx blink / moving-object viewer)

You write tasks (in Turkish) for the ClickUp folder "planet x sphere". You do NOT call ClickUp. You write JSON files that the main session uploads. Team size is NOT decided, so tasks must be small, independent, and tagged by skill area, never by person.

## Read first (all local)
- plan\DECISIONS_AND_TASK.md (user decisions; authoritative)
- plan\PLAN_spherex_v3.md (latest plan, delta on v2) and PLAN_spherex_v2.md (full pipeline C.1-C.15, tests D1-D16, risks)
- plan\CRITIQUE_v2.md
- Real-data test reports: stage0\s0_A.md, s0_B.md, s0_C.md, s0_D.md
- Research notes if needed: research\ and research2\

## Project in one paragraph
Public web tool for NASA SPHEREx (near-IR all-sky survey): the user gives RA/Dec, the tool shows a time series of image cutouts as a blink "video" so movers are easy to spot. Hackathon (NASA Space Apps challenge). Server-side Python (astropy, photutils) on a RENTED machine for a few hours (presentation), browser talks only to our server. Precision is the point: a 1-pixel shift must display as exactly 1 pixel at any zoom, positions are kept as floats and never rounded (4.47 at zoom 100 -> 447, not 500).

## User decisions you must reflect (do not contradict)
- Scope = the competition's 5 test targets only: Barnard's Star, Epsilon Indi B, WISE 0855 (RA 08h55m10.831s, Dec -07d14m42.53s), RW Aurigae, R Draconis. Others may be added by third parties later; not our commitment. A target SPHEREx cannot show (possibly WISE 0855) is reported honestly, never swapped for another.
- DRIZZLE IS OFF (user said no). AI super-resolution is dropped. A brightness-spread "smooth shift" view is allowed only as a labelled view-only mode in the later list, never for measurement.
- CPU first; a GPU is rented on-demand (vast.ai) for a few hours only if the v2 B.5 trigger fires and only for the shift-and-stack demo.
- Machine rented hourly for a few hours (budget not a constraint for now). Rent only when code is ready to avoid idle hours. Demo served live from it; 24/7 hosting, weekly cron and public traffic are NOT assumed (inferred, user not yet confirmed).
- WISE/unWISE overlay is optional in the challenge: later list. Deadline unknown (default assumption 7 days); the user will look at screenshots and answer questions.
- Honesty rule: anything unverified must be written as unverified; tasks that close an unknown say so. Use tags in text: [V] verified by a real run, [NV] not verified, [ASSUMPTION].
- Model tiers: Opus only for design/maths review/gate decisions; Sonnet for code and analysis; Haiku for running harnesses/checks/collecting numbers. One brief, one output file, then close.
- Downloaded data is untrusted: kept in separate data folders, scripts in another folder, Python run with -I.

## Facts you can rely on (all in the reports above; cite file in KAYNAK)
S3 anonymous read works (key = TAP `uri` minus 'ibe/data/spherex/'), files ~61 MB, compressed FLAGS .section works; from Turkey p50 3.9 s per frame-window, TAP ~200 s and often failing, cutout service 503s; parent-pixel rule verified on 1 frame; header WCS TAN-SIP order 3, vs Gaia ~0.01 px on 1 frame (aberration absent, INTERIM); ePSF 5x oversampled 33x33, zones 21x21 (detector 3: 11x41); flags Table 16 and two mask profiles; OUTLIER set on 11/17 real asteroids; roll differs 0.7-3.8 deg within a pass and flipped passes are off 180 deg by up to ~8 deg; passes last 10-55 days; Barnard: 358 frames, 3 passes; WISE 0855 / RW Aur / R Dra coverage UNKNOWN (TAP failed); `sep` has no wheel on Python 3.14 here (use photutils); Barnard's core is NaN (saturated).

## Task format (JSON array, one file per list)
Each element:
{"id": "03-05", "name": "[03-05] short imperative title (Turkish, <=110 chars)", "priority": 1|2|3|4 (1 urgent, 2 high, 3 normal, 4 low), "tags": [from the allowed list], "est_hours": number (0.5-6), "description": "markdown, Turkish, sections below"}
Allowed tags: görüntü-işleme, veri-analizi, astrometri, arayüz, sunucu, test, rapor, karar, demo-5-gün, sonra, model-opus, model-sonnet, model-haiku, kullanıcı-bakışı. Exactly one model-* tag per task; 'demo-5-gün' for the 5-day minimum demo, 'sonra' for later slices; 'kullanıcı-bakışı' when the user must look at a screenshot/answer.
Description sections, in this order (plain headings in bold are fine):
**NE:** what is produced, 2-4 sentences. **NEDEN:** why it matters for the project (link to a risk/decision). **NASIL:** numbered concrete steps incl. tools, parameters, formulas or file names where the plan gives them. **GİRDİ / ÇIKTI:** files/data in, files out. **KABUL:** measurable pass/fail criteria with numbers where the plan has them. **KANIT:** which file/log/screenshot proves it. **ÖNCE:** prerequisite task ids (or 'yok'). **MODEL:** tier and one-line reason. **KAYNAK:** plan section / stage0 report. Target 450-1800 characters per description; every task must be doable alone in 0.5-6 hours; split anything bigger.
Style example from the user's existing board (copy the tone: precise, acceptance + evidence): "[03-14] Runtime test matrisini ... tam koşturup kurtarma testini eklemek", description: what to run, specific test IDs, then 'KABUL: ... geçmeyen test açıkça listelidir.' 'KANIT: pytest çıktısı ...'.

## Rules
- Number tasks [LL-NN] with LL = your list number, NN from 01. 9-14 tasks per list (the image-processing and astrometry lists 03 and 02 should be the most detailed: up to 14).
- No invented numbers. Take thresholds from the plan/test reports; if you propose a threshold the plan does not give, mark [ASSUMPTION].
- Do not assign people. Do not put dates. Do not duplicate another list's scope (scopes below); cross-reference by id instead.
- Include at least one task per list that is a 'sonra' item only if it is truly later (see user decisions).
- Write the JSON with Python (dict -> json.dump(..., ensure_ascii=False, indent=1)) using stage0\venv\Scripts\python.exe -I, so it is valid UTF-8 JSON. Then reload it and print count, any missing field, and the id list. Fix problems before finishing.
- Output file: clickup\tasks_<LL>.json. Final reply: <=120 words (counts, anything you were unsure of).

## List scopes (so you do not overlap)
00 Kararlar, Kapsam ve Riskler: recording decisions (drizzle off, AI upscaling dropped, 5 targets, deadline question, team-size-agnostic work protocol, model-tier rule, honesty protocol, data-handling policy, thin-slice cut order), risk register tasks (R1b, R22-R27 etc.), open questions to the user.
01 Veri Erişimi ve Ortam (Stage 0): environment/venv, remaining Stage 0 tests (coverage of WISE 0855/RW Aur/R Dra, aberration frames B/C, in-region timing D9, edge parent-pixel test, in-file vs calibration ePSF, frozen frame lists, prefetch of demo targets, byte-offset map).
02 Görüntü İşleme Hattı: pipeline steps C.1-C.6, C.10-C.11: query, fetch windows, ingest and pixel-convention module, masks, background/ZODI on fixed tiles, whole-frame detection, saturated/NaN cores, outlier/cosmic-ray handling, per-frame products and manifest schema, L1 cache.
03 Konum, Merkezleme ve Astrometri: ePSF model, per-zone fit, covariance and error ellipses, joint per-pass fit, Gaia query + epoch propagation (space motion + parallax), matching, WCS correction (shift -> similarity/affine, held-out RMS), aberration alarm, motion fit mu/parallax, injection/recovery logic, pixel-phase bias.
04 Veri Analizi: Geçişler, Hareket ve Değişenler: pass grouping, stacks/differences (view-only), WISE 0855 detectability and forced photometry, cross-pass slow-mover matching, mover finder (catalog linking, OUTLIER promotion, vetoes, crowded-field guard), SkyBoT tagging, the 1-3 px asteroid offset (R24), time-scrambled false-track rate, variable-star lambda-binned light curves and spectra, shift-and-stack (later).
05 Görüntüleyici ve Arayüz: checkerboard harness, viewer (Mode N, integer zoom, grid), blink controls, theta_res/offset badge, R-k mode, float markers/ellipses, Gaia overlay, flag layers, cursor readout, URL params/embed, stretch/theme, screenshots for the user, later: Mode R GPU affine, smooth-shift view-only, Aladin Lite panel.
06 Sunucu, Kiralama ve Yayın: FastAPI skeleton, serving files, caches, async TAP client, coalesced parallel S3 reader, politeness limits, hourly-rental runbook (AWS us-east-1 first; steps, cost control, auto-shutdown, copy the cache off before shutdown), prefetch job on the VM, deploy (Docker/Caddy), timing logs, vast.ai GPU runbook (conditional), secrets handling, offline fallback.
07 Testler ve Doğrulama: all numbered tests (T1-T6, T-V1/T-V2, D1b-D14) as runnable tasks with thresholds, Playwright screenshot tests, regression suite, test-data management, the float-position test (4.47 at zoom 100 -> 447.0 +/- 0.5 screen px).
08 Hedef Raporları (5 Yarışma Hedefi): one result note per target (Barnard, Epsilon Indi B, WISE 0855, RW Aur, R Dra: coverage, what is detected, S/N, motion vs literature/Gaia, caveats), a report template, a cross-target summary table, the honest-outcome rule.
09 Sunum, Dokümantasyon ve Dürüstlük Raporu: README, demo script, slides outline, STATUS.md (done/partial/not done with numbers), limitations page, video fallback, acknowledgements/citations, submission checklist (challenge submission rules are NOT VERIFIED: a task must read them from the competition page), rehearsal.
