---
source: https://irsa.ipac.caltech.edu/data/SPHEREx/docs/spherex_spectral_calibrations.html
fetched: 2026-11-14
status: 200
---

SPHEREx Spectral Calibrations

|  |  |
| --- | --- |
|  | SPHEREx Spectral Calibrations |

This page provides SPHEREx spectral calibration products derived from
laboratory measurements. The calibration products are delivered at
four spectral granularities of 17, 34, 51, and 68 sub-channels per
detector. The products include normalized spectral response functions,
also referred to here as transmission curves.

The spectral calibration products are provided as a
[tar file](/data/SPHEREx/docs/spectral_files_20260812/SPHERExSpectralFiles_202607.tar). The package includes separate
subdirectories for each product type:

* `ChannelMaps/` contains FITS files describing the
  spectral-channel assignments for each detector.
* `MiddlePixel/` and `MeanAllPixel/` contain
  CSV files with the spectral response functions organized by
  sub-channel resolution (`SubChannel17, 34, 51, or 68`)
  and detector band (`Band1-Band6`).
* `FidSecSummary/` provides per-channel summary CSV
  files including the central wavelength of each channel.
* `ParameterFiles/` contains FITS maps of band-center
  and band-width parameters.

See the
[detailed spectral
calibration documentation](SPHERExSpectralFiles_202607.pdf) for additional information about the
calibration products, channel definitions, and file organization. A
brief summary of the transmission curves is provided below.
Note that these files are provided in detector coordinates and therefore are flipped in the x-axis - compare to the on-sky images for detectors 4, 5 and 6.

Transmission Curves
-------------------

While the transmission was measured for all pixels in lab testing,
the products available here include averaged transmission curves in
nominal SPHEREx channels, at four channel resolutions, derived from
the per-pixel measurements.

For each spectral channel, two representative normalized spectral response
functions, or transmission curves, are provided:

* **Middle-pixel response (Cent):** Represents the
  average transmission of pixels landing at the (spectral) center of
  the channel.
* **All-pixel response (Allpix):** Represents the
  average of the measured transmissions of all pixels belonging to the
  channel.

The appropriate response depends on the analysis. The middle-pixel response
is generally more representative of an individual measurement. The all-pixel
response may be more appropriate when measurements obtained at different
positions within a spectral channel are themselves combined or averaged.
For example, if multiple measurements of a deep-field source within a channel
are averaged into a single measurement, the corresponding individual
transmission curves sample slightly different central wavelengths; the
all-pixel response provides a similarly averaged representation of the
channel response.

Related Pipeline Calibration Products
-------------------------------------

These spectral calibration products are provided primarily for users who want
direct access to the underlying laboratory-derived calibration measurements.
Most are not calibration products used directly by the SPHEREx data-processing
pipeline.

Calibration products used by the SPHEREx processing pipeline are available
separately at IRSA:
[SPHEREx pipeline calibration products](https://caltech-ipac.github.io/spherex-archive-documentation/spherex-data-products/).

## Links found on page

- https://caltech-ipac.github.io/spherex-archive-documentation/spherex-data-products/
- https://irsa.ipac.caltech.edu/data/SPHEREx/docs/SPHERExSpectralFiles_202607.pdf
- https://irsa.ipac.caltech.edu/data/SPHEREx/docs/spectral_files_20260812/SPHERExSpectralFiles_202607.tar
