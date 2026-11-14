---
source: https://reproject.readthedocs.io/en/stable/
fetched: 2026-11-14
status: 200
---

Image reprojection (resampling) — reproject v0.21.0

[Skip to main content](#main-content)

Back to top


`Ctrl`+`K`

[Astropy](https://astropy.org/)

* [About](#)
  + [About Astropy](https://astropy.org/about.html)
  + [Code of Conduct](https://astropy.org/code_of_conduct.html)
  + [Acknowledging & Citing](https://astropy.org/acknowledging.html)
  + [History](https://astropy.org/history.html)
* [Documentation](#)
  + [astropy](https://docs.astropy.org)
  + [asdf-astropy](https://asdf-astropy.readthedocs.io)
  + [astropy-healpix](https://astropy-healpix.readthedocs.io)
  + [astroquery](https://astroquery.readthedocs.io)
  + [ccdproc](https://ccdproc.readthedocs.io)
  + [photutils](https://photutils.readthedocs.io)
  + [regions](https://astropy-regions.readthedocs.io)
  + [reproject](https://reproject.readthedocs.io)
  + [specreduce](https://specreduce.readthedocs.io)
  + [specutils](https://specutils.readthedocs.io)
* [Get Help](https://astropy.org/help.html)
* [Contribute](https://astropy.org/contribute.html)
* [Affiliated Packages](https://astropy.org/affiliated/index.html)
* [Team](https://astropy.org/team.html)

Search
`Ctrl`+`K`

* System Settings
* Light
* Dark

Search
`Ctrl`+`K`

* [About](#)
  + [About Astropy](https://astropy.org/about.html)
  + [Code of Conduct](https://astropy.org/code_of_conduct.html)
  + [Acknowledging & Citing](https://astropy.org/acknowledging.html)
  + [History](https://astropy.org/history.html)
* [Documentation](#)
  + [astropy](https://docs.astropy.org)
  + [asdf-astropy](https://asdf-astropy.readthedocs.io)
  + [astropy-healpix](https://astropy-healpix.readthedocs.io)
  + [astroquery](https://astroquery.readthedocs.io)
  + [ccdproc](https://ccdproc.readthedocs.io)
  + [photutils](https://photutils.readthedocs.io)
  + [regions](https://astropy-regions.readthedocs.io)
  + [reproject](https://reproject.readthedocs.io)
  + [specreduce](https://specreduce.readthedocs.io)
  + [specutils](https://specutils.readthedocs.io)
* [Get Help](https://astropy.org/help.html)
* [Contribute](https://astropy.org/contribute.html)
* [Affiliated Packages](https://astropy.org/affiliated/index.html)
* [Team](https://astropy.org/team.html)

* System Settings
* Light
* Dark

[![Logo image](_static/astropy_logo_notext.svg)

reproject v0.21.0](#)

* [Installing reproject](installation.html)
* [Regular celestial images and cubes](celestial.html)
* [HEALPIX images](healpix.html)
* [HiPS (Hierarchical Progressive Surveys)](hips.html)
* [Non-celestial images/data](noncelestial.html)
* [Footprint arrays](footprints.html)
* [Combining images into mosaics](mosaicking.html)
* [Optimizing performance for single-image reprojection](performance.html)
* [Optimizing performance for mosaicking](performance_mosaicking.html)

* [reproject\_adaptive](api/reproject.reproject_adaptive.html)
* [reproject\_exact](api/reproject.reproject_exact.html)
* [reproject\_from\_healpix](api/reproject.reproject_from_healpix.html)
* [reproject\_interp](api/reproject.reproject_interp.html)
* [reproject\_to\_healpix](api/reproject.reproject_to_healpix.html)

* [coadd\_hips](api/reproject.hips.coadd_hips.html)
* [hips\_as\_dask\_array](api/reproject.hips.hips_as_dask_array.html)
* [reproject\_from\_hips](api/reproject.hips.reproject_from_hips.html)
* [reproject\_to\_hips](api/reproject.hips.reproject_to_hips.html)

* [find\_optimal\_celestial\_wcs](api/reproject.mosaicking.find_optimal_celestial_wcs.html)
* [reproject\_and\_coadd](api/reproject.mosaicking.reproject_and_coadd.html)

Image reprojection (resampling)[#](#image-reprojection-resampling "Link to this heading")
=========================================================================================

Introduction[#](#introduction "Link to this heading")
-----------------------------------------------------

The *reproject* package implements image reprojection (resampling) methods
for astronomical images and more generally n-dimensional data. These assume
that the WCS information contained in the data are correct. This package does
**not** do image registration, which is the process of aligning images where
one or more images may have incorrect or missing WCS.

You can install *reproject* with [pip](http://www.pip-installer.org/en/latest/):

```
pip install reproject

```

or with [conda](https://continuum.io/):

```
conda install -c conda-forge reproject

```

More detailed installation instructions can be found in [Installing reproject](installation.html#installation).

Quick start[#](#quick-start "Link to this heading")
---------------------------------------------------

A common use case is that you have two FITS images, and want to reproject one
to the same header as the other. This can easily be done with the *reproject*
package, and we demonstrate this in the following example. We start off by
downloading two example images from <http://data.astropy.org>,
namely a 2MASS K-band image and an MSX band E image of the Galactic center:

```
from astropy.io import fits
from astropy.utils.data import get_pkg_data_filename
hdu1 = fits.open(get_pkg_data_filename('galactic_center/gc_2mass_k.fits'))[0]
hdu2 = fits.open(get_pkg_data_filename('galactic_center/gc_msx_e.fits'))[0]

```

We can examine the two images (this makes use of the
[wcsaxes](wcsaxes.readthedocs.io) package behind the scenes):

```
from astropy.wcs import WCS
import matplotlib.pyplot as plt

ax1 = plt.subplot(1,2,1, projection=WCS(hdu1.header))
ax1.imshow(hdu1.data, origin='lower', vmin=-100., vmax=2000.)
ax1.coords['ra'].set_axislabel('Right Ascension')
ax1.coords['dec'].set_axislabel('Declination')
ax1.set_title('2MASS K-band')

ax2 = plt.subplot(1,2,2, projection=WCS(hdu2.header))
ax2.imshow(hdu2.data, origin='lower', vmin=-2.e-4, vmax=5.e-4)
ax2.coords['glon'].set_axislabel('Galactic Longitude')
ax2.coords['glat'].set_axislabel('Galactic Latitude')
ax2.coords['glat'].set_axislabel_position('r')
ax2.coords['glat'].set_ticklabel_position('r')
ax2.set_title('MSX band E')

```

([`png`](_downloads/b99d8cdf078cd7abe42e329ff60021fa/index-2.png), [`svg`](_downloads/b8baeb3fd88aa34c4e7e7869775cb3ff/index-2.svg), [`pdf`](_downloads/7470fd799a96a2505da9a04873717e2c/index-2.pdf))

![_images/index-2.png](_images/index-2.png)

We now reproject the MSX image to be in the same projection as the 2MASS image:

```
from reproject import reproject_interp
array, footprint = reproject_interp(hdu2, hdu1.header)

```

The [`reproject_interp()`](api/reproject.reproject_interp.html#reproject.reproject_interp "reproject.reproject_interp") function above returns the
reprojected array as well as an array that provides information on the
footprint of the first image in the new reprojected image plane (essentially
which pixels in the new image had a corresponding pixel in the old image). We
can now visualize the reprojected data and footprint:

```
from astropy.wcs import WCS
import matplotlib.pyplot as plt

ax1 = plt.subplot(1,2,1, projection=WCS(hdu1.header))
ax1.imshow(array, origin='lower', vmin=-2.e-4, vmax=5.e-4)
ax1.coords['ra'].set_axislabel('Right Ascension')
ax1.coords['dec'].set_axislabel('Declination')
ax1.set_title('Reprojected MSX band E image')

ax2 = plt.subplot(1,2,2, projection=WCS(hdu1.header))
ax2.imshow(footprint, origin='lower', vmin=0, vmax=1.5)
ax2.coords['ra'].set_axislabel('Right Ascension')
ax2.coords['dec'].set_axislabel('Declination')
ax2.coords['dec'].set_axislabel_position('r')
ax2.coords['dec'].set_ticklabel_position('r')
ax2.set_title('MSX band E image footprint')

```

([`png`](_downloads/e73bacc672beca00a83b9e40c525ebf4/index-4.png), [`svg`](_downloads/15c8b38d58b2cc032bf85b03f2be5759/index-4.svg), [`pdf`](_downloads/6f73112476127a2b292493c3e7ad02c8/index-4.pdf))

![_images/index-4.png](_images/index-4.png)

We can then write out the image to a new FITS file. Note that, as for
plotting, we can use the header from the 2MASS image since both images are
now in the same projection:

```
fits.writeto('msx_on_2mass_header.fits', array, hdu1.header, overwrite=True)

```

Separately, using the [`reproject_interp()`](api/reproject.reproject_interp.html#reproject.reproject_interp "reproject.reproject_interp") together with the
[`find_optimal_celestial_wcs()`](api/reproject.mosaicking.find_optimal_celestial_wcs.html#reproject.mosaicking.find_optimal_celestial_wcs "reproject.mosaicking.find_optimal_celestial_wcs") function, we could rotate
an image to align it such that North is up:

```
from reproject.mosaicking import find_optimal_celestial_wcs

# obtain the projection for a north-aligned image
wcs_out, shape_out = find_optimal_celestial_wcs(hdu1)
# reproject the image to be north-aligned
array_north_aligned, _ = reproject_interp(hdu1, wcs_out, shape_out=shape_out)

```

The *reproject* package supports a number of different algorithms for
reprojection (interpolation, flux-conserving reprojection, etc.) and
different types of data (images, spectral cubes, HEALPIX images, etc.). For
more information, we encourage you to read the full documentation below!

Documentation[#](#documentation "Link to this heading")
-------------------------------------------------------

The reproject package consists of a few high-level functions to do
reprojection using different algorithms, which depend on the type of data
that you want to reproject.

* [Installing reproject](installation.html)
  + [Requirements](installation.html#requirements)
  + [Installation](installation.html#id1)
* [Regular celestial images and cubes](celestial.html)
  + [Common options](celestial.html#common-options)
  + [Interpolation](celestial.html#interpolation)
  + [Adaptive resampling](celestial.html#adaptive-resampling)
  + [Spherical Polygon Intersection](celestial.html#spherical-polygon-intersection)
* [HEALPIX images](healpix.html)
* [HiPS (Hierarchical Progressive Surveys)](hips.html)
  + [Getting started](hips.html#getting-started)
  + [Available options](hips.html#available-options)
  + [Generating HiPS3D datasets](hips.html#generating-hips3d-datasets)
* [Non-celestial images/data](noncelestial.html)
* [Footprint arrays](footprints.html)
* [Combining images into mosaics](mosaicking.html)
  + [Computing an optimal WCS](mosaicking.html#computing-an-optimal-wcs)
  + [Reprojecting and co-adding images into a mosaic](mosaicking.html#reprojecting-and-co-adding-images-into-a-mosaic)
* [Optimizing performance for single-image reprojection](performance.html)
  + [Disabling coordinate transformation round-tripping](performance.html#disabling-coordinate-transformation-round-tripping)
  + [Disabling returning the footprint](performance.html#disabling-returning-the-footprint)
  + [Using memory-mapped output arrays](performance.html#using-memory-mapped-output-arrays)
  + [Multiple images with the same coordinates](performance.html#multiple-images-with-the-same-coordinates)
  + [Chunk by chunk reprojection](performance.html#chunk-by-chunk-reprojection)
  + [Multi-threaded reprojection](performance.html#multi-threaded-reprojection)
  + [Input dask arrays](performance.html#input-dask-arrays)
  + [Output dask arrays](performance.html#output-dask-arrays)
  + [Using dask.distributed](performance.html#using-dask-distributed)
* [Optimizing performance for mosaicking](performance_mosaicking.html)
  + [Using memory-mapped output arrays](performance_mosaicking.html#using-memory-mapped-output-arrays)
  + [Using memory-mapped intermediate arrays](performance_mosaicking.html#using-memory-mapped-intermediate-arrays)
  + [Multi-threading](performance_mosaicking.html#multi-threading)
  + [Using dask.distributed](performance_mosaicking.html#using-dask-distributed)

Reference/API[#](#reference-api "Link to this heading")
-------------------------------------------------------

### reproject Package[#](#module-reproject "Link to this heading")

Astropy affiliated package for image reprojection (resampling).

#### Functions[#](#functions "Link to this heading")

|  |  |
| --- | --- |
| [`reproject_adaptive`](api/reproject.reproject_adaptive.html#reproject.reproject_adaptive "reproject.reproject_adaptive")(input\_data, output\_projection) | Reproject a 2D array from one WCS to another using the DeForest (2004) adaptive, anti-aliased resampling algorithm, with optional flux conservation. |
| [`reproject_exact`](api/reproject.reproject_exact.html#reproject.reproject_exact "reproject.reproject_exact")(input\_data, output\_projection) | Reproject data to a new projection using flux-conserving spherical polygon intersection (this is the slowest algorithm). |
| [`reproject_from_healpix`](api/reproject.reproject_from_healpix.html#reproject.reproject_from_healpix "reproject.reproject_from_healpix")(input\_data, ...[, ...]) | Reproject data from a HEALPIX projection to a standard projection. |
| [`reproject_interp`](api/reproject.reproject_interp.html#reproject.reproject_interp "reproject.reproject_interp")(input\_data, output\_projection) | Reproject data to a new projection using interpolation (this is typically the fastest way to reproject an image). |
| [`reproject_to_healpix`](api/reproject.reproject_to_healpix.html#reproject.reproject_to_healpix "reproject.reproject_to_healpix")(input\_data, ...[, ...]) | Reproject data from a standard projection to a HEALPIX projection. |

### reproject.hips Package[#](#module-reproject.hips "Link to this heading")

#### Functions[#](#id1 "Link to this heading")

|  |  |
| --- | --- |
| [`coadd_hips`](api/reproject.hips.coadd_hips.html#reproject.hips.coadd_hips "reproject.hips.coadd_hips")(input\_directories, output\_directory) | Given multiple HiPS directories, combine these into a single HiPS. |
| [`hips_as_dask_array`](api/reproject.hips.hips_as_dask_array.html#reproject.hips.hips_as_dask_array "reproject.hips.hips_as_dask_array")(directory\_or\_url, \*[, level]) | Return a dask array and WCS that represent a HiPS dataset at a particular level. |
| [`reproject_from_hips`](api/reproject.hips.reproject_from_hips.html#reproject.hips.reproject_from_hips "reproject.hips.reproject_from_hips")() |  |
| [`reproject_to_hips`](api/reproject.hips.reproject_to_hips.html#reproject.hips.reproject_to_hips "reproject.hips.reproject_to_hips")(input\_data, \*, ...[, ...]) | Reproject data from a standard projection to a set of Hierarchical Progressive Surveys (HiPS) tiles. |

### reproject.mosaicking Package[#](#module-reproject.mosaicking "Link to this heading")

#### Functions[#](#id2 "Link to this heading")

|  |  |
| --- | --- |
| [`find_optimal_celestial_wcs`](api/reproject.mosaicking.find_optimal_celestial_wcs.html#reproject.mosaicking.find_optimal_celestial_wcs "reproject.mosaicking.find_optimal_celestial_wcs")(input\_data[, ...]) | Given one or more images, return an optimal WCS projection object and shape. |
| [`reproject_and_coadd`](api/reproject.mosaicking.reproject_and_coadd.html#reproject.mosaicking.reproject_and_coadd "reproject.mosaicking.reproject_and_coadd")(input\_data, ...[, ...]) | Given a set of input data, reproject and co-add these to a single final image. |

[next

Installing reproject](installation.html "next page")

On this page

* [Introduction](#introduction)
* [Quick start](#quick-start)
* [Documentation](#documentation)
* [Reference/API](#reference-api)
  + [reproject Package](#module-reproject)
    - [Functions](#functions)
  + [reproject.hips Package](#module-reproject.hips)
    - [Functions](#id1)
  + [reproject.mosaicking Package](#module-reproject.mosaicking)
    - [Functions](#id2)

© Copyright 2026, Thomas Robitaille, Christoph Deil, Adam Ginsburg, Stuart Mumford, Sam Van Kooten.

[Code of Conduct](https://astropy.org/code_of_conduct.html)

Updated on 25 Jun 2026
, built with [Sphinx
9.0.4](http://sphinx-doc.org/)

## Links found on page

- http://data.astropy.org
- http://sphinx-doc.org/
- http://www.pip-installer.org/en/latest/
- https://asdf-astropy.readthedocs.io
- https://astropy-healpix.readthedocs.io
- https://astropy-regions.readthedocs.io
- https://astropy.org/
- https://astropy.org/about.html
- https://astropy.org/acknowledging.html
- https://astropy.org/affiliated/index.html
- https://astropy.org/code_of_conduct.html
- https://astropy.org/contribute.html
- https://astropy.org/help.html
- https://astropy.org/history.html
- https://astropy.org/team.html
- https://astroquery.readthedocs.io
- https://ccdproc.readthedocs.io
- https://continuum.io/
- https://docs.astropy.org
- https://docs.astropy.org/projects/reproject/en/stable/_downloads/15c8b38d58b2cc032bf85b03f2be5759/index-4.svg
- https://docs.astropy.org/projects/reproject/en/stable/_downloads/6f73112476127a2b292493c3e7ad02c8/index-4.pdf
- https://docs.astropy.org/projects/reproject/en/stable/_downloads/7470fd799a96a2505da9a04873717e2c/index-2.pdf
- https://docs.astropy.org/projects/reproject/en/stable/_downloads/b8baeb3fd88aa34c4e7e7869775cb3ff/index-2.svg
- https://docs.astropy.org/projects/reproject/en/stable/_downloads/b99d8cdf078cd7abe42e329ff60021fa/index-2.png
- https://docs.astropy.org/projects/reproject/en/stable/_downloads/e73bacc672beca00a83b9e40c525ebf4/index-4.png
- https://docs.astropy.org/projects/reproject/en/stable/api/reproject.hips.coadd_hips.html
- https://docs.astropy.org/projects/reproject/en/stable/api/reproject.hips.coadd_hips.html#reproject.hips.coadd_hips
- https://docs.astropy.org/projects/reproject/en/stable/api/reproject.hips.hips_as_dask_array.html
- https://docs.astropy.org/projects/reproject/en/stable/api/reproject.hips.hips_as_dask_array.html#reproject.hips.hips_as_dask_array
- https://docs.astropy.org/projects/reproject/en/stable/api/reproject.hips.reproject_from_hips.html
- https://docs.astropy.org/projects/reproject/en/stable/api/reproject.hips.reproject_from_hips.html#reproject.hips.reproject_from_hips
- https://docs.astropy.org/projects/reproject/en/stable/api/reproject.hips.reproject_to_hips.html
- https://docs.astropy.org/projects/reproject/en/stable/api/reproject.hips.reproject_to_hips.html#reproject.hips.reproject_to_hips
- https://docs.astropy.org/projects/reproject/en/stable/api/reproject.mosaicking.find_optimal_celestial_wcs.html
- https://docs.astropy.org/projects/reproject/en/stable/api/reproject.mosaicking.find_optimal_celestial_wcs.html#reproject.mosaicking.find_optimal_celestial_wcs
- https://docs.astropy.org/projects/reproject/en/stable/api/reproject.mosaicking.reproject_and_coadd.html
- https://docs.astropy.org/projects/reproject/en/stable/api/reproject.mosaicking.reproject_and_coadd.html#reproject.mosaicking.reproject_and_coadd
- https://docs.astropy.org/projects/reproject/en/stable/api/reproject.reproject_adaptive.html
- https://docs.astropy.org/projects/reproject/en/stable/api/reproject.reproject_adaptive.html#reproject.reproject_adaptive
- https://docs.astropy.org/projects/reproject/en/stable/api/reproject.reproject_exact.html
- https://docs.astropy.org/projects/reproject/en/stable/api/reproject.reproject_exact.html#reproject.reproject_exact
- https://docs.astropy.org/projects/reproject/en/stable/api/reproject.reproject_from_healpix.html
- https://docs.astropy.org/projects/reproject/en/stable/api/reproject.reproject_from_healpix.html#reproject.reproject_from_healpix
- https://docs.astropy.org/projects/reproject/en/stable/api/reproject.reproject_interp.html
- https://docs.astropy.org/projects/reproject/en/stable/api/reproject.reproject_interp.html#reproject.reproject_interp
- https://docs.astropy.org/projects/reproject/en/stable/api/reproject.reproject_to_healpix.html
- https://docs.astropy.org/projects/reproject/en/stable/api/reproject.reproject_to_healpix.html#reproject.reproject_to_healpix
- https://docs.astropy.org/projects/reproject/en/stable/celestial.html
- https://docs.astropy.org/projects/reproject/en/stable/celestial.html#adaptive-resampling
- https://docs.astropy.org/projects/reproject/en/stable/celestial.html#common-options
- https://docs.astropy.org/projects/reproject/en/stable/celestial.html#interpolation
- https://docs.astropy.org/projects/reproject/en/stable/celestial.html#spherical-polygon-intersection
- https://docs.astropy.org/projects/reproject/en/stable/footprints.html
- https://docs.astropy.org/projects/reproject/en/stable/healpix.html
- https://docs.astropy.org/projects/reproject/en/stable/hips.html
- https://docs.astropy.org/projects/reproject/en/stable/hips.html#available-options
- https://docs.astropy.org/projects/reproject/en/stable/hips.html#generating-hips3d-datasets
- https://docs.astropy.org/projects/reproject/en/stable/hips.html#getting-started
- https://docs.astropy.org/projects/reproject/en/stable/installation.html
- https://docs.astropy.org/projects/reproject/en/stable/installation.html#id1
- https://docs.astropy.org/projects/reproject/en/stable/installation.html#installation
- https://docs.astropy.org/projects/reproject/en/stable/installation.html#requirements
- https://docs.astropy.org/projects/reproject/en/stable/mosaicking.html
- https://docs.astropy.org/projects/reproject/en/stable/mosaicking.html#computing-an-optimal-wcs
- https://docs.astropy.org/projects/reproject/en/stable/mosaicking.html#reprojecting-and-co-adding-images-into-a-mosaic
- https://docs.astropy.org/projects/reproject/en/stable/noncelestial.html
- https://docs.astropy.org/projects/reproject/en/stable/performance.html
- https://docs.astropy.org/projects/reproject/en/stable/performance.html#chunk-by-chunk-reprojection
- https://docs.astropy.org/projects/reproject/en/stable/performance.html#disabling-coordinate-transformation-round-tripping
- https://docs.astropy.org/projects/reproject/en/stable/performance.html#disabling-returning-the-footprint
- https://docs.astropy.org/projects/reproject/en/stable/performance.html#input-dask-arrays
- https://docs.astropy.org/projects/reproject/en/stable/performance.html#multi-threaded-reprojection
- https://docs.astropy.org/projects/reproject/en/stable/performance.html#multiple-images-with-the-same-coordinates
- https://docs.astropy.org/projects/reproject/en/stable/performance.html#output-dask-arrays
- https://docs.astropy.org/projects/reproject/en/stable/performance.html#using-dask-distributed
- https://docs.astropy.org/projects/reproject/en/stable/performance.html#using-memory-mapped-output-arrays
- https://docs.astropy.org/projects/reproject/en/stable/performance_mosaicking.html
- https://docs.astropy.org/projects/reproject/en/stable/performance_mosaicking.html#multi-threading
- https://docs.astropy.org/projects/reproject/en/stable/performance_mosaicking.html#using-dask-distributed
- https://docs.astropy.org/projects/reproject/en/stable/performance_mosaicking.html#using-memory-mapped-intermediate-arrays
- https://docs.astropy.org/projects/reproject/en/stable/performance_mosaicking.html#using-memory-mapped-output-arrays
- https://docs.astropy.org/projects/reproject/en/stable/wcsaxes.readthedocs.io
- https://photutils.readthedocs.io
- https://reproject.readthedocs.io
- https://specreduce.readthedocs.io
- https://specutils.readthedocs.io
