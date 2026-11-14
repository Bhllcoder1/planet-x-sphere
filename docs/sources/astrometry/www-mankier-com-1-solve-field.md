---
source: https://www.mankier.com/1/solve-field
fetched: 2026-11-14
status: 200
---

solve-field: Main high-level command-line user interface. | Man Page | Commands | astrometry | ManKier

1. [Home](/)
2. [astrometry](/package/astrometry)

 ![Search](/img/search.svg)  [solve-field](#)

* [Synopsis](#Synopsis)
* [Description](#Description)
* [Options](#Options)
  + [The following options are valid for xylist inputs only](#Options-The_following_options_are_valid_for_xylist_inputs_only)
* [Author](#Author)
* [See Also](#See_Also)
* [Info](#Info)

[solve-field - Man Page](#)
===========================

Main high-level command-line user interface.

[Synopsis
--------](#Synopsis)

`solve-field [options] [image-file-1 image-file-2 ...] [xyls-file-1 xyls-file-2 ...]`

[Description
-----------](#Description)

Main high-level command-line user interface for astrometry.net

You can specify http:// or ftp:// URLs instead of filenames.  The "wget" or "curl" program will be used to retrieve the URL.

The astrometry engine will take any image and return the astrometry world coordinate system (WCS), ie a standards-based description of the (usually nonlinear) transformation between image coordinates and sky coordinates with absolutely no “false positives” (but maybe some “no answers”). It will do its best, even when the input image has no or totally incorrect meta data.

[Options
-------](#Options)

[-h](#-h),  [--help](#--help)
:   Print the help message

[-v](#-v),  [--verbose](#--verbose)
:   Be more chatty. Repeat for even more verboseness

[-D](#-D),  [--dir](#--dir) *directory*
:   Place all output files in the specified directory

[-o](#-o),  [--out](#--out) *file*
:   Name the output files with this base name

[-b](#-b),  [--backend-config](#--backend-config) *file*
:   Use this config file for the "astrometry-engine" program

[--config](#--config) *file*
:   Use this config file for the "astrometry-engine" program

[--batch](#--batch)
:   Run astrometry-engine once, rather than once per input file

[-f](#-f),  [--files-on-stdin](#--files-on-stdin)
:   Read filenames to solve on stdin, one per line

[-p](#-p),  [--no-plots](#--no-plots)
:   Don't create any plots of the results

[--plot-scale](#--plot-scale) *scale*
:   Scale the plots by this factor (eg, 0.25)

[--plot-bg](#--plot-bg) *file*
:   Set the background image to use for plots (JPEG)

[-G](#-G),  [--use-wget](#--use-wget)
:   Use wget instead of curl

[-O](#-O),  [--overwrite](#--overwrite)
:   Overwrite output files if they already exist

[-K](#-K),  [--continue](#--continue)
:   Don't overwrite output files if they already exist; continue a previous run

[-J](#-J),  [--skip-solved](#--skip-solved)
:   Skip input files for which the 'solved' output file already exists; NOTE: this assumes single-field input files

[--fits-image](#--fits-image)
:   assume the input files are FITS images

[-N](#-N),  [--new-fits](#--new-fits) *file*
:   Output filename of the new FITS file containing the WCS header; "none" to not create this file

[-Z](#-Z),  [--kmz](#--kmz) *file*
:   Create KMZ file for Google Sky. (requires wcs2kml)

[-i](#-i),  [--scamp](#--scamp) *file*
:   Create image object catalog for SCAMP

[-n](#-n),  [--scamp-config](#--scamp-config) *file*
:   Create SCAMP config file snippet

[-U](#-U),  [--index-xyls](#--index-xyls) *file*
:   Output filename for xylist containing the image coordinate of stars from the index

[--just-augment](#--just-augment)
:   Just write the augmented xylist files; don't run astrometry-engine.

[--axy](#--axy) *file*
:   Output filename for augment xy list (axy)

[--temp-axy](#--temp-axy)
:   Write 'augmented xy list' (axy) file to a temp file

[--timestamp](#--timestamp)
:   Add timestamps to log messages

[-7](#-7),  [--no-delete-temp](#--no-delete-temp)
:   Don't delete temp files (for debugging)

[-L](#-L),  [--scale-low](#--scale-low) *scale*
:   Lower bound of image scale estimate

[-H](#-H),  [--scale-high](#--scale-high) *scale*
:   Upper bound of image scale estimate

[-u](#-u),  [--scale-units](#--scale-units) *units*
:   In what units are the lower and upper bounds? Choices:

    "degwidth", "degw", "dw"
    :   width of the image, in degrees (default)

    "arcminwidth", "amw", "aw"
    :   width of the image, in arcminutes

    "arcsecperpix", "app"
    :   arcseconds per pixel

    "focalmm"
    :   35-mm (width-based) equivalent focal length

[-8](#-8),  [--parity](#--parity) *pos*/*neg*
:   Only check for matches with positive/negative parity (default: try both)

[-c](#-c),  [--code-tolerance](#--code-tolerance) *distance*
:   Matching distance for quads (default: 0.01)

[-E](#-E),  [--pixel-error](#--pixel-error) *pixels*
:   For verification, size of pixel positional error (default: 1)

[-q](#-q),  [--quad-size-min](#--quad-size-min) *fraction*
:   Minimum size of quads to try, as a fraction of the smaller image dimension, default: 0.1

[-Q](#-Q),  [--quad-size-max](#--quad-size-max) *fraction*
:   Maximum size of quads to try, as a fraction of the image hypotenuse, default 1.0

[--odds-to-tune-up](#--odds-to-tune-up) *odds*
:   Odds ratio at which to try tuning up a match that isn't good enough to solve (default: 1e6)

[--odds-to-solve](#--odds-to-solve) *odds*
:   Odds ratio at which to consider a field solved (default: 1e9)

[--odds-to-reject](#--odds-to-reject) *odds*
:   Odds ratio at which to reject a hypothesis (default: 1e-100)

[--odds-to-stop-looking](#--odds-to-stop-looking) *odds*
:   Odds ratio at which to stop adding stars when evaluating a hypothesis (default: HUGE\_VAL)

[--use-source-extractor](#--use-source-extractor)
:   Use Source Extractor rather than built-in image2xy to find sources

[--source-extractor-config](#--source-extractor-config) *file*
:   Use the given Source Extractor config file. Note that CATALOG\_NAME and CATALOG\_TYPE values will be over-ridden by command-line values.  This option implies **[--use-source-extractor](#--use-source-extractor)**.

[--source-extractor-path](#--source-extractor-path) *file*
:   Use the given path to the Source Extractor executable. Default: just 'source-extractor', assumed to be in your PATH. Note that you can give command line args here too (but put them in quotes), eg:

    **[--source-extractor-path](#--source-extractor-path)** 'source-extractor -DETECT\_TYPE CCD'.

    This option implies **[--use-source-extractor](#--use-source-extractor)**.

[-3](#-3) *RA*, [--ra](#--ra) *RA*
:   RA of field center for search, format: degrees or hh:mm:ss

[-4](#-4) *DEC*, [--dec](#--dec) *DEC*
:   DEC of field center for search, format: degrees or hh:mm:ss

[-5](#-5) *degrees*, [--radius](#--radius) *degrees*
:   Only search in indexes within 'radius' of the field center given by **[--ra](#--ra)** and **[--dec](#--dec)**

[-d](#-d),  [--depth](#--depth) *number* or *range*
:   Number of field objects to look at, or range of numbers; 1 is the brightest star, so "[-d](#-d) 10" or "[-d](#-d) 1-10" mean look at the top ten brightest stars only.

[--objs](#--objs) *int*
:   Cut the source list to have this many items (after sorting, if applicable).

[-l](#-l),  [--cpulimit](#--cpulimit) *seconds*
:   Give up solving after the specified number of seconds of CPU time

[-r](#-r),  [--resort](#--resort)
:   Sort the star brightnesses by background-subtracted flux; the default is to sort using acompromise between background-subtracted and non-background-subtracted flux

[-6](#-6),  [--extension](#--extension) *int*
:   FITS extension to read image from.

[--invert](#--invert)
:   Invert the image (for black-on-white images)

[-z](#-z),  [--downsample](#--downsample) *int*
:   Downsample the image by factor *int* before running source extraction

[--no-background-subtraction](#--no-background-subtraction)
:   Don't try to estimate a smoothly-varying sky background during source extraction.

[--sigma](#--sigma) *float*
:   Set the noise level in the image

[-9](#-9),  [--no-remove-lines](#--no-remove-lines)
:   Don't remove horizontal and vertical overdensities of sources.

[--uniformize](#--uniformize) *int*
:   Select sources uniformly using roughly this many boxes (0=disable; default 10)

[--no-verify-uniformize](#--no-verify-uniformize)
:   Don't uniformize the field stars during verification

[--no-verify-dedup](#--no-verify-dedup)
:   Don't deduplicate the field stars during verification

[-0](#-0),  [--no-fix-sdss](#--no-fix-sdss)
:   Don't try to fix SDSS idR files.

[-C](#-C),  [--cancel](#--cancel) *file*
:   Filename whose creation signals the process to stop

[-S](#-S),  [--solved](#--solved) *file*
:   Output file to mark that the solver succeeded

[-I](#-I),  [--solved-in](#--solved-in) *file*
:   Input filename for solved file

[-M](#-M),  [--match](#--match) *file*
:   Output filename for match file

[-R](#-R),  [--rdls](#--rdls) *file*
:   Output filename for RDLS file

[--sort-rdls](#--sort-rdls) *column*
:   Sort the RDLS file by this column; default is ascending; use "-column" to sort "column" in descending order instead.

[--tag](#--tag) *column*
:   Grab tag-along column from index into RDLS file

[--tag-all](#--tag-all)
:   Grab all tag-along columns from index into RDLS file

[-j](#-j),  [--scamp-ref](#--scamp-ref) *file*
:   Output filename for SCAMP reference catalog

[-B](#-B),  [--corr](#--corr) *file*
:   Output filename for correspondences

[-W](#-W),  [--wcs](#--wcs) *file*
:   Output filename for WCS file

[-P](#-P),  [--pnm](#--pnm) *file*
:   Save the PNM file as *file*

[-k](#-k),  [--keep-xylist](#--keep-xylist) *file*
:   Save the (unaugmented) xylist to *file*

[-A](#-A),  [--dont-augment](#--dont-augment)
:   Quit after writing the unaugmented xylist

[-V](#-V),  [--verify](#--verify) *file*
:   Try to verify an existing WCS file

[--verify-ext](#--verify-ext) *extension*
:   HDU from which to read WCS to verify; set this BEFORE **[--verify](#--verify)**

[-y](#-y),  [--no-verify](#--no-verify)
:   Ignore existing WCS headers in FITS input images

[-g](#-g),  [--guess-scale](#--guess-scale)
:   Try to guess the image scale from the FITS headers

[--crpix-center](#--crpix-center)
:   Set the WCS reference point to the image center

[--crpix-x](#--crpix-x) *pix*
:   Set the WCS reference point to the given position

[--crpix-y](#--crpix-y) *pix*
:   Set the WCS reference point to the given position

[-T](#-T),  [--no-tweak](#--no-tweak)
:   Don't fine-tune WCS by computing a SIP polynomial

[-t](#-t),  [--tweak-order](#--tweak-order) *int*
:   Polynomial order of SIP WCS corrections

[-m](#-m),  [--temp-dir](#--temp-dir) *dir*
:   Where to put temp files, default */tmp*

[### The following options are valid for xylist inputs only](#Options-The_following_options_are_valid_for_xylist_inputs_only)

[-F](#-F),  [--fields](#--fields) *number or range*
:   The FITS extension(s) to solve, inclusive

[-w](#-w),  [--width](#--width) *pixels*
:   Specify the field width

[-e](#-e),  [--height](#--height) *pixels*
:   Specify the field height

[-X](#-X),  [--x-column](#--x-column) *column-name*
:   The FITS column containing the X coordinate of the sources

[-Y](#-Y),  [--y-column](#--y-column) *column-name*
:   The FITS column containing the Y coordinate of the sources

[-s](#-s),  [--sort-column](#--sort-column) *column-name*
:   The FITS column that should be used to sort the sources

[-a](#-a),  [--sort-ascending](#--sort-ascending)
:   Sort in ascending order (smallest first); default is descending order

Note that most output files can be disabled by setting the filename to "none". (If you have a sick sense of humour and you really want to name your output file "none", you can use "./none" instead.)

[Author
------](#Author)

The Astrometry.net team. Principal investigators are David W. Hogg (NYU) and Dustin Lang (CMU).

[See Also
--------](#See_Also)

<http://astrometry.net>

[Info
----](#Info)

July 2015 0.56 astrometry.net

* [Home](/)
* [Blog](/blog/)
* [About](/about)

## Links found on page

- http://astrometry.net
- https://www.mankier.com/
- https://www.mankier.com/about
- https://www.mankier.com/blog/
- https://www.mankier.com/package/astrometry
