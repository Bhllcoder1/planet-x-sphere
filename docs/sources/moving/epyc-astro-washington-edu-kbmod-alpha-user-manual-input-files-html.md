---
source: https://epyc.astro.washington.edu/~kbmod/alpha/user_manual/input_files.html
fetched: 2026-11-14
status: 200
---

Input Files — KBMOD 0.1.dev1+g0529894 documentation
[Skip to main content](#main-content)



`Ctrl`+`K`

[![Logo image](../_static/kbmod.svg)](../index.html)

Site Navigation

* [User Manual](index.html)
* [Examples](../examples/index.html)
* [API Reference](../api_reference/index.html)
* [For Developers](../project_details/index.html)

Site Navigation

* [User Manual](index.html)
* [Examples](../examples/index.html)
* [API Reference](../api_reference/index.html)
* [For Developers](../project_details/index.html)

Section Navigation

* [Input Files](#)
* [Search Algorithm and Search Space](search_space.html)
* [Masking](masking.html)
* [Search Parameters](search_params.html)
* [Output Files](output_files.html)
* [Results analysis](results_filtering.html)

* [User Manual](index.html)
* Input Files

Input Files[#](#input-files "Permalink to this heading")
========================================================

KBMOD expects Vera C. Rubin Science Pipelines calexp-style FITS files. These are multi-extension fits files that contain:

* photometrically and astometrically calibrated single-CCD image, usually refered to as the “science image”,
* variance image, representing per-pixel noise levels, and a
* pixel bitmask

stored in 1st, 2nd and 3rd header extension/plane respectively. The zeroth header extension is expected to contain the image metadata. A collection of science images that overlap the same area on the sky at different times are expected to be grouped into directories, usually refered to as “pointing groups”. The path to this directory is a required input to KBMOD, see [Search Parameters](search_params.html#search-parameters).

The images are expected to be warped, i.e. geometrically transformed to a set of images with a consistent and uniform relationship between sky coordinates and image pixels on a shared pixel grid.

Visit ID[#](#visit-id "Permalink to this heading")
--------------------------------------------------

In order to associate input files with auxiliary data, such as time stamps or PSFs, each visit uses a unique numeric ID. This ID string can be provided in the `IDNUM` field of the FITS file’s header 0. If no `IDNUM` field is provided, then KBMOD will attempt to derive the visit ID from the file name as described in the next section.

Naming Scheme[#](#naming-scheme "Permalink to this heading")
------------------------------------------------------------

Each file **must** include `.fits` somewhere in the file name. Additionally the file names can be used to encode the visit ID. If no `IDNUM` field is provided, KBMOD will look for a contiguous sequence of five or more numeric digits in the file name. If found, the first such sequence is used as the visit ID. For example a file name “my12345.fits” will map to the visit ID “12345”.

Time file[#](#time-file "Permalink to this heading")
----------------------------------------------------

There are two cases where you would want to use an external time file:

* when the FITS files do not contain timestamp information
  :   If no file is included, KBMOD will attempt to extract the timestamp from the FITS file header (in the MJD field).
* when you want to prefilter the files based on the parameter `mjd_lims` (see [Search Parameters](search_params.html#search-parameters)) before loading the file.
  :   This reduces loading time when accessing a large directory.

The time file provides a mapping of visit ID to timestamp. The time file is an ASCII text file containing two space-separated columns of data: the visit IDs and MJD time of the observation. The first line is a header denoted by `#`:

```
# visit_id mean_julian_date
439116 57162.42540605324
439120 57162.42863899306
439124 57162.43279313658
439128 57162.436995358796
439707 57163.41836675926
439711 57163.421717488425

```

PSF File[#](#psf-file "Permalink to this heading")
--------------------------------------------------

The PSF file is an ASCII text file containing two space-separated columns of data: the visit IDs and variance of the PSF for the corresponding observation. The first line is a header denoted by `#`:

```
# visit_id psf_val
439116 1.1
439120 1.05
439124 1.4

```

A PSF file is needed whenever you do not want to use the same default value for every image.

Data Loading[#](#data-loading "Permalink to this heading")
----------------------------------------------------------

Data is loaded using [`load_images()`](../api_reference/analysis_utils.html#kbmod.analysis_utils.Interface.load_images "kbmod.analysis_utils.Interface.load_images"). The method creates an `ImageStack` object, which is a collection of `LayeredImage` objects. Each `LayeredImage` contains the PSF, mask and the science image while `ImageStack` tracks the properties that apply to all images in the collection, such as global masks etc. The `ImageStack` will include only those images that with observation timestamps within the given MJD bounds.

The [`load_images()`](../api_reference/analysis_utils.html#kbmod.analysis_utils.Interface.load_images "kbmod.analysis_utils.Interface.load_images") method also returns helper information:
:   * `img_info` - An object containing auxiliary data from the fits files such as their WCS and the location of the observatory.

[previous

User Manual](index.html "previous page")
[next

Search Algorithm and Search Space](search_space.html "next page")

On this page

* [Visit ID](#visit-id)
* [Naming Scheme](#naming-scheme)
* [Time file](#time-file)
* [PSF File](#psf-file)
* [Data Loading](#data-loading)

[Show Source](../_sources/user_manual/input_files.rst.txt)

© Copyright 2023, KBMOD Developers.

Created using [Sphinx](https://sphinx-doc.org/) 5.3.0.

Built with the [PyData Sphinx Theme](https://pydata-sphinx-theme.readthedocs.io/en/stable/index.html) 0.13.0.

## Links found on page

- https://epyc.astro.washington.edu/~kbmod/alpha/_sources/user_manual/input_files.rst.txt
- https://epyc.astro.washington.edu/~kbmod/alpha/api_reference/analysis_utils.html#kbmod.analysis_utils.Interface.load_images
- https://epyc.astro.washington.edu/~kbmod/alpha/api_reference/index.html
- https://epyc.astro.washington.edu/~kbmod/alpha/examples/index.html
- https://epyc.astro.washington.edu/~kbmod/alpha/index.html
- https://epyc.astro.washington.edu/~kbmod/alpha/project_details/index.html
- https://epyc.astro.washington.edu/~kbmod/alpha/user_manual/index.html
- https://epyc.astro.washington.edu/~kbmod/alpha/user_manual/masking.html
- https://epyc.astro.washington.edu/~kbmod/alpha/user_manual/output_files.html
- https://epyc.astro.washington.edu/~kbmod/alpha/user_manual/results_filtering.html
- https://epyc.astro.washington.edu/~kbmod/alpha/user_manual/search_params.html
- https://epyc.astro.washington.edu/~kbmod/alpha/user_manual/search_params.html#search-parameters
- https://epyc.astro.washington.edu/~kbmod/alpha/user_manual/search_space.html
- https://pydata-sphinx-theme.readthedocs.io/en/stable/index.html
- https://sphinx-doc.org/
