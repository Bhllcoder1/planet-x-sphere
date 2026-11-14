# SPHEREx Explanatory Supplement notes (SSDC-DP-017 v2.1, 2026-11-10)

Source: sources_pdf\SPHEREx_Expsupp.pdf (84 pages, 30 MB, downloaded from irsa.ipac.caltech.edu with normal TLS verification).
Method note: the Read tool could not render the PDF (poppler missing), so text was extracted per page with PyMuPDF. PDF page index equals the printed "Page N of 84". Page numbers below are those.

## 1. FLAGS bit table (Table 16, pp. 33-35) [VERIFIED from PDF pp. 33-35]
FLAGS HDU is 2040x2040 bitmap (p.13). Only these bits are defined in the table; bits 3, 4, 5, 8, 13, 16, 18 are NOT listed [NOT FOUND IN DOCUMENT].

| Bit | Name | Meaning (paraphrased from table) |
|---|---|---|
| 0 | TRANSIENT | Transient (e.g. cosmic ray) detected during SUR; transients in the first ~10 s may not be flagged; also set by bloom spillover from very bright neighbours (onboard, Level 0) |
| 1 | OVERFLOW | Overflow threshold reached during SUR; threshold is ~half of full-well saturation |
| 2 | SUR_ERROR | chksum_error bit; alone = onboard data-handling error; with TRANSIENT/OVERFLOW = early transient (first half of exposure) or early overflow (first ~5 s) |
| 6 | NONFUNC | Static pre-flight (updatable) permanently dead/unusable pixel; "unusable for any purpose" |
| 7 | DICHROIC | "Dark corners" of Bands 3 and 4 where the smile effect gives a bandpass incompatible with its side of the dichroic; low throughput, not usefully calibratable or of value for photometry (p.18: throughput < 50%) |
| 9 | MISSING_DATA | Onboard data lost before ingest |
| 10 | HOT | Per-exposure hot pixel; not usable for science |
| 11 | COLD | Per-exposure unresponsive/low pixel; not usable for science |
| 12 | FULLSAMPLE | Full sample history available (rotating 8x32 region); not usable for science, purely informational |
| 14 | PHANMISS | Cannot be corrected due to missing phantom pixels |
| 15 | NONLINEAR | No reliable nonlinearity correction; "excluded from most scientific analyses" |
| 17 | PERSIST | Persistence above the Level 2 threshold |
| 19 | OUTLIER | From Detect Outlier Pixels module (Sect. 3.2.10) |
| 20 | CROSSTALK | "Ordinary" crosstalk (Sect. 3.2.9) |
| 21 | SOURCE | Pixel mapped to a known source |
| 22 | GHOST | Optical ghost from bright source inside the exposure frame |
| 23 | GHOST_FPA | Ghost from a source on another detector in the FPA; currently unused (subsumed into GHOST_EXT), to be removed in Year 2 |
| 24 | GHOST_EXT | Ghost from a bright source outside the FOV; "currently in development" |
| 25 | STREAK | Streak from an Earth-orbiting object (Sect. 3.2.10) |
| 26 | BLOOM | Source blooming (Sect. 3.2.1) |
| 27 | SNOWBALL | Snowball events (Sect. 3.2.1) |
| 28 | HALO | Halo of a transient; "caution recommended" |
| 29 | SATELLITE_HALO | Halo of a satellite streak; "not recommended for use in science analysis" |

