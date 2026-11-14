---
source: https://irsa.ipac.caltech.edu/data/SPHEREx/docs/psfhdrerr.html
fetched: 2026-11-14
status: 200
---

SPHEREx Quick Release Spectral Images PSF Extension Header Error

|  |  |
| --- | --- |
|  | SPHEREx Quick Release Spectral Images PSF Extension Header Error |

Summary of Affected Data and Impact
-----------------------------------

The original SPHEREx QR1 and QR2 data products contained an
error in the PSF header. This issue affected the stand-alone PSF
calibration product, the PSF extension in individual spectral images,
and results produced by the SPHEREx Spectrophotometry Tool.

The impact varies with source location and the variation of the
PSF across the detector. The largest discrepancies occur in two of the
detector corners and can lead to photometric errors of up to +/-5%
relative to results obtained with the correct PSF.

Correction and Updated Data Products
------------------------------------

On March 31, 2026, the affected QR2 data products and the
Spectrophotometry Tool were updated to correct this issue. Corrected
spectral image files processed with pipeline versions 6.4 through
6.5.5 can be identified by header VERSION keywords that include the
suffix "+psffix1". Files processed with pipeline version 6.5.6 and
later were not affected.

Updated versions of the stand-alone PSF
calibration products are also available at IRSA. However, the calibration reference string in the spectral image FITS headers has not been updated.

The Python notebook [Understanding
and Extracting the PSF Extension in a SPHEREx Cutout](https://caltech-ipac.github.io/irsa-tutorials/spherex-psf/) has been
updated to:

* Check the pipeline version to determine if the PSF header needs to be updated.
* Provide a function to update the header.

More information about this issue and its resolution can be found in the [SPHEREx Explanatory Supplement](SPHEREx_Expsupp_QR.pdf).

For links to SPHEREx documentation and data, see the [SPHEREx mission page](/Missions/spherex.html) at IRSA.

Description of the Original Issue
---------------------------------

The SPHEREx PSF is represented as a cube, with each plane
representing the PSF for a different zone. The zones correspond to an
11×11 grid across the detector. The PSF cube planes are stored
in order of increasing x-index across the grid, but the header
incorrectly indicates increasing y-index (see below). As a result,
software that relies on the header information to select a PSF for a
given location on the detector may retrieve the wrong PSF cube
plane. The magnitude of this error depends both on the source location
and the variation of the PSF across the detector. The error is largest
in two of the corners and can result in a photometry error of +/-5% as
compared to using the correct PSF.

The issue is illustrated below with two small 4x4 grids (16
zones). The number in each cell of the grid represents the cube
plane (*i*plane) corresponding to that zone. Note
that the actual SPHEREx PSF cubes are computed for an 11x11 grid
(121 zones).

|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| |  |  |  |  | | --- | --- | --- | --- | | 13 | 14 | 15 | 16 | | 9 | 10 | 11 | 12 | | 5 | 6 | 7 | 8 | | 1 | 2 | 3 | 4 | |  | In the actual PSF cube, the FITS plane number, from 1 to 121, corresponding to a source in the zone at **zero-indexed** grid coordinates (x,y) is   *i*plane = *y* × *n*cols + *x* + 1 where *n*cols is the number of columns in the grid. The origin of the grid coordinates (x,y) = (0,0) is in the bottom left corner of each detector, such that the (0,0) zone contains the FITS origin pixel (1,1). |

  
  

|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| |  |  |  |  | | --- | --- | --- | --- | | 4 | 8 | 12 | 16 | | 3 | 7 | 11 | 15 | | 2 | 6 | 10 | 14 | | 1 | 5 | 9 | 13 | |  | The incorrect PSF headers indicate that *i*plane = *x* × *n*cols + *y* + 1 |

## Links found on page

- https://caltech-ipac.github.io/irsa-tutorials/spherex-psf/
- https://irsa.ipac.caltech.edu/Missions/spherex.html
- https://irsa.ipac.caltech.edu/data/SPHEREx/docs/SPHEREx_Expsupp_QR.pdf
