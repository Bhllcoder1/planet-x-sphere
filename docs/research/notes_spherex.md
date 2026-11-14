# SPHEREx programmatic access notes (researched 2026-11-14)

Page load status: ALL fetched OK: Missions/spherex.html, tutorials spherex-intro, spherex-cutouts, spherex-psf, irsa cutout_tool.html, ibe/cutouts.html, spherex-archive-documentation (data-products, data-access), overview_dr1.html, docs/program_interface/TAP.html.
NOT fetched (not read): euclid-clusters-tutorial, Explanatory Supplement PDF (Table 16 flags), overview_qr.html, cloud_access page, spherex-mosaic / spherex-hipscube tutorials.
Note: WebFetch summaries are produced by a small model; treat details as probably-right, re-check critical ones. Items marked [LIVE TEST] were run by me with curl on 2026-11-14.

## 1. Data products
- Spectral Image MEF (L2, per exposure per detector), 0.75-5.0 um. [VERIFIED: https://caltech-ipac.github.io/spherex-archive-documentation/spherex-data-products]
- DR1 = reprocessed QR2 spectral images, to be used with QR3 as uniform set, + All-Sky Cube. QR3 and DR1 supersede QR2. [VERIFIED: https://irsa.ipac.caltech.edu/data/SPHEREx/docs/overview_dr1.html ; spherex-intro]
- All-Sky Cube (DR1 only): 512x512x102 tiles, 12.9"/pix, HDUs IMAGE, NHITS, FLAGS, SPECTRAL_CHANNELS, WCS-WAVE; ZODI subtracted; 102 channels; collection spherex_dr1_cube. [VERIFIED: spherex-data-products; spherex-data-access]
- Mosaic Tool + Mosaic Cubes + HiPS Cubes tutorials exist (spherex-mosaic/, spherex-hipscube/) but I did NOT read them. [VERIFIED existence: https://irsa.ipac.caltech.edu/Missions/spherex.html]
- Release timeline on mission page: QR Jul 2025; QR2 Oct 2025; QR3 Sep 2026; DR1 Nov 2026. [VERIFIED: Missions/spherex.html]
- Surveys: Wide and Deep (collections *_deep). [VERIFIED: spherex-intro]

### MEF HDUs (DR1/QR3 L2) [VERIFIED: spherex-intro + spherex-data-products]
0 PRIMARY (no data) | 1 IMAGE 2040x2040 float32, MJy/sr, NO zodi subtraction | 2 FLAGS 2040x2040 int32 (compressed) bitmap | 3 VARIANCE float32 (MJy/sr)^2 | 4 ZODI float32 MJy/sr modeled, not subtracted | 5 EPSF BinTable 441 rows (21x21 zones, ~97x97 px each, 33x33 ePSF, oversample 5) (detector 3 has 11x41 zones; QR2 has "PSF" cube of 121 101x101 instead) | 6 WCS-WAVE BinTable 1 row, cols X,Y,VALUES.
- Pixel scale 6.15"/pix; array 2040x2040; PSF 0.615"/pix. [VERIFIED: spherex-data-products]
- 6 detectors, bands: 1: 0.75-1.09 (R39); 2: 1.10-1.62 (R41); 3: 1.63-2.41 (R41); 4: 2.42-3.82 (R35); 5: 3.83-4.41 (R112); 6: 4.42-5.00 (R128). Two FPAs x three 2Kx2K arrays behind LVFs. [VERIFIED: spherex-data-products, spherex-intro]
- Detector number in header = DETECTOR keyword; TAP bandpass name 'SPHEREx-D1'..'SPHEREx-D6' (D2 and D6 seen in examples). [VERIFIED for D2: spherex-cutouts; D6: LIVE TEST]
- 102 bands = the 102 spectral channels of All-Sky Cube (6 detectors x 17). The "6x17" split is [NOT VERIFIED from page].
- Wavelength varies across each detector (LVF); one image does not = one wavelength. Each image covers a range (e.g. det 1 example ~0.744-1.126 um across array in the notebook printout). [VERIFIED: spherex-intro]

## 2. Access endpoints
### TAP [VERIFIED: https://irsa.ipac.caltech.edu/docs/program_interface/TAP.html]
- Base https://irsa.ipac.caltech.edu/TAP ; sync .../TAP/sync ; async .../TAP/async. Sync timeout 5 min; async 3 days. TOP N or MAXREC; formats VOTABLE (default), CSV, TSV, IPAC_TABLE, HTML, FITS. One geometric constraint per query. No auth described.
- Tables: spherex.artifact (a), spherex.plane (p), join on planeid; columns a.uri, p.time_bounds_lower/upper, p.energy_bandpassname, p.provenance_version, p.poly (footprint). [VERIFIED: spherex-cutouts, spherex-psf]
- Query (verified in tutorial):
  SELECT a.uri, p.energy_bandpassname, p.time_bounds_lower, p.time_bounds_upper, p.provenance_version FROM spherex.artifact a JOIN spherex.plane p ON a.planeid = p.planeid WHERE 1 = CONTAINS(POINT('ICRS', RA, DEC), p.poly) ORDER BY p.time_bounds_lower
- [LIVE TEST] GET https://irsa.ipac.caltech.edu/TAP/sync?QUERY=<adql>&FORMAT=csv returned 200 text/csv: uri = ibe/data/spherex/dr1/level2/2025W19_2B/l2b-v27-2026-198/6/level2_2025W19_2B_0101_3D6_spx_l2b-v27-2026-198.fits, SPHEREx-D6, 60804.15 (MJD). Prefix with https://irsa.ipac.caltech.edu/ . A trivial query took ~28 s total in the first call (queue spinoff 17 s), second was fast-ish; expect latency.
- Tutorial notes the metadata includes DR1 and QR3 (QR2 superseded). Whether TAP also still returns QR2 rows: [NOT VERIFIED].
### SIA2 [VERIFIED: spherex-data-access]
- https://irsa.ipac.caltech.edu/SIA?COLLECTION=spherex_qr3&POS=circle+127.69444+-39.17760+0.01&RESPONSEFORMAT=HTML (default VOTable; [LIVE TEST] returns application/x-votable+xml). POS is circle RA Dec radius in deg. Collections: spherex_dr1, spherex_dr1_deep, spherex_dr1_cube, spherex_qr3, spherex_qr3_deep (QR2 not searchable; downloadable until Feb 2027). Columns include access_url, cloud_access, s_region, em_min, em_max, s_pixel_scale, t_exptime (51 cols). SIA lags ~1 day behind TAP/Data Explorer.
### Cutout service [VERIFIED: https://irsa.ipac.caltech.edu/ibe/cutouts.html and cutout_tool.html]
- Append query string to the file URL: ...fits?center=RA,Dec[deg|d|px...]&size=X[,Y][unit]. Default unit deg. units: px/pix/pixels, rad, deg, arcsec, arcmin. gzip param: default cutouts are GZIPPED; gzip=false for plain. 
- Errors: malformed -> HTTP 400; no overlap with parent -> 500; partial overlap -> clipped. No explicit max size stated. Output is full MEF (all HDUs incl. EPSF, WCS-WAVE, unmodified PSF/EPSF). Cutout header has CRPIX1A/CRPIX2A: xpix_orig = 1 + xpix_cutout - CRPIX1A (0-based coordinates).
- [LIVE TEST] https://irsa.ipac.caltech.edu/ibe/data/spherex/dr1/level2/2025W19_2B/l2b-v27-2026-198/6/level2_2025W19_2B_0101_3D6_spx_l2b-v27-2026-198.fits?center=210.8,54.35&size=0.02&gzip=false -> 200, application/fits, content-disposition: attachment, 3.95 MB (for a ~0.02 deg = ~12 px cutout; size dominated by EPSF/other tables, probably). Raw size breakdown: [NOT VERIFIED].
- Whole file MEFs are "several hundred MB". [VERIFIED: cutout_tool.html]
### Other
- Browsable dirs https://irsa.ipac.caltech.edu/ibe/data/spherex/{dr1,qr3,qr2}; cloud (AWS S3) via https://irsa.ipac.caltech.edu/cloud_access/#spherex (bucket details NOT read).
- Tools: Data Explorer /applications/spherex; Spectrophotometry, Mosaic, Source Discovery tools; MOST for moving objects. astroquery.ipac.irsa Irsa.query_tap / query_sia; pyvo. [VERIFIED: Missions/spherex.html]

### Auth / CORS / rate limits
- Auth: none needed for public data; anonymous cookie set; no auth in tutorials. [VERIFIED by tutorials + LIVE TEST]
- CORS: [LIVE TEST] requests with Origin: https://example.com to TAP/sync, SIA and the cutout URL returned NO Access-Control-Allow-Origin header; OPTIONS preflight to TAP/sync returned 200 text/xml with no CORS headers visible (I only saw first 10 lines of headers; grep for ACAO not done explicitly on full headers, so treat as "likely no CORS"). => Plan on a server-side proxy (e.g. Cloudflare Worker/serverless). Official docs do not mention CORS. [NOT VERIFIED from docs]
- Rate limits: none documented. Cutouts tutorial uses ThreadPoolExecutor(max_workers=10), notes the number depends on what IRSA server can handle; handle TimeoutError, HTTPError, IncompleteRead, RemoteDisconnected with retries (3 retries, sleep 10*(n+1) s). [VERIFIED: spherex-cutouts, spherex-intro]
- Reading files can exceed default timeouts; tutorials set remote_timeout=120 s.

## 3. WCS & flags
- Celestial WCS in IMAGE header: RA---TAN-SIP / DEC--TAN-SIP, CRPIX 1020.5, PC matrix, CDELT 1 (example). SIP coefficients present in header. [VERIFIED: spherex-intro] astropy WCS(header) works.
- Alternate key A = "0-based active pixel coordinates". Alternate key W = per-pixel wavelength+bandwidth via lookup table (WCS-WAVE: 9x9 control points at 1,256,511,766,1021,1275,1530,1785,2040; VALUES 2x9x9; bilinear interp, ~1 nm accuracy; for visualization; use CWAVE/CBAND (EPSF cols) for science). Use WCS(header=hdul["IMAGE"].header, fobj=hdul, key="W"), set .sip=None; pixel_to_world -> (wavelength um, bandwidth um). [VERIFIED: spherex-intro, spherex-data-products]
- Flag bits (header MSKNnnnn/MSKDnnnn; definitions in Expl. Suppl. Table 16 - not read) [VERIFIED listing: spherex-intro]: 0 TRANSIENT, 1 OVERFLOW, 2 SUR_ERROR, 6 NONFUNC, 7 DICHROIC, 9 MISSING_DATA, 10 HOT, 11 COLD, 12 FULLSAMPLE, 14 PHANMISS, 15 NONLINEAR, 17 PERSIST, 19 OUTLIER, 20 CROSSTALK, 21 SOURCE, 22 GHOST, 23 GHOST_FPA, 24 GHOST_EXT, 25 STREAK, 26 BLOOM, 27 SNOWBALL, 28 HALO. Most pixels are typically flagged SOURCE (bit 21), so do NOT mask SOURCE for display. Which bits are "bad" for science: [NOT VERIFIED]; header keys L2 N_*_NB / _NS count variants.
- Pixel scale derived from PC matrix ~6.1-6.2"/pix; doc states 6.15". 

## 4. Cadence / coverage
- IRSA releases Quick Release spectral images weekly; SIA lags ~1 day; counts at a position change weekly. [VERIFIED: overview_dr1.html, spherex-intro]
- Planned lifetime 2025-2027; 100% sky planned. A given position is seen many times (443 SIA rows for 1" radius at time of notebook; 84 D2 images for M101). [VERIFIED: pages]
- Whole-sky coverage fraction / images count: NOT stated.
- Cutout size limits: not documented. Rate limits: not documented.
- QR2 PSF header error fixed Apr 10 2026 (QR2 headers). [VERIFIED: Missions/spherex.html]

## Suggested web-tool flow
1. Proxy TAP sync CSV query above (FORMAT=csv) -> list uri, bandpass, MJD.
2. Per row, proxy fetch https://irsa.ipac.caltech.edu/{uri}?center=RA,Dec&size=0.05&gzip=false (or arcmin units), parse FITS in-browser (IMAGE/FLAGS/VARIANCE/ZODI, WCS, WCS-WAVE).
3. Fetch concurrency <=~10, retries.
