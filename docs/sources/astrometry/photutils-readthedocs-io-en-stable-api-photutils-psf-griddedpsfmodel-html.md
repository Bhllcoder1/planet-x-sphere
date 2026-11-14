---
source: https://photutils.readthedocs.io/en/stable/api/photutils.psf.GriddedPSFModel.html
fetched: 2026-11-14
status: 200
---

GriddedPSFModel — photutils 3.1.1

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
* [User Guide](../user_guide/index.html)
  + [Background Estimation (`photutils.background`)](../user_guide/background.html)
  + [Centroids (`photutils.centroids`)](../user_guide/centroids.html)
  + [Point-like Source Detection (`photutils.detection`)](../user_guide/detection.html)
  + [Image Segmentation (`photutils.segmentation`)](../user_guide/segmentation.html)
  + [Morphological Properties (`photutils.morphology`)](../user_guide/morphology.html)
  + [Aperture Photometry (`photutils.aperture`)](../user_guide/aperture.html)
  + [PSF Photometry (`photutils.psf`)](../user_guide/psf.html)
  + [Building an Effective Point Spread Function (ePSF)](../user_guide/epsf_building.html)
  + [Source Grouping](../user_guide/grouping.html)
  + [PSF Matching (`photutils.psf_matching`)](../user_guide/psf_matching.html)
  + [Radial Profiles (`photutils.profiles`)](../user_guide/radial_profiles.html)
  + [Curves of Growth (`photutils.profiles`)](../user_guide/curves_of_growth.html)
  + [Elliptical Isophote Analysis (`photutils.isophote`)](../user_guide/isophote.html)
    - [Isophote Frequently Asked Questions](../user_guide/isophote_faq.html)
  + [Datasets and Simulation (`photutils.datasets`)](../user_guide/datasets.html)
  + [ASDF Serialization](../user_guide/asdf.html)
  + [Utility Functions (`photutils.utils`)](../user_guide/utils.html)
  + [Geometry Functions (`photutils.geometry`)](../user_guide/geometry.html)
