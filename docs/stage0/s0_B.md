# Stage 0 test B: S3 byte-range windows vs cutout service, parent-pixel rule (real data)

Run date 2026-11-14. Scripts: `stage0/scripts/b1_tap.py ... b9_analyze.py`. Raw outputs: `stage0/data/B/` (`probe.json`, `lat_ra1m.json`, `cut_lat.json`, `cut_retry.json`, `parent.out`, `analysis.out`, `cut/*.fits`).
Tags: [VERIFIED by this run: script] / [NOT VERIFIED]. Python: the stage0 venv only, `-I`, TLS verification on, 1 IRSA request in flight at a time, 14 cutout downloads in total (limit 25).

## 0. Where this machine is (read this before any number)
- Home PC in Ankara, Turkey, residential ISP (Turkcell), found with an ipinfo.io lookup. It is **not** AWS and **not** us-east-1 (the bucket `nasa-irsa-spherex` is in us-east-1). Every latency below includes a transatlantic path and a consumer link. They are an upper bound for "far-away client", not a prediction for an EC2 box in us-east-1. [VERIFIED by this run: curl to ipinfo.io]
- Per sequential S3 GET round trip was about 0.22 s (22.3 s for 100 GETs of 400 bytes, `cache=none`; includes s3fs overhead). [VERIFIED by this run: b2_s3probe.py]
- Throughput was very erratic: 1 MiB GETs took 0.3 to 5.9 s each; one file open took 60 s, another 2 s. [VERIFIED by this run: b5_s3lat.py] I did not run a bandwidth test, so I cannot separate RTT from throughput. Whether an in-region VM would pass D8 is [NOT VERIFIED] (that is D9).