Which bits are bad for photometry [VERIFIED from PDF p.45, "Flag usage"]
- Masked in the photometry fit: SUR_ERROR, NONFUNC, MISSING_DATA, HOT, COLD, NONLINEAR, PERSIST, BLOOM, SNOWBALL, HALO, SATELLITE_HALO.
- Additionally masked for background estimation: OVERFLOW, OUTLIER, SOURCE, TRANSIENT.
- L3 photometry summary bit 32 CONTAINS_BAD_PIXEL is set if any pixel within 2.5 SPHEREx pixels has: TRANSIENT, OVERFLOW, SUR_ERROR, NONFUNC, DICHROIC, MISSING_DATA, HOT, COLD, NONLINEAR, CROSSTALK, GHOST, GHOST_FPA, GHOST_EXT, STREAK, PERSIST, BLOOM, SNOWBALL, HALO, SATELLITE_HALO. It is "only a warning", not necessarily grounds for exclusion.
- Mosaic tool (p.46) sets to NaN: TRANSIENT, SUR_ERROR, NONFUNC, DICHROIC, MISSING_DATA, HOT, COLD, PHANMISS, NONLINEAR, PERSIST, CROSSTALK, GHOST, GHOST_FPA, GHOST_EXT, STREAK, BLOOM, SNOWBALL, HALO, SATELLITE_HALO. Propagated only: OVERFLOW, SOURCE, OUTLIER. The all-sky cube rejection list (p.21) is similar (it omits GHOST*).
- Specific topics:
  - Saturation: OVERFLOW (bit 1). It is NOT in the photometry-masking list; it is in the background-masking list. Overflow-interrupted ramps use a reduced N (pp.28-29) and variance uses the overflow prescription (p.30). Early overflow (OVERFLOW + SUR_ERROR) gives NaN pixels (p.17, Fig. 9 caption).
  - Cosmic ray: TRANSIENT (0), plus HALO (28) and SNOWBALL (27). Onboard transient threshold is about 100 e- (pp.15, 79). Single-pixel hits above ~100 photoelectrons are removed onboard (p.15).
  - Non-linearity: NONLINEAR (15) masks the pixel. Correction is quadratic Q_obs = Q_coll(1 - Q_coll/Q_nl), Q_nl ~1.4e6 e- (Bands 1-3) and 0.8e6 e- (Bands 4-6), correction factor 1.05-1.08 for full-length exposures (p.28). L2 DQA fails if any pixel is corrected by more than 50% (p.42).
  - Ghost: GHOST/GHOST_FPA/GHOST_EXT (22-24) are not in the photometry fit mask, but are in CONTAINS_BAD_PIXEL. Beam-splitter ghost: sources of 100 Jy or more, Bands 3-6 only (p.39).
  - Halo / stray light: HALO and SATELLITE_HALO are masked. The 8 degree ghost and Moon stray light (p.15) have NO flag bit [NOT FOUND IN DOCUMENT as flags].
  - SOURCE (21): masked only for background estimation, NOT excluded in photometry. Masks pixels with at least 20% of pixel area inside a magnitude-dependent circle, for catalog sources with spherex_class <= 7 and brighter than 19 AB (pp.38-39).
- Flags are known to be incomplete in QR2: snowball/bloom/halo masking starts with planning period 2025W51_1A (pipeline 6.5); satellite-streak masking is incomplete; crosstalk was not implemented in QR2 (p.50). Type 3 crosstalk masking is not implemented in R7 (p.39).

## 2. WCS

