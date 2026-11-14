---
source: https://photutils.readthedocs.io/en/stable/user_guide/psf.html
fetched: 2026-11-14
status: 200
---

PSF Photometry (photutils.psf) — photutils 3.1.1

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
  + [Point-like Source Detection (`photutils.detection`)](detection.html)
  + [Image Segmentation (`photutils.segmentation`)](segmentation.html)
  + [Morphological Properties (`photutils.morphology`)](morphology.html)
  + [Aperture Photometry (`photutils.aperture`)](aperture.html)
  + [PSF Photometry (`photutils.psf`)](#)
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
* PSF Photometry (`photutils.psf`)

PSF Photometry ([`photutils.psf`](../reference/psf_api.html#module-photutils.psf "photutils.psf"))[#](#psf-photometry-photutils-psf "Link to this heading")
===========================================================================================================================================================

The [`photutils.psf`](../reference/psf_api.html#module-photutils.psf "photutils.psf") subpackage contains tools for model-fitting
photometry, often called “PSF photometry”.

PSF Photometry Overview[#](#psf-photometry-overview "Link to this heading")
---------------------------------------------------------------------------

Photutils provides a modular set of tools to perform PSF photometry
for different science cases. The tools are implemented as classes that
perform various subtasks of PSF photometry. High-level classes are also
provided to connect these pieces together.

The two main PSF-photometry classes are [`PSFPhotometry`](../api/photutils.psf.PSFPhotometry.html#photutils.psf.PSFPhotometry "photutils.psf.PSFPhotometry")
and [`IterativePSFPhotometry`](../api/photutils.psf.IterativePSFPhotometry.html#photutils.psf.IterativePSFPhotometry "photutils.psf.IterativePSFPhotometry").
[`PSFPhotometry`](../api/photutils.psf.PSFPhotometry.html#photutils.psf.PSFPhotometry "photutils.psf.PSFPhotometry") provides the framework for a flexible PSF
photometry workflow that can find sources in an image, optionally group
overlapping sources, fit the PSF model to the sources, and subtract the
fit PSF models from the image.

[`IterativePSFPhotometry`](../api/photutils.psf.IterativePSFPhotometry.html#photutils.psf.IterativePSFPhotometry "photutils.psf.IterativePSFPhotometry") is an iterative version of
[`PSFPhotometry`](../api/photutils.psf.PSFPhotometry.html#photutils.psf.PSFPhotometry "photutils.psf.PSFPhotometry") where new sources are detected in the
residual image after the fit sources are subtracted. The iterative
process can be useful for crowded fields where sources are blended. A
`mode` keyword is provided to control the behavior of the iterative
process, where either all sources or only the newly detected sources are
fit in subsequent iterations. The process repeats until no additional
sources are detected or a maximum number of iterations has been
reached. When used with the [`DAOStarFinder`](../api/photutils.detection.DAOStarFinder.html#photutils.detection.DAOStarFinder "photutils.detection.DAOStarFinder"),
[`IterativePSFPhotometry`](../api/photutils.psf.IterativePSFPhotometry.html#photutils.psf.IterativePSFPhotometry "photutils.psf.IterativePSFPhotometry") is essentially an implementation
of the DAOPHOT algorithm described by Stetson in his [seminal paper](https://ui.adsabs.harvard.edu/abs/1987PASP...99..191S/abstract) for
crowded-field stellar photometry.

The source-finding step is controlled by the `finder`
keyword, where one inputs a callable function or class
instance. Typically, this would be one of the source-detection
classes implemented in the [`photutils.detection`](../reference/detection_api.html#module-photutils.detection "photutils.detection")
subpackage, e.g., [`DAOStarFinder`](../api/photutils.detection.DAOStarFinder.html#photutils.detection.DAOStarFinder "photutils.detection.DAOStarFinder"),
[`IRAFStarFinder`](../api/photutils.detection.IRAFStarFinder.html#photutils.detection.IRAFStarFinder "photutils.detection.IRAFStarFinder"), or
[`StarFinder`](../api/photutils.detection.StarFinder.html#photutils.detection.StarFinder "photutils.detection.StarFinder").

After finding sources, one can optionally apply a clustering algorithm
to group overlapping sources using the `grouper` keyword. Usually,
groups are formed by a distance criterion, which is the case for the
grouping algorithm proposed by Stetson. Sources that are grouped are
fit simultaneously. The reason behind the construction of groups and
not fitting all sources simultaneously is illustrated as follows:
imagine that one would like to fit 300 sources and the model for each
source has three parameters to be fitted. If one constructs a single
model to fit the 300 sources simultaneously, then the optimization
algorithm will have to search for the solution in a 900-dimensional
space, which is computationally expensive and error-prone. Having
smaller groups of sources effectively reduces the dimension of the
parameter space, which facilitates the optimization process. For more
details see [Source Grouping](grouping.html#source-grouping).

The local background around each source can optionally be subtracted
using the `local_bkg_estimator` keyword. This keyword accepts a
[`LocalBackground`](../api/photutils.background.LocalBackground.html#photutils.background.LocalBackground "photutils.background.LocalBackground") instance that estimates the
local statistics in a circular annulus aperture centered on each source.
The size of the annulus and the statistic function can be configured in
[`LocalBackground`](../api/photutils.background.LocalBackground.html#photutils.background.LocalBackground "photutils.background.LocalBackground").

The next step is to fit the sources and/or groups. This
task is performed using an Astropy fitter, for example
[`TRFLSQFitter`](https://docs.astropy.org/en/stable/api/astropy.modeling.fitting.TRFLSQFitter.html#astropy.modeling.fitting.TRFLSQFitter "(in Astropy v8.0)"), input via the `fitter`
keyword. All of the PSF models provided by [`photutils.psf`](../reference/psf_api.html#module-photutils.psf "photutils.psf"), both the
analytic and the image-based models, provide analytic Jacobians that the
fitters use automatically, avoiding finite-difference approximations
of the parameter derivatives and speeding up the fits. The shape of
the region to be fitted can be configured using the `fit_shape`
parameter. In general, `fit_shape` should be set to a small size
(e.g., (5, 5)) that covers the central part of the source with the
highest flux signal-to-noise. The initial positions are derived from
the `finder` algorithm. The initial flux values for the fit are
derived from measuring the flux in a circular aperture with radius
`aperture_radius`. Alternatively, the initial positions and fluxes can
be input in a table via the `init_params` keyword when calling the
class.

After sources are fitted, a model image of the fit
sources or a residual image can be generated using the
[`make_model_image()`](../api/photutils.psf.PSFPhotometry.html#photutils.psf.PSFPhotometry.make_model_image "photutils.psf.PSFPhotometry.make_model_image") and
[`make_residual_image()`](../api/photutils.psf.PSFPhotometry.html#photutils.psf.PSFPhotometry.make_residual_image "photutils.psf.PSFPhotometry.make_residual_image") methods,
respectively.

For [`IterativePSFPhotometry`](../api/photutils.psf.IterativePSFPhotometry.html#photutils.psf.IterativePSFPhotometry "photutils.psf.IterativePSFPhotometry"), the above steps can be
repeated until no additional sources are detected (or until a maximum
number of iterations is reached).

The [`PSFPhotometry`](../api/photutils.psf.PSFPhotometry.html#photutils.psf.PSFPhotometry "photutils.psf.PSFPhotometry") and
[`IterativePSFPhotometry`](../api/photutils.psf.IterativePSFPhotometry.html#photutils.psf.IterativePSFPhotometry "photutils.psf.IterativePSFPhotometry") classes provide the structure
in which the PSF-fitting steps described above are performed, but
all the stages can be turned on or off or replaced with different
implementations as the user desires. This makes the tools very flexible.
One can also bypass several of the steps by directly inputting to
`init_params` an Astropy table containing the initial parameters for
the source centers, fluxes, group identifiers, and local backgrounds.
This is also useful if one is interested in fitting only one or a few
sources in an image.

Terminology[#](#terminology "Link to this heading")
---------------------------------------------------

PSF photometry measures the flux and position of a star by fitting a
model of how the light of a point source is distributed over the pixels
of an image. Several closely related terms are used for such models,
including “PSF”, “PRF”, and “ePSF”, and different astronomy subfields
use them in slightly different ways. This section defines the terms as
they are used in [`photutils.psf`](../reference/psf_api.html#module-photutils.psf "photutils.psf").

Point Spread Function (PSF)
:   The PSF is the distribution of light from a point source at the
    detector, after the light has passed through the atmosphere (for
    ground-based data) and the telescope optics. It is a smooth,
    continuous function of position that does not depend on the detector
    pixels. It is sometimes called the instrumental PSF (iPSF) to make
    that explicit.

Pixel response function
:   A detector does not record the PSF itself. Each pixel collects the
    light that falls on its area and reports a single value. The pixel
    response function describes how sensitive a pixel is to light at
    each position within it. The simplest and most common assumption is
    that a pixel is equally sensitive over its whole area. Some authors
    abbreviate the pixel response function as “PRF”. We always write it
    out in full, because we use “PRF” for the Point Response Function
    defined next.

Effective PSF (ePSF) or Point Response Function (PRF)
:   The ePSF is the PSF as it is recorded by the pixels. Formally, it
    is the convolution of the PSF and the pixel response function.
    Its value at a given offset from a source is the fraction of the
    source flux that is recorded by a pixel centered at that offset.
    For pixels with a uniform response, that is the integral of the PSF
    over the area of the pixel. “ePSF” and “PRF” are two names for the
    same function. The name “ePSF” comes from [Anderson & King 2000](https://ui.adsabs.harvard.edu/abs/2000PASP..112.1360A/abstract),
    which describes this formalism in detail. The name “PRF” emphasizes
    that the function describes the response of the detector to a point
    source, rather than the PSF of the optics.

The pixel values of an image are samples of the ePSF, not of the PSF.
Like the PSF, the ePSF is a continuous function, because a pixel could
be centered at any offset from a source. The image of a star samples
the ePSF at a spacing of one pixel, at offsets that depend on where the
center of the star falls within a pixel. An oversampled ePSF samples the
same function on a finer grid. Each of its values is still the flux in a
whole detector pixel, not the flux in a subpixel.

A model that is fit to the pixel values of an image should therefore
represent the ePSF. The names of the models in [`photutils.psf`](../reference/psf_api.html#module-photutils.psf "photutils.psf") show what
each model represents:

* The analytic models whose names end in `PSF` (e.g.,
  [`CircularGaussianPSF`](../api/photutils.psf.CircularGaussianPSF.html#photutils.psf.CircularGaussianPSF "photutils.psf.CircularGaussianPSF")) give the value of the PSF at the
  input positions. They are not integrated over the pixels.
* The analytic models whose names end in `PRF` (e.g.,
  [`CircularGaussianPRF`](../api/photutils.psf.CircularGaussianPRF.html#photutils.psf.CircularGaussianPRF "photutils.psf.CircularGaussianPRF")) are integrated over the pixels,
  assuming that the response is uniform across a pixel.
* The image-based models ([`ImagePSF`](../api/photutils.psf.ImagePSF.html#photutils.psf.ImagePSF "photutils.psf.ImagePSF") and
  [`GriddedPSFModel`](../api/photutils.psf.GriddedPSFModel.html#photutils.psf.GriddedPSFModel "photutils.psf.GriddedPSFModel")) interpolate an input image and do
  not integrate it over the pixels. Despite the “PSF” in their names,
  their input images must be ePSFs. An ePSF that is built from observed
  stars (see [Building an Effective Point Spread Function (ePSF)](epsf_building.html#build-epsf)) includes the actual response of the
  pixels.

The difference between the PSF and the ePSF is largest for undersampled
data, where the PSF is narrow compared with a pixel, and for detectors
with significant sensitivity variations within a pixel. For such data,
the PSF is much sharper than the image of a star, and the sum of its
values at the pixel centers changes with the subpixel position of the
star. The difference is smaller for well-sampled data, but it does
not vanish, because the integration over a pixel always broadens the
profile. A PSF model with a known, fixed width is then narrower than
the image of a star, which biases the fitted flux. The distinction
is largely inconsequential when the model width is measured directly
from the pixelated image of a well-sampled star, as the measured width
already incorporates the effects of broadening.

In common usage, all of these functions are often simply called
the “PSF”, and “PSF photometry” refers to the general technique of
model-fitting photometry, regardless of exactly which kind of model is
fit. We use both terms in that broad sense throughout [`photutils.psf`](../reference/psf_api.html#module-photutils.psf "photutils.psf")
and this documentation, and we use the specific terms defined above
where the distinction matters.

PSF Models[#](#psf-models "Link to this heading")
-------------------------------------------------

As mentioned above, PSF photometry fundamentally involves fitting
models to data. As such, the PSF model is a critical component of PSF
photometry. For accurate results, both for photometry and astrometry,
the PSF model should be a good representation of the actual data. The
PSF model can be a simple analytic function, such as a 2D Gaussian
or Moffat profile, or it can be a more complex model derived from a
2D PSF image, e.g., an effective PSF (ePSF). The PSF model can also
encapsulate changes in the PSF across the detector, e.g., due to optical
aberrations.

For image-based PSF models, the PSF model is typically derived from
observed data or from detailed optical modeling. The PSF model can be
a single PSF model for the entire image or a grid of PSF models at
fiducial detector positions. Image-based PSF models are also often
oversampled with respect to the pixel grid to increase the accuracy of
fitting the PSF model.

The observatory that obtained the data may provide tools for creating
PSF models for their data or an empirical library of PSF models
based on previous observations. For example, the [Hubble Space
Telescope](https://www.stsci.edu/hst) provides libraries of
empirical PSF models for ACS and WFC3 (e.g., [WFC3 PSF Search](https://www.stsci.edu/hst/instrumentation/wfc3/data-analysis/psf/psf-search)).
Similarly, the [James Webb Space Telescope](https://www.stsci.edu/jwst)
and the [Nancy Grace Roman Space Telescope](https://www.stsci.edu/roman)
provide the [STPSF](https://stpsf.readthedocs.io/) Python software
for creating PSF models. In particular, STPSF outputs gridded PSF
models directly as Photutils [`GriddedPSFModel`](../api/photutils.psf.GriddedPSFModel.html#photutils.psf.GriddedPSFModel "photutils.psf.GriddedPSFModel") instances.

If you cannot obtain a PSF model from an empirical library or
observatory-provided tool, Photutils provides tools for creating an
empirical PSF model from the data itself, provided you have a large
number of isolated stars. Please see [Building an Effective Point Spread Function (ePSF)](epsf_building.html#build-epsf) for more
information and an example.

The [`photutils.psf`](../reference/psf_api.html#module-photutils.psf "photutils.psf") subpackage provides several PSF models that
can be used for PSF photometry. The PSF models are based on the
[Astropy models and fitting](https://docs.astropy.org/en/stable/modeling/index.html#astropy-modeling "(in Astropy v8.0)") framework.
The PSF models are used as input (via the `psf_model` parameter)
to the PSF photometry classes [`PSFPhotometry`](../api/photutils.psf.PSFPhotometry.html#photutils.psf.PSFPhotometry "photutils.psf.PSFPhotometry") and
[`IterativePSFPhotometry`](../api/photutils.psf.IterativePSFPhotometry.html#photutils.psf.IterativePSFPhotometry "photutils.psf.IterativePSFPhotometry"). The PSF models are fitted to
the data using an Astropy fitter class. Typically, the model position
(`x_0` and `y_0`) and flux (`flux`) parameters are varied
during the fitting process. The PSF model can also include additional
parameters, such as the full width at half maximum (FWHM) or sigma of
a Gaussian PSF or the alpha and beta parameters of a Moffat PSF. By
default, these additional parameters are “fixed” (i.e., not varied
during the fitting process). The user can choose to also vary these
parameters by setting the `fixed` attribute on the model parameter
to [`False`](https://docs.python.org/3/builtins/constants.html#False "(in Python v3.15)"). The position and/or flux parameters can also be fixed
during the fitting process if needed, e.g., for forced photometry (see
[Forced Photometry (Fixed Model Parameters)](#psf-forced-photometry)). Any of the model parameters can also be
bounded during the fitting process (see [Bounded Model Parameters](#psf-bounded-parameters)).

You can also create your own custom PSF model using the Astropy modeling
framework. The PSF model must be a 2D model that is a subclass of
[`Fittable2DModel`](https://docs.astropy.org/en/stable/api/astropy.modeling.Fittable2DModel.html#astropy.modeling.Fittable2DModel "(in Astropy v8.0)"). It must have parameters called
`x_0`, `y_0`, and `flux`, specifying the central position and
total integrated flux. The value of the model at a position should be
the flux in a detector pixel centered at that position (see
[Terminology](#psf-terminology)), especially for data that are undersampled.

### Analytic PSF Models[#](#analytic-psf-models "Link to this heading")

The [`photutils.psf`](../reference/psf_api.html#module-photutils.psf "photutils.psf") subpackage provides the following analytic PSF
models:

* [`GaussianPSF`](../api/photutils.psf.GaussianPSF.html#photutils.psf.GaussianPSF "photutils.psf.GaussianPSF"): a general 2D Gaussian PSF model
  parameterized in terms of the position, total flux, and full width
  at half maximum (FWHM) along the x- and y-axes. Rotation can also be
  included.
* [`CircularGaussianPSF`](../api/photutils.psf.CircularGaussianPSF.html#photutils.psf.CircularGaussianPSF "photutils.psf.CircularGaussianPSF"): a circular 2D Gaussian PSF model
  parameterized in terms of the position, total flux, and FWHM.
* [`GaussianPRF`](../api/photutils.psf.GaussianPRF.html#photutils.psf.GaussianPRF "photutils.psf.GaussianPRF"): a general 2D Gaussian PRF model
  parameterized in terms of the position, total flux, and FWHM
  along the x- and y-axes. Rotation can also be included.
* [`CircularGaussianPRF`](../api/photutils.psf.CircularGaussianPRF.html#photutils.psf.CircularGaussianPRF "photutils.psf.CircularGaussianPRF"): a circular 2D Gaussian PRF model
  parameterized in terms of the position, total flux, and FWHM.
* [`CircularGaussianSigmaPRF`](../api/photutils.psf.CircularGaussianSigmaPRF.html#photutils.psf.CircularGaussianSigmaPRF "photutils.psf.CircularGaussianSigmaPRF"): a circular 2D Gaussian PRF
  model parameterized in terms of the position, total flux, and sigma
  (standard deviation).
* [`MoffatPSF`](../api/photutils.psf.MoffatPSF.html#photutils.psf.MoffatPSF "photutils.psf.MoffatPSF"): a 2D Moffat PSF model parameterized in
  terms of the position, total flux, \(\alpha\), and \(\beta\)
  parameters.
* [`MoffatPRF`](../api/photutils.psf.MoffatPRF.html#photutils.psf.MoffatPRF "photutils.psf.MoffatPRF"): a 2D Moffat PRF model with the same
  parameters as [`MoffatPSF`](../api/photutils.psf.MoffatPSF.html#photutils.psf.MoffatPSF "photutils.psf.MoffatPSF").
* [`AiryDiskPSF`](../api/photutils.psf.AiryDiskPSF.html#photutils.psf.AiryDiskPSF "photutils.psf.AiryDiskPSF"): a 2D Airy disk PSF model parameterized
  in terms of the position, total flux, and radius of the first dark
  ring.
* [`AiryDiskPRF`](../api/photutils.psf.AiryDiskPRF.html#photutils.psf.AiryDiskPRF "photutils.psf.AiryDiskPRF"): a 2D Airy disk PRF model with the same
  parameters as [`AiryDiskPSF`](../api/photutils.psf.AiryDiskPSF.html#photutils.psf.AiryDiskPSF "photutils.psf.AiryDiskPSF").

Note there are two types of defined models, PSF and PRF models. The PSF
models are evaluated by sampling the analytic function at the input (x,
y) coordinates. The PRF models are evaluated by integrating the analytic
function over the pixel areas.

The values of a PSF model on a grid of detector pixels are the values
of the PSF at the pixel centers, not the fluxes in the pixels. For a
PSF that is undersampled by the detector pixels (a FWHM of less than
about 2 pixels), a PSF model is sharper than the sources in the data
and the sum of its values over the pixels depends on the subpixel
position of the source. Even for a well-sampled PSF, a PSF model whose
shape parameters are fixed gives fitted fluxes that are biased by a few
percent for a FWHM of 2 to 3 pixels, because the integration over a
pixel broadens the image of a source. The PRF models should therefore
be used to fit the pixel values of an image, e.g., for PSF photometry.
Every PSF model above has a PRF counterpart.

The Gaussian PRF models are integrated over the pixels analytically.
The Moffat and Airy disk PRF models are integrated numerically at
`n_nodes**2` points in each pixel (81 by default), so they are much
slower to evaluate than their PSF counterparts. On a 7 x 7 pixel cutout,
which is typical for PSF fitting, [`MoffatPRF`](../api/photutils.psf.MoffatPRF.html#photutils.psf.MoffatPRF "photutils.psf.MoffatPRF") takes about
0.05 ms to evaluate and [`AiryDiskPRF`](../api/photutils.psf.AiryDiskPRF.html#photutils.psf.AiryDiskPRF "photutils.psf.AiryDiskPRF") about 0.08 ms,
which is about 10 times slower than [`MoffatPSF`](../api/photutils.psf.MoffatPSF.html#photutils.psf.MoffatPSF "photutils.psf.MoffatPSF") (0.005
ms) and [`AiryDiskPSF`](../api/photutils.psf.AiryDiskPSF.html#photutils.psf.AiryDiskPSF "photutils.psf.AiryDiskPSF") (0.009 ms). On a 101 x 101 pixel
image they take about 7 ms and 13 ms, which is about 70 times slower
than the PSF models (0.1 ms and 0.2 ms). A smaller `n_nodes` reduces
the time at the cost of accuracy.

If one needs a custom PRF model based on an analytical PSF
model that has no PRF counterpart, evaluate the PSF model on
an oversampled grid (a Moffat profile is used below only as an
illustration) and integrate the result over the detector pixels
with [`make_epsf_from_psf`](../api/photutils.psf.make_epsf_from_psf.html#photutils.psf.make_epsf_from_psf "photutils.psf.make_epsf_from_psf"). The resulting image
can then be used as the input to [`ImagePSF`](../api/photutils.psf.ImagePSF.html#photutils.psf.ImagePSF "photutils.psf.ImagePSF") (see
[Image-based PSF Models](#psf-image-models) below) with the same oversampling factor to
create an image-based PSF model:

```
>>> import numpy as np
>>> from photutils.psf import ImagePSF, MoffatPSF, make_epsf_from_psf
>>> oversampling = 4
>>> yy, xx = np.mgrid[-50:51, -50:51] / oversampling
>>> psf = MoffatPSF(alpha=1.2, beta=2.5)(xx, yy)
>>> epsf = make_epsf_from_psf(psf, oversampling=oversampling)
>>> model = ImagePSF(epsf, oversampling=oversampling)

```

The values of the oversampled PSF model sum to the square of the
oversampling factor, apart from the flux outside of the grid, which is
the normalization that [`ImagePSF`](../api/photutils.psf.ImagePSF.html#photutils.psf.ImagePSF "photutils.psf.ImagePSF") requires. Discretizing
the model on the detector pixel grid with
[`discretize_model()`](https://docs.astropy.org/en/stable/api/astropy.convolution.discretize_model.html#astropy.convolution.discretize_model "(in Astropy v8.0)") (with
`mode='oversample'` or `mode='integrate'`) also gives a
pixel-integrated image, but only for one subpixel position of the
source. A model made from that image is not accurate at other
positions unless the PSF is well sampled.

Note that all of the analytic models above have additional shape
parameters beyond the standard PSF model parameters of position and
flux (`x_0`, `y_0`, and `flux`), which are fixed by default as
described above.

### Custom PSF Models[#](#custom-psf-models "Link to this heading")

It is recommended that one use the PSF models provided by
[`photutils.psf`](../reference/psf_api.html#module-photutils.psf "photutils.psf") because they are optimized for PSF photometry. If a
different PSF profile is needed, there are two ways to make a model for
it.

If the shape of the PSF is known and does not need to be fit, evaluate
the profile on an oversampled grid and use the result to make an
image-based model with [`make_epsf_from_psf()`](../api/photutils.psf.make_epsf_from_psf.html#photutils.psf.make_epsf_from_psf "photutils.psf.make_epsf_from_psf") and
[`ImagePSF`](../api/photutils.psf.ImagePSF.html#photutils.psf.ImagePSF "photutils.psf.ImagePSF"), as shown above for the Moffat profile. This
is the recommended approach because the resulting model is integrated
over the detector pixels.

If the shape parameters of the PSF need to be fit, define a model with
the Astropy modeling framework. The PSF photometry classes accept any
[`Fittable2DModel`](https://docs.astropy.org/en/stable/api/astropy.modeling.Fittable2DModel.html#astropy.modeling.Fittable2DModel "(in Astropy v8.0)") that has parameters named `x_0`,
`y_0`, and `flux`. The model must be normalized so that `flux` is
the total flux of the source for any values of the shape parameters. For
example, a PSF model that is the sum of two circular Gaussians with the
same center:

```
>>> import numpy as np
>>> from astropy.modeling import Fittable2DModel, Parameter
>>> class DoubleGaussianPSF(Fittable2DModel):
...     flux = Parameter(default=1.0)
...     x_0 = Parameter(default=0.0)
...     y_0 = Parameter(default=0.0)
...     sigma_core = Parameter(default=1.0, fixed=True)
...     sigma_wing = Parameter(default=3.0, fixed=True)
...     wing_ratio = Parameter(default=0.1, fixed=True)
...
...     @staticmethod
...     def evaluate(x, y, flux, x_0, y_0, sigma_core, sigma_wing,
...                  wing_ratio):
...         r2 = (x - x_0)**2 + (y - y_0)**2
...         core = np.exp(-0.5 * r2 / sigma_core**2)
...         wing = wing_ratio * np.exp(-0.5 * r2 / sigma_wing**2)
...         norm = 2.0 * np.pi * (sigma_core**2
...                               + wing_ratio * sigma_wing**2)
...         return flux * (core + wing) / norm

>>> model = DoubleGaussianPSF(sigma_core=1.2, sigma_wing=3.5)

```

This model is evaluated at the input positions and is not integrated
over the detector pixels, so it has the same limitations as the `*PSF`
models described above. It is sharper than the sources in the data,
and its fitted fluxes are biased unless the PSF is well sampled by the
detector pixels. For accurate photometry, the `evaluate` method should
instead return the profile integrated over each pixel, as the `*PRF`
models provided by [`photutils.psf`](../reference/psf_api.html#module-photutils.psf "photutils.psf") do.

A model whose position and flux parameters have other names can also be
used if it has `x_name`, `y_name`, and `flux_name` attributes that
contain the names of those parameters.

The [`make_psf_model()`](../api/photutils.psf.make_psf_model.html#photutils.psf.make_psf_model "photutils.psf.make_psf_model") function, which wraps an
Astropy fittable 2D model in a compound model, is deprecated and will be
removed in version 4.0. Use one of the two approaches above instead.

### Image-based PSF Models[#](#image-based-psf-models "Link to this heading")

Image-based PSF models are typically derived from observed data or from
detailed optical modeling. The PSF model can be a single PSF model for
the entire image or a grid of PSF models at fiducial detector positions,
which are then interpolated for specific locations.

The model classes below provide the tools needed to perform PSF
photometry within Photutils using the Astropy modeling and fitting
framework. The user must provide the image-based PSF model as an input
to these classes. The input image(s) can be oversampled to increase the
accuracy of the PSF model.

* [`ImagePSF`](../api/photutils.psf.ImagePSF.html#photutils.psf.ImagePSF "photutils.psf.ImagePSF"): a general class for image-based PSF models
  that allows for intensity scaling and translations.
* [`GriddedPSFModel`](../api/photutils.psf.GriddedPSFModel.html#photutils.psf.GriddedPSFModel "photutils.psf.GriddedPSFModel"): a PSF model that contains a grid of
  image-based ePSF models at fiducial detector positions.

These models interpolate the input image(s) and do not integrate them
over the detector pixels. The input must therefore be an effective
PSF (ePSF), in which each value is the fraction of the source flux
that falls in a whole detector pixel centered at that position
relative to the source. An oversampled PSF whose values are samples
of the PSF, such as the output of an optical model, is not an ePSF.
A model made from such an image is sharper than the sources in the
data. If the PSF is also undersampled by the detector pixels, the sum
of the model over the detector pixels changes with the subpixel
position of the source. Use [`make_epsf_from_psf`](../api/photutils.psf.make_epsf_from_psf.html#photutils.psf.make_epsf_from_psf "photutils.psf.make_epsf_from_psf") to
make an ePSF from a sampled PSF:

```
>>> from photutils.psf import ImagePSF, make_epsf_from_psf
>>> epsf = make_epsf_from_psf(psf, oversampling=4)
>>> model = ImagePSF(epsf, oversampling=4)

```

An optical model with an even oversampling factor typically returns
an image with an even number of points along each axis, with the PSF
centered between the four central grid points. The image-based models
accept such an image, and the ePSF made from it, as they are. If an
ePSF with the PSF center on a grid point is needed, for example to
compare it with an ePSF made by [`EPSFBuilder`](../api/photutils.psf.EPSFBuilder.html#photutils.psf.EPSFBuilder "photutils.psf.EPSFBuilder"), use the
`midpoints=True` option of [`make_epsf_from_psf`](../api/photutils.psf.make_epsf_from_psf.html#photutils.psf.make_epsf_from_psf "photutils.psf.make_epsf_from_psf"). It
makes the ePSF at the points midway between the input grid points, so
the output image has one fewer point along each axis.

The gridded ePSF models that [STPSF](https://stpsf.readthedocs.io/)
makes with its `psf_grid` method (see
[`webbpsf_reader`](../api/photutils.psf.webbpsf_reader.html#photutils.psf.webbpsf_reader "photutils.psf.webbpsf_reader")) are already integrated over the
detector pixels, so [`make_epsf_from_psf`](../api/photutils.psf.make_epsf_from_psf.html#photutils.psf.make_epsf_from_psf "photutils.psf.make_epsf_from_psf") must not be
applied to them. STPSF integrates the sampled PSF with a discrete box
kernel, however, which is a low-order approximation of the integral.
In tests with STPSF 2.2.0 and an oversampling factor of 4, the ePSF
peak was too low by 2.5%, 1.1%, and 0.9% for the JWST NIRCam F115W,
F200W, and F444W filters, and the fluxes fitted with these models
to stars made from an accurate ePSF were too high by 1.3%, 0.6%,
and 0.5%. With an oversampling factor of 5 the errors were about a
third as large and had the opposite sign. When that accuracy matters,
make the ePSF from the oversampled PSF that the STPSF `calc_psf`
method returns, which is sampled at the grid points:

```
import stpsf
from photutils.psf import ImagePSF, make_epsf_from_psf

nrc = stpsf.NIRCam()
nrc.filter = 'F115W'
oversampling = 4
hdulist = nrc.calc_psf(fov_pixels=101, oversample=oversampling)
psf = hdulist['OVERDIST'].data * oversampling**2
epsf = make_epsf_from_psf(psf, oversampling=oversampling)
model = ImagePSF(epsf, oversampling=oversampling)

```

The values that `calc_psf` returns sum to the fraction of the flux
that is inside the field of view, so multiplying them by the square
of the oversampling factor gives the normalization that
[`ImagePSF`](../api/photutils.psf.ImagePSF.html#photutils.psf.ImagePSF "photutils.psf.ImagePSF") requires.

An image-based model is zero outside of its input image, so the flux
of the PSF wings beyond the image is not in the model. The sum of
the model over the detector pixels is then smaller than the model
flux, and it changes with the subpixel position of the source because
the number of detector pixels inside the image changes. For a
simulated JWST NIRCam F115W ePSF, the sum changes by up to 2.5% for
an image that covers 6x6 detector pixels and by up to 0.6% for one
that covers 16x16 pixels. The ePSF image should therefore be large
enough that the ePSF is small at its edges. The fluxes and positions
fitted by the PSF photometry classes are not affected if the fitted
region of each source is well inside the image, but the model and
residual images do not include the flux outside of it.

PSF Photometry Examples[#](#psf-photometry-examples "Link to this heading")
---------------------------------------------------------------------------

Let’s start with a simple example using simulated stars whose PSF is
assumed to be Gaussian. We’ll create a synthetic image using tools
provided by the [`photutils.psf`](../reference/psf_api.html#module-photutils.psf "photutils.psf") and [photutils.datasets](datasets.html#datasets)
modules:

```
>>> import numpy as np
>>> from photutils.datasets import make_noise_image
>>> from photutils.psf import CircularGaussianPRF, make_psf_model_image
>>> psf_model = CircularGaussianPRF(flux=1, fwhm=2.7)
>>> psf_shape = (9, 9)
>>> n_sources = 10
>>> shape = (101, 101)
>>> data, true_params = make_psf_model_image(shape, psf_model, n_sources,
...                                          model_shape=psf_shape,
...                                          flux=(500, 700),
...                                          min_separation=10, seed=0)
>>> noise = make_noise_image(data.shape, mean=0, stddev=1, seed=0)
>>> data += noise
>>> error = np.full(data.shape, 1.0)

```

Let’s plot the image:

([`Source code`](../_downloads/2dbdd9b7c304bc0e2e1351613f7d515e/psf-1.py), [`png`](../_downloads/b5c129ec82c29dfae2043c31d1e9c1a0/psf-1.png), [`hires.png`](../_downloads/bbb21055e82ea7172c77d5e9848a90be/psf-1.hires.png), [`pdf`](../_downloads/72f4ea29001ad9c60ff97704d34a5804/psf-1.pdf), [`svg`](../_downloads/59e3cf7cc1f1f0f6b2bc965ed5a2bc02/psf-1.svg))

![../_images/psf-1.png](../_images/psf-1.png)

### Fitting Multiple Sources[#](#fitting-multiple-sources "Link to this heading")

Now let’s use [`PSFPhotometry`](../api/photutils.psf.PSFPhotometry.html#photutils.psf.PSFPhotometry "photutils.psf.PSFPhotometry") to perform PSF photometry
on the sources in this image. Note that the input image must be
background-subtracted prior to using the photometry classes. See
[Background Estimation (photutils.background)](background.html#background) for tools to subtract a global background from an
image. This step is not needed for our synthetic image because it does
not include background.

We’ll use the [`DAOStarFinder`](../api/photutils.detection.DAOStarFinder.html#photutils.detection.DAOStarFinder "photutils.detection.DAOStarFinder") class for
source detection. We’ll estimate the initial fluxes of each
source using a circular aperture with a radius of 4 pixels. The
central 5x5 pixel region of each source will be fit using a
[`CircularGaussianPRF`](../api/photutils.psf.CircularGaussianPRF.html#photutils.psf.CircularGaussianPRF "photutils.psf.CircularGaussianPRF") PSF model. First, let’s create an
instance of the [`PSFPhotometry`](../api/photutils.psf.PSFPhotometry.html#photutils.psf.PSFPhotometry "photutils.psf.PSFPhotometry") class:

```
>>> from photutils.detection import DAOStarFinder
>>> from photutils.psf import PSFPhotometry
>>> psf_model = CircularGaussianPRF(flux=1, fwhm=2.7)
>>> fit_shape = (5, 5)
>>> finder = DAOStarFinder(6.0, 2.0)
>>> psfphot = PSFPhotometry(psf_model, fit_shape, finder=finder,
...                         aperture_radius=4)

```

To perform the PSF fitting, we then call the class instance
on the data array, and optionally an error and mask array. A
[`NDData`](https://docs.astropy.org/en/stable/api/astropy.nddata.NDData.html#astropy.nddata.NDData "(in Astropy v8.0)") object holding the data, error, and mask arrays
can also be input into the `data` parameter. Note that all nonfinite
(e.g., NaN or inf) data values are automatically masked. Here we input
the data and error arrays:

```
>>> phot = psfphot(data, error=error)

```

A table of initial PSF model parameter values can also be input when
calling the class instance. An example of that is shown later.

Equivalently, one can input an [`NDData`](https://docs.astropy.org/en/stable/api/astropy.nddata.NDData.html#astropy.nddata.NDData "(in Astropy v8.0)") object with any
uncertainty object that can be converted to standard-deviation errors:

```
>>> from astropy.nddata import NDData, StdDevUncertainty
>>> uncertainty = StdDevUncertainty(error)
>>> nddata = NDData(data, uncertainty=uncertainty)
>>> phot2 = psfphot(nddata)

```

The result is an Astropy [`QTable`](https://docs.astropy.org/en/stable/api/astropy.table.QTable.html#astropy.table.QTable "(in Astropy v8.0)") with columns for the
source and group identification numbers, the x, y, and flux initial,
fit, and error values, local background, number of unmasked pixels
fit, the group size, quality-of-fit metrics, and flags. See the
[`PSFPhotometry`](../api/photutils.psf.PSFPhotometry.html#photutils.psf.PSFPhotometry "photutils.psf.PSFPhotometry") documentation for descriptions of the
output columns.

The full table cannot be shown here as it has many columns, but let’s
print the source ID along with the fit x, y, and flux values:

```
>>> phot['x_fit'].info.format = '.4f'  # optional format
>>> phot['y_fit'].info.format = '.4f'
>>> phot['flux_fit'].info.format = '.4f'
>>> print(phot[('id', 'x_fit', 'y_fit', 'flux_fit')])
 id  x_fit   y_fit  flux_fit
--- ------- ------- --------
  1 54.5716  7.7458 513.2209
  2 29.0873 25.6223 534.1826
  3 79.6336 28.7482 619.7632
  4 63.2403 48.6157 560.0202
  5 88.8816 54.1347 616.2282
  6 79.8673 61.1302 650.1411
  7 90.9502 72.0862 597.1119
  8  7.8034 78.5703 638.4794
  9  5.5219 89.8622 542.6817
 10 71.8331 90.5734 692.6518

```

Let’s create the residual image:

```
>>> resid = psfphot.make_residual_image(data)

```

and plot it:

([`Source code`](../_downloads/3f9a84d98c722a2e2f0ace78a989ad47/psf-2.py), [`png`](../_downloads/1131c93d2270cb6e3d039ff2a8837774/psf-2.png), [`hires.png`](../_downloads/e6f9f83ce05e57f26ceaec2a26afb913/psf-2.hires.png), [`pdf`](../_downloads/f9432eb2d225148125944aaca876067b/psf-2.pdf), [`svg`](../_downloads/2bbf31f89e73d71b4db009339fee0ce6/psf-2.svg))

![../_images/psf-2.png](../_images/psf-2.png)

The residual image looks like noise, indicating good fits to the
sources.

Further details about the PSF fitting can be obtained from attributes on
the [`PSFPhotometry`](../api/photutils.psf.PSFPhotometry.html#photutils.psf.PSFPhotometry "photutils.psf.PSFPhotometry") instance. For example, the results
from the `finder` instance called during PSF fitting can be accessed
using the `finder_results` attribute (the `finder` returns an
Astropy table):

```
>>> psfphot.finder_results['x_centroid'].info.format = '.4f'  # optional format
>>> psfphot.finder_results['y_centroid'].info.format = '.4f'
>>> psfphot.finder_results['sharpness'].info.format = '.4f'
>>> psfphot.finder_results['peak'].info.format = '.4f'
>>> psfphot.finder_results['flux'].info.format = '.4f'
>>> psfphot.finder_results['mag'].info.format = '.4f'
>>> psfphot.finder_results['daofind_mag'].info.format = '.4f'
>>> print(psfphot.finder_results)
 id x_centroid y_centroid sharpness ...   peak    flux     mag   daofind_mag
--- ---------- ---------- --------- ... ------- -------- ------- -----------
  1    54.5299     7.7460    0.6006 ... 53.5953 374.4040 -6.4334     -2.1093
  2    29.0927    25.5992    0.5955 ... 57.1982 397.4367 -6.4982     -2.1958
  3    79.6185    28.7515    0.5957 ... 65.7175 458.8443 -6.6542     -2.3401
  4    63.2485    48.6134    0.5802 ... 58.3985 414.0679 -6.5427     -2.2209
  5    88.8820    54.1311    0.5948 ... 69.1869 467.3428 -6.6741     -2.4379
  6    79.8727    61.1208    0.6216 ... 74.0935 493.8497 -6.7340     -2.4799
  7    90.9621    72.0803    0.6167 ... 68.4157 455.3896 -6.6460     -2.4035
  8     7.7962    78.5465    0.5979 ... 66.2173 472.3818 -6.6857     -2.3167
  9     5.5858    89.8664    0.5741 ... 54.3786 396.0783 -6.4945     -2.1188
 10    71.8303    90.5624    0.6038 ... 73.5747 512.3211 -6.7739     -2.4516

```

### Fitting a Single Source[#](#fitting-a-single-source "Link to this heading")

In some cases, one may want to fit only a single source (or a few
sources) in an image. We can do that by defining a table of the sources
that we want to fit. For this example, let’s fit the single source at
`(x, y) = (63, 49)`. We first define a table with this position and
then pass that table into the `init_params` keyword when calling the
PSF photometry class on the data:

```
>>> from astropy.table import QTable
>>> init_params = QTable()
>>> init_params['x'] = [63]
>>> init_params['y'] = [49]
>>> phot = psfphot(data, error=error, init_params=init_params)

```

The PSF photometry class allows for flexible input column names
using a heuristic to identify the x, y, and flux columns. See
[`PSFPhotometry`](../api/photutils.psf.PSFPhotometry.html#photutils.psf.PSFPhotometry "photutils.psf.PSFPhotometry") for more details.

The output table contains only the fit results for the input source:

```
>>> phot['x_fit'].info.format = '.4f'  # optional format
>>> phot['y_fit'].info.format = '.4f'
>>> phot['flux_fit'].info.format = '.4f'
>>> print(phot[('id', 'x_fit', 'y_fit', 'flux_fit')])
 id  x_fit   y_fit  flux_fit
--- ------- ------- --------
  1 63.2403 48.6157 560.0201

```

Finally, let’s show the residual image. The red circular aperture shows
the location of the source that was fit and subtracted.

([`Source code`](../_downloads/8df56d4699795b927db4c7f7617bc579/psf-3.py), [`png`](../_downloads/e2e8785bf7910a65dd346565e5205390/psf-3.png), [`hires.png`](../_downloads/6c00fd1e3d841ca85e1f1970917a1e94/psf-3.hires.png), [`pdf`](../_downloads/4088c30a7a4e408d3431e322b98b7c56/psf-3.pdf), [`svg`](../_downloads/d4a1c953ecce173dc1968bd9d2a62e52/psf-3.svg))

![../_images/psf-3.png](../_images/psf-3.png)

### Forced Photometry (Fixed Model Parameters)[#](#forced-photometry-fixed-model-parameters "Link to this heading")

In general, the three parameters fit for each source are the x and
y positions and the flux. However, the Astropy modeling and fitting
framework allows any of these parameters to be fixed during the fitting.

Let’s say you want to fix the (x, y) position for each source. You can
do that by setting the `fixed` attribute on the model parameters:

```
>>> psf_model2 = CircularGaussianPRF(flux=1, fwhm=2.7)
>>> psf_model2.x_0.fixed = True
>>> psf_model2.y_0.fixed = True
>>> psf_model2.fixed
{'flux': False, 'x_0': True, 'y_0': True, 'fwhm': True}

```

Now when the model is fit, the flux will be varied, but the (x, y)
position will be fixed at its initial position for every source. Let’s
just fit a single source (defined in `init_params`):

```
>>> psfphot = PSFPhotometry(psf_model2, fit_shape, finder=finder,
...                         aperture_radius=4)
>>> phot = psfphot(data, error=error, init_params=init_params)

```

The output table shows that the (x, y) position was unchanged, with the
fit values being identical to the initial values. However, the flux was
fit:

```
>>> phot['flux_init'].info.format = '.4f'  # optional format
>>> phot['flux_fit'].info.format = '.4f'
>>> print(phot[('id', 'x_init', 'y_init', 'flux_init', 'x_fit',
...             'y_fit', 'flux_fit')])
 id x_init y_init flux_init x_fit y_fit flux_fit
--- ------ ------ --------- ----- ----- --------
  1     63     49  556.5067  63.0  49.0 539.4673

```

### Bounded Model Parameters[#](#bounded-model-parameters "Link to this heading")

The Astropy modeling and fitting framework also allows for bounding the
parameter values during the fitting process. However, not all Astropy
“Fitter” classes support parameter bounds. Please see [Fitting Models to
Data](https://docs.astropy.org/en/stable/modeling/fitting.html) for
more details.

The model parameter bounds apply to all sources in the image,
thus this mechanism cannot be used to bound the x and y positions
of individual sources. However, the x and y positions can be
bounded for individual sources during the fitting by using the
`xy_bounds` keyword in [`PSFPhotometry`](../api/photutils.psf.PSFPhotometry.html#photutils.psf.PSFPhotometry "photutils.psf.PSFPhotometry") and
[`IterativePSFPhotometry`](../api/photutils.psf.IterativePSFPhotometry.html#photutils.psf.IterativePSFPhotometry "photutils.psf.IterativePSFPhotometry"). This keyword accepts a float
or a 2-tuple of floats in `(x, y)` order representing the maximum
distance in pixels that a fitted source can be from its initial (x, y)
position.

For example, you may want to constrain the flux of a source to be
between certain values or ensure that it is a nonnegative value. This
can be done by setting the `bounds` attribute on the input PSF model
parameters. Here we constrain the flux to be greater than or equal to
0:

```
>>> psf_model3 = CircularGaussianPRF(flux=1, fwhm=2.7)
>>> psf_model3.flux.bounds = (0, None)
>>> psf_model3.bounds
{'flux': (0.0, None), 'x_0': (None, None), 'y_0': (None, None), 'fwhm': (1.1754943508222875e-38, None)}

```

The model parameter `bounds` can also be set using the `min` and/or
`max` attributes. Here we set the minimum flux to be 0:

```
>>> psf_model3.flux.min = 0
>>> psf_model3.bounds
{'flux': (0.0, None), 'x_0': (None, None), 'y_0': (None, None), 'fwhm': (1.1754943508222875e-38, None)}

```

For this example, let’s constrain the flux value to be between
400 and 600:

```
>>> psf_model3 = CircularGaussianPRF(flux=1, fwhm=2.7)
>>> psf_model3.flux.bounds = (400, 600)
>>> psf_model3.bounds
{'flux': (400.0, 600.0), 'x_0': (None, None), 'y_0': (None, None), 'fwhm': (1.1754943508222875e-38, None)}

```

### Source Grouping[#](#source-grouping "Link to this heading")

Source grouping is an optional feature. To turn it on, create a
[`SourceGrouper`](../api/photutils.psf.SourceGrouper.html#photutils.psf.SourceGrouper "photutils.psf.SourceGrouper") instance and input it via the `grouper`
keyword. Here we’ll group sources that are within 20 pixels of each
other:

```
>>> from photutils.psf import SourceGrouper
>>> grouper = SourceGrouper(min_separation=20)
>>> psfphot = PSFPhotometry(psf_model, fit_shape, finder=finder,
...                         grouper=grouper, aperture_radius=4)
>>> phot = psfphot(data, error=error)

```

The `group_id` column shows that seven groups were identified. The
sources in each group were simultaneously fit:

```
>>> print(phot[('id', 'group_id', 'group_size')])
 id group_id group_size
--- -------- ----------
  1        1          1
  2        2          1
  3        3          1
  4        4          1
  5        5          3
  6        5          3
  7        5          3
  8        6          2
  9        6          2
 10        7          1

```

Care should be taken in defining the source groups. Simultaneously
fitting very large source groups is computationally expensive and
error-prone, because the number of fitted parameters grows with the
group size. A warning will be raised if the number of sources in a group
exceeds a threshold defined by the `group_warning_threshold` keyword.

### Local Background Subtraction[#](#local-background-subtraction "Link to this heading")

To subtract a local background from each source, define a
[`LocalBackground`](../api/photutils.background.LocalBackground.html#photutils.background.LocalBackground "photutils.background.LocalBackground") instance and input it via
the `local_bkg_estimator` keyword. Here we’ll use an annulus with
an inner and outer radius of 5 and 10 pixels, respectively, with the
[`MMMBackground`](../api/photutils.background.MMMBackground.html#photutils.background.MMMBackground "photutils.background.MMMBackground") statistic (with its default sigma
clipping):

```
>>> from photutils.background import LocalBackground, MMMBackground
>>> bkgstat = MMMBackground()
>>> local_bkg_estimator = LocalBackground(5, 10, bkg_estimator=bkgstat)
>>> finder = DAOStarFinder(10.0, 2.0)
>>> psfphot = PSFPhotometry(psf_model, fit_shape, finder=finder,
...                         grouper=grouper, aperture_radius=4,
...                         local_bkg_estimator=local_bkg_estimator)
>>> phot = psfphot(data, error=error)

```

The local background values are output in the table:

```
>>> phot['local_bkg'].info.format = '.4f'  # optional format
>>> print(phot[('id', 'local_bkg')])
 id local_bkg
--- ---------
  1   -0.0839
  2    0.1784
  3    0.2593
  4   -0.0574
  5    0.2492
  6   -0.0818
  7   -0.1130
  8   -0.2166
  9    0.0102
 10    0.3926

```

The local background values can also be input directly using the
`init_params` keyword.

### Iterative PSF Photometry[#](#iterative-psf-photometry "Link to this heading")

Now let’s use the [`IterativePSFPhotometry`](../api/photutils.psf.IterativePSFPhotometry.html#photutils.psf.IterativePSFPhotometry "photutils.psf.IterativePSFPhotometry") class to
iteratively fit the sources in the image. This class is useful for
crowded fields where faint sources are very close to bright sources. The
faint sources may not be detected until after the bright sources are
subtracted.

For this simple example, let’s input a table of three sources for the
first fit iteration. Subsequent iterations will use the `finder` to
find additional sources:

```
>>> from photutils.background import LocalBackground, MMMBackground
>>> from photutils.psf import IterativePSFPhotometry
>>> fit_shape = (5, 5)
>>> finder = DAOStarFinder(10.0, 2.0)
>>> bkgstat = MMMBackground()
>>> local_bkg_estimator = LocalBackground(5, 10, bkg_estimator=bkgstat)
>>> init_params = QTable()
>>> init_params['x'] = [54, 29, 80]
>>> init_params['y'] = [8, 26, 29]
>>> psfphot2 = IterativePSFPhotometry(psf_model, fit_shape, finder=finder,
...                                   local_bkg_estimator=local_bkg_estimator,
...                                   aperture_radius=4)
>>> phot = psfphot2(data, error=error, init_params=init_params)

```

The table output from [`IterativePSFPhotometry`](../api/photutils.psf.IterativePSFPhotometry.html#photutils.psf.IterativePSFPhotometry "photutils.psf.IterativePSFPhotometry") contains a
column called `iter_detected` that returns the fit iteration in which
the source was detected:

```
>>> phot['x_fit'].info.format = '.4f'  # optional format
>>> phot['y_fit'].info.format = '.4f'
>>> phot['flux_fit'].info.format = '.4f'
>>> print(phot[('id', 'iter_detected', 'x_fit', 'y_fit', 'flux_fit')])
 id iter_detected  x_fit   y_fit  flux_fit
--- ------------- ------- ------- --------
  1             1 54.5694  7.7454 513.4505
  2             1 29.0875 25.6216 531.3096
  3             1 79.6327 28.7475 615.1111
  4             2 63.2401 48.6159 560.9633
  5             2 88.8813 54.1350 612.0937
  6             2 79.8674 61.1301 651.4973
  7             2 90.9502 72.0861 598.9888
  8             2  7.8037 78.5711 642.0335
  9             2  5.5218 89.8621 542.5141
 10             2 71.8326 90.5721 686.2071

```

Estimating the FWHM of Sources[#](#estimating-the-fwhm-of-sources "Link to this heading")
-----------------------------------------------------------------------------------------

The [`photutils.psf`](../reference/psf_api.html#module-photutils.psf "photutils.psf") package also provides a convenience
function called [`fit_fwhm`](../api/photutils.psf.fit_fwhm.html#photutils.psf.fit_fwhm "photutils.psf.fit_fwhm") to estimate the
full width at half maximum (FWHM) of one or more sources in
an image. This function fits the source(s) with a circular
2D Gaussian PRF model ([`CircularGaussianPRF`](../api/photutils.psf.CircularGaussianPRF.html#photutils.psf.CircularGaussianPRF "photutils.psf.CircularGaussianPRF"))
using the [`PSFPhotometry`](../api/photutils.psf.PSFPhotometry.html#photutils.psf.PSFPhotometry "photutils.psf.PSFPhotometry") class. If your sources
are noncircular or non-Gaussian, you can fit them with the
[`PSFPhotometry`](../api/photutils.psf.PSFPhotometry.html#photutils.psf.PSFPhotometry "photutils.psf.PSFPhotometry") class and a different PSF model. Because
the model is integrated over the pixels, the returned FWHM is the FWHM
of the Gaussian before that integration, which is smaller than the
FWHM of the pixelated image of a source. The integration over a pixel
adds 1/12 pixel\*\*2 to the variance of the profile, so the FWHM of the
pixelated image is approximately `sqrt(fwhm**2 + 8 * ln(2) / 12)`, or
`sqrt(fwhm**2 + 0.462)`, in pixels.

For example, let’s estimate the FWHM of the sources in our example image
defined above:

```
>>> from photutils.psf import fit_fwhm
>>> finder = DAOStarFinder(6.0, 2.0)
>>> finder_tbl = finder(data)
>>> xypos = list(zip(finder_tbl['x_centroid'],
...                  finder_tbl['y_centroid'], strict=True))
>>> fwhm = fit_fwhm(data, xypos=xypos, error=error, fit_shape=(5, 5),
...                 fwhm=2)
>>> print(fwhm)
[2.70583788 2.71009672 2.67319671 2.69326964 2.66743315 2.69499684
 2.68722492 2.73280668 2.72006396 2.68340929]

```

The FWHM of the pixelated image of each source is then:

```
>>> fwhm_pixelated = np.sqrt(fwhm**2 + 8 * np.log(2) / 12)
>>> print(fwhm_pixelated)
[2.78992056 2.79405124 2.7582746  2.7777328  2.75268918 2.7794075
 2.77187227 2.81608425 2.80372005 2.76817332]

```

Convenience Gaussian Fitting Function[#](#convenience-gaussian-fitting-function "Link to this heading")
-------------------------------------------------------------------------------------------------------

The [`photutils.psf`](../reference/psf_api.html#module-photutils.psf "photutils.psf") package also provides a convenience function called
[`fit_2dgaussian()`](../api/photutils.psf.fit_2dgaussian.html#photutils.psf.fit_2dgaussian "photutils.psf.fit_2dgaussian") for fitting one or more sources
with a 2D Gaussian PRF model ([`CircularGaussianPRF`](../api/photutils.psf.CircularGaussianPRF.html#photutils.psf.CircularGaussianPRF "photutils.psf.CircularGaussianPRF"))
using the [`PSFPhotometry`](../api/photutils.psf.PSFPhotometry.html#photutils.psf.PSFPhotometry "photutils.psf.PSFPhotometry") class. See the function
documentation for more details and examples.

API Reference[#](#api-reference "Link to this heading")
-------------------------------------------------------

[PSF Photometry (photutils.psf)](../reference/psf_api.html)

[previous

Aperture Photometry (`photutils.aperture`)](aperture.html "previous page")
[next

Building an Effective Point Spread Function (ePSF)](epsf_building.html "next page")

On this page

* [PSF Photometry Overview](#psf-photometry-overview)
* [Terminology](#terminology)
* [PSF Models](#psf-models)
  + [Analytic PSF Models](#analytic-psf-models)
  + [Custom PSF Models](#custom-psf-models)
  + [Image-based PSF Models](#image-based-psf-models)
* [PSF Photometry Examples](#psf-photometry-examples)
  + [Fitting Multiple Sources](#fitting-multiple-sources)
  + [Fitting a Single Source](#fitting-a-single-source)
  + [Forced Photometry (Fixed Model Parameters)](#forced-photometry-fixed-model-parameters)
  + [Bounded Model Parameters](#bounded-model-parameters)
  + [Source Grouping](#source-grouping)
  + [Local Background Subtraction](#local-background-subtraction)
  + [Iterative PSF Photometry](#iterative-psf-photometry)
* [Estimating the FWHM of Sources](#estimating-the-fwhm-of-sources)
* [Convenience Gaussian Fitting Function](#convenience-gaussian-fitting-function)
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
- https://docs.astropy.org/en/stable/api/astropy.convolution.discretize_model.html#astropy.convolution.discretize_model
- https://docs.astropy.org/en/stable/api/astropy.modeling.Fittable2DModel.html#astropy.modeling.Fittable2DModel
- https://docs.astropy.org/en/stable/api/astropy.modeling.fitting.TRFLSQFitter.html#astropy.modeling.fitting.TRFLSQFitter
- https://docs.astropy.org/en/stable/api/astropy.nddata.NDData.html#astropy.nddata.NDData
- https://docs.astropy.org/en/stable/api/astropy.table.QTable.html#astropy.table.QTable
- https://docs.astropy.org/en/stable/modeling/fitting.html
- https://docs.astropy.org/en/stable/modeling/index.html#astropy-modeling
- https://docs.astropy.org/projects/photutils/en/stable/_downloads/1131c93d2270cb6e3d039ff2a8837774/psf-2.png
- https://docs.astropy.org/projects/photutils/en/stable/_downloads/2bbf31f89e73d71b4db009339fee0ce6/psf-2.svg
- https://docs.astropy.org/projects/photutils/en/stable/_downloads/2dbdd9b7c304bc0e2e1351613f7d515e/psf-1.py
- https://docs.astropy.org/projects/photutils/en/stable/_downloads/3f9a84d98c722a2e2f0ace78a989ad47/psf-2.py
- https://docs.astropy.org/projects/photutils/en/stable/_downloads/4088c30a7a4e408d3431e322b98b7c56/psf-3.pdf
- https://docs.astropy.org/projects/photutils/en/stable/_downloads/59e3cf7cc1f1f0f6b2bc965ed5a2bc02/psf-1.svg
- https://docs.astropy.org/projects/photutils/en/stable/_downloads/6c00fd1e3d841ca85e1f1970917a1e94/psf-3.hires.png
- https://docs.astropy.org/projects/photutils/en/stable/_downloads/72f4ea29001ad9c60ff97704d34a5804/psf-1.pdf
- https://docs.astropy.org/projects/photutils/en/stable/_downloads/8df56d4699795b927db4c7f7617bc579/psf-3.py
- https://docs.astropy.org/projects/photutils/en/stable/_downloads/b5c129ec82c29dfae2043c31d1e9c1a0/psf-1.png
- https://docs.astropy.org/projects/photutils/en/stable/_downloads/bbb21055e82ea7172c77d5e9848a90be/psf-1.hires.png
- https://docs.astropy.org/projects/photutils/en/stable/_downloads/d4a1c953ecce173dc1968bd9d2a62e52/psf-3.svg
- https://docs.astropy.org/projects/photutils/en/stable/_downloads/e2e8785bf7910a65dd346565e5205390/psf-3.png
- https://docs.astropy.org/projects/photutils/en/stable/_downloads/e6f9f83ce05e57f26ceaec2a26afb913/psf-2.hires.png
- https://docs.astropy.org/projects/photutils/en/stable/_downloads/f9432eb2d225148125944aaca876067b/psf-2.pdf
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
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.background.LocalBackground.html#photutils.background.LocalBackground
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.background.MADStdBackgroundRMS.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.background.MMMBackground.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.background.MMMBackground.html#photutils.background.MMMBackground
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
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.AiryDiskPRF.html#photutils.psf.AiryDiskPRF
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.AiryDiskPSF.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.AiryDiskPSF.html#photutils.psf.AiryDiskPSF
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.CircularGaussianPRF.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.CircularGaussianPRF.html#photutils.psf.CircularGaussianPRF
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.CircularGaussianPSF.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.CircularGaussianPSF.html#photutils.psf.CircularGaussianPSF
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.CircularGaussianSigmaPRF.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.CircularGaussianSigmaPRF.html#photutils.psf.CircularGaussianSigmaPRF
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.EPSFBuildResults.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.EPSFBuilder.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.EPSFBuilder.html#photutils.psf.EPSFBuilder
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.EPSFFitter.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.EPSFStar.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.EPSFStars.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.GaussianPRF.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.GaussianPRF.html#photutils.psf.GaussianPRF
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.GaussianPSF.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.GaussianPSF.html#photutils.psf.GaussianPSF
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.GriddedPSFModel.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.GriddedPSFModel.html#photutils.psf.GriddedPSFModel
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.GriddedPSFModelRead.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.ImagePSF.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.ImagePSF.html#photutils.psf.ImagePSF
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.IterativePSFPhotometry.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.IterativePSFPhotometry.html#photutils.psf.IterativePSFPhotometry
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.LinkedEPSFStar.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.MoffatPRF.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.MoffatPRF.html#photutils.psf.MoffatPRF
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.MoffatPSF.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.MoffatPSF.html#photutils.psf.MoffatPSF
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.PSFPhotometry.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.PSFPhotometry.html#photutils.psf.PSFPhotometry
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.PSFPhotometry.html#photutils.psf.PSFPhotometry.make_model_image
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.PSFPhotometry.html#photutils.psf.PSFPhotometry.make_residual_image
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.STDPSFGrid.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.SourceGrouper.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.SourceGrouper.html#photutils.psf.SourceGrouper
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.SourceGroups.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.decode_psf_flags.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.extract_stars.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.fit_2dgaussian.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.fit_2dgaussian.html#photutils.psf.fit_2dgaussian
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.fit_fwhm.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.fit_fwhm.html#photutils.psf.fit_fwhm
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.grid_from_epsfs.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.make_epsf_from_psf.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.make_epsf_from_psf.html#photutils.psf.make_epsf_from_psf
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.make_psf_model.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.make_psf_model.html#photutils.psf.make_psf_model
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.make_psf_model_image.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.stdpsf_reader.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.webbpsf_reader.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.webbpsf_reader.html#photutils.psf.webbpsf_reader
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
- https://docs.astropy.org/projects/photutils/en/stable/reference/psf_api.html#module-photutils.psf
- https://docs.astropy.org/projects/photutils/en/stable/reference/psf_matching_api.html
- https://docs.astropy.org/projects/photutils/en/stable/reference/segmentation_api.html
- https://docs.astropy.org/projects/photutils/en/stable/reference/utils_api.html
- https://docs.astropy.org/projects/photutils/en/stable/release_notes/index.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/aperture.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/asdf.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/background.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/background.html#background
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/centroids.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/curves_of_growth.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/datasets.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/datasets.html#datasets
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/detection.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/epsf_building.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/epsf_building.html#build-epsf
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/geometry.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/grouping.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/grouping.html#source-grouping
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/index.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/isophote.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/isophote_faq.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/morphology.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/psf_matching.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/radial_profiles.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/segmentation.html
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
- https://docs.python.org/3/builtins/constants.html#False
- https://github.com/astropy/photutils
- https://photutils.readthedocs.io
- https://reproject.readthedocs.io
- https://specreduce.readthedocs.io
- https://specutils.readthedocs.io
- https://stpsf.readthedocs.io/
- https://ui.adsabs.harvard.edu/abs/1987PASP...99..191S/abstract
- https://ui.adsabs.harvard.edu/abs/2000PASP..112.1360A/abstract
- https://www.stsci.edu/hst
- https://www.stsci.edu/hst/instrumentation/wfc3/data-analysis/psf/psf-search
- https://www.stsci.edu/jwst
- https://www.stsci.edu/roman