* [API Reference Guide](../reference/index.html)
  + [Aperture Photometry (`photutils.aperture`)](../reference/aperture_api.html)
    - [aperture\_photometry](photutils.aperture.aperture_photometry.html)
    - [aperture\_to\_region](photutils.aperture.aperture_to_region.html)
    - [decode\_aperture\_flags](photutils.aperture.decode_aperture_flags.html)
    - [region\_to\_aperture](photutils.aperture.region_to_aperture.html)
    - [Aperture](photutils.aperture.Aperture.html)
    - [ApertureMask](photutils.aperture.ApertureMask.html)
    - [AperturePhotometry](photutils.aperture.AperturePhotometry.html)
    - [ApertureStats](photutils.aperture.ApertureStats.html)
    - [BoundingBox](photutils.aperture.BoundingBox.html)
    - [CircularAnnulus](photutils.aperture.CircularAnnulus.html)
    - [CircularAperture](photutils.aperture.CircularAperture.html)
    - [CircularMaskMixin](photutils.aperture.CircularMaskMixin.html)
    - [EllipticalAnnulus](photutils.aperture.EllipticalAnnulus.html)
    - [EllipticalAperture](photutils.aperture.EllipticalAperture.html)
    - [EllipticalMaskMixin](photutils.aperture.EllipticalMaskMixin.html)
    - [PixelAperture](photutils.aperture.PixelAperture.html)
    - [PolygonAperture](photutils.aperture.PolygonAperture.html)
    - [RectangularAnnulus](photutils.aperture.RectangularAnnulus.html)
    - [RectangularAperture](photutils.aperture.RectangularAperture.html)
    - [RectangularMaskMixin](photutils.aperture.RectangularMaskMixin.html)
    - [SkyAperture](photutils.aperture.SkyAperture.html)
    - [SkyCircularAnnulus](photutils.aperture.SkyCircularAnnulus.html)
    - [SkyCircularAperture](photutils.aperture.SkyCircularAperture.html)
    - [SkyEllipticalAnnulus](photutils.aperture.SkyEllipticalAnnulus.html)
    - [SkyEllipticalAperture](photutils.aperture.SkyEllipticalAperture.html)
    - [SkyPolygonAperture](photutils.aperture.SkyPolygonAperture.html)
    - [SkyRectangularAnnulus](photutils.aperture.SkyRectangularAnnulus.html)
    - [SkyRectangularAperture](photutils.aperture.SkyRectangularAperture.html)
  + [Backgrounds (`photutils.background`)](../reference/background_api.html)
    - [Background2D](photutils.background.Background2D.html)
    - [BackgroundBase](photutils.background.BackgroundBase.html)
    - [BackgroundRMSBase](photutils.background.BackgroundRMSBase.html)
    - [BiweightLocationBackground](photutils.background.BiweightLocationBackground.html)
    - [BiweightScaleBackgroundRMS](photutils.background.BiweightScaleBackgroundRMS.html)
    - [BkgIDWInterpolator](photutils.background.BkgIDWInterpolator.html)
    - [BkgZoomInterpolator](photutils.background.BkgZoomInterpolator.html)
    - [LocalBackground](photutils.background.LocalBackground.html)
    - [MADStdBackgroundRMS](photutils.background.MADStdBackgroundRMS.html)
    - [MMMBackground](photutils.background.MMMBackground.html)
    - [MeanBackground](photutils.background.MeanBackground.html)
    - [MedianBackground](photutils.background.MedianBackground.html)
    - [ModeEstimatorBackground](photutils.background.ModeEstimatorBackground.html)
    - [SExtractorBackground](photutils.background.SExtractorBackground.html)
    - [StdBackgroundRMS](photutils.background.StdBackgroundRMS.html)
  + [Centroids (`photutils.centroids`)](../reference/centroids_api.html)
    - [centroid\_1dg](photutils.centroids.centroid_1dg.html)
    - [centroid\_2dg](photutils.centroids.centroid_2dg.html)
    - [centroid\_com](photutils.centroids.centroid_com.html)
    - [centroid\_quadratic](photutils.centroids.centroid_quadratic.html)
    - [centroid\_sources](photutils.centroids.centroid_sources.html)
    - [centroid\_symmetry](photutils.centroids.centroid_symmetry.html)
    - [CentroidQuadratic](photutils.centroids.CentroidQuadratic.html)
  + [Datasets and Simulation (`photutils.datasets`)](../reference/datasets_api.html)
    - [apply\_poisson\_noise](photutils.datasets.apply_poisson_noise.html)
    - [get\_path](photutils.datasets.get_path.html)
    - [load\_irac\_psf](photutils.datasets.load_irac_psf.html)
    - [load\_simulated\_hst\_star\_image](photutils.datasets.load_simulated_hst_star_image.html)
    - [load\_spitzer\_catalog](photutils.datasets.load_spitzer_catalog.html)
    - [load\_spitzer\_image](photutils.datasets.load_spitzer_image.html)
    - [load\_star\_image](photutils.datasets.load_star_image.html)
    - [make\_100gaussians\_image](photutils.datasets.make_100gaussians_image.html)
    - [make\_4gaussians\_image](photutils.datasets.make_4gaussians_image.html)
    - [make\_gwcs](photutils.datasets.make_gwcs.html)
    - [make\_model\_image](photutils.datasets.make_model_image.html)
    - [make\_model\_params](photutils.datasets.make_model_params.html)
    - [make\_noise\_image](photutils.datasets.make_noise_image.html)
    - [make\_random\_models\_table](photutils.datasets.make_random_models_table.html)
    - [make\_wcs](photutils.datasets.make_wcs.html)
    - [params\_table\_to\_models](photutils.datasets.params_table_to_models.html)
  + [Point-like Source Detection (`photutils.detection`)](../reference/detection_api.html)
    - [find\_peaks](photutils.detection.find_peaks.html)
    - [DAOStarFinder](photutils.detection.DAOStarFinder.html)
    - [IRAFStarFinder](photutils.detection.IRAFStarFinder.html)
    - [StarFinder](photutils.detection.StarFinder.html)
    - [StarFinderBase](photutils.detection.StarFinderBase.html)
    - [StarFinderCatalogBase](photutils.detection.StarFinderCatalogBase.html)
  + [Geometry Functions (`photutils.geometry`)](../reference/geometry_api.html)
    - [circular\_overlap\_grid](photutils.geometry.circular_overlap_grid.html)
    - [elliptical\_overlap\_grid](photutils.geometry.elliptical_overlap_grid.html)
    - [rectangular\_overlap\_grid](photutils.geometry.rectangular_overlap_grid.html)
  + [Elliptical Isophote Analysis (`photutils.isophote`)](../reference/isophote_api.html)
    - [build\_ellipse\_model](photutils.isophote.build_ellipse_model.html)
    - [first\_and\_second\_harmonic\_function](photutils.isophote.first_and_second_harmonic_function.html)
    - [fit\_first\_and\_second\_harmonics](photutils.isophote.fit_first_and_second_harmonics.html)
    - [fit\_upper\_harmonic](photutils.isophote.fit_upper_harmonic.html)
    - [Ellipse](photutils.isophote.Ellipse.html)
    - [EllipseFitter](photutils.isophote.EllipseFitter.html)
    - [EllipseGeometry](photutils.isophote.EllipseGeometry.html)
    - [EllipseSample](photutils.isophote.EllipseSample.html)
    - [Isophote](photutils.isophote.Isophote.html)
    - [IsophoteList](photutils.isophote.IsophoteList.html)
  + [Morphological Properties (`photutils.morphology`)](../reference/morphology_api.html)
    - [data\_properties](photutils.morphology.data_properties.html)
    - [gini](photutils.morphology.gini.html)
  + [Profiles (`photutils.profiles`)](../reference/profiles_api.html)
    - [CurveOfGrowth](photutils.profiles.CurveOfGrowth.html)
    - [EllipticalCurveOfGrowth](photutils.profiles.EllipticalCurveOfGrowth.html)
    - [EnsquaredCurveOfGrowth](photutils.profiles.EnsquaredCurveOfGrowth.html)
    - [ProfileBase](photutils.profiles.ProfileBase.html)
    - [RadialProfile](photutils.profiles.RadialProfile.html)
  + [PSF Photometry (`photutils.psf`)](../reference/psf_api.html)
    - [decode\_psf\_flags](photutils.psf.decode_psf_flags.html)
    - [extract\_stars](photutils.psf.extract_stars.html)
    - [fit\_2dgaussian](photutils.psf.fit_2dgaussian.html)
    - [fit\_fwhm](photutils.psf.fit_fwhm.html)
    - [grid\_from\_epsfs](photutils.psf.grid_from_epsfs.html)
    - [make\_epsf\_from\_psf](photutils.psf.make_epsf_from_psf.html)
    - [make\_psf\_model](photutils.psf.make_psf_model.html)
    - [make\_psf\_model\_image](photutils.psf.make_psf_model_image.html)
    - [stdpsf\_reader](photutils.psf.stdpsf_reader.html)
    - [webbpsf\_reader](photutils.psf.webbpsf_reader.html)
    - [AiryDiskPRF](photutils.psf.AiryDiskPRF.html)
    - [AiryDiskPSF](photutils.psf.AiryDiskPSF.html)
    - [CircularGaussianPRF](photutils.psf.CircularGaussianPRF.html)
    - [CircularGaussianPSF](photutils.psf.CircularGaussianPSF.html)
    - [CircularGaussianSigmaPRF](photutils.psf.CircularGaussianSigmaPRF.html)
    - [EPSFBuildResults](photutils.psf.EPSFBuildResults.html)
    - [EPSFBuilder](photutils.psf.EPSFBuilder.html)
    - [EPSFFitter](photutils.psf.EPSFFitter.html)
    - [EPSFStar](photutils.psf.EPSFStar.html)
    - [EPSFStars](photutils.psf.EPSFStars.html)
    - [GaussianPRF](photutils.psf.GaussianPRF.html)
    - [GaussianPSF](photutils.psf.GaussianPSF.html)
    - [GriddedPSFModel](#)
    - [GriddedPSFModelRead](photutils.psf.GriddedPSFModelRead.html)
    - [ImagePSF](photutils.psf.ImagePSF.html)
    - [IterativePSFPhotometry](photutils.psf.IterativePSFPhotometry.html)
    - [LinkedEPSFStar](photutils.psf.LinkedEPSFStar.html)
    - [MoffatPRF](photutils.psf.MoffatPRF.html)
    - [MoffatPSF](photutils.psf.MoffatPSF.html)
    - [PSFPhotometry](photutils.psf.PSFPhotometry.html)
    - [STDPSFGrid](photutils.psf.STDPSFGrid.html)
    - [SourceGrouper](photutils.psf.SourceGrouper.html)
    - [SourceGroups](photutils.psf.SourceGroups.html)
  + [PSF Matching (`photutils.psf_matching`)](../reference/psf_matching_api.html)
    - [create\_matching\_kernel](photutils.psf_matching.create_matching_kernel.html)
    - [make\_kernel](photutils.psf_matching.make_kernel.html)
    - [make\_wiener\_kernel](photutils.psf_matching.make_wiener_kernel.html)
    - [resize\_psf](photutils.psf_matching.resize_psf.html)
    - [CosineBellWindow](photutils.psf_matching.CosineBellWindow.html)
    - [HanningWindow](photutils.psf_matching.HanningWindow.html)
    - [SplitCosineBellWindow](photutils.psf_matching.SplitCosineBellWindow.html)
    - [TopHatWindow](photutils.psf_matching.TopHatWindow.html)
    - [TukeyWindow](photutils.psf_matching.TukeyWindow.html)
  + [Image Segmentation (`photutils.segmentation`)](../reference/segmentation_api.html)
    - [deblend\_sources](photutils.segmentation.deblend_sources.html)
    - [decode\_segmentation\_flags](photutils.segmentation.decode_segmentation_flags.html)
    - [detect\_sources](photutils.segmentation.detect_sources.html)
    - [detect\_threshold](photutils.segmentation.detect_threshold.html)
    - [make\_2dgaussian\_kernel](photutils.segmentation.make_2dgaussian_kernel.html)
    - [Segment](photutils.segmentation.Segment.html)
    - [SegmentationImage](photutils.segmentation.SegmentationImage.html)
    - [SourceCatalog](photutils.segmentation.SourceCatalog.html)
    - [SourceFinder](photutils.segmentation.SourceFinder.html)
  + [Utility Functions (`photutils.utils`)](../reference/utils_api.html)
    - [calc\_total\_error](photutils.utils.calc_total_error.html)
    - [circular\_footprint](photutils.utils.circular_footprint.html)
    - [compute\_pixel\_area\_map](photutils.utils.compute_pixel_area_map.html)
    - [compute\_pixel\_areas](photutils.utils.compute_pixel_areas.html)
    - [make\_random\_cmap](photutils.utils.make_random_cmap.html)
    - [CutoutImage](photutils.utils.CutoutImage.html)
    - [DeblendWarning](photutils.utils.DeblendWarning.html)
    - [ImageDepth](photutils.utils.ImageDepth.html)
    - [NoDetectionsWarning](photutils.utils.NoDetectionsWarning.html)
    - [PhotutilsDeprecationWarning](photutils.utils.PhotutilsDeprecationWarning.html)
    - [ShepardIDWInterpolator](photutils.utils.ShepardIDWInterpolator.html)
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

* [API Reference Guide](../reference/index.html)
* [PSF Photometry (`photutils.psf`)](../reference/psf_api.html)
* GriddedPSFModel

GriddedPSFModel[#](#griddedpsfmodel "Link to this heading")
===========================================================

class photutils.psf.GriddedPSFModel(*nddata*, *\**, *flux=1.0*, *x\_0=0.0*, *y\_0=0.0*, *fill\_value=0.0*)[[source]](../_modules/photutils/psf/gridded_models.html#GriddedPSFModel)[#](#photutils.psf.GriddedPSFModel "Link to this definition")
:   Bases: [`Fittable2DModel`](https://docs.astropy.org/en/stable/api/astropy.modeling.Fittable2DModel.html#astropy.modeling.Fittable2DModel "(in Astropy v8.0)")

    A model representing a grid of 2D ePSF models.

    The ePSF models are defined at fiducial detector locations specified
    by their `(x, y)` detector coordinates. The fiducial locations
    must form a rectangular grid.

    This model has three parameters: an image intensity scaling factor
    (`flux`), which scales the input image, and two positional
    parameters (`x_0` and `y_0`), which specify the location of the
    feature in the coordinate grid where the model is evaluated.

    When evaluating this model, the input `x` and `y` arrays must
    have no more than two dimensions.

    Parameters:
    :   **nddata**[`NDData`](https://docs.astropy.org/en/stable/api/astropy.nddata.NDData.html#astropy.nddata.NDData "(in Astropy v8.0)")
        :   A [`NDData`](https://docs.astropy.org/en/stable/api/astropy.nddata.NDData.html#astropy.nddata.NDData "(in Astropy v8.0)") object containing the reference ePSF
            grid. Its `data` attribute must be a 3D [`ndarray`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray "(in NumPy v2.5)") with
            shape `(N_psf, ePSF_ny, ePSF_nx)`, where each plane is a 2D
            ePSF image. The x and y dimensions of each ePSF image must both
            be at least 4 pixels. `N_psf` must not be 2 or 3. All values
            in `data` must be finite. The ePSF peak is assumed to be
            centered in each input image. See the Notes section for details
            on the required normalization of the input ePSF images.

            If `N_psf` is 1, the single ePSF image is used at all detector
            positions. This is equivalent to using [`ImagePSF`](photutils.psf.ImagePSF.html#photutils.psf.ImagePSF "photutils.psf.ImagePSF")
            with the same ePSF image.

            The `meta` attribute must be a dictionary containing:

            * `'grid_xypos'`: A sequence of the fiducial `(x, y)`
              detector coordinates for each reference ePSF. The order must
              match the first axis of `data`. That is, `grid_xypos[i]`
              gives the detector coordinates of `nddata.data[i]`. The
              coordinates must form a rectangular grid.
            * `'oversampling'`: The integer oversampling factor(s) of the
              input ePSF images. If a scalar is provided, it is applied to
              both axes. If two values are provided, they must be in `(y,
              x)` order.

            The `meta` dictionary may also contain additional metadata,
            such as the telescope, instrument, detector, or filter.

        **flux**float, optional
        :   The flux scaling factor. This corresponds to the total
            source flux, assuming the input ePSF images are properly
            normalized.

        **x\_0, y\_0**float, optional
        :   The `(x, y)` coordinates of the ePSF peak in the output
            coordinate grid where the model is evaluated.

        **fill\_value**float or [`None`](https://docs.python.org/3/builtins/constants.html#None "(in Python v3.15)"), optional
        :   The value used for points outside the input pixel grid. The
            default is 0.0. If [`None`](https://docs.python.org/3/builtins/constants.html#None "(in Python v3.15)"), a point outside the input pixel grid
            takes the value of the spline at the nearest point on the edge
            of the grid.

    Methods

    |  |  |
    | --- | --- |
    | **read(\*args, \*\*kwargs)** | Class method to create a [`GriddedPSFModel`](#photutils.psf.GriddedPSFModel "photutils.psf.GriddedPSFModel") instance from a STDPSF FITS file or a WebbPSF (STPSF) FITS file. The file format is identified automatically, or it can be set with the `format` keyword (`'stdpsf'` or `'webbpsf'`). This method uses [`stdpsf_reader()`](photutils.psf.stdpsf_reader.html#photutils.psf.stdpsf_reader "photutils.psf.stdpsf_reader") or [`webbpsf_reader()`](photutils.psf.webbpsf_reader.html#photutils.psf.webbpsf_reader "photutils.psf.webbpsf_reader") with the provided parameters. |

    See also

    [`ImagePSF`](photutils.psf.ImagePSF.html#photutils.psf.ImagePSF "photutils.psf.ImagePSF")
    :   A model for a single ePSF image.

    [`make_epsf_from_psf`](photutils.psf.make_epsf_from_psf.html#photutils.psf.make_epsf_from_psf "photutils.psf.make_epsf_from_psf")
    :   Make an ePSF image from a sampled PSF.

    Notes

    The input images must be effective PSFs (ePSFs). Each value of an
    ePSF is the fraction of the source flux that falls in a whole
    detector pixel centered at that position relative to the source,
    even when the image is oversampled. The model interpolates the
    input images and does not integrate them over the detector pixels.
    Evaluating the model at a position `(x, y)` therefore gives the
    flux in a detector pixel centered at `(x, y)`, which can be any
    fractional pixel position.

    Because each value is the flux in a whole detector pixel, the model
    values sum to `flux` only when the model is evaluated on a grid
    with a spacing of one detector pixel. That holds for any values of
    `x_0` and `y_0`. On a finer grid the pixels overlap, and the
    sum is larger than `flux` by the ratio of the pixel area to the
    area of a grid cell.

    Oversampled images that are not ePSFs, such as PSFs sampled at the
    points of a fine grid or binned into subpixels, are not converted
    to ePSFs by this model. The model is then sharper than a source
    in the data. For an undersampled PSF, the sum of the model values
    over the detector pixels can also change with the subpixel position
    of the source. Such images should first be integrated over the
    area of a detector pixel centered at each of their grid points,
    which is what [`make_epsf_from_psf`](photutils.psf.make_epsf_from_psf.html#photutils.psf.make_epsf_from_psf "photutils.psf.make_epsf_from_psf") does.

    The fitted `flux` parameter represents the total source flux,
    provided the input ePSF images are properly normalized. The fitted
    flux is a multiplicative scale factor applied to the input ePSF
    after accounting for any oversampling.

    For a fully sampled ePSF (i.e., no oversampling), the sum of
    the ePSF values over an infinite grid is 1.0. Because ePSFs are
    represented by finite images in practice, the sum of the array
    values may be less than 1.0.

    For oversampled ePSFs, the normalization should instead be such
    that the sum of the array values over an infinite grid equals the
    product of the oversampling factors (e.g., `oversampling**2` when
    the oversampling is the same along both axes). Again, a finite image
    will generally have a smaller sum because it does not contain the
    full PSF wings.

    If the input ePSF image covers only a finite region of the PSF,
    correction factors based on the encircled or ensquared energy
    can be used to estimate the missing flux and obtain the proper
    normalization.

    With the default `fill_value` of 0, the model is zero outside of
    the extent of the input ePSF images. The model values on a grid of
    detector pixels therefore sum to less than `flux` by the fraction
    of the source flux that is outside of the images. That sum also
    changes with the subpixel position of the source, because the
    number of detector pixels inside the images changes (see
    [Image-based PSF Models](../user_guide/psf.html#psf-image-models) for example values). The input images
    should therefore be large enough that the ePSF is small at their
    edges.

    Internally, the ePSF grid is reordered so that the reference ePSFs
    are sorted first by their y detector coordinate and then by their x
    detector coordinate.

    Each grid plane is interpolated with a bicubic spline
    ([`RectBivariateSpline`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.RectBivariateSpline.html#scipy.interpolate.RectBivariateSpline "(in SciPy v1.18.0)") with `kx=ky=3` and
    `s=0`). The spline coefficients of each evaluated grid plane are
    cached on the model, in a float64 array with the same number of
    elements as the grid data, and shared across copies made with the
    [`copy`](#photutils.psf.GriddedPSFModel.copy "photutils.psf.GriddedPSFModel.copy") method.
    When every grid plane has been evaluated, the cache roughly doubles
    the model’s memory footprint for float64 grid data and triples it
    for float32 grid data. The cache is not included when the model is
    pickled, and a deep copy gets its own copy of it. The splines of
    the four bounding grid planes are evaluated together by a compiled
    kernel, which also computes the analytic partial derivatives used by
    [`fit_deriv`](#photutils.psf.GriddedPSFModel.fit_deriv "photutils.psf.GriddedPSFModel.fit_deriv").

    Examples

    Oversampled PSFs whose values are samples of the PSF, such as the
    output of an optical model, must be converted to ePSFs before they
    are used as the input images. Here, four narrow Gaussian PSFs are
    sampled on a grid that is oversampled by a factor of 4 and then
    integrated over the detector pixels with [`make_epsf_from_psf`](photutils.psf.make_epsf_from_psf.html#photutils.psf.make_epsf_from_psf "photutils.psf.make_epsf_from_psf"):

    ```
    >>> import numpy as np
    >>> from astropy.nddata import NDData
    >>> from photutils.psf import GriddedPSFModel, make_epsf_from_psf
    >>> oversampling = 4
    >>> yy, xx = np.mgrid[-30:31, -30:31] / oversampling
    >>> sigmas = (0.5, 0.55, 0.6, 0.65)  # detector pixels
    >>> psfs = np.array([np.exp(-(xx**2 + yy**2) / (2 * sigma**2))
    ...                  for sigma in sigmas])
    >>> psfs *= oversampling**2 / psfs.sum(axis=(1, 2), keepdims=True)
    >>> epsfs = make_epsf_from_psf(psfs, oversampling=oversampling)
    >>> meta = {'grid_xypos': [(0, 0), (100, 0), (0, 100), (100, 100)],
    ...         'oversampling': oversampling}
    >>> model = GriddedPSFModel(NDData(epsfs, meta=meta), x_0=40.3,
    ...                         y_0=29.6)

    ```

    The model values on a grid of detector pixels sum to the model
    flux for any subpixel position of the source:

    ```
    >>> yy, xx = np.mgrid[23:38, 33:48]
    >>> print(f'{model(xx, yy).sum():.3f}')
    1.000

    ```

    Attributes Summary

    |  |  |
    | --- | --- |
    | [`bbox_with_units`](#photutils.psf.GriddedPSFModel.bbox_with_units "photutils.psf.GriddedPSFModel.bbox_with_units") |  |
    | [`bounding_box`](#photutils.psf.GriddedPSFModel.bounding_box "photutils.psf.GriddedPSFModel.bounding_box") | A [`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple "(in Python v3.15)") of length [`n_inputs`](#photutils.psf.GriddedPSFModel.n_inputs "photutils.psf.GriddedPSFModel.n_inputs") defining the bounding box limits, or raise [`NotImplementedError`](https://docs.python.org/3/builtins/exceptions.html#NotImplementedError "(in Python v3.15)") for no bounding\_box. |
    | [`bounds`](#photutils.psf.GriddedPSFModel.bounds "photutils.psf.GriddedPSFModel.bounds") | A `dict` mapping parameter names to their upper and lower bounds as `(min, max)` tuples or `[min, max]` lists. |
    | [`col_fit_deriv`](#photutils.psf.GriddedPSFModel.col_fit_deriv "photutils.psf.GriddedPSFModel.col_fit_deriv") |  |
    | [`cov_matrix`](#photutils.psf.GriddedPSFModel.cov_matrix "photutils.psf.GriddedPSFModel.cov_matrix") | Fitter should set covariance matrix, if available. |
    | [`data`](#photutils.psf.GriddedPSFModel.data "photutils.psf.GriddedPSFModel.data") | The 3D array of ePSFs. |
    | [`eqcons`](#photutils.psf.GriddedPSFModel.eqcons "photutils.psf.GriddedPSFModel.eqcons") | List of parameter equality constraints. |
    | [`fittable`](#photutils.psf.GriddedPSFModel.fittable "photutils.psf.GriddedPSFModel.fittable") |  |
    | [`fixed`](#photutils.psf.GriddedPSFModel.fixed "photutils.psf.GriddedPSFModel.fixed") | A `dict` mapping parameter names to their fixed constraint. |
    | [`flux`](#photutils.psf.GriddedPSFModel.flux "photutils.psf.GriddedPSFModel.flux") |  |
    | [`grid_shape`](#photutils.psf.GriddedPSFModel.grid_shape "photutils.psf.GriddedPSFModel.grid_shape") | The `(ny, nx)` shape of the ePSF grid. |
    | [`grid_xypos`](#photutils.psf.GriddedPSFModel.grid_xypos "photutils.psf.GriddedPSFModel.grid_xypos") | The (x, y) positions of the ePSFs, as an `(N_psf, 2)` array. |
    | [`has_bounds`](#photutils.psf.GriddedPSFModel.has_bounds "photutils.psf.GriddedPSFModel.has_bounds") | Whether the model has any bounds constraints. |
    | [`has_fixed`](#photutils.psf.GriddedPSFModel.has_fixed "photutils.psf.GriddedPSFModel.has_fixed") | Whether the model has any fixed constraints. |
    | [`has_tied`](#photutils.psf.GriddedPSFModel.has_tied "photutils.psf.GriddedPSFModel.has_tied") | Whether the model has any tied constraints. |
    | [`has_user_bounding_box`](#photutils.psf.GriddedPSFModel.has_user_bounding_box "photutils.psf.GriddedPSFModel.has_user_bounding_box") | A flag indicating whether or not a custom bounding\_box has been assigned to this model by a user, via assignment to `model.bounding_box`. |
    | [`has_user_inverse`](#photutils.psf.GriddedPSFModel.has_user_inverse "photutils.psf.GriddedPSFModel.has_user_inverse") | A flag indicating whether or not a custom inverse model has been assigned to this model by a user, via assignment to `model.inverse`. |
    | [`ineqcons`](#photutils.psf.GriddedPSFModel.ineqcons "photutils.psf.GriddedPSFModel.ineqcons") | List of parameter inequality constraints. |
    | [`input_units`](#photutils.psf.GriddedPSFModel.input_units "photutils.psf.GriddedPSFModel.input_units") | This property is used to indicate what units or sets of units the evaluate method expects, and returns a dictionary mapping inputs to units (or [`None`](https://docs.python.org/3/builtins/constants.html#None "(in Python v3.15)") if any units are accepted). |
    | [`input_units_allow_dimensionless`](#photutils.psf.GriddedPSFModel.input_units_allow_dimensionless "photutils.psf.GriddedPSFModel.input_units_allow_dimensionless") | Allow dimensionless input (and corresponding output). |
    | [`input_units_equivalencies`](#photutils.psf.GriddedPSFModel.input_units_equivalencies "photutils.psf.GriddedPSFModel.input_units_equivalencies") |  |
    | [`input_units_strict`](#photutils.psf.GriddedPSFModel.input_units_strict "photutils.psf.GriddedPSFModel.input_units_strict") | Enforce strict units on inputs to evaluate. |
    | [`inputs`](#photutils.psf.GriddedPSFModel.inputs "photutils.psf.GriddedPSFModel.inputs") |  |
    | [`inverse`](#photutils.psf.GriddedPSFModel.inverse "photutils.psf.GriddedPSFModel.inverse") | Returns a new [`Model`](https://docs.astropy.org/en/stable/api/astropy.modeling.Model.html#astropy.modeling.Model "(in Astropy v8.0)") instance which performs the inverse transform, if an analytic inverse is defined for this model. |
    | [`linear`](#photutils.psf.GriddedPSFModel.linear "photutils.psf.GriddedPSFModel.linear") |  |
    | [`meta`](#photutils.psf.GriddedPSFModel.meta "photutils.psf.GriddedPSFModel.meta") | A dict-like object to store optional information. |
    | [`model_constraints`](#photutils.psf.GriddedPSFModel.model_constraints "photutils.psf.GriddedPSFModel.model_constraints") | Primarily for informational purposes, these are the types of constraints that constrain model evaluation. |
    | [`model_set_axis`](#photutils.psf.GriddedPSFModel.model_set_axis "photutils.psf.GriddedPSFModel.model_set_axis") | The index of the model set axis--that is the axis of a parameter array that pertains to which model a parameter value pertains to--as specified when the model was initialized. |
    | [`n_inputs`](#photutils.psf.GriddedPSFModel.n_inputs "photutils.psf.GriddedPSFModel.n_inputs") |  |
    | [`n_outputs`](#photutils.psf.GriddedPSFModel.n_outputs "photutils.psf.GriddedPSFModel.n_outputs") |  |
    | [`n_submodels`](#photutils.psf.GriddedPSFModel.n_submodels "photutils.psf.GriddedPSFModel.n_submodels") | Return the number of components in a single model, which is obviously 1. |
    | [`name`](#photutils.psf.GriddedPSFModel.name "photutils.psf.GriddedPSFModel.name") | User-provided name for this model instance. |
    | [`origin`](#photutils.psf.GriddedPSFModel.origin "photutils.psf.GriddedPSFModel.origin") | The (x, y) pixel coordinates, as a 1D [`ndarray`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray "(in NumPy v2.5)"), of the origin of the coordinate system within the model image. |
    | [`outputs`](#photutils.psf.GriddedPSFModel.outputs "photutils.psf.GriddedPSFModel.outputs") |  |
    | [`oversampling`](#photutils.psf.GriddedPSFModel.oversampling "photutils.psf.GriddedPSFModel.oversampling") | The integer oversampling factors of the input ePSF images, as a 1D [`ndarray`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray "(in NumPy v2.5)") in `(y, x)` order. |
    | [`param_names`](#photutils.psf.GriddedPSFModel.param_names "photutils.psf.GriddedPSFModel.param_names") | Names of the parameters that describe models of this type. |
    | [`param_sets`](#photutils.psf.GriddedPSFModel.param_sets "photutils.psf.GriddedPSFModel.param_sets") | Return parameters as a pset. |
    | [`parameter_constraints`](#photutils.psf.GriddedPSFModel.parameter_constraints "photutils.psf.GriddedPSFModel.parameter_constraints") | Primarily for informational purposes, these are the types of constraints that can be set on a model's parameters. |
    | [`parameters`](#photutils.psf.GriddedPSFModel.parameters "photutils.psf.GriddedPSFModel.parameters") | A flattened array of all parameter values in all parameter sets. |
    | [`read`](#photutils.psf.GriddedPSFModel.read "photutils.psf.GriddedPSFModel.read") | Read and parse a FITS file into a [`GriddedPSFModel`](#photutils.psf.GriddedPSFModel "photutils.psf.GriddedPSFModel") instance. |
    | [`return_units`](#photutils.psf.GriddedPSFModel.return_units "photutils.psf.GriddedPSFModel.return_units") | This property is used to indicate what units or sets of units the output of evaluate should be in, and returns a dictionary mapping outputs to units (or [`None`](https://docs.python.org/3/builtins/constants.html#None "(in Python v3.15)") if any units are accepted). |
    | [`separable`](#photutils.psf.GriddedPSFModel.separable "photutils.psf.GriddedPSFModel.separable") | A flag indicating whether a model is separable. |
    | [`standard_broadcasting`](#photutils.psf.GriddedPSFModel.standard_broadcasting "photutils.psf.GriddedPSFModel.standard_broadcasting") |  |
    | [`stds`](#photutils.psf.GriddedPSFModel.stds "photutils.psf.GriddedPSFModel.stds") | Standard deviation of parameters, if covariance matrix is available. |
    | [`sync_constraints`](#photutils.psf.GriddedPSFModel.sync_constraints "photutils.psf.GriddedPSFModel.sync_constraints") | This is a boolean property that indicates whether or not accessing constraints automatically check the constituent models current values. |
    | [`tied`](#photutils.psf.GriddedPSFModel.tied "photutils.psf.GriddedPSFModel.tied") | A `dict` mapping parameter names to their tied constraint. |
    | [`uses_quantity`](#photutils.psf.GriddedPSFModel.uses_quantity "photutils.psf.GriddedPSFModel.uses_quantity") | True if this model has been created with [`Quantity`](https://docs.astropy.org/en/stable/api/astropy.units.Quantity.html#astropy.units.Quantity "(in Astropy v8.0)") objects or if there are no parameters. |
    | [`x_0`](#photutils.psf.GriddedPSFModel.x_0 "photutils.psf.GriddedPSFModel.x_0") |  |
    | [`y_0`](#photutils.psf.GriddedPSFModel.y_0 "photutils.psf.GriddedPSFModel.y_0") |  |

    Methods Summary

    |  |  |
    | --- | --- |
    | [`__call__`](#photutils.psf.GriddedPSFModel.__call__ "photutils.psf.GriddedPSFModel.__call__")(\*inputs[, model\_set\_axis, ...]) | Evaluate this model using the given input(s) and the parameter values that were specified when the model was instantiated. |
    | [`coerce_units`](#photutils.psf.GriddedPSFModel.coerce_units "photutils.psf.GriddedPSFModel.coerce_units")([input\_units, return\_units, ...]) | Attach units to this (unitless) model. |
    | [`copy`](#photutils.psf.GriddedPSFModel.copy "photutils.psf.GriddedPSFModel.copy")() | Return a copy of this model where only the model parameters are copied. |
    | [`deepcopy`](#photutils.psf.GriddedPSFModel.deepcopy "photutils.psf.GriddedPSFModel.deepcopy")() | Return a deep copy of this model. |
    | [`evaluate`](#photutils.psf.GriddedPSFModel.evaluate "photutils.psf.GriddedPSFModel.evaluate")(x, y, flux, x\_0, y\_0) | Calculate the ePSF model at the input coordinates for the given model parameters. |
    | [`fit_deriv`](#photutils.psf.GriddedPSFModel.fit_deriv "photutils.psf.GriddedPSFModel.fit_deriv")(x, y, flux, x\_0, y\_0) | Calculate the partial derivatives of the ePSF model with respect to the model parameters. |
    | [`get_bounding_box`](#photutils.psf.GriddedPSFModel.get_bounding_box "photutils.psf.GriddedPSFModel.get_bounding_box")([with\_bbox]) | Return the `bounding_box` of a model if it exists or `None` otherwise. |
    | [`has_inverse`](#photutils.psf.GriddedPSFModel.has_inverse "photutils.psf.GriddedPSFModel.has_inverse")() | Returns True if the model has an analytic or user inverse defined. |
    | [`input_shape`](#photutils.psf.GriddedPSFModel.input_shape "photutils.psf.GriddedPSFModel.input_shape")(inputs) | Get input shape for bounding\_box evaluation. |
    | [`output_units`](#photutils.psf.GriddedPSFModel.output_units "photutils.psf.GriddedPSFModel.output_units")(\*\*kwargs) | Return a dictionary of output units for this model given a dictionary of fitting inputs and outputs. |
    | [`plot_grid`](#photutils.psf.GriddedPSFModel.plot_grid "photutils.psf.GriddedPSFModel.plot_grid")(\*[, ax, vmax\_scale, peak\_norm, ...]) | Plot the grid of ePSF models. |
    | [`prepare_inputs`](#photutils.psf.GriddedPSFModel.prepare_inputs "photutils.psf.GriddedPSFModel.prepare_inputs")(\*inputs[, model\_set\_axis, ...]) | This method is used in [`__call__`](https://docs.astropy.org/en/stable/api/astropy.modeling.Model.html#astropy.modeling.Model.__call__ "(in Astropy v8.0)") to ensure that all the inputs to the model can be broadcast into compatible shapes (if one or both of them are input as arrays), particularly if there are more than one parameter sets. |
    | [`prepare_outputs`](#photutils.psf.GriddedPSFModel.prepare_outputs "photutils.psf.GriddedPSFModel.prepare_outputs")(broadcasted\_shapes, ...) |  |
    | [`rename`](#photutils.psf.GriddedPSFModel.rename "photutils.psf.GriddedPSFModel.rename")([name, inputs, outputs]) | Return a copy of this model with a new name. |
    | [`render`](#photutils.psf.GriddedPSFModel.render "photutils.psf.GriddedPSFModel.render")([out, coords]) | Evaluate a model at fixed positions, respecting the `bounding_box`. |
    | [`set_slice_args`](#photutils.psf.GriddedPSFModel.set_slice_args "photutils.psf.GriddedPSFModel.set_slice_args")(\*args) |  |
    | [`strip_units_from_tree`](#photutils.psf.GriddedPSFModel.strip_units_from_tree "photutils.psf.GriddedPSFModel.strip_units_from_tree")() |  |
    | [`sum_of_implicit_terms`](#photutils.psf.GriddedPSFModel.sum_of_implicit_terms "photutils.psf.GriddedPSFModel.sum_of_implicit_terms")(\*args, \*\*kwargs) | Evaluate the sum of any implicit model terms on some input variables. |
    | [`with_units_from_data`](#photutils.psf.GriddedPSFModel.with_units_from_data "photutils.psf.GriddedPSFModel.with_units_from_data")(\*\*kwargs) | Return an instance of the model which has units for which the parameter values are compatible with the data units specified. |
    | [`without_units_for_data`](#photutils.psf.GriddedPSFModel.without_units_for_data "photutils.psf.GriddedPSFModel.without_units_for_data")(\*\*kwargs) | Return an instance of the model for which the parameter values have been converted to the right units for the data, then the units have been stripped away. |

    Attributes Documentation

    bbox\_with\_units[#](#photutils.psf.GriddedPSFModel.bbox_with_units "Link to this definition")

    bounding\_box[#](#photutils.psf.GriddedPSFModel.bounding_box "Link to this definition")
    :   A [`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple "(in Python v3.15)") of length [`n_inputs`](#photutils.psf.GriddedPSFModel.n_inputs "photutils.psf.GriddedPSFModel.n_inputs") defining the bounding box limits, or
        raise [`NotImplementedError`](https://docs.python.org/3/builtins/exceptions.html#NotImplementedError "(in Python v3.15)") for no bounding\_box.

        The default limits are given by a `bounding_box` property or method
        defined in the class body of a specific model. If not defined then
        this property just raises [`NotImplementedError`](https://docs.python.org/3/builtins/exceptions.html#NotImplementedError "(in Python v3.15)") by default (but may be
        assigned a custom value by a user). `bounding_box` can be set
        manually to an array-like object of shape `(model.n_inputs, 2)`. For
        further usage, see [Efficient Model Rendering with Bounding Boxes](https://docs.astropy.org/en/stable/modeling/models.html#id2 "(in Astropy v8.0)")

        The limits are ordered according to the [`numpy`](https://numpy.org/doc/stable/reference/index.html#module-numpy "(in NumPy v2.5)") `'C'` indexing
        convention, and are the reverse of the model input order,
        e.g. for inputs `('x', 'y', 'z')`, `bounding_box` is defined:

        * for 1D: `(x_low, x_high)`
        * for 2D: `((y_low, y_high), (x_low, x_high))`
        * for 3D: `((z_low, z_high), (y_low, y_high), (x_low, x_high))`

        Examples

        Setting the `bounding_box` limits for a 1D and 2D model:

        ```
        >>> from astropy.modeling.models import Gaussian1D, Gaussian2D
        >>> model_1d = Gaussian1D()
        >>> model_2d = Gaussian2D(x_stddev=1, y_stddev=1)
        >>> model_1d.bounding_box = (-5, 5)
        >>> model_2d.bounding_box = ((-6, 6), (-5, 5))

        ```

        Setting the bounding\_box limits for a user-defined 3D
        [`custom_model`](https://docs.astropy.org/en/stable/api/astropy.modeling.custom_model.html#astropy.modeling.custom_model "(in Astropy v8.0)"):

        ```
        >>> from astropy.modeling.models import custom_model
        >>> def const3d(x, y, z, amp=1):
        ...    return amp
        ...
        >>> Const3D = custom_model(const3d)
        >>> model_3d = Const3D()
        >>> model_3d.bounding_box = ((-6, 6), (-5, 5), (-4, 4))

        ```

        To reset `bounding_box` to its default limits just delete the
        user-defined value–this will reset it back to the default defined
        on the class:

        ```
        >>> del model_1d.bounding_box

        ```

        To disable the bounding box entirely (including the default),
        set `bounding_box` to [`None`](https://docs.python.org/3/builtins/constants.html#None "(in Python v3.15)"):

        ```
        >>> model_1d.bounding_box = None
        >>> model_1d.bounding_box
        Traceback (most recent call last):
        NotImplementedError: No bounding box is defined for this model
        (note: the bounding box was explicitly disabled for this model;
        use `del model.bounding_box` to restore the default bounding box,
        if one is defined for this model).

        ```

    bounds[#](#photutils.psf.GriddedPSFModel.bounds "Link to this definition")
    :   A `dict` mapping parameter names to their upper and lower bounds as
        `(min, max)` tuples or `[min, max]` lists.

    col\_fit\_deriv = True[#](#photutils.psf.GriddedPSFModel.col_fit_deriv "Link to this definition")

    cov\_matrix[#](#photutils.psf.GriddedPSFModel.cov_matrix "Link to this definition")
    :   Fitter should set covariance matrix, if available.

    data[#](#photutils.psf.GriddedPSFModel.data "Link to this definition")
    :   The 3D array of ePSFs.

        The shape is `(N_psf, ePSF_ny, ePSF_nx)`.

    eqcons[#](#photutils.psf.GriddedPSFModel.eqcons "Link to this definition")
    :   List of parameter equality constraints.

    fittable = True[#](#photutils.psf.GriddedPSFModel.fittable "Link to this definition")

    fixed[#](#photutils.psf.GriddedPSFModel.fixed "Link to this definition")
    :   A `dict` mapping parameter names to their fixed constraint.

    flux = Parameter('flux', value=1.0)[#](#photutils.psf.GriddedPSFModel.flux "Link to this definition")

    grid\_shape[#](#photutils.psf.GriddedPSFModel.grid_shape "Link to this definition")
    :   The `(ny, nx)` shape of the ePSF grid.

    grid\_xypos[#](#photutils.psf.GriddedPSFModel.grid_xypos "Link to this definition")
    :   The (x, y) positions of the ePSFs, as an `(N_psf, 2)` array.

        The positions are sorted first by y and then by x, which can
        differ from the order of the input `grid_xypos`.
        `grid_xypos[i]` is the (x, y) position of the reference ePSF
        in `data[i]`.

    has\_bounds[#](#photutils.psf.GriddedPSFModel.has_bounds "Link to this definition")
    :   Whether the model has any bounds constraints.

    has\_fixed[#](#photutils.psf.GriddedPSFModel.has_fixed "Link to this definition")
    :   Whether the model has any fixed constraints.

    has\_tied[#](#photutils.psf.GriddedPSFModel.has_tied "Link to this definition")
    :   Whether the model has any tied constraints.

    has\_user\_bounding\_box[#](#photutils.psf.GriddedPSFModel.has_user_bounding_box "Link to this definition")
    :   A flag indicating whether or not a custom bounding\_box has been
        assigned to this model by a user, via assignment to
        `model.bounding_box`.

    has\_user\_inverse[#](#photutils.psf.GriddedPSFModel.has_user_inverse "Link to this definition")
    :   A flag indicating whether or not a custom inverse model has been
        assigned to this model by a user, via assignment to `model.inverse`.

    ineqcons[#](#photutils.psf.GriddedPSFModel.ineqcons "Link to this definition")
    :   List of parameter inequality constraints.

    input\_units[#](#photutils.psf.GriddedPSFModel.input_units "Link to this definition")
    :   This property is used to indicate what units or sets of units the
        evaluate method expects, and returns a dictionary mapping inputs to
        units (or [`None`](https://docs.python.org/3/builtins/constants.html#None "(in Python v3.15)") if any units are accepted).

        Model sub-classes can also use function annotations in evaluate to
        indicate valid input units, in which case this property should
        not be overridden since it will return the input units based on the
        annotations.

    input\_units\_allow\_dimensionless[#](#photutils.psf.GriddedPSFModel.input_units_allow_dimensionless "Link to this definition")
    :   Allow dimensionless input (and corresponding output). If this is True,
        input values to evaluate will gain the units specified in input\_units. If
        this is a dictionary then it should map input name to a bool to allow
        dimensionless numbers for that input.
        Only has an effect if input\_units is defined.

    input\_units\_equivalencies = None[#](#photutils.psf.GriddedPSFModel.input_units_equivalencies "Link to this definition")

    input\_units\_strict[#](#photutils.psf.GriddedPSFModel.input_units_strict "Link to this definition")
    :   Enforce strict units on inputs to evaluate. If this is set to True,
        input values to evaluate will be in the exact units specified by
        input\_units. If the input quantities are convertible to input\_units,
        they are converted. If this is a dictionary then it should map input
        name to a bool to set strict input units for that parameter.

    inputs[#](#photutils.psf.GriddedPSFModel.inputs "Link to this definition")

    inverse[#](#photutils.psf.GriddedPSFModel.inverse "Link to this definition")
    :   Returns a new [`Model`](https://docs.astropy.org/en/stable/api/astropy.modeling.Model.html#astropy.modeling.Model "(in Astropy v8.0)") instance which performs the
        inverse transform, if an analytic inverse is defined for this model.

        Even on models that don’t have an inverse defined, this property can be
        set with a manually-defined inverse, such a pre-computed or
        experimentally determined inverse (often given as a
        [`PolynomialModel`](https://docs.astropy.org/en/stable/api/astropy.modeling.polynomial.PolynomialModel.html#astropy.modeling.polynomial.PolynomialModel "(in Astropy v8.0)"), but not by
        requirement).

        A custom inverse can be deleted with `del model.inverse`. In this
        case the model’s inverse is reset to its default, if a default exists
        (otherwise the default is to raise [`NotImplementedError`](https://docs.python.org/3/builtins/exceptions.html#NotImplementedError "(in Python v3.15)")).

        Note to authors of [`Model`](https://docs.astropy.org/en/stable/api/astropy.modeling.Model.html#astropy.modeling.Model "(in Astropy v8.0)") subclasses: To define an
        inverse for a model simply override this property to return the
        appropriate model representing the inverse. The machinery that will
        make the inverse manually-overridable is added automatically by the
        base class.

    linear = False[#](#photutils.psf.GriddedPSFModel.linear "Link to this definition")

    meta = None[#](#photutils.psf.GriddedPSFModel.meta "Link to this definition")
    :   A dict-like object to store optional information.

    model\_constraints = ('eqcons', 'ineqcons')[#](#photutils.psf.GriddedPSFModel.model_constraints "Link to this definition")
    :   Primarily for informational purposes, these are the types of constraints
        that constrain model evaluation.

    model\_set\_axis[#](#photutils.psf.GriddedPSFModel.model_set_axis "Link to this definition")
    :   The index of the model set axis–that is the axis of a parameter array
        that pertains to which model a parameter value pertains to–as
        specified when the model was initialized.

        See the documentation on [Model Sets](https://docs.astropy.org/en/stable/modeling/models.html#modeling-model-sets "(in Astropy v8.0)")
        for more details.

    n\_inputs = 2[#](#photutils.psf.GriddedPSFModel.n_inputs "Link to this definition")

    n\_outputs = 1[#](#photutils.psf.GriddedPSFModel.n_outputs "Link to this definition")

    n\_submodels[#](#photutils.psf.GriddedPSFModel.n_submodels "Link to this definition")
    :   Return the number of components in a single model, which is
        obviously 1.

    name[#](#photutils.psf.GriddedPSFModel.name "Link to this definition")
    :   User-provided name for this model instance.

    origin[[source]](../_modules/photutils/psf/gridded_models.html#GriddedPSFModel.origin)[#](#photutils.psf.GriddedPSFModel.origin "Link to this definition")
    :   The (x, y) pixel coordinates, as a 1D [`ndarray`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray "(in NumPy v2.5)"), of the
        origin of the coordinate system within the model image.

    outputs[#](#photutils.psf.GriddedPSFModel.outputs "Link to this definition")

    oversampling[#](#photutils.psf.GriddedPSFModel.oversampling "Link to this definition")
    :   The integer oversampling factors of the input ePSF images, as a
        1D [`ndarray`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray "(in NumPy v2.5)") in `(y, x)` order.

        The value can be set with a positive integer, which is used for
        both axes, or with two positive integers in `(y, x)` order.

    param\_names = ('flux', 'x\_0', 'y\_0')[#](#photutils.psf.GriddedPSFModel.param_names "Link to this definition")
    :   Names of the parameters that describe models of this type.

        The parameters in this tuple are in the same order they should be passed in
        when initializing a model of a specific type. Some types of models, such
        as polynomial models, have a different number of parameters depending on
        some other property of the model, such as the degree.

        When defining a custom model class the value of this attribute is
        automatically set by the [`Parameter`](https://docs.astropy.org/en/stable/api/astropy.modeling.Parameter.html#astropy.modeling.Parameter "(in Astropy v8.0)") attributes defined
        in the class body.

    param\_sets[#](#photutils.psf.GriddedPSFModel.param_sets "Link to this definition")
    :   Return parameters as a pset.

        This is a list with one item per parameter set, which is an array of
        that parameter’s values across all parameter sets, with the last axis
        associated with the parameter set.

    parameter\_constraints = ('fixed', 'tied', 'bounds')[#](#photutils.psf.GriddedPSFModel.parameter_constraints "Link to this definition")
    :   Primarily for informational purposes, these are the types of constraints
        that can be set on a model’s parameters.

    parameters[#](#photutils.psf.GriddedPSFModel.parameters "Link to this definition")
    :   A flattened array of all parameter values in all parameter sets.

        Fittable parameters maintain this list and fitters modify it.

    read[#](#photutils.psf.GriddedPSFModel.read "Link to this definition")
    :   Read and parse a FITS file into a [`GriddedPSFModel`](#photutils.psf.GriddedPSFModel "photutils.psf.GriddedPSFModel") instance.

        This class enables the astropy unified I/O layer for
        [`GriddedPSFModel`](#photutils.psf.GriddedPSFModel "photutils.psf.GriddedPSFModel"). This allows easily reading a file
        in different supported data formats using syntax such as:

        ```
        >>> from photutils.psf import GriddedPSFModel
        >>> psf_model = GriddedPSFModel.read('filename.fits', format=format)

        ```

        Get help on the available readers for
        [`GriddedPSFModel`](#photutils.psf.GriddedPSFModel "photutils.psf.GriddedPSFModel") using the `help()` method:

        ```
        >>> # Get help reading a GriddedPSFModel and list supported formats
        >>> GriddedPSFModel.read.help()

        >>> # Get detailed help on the STDPSF FITS reader
        >>> GriddedPSFModel.read.help('stdpsf')

        >>> # Get detailed help on the WebbPSF FITS reader
        >>> GriddedPSFModel.read.help('webbpsf')

        >>> # Print list of available formats
        >>> GriddedPSFModel.read.list_formats()

        ```

        Parameters:
        :   **instance**object
            :   Descriptor calling instance or [`None`](https://docs.python.org/3/builtins/constants.html#None "(in Python v3.15)") if no instance.

            **cls**type
            :   Descriptor calling class (either owner class or instance class).

    return\_units[#](#photutils.psf.GriddedPSFModel.return_units "Link to this definition")
    :   This property is used to indicate what units or sets of units the
        output of evaluate should be in, and returns a dictionary mapping
        outputs to units (or [`None`](https://docs.python.org/3/builtins/constants.html#None "(in Python v3.15)") if any units are accepted).

        Model sub-classes can also use function annotations in evaluate to
        indicate valid output units, in which case this property should not be
        overridden since it will return the return units based on the
        annotations.

    separable[#](#photutils.psf.GriddedPSFModel.separable "Link to this definition")
    :   A flag indicating whether a model is separable.

    standard\_broadcasting = True[#](#photutils.psf.GriddedPSFModel.standard_broadcasting "Link to this definition")

    stds[#](#photutils.psf.GriddedPSFModel.stds "Link to this definition")
    :   Standard deviation of parameters, if covariance matrix is available.

    sync\_constraints[#](#photutils.psf.GriddedPSFModel.sync_constraints "Link to this definition")
    :   This is a boolean property that indicates whether or not accessing constraints
        automatically check the constituent models current values. It defaults to True
        on creation of a model, but for fitting purposes it should be set to False
        for performance reasons.

    tied[#](#photutils.psf.GriddedPSFModel.tied "Link to this definition")
    :   A `dict` mapping parameter names to their tied constraint.

    uses\_quantity[#](#photutils.psf.GriddedPSFModel.uses_quantity "Link to this definition")
    :   True if this model has been created with [`Quantity`](https://docs.astropy.org/en/stable/api/astropy.units.Quantity.html#astropy.units.Quantity "(in Astropy v8.0)")
        objects or if there are no parameters.

        This can be used to determine if this model should be evaluated with
        [`Quantity`](https://docs.astropy.org/en/stable/api/astropy.units.Quantity.html#astropy.units.Quantity "(in Astropy v8.0)") or regular floats.

    x\_0 = Parameter('x\_0', value=0.0)[#](#photutils.psf.GriddedPSFModel.x_0 "Link to this definition")

    y\_0 = Parameter('y\_0', value=0.0)[#](#photutils.psf.GriddedPSFModel.y_0 "Link to this definition")

    Methods Documentation

    \_\_call\_\_(*\*inputs*, *model\_set\_axis=None*, *with\_bounding\_box=False*, *fill\_value=nan*, *equivalencies=None*, *inputs\_map=None*, *\*\*new\_inputs*)[#](#photutils.psf.GriddedPSFModel.__call__ "Link to this definition")
    :   Evaluate this model using the given input(s) and the parameter values
        that were specified when the model was instantiated.

    coerce\_units(*input\_units=None*, *return\_units=None*, *input\_units\_equivalencies=None*, *input\_units\_allow\_dimensionless=False*)[#](#photutils.psf.GriddedPSFModel.coerce_units "Link to this definition")
    :   Attach units to this (unitless) model.

        Parameters:
        :   **input\_units**dict or tuple, optional
            :   Input units to attach. If dict, each key is the name of a model input,
                and the value is the unit to attach. If tuple, the elements are units
                to attach in order corresponding to [`inputs`](https://docs.astropy.org/en/stable/api/astropy.modeling.Model.html#astropy.modeling.Model.inputs "(in Astropy v8.0)").

            **return\_units**dict or tuple, optional
            :   Output units to attach. If dict, each key is the name of a model output,
                and the value is the unit to attach. If tuple, the elements are units
                to attach in order corresponding to [`outputs`](https://docs.astropy.org/en/stable/api/astropy.modeling.Model.html#astropy.modeling.Model.outputs "(in Astropy v8.0)").

            **input\_units\_equivalencies**dict, optional
            :   Default equivalencies to apply to input values. If set, this should be a
                dictionary where each key is a string that corresponds to one of the
                model inputs.

            **input\_units\_allow\_dimensionless**bool or dict, optional
            :   Allow dimensionless input. If this is True, input values to evaluate will
                gain the units specified in input\_units. If this is a dictionary then it
                should map input name to a bool to allow dimensionless numbers for that
                input.

        Returns:
        :   [`CompoundModel`](https://docs.astropy.org/en/stable/api/astropy.modeling.CompoundModel.html#astropy.modeling.CompoundModel "(in Astropy v8.0)")
            :   A [`CompoundModel`](https://docs.astropy.org/en/stable/api/astropy.modeling.CompoundModel.html#astropy.modeling.CompoundModel "(in Astropy v8.0)") composed of the current
                model plus [`UnitsMapping`](https://docs.astropy.org/en/stable/api/astropy.modeling.mappings.UnitsMapping.html#astropy.modeling.mappings.UnitsMapping "(in Astropy v8.0)")
                model(s) that attach the units.

        Raises:
        :   ValueError
            :   If the current model already has units.

        Examples

        Wrapping a unitless model to require and convert units:

        ```
        >>> from astropy.modeling.models import Polynomial1D
        >>> from astropy import units as u
        >>> poly = Polynomial1D(1, c0=1, c1=2)
        >>> model = poly.coerce_units((u.m,), (u.s,))
        >>> model(u.Quantity(10, u.m))
        <Quantity 21. s>
        >>> model(u.Quantity(1000, u.cm))
        <Quantity 21. s>
        >>> model(u.Quantity(10, u.cm))
        <Quantity 1.2 s>

        ```

        Wrapping a unitless model but still permitting unitless input:

        ```
        >>> from astropy.modeling.models import Polynomial1D
        >>> from astropy import units as u
        >>> poly = Polynomial1D(1, c0=1, c1=2)
        >>> model = poly.coerce_units((u.m,), (u.s,), input_units_allow_dimensionless=True)
        >>> model(u.Quantity(10, u.m))
        <Quantity 21. s>
        >>> model(10)
        <Quantity 21. s>

        ```

    copy()[[source]](../_modules/photutils/psf/gridded_models.html#GriddedPSFModel.copy)[#](#photutils.psf.GriddedPSFModel.copy "Link to this definition")
    :   Return a copy of this model where only the model parameters are
        copied.

        All other model attributes are references to the original
        model, except the `meta` dictionary, which is copied
        shallowly. This prevents copying the ePSF grid data, which may
        contain a large array.

        This method is useful if one is interested in only changing
        the model parameters in a model copy. It is used in the PSF
        photometry classes during model fitting.

        Use the [`deepcopy`](#photutils.psf.GriddedPSFModel.deepcopy "photutils.psf.GriddedPSFModel.deepcopy") method if you want to copy all the model
        attributes, including the ePSF grid data.

        Returns:
        :   **result**[`GriddedPSFModel`](#photutils.psf.GriddedPSFModel "photutils.psf.GriddedPSFModel")
            :   A copy of this model with only the model parameters copied.

    deepcopy()[[source]](../_modules/photutils/psf/gridded_models.html#GriddedPSFModel.deepcopy)[#](#photutils.psf.GriddedPSFModel.deepcopy "Link to this definition")
    :   Return a deep copy of this model.

        The deep copy gets its own copy of the cached spline
        coefficients, so it does not rebuild the splines that this model
        already has.

        Returns:
        :   **result**[`GriddedPSFModel`](#photutils.psf.GriddedPSFModel "photutils.psf.GriddedPSFModel")
            :   A deep copy of this model.

    evaluate(*x*, *y*, *flux*, *x\_0*, *y\_0*)[[source]](../_modules/photutils/psf/gridded_models.html#GriddedPSFModel.evaluate)[#](#photutils.psf.GriddedPSFModel.evaluate "Link to this definition")
    :   Calculate the ePSF model at the input coordinates for the given
        model parameters.

        Parameters:
        :   **x, y**float or [`ndarray`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray "(in NumPy v2.5)")
            :   The x and y positions at which to evaluate the model.

            **flux**float
            :   The flux scaling factor for the model.

            **x\_0, y\_0**float
            :   The (x, y) position of the model.

        Returns:
        :   **evaluated\_model**[`ndarray`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray "(in NumPy v2.5)")
            :   The evaluated model.

    fit\_deriv(*x*, *y*, *flux*, *x\_0*, *y\_0*)[[source]](../_modules/photutils/psf/gridded_models.html#GriddedPSFModel.fit_deriv)[#](#photutils.psf.GriddedPSFModel.fit_deriv "Link to this definition")
    :   Calculate the partial derivatives of the ePSF model with respect
        to the model parameters.

        Providing this analytic Jacobian allows the fitter to avoid the
        finite-difference approximation, which requires additional model
        evaluations.

        The position derivatives include both the shift of the ePSF with
        the model position and the change of the bilinearly interpolated
        ePSF itself with the model position across the reference grid.

        Parameters:
        :   **x, y**float or [`ndarray`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray "(in NumPy v2.5)")
            :   The x and y positions at which to evaluate the model.

            **flux**float
            :   The flux scaling factor for the model.

            **x\_0, y\_0**float
            :   The (x, y) position of the model.

        Returns:
        :   **result**list of [`ndarray`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray "(in NumPy v2.5)")
            :   The list of partial derivatives with respect to the
                `flux`, `x_0`, and `y_0` parameters.

    get\_bounding\_box(*with\_bbox=True*)[#](#photutils.psf.GriddedPSFModel.get_bounding_box "Link to this definition")
    :   Return the `bounding_box` of a model if it exists or `None`
        otherwise.

        Parameters:
        :   **with\_bbox**
            :   The value of the `with_bounding_box` keyword argument
                when calling the model. Default is [`True`](https://docs.python.org/3/builtins/constants.html#True "(in Python v3.15)") for usage when
                looking up the model’s `bounding_box` without risk of error.

    has\_inverse()[#](#photutils.psf.GriddedPSFModel.has_inverse "Link to this definition")
    :   Returns True if the model has an analytic or user
        inverse defined.

    input\_shape(*inputs*)[#](#photutils.psf.GriddedPSFModel.input_shape "Link to this definition")
    :   Get input shape for bounding\_box evaluation.

    output\_units(*\*\*kwargs*)[#](#photutils.psf.GriddedPSFModel.output_units "Link to this definition")
    :   Return a dictionary of output units for this model given a dictionary
        of fitting inputs and outputs.

        The input and output Quantity objects should be given as keyword
        arguments.

        Notes

        This method is needed in order to be able to fit models with units in
        the parameters, since we need to temporarily strip away the units from
        the model during the fitting (which might be done by e.g. scipy
        functions).

        This method will force extra model evaluations, which maybe computationally
        expensive. To avoid this, one can add a return\_units property to the model,
        see [return\_units](https://docs.astropy.org/en/stable/modeling/add-units.html#models-return-units "(in Astropy v8.0)").

    plot\_grid(*\**, *ax=None*, *vmax\_scale=None*, *peak\_norm=False*, *deltas=False*, *cmap='viridis'*, *dividers=True*, *divider\_color='darkgray'*, *divider\_ls='-'*, *figsize=None*)[[source]](../_modules/photutils/psf/gridded_models.html#GriddedPSFModel.plot_grid)[#](#photutils.psf.GriddedPSFModel.plot_grid "Link to this definition")
    :   Plot the grid of ePSF models.

        Parameters:
        :   **ax**[`matplotlib.axes.Axes`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.html#matplotlib.axes.Axes "(in Matplotlib v3.11.2)") or [`None`](https://docs.python.org/3/builtins/constants.html#None "(in Python v3.15)"), optional
            :   The matplotlib axes on which to plot. If [`None`](https://docs.python.org/3/builtins/constants.html#None "(in Python v3.15)"), a new
                figure and axes are created.

            **vmax\_scale**float or [`None`](https://docs.python.org/3/builtins/constants.html#None "(in Python v3.15)"), optional
            :   Scale factor to apply to the image stretch limits. This
                value is multiplied by the maximum of the plotted data (the
                ePSF data, or the ePSF differences if `deltas=True`) to
                determine the plotting `vmax`. If [`None`](https://docs.python.org/3/builtins/constants.html#None "(in Python v3.15)"), the value is 1.0
                for the ePSF data and 0.03 for the ePSF differences. If
                `deltas=True`, `vmin` is set to `-vmax`. Otherwise
                `vmin` is set to `vmax / 1e4`.

            **peak\_norm**bool, optional
            :   Whether to normalize the ePSF data by the peak value. The
                default shows the ePSF flux per pixel. If `deltas=True`,
                the differences are divided by the peak of the average
                ePSF.

            **deltas**bool, optional
            :   Set to [`True`](https://docs.python.org/3/builtins/constants.html#True "(in Python v3.15)") to show the differences between each ePSF
                and the average ePSF.

            **cmap**str or [`matplotlib.colors.Colormap`](https://matplotlib.org/stable/api/_as_gen/matplotlib.colors.Colormap.html#matplotlib.colors.Colormap "(in Matplotlib v3.11.2)"), optional
            :   The colormap to use. The default is ‘viridis’.

            **dividers**bool, optional
            :   Whether to show divider lines between the ePSFs.

            **divider\_color, divider\_ls**str, optional
            :   Matplotlib color and linestyle options for the divider
                lines between ePSFs. These keywords have no effect unless
                `dividers=True`.

            **figsize**(float, float), optional
            :   The figure (width, height) in inches. It is used only if
                `ax` is [`None`](https://docs.python.org/3/builtins/constants.html#None "(in Python v3.15)").

        Returns:
        :   **fig**[`matplotlib.figure.Figure`](https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.html#matplotlib.figure.Figure "(in Matplotlib v3.11.2)")
            :   The matplotlib figure object. This is a new figure if
                `ax=None`, otherwise the figure of `ax`. Use
                `fig.savefig()` to save the figure to a file.

        Raises:
        :   ValueError
            :   If `deltas=True` and all ePSFs in the grid are blank (all
                pixels are zero).

        Notes

        This method returns a figure object. If you are using this
        method in a script, you will need to call `fig.show()` to
        display the figure. If you are using this method in a Jupyter
        notebook, the figure will be displayed automatically.

        When in a notebook, if you do not store the return value of this
        function, the figure will be displayed twice due to the REPL
        automatically displaying the return value of the last function
        call. Alternatively, you can append a semicolon to the end of
        the function call to suppress the display of the return value.

    prepare\_inputs(*\*inputs*, *model\_set\_axis=None*, *equivalencies=None*, *\*\*kwargs*)[#](#photutils.psf.GriddedPSFModel.prepare_inputs "Link to this definition")
    :   This method is used in [`__call__`](https://docs.astropy.org/en/stable/api/astropy.modeling.Model.html#astropy.modeling.Model.__call__ "(in Astropy v8.0)") to ensure
        that all the inputs to the model can be broadcast into compatible
        shapes (if one or both of them are input as arrays), particularly if
        there are more than one parameter sets. This also makes sure that (if
        applicable) the units of the input will be compatible with the evaluate
        method.

    prepare\_outputs(*broadcasted\_shapes*, *\*outputs*, *\*\*kwargs*)[#](#photutils.psf.GriddedPSFModel.prepare_outputs "Link to this definition")

    classmethod rename(*name=None*, *inputs=None*, *outputs=None*)[#](#photutils.psf.GriddedPSFModel.rename "Link to this definition")
    :   Return a copy of this model with a new name.

    render(*out=None*, *coords=None*)[#](#photutils.psf.GriddedPSFModel.render "Link to this definition")
    :   Evaluate a model at fixed positions, respecting the `bounding_box`.

        The key difference relative to evaluating the model directly is that
        this method is limited to a bounding box if the
        [`bounding_box`](https://docs.astropy.org/en/stable/api/astropy.modeling.Model.html#astropy.modeling.Model.bounding_box "(in Astropy v8.0)") attribute is set.

        Parameters:
        :   **out**[`numpy.ndarray`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray "(in NumPy v2.5)"), optional
            :   An array that the evaluated model will be added to. If this is not
                given (or given as `None`), a new array will be created.

            **coords**array-like, optional
            :   An array to be used to translate from the model’s input coordinates
                to the `out` array. It should have the property that
                `self(coords)` yields the same shape as `out`. If `out` is
                not specified, `coords` will be used to determine the shape of
                the returned array. If this is not provided (or None), the model
                will be evaluated on a grid determined by
                [`bounding_box`](https://docs.astropy.org/en/stable/api/astropy.modeling.Model.html#astropy.modeling.Model.bounding_box "(in Astropy v8.0)").

        Returns:
        :   **out**[`numpy.ndarray`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray "(in NumPy v2.5)")
            :   The model added to `out` if `out` is not `None`,
                or else a new array from evaluating the model
                over `coords`. If `out` and `coords` are
                both [`None`](https://docs.python.org/3/builtins/constants.html#None "(in Python v3.15)"), the returned array is limited to the
                [`bounding_box`](https://docs.astropy.org/en/stable/api/astropy.modeling.Model.html#astropy.modeling.Model.bounding_box "(in Astropy v8.0)") limits. If
                [`bounding_box`](https://docs.astropy.org/en/stable/api/astropy.modeling.Model.html#astropy.modeling.Model.bounding_box "(in Astropy v8.0)") is [`None`](https://docs.python.org/3/builtins/constants.html#None "(in Python v3.15)"), `arr` or
                `coords` must be passed.

        Raises:
        :   ValueError
            :   If `coords` are not given and the
                [`bounding_box`](https://docs.astropy.org/en/stable/api/astropy.modeling.Model.html#astropy.modeling.Model.bounding_box "(in Astropy v8.0)") of this model is not
                set.

        Examples

        [Efficient Model Rendering with Bounding Boxes](https://docs.astropy.org/en/stable/modeling/models.html#id2 "(in Astropy v8.0)")

    set\_slice\_args(*\*args*)[#](#photutils.psf.GriddedPSFModel.set_slice_args "Link to this definition")

    strip\_units\_from\_tree()[#](#photutils.psf.GriddedPSFModel.strip_units_from_tree "Link to this definition")

    sum\_of\_implicit\_terms(*\*args*, *\*\*kwargs*)[#](#photutils.psf.GriddedPSFModel.sum_of_implicit_terms "Link to this definition")
    :   Evaluate the sum of any implicit model terms on some input variables.
        This includes any fixed terms used in evaluating a linear model that
        do not have corresponding parameters exposed to the user. The
        prototypical case is [`astropy.modeling.functional_models.Shift`](https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Shift.html#astropy.modeling.functional_models.Shift "(in Astropy v8.0)"), which
        corresponds to a function y = a + bx, where b=1 is intrinsically fixed
        by the type of model, such that sum\_of\_implicit\_terms(x) == x. This
        method is needed by linear fitters to correct the dependent variable
        for the implicit term(s) when solving for the remaining terms
        (ie. a = y - bx).

    with\_units\_from\_data(*\*\*kwargs*)[#](#photutils.psf.GriddedPSFModel.with_units_from_data "Link to this definition")
    :   Return an instance of the model which has units for which the parameter
        values are compatible with the data units specified.

        The input and output Quantity objects should be given as keyword
        arguments.

        Notes

        This method is needed in order to be able to fit models with units in
        the parameters, since we need to temporarily strip away the units from
        the model during the fitting (which might be done by e.g. scipy
        functions).

        The units that the parameters will gain are not necessarily the units
        of the input data, but are derived from them. Model subclasses that
        want fitting to work in the presence of quantities need to define a
        `_parameter_units_for_data_units` method that takes the input and output
        units (as two dictionaries) and returns a dictionary giving the target
        units for each parameter.

    without\_units\_for\_data(*\*\*kwargs*)[#](#photutils.psf.GriddedPSFModel.without_units_for_data "Link to this definition")
    :   Return an instance of the model for which the parameter values have
        been converted to the right units for the data, then the units have
        been stripped away.

        The input and output Quantity objects should be given as keyword
        arguments.

        Notes

        This method is needed in order to be able to fit models with units in
        the parameters, since we need to temporarily strip away the units from
        the model during the fitting (which might be done by e.g. scipy
        functions).

        The units that the parameters should be converted to are not
        necessarily the units of the input data, but are derived from them.
        Model subclasses that want fitting to work in the presence of
        quantities need to define a `_parameter_units_for_data_units` method
        that takes the input and output units (as two dictionaries) and
        returns a dictionary giving the target units for each parameter.

[previous

GaussianPSF](photutils.psf.GaussianPSF.html "previous page")
[next

GriddedPSFModelRead](photutils.psf.GriddedPSFModelRead.html "next page")

On this page

* [`GriddedPSFModel`](#photutils.psf.GriddedPSFModel)
  + [`GriddedPSFModel.bbox_with_units`](#photutils.psf.GriddedPSFModel.bbox_with_units)
  + [`GriddedPSFModel.bounding_box`](#photutils.psf.GriddedPSFModel.bounding_box)
  + [`GriddedPSFModel.bounds`](#photutils.psf.GriddedPSFModel.bounds)
  + [`GriddedPSFModel.col_fit_deriv`](#photutils.psf.GriddedPSFModel.col_fit_deriv)
  + [`GriddedPSFModel.cov_matrix`](#photutils.psf.GriddedPSFModel.cov_matrix)
  + [`GriddedPSFModel.data`](#photutils.psf.GriddedPSFModel.data)
  + [`GriddedPSFModel.eqcons`](#photutils.psf.GriddedPSFModel.eqcons)
  + [`GriddedPSFModel.fittable`](#photutils.psf.GriddedPSFModel.fittable)
  + [`GriddedPSFModel.fixed`](#photutils.psf.GriddedPSFModel.fixed)
  + [`GriddedPSFModel.flux`](#photutils.psf.GriddedPSFModel.flux)
  + [`GriddedPSFModel.grid_shape`](#photutils.psf.GriddedPSFModel.grid_shape)
  + [`GriddedPSFModel.grid_xypos`](#photutils.psf.GriddedPSFModel.grid_xypos)
  + [`GriddedPSFModel.has_bounds`](#photutils.psf.GriddedPSFModel.has_bounds)
  + [`GriddedPSFModel.has_fixed`](#photutils.psf.GriddedPSFModel.has_fixed)
  + [`GriddedPSFModel.has_tied`](#photutils.psf.GriddedPSFModel.has_tied)
  + [`GriddedPSFModel.has_user_bounding_box`](#photutils.psf.GriddedPSFModel.has_user_bounding_box)
  + [`GriddedPSFModel.has_user_inverse`](#photutils.psf.GriddedPSFModel.has_user_inverse)
  + [`GriddedPSFModel.ineqcons`](#photutils.psf.GriddedPSFModel.ineqcons)
  + [`GriddedPSFModel.input_units`](#photutils.psf.GriddedPSFModel.input_units)
  + [`GriddedPSFModel.input_units_allow_dimensionless`](#photutils.psf.GriddedPSFModel.input_units_allow_dimensionless)
  + [`GriddedPSFModel.input_units_equivalencies`](#photutils.psf.GriddedPSFModel.input_units_equivalencies)
  + [`GriddedPSFModel.input_units_strict`](#photutils.psf.GriddedPSFModel.input_units_strict)
  + [`GriddedPSFModel.inputs`](#photutils.psf.GriddedPSFModel.inputs)
  + [`GriddedPSFModel.inverse`](#photutils.psf.GriddedPSFModel.inverse)
  + [`GriddedPSFModel.linear`](#photutils.psf.GriddedPSFModel.linear)
  + [`GriddedPSFModel.meta`](#photutils.psf.GriddedPSFModel.meta)
  + [`GriddedPSFModel.model_constraints`](#photutils.psf.GriddedPSFModel.model_constraints)
  + [`GriddedPSFModel.model_set_axis`](#photutils.psf.GriddedPSFModel.model_set_axis)
  + [`GriddedPSFModel.n_inputs`](#photutils.psf.GriddedPSFModel.n_inputs)
  + [`GriddedPSFModel.n_outputs`](#photutils.psf.GriddedPSFModel.n_outputs)
  + [`GriddedPSFModel.n_submodels`](#photutils.psf.GriddedPSFModel.n_submodels)
  + [`GriddedPSFModel.name`](#photutils.psf.GriddedPSFModel.name)
  + [`GriddedPSFModel.origin`](#photutils.psf.GriddedPSFModel.origin)
  + [`GriddedPSFModel.outputs`](#photutils.psf.GriddedPSFModel.outputs)
  + [`GriddedPSFModel.oversampling`](#photutils.psf.GriddedPSFModel.oversampling)
  + [`GriddedPSFModel.param_names`](#photutils.psf.GriddedPSFModel.param_names)
  + [`GriddedPSFModel.param_sets`](#photutils.psf.GriddedPSFModel.param_sets)
  + [`GriddedPSFModel.parameter_constraints`](#photutils.psf.GriddedPSFModel.parameter_constraints)
  + [`GriddedPSFModel.parameters`](#photutils.psf.GriddedPSFModel.parameters)
  + [`GriddedPSFModel.read`](#photutils.psf.GriddedPSFModel.read)
  + [`GriddedPSFModel.return_units`](#photutils.psf.GriddedPSFModel.return_units)
  + [`GriddedPSFModel.separable`](#photutils.psf.GriddedPSFModel.separable)
  + [`GriddedPSFModel.standard_broadcasting`](#photutils.psf.GriddedPSFModel.standard_broadcasting)
  + [`GriddedPSFModel.stds`](#photutils.psf.GriddedPSFModel.stds)
  + [`GriddedPSFModel.sync_constraints`](#photutils.psf.GriddedPSFModel.sync_constraints)
  + [`GriddedPSFModel.tied`](#photutils.psf.GriddedPSFModel.tied)
  + [`GriddedPSFModel.uses_quantity`](#photutils.psf.GriddedPSFModel.uses_quantity)
  + [`GriddedPSFModel.x_0`](#photutils.psf.GriddedPSFModel.x_0)
  + [`GriddedPSFModel.y_0`](#photutils.psf.GriddedPSFModel.y_0)
  + [`GriddedPSFModel.__call__()`](#photutils.psf.GriddedPSFModel.__call__)
  + [`GriddedPSFModel.coerce_units()`](#photutils.psf.GriddedPSFModel.coerce_units)
  + [`GriddedPSFModel.copy()`](#photutils.psf.GriddedPSFModel.copy)
  + [`GriddedPSFModel.deepcopy()`](#photutils.psf.GriddedPSFModel.deepcopy)
  + [`GriddedPSFModel.evaluate()`](#photutils.psf.GriddedPSFModel.evaluate)
  + [`GriddedPSFModel.fit_deriv()`](#photutils.psf.GriddedPSFModel.fit_deriv)
  + [`GriddedPSFModel.get_bounding_box()`](#photutils.psf.GriddedPSFModel.get_bounding_box)
  + [`GriddedPSFModel.has_inverse()`](#photutils.psf.GriddedPSFModel.has_inverse)
  + [`GriddedPSFModel.input_shape()`](#photutils.psf.GriddedPSFModel.input_shape)
  + [`GriddedPSFModel.output_units()`](#photutils.psf.GriddedPSFModel.output_units)
  + [`GriddedPSFModel.plot_grid()`](#photutils.psf.GriddedPSFModel.plot_grid)
  + [`GriddedPSFModel.prepare_inputs()`](#photutils.psf.GriddedPSFModel.prepare_inputs)
  + [`GriddedPSFModel.prepare_outputs()`](#photutils.psf.GriddedPSFModel.prepare_outputs)
  + [`GriddedPSFModel.rename()`](#photutils.psf.GriddedPSFModel.rename)
  + [`GriddedPSFModel.render()`](#photutils.psf.GriddedPSFModel.render)
  + [`GriddedPSFModel.set_slice_args()`](#photutils.psf.GriddedPSFModel.set_slice_args)
  + [`GriddedPSFModel.strip_units_from_tree()`](#photutils.psf.GriddedPSFModel.strip_units_from_tree)
  + [`GriddedPSFModel.sum_of_implicit_terms()`](#photutils.psf.GriddedPSFModel.sum_of_implicit_terms)
  + [`GriddedPSFModel.with_units_from_data()`](#photutils.psf.GriddedPSFModel.with_units_from_data)
  + [`GriddedPSFModel.without_units_for_data()`](#photutils.psf.GriddedPSFModel.without_units_for_data)

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
- https://docs.astropy.org/en/stable/api/astropy.modeling.CompoundModel.html#astropy.modeling.CompoundModel
- https://docs.astropy.org/en/stable/api/astropy.modeling.Fittable2DModel.html#astropy.modeling.Fittable2DModel
- https://docs.astropy.org/en/stable/api/astropy.modeling.Model.html#astropy.modeling.Model
- https://docs.astropy.org/en/stable/api/astropy.modeling.Model.html#astropy.modeling.Model.__call__
- https://docs.astropy.org/en/stable/api/astropy.modeling.Model.html#astropy.modeling.Model.bounding_box
- https://docs.astropy.org/en/stable/api/astropy.modeling.Model.html#astropy.modeling.Model.inputs
- https://docs.astropy.org/en/stable/api/astropy.modeling.Model.html#astropy.modeling.Model.outputs
- https://docs.astropy.org/en/stable/api/astropy.modeling.Parameter.html#astropy.modeling.Parameter
- https://docs.astropy.org/en/stable/api/astropy.modeling.custom_model.html#astropy.modeling.custom_model
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Shift.html#astropy.modeling.functional_models.Shift
- https://docs.astropy.org/en/stable/api/astropy.modeling.mappings.UnitsMapping.html#astropy.modeling.mappings.UnitsMapping
- https://docs.astropy.org/en/stable/api/astropy.modeling.polynomial.PolynomialModel.html#astropy.modeling.polynomial.PolynomialModel
- https://docs.astropy.org/en/stable/api/astropy.nddata.NDData.html#astropy.nddata.NDData
- https://docs.astropy.org/en/stable/api/astropy.units.Quantity.html#astropy.units.Quantity
- https://docs.astropy.org/en/stable/modeling/add-units.html#models-return-units
- https://docs.astropy.org/en/stable/modeling/models.html#id2
- https://docs.astropy.org/en/stable/modeling/models.html#modeling-model-sets
- https://docs.astropy.org/projects/photutils/en/stable/_modules/photutils/psf/gridded_models.html#GriddedPSFModel
- https://docs.astropy.org/projects/photutils/en/stable/_modules/photutils/psf/gridded_models.html#GriddedPSFModel.copy
- https://docs.astropy.org/projects/photutils/en/stable/_modules/photutils/psf/gridded_models.html#GriddedPSFModel.deepcopy
- https://docs.astropy.org/projects/photutils/en/stable/_modules/photutils/psf/gridded_models.html#GriddedPSFModel.evaluate
- https://docs.astropy.org/projects/photutils/en/stable/_modules/photutils/psf/gridded_models.html#GriddedPSFModel.fit_deriv
- https://docs.astropy.org/projects/photutils/en/stable/_modules/photutils/psf/gridded_models.html#GriddedPSFModel.origin
- https://docs.astropy.org/projects/photutils/en/stable/_modules/photutils/psf/gridded_models.html#GriddedPSFModel.plot_grid
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
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.detection.IRAFStarFinder.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.detection.StarFinder.html
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
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.GriddedPSFModelRead.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.ImagePSF.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.ImagePSF.html#photutils.psf.ImagePSF
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
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.make_epsf_from_psf.html#photutils.psf.make_epsf_from_psf
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.make_psf_model.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.make_psf_model_image.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.stdpsf_reader.html
- https://docs.astropy.org/projects/photutils/en/stable/api/photutils.psf.stdpsf_reader.html#photutils.psf.stdpsf_reader
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
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/detection.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/epsf_building.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/geometry.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/grouping.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/index.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/isophote.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/isophote_faq.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/morphology.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/psf.html
- https://docs.astropy.org/projects/photutils/en/stable/user_guide/psf.html#psf-image-models
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
- https://docs.python.org/3/builtins/constants.html#None
- https://docs.python.org/3/builtins/constants.html#True
- https://docs.python.org/3/builtins/exceptions.html#NotImplementedError
- https://docs.python.org/3/builtins/stdtypes.html#tuple
- https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.RectBivariateSpline.html#scipy.interpolate.RectBivariateSpline
- https://github.com/astropy/photutils
- https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.html#matplotlib.axes.Axes
- https://matplotlib.org/stable/api/_as_gen/matplotlib.colors.Colormap.html#matplotlib.colors.Colormap
- https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.html#matplotlib.figure.Figure
- https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray
- https://numpy.org/doc/stable/reference/index.html#module-numpy
- https://photutils.readthedocs.io
- https://reproject.readthedocs.io
- https://specreduce.readthedocs.io
- https://specutils.readthedocs.io