## 1. Frame selection
- Barnard's Star position used for the TAP query: J2000 (269.45207, +4.69335) propagated with PM (-797.8, +10362.5 mas/yr) to the observation epoch, ~(269.4464, +4.7672). Query: `spherex.artifact JOIN spherex.plane ... 1=CONTAINS(POINT('ICRS',269.446,4.766), p.poly)`. TAP sync returned 357 rows (239 under `dr1/level2`, the rest `qr3`) after **202 s**. [VERIFIED by this run: b1_tap.py]
- `spherex.artifact` has NO `cloud_access` column. Columns returned: planeid, artifactid, uri, producttype, releasetype, contenttype, contentlength, contentchecksum, ipac_gid, mission_id, ipac_pub_date, lastmodified. The S3 key is the `uri` with the prefix `ibe/data/spherex/` removed, i.e. `s3://nasa-irsa-spherex/dr1/level2/<week>/<ver>/<det>/level2_....fits`; this opened anonymously. [VERIFIED by this run: b1_tap.py, b2_s3probe.py]
- Files are about 61-65 MB each (TAP `contentlength`), not "several hundred MB". [VERIFIED by this run: b1_tap.py; the notes' "several hundred MB" is wrong for these L2 frames]
- 5 frames used: `cands.json` indices 4,0,2,3,1 (detectors D2, D6, D3, D6, D3; weeks 2025W33-W34). Main frame: `dr1/level2/2025W34_2B/l2b-v27-2026-229/2/level2_2025W34_2B_0557_2D2_spx_l2b-v27-2026-229.fits`, detector 2, MJD 60911.49, 61,093,440 bytes. [VERIFIED by this run: b4_pick.py (it timed out after 5 frames, so only 5 candidates were scanned)]
- HDU layout of that file: PRIMARY, IMAGE (ImageHDU), FLAGS (CompImageHDU), VARIANCE, ZODI, EPSF (BinTable), WCS-WAVE. NOTE the order is IMAGE, FLAGS, VARIANCE, ZODI. All four image HDUs are 2040x2040; raw size 16,646,400 bytes each. [VERIFIED by this run: b2_s3probe.py]
- Barnard's Star is in this frame at parent pixel (1156.7, 1743.3) (0-based), within 0.25 px of the proper-motion prediction (1156.5, 1743.4). Peak 1122.8 MJy/sr, and the 2x2 core is NaN in IMAGE and VARIANCE (saturated or masked). [VERIFIED by this run: b8_explore.py, b7_parent.py]

## 2. Task 1: bytes on the wire per 100x100 window (one frame, one window at x0=900,y0=900)
Window = 100x100 = 40,000 bytes per HDU (float32/int32). Headers = `open` + header scans. GETs were counted by wrapping `s3fs.core.S3File._fetch_range`. [VERIFIED by this run: b2_s3probe.py]

| s3fs cache | open (GETs / bytes) | header scan for `hdul["IMAGE"]` | IMAGE window | VARIANCE | ZODI | FLAGS window |
|---|---|---|---|---|---|---|
| readahead, 5 MiB blocks (s3fs default type) | 1 / 5,242,886 | 4 / **19,610,880** | 1 / 5,243,280 | 1 / 5,243,280 | 1 / 5,243,280 | 1 / 5,259,200 |
| none | 3 / 2,966 | 26 / 74,880 | **100 / 40,000** | 100 / 40,000 | 100 / 40,000 | 101 / **359,325** |
| bytes, 64 KiB blocks | 1 / 65,542 | 5 / 279,424 | 22 / 1,441,936 | 22 / 1,441,936 | 22 / 1,441,936 | 11 / 738,399 |

Findings:
- With `cache_type=none` the transfer is exactly the window (100 row-segments of 400 bytes, 40,000 B) for IMAGE/VARIANCE/ZODI. Each row of the window is a separate GET because rows are 8,160 bytes apart. Astropy `.section` therefore does a true partial read, but one GET per image row. [VERIFIED by this run: b2_s3probe.py]
- Looking an HDU up **by name** (`hdul["IMAGE"]`) scanned the file: 19.6 MB with the default readahead cache. Using the integer index (`hdul[1]`) avoids that. [VERIFIED by this run: b2_s3probe.py for the 19.6 MB; b5_s3lat.py used indices and made 4 GETs/4.2 MB for the open with 1 MiB readahead]
- **Compressed FLAGS `.section` works without downloading the whole HDU.** It returned a 100x100 int32 array, exactly equal to the cutout service's FLAGS (section 4). With `cache=none` it cost 101 GETs and 359,325 bytes (about 9x the 40,000-byte raw window; tiles are most likely whole rows, [NOT VERIFIED] directly: I read no ZTILE keywords because astropy had already translated the header). Whole HDU raw = 16.6 MB; whole file = 61.1 MB. [VERIFIED by this run: b2_s3probe.py]
- With 1 MiB readahead (the config used for timing) each HDU window was exactly 1 GET of 1,048,976 bytes (26x the window); FLAGS averaged 1.1 GETs and 1,160,217 bytes, max 2,118,555. A frame-window (4 HDUs) averaged 4,307,145 bytes, about 7% of the file. [VERIFIED by this run: b5_s3lat.py, b9_analyze.py]
- A 100-row window spans 99 x 8160 + 400 = 808,000 contiguous-ish bytes, so one ~0.8 MB GET would be the best single-GET design (about 20x the window). Not run as its own config. [NOT VERIFIED]

## 3. Task 2: latency
S3 (5 files x 6 windows, 4 HDUs each, 100x100, 1 MiB readahead, headers by index; the first window of file 0 was centred on the star, others random). Sequential reads. [VERIFIED by this run: b5_s3lat.py + b9_analyze.py]
- Per frame-window (IMAGE+FLAGS+VARIANCE+ZODI, 4 GETs): n=30, **p50 3.90 s, p95 12.73 s**, min 1.56, max 17.56, mean 5.34.
- Per HDU window (1 GET): IMAGE p50 0.88 / p95 3.02 s; VARIANCE 0.81 / 3.17; ZODI 0.98 / 3.87; FLAGS 0.73 / 4.17.
- File open + header reads (4 GETs, 4.2 MB, 5 files): 35.8, 60.1, 5.1, 2.1, 3.8 s; p50 5.1 s. A cold frame therefore costs open + window.
- No read failed (30/30 returned 100x100 arrays for all 4 HDUs).
- `cache=none` single window (probe): about 22-23 s per HDU window (100 sequential GETs). [VERIFIED by this run: b2_s3probe.py]

Cutout service (size=0.05 deg -> 29x29 px, gzip=false, 1 request in flight, 5 files x 2 centres, TLS verified). [VERIFIED by this run: b6_cutouts.py, b6b_retry.py]
- 14 requests were sent in total; **9 returned HTTP 200, 5 returned HTTP 503 "Server busy, retry later."** (frame 0 centre A: 503 twice, then 200 after a 45 s wait; frame 3 centre A: 503 three times, never fetched; I stopped retrying). So 9 of the intended 10 cutouts succeeded.
- Latency of the 9 successful requests: **p50 12.4 s, p95 15.9 s** (min 9.8, max 16.1). Body size 3.96-4.05 MB per cutout, constant, regardless of centre. 503s answered in 0.3-1.5 s. Note: `cut_retry.json` only holds the second retry round (the first round's 2 results are in this text and in the console output); counts above are the sum.
- Content: full MEF (PRIMARY, IMAGE, FLAGS, VARIANCE, ZODI, EPSF, WCS-WAVE) at 29x29. That the EPSF table is the bulk of the 4 MB is [NOT VERIFIED] (I did not measure per-HDU sizes).

## 4. Task 3: parent-pixel rule (frame 0, detector 2) [VERIFIED by this run: b8_explore.py, b7_parent.py]
- Full frame (S3 header): CRPIX1A = CRPIX2A = 1.0, CRVAL1A = CRVAL2A = 0.0, WCSNAMEA = '0-based active pixel coordinates', CRPIX1/2 = 1020.5. This matches the notes' "full-frame value 1.0".
- Cutout A (centre = star): NAXIS 29x29, CRPIX1A/2A = -1142.0 / -1728.0, CRPIX1/2 = -122.5 / -708.5 -> offset (1 - CRPIX1A, 1 - CRPIX2A) = (1143, 1729).
- Cutout B (centre shifted by +0.012 deg/cos(dec) in RA, +0.008 deg in Dec): CRPIX1A/2A = -1148.0 / -1724.0 -> offset (1149, 1725). The A and B cutouts overlap in a 25x23 pixel area.
- CRPIX1A/2A are present in IMAGE, FLAGS, VARIANCE and ZODI cutout headers (identical values) but NOT in the EPSF and WCS-WAVE table headers.
- S3 window: parent origin (1106, 1693), 100x100.
- Convention: with x_cut 0-based, `x_orig = 1 + x_cut - CRPIX1A` gives the 0-based parent pixel (full frame: x_orig = x_cut). I did not test the 1-based reading.
- **Independent check with the celestial WCS:** cutout SIP WCS -> sky -> full-frame SIP WCS (from the S3 header) vs the rule: max |dx| = 2.6e-8 px, |dy| = 7.1e-8 px (A); 2.7e-8, 7.2e-8 (B). So the rule is correct to float precision for these two cutouts.
- **Pixel arrays agree exactly:** for both cutouts and all four HDUs (IMAGE, VARIANCE, ZODI, FLAGS) the cutout array equals the S3 array at the rule-mapped location (`np.array_equal`, equal NaN positions, max |diff| 0.0). The cutout dtype is big-endian (>f4, >i4), S3 native, values identical. A vs B in their overlap: identical IMAGE.
- **Star centroid in parent pixels (0-based), same star in all three:** integer peak pixel (1157, 1742) in all three. Masked centroids (11x11 stamp around the peak, NaN core masked, fixed background 0.3035 for all three):
  - centroid_2dg: S3 (1156.714058, 1743.273965); A and B equal to S3 to <1e-6 px (printed difference 0.0 in dx and dy).
  - centroid_com: S3 (1157.042674, 1742.831276); A-S3 dx = 2.3e-13, dy = 0; B-S3 dx = 2.3e-13, dy = 0.
  - Plan test S0.4 requires "same parent pixel within 1e-6": **pass** for this frame (differences <= 2.3e-13 px).
- Caveat 1: a first run with a per-array median background gave COM differences up to 9.7e-3 px between the 100x100 window and the 29x29 cutouts. That was the background estimate, not the coordinates; with a fixed background the difference vanished. Any production code must not subtract a window-dependent background before centroiding if parent-pixel agreement matters.
- Caveat 2: **DAOStarFinder did not detect Barnard's Star** (the saturated core is NaN, which I set to 0; in cutout A DAO found nothing at 5 sigma, fwhm 2). DAO found 38 other sources in the S3 window, so DAO is fine for normal stars. For the saturated star I used masked `centroid_com` and `centroid_2dg`. The comparison is the same pixel data in all three, so it tests the coordinate rule, not centroid accuracy.
- Caveat 3: only one frame and one star; the rule was not tested for cutouts clipped at a frame edge (partial overlap) or for the other five detectors. [NOT VERIFIED]
- Note on the Explanatory Supplement: it states no cutout rule (notes_expsupp). The rule is confirmed here from the cutout-tool documentation plus this run.

## 5. Task 4: D8 verdict ("S3 wins if bytes <= 2x (window + headers) and p50 < 1 s/frame")
Budget used: window = 4 HDUs x 40,000 = 160,000 B; headers = 2,966 + 74,880 = 77,846 B (from the `cache=none` open + header scan). 2 x (160,000 + 77,846) = 475,692 B.

| S3 config | bytes per frame-window | <= 2x(window+headers)? | p50 latency | < 1 s? |
|---|---|---|---|---|
| cache=none | 3 x 40,000 + 359,325 = 479,325 (+77,846 headers = 557,171) | **Marginal fail** (1.17x budget; IMAGE/VARIANCE/ZODI alone are exact, FLAGS tiles cause the excess) | about 90 s (4 x ~22 s, one probe) | **FAIL** |
| readahead 1 MiB | 4,307,145 (+4.2 MB per open) | **FAIL** (9x) | **3.90 s** (p95 12.73 s) | **FAIL** |
| readahead 5 MiB | about 21 MB | FAIL | about 12 s (one probe) | FAIL |

- **D8 does not pass for S3 on this machine in any configuration tested.** Bytes: minimal config only just misses; latency: fails by 4x to 90x because astropy's synchronous per-row GETs meet a ~0.2 s round trip, and larger blocks meet an erratic, slow link.
- Cutout service for comparison: ~4.0 MB per cutout, p50 12.4 s, 5 of 14 requests answered 503. That is worse than S3 readahead on latency and about equal on bytes, and it is not a "win" for the cutout either: D8 has no pass criterion defined for the cutout, so I make no cutout-passes claim.
- Not tested, so the verdict is limited: the plan asks for 50 frames; I did 5 frames / 30 windows [VERIFIED by this run: b5_s3lat.py]. Not run: in-region (us-east-1) timing, parallel GETs (asyncio/`s3fs.cat_ranges` or a custom coalescing cache, which would turn 100 sequential GETs into 1-4 parallel ones), a single exact-span GET, or hybrid caching (tiny blocks for headers, big block for data). Whether any of these meets p50 < 1 s is [NOT VERIFIED]. The most likely fix, in-region compute plus one coalesced GET of ~0.8 MB per HDU, would still miss the strict "2x" bytes test (about 20x) unless the byte criterion is applied per useful row-span rather than per window.
- Plan risk R1 ("S3 byte-range / compressed FLAGS section does not work"): **not triggered** (both work and are exact); the open risk is performance, not correctness.

## 6. Failures and oddities (honest list)
- `b4_pick.py` exceeded the tool timeout after 5 frames (each header-only open took 10-17 s with 5 MiB readahead); the 5 printed candidates were transcribed into `data/B/cands.json` by hand from the console output (values identical to the printed ones).
- First launch of `b5`/`b6` failed (missing cands.json); re-run once. First `b7` run crashed on a photutils 3.x column rename (`x_centroid`), and a second crashed because DAO found nothing in cutout A (NaN core). The final `b7_parent.py` is the one summarised.
- TAP sync latency 202 s for one position query (5 min limit is close).
- Cutout server returned 503 for 5 of 14 requests despite 1 in flight; whether that is a rate limit, a concurrency cap with other users, or a per-file effect is [NOT VERIFIED] (notes say no limits are documented).