- Derivation [VERIFIED pp. 35-37, 56-58]. Coarse WCS comes from planned pointing, accurate to 2'-10' plus a rotation of a few degrees (p.23). Fine astrometry then runs astrometry.net (solve-field, 3rd-order SIP, CRPIX=(1020.5,1020.5), sep at 100 sigma, Gaia DR3 + 2MASS index files 4100/5200) for an initial solution accurate to a few arcsec (pp.36-37). scamp is run iteratively with SExtractor against 2,000-10,000 Gaia calibrators. Gaia proper motions propagate positions to the observation epoch (p.36). scamp's TPV distortion is converted to SIP with wcs-sip2pv (p.37). In pipeline R7 an astrometry retry module reuses WCS+SIP from "seed" images, giving a sub-percent failure rate (p.37).
- Stated accuracy [VERIFIED p.58]: "RMS values of <0.3''" vs Gaia/2MASS stars, with no significant degradation toward corners (exposures outside the SAA with fewer than 300,000 transient pixels). Also "sub-arcsecond" (pp.35, 37) and "<1''" as a convergence criterion (p.37). Coarse astrometry is better by "more than a factor of two" for pipeline >= 6.5 (p.56). Maximum distortion in the corners is ~13 px or ~80'' (p.58), and 15 px or ~90'' is stated on p.57.
- Absolute vs relative astrometric accuracy: the document gives one RMS figure vs Gaia and does not separate absolute from relative accuracy [NOT FOUND IN DOCUMENT as separate numbers].
- Quality flag FINAST [VERIFIED pp.37, 57-58]: 0 good; 1 partial (offsets of a couple of pixels in corners); higher = poor, "should not be used". The archive requires FINAST = 0 (p.42).
- Frame [VERIFIED p.74]: header RADESYS = 'ICRS'. Aberration: "aberration" is not mentioned anywhere [NOT FOUND IN DOCUMENT]. Whether coordinates are astrometric or aberration-corrected is not stated. The pipeline uses Gaia positions propagated by proper motion to the observation epoch (p.36); nothing is said about parallax or aberration. Spacecraft position and velocity (geocentric) are in the header (p.74).
- Projection and SIP [VERIFIED pp.75-77]: CTYPE1/2 = 'RA---TAN-SIP' / 'DEC--TAN-SIP', CRPIX1=CRPIX2=1020.5, CDELT=1.0 with a PC matrix in degrees, A_ORDER=B_ORDER=AP_ORDER=BP_ORDER=3 (example header). CRVAL1/2 are the per-band RA/Dec (p.14).
- Alternate WCS 'A' [VERIFIED p.77]: WCSNAMEA = '0-based active pixel coordinates', CTYPE1A/2A='LINEAR', CRPIX1A=CRPIX2A=1.0, CRVAL1A=CRVAL2A=0.0, CDELT1A=CDELT2A=1.0 pixel, in the full-image example header. IMAGE is 2040x2040 active pixels (NAXIS1/2 = 2040).
- Cutout vs parent, `x_orig = 1 + x_cut - CRPIX1A`: [NOT FOUND IN DOCUMENT]. The words "cutout" and "cut-out" appear only for stellar photometry/ePSF cutouts. No rule is given for how CRPIX1A/CRPIX2A change in a cutout. The only fact is that in the uncut image CRPIX1A=CRPIX2A=1.0 with CRVAL1A=CRVAL2A=0.0 and the name "0-based active pixel coordinates". That is consistent with, but does not verify, the cutout rule. DETCOORD = 'sky' notes that MWIR pixels are flipped on X to match the SWIR view (p.74).
- Pixel scale 6.15'' x 6.15'' (p.6); example OMEGA_MEDIAN = 37.945 arcsec^2 (p.75).

## 3. PSF / EPSF HDU
- [VERIFIED pp.13, 52, 59-60] Oversampling factor is FIVE. Each ePSF is a 33 x 33 array at 5x oversampling ("33 x 33 pixels sampled at an oversampling factor of five", p.52; "five times the native detector resolution ... 33 x 33", p.59). No 10x oversampling is mentioned anywhere in the document [NOT FOUND]. The earlier "5x with 33x33" is the one this document supports, and the "10x" in the earlier notes is not supported by this PDF.
- Zone layout [VERIFIED pp.13, 52, 59]: 21x21 zones for Detectors 1, 2, 4, 5, 6 (441 rows in the EPSF HDU) and 11x41 zones for Detector 3 (451 rows), with the finer sampling along the spectral/dispersion direction because of dichroic-beamsplitter birefringence.
- Normalization [p.13, 60]: normalized to unit total flux, dimensionless. It is an effective PSF (optical response x pixel response), not the optical PSF, and the pixel response is not deconvolved (p.59). Value at an offset = fraction of source flux in a pixel whose centre has that offset (p.59).
- Table columns (stand-alone product) [p.52, 60]: BINX, BINY, zone centre and extent, NSTAR, mean effective number of pixels (NEFF_MEAN), representative central-wavelength and bandpass info, 33x33 ePSF.
- Wavelength dependence: One ePSF per detector zone; each zone row records "representative wavelength information" [pp.52, 59, 60]. Fig. 21 caption: Neff "varies with wavelength" and Detector 3 is finer "to resolve the more rapid variation along its spectral direction" (p.61). Beyond this, a wavelength-interpolation rule is [NOT FOUND IN DOCUMENT].
- Header error [VERIFIED pp.13-14]: in QR1/QR2 files, PSF cube planes are stored in increasing x-index order, but the header says increasing y-index. The error can cause +/-5% photometry errors, largest in two corners. Fixed files carry the suffix "+psffix1" (pipeline 6.4 to 6.5.5), and 6.5.6+ and QR3/DR1 are correct. The ePSF method is new in R7 (p.52); the earlier optical-PSF method was replaced.
- Example PSF_FWHM (median) = 8.67 arcsec (p.75, one example header only).

