# NEOSSat research notes

Load status: data.asc-csa.gc.ca failed via WebFetch (cert error); fetched with curl -k instead (content read OK, TLS not verified). Other 3 pages + GitHub notebooks (raw, read via curl) OK.

## Dataset page (https://data.asc-csa.gc.ca/dataset/neossat)
- Title "NEOSSAT - Astronomy Data", Open Government Licence - Canada, published 2018-10-16, update "As Needed". [VERIFIED from page: https://data.asc-csa.gc.ca/dataset/neossat]
- Resources: CADC Data Archive, Astronomy Data, "NEOSSat FITS Image User's Guide" (PDF). Guide itself NOT read. [VERIFIED listing; guide contents NOT VERIFIED]
- Says altitude ~780 km (mission page says ~800 km). [VERIFIED both]

## Mission page (https://www.asc-csa.gc.ca/eng/satellites/neossat/)
- Launched 2013-02-25; asteroids/comets, satellites/debris (DRDC HEOSS), exoplanets; ~100 min orbit; open astronomy data since 2019. [VERIFIED]

## GitHub NEOSSAT_Tutorial (https://github.com/asc-csa/NEOSSAT_Tutorial)
README: deps astropy, numpy, matplotlib, pandas, Python 3.9+, modified MIT. [VERIFIED] Two notebooks (EN+FR) in code/. [VERIFIED]

Notebook 01 (Extracting Data and Visualization) [VERIFIED from raw notebooks in asc-csa/NEOSSAT_Tutorial/code]:
- CSA FTP: ftp.asc-csa.gc.ca /users/OpenData_DonneesOuvertes/pub/NEOSSAT/ASTRO/{year}/{doy}/, names NEOS_SCI_YYYYDOYHHMMSS.fits.
- CADC via astroquery.cadc.Cadc: get_collections, query_region(coords, radius, collection='NEOSSAT'), filter on time_exposure, get_image_list. Plot with astropy_mpl_style imshow.

Notebook 02 (Pre Processing and Analysis):
- ADQL on CAOM2: caom2.Plane JOIN caom2.Observation, INTERSECTS(INTERVAL(mjd0,mjd1), Plane.time_bounds_samples)=1, collection='NEOSSAT', calibrationLevel='2', quality_flag != 'junk'; Cadc().exec_sync(query).
- Columns/keys: productID suffixes cor/cord/clean = processing level; instrument_keywords 06-ST_ACQUIRE vs 16-FINE_POINT; type object/dark; target_name; time_exposure. Downloads via cadc.get_data_urls + requests.
- Calibration: overscan columns (last 50 cols) -> per-row median subtract (_cor); master dark = median of overscan-corrected darks (_cord). Text notes dark+flat usually needed; no flat code. Points to Jason Rowe's NEOSSat library (jasonfrowe/neossat) for advanced work (not opened).
- Stacking: np.median across frames, NO alignment/registration (fine for fixed pointing; star-tracked frames).
- Streak detection: gaussian_filter sigma=1 -> normalise uint8 -> pylsd LSD, min length 10 px, draw mask, morphology cleanup.
- Moving object: per-pixel median of cube as background, subtract, threshold 3*global std, binary_opening. Text says tracking/centroiding is a next step but no code.
- Viz: percentile 5-95 stretch, imageio GIF blink animation.
- Libs: astropy, astroquery, scipy.ndimage, scikit-image, pylsd, opencv, imageio, tqdm. No photutils, no WCS, no astrometry/reproject in the notebooks (grep of notebook found none). [VERIFIED by search of notebook text]

## CADC (https://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/ and /en/services/)
- TAP service "argus": https://ws.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/argus/ (CAOM TAP). [VERIFIED /en/services/]
- Cutout: caom2ops, IVOA SODA, https://ws.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/caom2ops/ ; pkg tar of a plane's artifacts same base. [VERIFIED]
- Data: https://ws.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/data/ [VERIFIED]
- Home page lists SSOIS (Solar System Object Image Search), DSS, certificate generation (30 days), CANFAR, github.com/opencadc. [VERIFIED home page]
- Cutout parameter syntax (SODA POS/CIRCLE etc.) not on these pages. [NOT VERIFIED]

## Reuse for SPHEREx moving-object viewer (my assessment)
Reusable:
- Pattern: TAP ADQL (INTERSECTS on time/pos) -> access URL -> SODA cutout. IRSA offers TAP and SIA/SODA-like cutouts too [NOT VERIFIED here; check IRSA docs]. CAOM2 is CADC-specific.
- Median-stack background + difference + sigma threshold + morphological opening for transient/moving detection; percentile stretch; GIF/blink animation for UI.
- Overscan/dark/median-stack calibration ideas only as concept; SPHEREx products are already calibrated (not from these pages).
- astroquery as client; astropy FITS/Time.
Not relevant:
- Overscan/dark calibration (SPHEREx L2 already calibrated), LSD streak detection (SPHEREx exposures are a moving object appearing as a point source at different positions per frame, not streaks - assumption NOT VERIFIED), CSA FTP layout, FINE_POINT/ST_ACQUIRE keywords, exoplanet/debris mission context.
Caveats: tutorial lacks WCS/astrometry, alignment, photutils; stacking without alignment would smear moving objects/needs WCS reprojection for SPHEREx. Use astropy.wcs, reproject, photutils, SSOIS-like ephemeris matching (JPL Horizons/ astroquery) - these are my suggestions, NOT VERIFIED from pages.
