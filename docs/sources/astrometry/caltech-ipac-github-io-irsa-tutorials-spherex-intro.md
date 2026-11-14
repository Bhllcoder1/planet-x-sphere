---
source: https://caltech-ipac.github.io/irsa-tutorials/spherex-intro
fetched: 2026-11-14
status: 200
---

Introduction to SPHEREx Spectral Images - IRSA Notebooks

[Skip to article frontmatter](#skip-to-frontmatter)[Skip to article content](#skip-to-article)

**Site not loading correctly?**

This may be due to an incorrect `BASE_URL` configuration. See [the MyST Documentation](https://mystmd.org/guide/deployment#deploy-base-url) for reference.

Open Menu

[![](/irsa-tutorials/_public/irsa_logo-3035c03f80b795b927451a0fd4c2e41a.png)

Made with MyST](/irsa-tutorials/)

[IRSA Notebooks](/irsa-tutorials/)

[Contributed Notebooks](https://irsa.ipac.caltech.edu/irsa-contributed-notebooks/)

Search

[IRSA Notebooks](/irsa-tutorials/)[Contributed Notebooks](https://irsa.ipac.caltech.edu/irsa-contributed-notebooks/)

[IRSA Notebooks](/irsa-tutorials/ "IRSA Notebooks")

[SPHEREx](/irsa-tutorials/spherex "SPHEREx Tutorial Notebooks")

[Data Overview](/irsa-tutorials/spherex-intro "Introduction to SPHEREx Spectral Images")[Spectral Image Cutouts](/irsa-tutorials/spherex-cutouts "Download a collection of SPHEREx Spectral Image cutouts as a multi-extension FITS file")[PSF Models](/irsa-tutorials/spherex-psf "Understanding and Extracting the ePSF Extension in a SPHEREx Cutout")[Source Discovery Tool](/irsa-tutorials/spherex-source-discovery-tool-demo "SPHEREx Source Discovery Tool IRSA Demo")[Mosaic Cube](/irsa-tutorials/spherex-mosaic "Understanding and Analyzing SPHEREx Mosaic Cubes")[HiPS All-Sky Cube](/irsa-tutorials/spherex-hipscube "Using SPHEREx HiPS All-Sky Mosaic Cubes")

[Euclid](/irsa-tutorials/euclid "Euclid Tutorial Notebooks")

[WISE](/irsa-tutorials/wise "WISE Tutorial Notebooks")

COSMOS

Spitzer

ZTF

[Simulated Data](/irsa-tutorials/simulated "Simulated Data Tutorial Notebooks")

[Techniques & Tools](/irsa-tutorials/techniques "Techniques & Tools Tutorial Notebooks")

[Made with MyST](https://mystmd.org/made-with-myst)

1. [IRSA Notebooks](/irsa-tutorials/)
2. [SPHEREx](/irsa-tutorials/spherex)
3. Data Overview

IRSA Notebooks

Downloads

Introduction to SPHEREx Spectral Images
=======================================

Jessica KrickVandana DesaiAndreas FaisstTroy RaenBrigitta Sipőcz

1. Learning Goals[¶](#id-1-learning-goals "Link to this Section")
-----------------------------------------------------------------

* Query for SPHEREx Spectral Image Multi-Extension FITS files (MEFs) that overlap a given coordinate on the sky.
* Read in a SPHEREx Spectral Image MEF using Astropy and understand its structure.
* Interactively visualize a SPHEREx Spectral Image MEF using Firefly.
* Explore each extension. For the Spectral Image extension, this includes understanding the astrometric and spectral WCS systems.

2. SPHEREx Overview[¶](#id-2-spherex-overview "Link to this Section")
---------------------------------------------------------------------

SPHEREx is a NASA Astrophysics Medium Explorer mission that launched in March 2025. During its planned two-year mission, SPHEREx will obtain 0.75-5 micron spectroscopy over the entire sky, with deeper data in the SPHEREx Deep Fields. SPHEREx data will be used to:

* **constrain the physics of inflation** by measuring its imprints on the three-dimensional large-scale distribution of matter,
* **trace the history of galactic light production** through a deep multi-band measurement of large-scale clustering,
* **investigate the abundance and composition of water and biogenic ices** in the early phases of star and planetary disk formation.

The community will also mine SPHEREx data and combine it with synergistic data sets to address a variety of additional topics in astrophysics.

More information about SPHEREx, the data releases, and the data products is available in the [SPHEREx Archive at IRSA User Guide](https://caltech-ipac.github.io/spherex-archive-documentation).

This notebook uses data from SPHEREx Data Release 1 (DR1).
QR3 and DR1 supersede the earlier Quick Release 2 (QR2), and SPHEREx recommends using QR3 and DR1 over QR2.

3. Requirements[¶](#id-3-requirements "Link to this Section")
-------------------------------------------------------------

The following packages must be installed to run this notebook.

```
# Uncomment the next line to install dependencies if needed.
# %pip install numpy matplotlib astropy astroquery firefly-client
```

4. Imports[¶](#id-4-imports "Link to this Section")
---------------------------------------------------

```
import http.client
import time
import urllib.error

import numpy as np
import matplotlib.pyplot as plt

from astropy.io import fits
from astropy.wcs import WCS
from astropy.table import Table
from astropy import units as u
from astropy.coordinates import SkyCoord

from astroquery.ipac.irsa import Irsa

from firefly_client import FireflyClient

# The time it takes to read SPHEREx files can exceed
# astropy's default timeout limit. Increase it.
from astropy.utils.data import conf
conf.remote_timeout = 120
```

5. Search for SPHEREx Spectral Image MEFs that overlap coordinates you are interested in[¶](#id-5-search-for-spherex-spectral-image-mefs-that-overlap-coordinates-you-are-interested-in "Link to this Section")
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Define some coordinates of interest.

```
ra_deg = 304.693508808
dec_deg = 42.4436872991

coord = SkyCoord(ra_deg, dec_deg, unit='deg')
search_radius = 1 * u.arcsec
```

Query IRSA for a list of Spectral Image MEFs that overlap this position. We use the [IRSA module in astroquery](https://astroquery.readthedocs.io/en/latest/ipac/irsa/irsa.html) and the Simple Image Access (SIA) API.

Tip

The IRSA SIA collections can be listed using using the `list_collections` method, we can filter on the ones containing “spherex” in the collection name:

```
Irsa.list_collections(servicetype='SIA', filter='spherex')
```

The collections are documented at [SPHEREx Data Access: Application Program Interfaces (APIs)](https://caltech-ipac.github.io/spherex-archive-documentation/spherex-data-access#application-program-interfaces-apis)
The Spectral Image MEFs are available in four collections:

* `'spherex_dr1'` -- DR1 Spectral Image MEFs that are part of the SPHEREx **Wide Survey**
* `'spherex_dr1_deep'` -- DR1 Spectral Image MEFs that are part of the SPHEREx **Deep Survey**
* `'spherex_qr3'` -- QR3 Spectral Image MEFs that are part of the SPHEREx **Wide Survey**
* `'spherex_qr3_deep'` -- QR3 Spectral Image MEFs that are part of the SPHEREx **Deep Survey**

```
results = Irsa.query_sia(pos=(coord, search_radius), collection=['spherex_dr1', 'spherex_qr3'])
```

Note

SPHEREx data are ingested on a weekly basis.
Due to the nature of the ingestion process, availability via SIA will lag on the order of a day.
To avoid this delay, users can access data through the browsable directories or the SPHEREx Data Explorer GUI (see [SPHEREx Data Access](https://caltech-ipac.github.io/spherex-archive-documentation/spherex-data-access)), or do a TAP query as shown in [Download a collection of SPHEREx Spectral Image cutouts as a multi-extension FITS file](/irsa-tutorials/spherex-cutouts).

Each row of the results of your query represents a different spectral image.
Because SPHEREx data will be released on a weekly basis, the number of rows returned will change
depending on when you submit the query.
Let’s see how many images are returned today.

```
len(results)
```

`443`

The query results provide a lot of metadata about each spectral image. These columns have standard names as defined by the IVOA. Let’s list them:

```
results.colnames
```

`['s_ra',
's_dec',
'facility_name',
'instrument_name',
'dataproduct_subtype',
'calib_level',
'dataproduct_type',
'energy_bandpassname',
'energy_emband',
'obs_id',
's_resolution',
'em_min',
'em_max',
'em_res_power',
'proposal_title',
'access_url',
'access_format',
'access_estsize',
't_exptime',
's_region',
'obs_collection',
'obs_intent',
'algorithm_name',
'facility_keywords',
'instrument_keywords',
'environment_photometric',
'proposal_id',
'proposal_pi',
'proposal_project',
'target_name',
'target_type',
'target_standard',
'target_moving',
'target_keywords',
'obs_release_date',
's_xel1',
's_xel2',
's_pixel_scale',
'position_timedependent',
't_min',
't_max',
't_resolution',
't_xel',
'obs_publisher_did',
's_fov',
'em_xel',
'pol_states',
'pol_xel',
'cloud_access',
'o_ucd',
'upload_row_id']`

The `'access_url'` column is particularly important because it tells you how to access the data. Let’s look at the `'access_url'` value for the first row:

```
spectral_image_url = results['access_url'][0]
print(spectral_image_url)
```

```
https://irsa.ipac.caltech.edu/ibe/data/spherex/dr1/level2/2025W18_1B/l2b-v27-2026-196/1/level2_2025W18_1B_0074_2D1_spx_l2b-v27-2026-196.fits

```

You can put this URL into a browser to download the file. Or you can work with it in Python, as shown below.

6. Examine the header of one of the SPHEREx Spectral Image MEFs[¶](#id-6-examine-the-header-of-one-of-the-spherex-spectral-image-mefs "Link to this Section")
-------------------------------------------------------------------------------------------------------------------------------------------------------------

First, use Astropy to load the data using the URL from the previous step.
Transient read errors occur sometimes, so we’ll catch those and retry a few times.

```
# Max number of times to retry HTTP errors.
max_retries = 3
for attempt in range(max_retries):
    try:
        # Load the data, reading every extension into memory so that
        # hdulist stays usable after the file is closed.
        with fits.open(spectral_image_url, memmap=False) as hdulist:
            for hdu in hdulist:
                hdu.data
        break
    except (TimeoutError, urllib.error.HTTPError, http.client.IncompleteRead):
        if attempt == max_retries - 1:
            raise
        time.sleep(10 * (attempt + 1))
```

Examine the header.

```
hdulist.info()
```

```
Filename: /home/runner/.cache/astropy/download/url/2edb0eda84f44a114b0a0118c29fe067/contents
No.    Name      Ver    Type      Cards   Dimensions   Format
  0  PRIMARY       1 PrimaryHDU       5   ()      
  1  IMAGE         1 ImageHDU       293   (2040, 2040)   float32   
  2  FLAGS         1 CompImageHDU    185   (2040, 2040)   int32   
  3  VARIANCE      1 ImageHDU       119   (2040, 2040)   float32   
  4  ZODI          1 ImageHDU       122   (2040, 2040)   float32   
  5  EPSF          1 BinTableHDU     56   441R x 11C   ['J', 'J', 'E', 'E', 'E', 'E', 'J', 'E', 'E', 'E', '1089D']   
  6  WCS-WAVE      1 BinTableHDU     22   1R x 3C   ['9J', '9J', '162E']   

```

You can see that the Level 2 Spectral Image files are multi-extension FITS files (MEFs) with the following extensions:

* **IMAGE:** Calibrated fluxes for a detector array in scientific units of MJy/sr.
* **FLAGS:** A bitmap with per-pixel status and processing flags.
* **VARIANCE:** A per-pixel estimate of the variance.
* **ZODI:** An model of the zodiacal dust background signal. Note that this is not subtracted from the IMAGE extension.
* **EPSF:** A table of effective Point Spread Functions (ePSFs), one for each of 441 regions of the detector, in over-sampled pixel space.
* **WCS-WAVE:** Spectral WCS lookup table that maps pixel coordinates to the central wavelength and bandwidth of each pixel.

We will tour each extension in the sections below.

7. Visualize a SPHEREx Spectral Image MEF using the Firefly Python Client.[¶](#id-7-visualize-a-spherex-spectral-image-mef-using-the-firefly-python-client "Link to this Section")
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

We will use the open-source astronomy data visualization software Firefly visualize SPHEREx data. Firefly has a Python client and it understands the alternative WCS coordinates of SPHEREx, allowing users to see how the wavelength and bandwidth vary with spectral image pixels.

Open a Firefly viewer in a separate browser tab and initialize it.

```
fc = FireflyClient.make_client(url="https://irsa.ipac.caltech.edu/irsaviewer")

fc.reinit_viewer()
```

Loading...

`{'success': True}`

Visualize a spectral image MEF by sending its URL to the viewer.

```
fc.show_fits_image(file_input=spectral_image_url,
             plot_id="spectral_image",
             Title="Spectral Image"
             )
```

`{'success': True}`

Try use the interactive tools in the viewer to explore the data.

8. Explore the first extension: IMAGE[¶](#id-8-explore-the-first-extension-image "Link to this Section")
--------------------------------------------------------------------------------------------------------

The first extension of the MEF is the the calibrated surface brightness flux density in units of MJy/sr, stored as a 2040 x 2040 image. No zodiacal light subtraction is applied.

The SPHEREx focal plane is split with a dichroic to three short-wavelength and three long-wavelength detector arrays. Two focal plane assemblies (FPAs) simultaneously image the sky through a dichroic beam splitter. Each FPA contains three 2K x 2K detector arrays placed behind a set of linear variable filters (LVFs), providing narrow-band response with a band center that varies along one axis of the array. SPHEREx obtains spectra through multiple exposures, placing a given source at multiple positions in the field of view, where it is measured at multiple wavelengths by repointing the spacecraft.

* Band 1: λ= 0.75 - 1.09 µm; R=39
* Band 2: λ= 1.10 - 1.62 µm; R=41
* Band 3: λ= 1.63 - 2.41 µm; R=41
* Band 4: λ= 2.42 - 3.82 µm; R=35
* Band 5: λ= 3.83 - 4.41 µm; R=112
* Band 6: λ= 4.42 - 5.00 µm; R=128

Examine the header of the first extension, printing out select keywords.

```
spectral_image_header = hdulist[1].header

keywords_to_print = ['EXTNAME', 'NAXIS1', 'NAXIS2', 'BUNIT', 'DETECTOR', 'OBSID', 'DATE', 'PSF_FWHM']

for keyword in keywords_to_print:
    value = spectral_image_header.get(keyword, 'Keyword not found')
    print(f"{keyword}: {value}")
```

```
EXTNAME: IMAGE
NAXIS1: 2040
NAXIS2: 2040
BUNIT: MJy / sr
DETECTOR: 1
OBSID: 2025W18_1B_0074_2
DATE: 2026-07-16T03:19:15.597
PSF_FWHM: 7.530770327317724

```

We can see that this image was taken with Detector 2, so we can expect the wavelength to vary from 1.10 - 1.62 µm. Try examining the Firefly visualization to confirm this.

Notice that there is more than one WCS!

```
spectral_image_header['WCSNAME*']
```

`WCSNAMEA= '0-based active pixel coordinates' / Coordinate system title
WCSNAMEW= 'Approximated per-pixel wavelength and bandwidth' / WCS label`

The main WCS describes the astrometric registration of the image, including optical distortion parameters, based on the FITS pixel convention starting with 1.

There are two alternative WCS systems:

* WCSNAMEA describes zero-based pixel coordinates.
* WCSNAMEW describes spectral coordinates ‘Wavelength’ and ‘Bandwidth’. This WCS contains a reference to the lookup table in the ‘WCS-WAVE’ extension.

### 8a. Spatial WCS[¶](#id-8a-spatial-wcs "Link to this Section")

Load the Spatial WCS

```
wcs = WCS(spectral_image_header)
wcs
```

`WCS Keywords
Number of WCS axes: 2
CTYPE : 'RA---TAN-SIP' 'DEC--TAN-SIP'
CUNIT : 'deg' 'deg'
CRVAL : 303.877766184 40.5489585415
CRPIX : 1020.5 1020.5
PC1_1 PC1_2 : -0.00161399858549 -0.000503359988208
PC2_1 PC2_2 : -0.000566313443671 0.00163301103545
CDELT : 1.0 1.0
NAXIS : 2040 2040`

Use standard Astropy methods to resolve the central ra and dec (given by crval1 and crval2 in the header) into image pixel coordinates.

```
ra, dec = wcs.wcs.crval
x, y = wcs.world_to_pixel(SkyCoord(ra=ra, dec=dec, unit="deg"))
print(ra, dec, x, y)
```

```
303.877766184 40.5489585415 1019.0880637763953 1020.746373505631

```

### 8b. Spectral WCS[¶](#id-8b-spectral-wcs "Link to this Section")

The use of Linear Variable Filters (LVFs) is a key component of SPHEREx imaging. Each pixel of the detector corresponds to a slightly different wavelength and bandwidth due to the LVF’s gradual variation in spectral transmission across its surface. Contours of constant wavelength are curved due to the method of filter fabrication, so the wavelength-vs-pixel function is inherently two-dimensional.

A compact, approximate representation of the wavelength and bandwidth per pixel is included in each image using the WAVE-TAB lookup-table mechanism defined in the FITS standard.

Below we illustrate how to use Spectral WCS to find an approximate wavelength at each pixel.

```
# Load the Spectral WCS from the header.
# Note that we need to provide a reference to HDU List, which contains a lookup table.
spectral_wcs = WCS(header=hdulist["IMAGE"].header, fobj=hdulist, key="W")
```

```
INFO: 
                Inconsistent SIP distortion information is present in the FITS header and the WCS object:
                SIP coefficients were detected, but CTYPE is missing a "-SIP" suffix.
                astropy.wcs is using the SIP distortion coefficients,
                therefore the coordinates calculated here might be incorrect.

                If you do not want to apply the SIP distortion coefficients,
                please remove the SIP coefficients from the FITS header or the
                WCS object.  As an example, if the image is already distortion-corrected
                (e.g., drizzled) then distortion components should not apply and the SIP
                coefficients should be removed.

                While the SIP distortion coefficients are being applied here, if that was indeed the intent,
                for consistency please append "-SIP" to the CTYPE in the FITS header or the WCS object.

                 [astropy.wcs.wcs]

```

Note: The previous line triggers an Astropy INFO printout,
which implies that the SIP distortion coefficients from the main WCS are preserved in the alternative WCS.
This is because the SIP convention, not formally part of the FITS standard,
is ambiguous as to whether it is meant to apply to ‘alternative’ (lettered) WCSes in addition to the primary WCS.
See [astropy/astropy#13105](https://github.com/astropy/astropy/issues/13105).

The wavelength per pixel is a property of the detector-filter combination and is independent of optical distortion in the telescope,
and is modeled accordingly in WCS ‘W’, so we turn the SIP distortion off for this WCS.

```
# SIP distortions must be turned off for the spectral WCS.
spectral_wcs.sip = None
```

```
# The standard Astropy methods for converting pixel coordinates to world coordinates can also be used to obtain spectral coordinates.
# Take the pixel coordinates that we determined for the image center and resolve them to the wavelength and bandwidth for that pixel
wl, bw = spectral_wcs.pixel_to_world(x, y)
wl, bw
```

`(<SpectralCoord 0.90416686 um>, <Quantity 0.02298403 um>)`

### 8c. How does wavelength vary across the detector?[¶](#id-8c-how-does-wavelength-vary-across-the-detector "Link to this Section")

```
# Read in the spectral image data.
spectral_image = hdulist["IMAGE"]
spectral_image_data = spectral_image.data

# Get arrays of pixel coordinates for the image.
(y, x) = np.indices(spectral_image.shape)

# Use the spectral WCS to convert these pixel coordinates to spectral coordinates.
spectral_coords = spectral_wcs.pixel_to_world(x, y)

# Break out the two spectral coordinates (wavelength and bandwidth) from the spectral coordinates, and print the results.
wavelength, bandwidth = spectral_coords
print("Wavelength: \n", wavelength)
print("Bandwidth: \n", bandwidth)
```

```
Wavelength: 
 [[1.12616599 1.12614512 1.12612426 ... 1.12623829 1.12625823 1.12627816]
 [1.12594346 1.1259226  1.12590174 ... 1.1260164  1.12603634 1.12605627]
 [1.12572094 1.12570008 1.12567922 ... 1.12579451 1.12581444 1.12583438]
 ...
 [0.74469219 0.74467621 0.74466023 ... 0.74529567 0.74531224 0.74532881]
 [0.74453702 0.74452105 0.74450508 ... 0.74514335 0.74515991 0.74517648]
 [0.74438184 0.74436589 0.74434993 ... 0.74499102 0.74500758 0.74502414]] um
Bandwidth: 
 [[0.02880928 0.02881236 0.02881544 ... 0.02953041 0.02952625 0.02952209]
 [0.02880678 0.02880985 0.02881291 ... 0.02952707 0.02952292 0.02951877]
 [0.02880427 0.02880733 0.02881039 ... 0.02952373 0.02951959 0.02951546]
 ...
 [0.01724998 0.01725043 0.01725087 ... 0.01568995 0.01568707 0.01568419]
 [0.01724339 0.01724384 0.0172443  ... 0.01567851 0.01567563 0.01567275]
 [0.0172368  0.01723726 0.01723772 ... 0.01566708 0.01566419 0.0156613 ]] um

```

```
# Plot the wavelength as a greyscale color map across the image pixels.
plt.imshow(wavelength.value, origin='lower', cmap='gray')
plt.colorbar(label=f"Wavelength [{wavelength.unit}]")

detector = hdulist["IMAGE"].header["DETECTOR"]
plt.title(f"Wavelength - Detector {detector}")
plt.show()
```

![<Figure size 640x480 with 2 Axes>](/irsa-tutorials/_public/cae4d4ee10883fe69a0ef1a138cad45c.png)

As expected, the wavelengths range from approximately 1.1=16 micron for Detector 2. You can see that the longest wavelengths are at the bottom and the shortest wavelengths are at the top. You can verify this is the case in the Firefly visualization, as well.

### 8d. Number of flagged pixels in this image[¶](#id-8d-number-of-flagged-pixels-in-this-image "Link to this Section")

Now let’s take a look at some header keywords that provide information about how many pixels have been flagged during processing.

```
spectral_image_header['L2 N_*']
```

`HIERARCH L2 N_NONLINEAR = 0 / number of pixels flagged nonlinear
HIERARCH L2 N_PERSIST = 23502 / number of pixels flagged persist
HIERARCH L2 N_HOT = 1 / number of pixels flagged hot
HIERARCH L2 N_COLD = 1307 / number of pixels flagged cold
HIERARCH L2 N_TRAN_NB = 23511 / number of not bad transient pixels
HIERARCH L2 N_PERS_NB = 23498 / number of persistence and not bad pixels
HIERARCH L2 N_SOURCE = 4135535 / number of source flagged pixels
HIERARCH L2 N_XTALK = 53262 / number of crosstalk flagged pixels
HIERARCH L2 N_GHOST = 0 / number of ghost flagged pixels
HIERARCH L2 N_GHOST_FPA = 0 / number of ghost_fpa flagged pixels
HIERARCH L2 N_GHOST_EXT = 0 / number of ghost_ext flagged pixels
HIERARCH L2 N_BLOOM_NS = 0 / number of BLOOM flagged pixels not flagged SOURCE
HIERARCH L2 N_SNOW_NS = 0 / number of SNOW flagged pixels not flagged SOURCE
HIERARCH L2 N_OUTLIER = 842 / number of flagged outlier pixels
HIERARCH L2 N_TRANSIENT = 31044 / number of flagged flagged transient pixels
HIERARCH L2 N_OVERFLOW = 2976 / number of flagged overflow pixels
HIERARCH L2 N_SUR_ERROR = 20025 / number of flagged sur error pixels
HIERARCH L2 N_NONFUNC = 10924 / number of flagged nonfunctional pixels
HIERARCH L2 N_DICHROIC = 0 / number of flagged pixels due to low efficiency
HIERARCH L2 N_MISSING = 0 / number of flagged pixels with missing data
HIERARCH L2 N_FULLSAMPLE = 240 / number of flagged full-sample pixels
HIERARCH L2 N_PHANMISS = 0 / number of flagged phanmiss pixels
HIERARCH L2 N_SNOWBALL = 84 / number of flagged snowball artifact pixels
HIERARCH L2 N_BLOOM = 7944 / number of flagged bloom artifact pixels
HIERARCH L2 N_HALO = 71118 / number of flagged transient halo pixels
HIERARCH L2 N_SAT_HALO = 0 / number of flagged streak halo pixels`

These keywords count the pixels carrying most of the flags defined in the FLAGS header (see section 9), plus a few combined counts: keywords ending in `_NB` count pixels that are not also flagged as bad, and those ending in `_NS` count pixels that are not also flagged SOURCE. Typically, most of the pixels are identified as SOURCE pixels, which are pixels mapped to a known source. The flags are described in Table 16 of the [SPHEREx Explanatory Supplement](https://irsa.ipac.caltech.edu/data/SPHEREx/docs/SPHEREx_Expsupp.pdf).

9. Explore the second extension: FLAGS[¶](#id-9-explore-the-second-extension-flags "Link to this Section")
----------------------------------------------------------------------------------------------------------

The second extension (FLAGS) provides a bitmap of per-pixel status and processing flags, stored as a 2040 x 2040 image.

Let’s take a look at the header of the FLAGS extension, and print out some header keywords of interest.

```
flags_header = hdulist[2].header

keywords_to_print = ['EXTNAME', 'NAXIS1', 'NAXIS2', 'BUNIT']

for keyword in keywords_to_print:
    value = flags_header.get(keyword, 'Keyword not found')
    print(f"{keyword}: {value}")
```

```
EXTNAME: FLAGS
NAXIS1: 2040
NAXIS2: 2040
BUNIT: 

```

Conveniently, the definitions of the flags are also provided in the FLAGS header. For each bit number n, the keyword `MSKNnnnn` gives the flag name and `MSKDnnnn` gives its description.

```
for key in flags_header['MSKN*']:
    bit = key[4:]
    print(f"{int(bit):2d}  {flags_header[key]:<13} {flags_header['MSKD' + bit]}")
```

```
 0  TRANSIENT     Transient detected during SUR
 1  OVERFLOW      Overflow detected during SUR
 2  SUR_ERROR     Error in onboard processing
 6  NONFUNC       Permanently unusable
 7  DICHROIC      Low efficiency due to dichroic
 9  MISSING_DATA  Onboard data lost
10  HOT           Hot pixel
11  COLD          Anomalously low signal
12  FULLSAMPLE    Pixel full sample history is available
14  PHANMISS      Phantom correction was not applied
15  NONLINEAR     Nonlinearity correction cannot be applied reliably
17  PERSIST       Persistent charge above threshold
19  OUTLIER       Pixel flagged by Detect Outliers
20  CROSSTALK     Pixel affected by crosstalk.
21  SOURCE        Pixel mapped to a known source
22  GHOST         Affected by a bright source inside the exposure
23  GHOST_FPA     Affected by a bright source on another detector
24  GHOST_EXT     Pixel affected by a bright source outside FOV
25  STREAK        Pixel affected by a streak
26  BLOOM         Pixel part of a bloom artifact
27  SNOWBALL      Pixel part of a snowball artifact
28  HALO          Pixel part of a transient halo

```

Tip: In the Firefly visualization, if you are looking at the first extension (IMAGE), you can open up the layers icon (top right) to enable overlaying a visualization of the flags.

10. Explore the third extension: VARIANCE[¶](#id-10-explore-the-third-extension-variance "Link to this Section")
----------------------------------------------------------------------------------------------------------------

The third extension of the MEF is the variance of the calibrated surface brightness flux in units of (MJy/sr)^2, stored as a 2,040 x 2,040 image. Let’s look at some specific header keywords:

```
variance_header = hdulist[3].header

keywords_to_print = ['EXTNAME', 'NAXIS1', 'NAXIS2', 'BUNIT']

for keyword in keywords_to_print:
    value = variance_header.get(keyword, 'Keyword not found')
    print(f"{keyword}: {value}")
```

```
EXTNAME: VARIANCE
NAXIS1: 2040
NAXIS2: 2040
BUNIT: MJy2 / sr2

```

11. Explore the fourth extension: ZODI[¶](#id-11-explore-the-fourth-extension-zodi "Link to this Section")
----------------------------------------------------------------------------------------------------------

The fourth extension of the MEF is the modeled zodiacal light background flux in units of MJy/sr, stored as a 2040 x 2040 image. This has not been subtracted from the IMAGE extension. Let’s examine some header keywords:

```
zodi_header = hdulist[4].header

keywords_to_print = ['EXTNAME', 'NAXIS1', 'NAXIS2', 'BUNIT']

for keyword in keywords_to_print:
    value = zodi_header.get(keyword, 'Keyword not found')
    print(f"{keyword}: {value}")
```

```
EXTNAME: ZODI
NAXIS1: 2040
NAXIS2: 2040
BUNIT: MJy / sr

```

12. Explore the fifth extension: EPSF[¶](#id-12-explore-the-fifth-extension-epsf "Link to this Section")
--------------------------------------------------------------------------------------------------------

The fifth extension of the MEF contains the effective Point Spread Function (ePSF), stored as a binary table. The detector is divided into a 21 x 21 grid of regions (each about 97 x 97 spectral image pixels), and each of the 441 rows of the table holds the ePSF for one region, along with that region’s position on the detector (`XCENTER`, `YCENTER`) and its central wavelength and bandwidth (`CWAVE`, `CBAND`). Each ePSF is a 33 x 33 array, oversampled by a factor of 5 relative to the spectral image pixels (header keywords `OVSMPX` and `OVSMPY`). Unlike an optical PSF, the ePSF is a model of the pixel-convolved PSF: it predicts the pixel values of a point source at any sub-pixel position. The [SPHEREx ePSF tutorial](/irsa-tutorials/spherex-psf) shows how to find and use the ePSF for a given position. Let’s look at some specific header keywords for the EPSF:

```
psf_header = hdulist["EPSF"].header

keywords_to_print = ['EXTNAME', 'NAXIS2', 'DETECTOR', 'OVSMPX', 'OVSMPY']

for keyword in keywords_to_print:
    value = psf_header.get(keyword, 'Keyword not found')
    print(f"{keyword}: {value}")
```

```
EXTNAME: EPSF
NAXIS2: 441
DETECTOR: 1
OVSMPX: 5
OVSMPY: 5

```

13. Explore the sixth extension: WCS-WAVE[¶](#id-13-explore-the-sixth-extension-wcs-wave "Link to this Section")
----------------------------------------------------------------------------------------------------------------

The sixth extension is a FITS-compliant spectral World Coordinate System (WCS) lookup table that maps spectral image pixel coordinates to central wavelengths and bandwidths. The lookup table consists of 1 row with 3 columns (X, Y, VALUES). X and Y are each arrays defining a grid of control points in spectral image pixel space. For each (X, Y) control point, VALUES defines a two-element array containing the central wavelength and the corresponding bandwidth. Originally adopted to support the unique nature of the SPHEREx LVF filters, this rarely-used part of the FITS standard has yet to be implemented by all readers. The Firefly client we use in this notebook does correctly interpret this lookup table.

Let’s look at the header of the WCS-WAVE extension:

```
wcs_wave_header = hdulist[6].header
wcs_wave_header
```

`XTENSION= 'BINTABLE' / binary table extension
BITPIX = 8 / array data type
NAXIS = 2 / number of array dimensions
NAXIS1 = 720 / length of dimension 1
NAXIS2 = 1 / length of dimension 2
PCOUNT = 0 / number of group parameters
GCOUNT = 1 / number of groups
TFIELDS = 3 / number of table fields
TTYPE1 = 'X '
TFORM1 = '9J '
TDIM1 = '(9) '
TTYPE2 = 'Y '
TFORM2 = '9J '
TDIM2 = '(9) '
TTYPE3 = 'VALUES '
TFORM3 = '162E '
TDIM3 = '(2,9,9) '
EXTNAME = 'WCS-WAVE'
DETECTOR= '1 '
DETCOORD= 'sky '
HISTORY Headers standardized by SSDC on 2026-06-26T22:53:34.735 (UTC)
HISTORY Calibration source file: spectral_wcs_1_v2.2.fits`

Unlike the other extensions, this is a binary table. Let’s read it iinto an Astropy table.

```
wcs_wave_table = Table(hdulist[6].data)

print("Number of rows:", len(wcs_wave_table))
print("Column names:", wcs_wave_table.colnames)
```

```
Number of rows: 1
Column names: ['X', 'Y', 'VALUES']

```

This table consists of just 1 row with three columns. Let’s inspect the columns:

```
x_array      = wcs_wave_table["X"][0]
y_array      = wcs_wave_table["Y"][0]
wavelengths  = wcs_wave_table["VALUES"][0]

print("X:",  x_array)
print("Y:",y_array)
print("Dimensions of VALUES array:",  wavelengths.shape)
```

```
X: [   1  256  511  766 1021 1275 1530 1785 2040]
Y: [   1  256  511  766 1021 1275 1530 1785 2040]
Dimensions of VALUES array: (9, 9, 2)

```

Acknowledgements[¶](#acknowledgements "Link to this Section")
-------------------------------------------------------------

* [IPAC-IRSA](https://irsa.ipac.caltech.edu/)

About this notebook[¶](#about-this-notebook "Link to this Section")
-------------------------------------------------------------------

**Contact:** [IRSA Helpdesk](https://irsa.ipac.caltech.edu/docs/help_desk.html) with questions
or problems.

**Updated:** 5 March 2026

**Runtime:** approximately 30 seconds

## Links found on page

- https://astroquery.readthedocs.io/en/latest/ipac/irsa/irsa.html
- https://caltech-ipac.github.io/irsa-tutorials/
- https://caltech-ipac.github.io/irsa-tutorials/euclid
- https://caltech-ipac.github.io/irsa-tutorials/simulated
- https://caltech-ipac.github.io/irsa-tutorials/spherex
- https://caltech-ipac.github.io/irsa-tutorials/spherex-cutouts
- https://caltech-ipac.github.io/irsa-tutorials/spherex-hipscube
- https://caltech-ipac.github.io/irsa-tutorials/spherex-intro
- https://caltech-ipac.github.io/irsa-tutorials/spherex-mosaic
- https://caltech-ipac.github.io/irsa-tutorials/spherex-psf
- https://caltech-ipac.github.io/irsa-tutorials/spherex-source-discovery-tool-demo
- https://caltech-ipac.github.io/irsa-tutorials/techniques
- https://caltech-ipac.github.io/irsa-tutorials/wise
- https://caltech-ipac.github.io/spherex-archive-documentation
- https://caltech-ipac.github.io/spherex-archive-documentation/spherex-data-access
- https://caltech-ipac.github.io/spherex-archive-documentation/spherex-data-access#application-program-interfaces-apis
- https://github.com/Caltech-IPAC/irsa-tutorials/
- https://github.com/Caltech-IPAC/irsa-tutorials//edit/main/tutorials/spherex/spherex_intro.md
- https://github.com/Caltech-IPAC/irsa-tutorials/blob/main/LICENSE
- https://github.com/astropy/astropy/issues/13105
- https://irsa.ipac.caltech.edu/
- https://irsa.ipac.caltech.edu/data/SPHEREx/docs/SPHEREx_Expsupp.pdf
- https://irsa.ipac.caltech.edu/docs/help_desk.html
- https://irsa.ipac.caltech.edu/irsa-contributed-notebooks/
- https://mystmd.org/guide/deployment#deploy-base-url
- https://mystmd.org/made-with-myst