## 4. Time, exposure, visits, survey dates
- Time scale [VERIFIED p.77]: TIMESYS = 'UTC'; MJDREF = 0.0; DATE-OBS/MJD-OBS = start of observation; also DATE-BEG/MJD-BEG, DATE-AVG/MJD-AVG (midpoint), DATE-END/MJD-END. Example: MJD-OBS 60792.774884525, MJD-AVG 60792.775550715, MJD-END 60792.776216904. Barycentric correction is not mentioned [NOT FOUND].
- Exposure [VERIFIED pp.6, 77]: Table 2 gives frame time 1.5349 s and exposure time 113.58 s. Header example XPOSURE = 113.5826 s ("scientifically meaningful exposure time") and TELAPSE = 118.1873 s (start to stop, including discarded frames; it "starts prior to MJD-BEG"). TSAMP=1.5349 s, SURLIM=77 frames, SURDLY=3 (pp.73, 28).
- Visits per sky position [partial]: "assuming 4 observations per wavelength" and "four full-survey passes" (pp.6, 8); four complete surveys over a 25-month mission (p.4); each sky position is covered in each spectral channel per survey. A precise count of exposures per sky position per pass is [NOT FOUND IN DOCUMENT]. One target group = 17 pointings at the same ecliptic longitude, spaced by one channel width in ecliptic latitude (p.8). Latitude rings and target groups are overlapped for redundancy. Full spectral sampling occurs twice a year (p.9, Fig. 4 caption).
- Survey passes [VERIFIED pp.4, 8-9, 14]: science operations began May 1, 2025 (p.4); launch 12 March 2025 03:10:12 UTC. Survey 1 = first 12.5 months with PA = 0 deg; Survey 2 = first 12.5 months with PA = 180 deg; Survey 3 = second 12.5 months with PA = 0; Survey 4 = second 12.5 months with PA = 180. Surveys 3-4 are shifted by 6' (half a channel) relative to 1-2. SPS_PA_ECL in the header identifies the survey. Explicit calendar end dates are not given (they follow from 12.5 months after May 1, 2025) [NOT FOUND as explicit dates]. Survey 3/4 data began 2026-05-16 (QR3, p.11). First plan 2025W17_4B (p.10).
- Observation ID format: e.g. 2025W22_2B_0001_1, with a maximum of 4 small slews per large slew (p.13).

