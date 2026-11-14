# Tech notes: sub-pixel SPHEREx cutout viewer

## SPHEREx facts
- [VERIFIED from https://caltech-ipac.github.io/spherex-archive-documentation/spherex-data-products] Spectral image 2040x2040; HDUs IMAGE, FLAGS, VARIANCE, ZODI, PSF/EPSF, WCS-WAVE; units MJy/sr; PSF pixel 0.615" = 1/10 of 6.15" image pixel (6.15" implied, not stated directly). SIP coefficients mentioned only for separate SIP products; SIP in science WCS not confirmed on page.
- [VERIFIED from https://irsa.ipac.caltech.edu/data/SPHEREx/docs/cutout_tool.html via search snippet] IRSA cutout service keeps all HDUs, trims spatial ones, rewrites WCS-WAVE; tutorial reads WCS-WAVE with SIP disabled. (page not fetched directly)
- WCS-WAVE: wavelength varies per pixel -> each epoch/band has different wavelength; stacking across bands mixes SEDs. [inference]

## 1. Browser vs server
- Aladin Lite v3 [VERIFIED https://github.com/cds-astro/aladin-lite]: HiPS, FITS images+tables (Rust fitsrs), WCS parsing (mapproj), VOTable catalogs, proper-motion vectors, Rust/WebGL2, LGPL-3. SIP support NOT VERIFIED. Nearest-neighbor at high zoom NOT VERIFIED. Docs URLs (/AladinLite/doc/API/) returned 404.
- JS9 [VERIFIED https://github.com/ericmandel/js9]: FITS images/tables/cubes, regions, catalogs; ARCHIVED, development ended July 2022, last release v3.9 Dec 2024, "no maintainer". WCS/SIP/smoothing not documented in README. js9.si.edu fetch failed (ECONNREFUSED).
- fitsjs (astrojs/fitsjs) [VERIFIED https://github.com/astrojs/fitsjs]: HDUs, images, cubes, tables, Rice compression. No WCS mentioned; maintenance unclear (not shown). Needs own WCS (incl. SIP) code.
- Python server/offline (astropy.wcs handles SIP): best accuracy, can precompute PNG/binary tiles per epoch. Pyodide [VERIFIED https://pyodide.org/en/stable/usage/packages-in-pyodide.html]: astropy 7.2.0, numpy, scipy, scikit-image included; photutils, sep, reproject NOT in the list.
- Recommendation [opinion]: precompute in Python (reproject to common grid, detect, centroid) -> ship float arrays/PNG + JSON; custom canvas/WebGL viewer for pixel-exactness; Aladin only if HiPS/sky context needed.

## 2. Sub-pixel fidelity
- reproject [VERIFIED https://docs.astropy.org/projects/reproject/en/stable/celestial.html]: interp "not flux conserving", fastest, aliasing-prone when pixel sizes differ; adaptive: anti-aliased, optional conserve_flux, better with strong distortion; exact: "essentially an exact form of drizzling", slowest, only spherical celestial coords same origin, precision warning below ~0.05". SIP handling not discussed on page (astropy.wcs input is accepted; NOT VERIFIED here).
- Error budget: if target grid = same orientation/scale, exact reprojection of shifted frames introduces pixel-covariance (correlated noise) and slight smoothing; interp (bilinear) smooths PSF more. Prefer: do astrometry on native pixels, display on native grid, only resample for blinking/differencing. [inference]
- Display: CSS image-rendering: pixelated / WebGL NEAREST + grid overlay at zoom >~8x; draw pixel centers at integer coords (FITS 1-based vs 0-based, half-pixel offset trap). [general knowledge, NOT VERIFIED from URL]

## 3. Detection/centroiding
- photutils [VERIFIED https://docs.astropy.org/projects/photutils/en/stable/user_guide/detection.html]: DAOStarFinder (Stetson DAOFIND), IRAFStarFinder (moments), find_peaks centroid_func gives subpixel; page gives no accuracy numbers.
- SEP [VERIFIED https://sep.readthedocs.io/en/stable/]: background, extraction, deblending, aperture photometry w/ exact overlap; centroid not mentioned there; pip/conda; LGPL.
- Accuracy: [VERIFIED https://arxiv.org/abs/1610.05873] known-PSF polynomial centroid after PSF smoothing ~ ML efficiency; PSF fitting beats polynomial when PSF unknown; center-of-light never approaches CRLB. [search snippet, arXiv:2004.06253] Gaussian fit variance up to 8/(3*sqrt3) of ePSF fit at high S/N. sigma ~ FWHM/SNR scaling: NOT VERIFIED from a source (general knowledge; check Mendez et al. 2013). SPHEREx PSF is undersampled at 6.15" -> use the provided EPSF/PSF HDU for fitting.
- Proper motion: fit centroid per epoch in a common WCS (astropy WCS pixel->world), linear fit of position vs time; uncertainty = per-epoch sigma / time baseline. SPHEREx epochs are different wavelengths -> color-dependent centroid shifts possible. [inference]

## 4. Moving objects
- Not researched via URL. Approach [NOT VERIFIED]: build median stack as static template, subtract per epoch, detect residual peaks, link detections across epochs with linear-motion fit (shift-and-stack). Beware per-band PSF/flux differences.

## 5. Hosting
- Cloudflare Workers free [VERIFIED https://developers.cloudflare.com/workers/platform/limits/]: 100k req/day, 10 ms CPU/request, 128 MB memory, 64 MiB bundle. Too tight for astropy work; Python Workers exist (snippet claims) but compute budget tiny.
- Hugging Face Spaces [VERIFIED https://huggingface.co/docs/hub/spaces-overview]: Static Spaces free; Gradio/Docker require paid plan (PRO) to create; CPU Basic 2 vCPU 16 GB; free hardware sleeps. So free Python API on HF is NOT available without PRO.
- Cloudflare Pages free file limit 20,000 files [secondary source only, NOT VERIFIED]; GitHub Pages not fetched.
- Best hackathon plan: precompute everything locally, host static files (GitHub/Cloudflare Pages or HF static Space); pull cutouts live from IRSA only if needed.
