---
source: https://docs.astropy.org/projects/photutils/en/stable/user_guide/detection.html
fetched: 2026-11-14
status: 200
---

Point-like Source Detection (photutils.detection) — photutils 3.1.1

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

* [GitHub](https://github.com/astropy/photutils "GitHub")

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

* [GitHub](https://github.com/astropy/photutils "GitHub")

[![Logo image](../_static/photutils_logo_light_plain_path.svg)

photutils 3.1.1](../index.html)

* [Getting Started](../getting_started/index.html)
  + [Installation](../getting_started/install.html)
  + [Overview](../getting_started/overview.html)
  + [Importing from Photutils](../getting_started/importing.html)
  + [Pixel Coordinate Conventions](../getting_started/pixel_conventions.html)
  + [Performance Tips](../getting_started/performance_tips.html)
  + [Citing Photutils](../getting_started/citation.html)
* [User Guide](index.html)
  + [Background Estimation (`photutils.background`)](background.html)
  + [Centroids (`photutils.centroids`)](centroids.html)
  + [Point-like Source Detection (`photutils.detection`)](#)
  + [Image Segmentation (`photutils.segmentation`)](segmentation.html)
  + [Morphological Properties (`photutils.morphology`)](morphology.html)
  + [Aperture Photometry (`photutils.aperture`)](aperture.html)
  + [PSF Photometry (`photutils.psf`)](psf.html)
  + [Building an Effective Point Spread Function (ePSF)](epsf_building.html)
  + [Source Grouping](grouping.html)
  + [PSF Matching (`photutils.psf_matching`)](psf_matching.html)
  + [Radial Profiles (`photutils.profiles`)](radial_profiles.html)
  + [Curves of Growth (`photutils.profiles`)](curves_of_growth.html)
  + [Elliptical Isophote Analysis (`photutils.isophote`)](isophote.html)
    - [Isophote Frequently Asked Questions](isophote_faq.html)
  + [Datasets and Simulation (`photutils.datasets`)](datasets.html)
  + [ASDF Serialization](asdf.html)
  + [Utility Functions (`photutils.utils`)](utils.html)
  + [Geometry Functions (`photutils.geometry`)](geometry.html)
* [API Reference Guide](../reference/index.html)
  + [Aperture Photometry (`photutils.aperture`)](../reference/aperture_api.html)
    - [aperture\_photometry](../api/photutils.aperture.aperture_photometry.html)
    - [aperture\_to\_region](../api/photutils.aperture.aperture_to_region.html)
    - [decode\_aperture\_flags](../api/photutils.aperture.decode_aperture_flags.html)
    - [region\_to\_aperture](../api/photutils.aperture.region_to_aperture.html)
    - [Aperture](../api/photutils.aperture.Aperture.html)
    - [ApertureMask](../api/photutils.aperture.ApertureMask.html)
    - [AperturePhotometry](../api/photutils.aperture.AperturePhotometry.html)
    - [ApertureStats](../api/photutils.aperture.ApertureStats.html)
    - [BoundingBox](../api/photutils.aperture.BoundingBox.html)
    - [CircularAnnulus](../api/photutils.aperture.CircularAnnulus.html)
    - [CircularAperture](../api/photutils.aperture.CircularAperture.html)
    - [CircularMaskMixin](../api/photutils.aperture.CircularMaskMixin.html)
    - [EllipticalAnnulus](../api/photutils.aperture.EllipticalAnnulus.html)
    - [EllipticalAperture](../api/photutils.aperture.EllipticalAperture.html)
    - [EllipticalMaskMixin](../api/photutils.aperture.EllipticalMaskMixin.html)
    - [PixelAperture](../api/photutils.aperture.PixelAperture.html)
    - [PolygonAperture](../api/photutils.aperture.PolygonAperture.html)
    - [RectangularAnnulus](../api/photutils.aperture.RectangularAnnulus.html)
    - [RectangularAperture](../api/photutils.aperture.RectangularAperture.html)
    - [RectangularMaskMixin](../api/photutils.aperture.RectangularMaskMixin.html)
    - [SkyAperture](../api/photutils.aperture.SkyAperture.html)
    - [SkyCircularAnnulus](../api/photutils.aperture.SkyCircularAnnulus.html)
    - [SkyCircularAperture](../api/photutils.aperture.SkyCircularAperture.html)
    - [SkyEllipticalAnnulus](../api/photutils.aperture.SkyEllipticalAnnulus.html)
    - [SkyEllipticalAperture](../api/photutils.aperture.SkyEllipticalAperture.html)
    - [SkyPolygonAperture](../api/photutils.aperture.SkyPolygonAperture.html)
    - [SkyRectangularAnnulus](../api/photutils.aperture.SkyRectangularAnnulus.html)
    - [SkyRectangularAperture](../api/photutils.aperture.SkyRectangularAperture.html)
  + [Backgrounds (`photutils.background`)](../reference/background_api.html)
    - [Background2D](../api/photutils.background.Background2D.html)
    - [BackgroundBase](../api/photutils.background.BackgroundBase.html)
    - [BackgroundRMSBase](../api/photutils.background.BackgroundRMSBase.html)
    - [BiweightLocationBackground](../api/photutils.background.BiweightLocationBackground.html)
    - [BiweightScaleBackgroundRMS](../api/photutils.background.BiweightScaleBackgroundRMS.html)
    - [BkgIDWInterpolator](../api/photutils.background.BkgIDWInterpolator.html)
    - [BkgZoomInterpolator](../api/photutils.background.BkgZoomInterpolator.html)
    - [LocalBackground](../api/photutils.background.LocalBackground.html)
    - [MADStdBackgroundRMS](../api/photutils.background.MADStdBackgroundRMS.html)
    - [MMMBackground](../api/photutils.background.MMMBackground.html)
    - [MeanBackground](../api/photutils.background.MeanBackground.html)
    - [MedianBackground](../api/photutils.background.MedianBackground.html)
    - [ModeEstimatorBackground](../api/photutils.background.ModeEstimatorBackground.html)
    - [SExtractorBackground](../api/photutils.background.SExtractorBackground.html)
    - [StdBackgroundRMS](../api/photutils.background.StdBackgroundRMS.html)
  + [Centroids (`photutils.centroids`)](../reference/centroids_api.html)
    - [centroid\_1dg](../api/photutils.centroids.centroid_1dg.html)
    - [centroid\_2dg](../api/photutils.centroids.centroid_2dg.html)
    - [centroid\_com](../api/photutils.centroids.centroid_com.html)
    - [centroid\_quadratic](../api/photutils.centroids.centroid_quadratic.html)
    - [centroid\_sources](../api/photutils.centroids.centroid_sources.html)
    - [centroid\_symmetry](../api/photutils.centroids.centroid_symmetry.html)
    - [CentroidQuadratic](../api/photutils.centroids.CentroidQuadratic.html)
  + [Datasets and Simulation (`photutils.datasets`)](../reference/datasets_api.html)
    - [apply\_poisson\_noise](../api/photutils.datasets.apply_poisson_noise.html)
    - [get\_path](../api/photutils.datasets.get_path.html)
    - [load\_irac\_psf](../api/photutils.datasets.load_irac_psf.html)
    - [load\_simulated\_hst\_star\_image](../api/photutils.datasets.load_simulated_hst_star_image.html)
    - [load\_spitzer\_catalog](../api/photutils.datasets.load_spitzer_catalog.html)
    - [load\_spitzer\_image](../api/photutils.datasets.load_spitzer_image.html)
    - [load\_star\_image](../api/photutils.datasets.load_star_image.html)
    - [make\_100gaussians\_image](../api/photutils.datasets.make_100gaussians_image.html)
    - [make\_4gaussians\_image](../api/photutils.datasets.make_4gaussians_image.html)
    - [make\_gwcs](../api/photutils.datasets.make_gwcs.html)
    - [make\_model\_image](../api/photutils.datasets.make_model_image.html)
    - [make\_model\_params](../api/photutils.datasets.make_model_params.html)
    - [make\_noise\_image](../api/photutils.datasets.make_noise_image.html)
    - [make\_random\_models\_table](../api/photutils.datasets.make_random_models_table.html)
    - [make\_wcs](../api/photutils.datasets.make_wcs.html)
    - [params\_table\_to\_models](../api/photutils.datasets.params_table_to_models.html)
  + [Point-like Source Detection (`photutils.detection`)](../reference/detection_api.html)
    - [find\_peaks](../api/photutils.detection.find_peaks.html)
    - [DAOStarFinder](../api/photutils.detection.DAOStarFinder.html)
    - [IRAFStarFinder](../api/photutils.detection.IRAFStarFinder.html)
    - [StarFinder](../api/photutils.detection.StarFinder.html)
    - [StarFinderBase](../api/photutils.detection.StarFinderBase.html)
    - [StarFinderCatalogBase](../api/photutils.detection.StarFinderCatalogBase.html)
  + [Geometry Functions (`photutils.geometry`)](../reference/geometry_api.html)
    - [circular\_overlap\_grid](../api/photutils.geometry.circular_overlap_grid.html)
    - [elliptical\_overlap\_grid](../api/photutils.geometry.elliptical_overlap_grid.html)
    - [rectangular\_overlap\_grid](../api/photutils.geometry.rectangular_overlap_grid.html)
  + [Elliptical Isophote Analysis (`photutils.isophote`)](../reference/isophote_api.html)
    - [build\_ellipse\_model](../api/photutils.isophote.build_ellipse_model.html)
    - [first\_and\_second\_harmonic\_function](../api/photutils.isophote.first_and_second_harmonic_function.html)
    - [fit\_first\_and\_second\_harmonics](../api/photutils.isophote.fit_first_and_second_harmonics.html)
    - [fit\_upper\_harmonic](../api/photutils.isophote.fit_upper_harmonic.html)
    - [Ellipse](../api/photutils.isophote.Ellipse.html)
    - [EllipseFitter](../api/photutils.isophote.EllipseFitter.html)
    - [EllipseGeometry](../api/photutils.isophote.EllipseGeometry.html)
    - [EllipseSample](../api/photutils.isophote.EllipseSample.html)
    - [Isophote](../api/photutils.isophote.Isophote.html)
    - [IsophoteList](../api/photutils.isophote.IsophoteList.html)
  + [Morphological Properties (`photutils.morphology`)](../reference/morphology_api.html)
    - [data\_properties](../api/photutils.morphology.data_properties.html)
    - [gini](../api/photutils.morphology.gini.html)
  + [Profiles (`photutils.profiles`)](../reference/profiles_api.html)
    - [CurveOfGrowth](../api/photutils.profiles.CurveOfGrowth.html)
    - [EllipticalCurveOfGrowth](../api/photutils.profiles.EllipticalCurveOfGrowth.html)
    - [EnsquaredCurveOfGrowth](../api/photutils.profiles.EnsquaredCurveOfGrowth.html)
    - [ProfileBase](../api/photutils.profiles.ProfileBase.html)
    - [RadialProfile](../api/photutils.profiles.RadialProfile.html)
  + [PSF Photometry (`photutils.psf`)](../reference/psf_api.html)
    - [decode\_psf\_flags](../api/photutils.psf.decode_psf_flags.html)
    - [extract\_stars](../api/photutils.psf.extract_stars.html)
    - [fit\_2dgaussian](../api/photutils.psf.fit_2dgaussian.html)
    - [fit\_fwhm](../api/photutils.psf.fit_fwhm.html)
    - [grid\_from\_epsfs](../api/photutils.psf.grid_from_epsfs.html)
    - [make\_epsf\_from\_psf](../api/photutils.psf.make_epsf_from_psf.html)
    - [make\_psf\_model](../api/photutils.psf.make_psf_model.html)
    - [make\_psf\_model\_image](../api/photutils.psf.make_psf_model_image.html)
    - [stdpsf\_reader](../api/photutils.psf.stdpsf_reader.html)
    - [webbpsf\_reader](../api/photutils.psf.webbpsf_reader.html)
    - [AiryDiskPRF](../api/photutils.psf.AiryDiskPRF.html)
    - [AiryDiskPSF](../api/photutils.psf.AiryDiskPSF.html)
    - [CircularGaussianPRF](../api/photutils.psf.CircularGaussianPRF.html)
    - [CircularGaussianPSF](../api/photutils.psf.CircularGaussianPSF.html)
    - [CircularGaussianSigmaPRF](../api/photutils.psf.CircularGaussianSigmaPRF.html)
    - [EPSFBuildResults](../api/photutils.psf.EPSFBuildResults.html)
    - [EPSFBuilder](../api/photutils.psf.EPSFBuilder.html)
    - [EPSFFitter](../api/photutils.psf.EPSFFitter.html)
    - [EPSFStar](../api/photutils.psf.EPSFStar.html)
    - [EPSFStars](../api/photutils.psf.EPSFStars.html)
    - [GaussianPRF](../api/photutils.psf.GaussianPRF.html)
    - [GaussianPSF](../api/photutils.psf.GaussianPSF.html)
    - [GriddedPSFModel](../api/photutils.psf.GriddedPSFModel.html)
    - [GriddedPSFModelRead](../api/photutils.psf.GriddedPSFModelRead.html)
    - [ImagePSF](../api/photutils.psf.ImagePSF.html)
    - [IterativePSFPhotometry](../api/photutils.psf.IterativePSFPhotometry.html)
    - [LinkedEPSFStar](../api/photutils.psf.LinkedEPSFStar.html)
    - [MoffatPRF](../api/photutils.psf.MoffatPRF.html)
    - [MoffatPSF](../api/photutils.psf.MoffatPSF.html)
    - [PSFPhotometry](../api/photutils.psf.PSFPhotometry.html)
    - [STDPSFGrid](../api/photutils.psf.STDPSFGrid.html)
    - [SourceGrouper](../api/photutils.psf.SourceGrouper.html)
    - [SourceGroups](../api/photutils.psf.SourceGroups.html)
  + [PSF Matching (`photutils.psf_matching`)](../reference/psf_matching_api.html)
    - [create\_matching\_kernel](../api/photutils.psf_matching.create_matching_kernel.html)
    - [make\_kernel](../api/photutils.psf_matching.make_kernel.html)
    - [make\_wiener\_kernel](../api/photutils.psf_matching.make_wiener_kernel.html)
    - [resize\_psf](../api/photutils.psf_matching.resize_psf.html)
    - [CosineBellWindow](../api/photutils.psf_matching.CosineBellWindow.html)
    - [HanningWindow](../api/photutils.psf_matching.HanningWindow.html)
    - [SplitCosineBellWindow](../api/photutils.psf_matching.SplitCosineBellWindow.html)
    - [TopHatWindow](../api/photutils.psf_matching.TopHatWindow.html)
    - [TukeyWindow](../api/photutils.psf_matching.TukeyWindow.html)
  + [Image Segmentation (`photutils.segmentation`)](../reference/segmentation_api.html)
    - [deblend\_sources](../api/photutils.segmentation.deblend_sources.html)
    - [decode\_segmentation\_flags](../api/photutils.segmentation.decode_segmentation_flags.html)
    - [detect\_sources](../api/photutils.segmentation.detect_sources.html)
    - [detect\_threshold](../api/photutils.segmentation.detect_threshold.html)
    - [make\_2dgaussian\_kernel](../api/photutils.segmentation.make_2dgaussian_kernel.html)
    - [Segment](../api/photutils.segmentation.Segment.html)
    - [SegmentationImage](../api/photutils.segmentation.SegmentationImage.html)
    - [SourceCatalog](../api/photutils.segmentation.SourceCatalog.html)
    - [SourceFinder](../api/photutils.segmentation.SourceFinder.html)
  + [Utility Functions (`photutils.utils`)](../reference/utils_api.html)
    - [calc\_total\_error](../api/photutils.utils.calc_total_error.html)
    - [circular\_footprint](../api/photutils.utils.circular_footprint.html)
    - [compute\_pixel\_area\_map](../api/photutils.utils.compute_pixel_area_map.html)
    - [compute\_pixel\_areas](../api/photutils.utils.compute_pixel_areas.html)
    - [make\_random\_cmap](../api/photutils.utils.make_random_cmap.html)
    - [CutoutImage](../api/photutils.utils.CutoutImage.html)
    - [DeblendWarning](../api/photutils.utils.DeblendWarning.html)
    - [ImageDepth](../api/photutils.utils.ImageDepth.html)
    - [NoDetectionsWarning](../api/photutils.utils.NoDetectionsWarning.html)
    - [PhotutilsDeprecationWarning](../api/photutils.utils.PhotutilsDeprecationWarning.html)
    - [ShepardIDWInterpolator](../api/photutils.utils.ShepardIDWInterpolator.html)
* [Development](../development/index.html)
  + [Reporting Issues and Contributing](../development/contributing.html)
  + [Contributors](../development/contributors.html)
  + [Package Release Instructions](../development/releasing.html)
  + [License](../development/license.html)
* [Release Notes](../release_notes/index.html)
  + [Changelog](../changelog.html)
  + [What’s New in Photutils 3.1?](../whats_new/3.1.html)
  + [What’s New in Photutils 3.0?](../whats_new/3.0.html)
  + [What’s New in Photutils 2.3?](../whats_new/2.3.html)
  + [What’s New in Photutils 2.2?](../whats_new/2.2.html)
  + [What’s New in Photutils 2.1?](../whats_new/2.1.html)
  + [What’s New in Photutils 2.0?](../whats_new/2.0.html)
  + [What’s New in Photutils 1.13?](../whats_new/1.13.html)
  + [What’s New in Photutils 1.12?](../whats_new/1.12.html)
  + [What’s New in Photutils 1.11?](../whats_new/1.11.html)
  + [What’s New in Photutils 1.10?](../whats_new/1.10.html)
  + [What’s New in Photutils 1.9?](../whats_new/1.9.html)
  + [What’s New in Photutils 1.8?](../whats_new/1.8.html)
  + [What’s New in Photutils 1.7?](../whats_new/1.7.html)
  + [What’s New in Photutils 1.6?](../whats_new/1.6.html)
  + [What’s New in Photutils 1.5?](../whats_new/1.5.html)
  + [What’s New in Photutils 1.4?](../whats_new/1.4.html)
  + [What’s New in Photutils 1.3?](../whats_new/1.3.html)
  + [What’s New in Photutils 1.2?](../whats_new/1.2.html)
  + [What’s New in Photutils 1.1?](../whats_new/1.1.html)

* [User Guide](index.html)
* Point-like Source Detection (`photutils.detection`)

Point-like Source Detection ([`photutils.detection`](../reference/detection_api.html#module-photutils.detection "photutils.detection"))[#](#point-like-source-detection-photutils-detection "Link to this heading")
===================================================================================================================================================================================================================

Introduction[#](#introduction "Link to this heading")
-----------------------------------------------------

One generally needs to identify astronomical sources in the data before
performing photometry or other measurements. The [`photutils.detection`](../reference/detection_api.html#module-photutils.detection "photutils.detection")
subpackage provides tools to detect point-like (stellar) sources in an
image. This subpackage also provides tools to find local peaks in an
image that are above a specified threshold value.

For general-use source detection and extraction of both point-like
and extended sources, please see [Image Segmentation](segmentation.html#image-segmentation).

Detecting Stars[#](#detecting-stars "Link to this heading")
-----------------------------------------------------------

Photutils includes two widely used tools for detecting stars in an
image, [DAOFIND](https://iraf.readthedocs.io/en/latest/tasks/noao/digiphot/apphot/daofind.html) and IRAF’s [starfind](https://iraf.readthedocs.io/en/latest/tasks/images/imcoords/starfind.html), plus a third tool that allows
input of a custom user-defined kernel.

[`DAOStarFinder`](../api/photutils.detection.DAOStarFinder.html#photutils.detection.DAOStarFinder "photutils.detection.DAOStarFinder") implements
the [DAOFIND](https://iraf.readthedocs.io/en/latest/tasks/noao/digiphot/apphot/daofind.html) algorithm ([Stetson 1987, PASP 99, 191](https://ui.adsabs.harvard.edu/abs/1987PASP...99..191S/abstract)).
It searches images for local density maxima that have a peak amplitude
above a specified threshold (applied to a convolved image) and with
size and shape similar to a defined 2D Gaussian kernel. To match the
original DAOFIND algorithm, the input `threshold` is internally scaled
by a factor derived from the convolution kernel. To apply the threshold
exactly as given (e.g., when supplying a spatial background-RMS map),
set `scale_threshold=False`. The class also computes roundness and
sharpness statistics for detected sources, with configurable lower and
upper bounds.

[`IRAFStarFinder`](../api/photutils.detection.IRAFStarFinder.html#photutils.detection.IRAFStarFinder "photutils.detection.IRAFStarFinder") is a class that
implements IRAF’s [starfind](https://iraf.readthedocs.io/en/latest/tasks/images/imcoords/starfind.html) algorithm. It is fundamentally
similar to [`DAOStarFinder`](../api/photutils.detection.DAOStarFinder.html#photutils.detection.DAOStarFinder "photutils.detection.DAOStarFinder"), but
[`IRAFStarFinder`](../api/photutils.detection.IRAFStarFinder.html#photutils.detection.IRAFStarFinder "photutils.detection.IRAFStarFinder") always uses a circular
Gaussian kernel whereas [`DAOStarFinder`](../api/photutils.detection.DAOStarFinder.html#photutils.detection.DAOStarFinder "photutils.detection.DAOStarFinder")
can use an elliptical Gaussian kernel. Another difference is that
[`IRAFStarFinder`](../api/photutils.detection.IRAFStarFinder.html#photutils.detection.IRAFStarFinder "photutils.detection.IRAFStarFinder") calculates the objects’
centroid, roundness, and sharpness using image moments.

[`StarFinder`](../api/photutils.detection.StarFinder.html#photutils.detection.StarFinder "photutils.detection.StarFinder") is a class similar to
[`IRAFStarFinder`](../api/photutils.detection.IRAFStarFinder.html#photutils.detection.IRAFStarFinder "photutils.detection.IRAFStarFinder"), but which allows input
of a custom user-defined kernel as a 2D array. This allows for more
generalization beyond simple Gaussian kernels.

The usage of [`IRAFStarFinder`](../api/photutils.detection.IRAFStarFinder.html#photutils.detection.IRAFStarFinder "photutils.detection.IRAFStarFinder") and
[`StarFinder`](../api/photutils.detection.StarFinder.html#photutils.detection.StarFinder "photutils.detection.StarFinder") follows the same pattern
as [`DAOStarFinder`](../api/photutils.detection.DAOStarFinder.html#photutils.detection.DAOStarFinder "photutils.detection.DAOStarFinder") shown below. Replace
the class name and adjust the parameters (e.g., `fwhm` and
`kernel`) as needed. Note that the `scale_threshold` parameter
is specific to [`DAOStarFinder`](../api/photutils.detection.DAOStarFinder.html#photutils.detection.DAOStarFinder "photutils.detection.DAOStarFinder").
Note also that each class returns different output columns. For
example, [`DAOStarFinder`](../api/photutils.detection.DAOStarFinder.html#photutils.detection.DAOStarFinder "photutils.detection.DAOStarFinder") includes
`roundness1`, `roundness2`, and `daofind_mag` columns, while
[`IRAFStarFinder`](../api/photutils.detection.IRAFStarFinder.html#photutils.detection.IRAFStarFinder "photutils.detection.IRAFStarFinder") includes `fwhm` and
`orientation` columns. See each class’s API documentation for the full
list of output columns.

As an example, let’s load a simulated HST star image and add Gaussian
noise. We will then estimate the background and background noise using
sigma-clipped statistics:

```
>>> import numpy as np
>>> from astropy.io import fits
>>> from astropy.stats import sigma_clipped_stats
>>> from photutils.datasets import make_noise_image
>>> url = ('https://github.com/astropy/photutils-datasets/raw/main/'
...        'data/hst_wfc3ir_f160w_simulated_starfield.fits')
>>> data = fits.getdata(url)
>>> data += make_noise_image(data.shape, distribution='gaussian',
...                          mean=10.0, stddev=5.0, seed=0)
>>> mean, median, std = sigma_clipped_stats(data, sigma=3.0)
>>> print(np.array((mean, median, std)))
[10.44410657 10.39699777  5.09141794]

```

Now we will subtract the background and use an instance of
[`DAOStarFinder`](../api/photutils.detection.DAOStarFinder.html#photutils.detection.DAOStarFinder "photutils.detection.DAOStarFinder") to find the stars in the
image, using a Gaussian kernel with a FWHM of 2.5 pixels, that have
peaks approximately 5 times the background standard deviation above the
background (i.e., the threshold is `5 * std`). The stars in the image
are undersampled, so we will slightly relax the `sharpness_range` to
allow for a wider range of values.

First, we create the star finder. Calling it on the data returns an
astropy [`QTable`](https://docs.astropy.org/en/stable/api/astropy.table.QTable.html#astropy.table.QTable "(in Astropy v8.0)") containing the results of the star
finder:

```
>>> from photutils.detection import DAOStarFinder
>>> threshold = 5.0 * std
>>> daofind = DAOStarFinder(threshold, fwhm=2.5,
...                         sharpness_range=(0.2, 1.5))

```

By default, [`DAOStarFinder`](../api/photutils.detection.DAOStarFinder.html#photutils.detection.DAOStarFinder "photutils.detection.DAOStarFinder") internally
scales the input threshold by a factor derived from the convolution
kernel to match the original [DAOFIND](https://iraf.readthedocs.io/en/latest/tasks/noao/digiphot/apphot/daofind.html) algorithm. To apply
the threshold exactly as given (e.g., when supplying a spatial
background-RMS map), set `scale_threshold=False`:

```
>>> daofind_unscaled = DAOStarFinder(threshold, fwhm=2.5,
...                                  sharpness_range=(0.2, 1.5),
...                                  scale_threshold=False)

```

Running the finder on the background-subtracted data:

```
>>> sources = daofind(data - median)
>>> for col in sources.colnames:
...     if col not in ('id', 'n_pixels'):
...         sources[col].info.format = '%.2f'  # for consistent table output
>>> sources.pprint(max_lines=12, max_width=76)
 id x_centroid y_centroid sharpness ...   peak    flux   mag  daofind_mag
--- ---------- ---------- --------- ... ------- ------- ----- -----------
  1     848.57       2.15      0.89 ... 1051.78 3391.76 -8.83       -3.80
  2     181.85       3.75      0.97 ... 1711.87 4823.64 -9.21       -4.28
  3     323.88       3.70      0.96 ... 3005.97 8627.30 -9.84       -4.90
  4      99.89       8.95      1.07 ... 1134.12 2789.54 -8.61       -3.77
...        ...        ...       ... ...     ...     ...   ...         ...
497     114.16     993.47      0.84 ... 1577.91 5697.73 -9.39       -4.26
498     298.44     993.87      0.83 ...  644.97 2282.34 -8.40       -3.31
499     207.21     998.15      0.97 ... 2800.62 7693.48 -9.72       -4.83
500     691.03     998.77      1.15 ... 2600.83 5132.75 -9.28       -4.64
Length = 500 rows

```

Let’s plot the image and mark the location of detected sources:

([`Source code`](../_downloads/5b4c4884c1923691a8aefed434a9b3ee/detection-1.py), [`png`](../_downloads/a7a16469ca0e02a03c8206e2582f59af/detection-1.png), [`hires.png`](../_downloads/5a68ec63f108de4265d3f6d68bb148a5/detection-1.hires.png), [`pdf`](../_downloads/2c277d28556657b514e5cee48d44eed6/detection-1.pdf), [`svg`](../_downloads/6a686784d5175f11dab19041730ffec4/detection-1.svg))

![../_images/detection-1.png](../_images/detection-1.png)

### Masking Regions[#](#masking-regions "Link to this heading")

Regions of the input image can be masked by using the `mask`
keyword with the [`DAOStarFinder`](../api/photutils.detection.DAOStarFinder.html#photutils.detection.DAOStarFinder "photutils.detection.DAOStarFinder"),
[`IRAFStarFinder`](../api/photutils.detection.IRAFStarFinder.html#photutils.detection.IRAFStarFinder "photutils.detection.IRAFStarFinder"), or
[`StarFinder`](../api/photutils.detection.StarFinder.html#photutils.detection.StarFinder "photutils.detection.StarFinder") instance. This simple example
uses [`DAOStarFinder`](../api/photutils.detection.DAOStarFinder.html#photutils.detection.DAOStarFinder "photutils.detection.DAOStarFinder") and masks two
rectangular regions. No sources will be detected in the masked regions:

```
>>> from photutils.detection import DAOStarFinder
>>> daofind = DAOStarFinder(threshold, fwhm=2.5, sharpness_range=(0.2, 1.5))
>>> mask = np.zeros(data.shape, dtype=bool)
>>> mask[650:851, 600:851] = True
>>> mask[250:451, 150:551] = True
>>> sources = daofind(data - median, mask=mask)

```

([`Source code`](../_downloads/c0cec17767d697ba01632f56e24a138f/detection-2.py), [`png`](../_downloads/632fe1243d8ea36a08e62714abbf29e2/detection-2.png), [`hires.png`](../_downloads/a1c215a1359a64e9e8c6a551631f0fa4/detection-2.hires.png), [`pdf`](../_downloads/59f8cb705f79e0458ce0b54fa91e4cae/detection-2.pdf), [`svg`](../_downloads/3be9edea50946948abf25ba796850dc2/detection-2.svg))

![../_images/detection-2.png](../_images/detection-2.png)

Local Peak Detection[#](#local-peak-detection "Link to this heading")
---------------------------------------------------------------------

Photutils also includes a [`find_peaks()`](../api/photutils.detection.find_peaks.html#photutils.detection.find_peaks "photutils.detection.find_peaks")
function to find local peaks in an image that are above a specified
threshold value. Peaks are the local maxima above a specified threshold
that are separated by a specified minimum number of pixels, defined by a
box size or a local footprint.

The returned pixel coordinates for the peaks are always integer-valued
(i.e., no centroiding is performed, only the peak pixel is identified).
However, a centroiding function can be input via the `centroid_func`
keyword to [`find_peaks()`](../api/photutils.detection.find_peaks.html#photutils.detection.find_peaks "photutils.detection.find_peaks") to also compute
centroid coordinates with subpixel precision.

The `box_size` parameter also effectively imposes a minimum separation
between detected peaks, since only one peak can be found within each box
of that size. Specifically, two peaks must be separated by at least
`box_size // 2 + 1` pixels along at least one axis. For example, with
a `box_size` of 11, two peaks must be at least 6 pixels apart along
the x- or y-axis.

As a simple example, let’s find the local peaks in the image above that
are 5 sigma above the background using a box size of 11 pixels:

```
>>> from photutils.detection import find_peaks
>>> threshold = median + (5.0 * std)
>>> tbl = find_peaks(data, threshold, box_size=11)
>>> tbl['peak_value'].info.format = '%.8g'
>>> print(tbl)
 id x_peak y_peak peak_value
--- ------ ------ ----------
  1    849      2  1062.1752
  2    182      4  1722.2687
  3    324      4  3016.3684
  4    100      9  1144.5217
  5    824      9  1311.2049
...    ...    ...        ...
497    889    992  194.27323
498    114    994  1588.3073
499    299    994  655.36699
500    207    998  2811.0195
501    691    999  2611.2233
Length = 501 rows

```

Let’s plot the location of the detected peaks in the image:

([`Source code`](../_downloads/ab1f0535861e0b7b01ae2274669f2733/detection-3.py), [`png`](../_downloads/362567d774e72cc0d5beb37964f9cf5c/detection-3.png), [`hires.png`](../_downloads/95e720421b1d7643fc076eb83c85616a/detection-3.hires.png), [`pdf`](../_downloads/23ce83b70cd61f79ddbea1831f0bb828/detection-3.pdf), [`svg`](../_downloads/33c234bc49afffcb6309078b4623b2fb/detection-3.svg))

![../_images/detection-3.png](../_images/detection-3.png)

API Reference[#](#api-reference "Link to this heading")
-------------------------------------------------------

[Point-like Source Detection (photutils.detection)](../reference/detection_api.html)

[previous

Centroids (`photutils.centroids`)](centroids.html "previous page")
[next

Image Segmentation (`photutils.segmentation`)](segmentation.html "next page")

On this page

* [Introduction](#introduction)
* [Detecting Stars](#detecting-stars)
  + [Masking Regions](#masking-regions)
* [Local Peak Detection](#local-peak-detection)
* [API Reference](#api-reference)

© Copyright 2011-2026, Photutils Developers.

[Code of Conduct](https://astropy.org/code_of_conduct.html)

Updated on 16 Oct 2026
, built with [Sphinx
9.1.0](http://sphinx-doc.org/)

## Links found on page

- http://sphinx-doc.org/
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
- https://docs.astropy.org
- https://docs.astropy.org/en/stable/api/astropy.table.QTable.html#astropy.table.QTable
- https://docs.astropy.org/projects/photutils/en/stable/_downloads/23ce83b70cd61f79ddbea1831f0bb828/detection-3.pdf
- https://docs.astropy.org/projects/photutils/en/stable/_downloads/2c277d28556657b514e5cee48d44eed6/detection-1.pdf
- https://docs.astropy.org/projects/photutils/en/stable/_downloads/33c234bc49afffcb6309078b4623b2fb/detection-3.svg
- https://docs.astropy.org/projects/photutils/en/stable/_downloads/362567d774e72cc0d5beb37964f9cf5c/detection-3.png
- https://docs.astropy.org/projects/photutils/en/stable/_downloads/3be9edea50946948abf25ba796850dc2/detection-2.svg
- https://docs.astropy.org/projects/photutils/en/stable/_downloads/59f8cb705f79e0458ce0b54fa91e4cae/detection-2.pdf
- https://docs.astropy.org/projects/photutils/en/stable/_downloads/5a68ec63f108de4265d3f6d68bb148a5/detection-1.hires.png
- https://docs.astropy.org/projects/photutils/en/stable/_downloads/5b4c4884c1923691a8aefed434a9b3ee/detection-1.py
- https://docs.astropy.org/projects/photutils/en/stable/_downloads/632fe1243d8ea36a08e62714abbf29e2/detection-2.png
- https://docs.astropy.org/projects/photutils/en/stable/_downloads/6a686784d5175f11dab19041730ffec4/detection-1.svg
- https://docs.astropy.org/projects/photutils/en/stable/_downloads/95e720421b1d7643fc076eb83c85616a/detection-3.hires.png
- https://docs.astropy.org/projects/photutils/en/stable/_downloads/a1c215a1359a64e9e8c6a551631f0fa4/detection-2.hires.png
- https://docs.astropy.org/projects/photutils/en/stable/_downloads/a7a16469ca0e02a03c8206e2582f59af/detection-1.png
- https://docs.astropy.org/projects/photutils/en/stable/_downloads/ab1f0535861e0b7b01ae2274669f2733/detection-3.py
- https://docs.astropy.org/projects/photutils/en/stable/_downloads/c0cec17767d697ba01632f56e24a138f/detection-2.py
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.aperture.Aperture.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.aperture.ApertureMask.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.aperture.AperturePhotometry.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.aperture.ApertureStats.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.aperture.BoundingBox.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.aperture.CircularAnnulus.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.aperture.CircularAperture.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.aperture.CircularMaskMixin.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.aperture.EllipticalAnnulus.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.aperture.EllipticalAperture.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.aperture.EllipticalMaskMixin.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.aperture.PixelAperture.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.aperture.PolygonAperture.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.aperture.RectangularAnnulus.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.aperture.RectangularAperture.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.aperture.RectangularMaskMixin.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.aperture.SkyAperture.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.aperture.SkyCircularAnnulus.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.aperture.SkyCircularAperture.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.aperture.SkyEllipticalAnnulus.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.aperture.SkyEllipticalAperture.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.aperture.SkyPolygonAperture.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.aperture.SkyRectangularAnnulus.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.aperture.SkyRectangularAperture.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.aperture.aperture_photometry.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.aperture.aperture_to_region.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.aperture.decode_aperture_flags.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.aperture.region_to_aperture.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.background.Background2D.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.background.BackgroundBase.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.background.BackgroundRMSBase.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.background.BiweightLocationBackground.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.background.BiweightScaleBackgroundRMS.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.background.BkgIDWInterpolator.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.background.BkgZoomInterpolator.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.background.LocalBackground.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.background.MADStdBackgroundRMS.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.background.MMMBackground.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.background.MeanBackground.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.background.MedianBackground.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.background.ModeEstimatorBackground.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.background.SExtractorBackground.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.background.StdBackgroundRMS.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.centroids.CentroidQuadratic.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.centroids.centroid_1dg.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.centroids.centroid_2dg.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.centroids.centroid_com.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.centroids.centroid_quadratic.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.centroids.centroid_sources.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.centroids.centroid_symmetry.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.datasets.apply_poisson_noise.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.datasets.get_path.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.datasets.load_irac_psf.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.datasets.load_simulated_hst_star_image.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.datasets.load_spitzer_catalog.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.datasets.load_spitzer_image.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.datasets.load_star_image.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.datasets.make_100gaussians_image.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.datasets.make_4gaussians_image.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.datasets.make_gwcs.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.datasets.make_model_image.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.datasets.make_model_params.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.datasets.make_noise_image.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.datasets.make_random_models_table.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.datasets.make_wcs.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.datasets.params_table_to_models.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.detection.DAOStarFinder.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.detection.DAOStarFinder.html#photutils.detection.DAOStarFinder
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.detection.IRAFStarFinder.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.detection.IRAFStarFinder.html#photutils.detection.IRAFStarFinder
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.detection.StarFinder.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.detection.StarFinder.html#photutils.detection.StarFinder
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.detection.StarFinderBase.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.detection.StarFinderCatalogBase.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.detection.find_peaks.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.detection.find_peaks.html#photutils.detection.find_peaks
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.geometry.circular_overlap_grid.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.geometry.elliptical_overlap_grid.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.geometry.rectangular_overlap_grid.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.isophote.Ellipse.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.isophote.EllipseFitter.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.isophote.EllipseGeometry.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.isophote.EllipseSample.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.isophote.Isophote.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.isophote.IsophoteList.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.isophote.build_ellipse_model.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.isophote.first_and_second_harmonic_function.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.isophote.fit_first_and_second_harmonics.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.isophote.fit_upper_harmonic.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.morphology.data_properties.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.morphology.gini.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.profiles.CurveOfGrowth.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.profiles.EllipticalCurveOfGrowth.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.profiles.EnsquaredCurveOfGrowth.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.profiles.ProfileBase.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.profiles.RadialProfile.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.AiryDiskPRF.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.AiryDiskPSF.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.CircularGaussianPRF.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.CircularGaussianPSF.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.CircularGaussianSigmaPRF.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.EPSFBuildResults.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.EPSFBuilder.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.EPSFFitter.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.EPSFStar.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.EPSFStars.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.GaussianPRF.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.GaussianPSF.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.GriddedPSFModel.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.GriddedPSFModelRead.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.ImagePSF.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.IterativePSFPhotometry.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.LinkedEPSFStar.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.MoffatPRF.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.MoffatPSF.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.PSFPhotometry.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.STDPSFGrid.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.SourceGrouper.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.SourceGroups.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.decode_psf_flags.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.extract_stars.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.fit_2dgaussian.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.fit_fwhm.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.grid_from_epsfs.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.make_epsf_from_psf.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.make_psf_model.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.make_psf_model_image.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.stdpsf_reader.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.webbpsf_reader.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf_matching.CosineBellWindow.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf_matching.HanningWindow.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf_matching.SplitCosineBellWindow.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf_matching.TopHatWindow.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf_matching.TukeyWindow.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf_matching.create_matching_kernel.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf_matching.make_kernel.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf_matching.make_wiener_kernel.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf_matching.resize_psf.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.segmentation.Segment.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.segmentation.SegmentationImage.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.segmentation.SourceCatalog.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.segmentation.SourceFinder.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.segmentation.deblend_sources.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.segmentation.decode_segmentation_flags.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.segmentation.detect_sources.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.segmentation.detect_threshold.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.segmentation.make_2dgaussian_kernel.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.utils.CutoutImage.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.utils.DeblendWarning.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.utils.ImageDepth.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.utils.NoDetectionsWarning.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.utils.PhotutilsDeprecationWarning.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.utils.ShepardIDWInterpolator.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.utils.calc_total_error.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.utils.circular_footprint.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.utils.compute_pixel_area_map.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.utils.compute_pixel_areas.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.utils.make_random_cmap.html
- https://docs.astropy.org/projects/photutils/en/stable/changelog.html
- https://docs.astropy.org/projects/photutils/en/stable/development/contributing.html
- https://docs.astropy.org/projects/photutils/en/stable/development/contributors.html
- https://docs.astropy.org/projects/photutils/en/stable/development/index.html
- https://docs.astropy.org/projects/photutils/en/stable/development/license.html
- https://docs.astropy.org/projects/photutils/en/stable/development/releasing.html
- https://docs.astropy.org/projects/photutils/en/stable/getting_started/citation.html
- https://docs.astropy.org/projects/photutils/en/stable/getting_started/importing.html
- https://docs.astropy.org/projects/photutils/en/stable/getting_started/index.html
- https://docs.astropy.org/projects/photutils/en/stable/getting_started/install.html
- https://docs.astropy.org/projects/photutils/en/stable/getting_started/overview.html
- https://docs.astropy.org/projects/photutils/en/stable/getting_started/performance_tips.html
- https://docs.astropy.org/projects/photutils/en/stable/getting_started/pixel_conventions.html
- https://docs.astropy.org/projects/photutils/en/stable/index.html
- https://docs.astropy.org/projects/photutils/en/stable/reference/aperture_api.html
- https://docs.astropy.org/projects/photutils/en/stable/reference/background_api.html
- https://docs.astropy.org/projects/photutils/en/stable/reference/centroids_api.html
- https://docs.astropy.org/projects/photutils/en/stable/reference/datasets_api.html
- https://docs.astropy.org/projects/photutils/en/stable/reference/detection_api.html
- https://docs.astropy.org/projects/photutils/en/stable/reference/detection_api.html#module-photutils.detection
- https://docs.astropy.org/projects/photutils/en/stable/reference/geometry_api.html
- https://docs.astropy.org/projects/photutils/en/stable/reference/index.html
- https://docs.astropy.org/projects/photutils/en/stable/reference/isophote_api.html
- https://docs.astropy.org/projects/photutils/en/stable/reference/morphology_api.html
- https://docs.astropy.org/projects/photutils/en/stable/reference/profiles_api.html
- https://docs.astropy.org/projects/photutils/en/stable/reference/psf_api.html
- https://docs.astropy.org/projects/photutils/en/stable/reference/psf_matching_api.html
- https://docs.astropy.org/projects/photutils/en/stable/reference/segmentation_api.html
- https://docs.astropy.org/projects/photutils/en/stable/reference/utils_api.html
- https://docs.astropy.org/projects/photutils/en/stable/release_notes/index.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/aperture.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/asdf.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/background.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/centroids.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/curves_of_growth.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/datasets.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/epsf_building.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/geometry.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/grouping.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/index.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/isophote.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/isophote_faq.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/morphology.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/psf.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/psf_matching.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/radial_profiles.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/segmentation.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/segmentation.html#image-segmentation
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/utils.html
- https://docs.astropy.org/projects/photutils/en/stable/whats_new/1.1.html
- https://docs.astropy.org/projects/photutils/en/stable/whats_new/1.10.html
- https://docs.astropy.org/projects/photutils/en/stable/whats_new/1.11.html
- https://docs.astropy.org/projects/photutils/en/stable/whats_new/1.12.html
- https://docs.astropy.org/projects/photutils/en/stable/whats_new/1.13.html
- https://docs.astropy.org/projects/photutils/en/stable/whats_new/1.2.html
- https://docs.astropy.org/projects/photutils/en/stable/whats_new/1.3.html
- https://docs.astropy.org/projects/photutils/en/stable/whats_new/1.4.html
- https://docs.astropy.org/projects/photutils/en/stable/whats_new/1.5.html
- https://docs.astropy.org/projects/photutils/en/stable/whats_new/1.6.html
- https://docs.astropy.org/projects/photutils/en/stable/whats_new/1.7.html
- https://docs.astropy.org/projects/photutils/en/stable/whats_new/1.8.html
- https://docs.astropy.org/projects/photutils/en/stable/whats_new/1.9.html
- https://docs.astropy.org/projects/photutils/en/stable/whats_new/2.0.html
- https://docs.astropy.org/projects/photutils/en/stable/whats_new/2.1.html
- https://docs.astropy.org/projects/photutils/en/stable/whats_new/2.2.html
- https://docs.astropy.org/projects/photutils/en/stable/whats_new/2.3.html
- https://docs.astropy.org/projects/photutils/en/stable/whats_new/3.0.html
- https://docs.astropy.org/projects/photutils/en/stable/whats_new/3.1.html
- https://github.com/astropy/photutils
- https://iraf.readthedocs.io/en/latest/tasks/images/imcoords/starfind.html
- https://iraf.readthedocs.io/en/latest/tasks/noao/digiphot/apphot/daofind.html
- https://photutils.readthedocs.io
- https://reproject.readthedocs.io
- https://specreduce.readthedocs.io
- https://specutils.readthedocs.io
- https://ui.adsabs.harvard.edu/abs/1987PASP...99..191S/abstract