## 5. Detectors and wavelength
- Table 2 (p.6): Band 1 0.744-1.116 um R=39; Band 2 1.099-1.651 R=41; Band 3 1.636-2.421 R=41; Band 4 2.423-3.822 R=35; Band 5 3.809-4.420 R=112; Band 6 4.412-5.002 R=128. 3x H2RG with 2.6 um cutoff (SWIR) and 3x H2RG with 5.3 um cutoff (MWIR).
- SWIR FPA (0.75-2.44 um, reflection, 62 K); MWIR FPA (2.40-5.01 um, transmission, 45 K); dichroic beamsplitter (p.7). DETECTOR header: 1-3 SWIR, 4-6 MWIR (p.73).
- Linear variable filter: one LVF over each detector; wavelength varies continuously with position along one axis (pp.7, 47, 22). Contours are curved ("smile"), not straight lines (pp.47, 63). y = 0 is the long-wavelength side of a detector in the Level-2 pixel convention (p.40). Per-pixel central wavelength = CWAVE (50% of cumulative transmission area), bandwidth = CWAVE / spectral resolution (CBAND) (p.61). The WCS-WAVE table in each image is an approximate piecewise-bilinear model intended for visualization only (pp.13, 61). For science use the separate Spectral WCS files (CWAVE/CBAND).
- Spectral channels (pp.62-66, Tables 29-34): 17 nominal channels per detector (1-17), plus 0 and 18 for corners/edges; the definition is geometric, not a calibrated wavelength solution. Band 1 median lambda_c 0.753-1.102 um (ch 1-17); Band 2 1.113-1.631; Band 3 1.656-2.399; Band 4 2.445-3.768; Band 5 3.834-4.405; Band 6 4.435-4.989. Bands 5 and 6 wavelengths were shifted in R7 per on-sky calibration (p.63).
- Dichroic edge pixels of Band 3 long side and Band 4 short side: DICHROIC flag where throughput < 50% (p.18).

## 6. Known data-quality issues (VERIFIED, pp.13-22, 24-30, 50, 56-58)
- PSF header ordering error in QR1/QR2 (p.13-14); do NOT combine QR1 and QR2 files; caution combining QR2 and QR3 (p.11).
- Image anomalies (pp.14-18): frame-edge ghost, linear bright-source ghost, beam-splitter ghost (~10' disk, Bands 3-6), 8 degree ghost (Bands 2-6), Moon stray light at edges (Bands 1, 4, 5, 6), extended cosmic ray signatures and snowballs, cosmic-ray-induced glow, three types of crosstalk (~32-row negative image, smear, 64-pixel channel spacing).
- Atmospheric features (pp.17-19): He 1.083 um line in Bands 1-2 (factor of few to 30 above zodi), spectral leaks near 0.84 um (Band 1) and 1.49 / 1.25 um (Band 2), auroral lines, other lines at 0.78, 0.84, 0.93, 1.13, 1.81, 2.63, 2.75, 4.03, 4.64 um, shuttle glow (~2.9 um in Band 4, ~4.5 um in Bands 5-6), diffuse optical transients (~1% of exposures), satellite streaks.
- Limitations (p.18): source-mask size depends on catalogued magnitude; dichroic-edge pixels have higher noise and less certain calibration. ZODI is NOT subtracted from IMAGE (p.11; mosaics subtract it, p.46). Emission lines are not subtracted (p.24).
- Bloom/snowball/halo masking only from planning period 2025W51_1A (p.50). Astrometry failure rate "<3%" before the R7 retry, sub-percent after (pp.37, 56-57). Variance underestimates scatter, so catalog uncertainties get an extra 3% added in quadrature (p.44). Absolute calibration "<1%" for the great majority of channels relative to CALSPEC (p.56); standards carry 1-4% systematics (Table 26). All-sky cube: channels 51/52 blank, airglow and extended-source striping (p.22). Mosaics: no precision photometry, use L2 images (p.46).
- Archive inclusion criteria (p.42): N_TRANSIENT < 435,000, not in the SAA, FINAST = 0, L2DQA = PASS.

## 7. Moving objects / proper motion
- Proper motion of reference stars [VERIFIED pp.24, 36, 59]: Gaia proper motions propagate stellar positions to the observation epoch for astrometry; sources with poorly constrained proper motions are excluded; pipeline 6.3.0 "Updated proper motion application for astrometry and source masking" (p.24).
- Solar System objects [VERIFIED p.38]: the source-mask mini-catalog is generated "from the Reference Catalog and the known Solar System object catalog". Moving-object detection, forced photometry or ephemeris handling for asteroids in the spectral images is [NOT FOUND IN DOCUMENT] beyond this single mention. Orbiting satellites are flagged as STREAK. Asteroid and comet spectra appear as a mission goal (p.4, "100,000 asteroid and comet spectra"). The forced photometry fixes source positions ("Source positions are not floated in the fit", p.43), so any moving-target use needs user-supplied per-exposure positions. This is an inference and not a statement in the document.
