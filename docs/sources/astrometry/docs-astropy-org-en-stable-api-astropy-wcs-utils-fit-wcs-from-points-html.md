---
source: https://docs.astropy.org/en/stable/api/astropy.wcs.utils.fit_wcs_from_points.html
fetched: 2026-11-14
status: 200
---

fit\_wcs\_from\_points — Astropy v8.0.2

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

* [GitHub](https://github.com/astropy/astropy "GitHub")

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

* [GitHub](https://github.com/astropy/astropy "GitHub")

[![Logo image](../_static/astropy_logo_notext.svg)

Astropy v8.0.2](../index.html)

* [Getting Started](../index_getting_started.html)
  + [Installation](../install.html)
  + [Importing `astropy` and Sub-packages](../importing_astropy.html)
  + [Tutorials](https://learn.astropy.org/)
* [User Guide](../index_user_docs.html)
  + [Constants (`astropy.constants`)](../constants/index.html)
    - [Constant](astropy.constants.Constant.html)
    - [EMConstant](astropy.constants.EMConstant.html)
  + [Units and Quantities (`astropy.units`)](../units/index.html)
    - [Quantity](../units/quantity.html)
    - [Unit-Aware Type Annotations](../units/type_hints.html)
    - [Standard Units](../units/standard_units.html)
    - [Combining and Defining Units](../units/combining_and_defining.html)
    - [Decomposing and Composing Units](../units/decomposing_and_composing.html)
    - [Magnitudes and Other Logarithmic Units](../units/logarithmic_units.html)
    - [Structured Units](../units/structured_units.html)
    - [String Representations of Units and Quantities](../units/format.html)
    - [Equivalencies](../units/equivalencies.html)
    - [Physical Types](../units/physical_types.html)
    - [Using Prior Versions of Constants](../units/constants_versions.html)
    - [Low-Level Unit Conversion](../units/conversion.html)
    - [Reference/API](../units/ref_api.html)
      * [add\_enabled\_aliases](astropy.units.add_enabled_aliases.html)
      * [add\_enabled\_equivalencies](astropy.units.add_enabled_equivalencies.html)
      * [add\_enabled\_units](astropy.units.add_enabled_units.html)
      * [allclose](astropy.units.allclose.html)
      * [beam\_angular\_area](astropy.units.beam_angular_area.html)
      * [brightness\_temperature](astropy.units.brightness_temperature.html)
      * [def\_physical\_type](astropy.units.def_physical_type.html)
      * [def\_unit](astropy.units.def_unit.html)
      * [dimensionless\_angles](astropy.units.dimensionless_angles.html)
      * [doppler\_optical](astropy.units.doppler_optical.html)
      * [doppler\_radio](astropy.units.doppler_radio.html)
      * [doppler\_redshift](astropy.units.doppler_redshift.html)
      * [doppler\_relativistic](astropy.units.doppler_relativistic.html)
      * [get\_current\_unit\_registry](astropy.units.get_current_unit_registry.html)
      * [get\_physical\_type](astropy.units.get_physical_type.html)
      * [isclose](astropy.units.isclose.html)
      * [logarithmic](astropy.units.logarithmic.html)
      * [magnetic\_flux\_field](astropy.units.magnetic_flux_field.html)
      * [mass\_energy](astropy.units.mass_energy.html)
      * [molar\_mass\_amu](astropy.units.molar_mass_amu.html)
      * [parallax](astropy.units.parallax.html)
      * [pixel\_scale](astropy.units.pixel_scale.html)
      * [plate\_scale](astropy.units.plate_scale.html)
      * [quantity\_input](astropy.units.quantity_input.html)
      * [set\_enabled\_aliases](astropy.units.set_enabled_aliases.html)
      * [set\_enabled\_equivalencies](astropy.units.set_enabled_equivalencies.html)
      * [set\_enabled\_units](astropy.units.set_enabled_units.html)
      * [spectral](astropy.units.spectral.html)
      * [spectral\_density](astropy.units.spectral_density.html)
      * [temperature](astropy.units.temperature.html)
      * [temperature\_energy](astropy.units.temperature_energy.html)
      * [thermodynamic\_temperature](astropy.units.thermodynamic_temperature.html)
      * [zero\_point\_flux](astropy.units.zero_point_flux.html)
      * [CompositeUnit](astropy.units.CompositeUnit.html)
      * [Decibel](astropy.units.Decibel.html)
      * [DecibelUnit](astropy.units.DecibelUnit.html)
      * [Dex](astropy.units.Dex.html)
      * [DexUnit](astropy.units.DexUnit.html)
      * [Equivalency](astropy.units.Equivalency.html)
      * [FunctionQuantity](astropy.units.FunctionQuantity.html)
      * [FunctionUnitBase](astropy.units.FunctionUnitBase.html)
      * [IrreducibleUnit](astropy.units.IrreducibleUnit.html)
      * [LogQuantity](astropy.units.LogQuantity.html)
      * [LogUnit](astropy.units.LogUnit.html)
      * [MagUnit](astropy.units.MagUnit.html)
      * [Magnitude](astropy.units.Magnitude.html)
      * [NamedUnit](astropy.units.NamedUnit.html)
      * [PhysicalType](astropy.units.PhysicalType.html)
      * [PrefixUnit](astropy.units.PrefixUnit.html)
      * [Quantity](astropy.units.Quantity.html)
      * [QuantityInfo](astropy.units.QuantityInfo.html)
      * [QuantityInfoBase](astropy.units.QuantityInfoBase.html)
      * [SpecificTypeQuantity](astropy.units.SpecificTypeQuantity.html)
      * [StructuredUnit](astropy.units.StructuredUnit.html)
      * [Unit](astropy.units.Unit.html)
      * [UnitBase](astropy.units.UnitBase.html)
      * [UnitConversionError](astropy.units.UnitConversionError.html)
      * [UnitParserWarning](astropy.units.UnitParserWarning.html)
      * [UnitPrefix](astropy.units.UnitPrefix.html)
      * [UnitScaleError](astropy.units.UnitScaleError.html)
      * [UnitTypeError](astropy.units.UnitTypeError.html)
      * [UnitsError](astropy.units.UnitsError.html)
      * [UnitsWarning](astropy.units.UnitsWarning.html)
      * [UnrecognizedUnit](astropy.units.UnrecognizedUnit.html)
      * [enable](astropy.units.imperial.enable.html)
      * [enable](astropy.units.cds.enable.html)
      * [def\_physical\_type](astropy.units.physical.def_physical_type.html)
      * [get\_physical\_type](astropy.units.physical.get_physical_type.html)
      * [PhysicalType](astropy.units.physical.PhysicalType.html)
      * [get\_format](astropy.units.format.get_format.html)
      * [CDS](astropy.units.format.CDS.html)
      * [FITS](astropy.units.format.FITS.html)
      * [OGIP](astropy.units.format.OGIP.html)
      * [Base](astropy.units.format.Base.html)
      * [Console](astropy.units.format.Console.html)
      * [Generic](astropy.units.format.Generic.html)
      * [Latex](astropy.units.format.Latex.html)
      * [LatexInline](astropy.units.format.LatexInline.html)
      * [Unicode](astropy.units.format.Unicode.html)
      * [VOUnit](astropy.units.format.VOUnit.html)
  + [N-Dimensional Datasets (`astropy.nddata`)](../nddata/index.html)
    - [CCDData Class](../nddata/ccddata.html)
    - [Image Utilities](../nddata/utils.html)
    - [Utility Functions for Handling Bit Masks and Mask Arrays](../nddata/bitmask.html)
    - [Decorating Functions to Accept NDData Objects](../nddata/decorator.html)
    - [NDData](../nddata/nddata.html)
    - [Covariance](../nddata/covariance.html)
    - [Mixins for Added Functionality](../nddata/mixins/index.html)
      * [Slicing and Indexing NDData](../nddata/mixins/ndslicing.html)
      * [NDData Arithmetic](../nddata/mixins/ndarithmetic.html)
      * [I/O Mixin](../nddata/mixins/ndio.html)
    - [Subclassing](../nddata/subclassing.html)
    - [Reference/API](../nddata/ref_api.html)
      * [add\_array](astropy.nddata.add_array.html)
      * [bitfield\_to\_boolean\_mask](astropy.nddata.bitfield_to_boolean_mask.html)
      * [block\_reduce](astropy.nddata.block_reduce.html)
      * [block\_replicate](astropy.nddata.block_replicate.html)
      * [extend\_bit\_flag\_map](astropy.nddata.extend_bit_flag_map.html)
      * [extract\_array](astropy.nddata.extract_array.html)
      * [fits\_ccddata\_reader](astropy.nddata.fits_ccddata_reader.html)
      * [fits\_ccddata\_writer](astropy.nddata.fits_ccddata_writer.html)
      * [interpret\_bit\_flags](astropy.nddata.interpret_bit_flags.html)
      * [overlap\_slices](astropy.nddata.overlap_slices.html)
      * [reshape\_as\_blocks](astropy.nddata.reshape_as_blocks.html)
      * [subpixel\_indices](astropy.nddata.subpixel_indices.html)
      * [support\_nddata](astropy.nddata.support_nddata.html)
      * [BitFlagNameMap](astropy.nddata.BitFlagNameMap.html)
      * [CCDData](astropy.nddata.CCDData.html)
      * [Conf](astropy.nddata.Conf.html)
      * [Covariance](astropy.nddata.Covariance.html)
      * [Cutout2D](astropy.nddata.Cutout2D.html)
      * [FlagCollection](astropy.nddata.FlagCollection.html)
      * [IncompatibleUncertaintiesException](astropy.nddata.IncompatibleUncertaintiesException.html)
      * [InvalidBitFlag](astropy.nddata.InvalidBitFlag.html)
      * [InverseVariance](astropy.nddata.InverseVariance.html)
      * [MissingDataAssociationException](astropy.nddata.MissingDataAssociationException.html)
      * [NDArithmeticMixin](astropy.nddata.NDArithmeticMixin.html)
      * [NDData](astropy.nddata.NDData.html)
      * [NDDataArray](astropy.nddata.NDDataArray.html)
      * [NDDataBase](astropy.nddata.NDDataBase.html)
      * [NDDataRef](astropy.nddata.NDDataRef.html)
      * [NDIOMixin](astropy.nddata.NDIOMixin.html)
      * [NDSlicingMixin](astropy.nddata.NDSlicingMixin.html)
      * [NDUncertainty](astropy.nddata.NDUncertainty.html)
      * [NoOverlapError](astropy.nddata.NoOverlapError.html)
      * [PartialOverlapError](astropy.nddata.PartialOverlapError.html)
      * [StdDevUncertainty](astropy.nddata.StdDevUncertainty.html)
      * [UnknownUncertainty](astropy.nddata.UnknownUncertainty.html)
      * [VarianceUncertainty](astropy.nddata.VarianceUncertainty.html)
      * [bitfield\_to\_boolean\_mask](astropy.nddata.bitmask.bitfield_to_boolean_mask.html)
      * [extend\_bit\_flag\_map](astropy.nddata.bitmask.extend_bit_flag_map.html)
      * [interpret\_bit\_flags](astropy.nddata.bitmask.interpret_bit_flags.html)
      * [BitFlagNameMap](astropy.nddata.bitmask.BitFlagNameMap.html)
      * [InvalidBitFlag](astropy.nddata.bitmask.InvalidBitFlag.html)
      * [add\_array](astropy.nddata.utils.add_array.html)
      * [extract\_array](astropy.nddata.utils.extract_array.html)
      * [overlap\_slices](astropy.nddata.utils.overlap_slices.html)
      * [subpixel\_indices](astropy.nddata.utils.subpixel_indices.html)
      * [Cutout2D](astropy.nddata.utils.Cutout2D.html)
      * [NoOverlapError](astropy.nddata.utils.NoOverlapError.html)
      * [PartialOverlapError](astropy.nddata.utils.PartialOverlapError.html)
  + [Data Tables (`astropy.table`)](../table/index.html)
    - [Constructing a Table](../table/construct_table.html)
    - [Accessing a Table](../table/access_table.html)
    - [Modifying a Table](../table/modify_table.html)
    - [Table Operations](../table/operations.html)
    - [Table Indexing](../table/indexing.html)
    - [Masking and Missing Values](../table/masking.html)
    - [Mixin Columns](../table/mixin_columns.html)
    - [Interfacing with DataFrames](../table/dataframes.html)
    - [Interfacing with the Pandas Package](../table/pandas.html)
    - [Astropy Table and DataFrames](../table/table_and_dataframes.html)
    - [Table Implementation Details](../table/implementation_details.html)
    - [Reference/API](../table/ref_api.html)
      * [dstack](astropy.table.dstack.html)
      * [hstack](astropy.table.hstack.html)
      * [join](astropy.table.join.html)
      * [join\_distance](astropy.table.join_distance.html)
      * [join\_skycoord](astropy.table.join_skycoord.html)
      * [represent\_mixins\_as\_columns](astropy.table.represent_mixins_as_columns.html)
      * [setdiff](astropy.table.setdiff.html)
      * [unique](astropy.table.unique.html)
      * [vstack](astropy.table.vstack.html)
      * [BST](astropy.table.BST.html)
      * [Column](astropy.table.Column.html)
      * [ColumnGroups](astropy.table.ColumnGroups.html)
      * [ColumnInfo](astropy.table.ColumnInfo.html)
      * [Conf](astropy.table.Conf.html)
      * [JSViewer](astropy.table.JSViewer.html)
      * [MaskedColumn](astropy.table.MaskedColumn.html)
      * [NdarrayMixin](astropy.table.NdarrayMixin.html)
      * [PprintIncludeExclude](astropy.table.PprintIncludeExclude.html)
      * [QTable](astropy.table.QTable.html)
      * [Row](astropy.table.Row.html)
      * [SCEngine](astropy.table.SCEngine.html)
      * [SerializedColumn](astropy.table.SerializedColumn.html)
      * [SortedArray](astropy.table.SortedArray.html)
      * [StringTruncateWarning](astropy.table.StringTruncateWarning.html)
      * [Table](astropy.table.Table.html)
      * [TableAttribute](astropy.table.TableAttribute.html)
      * [TableColumns](astropy.table.TableColumns.html)
      * [TableFormatter](astropy.table.TableFormatter.html)
      * [TableGroups](astropy.table.TableGroups.html)
      * [TableMergeError](astropy.table.TableMergeError.html)
      * [TableReplaceWarning](astropy.table.TableReplaceWarning.html)
      * [classic](astropy.table.notebook_backends.classic.html)
      * [ipydatagrid](astropy.table.notebook_backends.ipydatagrid.html)
  + [Time and Dates (`astropy.time`)](../time/index.html)
    - [Reference/API](../time/ref_api.html)
      * [update\_leap\_seconds](astropy.time.update_leap_seconds.html)
      * [AstropyDatetimeLeapSecondWarning](astropy.time.AstropyDatetimeLeapSecondWarning.html)
      * [Conf](astropy.time.Conf.html)
      * [OperandTypeError](astropy.time.OperandTypeError.html)
      * [ScaleValueError](astropy.time.ScaleValueError.html)
      * [Time](astropy.time.Time.html)
      * [TimeBase](astropy.time.TimeBase.html)
      * [TimeBesselianEpoch](astropy.time.TimeBesselianEpoch.html)
      * [TimeBesselianEpochString](astropy.time.TimeBesselianEpochString.html)
      * [TimeCxcSec](astropy.time.TimeCxcSec.html)
      * [TimeDatetime](astropy.time.TimeDatetime.html)
      * [TimeDatetime64](astropy.time.TimeDatetime64.html)
      * [TimeDecimalYear](astropy.time.TimeDecimalYear.html)
      * [TimeDelta](astropy.time.TimeDelta.html)
      * [TimeDeltaDatetime](astropy.time.TimeDeltaDatetime.html)
      * [TimeDeltaFormat](astropy.time.TimeDeltaFormat.html)
      * [TimeDeltaJD](astropy.time.TimeDeltaJD.html)
      * [TimeDeltaMissingUnitWarning](astropy.time.TimeDeltaMissingUnitWarning.html)
      * [TimeDeltaNumeric](astropy.time.TimeDeltaNumeric.html)
      * [TimeDeltaQuantityString](astropy.time.TimeDeltaQuantityString.html)
      * [TimeDeltaSec](astropy.time.TimeDeltaSec.html)
      * [TimeEpochDate](astropy.time.TimeEpochDate.html)
      * [TimeEpochDateString](astropy.time.TimeEpochDateString.html)
      * [TimeFITS](astropy.time.TimeFITS.html)
      * [TimeFormat](astropy.time.TimeFormat.html)
      * [TimeFromEpoch](astropy.time.TimeFromEpoch.html)
      * [TimeGPS](astropy.time.TimeGPS.html)
      * [TimeGalexSec](astropy.time.TimeGalexSec.html)
      * [TimeISO](astropy.time.TimeISO.html)
      * [TimeISOT](astropy.time.TimeISOT.html)
      * [TimeInfo](astropy.time.TimeInfo.html)
      * [TimeInfoBase](astropy.time.TimeInfoBase.html)
      * [TimeJD](astropy.time.TimeJD.html)
      * [TimeJulianEpoch](astropy.time.TimeJulianEpoch.html)
      * [TimeJulianEpochString](astropy.time.TimeJulianEpochString.html)
      * [TimeMJD](astropy.time.TimeMJD.html)
      * [TimeNumeric](astropy.time.TimeNumeric.html)
      * [TimePlotDate](astropy.time.TimePlotDate.html)
      * [TimeString](astropy.time.TimeString.html)
      * [TimeUnique](astropy.time.TimeUnique.html)
      * [TimeUnix](astropy.time.TimeUnix.html)
      * [TimeUnixTai](astropy.time.TimeUnixTai.html)
      * [TimeYMDHMS](astropy.time.TimeYMDHMS.html)
      * [TimeYearDayTime](astropy.time.TimeYearDayTime.html)
      * [TimezoneInfo](astropy.time.TimezoneInfo.html)
  + [Time Series (`astropy.timeseries`)](../timeseries/index.html)
    - [Creating Time Series](../timeseries/initializing.html)
    - [Reading and Writing Time Series](../timeseries/io.html)
    - [Accessing Data in Time Series](../timeseries/data_access.html)
    - [Converting between Different Time Representations](../timeseries/times.html)
    - [Manipulation and Analysis of Time Series](../timeseries/analysis.html)
    - [Masking Values in Time Series](../timeseries/masking.html)
    - [Interfacing with the Pandas Package](../timeseries/pandas.html)
    - [Lomb-Scargle Periodograms](../timeseries/lombscargle.html)
    - [Lomb-Scargle Periodograms for Multiband Data](../timeseries/lombscarglemb.html)
    - [Box Least Squares (BLS) Periodogram](../timeseries/bls.html)
    - [Reference/API](../timeseries/ref_api.html)
      * [aggregate\_downsample](astropy.timeseries.aggregate_downsample.html)
      * [autocheck\_required\_columns](astropy.timeseries.autocheck_required_columns.html)
      * [BasePeriodogram](astropy.timeseries.BasePeriodogram.html)
      * [BaseTimeSeries](astropy.timeseries.BaseTimeSeries.html)
      * [BinnedTimeSeries](astropy.timeseries.BinnedTimeSeries.html)
      * [BoxLeastSquares](astropy.timeseries.BoxLeastSquares.html)
      * [BoxLeastSquaresResults](astropy.timeseries.BoxLeastSquaresResults.html)
      * [LombScargle](astropy.timeseries.LombScargle.html)
      * [LombScargleMultiband](astropy.timeseries.LombScargleMultiband.html)
      * [TimeSeries](astropy.timeseries.TimeSeries.html)
      * [kepler\_fits\_reader](astropy.timeseries.io.kepler_fits_reader.html)
  + [Astronomical Coordinate Systems (`astropy.coordinates`)](../coordinates/index.html)
    - [Working with Angles](../coordinates/angles.html)
    - [Using the SkyCoord High-Level Class](../coordinates/skycoord.html)
    - [Transforming between Systems](../coordinates/transforming.html)
    - [Solar System Ephemerides](../coordinates/solarsystem.html)
    - [Working with Earth Satellites Using Astropy Coordinates](../coordinates/satellites.html)
    - [Formatting Coordinate Strings](../coordinates/formatting.html)
    - [Separations, Offsets, Catalog Matching, and Related Functionality](../coordinates/matchsep.html)
    - [Using and Designing Coordinate Representations](../coordinates/representations.html)
    - [Using and Designing Coordinate Frames](../coordinates/frames.html)
    - [Working with Velocities in Astropy Coordinates](../coordinates/velocities.html)
    - [Accounting for Space Motion](../coordinates/apply_space_motion.html)
    - [Using the SpectralCoord Class](../coordinates/spectralcoord.html)
    - [Using the `StokesCoord` Class](../coordinates/stokescoord.html)
    - [Description of the Galactocentric Coordinate Frame](../coordinates/galactocentric.html)
    - [Usage Tips/Suggestions for Methods That Access Remote Resources](../coordinates/remote_methods.html)
    - [Common mistakes](../coordinates/common_errors.html)
    - [Important Definitions](../coordinates/definitions.html)
    - [Fast In-Place Modification of Coordinates](../coordinates/inplace.html)
    - [Example Gallery](../coordinates/example_gallery_index.html)
      * [Transforming positions and velocities to and from a Galactocentric frame](../coordinates/example_gallery_plot_galactocentric_frame.html)
      * [Create a new coordinate frame class for Mars](../coordinates/example_gallery_plot_mars_coordinate_frame.html)
      * [Determining and plotting the altitude/azimuth of a celestial object](../coordinates/example_gallery_plot_obs_planning.html)
      * [Create a new coordinate class (for the Sagittarius stream)](../coordinates/example_gallery_plot_sgr_coordinate_frame.html)
      * [Convert a radial velocity to the Galactic Standard of Rest (GSR)](../coordinates/example_gallery_rv_to_gsr.html)
    - [Reference/API](../coordinates/ref_api.html)
      * [angular\_separation](astropy.coordinates.angular_separation.html)
      * [cartesian\_to\_spherical](astropy.coordinates.cartesian_to_spherical.html)
      * [concatenate](astropy.coordinates.concatenate.html)
      * [concatenate\_representations](astropy.coordinates.concatenate_representations.html)
      * [custom\_stokes\_symbol\_mapping](astropy.coordinates.custom_stokes_symbol_mapping.html)
      * [get\_body](astropy.coordinates.get_body.html)
      * [get\_body\_barycentric](astropy.coordinates.get_body_barycentric.html)
      * [get\_body\_barycentric\_posvel](astropy.coordinates.get_body_barycentric_posvel.html)
      * [get\_constellation](astropy.coordinates.get_constellation.html)
      * [get\_icrs\_coordinates](astropy.coordinates.get_icrs_coordinates.html)
      * [get\_sun](astropy.coordinates.get_sun.html)
      * [golden\_spiral\_grid](astropy.coordinates.golden_spiral_grid.html)
      * [is\_rotation\_or\_reflection](astropy.coordinates.is_rotation_or_reflection.html)
      * [make\_transform\_graph\_docs](astropy.coordinates.make_transform_graph_docs.html)
      * [match\_coordinates\_3d](astropy.coordinates.match_coordinates_3d.html)
      * [match\_coordinates\_sky](astropy.coordinates.match_coordinates_sky.html)
      * [offset\_by](astropy.coordinates.offset_by.html)
      * [position\_angle](astropy.coordinates.position_angle.html)
      * [rotation\_matrix](astropy.coordinates.rotation_matrix.html)
      * [search\_around\_3d](astropy.coordinates.search_around_3d.html)
      * [search\_around\_sky](astropy.coordinates.search_around_sky.html)
      * [spherical\_to\_cartesian](astropy.coordinates.spherical_to_cartesian.html)
      * [uniform\_spherical\_random\_surface](astropy.coordinates.uniform_spherical_random_surface.html)
      * [uniform\_spherical\_random\_volume](astropy.coordinates.uniform_spherical_random_volume.html)
      * [AffineTransform](astropy.coordinates.AffineTransform.html)
      * [AltAz](astropy.coordinates.AltAz.html)
      * [Angle](astropy.coordinates.Angle.html)
      * [Attribute](astropy.coordinates.Attribute.html)
      * [BarycentricMeanEcliptic](astropy.coordinates.BarycentricMeanEcliptic.html)
      * [BarycentricTrueEcliptic](astropy.coordinates.BarycentricTrueEcliptic.html)
      * [BaseAffineTransform](astropy.coordinates.BaseAffineTransform.html)
      * [BaseBodycentricRepresentation](astropy.coordinates.BaseBodycentricRepresentation.html)
      * [BaseCoordinateFrame](astropy.coordinates.BaseCoordinateFrame.html)
      * [BaseDifferential](astropy.coordinates.BaseDifferential.html)
      * [BaseEclipticFrame](astropy.coordinates.BaseEclipticFrame.html)
      * [BaseGeodeticRepresentation](astropy.coordinates.BaseGeodeticRepresentation.html)
      * [BaseRADecFrame](astropy.coordinates.BaseRADecFrame.html)
      * [BaseRepresentation](astropy.coordinates.BaseRepresentation.html)
      * [BaseRepresentationOrDifferential](astropy.coordinates.BaseRepresentationOrDifferential.html)
      * [BaseSphericalCosLatDifferential](astropy.coordinates.BaseSphericalCosLatDifferential.html)
      * [BaseSphericalDifferential](astropy.coordinates.BaseSphericalDifferential.html)
      * [BoundsError](astropy.coordinates.BoundsError.html)
      * [CIRS](astropy.coordinates.CIRS.html)
      * [CartesianDifferential](astropy.coordinates.CartesianDifferential.html)
      * [CartesianRepresentation](astropy.coordinates.CartesianRepresentation.html)
      * [CartesianRepresentationAttribute](astropy.coordinates.CartesianRepresentationAttribute.html)
      * [CompositeTransform](astropy.coordinates.CompositeTransform.html)
      * [ConvertError](astropy.coordinates.ConvertError.html)
      * [CoordinateAttribute](astropy.coordinates.CoordinateAttribute.html)
      * [CoordinateFrameInfo](astropy.coordinates.CoordinateFrameInfo.html)
      * [CoordinateMatchResult](astropy.coordinates.CoordinateMatchResult.html)
      * [CoordinateSearchResult](astropy.coordinates.CoordinateSearchResult.html)
      * [CoordinateTransform](astropy.coordinates.CoordinateTransform.html)
      * [CustomBarycentricEcliptic](astropy.coordinates.CustomBarycentricEcliptic.html)
      * [CylindricalDifferential](astropy.coordinates.CylindricalDifferential.html)
      * [CylindricalRepresentation](astropy.coordinates.CylindricalRepresentation.html)
      * [DifferentialAttribute](astropy.coordinates.DifferentialAttribute.html)
      * [Distance](astropy.coordinates.Distance.html)
      * [DynamicMatrixTransform](astropy.coordinates.DynamicMatrixTransform.html)
      * [EarthLocation](astropy.coordinates.EarthLocation.html)
      * [EarthLocationAttribute](astropy.coordinates.EarthLocationAttribute.html)
      * [FK4](astropy.coordinates.FK4.html)
      * [FK4NoETerms](astropy.coordinates.FK4NoETerms.html)
      * [FK5](astropy.coordinates.FK5.html)
      * [FunctionTransform](astropy.coordinates.FunctionTransform.html)
      * [FunctionTransformWithFiniteDifference](astropy.coordinates.FunctionTransformWithFiniteDifference.html)
      * [GCRS](astropy.coordinates.GCRS.html)
      * [GRS80GeodeticRepresentation](astropy.coordinates.GRS80GeodeticRepresentation.html)
      * [Galactic](astropy.coordinates.Galactic.html)
      * [GalacticLSR](astropy.coordinates.GalacticLSR.html)
      * [Galactocentric](astropy.coordinates.Galactocentric.html)
      * [GenericFrame](astropy.coordinates.GenericFrame.html)
      * [GeocentricMeanEcliptic](astropy.coordinates.GeocentricMeanEcliptic.html)
      * [GeocentricTrueEcliptic](astropy.coordinates.GeocentricTrueEcliptic.html)
      * [HADec](astropy.coordinates.HADec.html)
      * [HCRS](astropy.coordinates.HCRS.html)
      * [HeliocentricEclipticIAU76](astropy.coordinates.HeliocentricEclipticIAU76.html)
      * [HeliocentricMeanEcliptic](astropy.coordinates.HeliocentricMeanEcliptic.html)
      * [HeliocentricTrueEcliptic](astropy.coordinates.HeliocentricTrueEcliptic.html)
      * [ICRS](astropy.coordinates.ICRS.html)
      * [ITRS](astropy.coordinates.ITRS.html)
      * [IllegalHourError](astropy.coordinates.IllegalHourError.html)
      * [IllegalHourWarning](astropy.coordinates.IllegalHourWarning.html)
      * [IllegalMinuteError](astropy.coordinates.IllegalMinuteError.html)
      * [IllegalMinuteWarning](astropy.coordinates.IllegalMinuteWarning.html)
      * [IllegalSecondError](astropy.coordinates.IllegalSecondError.html)
      * [IllegalSecondWarning](astropy.coordinates.IllegalSecondWarning.html)
      * [LSR](astropy.coordinates.LSR.html)
      * [LSRD](astropy.coordinates.LSRD.html)
      * [LSRK](astropy.coordinates.LSRK.html)
      * [Latitude](astropy.coordinates.Latitude.html)
      * [Longitude](astropy.coordinates.Longitude.html)
      * [NonRotationTransformationError](astropy.coordinates.NonRotationTransformationError.html)
      * [NonRotationTransformationWarning](astropy.coordinates.NonRotationTransformationWarning.html)
      * [PhysicsSphericalDifferential](astropy.coordinates.PhysicsSphericalDifferential.html)
      * [PhysicsSphericalRepresentation](astropy.coordinates.PhysicsSphericalRepresentation.html)
      * [PrecessedGeocentric](astropy.coordinates.PrecessedGeocentric.html)
      * [QuantityAttribute](astropy.coordinates.QuantityAttribute.html)
      * [RadialDifferential](astropy.coordinates.RadialDifferential.html)
      * [RadialRepresentation](astropy.coordinates.RadialRepresentation.html)
      * [RangeError](astropy.coordinates.RangeError.html)
      * [RepresentationMapping](astropy.coordinates.RepresentationMapping.html)
      * [SkyCoord](astropy.coordinates.SkyCoord.html)
      * [SkyCoordInfo](astropy.coordinates.SkyCoordInfo.html)
      * [SkyOffsetFrame](astropy.coordinates.SkyOffsetFrame.html)
      * [SpectralCoord](astropy.coordinates.SpectralCoord.html)
      * [SpectralQuantity](astropy.coordinates.SpectralQuantity.html)
      * [SphericalCosLatDifferential](astropy.coordinates.SphericalCosLatDifferential.html)
      * [SphericalDifferential](astropy.coordinates.SphericalDifferential.html)
      * [SphericalRepresentation](astropy.coordinates.SphericalRepresentation.html)
      * [StaticMatrixTransform](astropy.coordinates.StaticMatrixTransform.html)
      * [StokesCoord](astropy.coordinates.StokesCoord.html)
      * [StokesSymbol](astropy.coordinates.StokesSymbol.html)
      * [Supergalactic](astropy.coordinates.Supergalactic.html)
      * [TEME](astropy.coordinates.TEME.html)
      * [TETE](astropy.coordinates.TETE.html)
      * [TimeAttribute](astropy.coordinates.TimeAttribute.html)
      * [TransformGraph](astropy.coordinates.TransformGraph.html)
      * [UnitSphericalCosLatDifferential](astropy.coordinates.UnitSphericalCosLatDifferential.html)
      * [UnitSphericalDifferential](astropy.coordinates.UnitSphericalDifferential.html)
      * [UnitSphericalRepresentation](astropy.coordinates.UnitSphericalRepresentation.html)
      * [UnknownSiteException](astropy.coordinates.UnknownSiteException.html)
      * [WGS72GeodeticRepresentation](astropy.coordinates.WGS72GeodeticRepresentation.html)
      * [WGS84GeodeticRepresentation](astropy.coordinates.WGS84GeodeticRepresentation.html)
      * [galactocentric\_frame\_defaults](astropy.coordinates.galactocentric_frame_defaults.html)
      * [solar\_system\_ephemeris](astropy.coordinates.solar_system_ephemeris.html)
  + [World Coordinate System (`astropy.wcs`)](../wcs/index.html)
    - [Shared Python Interface for World Coordinate Systems](../wcs/wcsapi.html)
    - [Legacy Interface](../wcs/legacy_interface.html)
    - [Supported Projections](../wcs/supported_projections.html)
    - [Example of Imaging WCS](../wcs/example_create_imaging.html)
    - [Example of Cube WCS](../wcs/example_cube_wcs.html)
    - [Example of a Planetary WCS](../wcs/creating_planetary_wcs.html)
    - [Loading From a FITS File](../wcs/loading_from_fits.html)
    - [Subsetting and Pixel Scales](../wcs/wcstools.html)
    - [Header-reading relaxation constants](../wcs/relax.html)
    - [astropy.wcs History](../wcs/history.html)
    - [Validation and Bounds checking](../wcs/validation.html)
    - [Reference/API](../wcs/reference_api.html)
      * [find\_all\_wcs](astropy.wcs.find_all_wcs.html)
      * [get\_include](astropy.wcs.get_include.html)
      * [validate](astropy.wcs.validate.html)
      * [Auxprm](astropy.wcs.Auxprm.html)
      * [Celprm](astropy.wcs.Celprm.html)
      * [DistortionLookupTable](astropy.wcs.DistortionLookupTable.html)
      * [FITSFixedWarning](astropy.wcs.FITSFixedWarning.html)
      * [InconsistentAxisTypesError](astropy.wcs.InconsistentAxisTypesError.html)
      * [InvalidCoordinateError](astropy.wcs.InvalidCoordinateError.html)
      * [InvalidPrjParametersError](astropy.wcs.InvalidPrjParametersError.html)
      * [InvalidSubimageSpecificationError](astropy.wcs.InvalidSubimageSpecificationError.html)
      * [InvalidTabularParametersError](astropy.wcs.InvalidTabularParametersError.html)
      * [InvalidTransformError](astropy.wcs.InvalidTransformError.html)
      * [NoConvergence](astropy.wcs.NoConvergence.html)
      * [NoSolutionError](astropy.wcs.NoSolutionError.html)
      * [NoWcsKeywordsFoundError](astropy.wcs.NoWcsKeywordsFoundError.html)
      * [NonseparableSubimageCoordinateSystemError](astropy.wcs.NonseparableSubimageCoordinateSystemError.html)
      * [Prjprm](astropy.wcs.Prjprm.html)
      * [SingularMatrixError](astropy.wcs.SingularMatrixError.html)
      * [Sip](astropy.wcs.Sip.html)
      * [Tabprm](astropy.wcs.Tabprm.html)
      * [WCS](astropy.wcs.WCS.html)
      * [WCSBase](astropy.wcs.WCSBase.html)
      * [WcsError](astropy.wcs.WcsError.html)
      * [Wcsprm](astropy.wcs.Wcsprm.html)
      * [Wtbarr](astropy.wcs.Wtbarr.html)
      * [add\_stokes\_axis\_to\_wcs](astropy.wcs.utils.add_stokes_axis_to_wcs.html)
      * [celestial\_frame\_to\_wcs](astropy.wcs.utils.celestial_frame_to_wcs.html)
      * [fit\_wcs\_from\_points](#)
      * [is\_proj\_plane\_distorted](astropy.wcs.utils.is_proj_plane_distorted.html)
      * [local\_partial\_pixel\_derivatives](astropy.wcs.utils.local_partial_pixel_derivatives.html)
      * [non\_celestial\_pixel\_scales](astropy.wcs.utils.non_celestial_pixel_scales.html)
      * [obsgeo\_to\_frame](astropy.wcs.utils.obsgeo_to_frame.html)
      * [pixel\_to\_pixel](astropy.wcs.utils.pixel_to_pixel.html)
      * [pixel\_to\_skycoord](astropy.wcs.utils.pixel_to_skycoord.html)
      * [proj\_plane\_pixel\_area](astropy.wcs.utils.proj_plane_pixel_area.html)
      * [proj\_plane\_pixel\_scales](astropy.wcs.utils.proj_plane_pixel_scales.html)
      * [skycoord\_to\_pixel](astropy.wcs.utils.skycoord_to_pixel.html)
      * [wcs\_to\_celestial\_frame](astropy.wcs.utils.wcs_to_celestial_frame.html)
      * [custom\_frame\_to\_wcs\_mappings](astropy.wcs.utils.custom_frame_to_wcs_mappings.html)
      * [custom\_wcs\_to\_frame\_mappings](astropy.wcs.utils.custom_wcs_to_frame_mappings.html)
      * [deserialize\_class](astropy.wcs.wcsapi.deserialize_class.html)
      * [high\_level\_objects\_to\_values](astropy.wcs.wcsapi.high_level_objects_to_values.html)
      * [sanitize\_slices](astropy.wcs.wcsapi.sanitize_slices.html)
      * [validate\_physical\_types](astropy.wcs.wcsapi.validate_physical_types.html)
      * [values\_to\_high\_level\_objects](astropy.wcs.wcsapi.values_to_high_level_objects.html)
      * [wcs\_info\_str](astropy.wcs.wcsapi.wcs_info_str.html)
      * [BaseHighLevelWCS](astropy.wcs.wcsapi.BaseHighLevelWCS.html)
      * [BaseLowLevelWCS](astropy.wcs.wcsapi.BaseLowLevelWCS.html)
      * [BaseWCSWrapper](astropy.wcs.wcsapi.BaseWCSWrapper.html)
      * [HighLevelWCSMixin](astropy.wcs.wcsapi.HighLevelWCSMixin.html)
      * [HighLevelWCSWrapper](astropy.wcs.wcsapi.HighLevelWCSWrapper.html)
      * [SlicedLowLevelWCS](astropy.wcs.wcsapi.SlicedLowLevelWCS.html)
  + [Models and Fitting (`astropy.modeling`)](../modeling/index.html)
    - [Models](../modeling/models.html)
    - [Compound Models](../modeling/compound-models.html)
    - [Model Parameters](../modeling/parameters.html)
    - [Fitting](../modeling/fitting.html)
    - [Using Units with Models and Fitting](../modeling/units.html)
    - [Performance Tips](../modeling/performance.html)
    - [Extending Models](../modeling/new-model.html)
    - [Extending Fitters](../modeling/new-fitter.html)
    - [Adding support for units to models](../modeling/add-units.html)
    - [JointFitter](../modeling/jointfitter.html)
    - [Parallel Fitting](../modeling/parallel-fitting.html)
    - [1D Models](../modeling/predef_models1D.html)
    - [2D Models](../modeling/predef_models2D.html)
    - [Physical Models](../modeling/physical_models.html)
    - [Polynomial Models](../modeling/polynomial_models.html)
    - [Powerlaw Models](../modeling/powerlaw_models.html)
    - [Spline Models](../modeling/spline_models.html)
    - [Fitting a line](../modeling/example-fitting-line.html)
    - [Fitting with constraints](../modeling/example-fitting-constraints.html)
    - [Fitting Model Sets](../modeling/example-fitting-model-sets.html)
    - [Reference/API](../modeling/reference_api.html)
      * [bind\_bounding\_box](astropy.modeling.bind_bounding_box.html)
      * [bind\_compound\_bounding\_box](astropy.modeling.bind_compound_bounding_box.html)
      * [compose\_models\_with\_units](astropy.modeling.compose_models_with_units.html)
      * [custom\_model](astropy.modeling.custom_model.html)
      * [fix\_inputs](astropy.modeling.fix_inputs.html)
      * [is\_separable](astropy.modeling.is_separable.html)
      * [separability\_matrix](astropy.modeling.separability_matrix.html)
      * [CompoundModel](astropy.modeling.CompoundModel.html)
      * [Fittable1DModel](astropy.modeling.Fittable1DModel.html)
      * [Fittable2DModel](astropy.modeling.Fittable2DModel.html)
      * [FittableModel](astropy.modeling.FittableModel.html)
      * [InputParameterError](astropy.modeling.InputParameterError.html)
      * [Model](astropy.modeling.Model.html)
      * [ModelDefinitionError](astropy.modeling.ModelDefinitionError.html)
      * [Parameter](astropy.modeling.Parameter.html)
      * [ParameterError](astropy.modeling.ParameterError.html)
      * [CompoundBoundingBox](astropy.modeling.bounding_box.CompoundBoundingBox.html)
      * [ModelBoundingBox](astropy.modeling.bounding_box.ModelBoundingBox.html)
      * [Identity](astropy.modeling.mappings.Identity.html)
      * [Mapping](astropy.modeling.mappings.Mapping.html)
      * [UnitsMapping](astropy.modeling.mappings.UnitsMapping.html)
      * [parallel\_fit\_dask](astropy.modeling.fitting.parallel_fit_dask.html)
      * [DogBoxLSQFitter](astropy.modeling.fitting.DogBoxLSQFitter.html)
      * [FitInfoArrayContainer](astropy.modeling.fitting.FitInfoArrayContainer.html)
      * [Fitter](astropy.modeling.fitting.Fitter.html)
      * [FittingWithOutlierRemoval](astropy.modeling.fitting.FittingWithOutlierRemoval.html)
      * [JointFitter](astropy.modeling.fitting.JointFitter.html)
      * [LMLSQFitter](astropy.modeling.fitting.LMLSQFitter.html)
      * [LevMarLSQFitter](astropy.modeling.fitting.LevMarLSQFitter.html)
      * [LinearLSQFitter](astropy.modeling.fitting.LinearLSQFitter.html)
      * [ModelLinearityError](astropy.modeling.fitting.ModelLinearityError.html)
      * [ModelsError](astropy.modeling.fitting.ModelsError.html)
      * [SLSQPLSQFitter](astropy.modeling.fitting.SLSQPLSQFitter.html)
      * [SimplexLSQFitter](astropy.modeling.fitting.SimplexLSQFitter.html)
      * [TRFLSQFitter](astropy.modeling.fitting.TRFLSQFitter.html)
      * [SLSQP](astropy.modeling.optimizers.SLSQP.html)
      * [Optimization](astropy.modeling.optimizers.Optimization.html)
      * [Simplex](astropy.modeling.optimizers.Simplex.html)
      * [leastsquare](astropy.modeling.statistic.leastsquare.html)
      * [leastsquare\_1d](astropy.modeling.statistic.leastsquare_1d.html)
      * [leastsquare\_2d](astropy.modeling.statistic.leastsquare_2d.html)
      * [leastsquare\_3d](astropy.modeling.statistic.leastsquare_3d.html)
      * [is\_separable](astropy.modeling.separable.is_separable.html)
      * [separability\_matrix](astropy.modeling.separable.separability_matrix.html)
      * [AiryDisk2D](astropy.modeling.functional_models.AiryDisk2D.html)
      * [ArcCosine1D](astropy.modeling.functional_models.ArcCosine1D.html)
      * [ArcSine1D](astropy.modeling.functional_models.ArcSine1D.html)
      * [ArcTangent1D](astropy.modeling.functional_models.ArcTangent1D.html)
      * [Box1D](astropy.modeling.functional_models.Box1D.html)
      * [Box2D](astropy.modeling.functional_models.Box2D.html)
      * [Const1D](astropy.modeling.functional_models.Const1D.html)
      * [Const2D](astropy.modeling.functional_models.Const2D.html)
      * [Cosine1D](astropy.modeling.functional_models.Cosine1D.html)
      * [Disk2D](astropy.modeling.functional_models.Disk2D.html)
      * [Ellipse2D](astropy.modeling.functional_models.Ellipse2D.html)
      * [Exponential1D](astropy.modeling.functional_models.Exponential1D.html)
      * [Gaussian1D](astropy.modeling.functional_models.Gaussian1D.html)
      * [Gaussian2D](astropy.modeling.functional_models.Gaussian2D.html)
      * [GeneralSersic2D](astropy.modeling.functional_models.GeneralSersic2D.html)
      * [KingProjectedAnalytic1D](astropy.modeling.functional_models.KingProjectedAnalytic1D.html)
      * [Linear1D](astropy.modeling.functional_models.Linear1D.html)
      * [Logarithmic1D](astropy.modeling.functional_models.Logarithmic1D.html)
      * [Lorentz1D](astropy.modeling.functional_models.Lorentz1D.html)
      * [Lorentz2D](astropy.modeling.functional_models.Lorentz2D.html)
      * [Moffat1D](astropy.modeling.functional_models.Moffat1D.html)
      * [Moffat2D](astropy.modeling.functional_models.Moffat2D.html)
      * [Multiply](astropy.modeling.functional_models.Multiply.html)
      * [Planar2D](astropy.modeling.functional_models.Planar2D.html)
      * [RedshiftScaleFactor](astropy.modeling.functional_models.RedshiftScaleFactor.html)
      * [RickerWavelet1D](astropy.modeling.functional_models.RickerWavelet1D.html)
      * [RickerWavelet2D](astropy.modeling.functional_models.RickerWavelet2D.html)
      * [Ring2D](astropy.modeling.functional_models.Ring2D.html)
      * [Scale](astropy.modeling.functional_models.Scale.html)
      * [Sersic1D](astropy.modeling.functional_models.Sersic1D.html)
      * [Sersic2D](astropy.modeling.functional_models.Sersic2D.html)
      * [Shift](astropy.modeling.functional_models.Shift.html)
      * [Sine1D](astropy.modeling.functional_models.Sine1D.html)
      * [Tangent1D](astropy.modeling.functional_models.Tangent1D.html)
      * [Trapezoid1D](astropy.modeling.functional_models.Trapezoid1D.html)
      * [TrapezoidDisk2D](astropy.modeling.functional_models.TrapezoidDisk2D.html)
      * [Voigt1D](astropy.modeling.functional_models.Voigt1D.html)
      * [NFW](astropy.modeling.physical_models.NFW.html)
      * [BlackBody](astropy.modeling.physical_models.BlackBody.html)
      * [Drude1D](astropy.modeling.physical_models.Drude1D.html)
      * [Plummer1D](astropy.modeling.physical_models.Plummer1D.html)
      * [BrokenPowerLaw1D](astropy.modeling.powerlaws.BrokenPowerLaw1D.html)
      * [ExponentialCutoffPowerLaw1D](astropy.modeling.powerlaws.ExponentialCutoffPowerLaw1D.html)
      * [LogParabola1D](astropy.modeling.powerlaws.LogParabola1D.html)
      * [PowerLaw1D](astropy.modeling.powerlaws.PowerLaw1D.html)
      * [Schechter1D](astropy.modeling.powerlaws.Schechter1D.html)
      * [SmoothlyBrokenPowerLaw1D](astropy.modeling.powerlaws.SmoothlyBrokenPowerLaw1D.html)
      * [SIP](astropy.modeling.polynomial.SIP.html)
      * [Chebyshev1D](astropy.modeling.polynomial.Chebyshev1D.html)
      * [Chebyshev2D](astropy.modeling.polynomial.Chebyshev2D.html)
      * [Hermite1D](astropy.modeling.polynomial.Hermite1D.html)
      * [Hermite2D](astropy.modeling.polynomial.Hermite2D.html)
      * [InverseSIP](astropy.modeling.polynomial.InverseSIP.html)
      * [Legendre1D](astropy.modeling.polynomial.Legendre1D.html)
      * [Legendre2D](astropy.modeling.polynomial.Legendre2D.html)
      * [OrthoPolynomialBase](astropy.modeling.polynomial.OrthoPolynomialBase.html)
      * [Polynomial1D](astropy.modeling.polynomial.Polynomial1D.html)
      * [Polynomial2D](astropy.modeling.polynomial.Polynomial2D.html)
      * [PolynomialModel](astropy.modeling.polynomial.PolynomialModel.html)
      * [AffineTransformation2D](astropy.modeling.projections.AffineTransformation2D.html)
      * [Conic](astropy.modeling.projections.Conic.html)
      * [Cylindrical](astropy.modeling.projections.Cylindrical.html)
      * [HEALPix](astropy.modeling.projections.HEALPix.html)
      * [Pix2SkyProjection](astropy.modeling.projections.Pix2SkyProjection.html)
      * [Projection](astropy.modeling.projections.Projection.html)
      * [PseudoConic](astropy.modeling.projections.PseudoConic.html)
      * [PseudoCylindrical](astropy.modeling.projections.PseudoCylindrical.html)
      * [QuadCube](astropy.modeling.projections.QuadCube.html)
      * [Sky2PixProjection](astropy.modeling.projections.Sky2PixProjection.html)
      * [Zenithal](astropy.modeling.projections.Zenithal.html)
      * [Pix2Sky\_ZenithalPerspective](astropy.modeling.projections.Pix2Sky_ZenithalPerspective.html)
      * [Pix2Sky\_AZP](astropy.modeling.projections.Pix2Sky_AZP.html)
      * [Pix2Sky\_SlantZenithalPerspective](astropy.modeling.projections.Pix2Sky_SlantZenithalPerspective.html)
      * [Pix2Sky\_SZP](astropy.modeling.projections.Pix2Sky_SZP.html)
      * [Pix2Sky\_Gnomonic](astropy.modeling.projections.Pix2Sky_Gnomonic.html)
      * [Pix2Sky\_TAN](astropy.modeling.projections.Pix2Sky_TAN.html)
      * [Pix2Sky\_Stereographic](astropy.modeling.projections.Pix2Sky_Stereographic.html)
      * [Pix2Sky\_STG](astropy.modeling.projections.Pix2Sky_STG.html)
      * [Pix2Sky\_SlantOrthographic](astropy.modeling.projections.Pix2Sky_SlantOrthographic.html)
      * [Pix2Sky\_SIN](astropy.modeling.projections.Pix2Sky_SIN.html)
      * [Pix2Sky\_ZenithalEquidistant](astropy.modeling.projections.Pix2Sky_ZenithalEquidistant.html)
      * [Pix2Sky\_ARC](astropy.modeling.projections.Pix2Sky_ARC.html)
      * [Pix2Sky\_ZenithalEqualArea](astropy.modeling.projections.Pix2Sky_ZenithalEqualArea.html)
      * [Pix2Sky\_ZEA](astropy.modeling.projections.Pix2Sky_ZEA.html)
      * [Pix2Sky\_Airy](astropy.modeling.projections.Pix2Sky_Airy.html)
      * [Pix2Sky\_AIR](astropy.modeling.projections.Pix2Sky_AIR.html)
      * [Pix2Sky\_CylindricalPerspective](astropy.modeling.projections.Pix2Sky_CylindricalPerspective.html)
      * [Pix2Sky\_CYP](astropy.modeling.projections.Pix2Sky_CYP.html)
      * [Pix2Sky\_CylindricalEqualArea](astropy.modeling.projections.Pix2Sky_CylindricalEqualArea.html)
      * [Pix2Sky\_CEA](astropy.modeling.projections.Pix2Sky_CEA.html)
      * [Pix2Sky\_PlateCarree](astropy.modeling.projections.Pix2Sky_PlateCarree.html)
      * [Pix2Sky\_CAR](astropy.modeling.projections.Pix2Sky_CAR.html)
      * [Pix2Sky\_Mercator](astropy.modeling.projections.Pix2Sky_Mercator.html)
      * [Pix2Sky\_MER](astropy.modeling.projections.Pix2Sky_MER.html)
      * [Pix2Sky\_SansonFlamsteed](astropy.modeling.projections.Pix2Sky_SansonFlamsteed.html)
      * [Pix2Sky\_SFL](astropy.modeling.projections.Pix2Sky_SFL.html)
      * [Pix2Sky\_Parabolic](astropy.modeling.projections.Pix2Sky_Parabolic.html)
      * [Pix2Sky\_PAR](astropy.modeling.projections.Pix2Sky_PAR.html)
      * [Pix2Sky\_Molleweide](astropy.modeling.projections.Pix2Sky_Molleweide.html)
      * [Pix2Sky\_MOL](astropy.modeling.projections.Pix2Sky_MOL.html)
      * [Pix2Sky\_HammerAitoff](astropy.modeling.projections.Pix2Sky_HammerAitoff.html)
      * [Pix2Sky\_AIT](astropy.modeling.projections.Pix2Sky_AIT.html)
      * [Pix2Sky\_ConicPerspective](astropy.modeling.projections.Pix2Sky_ConicPerspective.html)
      * [Pix2Sky\_COP](astropy.modeling.projections.Pix2Sky_COP.html)
      * [Pix2Sky\_ConicEqualArea](astropy.modeling.projections.Pix2Sky_ConicEqualArea.html)
      * [Pix2Sky\_COE](astropy.modeling.projections.Pix2Sky_COE.html)
      * [Pix2Sky\_ConicEquidistant](astropy.modeling.projections.Pix2Sky_ConicEquidistant.html)
      * [Pix2Sky\_COD](astropy.modeling.projections.Pix2Sky_COD.html)
      * [Pix2Sky\_ConicOrthomorphic](astropy.modeling.projections.Pix2Sky_ConicOrthomorphic.html)
      * [Pix2Sky\_COO](astropy.modeling.projections.Pix2Sky_COO.html)
      * [Pix2Sky\_BonneEqualArea](astropy.modeling.projections.Pix2Sky_BonneEqualArea.html)
      * [Pix2Sky\_BON](astropy.modeling.projections.Pix2Sky_BON.html)
      * [Pix2Sky\_Polyconic](astropy.modeling.projections.Pix2Sky_Polyconic.html)
      * [Pix2Sky\_PCO](astropy.modeling.projections.Pix2Sky_PCO.html)
      * [Pix2Sky\_TangentialSphericalCube](astropy.modeling.projections.Pix2Sky_TangentialSphericalCube.html)
      * [Pix2Sky\_TSC](astropy.modeling.projections.Pix2Sky_TSC.html)
      * [Pix2Sky\_COBEQuadSphericalCube](astropy.modeling.projections.Pix2Sky_COBEQuadSphericalCube.html)
      * [Pix2Sky\_CSC](astropy.modeling.projections.Pix2Sky_CSC.html)
      * [Pix2Sky\_QuadSphericalCube](astropy.modeling.projections.Pix2Sky_QuadSphericalCube.html)
      * [Pix2Sky\_QSC](astropy.modeling.projections.Pix2Sky_QSC.html)
      * [Pix2Sky\_HEALPix](astropy.modeling.projections.Pix2Sky_HEALPix.html)
      * [Pix2Sky\_HPX](astropy.modeling.projections.Pix2Sky_HPX.html)
      * [Pix2Sky\_HEALPixPolar](astropy.modeling.projections.Pix2Sky_HEALPixPolar.html)
      * [Pix2Sky\_XPH](astropy.modeling.projections.Pix2Sky_XPH.html)
      * [Sky2Pix\_ZenithalPerspective](astropy.modeling.projections.Sky2Pix_ZenithalPerspective.html)
      * [Sky2Pix\_AZP](astropy.modeling.projections.Sky2Pix_AZP.html)
      * [Sky2Pix\_SlantZenithalPerspective](astropy.modeling.projections.Sky2Pix_SlantZenithalPerspective.html)
      * [Sky2Pix\_SZP](astropy.modeling.projections.Sky2Pix_SZP.html)
      * [Sky2Pix\_Gnomonic](astropy.modeling.projections.Sky2Pix_Gnomonic.html)
      * [Sky2Pix\_TAN](astropy.modeling.projections.Sky2Pix_TAN.html)
      * [Sky2Pix\_Stereographic](astropy.modeling.projections.Sky2Pix_Stereographic.html)
      * [Sky2Pix\_STG](astropy.modeling.projections.Sky2Pix_STG.html)
      * [Sky2Pix\_SlantOrthographic](astropy.modeling.projections.Sky2Pix_SlantOrthographic.html)
      * [Sky2Pix\_SIN](astropy.modeling.projections.Sky2Pix_SIN.html)
      * [Sky2Pix\_ZenithalEquidistant](astropy.modeling.projections.Sky2Pix_ZenithalEquidistant.html)
      * [Sky2Pix\_ARC](astropy.modeling.projections.Sky2Pix_ARC.html)
      * [Sky2Pix\_ZenithalEqualArea](astropy.modeling.projections.Sky2Pix_ZenithalEqualArea.html)
      * [Sky2Pix\_ZEA](astropy.modeling.projections.Sky2Pix_ZEA.html)
      * [Sky2Pix\_Airy](astropy.modeling.projections.Sky2Pix_Airy.html)
      * [Sky2Pix\_AIR](astropy.modeling.projections.Sky2Pix_AIR.html)
      * [Sky2Pix\_CylindricalPerspective](astropy.modeling.projections.Sky2Pix_CylindricalPerspective.html)
      * [Sky2Pix\_CYP](astropy.modeling.projections.Sky2Pix_CYP.html)
      * [Sky2Pix\_CylindricalEqualArea](astropy.modeling.projections.Sky2Pix_CylindricalEqualArea.html)
      * [Sky2Pix\_CEA](astropy.modeling.projections.Sky2Pix_CEA.html)
      * [Sky2Pix\_PlateCarree](astropy.modeling.projections.Sky2Pix_PlateCarree.html)
      * [Sky2Pix\_CAR](astropy.modeling.projections.Sky2Pix_CAR.html)
      * [Sky2Pix\_Mercator](astropy.modeling.projections.Sky2Pix_Mercator.html)
      * [Sky2Pix\_MER](astropy.modeling.projections.Sky2Pix_MER.html)
      * [Sky2Pix\_SansonFlamsteed](astropy.modeling.projections.Sky2Pix_SansonFlamsteed.html)
      * [Sky2Pix\_SFL](astropy.modeling.projections.Sky2Pix_SFL.html)
      * [Sky2Pix\_Parabolic](astropy.modeling.projections.Sky2Pix_Parabolic.html)
      * [Sky2Pix\_PAR](astropy.modeling.projections.Sky2Pix_PAR.html)
      * [Sky2Pix\_Molleweide](astropy.modeling.projections.Sky2Pix_Molleweide.html)
      * [Sky2Pix\_MOL](astropy.modeling.projections.Sky2Pix_MOL.html)
      * [Sky2Pix\_HammerAitoff](astropy.modeling.projections.Sky2Pix_HammerAitoff.html)
      * [Sky2Pix\_AIT](astropy.modeling.projections.Sky2Pix_AIT.html)
      * [Sky2Pix\_ConicPerspective](astropy.modeling.projections.Sky2Pix_ConicPerspective.html)
      * [Sky2Pix\_COP](astropy.modeling.projections.Sky2Pix_COP.html)
      * [Sky2Pix\_ConicEqualArea](astropy.modeling.projections.Sky2Pix_ConicEqualArea.html)
      * [Sky2Pix\_COE](astropy.modeling.projections.Sky2Pix_COE.html)
      * [Sky2Pix\_ConicEquidistant](astropy.modeling.projections.Sky2Pix_ConicEquidistant.html)
      * [Sky2Pix\_COD](astropy.modeling.projections.Sky2Pix_COD.html)
      * [Sky2Pix\_ConicOrthomorphic](astropy.modeling.projections.Sky2Pix_ConicOrthomorphic.html)
      * [Sky2Pix\_COO](astropy.modeling.projections.Sky2Pix_COO.html)
      * [Sky2Pix\_BonneEqualArea](astropy.modeling.projections.Sky2Pix_BonneEqualArea.html)
      * [Sky2Pix\_BON](astropy.modeling.projections.Sky2Pix_BON.html)
      * [Sky2Pix\_Polyconic](astropy.modeling.projections.Sky2Pix_Polyconic.html)
      * [Sky2Pix\_PCO](astropy.modeling.projections.Sky2Pix_PCO.html)
      * [Sky2Pix\_TangentialSphericalCube](astropy.modeling.projections.Sky2Pix_TangentialSphericalCube.html)
      * [Sky2Pix\_TSC](astropy.modeling.projections.Sky2Pix_TSC.html)
      * [Sky2Pix\_COBEQuadSphericalCube](astropy.modeling.projections.Sky2Pix_COBEQuadSphericalCube.html)
      * [Sky2Pix\_CSC](astropy.modeling.projections.Sky2Pix_CSC.html)
      * [Sky2Pix\_QuadSphericalCube](astropy.modeling.projections.Sky2Pix_QuadSphericalCube.html)
      * [Sky2Pix\_QSC](astropy.modeling.projections.Sky2Pix_QSC.html)
      * [Sky2Pix\_HEALPix](astropy.modeling.projections.Sky2Pix_HEALPix.html)
      * [Sky2Pix\_HPX](astropy.modeling.projections.Sky2Pix_HPX.html)
      * [Sky2Pix\_HEALPixPolar](astropy.modeling.projections.Sky2Pix_HEALPixPolar.html)
      * [Sky2Pix\_XPH](astropy.modeling.projections.Sky2Pix_XPH.html)
      * [EulerAngleRotation](astropy.modeling.rotations.EulerAngleRotation.html)
      * [RotateCelestial2Native](astropy.modeling.rotations.RotateCelestial2Native.html)
      * [RotateNative2Celestial](astropy.modeling.rotations.RotateNative2Celestial.html)
      * [Rotation2D](astropy.modeling.rotations.Rotation2D.html)
      * [RotationSequence3D](astropy.modeling.rotations.RotationSequence3D.html)
      * [SphericalRotationSequence](astropy.modeling.rotations.SphericalRotationSequence.html)
      * [Spline1D](astropy.modeling.spline.Spline1D.html)
      * [SplineExactKnotsFitter](astropy.modeling.spline.SplineExactKnotsFitter.html)
      * [SplineInterpolateFitter](astropy.modeling.spline.SplineInterpolateFitter.html)
      * [SplineSmoothingFitter](astropy.modeling.spline.SplineSmoothingFitter.html)
      * [SplineSplrepFitter](astropy.modeling.spline.SplineSplrepFitter.html)
      * [tabular\_model](astropy.modeling.tabular.tabular_model.html)
      * [Tabular1D](astropy.modeling.tabular.Tabular1D.html)
      * [Tabular2D](astropy.modeling.tabular.Tabular2D.html)
  + [Uncertainties and Distributions (`astropy.uncertainty`)](../uncertainty/index.html)
    - [normal](astropy.uncertainty.normal.html)
    - [poisson](astropy.uncertainty.poisson.html)
    - [uniform](astropy.uncertainty.uniform.html)
    - [Distribution](astropy.uncertainty.Distribution.html)
  + [Overview of Astropy File I/O](../io/overview.html)
  + [High-level Unified File I/O](../io/unified.html)
    - [Image Data](../io/unified_image.html)
    - [Table Data](../io/unified_table.html)
      * [Text (CSV, fixed-width, HTML, and specialized)](../io/unified_table_text.html)
      * [FITS](../io/unified_table_fits.html)
      * [HDF5](../io/unified_table_hdf5.html)
      * [Parquet](../io/unified_table_parquet.html)
      * [VO Tables](../io/unified_table_votable.html)
  + [FITS File Handling (`astropy.io.fits`)](../io/fits/index.html)
    - [FITS Headers](../io/fits/usage/headers.html)
    - [Image Data](../io/fits/usage/image.html)
    - [Table Data](../io/fits/usage/table.html)
    - [Verification](../io/fits/usage/verification.html)
    - [Less Familiar Objects](../io/fits/usage/unfamiliar.html)
    - [Executable Scripts](../io/fits/usage/scripts.html)
    - [Miscellaneous Features](../io/fits/usage/misc.html)
    - [Obtaining subsets from cloud-hosted FITS files](../io/fits/usage/cloud.html)
    - [astropy.io.fits FAQ](../io/fits/appendix/faq.html)
    - [Header Interface Transition Guide](../io/fits/appendix/header_transition.html)
    - [astropy.io.fits History](../io/fits/appendix/history.html)
    - [Reference/API](../io/fits/api/index.html)
      * [File Handling and Convenience Functions](../io/fits/api/files.html)
      * [HDU Lists](../io/fits/api/hdulists.html)
      * [Header Data Unit](../io/fits/api/hdus.html)
      * [Headers](../io/fits/api/headers.html)
      * [Cards](../io/fits/api/cards.html)
      * [Tables](../io/fits/api/tables.html)
      * [Images](../io/fits/api/images.html)
      * [Differs](../io/fits/api/diff.html)
      * [Verification Options](../io/fits/api/verification.html)
      * [Tiled Compression](../io/fits/api/tiled_compression.html)
  + [Text Tables (`astropy.io.ascii`)](../io/ascii/index.html)
    - [Reading Tables](../io/ascii/read.html)
    - [Writing Tables](../io/ascii/write.html)
    - [ECSV Format](../io/ascii/ecsv.html)
    - [Fixed-Width Gallery](../io/ascii/fixed_width_gallery.html)
    - [Fast ASCII I/O](../io/ascii/fast_ascii_io.html)
    - [Base Class Elements](../io/ascii/base_classes.html)
    - [Extension Reader Classes](../io/ascii/extension_classes.html)
    - [Reference/API](../io/ascii/ref_api.html)
      * [convert\_numpy](astropy.io.ascii.convert_numpy.html)
      * [get\_read\_trace](astropy.io.ascii.get_read_trace.html)
      * [get\_reader](astropy.io.ascii.get_reader.html)
      * [get\_writer](astropy.io.ascii.get_writer.html)
      * [read](astropy.io.ascii.read.html)
      * [set\_guess](astropy.io.ascii.set_guess.html)
      * [write](astropy.io.ascii.write.html)
      * [AASTex](astropy.io.ascii.AASTex.html)
      * [AllType](astropy.io.ascii.AllType.html)
      * [BaseData](astropy.io.ascii.BaseData.html)
      * [BaseHeader](astropy.io.ascii.BaseHeader.html)
      * [BaseInputter](astropy.io.ascii.BaseInputter.html)
      * [BaseOutputter](astropy.io.ascii.BaseOutputter.html)
      * [BaseReader](astropy.io.ascii.BaseReader.html)
      * [BaseSplitter](astropy.io.ascii.BaseSplitter.html)
      * [Basic](astropy.io.ascii.Basic.html)
      * [BasicData](astropy.io.ascii.BasicData.html)
      * [BasicHeader](astropy.io.ascii.BasicHeader.html)
      * [Cds](astropy.io.ascii.Cds.html)
      * [Column](astropy.io.ascii.Column.html)
      * [CommentedHeader](astropy.io.ascii.CommentedHeader.html)
      * [Conf](astropy.io.ascii.Conf.html)
      * [ContinuationLinesInputter](astropy.io.ascii.ContinuationLinesInputter.html)
      * [Csv](astropy.io.ascii.Csv.html)
      * [Daophot](astropy.io.ascii.Daophot.html)
      * [DefaultSplitter](astropy.io.ascii.DefaultSplitter.html)
      * [Ecsv](astropy.io.ascii.Ecsv.html)
      * [FastBasic](astropy.io.ascii.FastBasic.html)
      * [FastCommentedHeader](astropy.io.ascii.FastCommentedHeader.html)
      * [FastCsv](astropy.io.ascii.FastCsv.html)
      * [FastNoHeader](astropy.io.ascii.FastNoHeader.html)
      * [FastRdb](astropy.io.ascii.FastRdb.html)
      * [FastTab](astropy.io.ascii.FastTab.html)
      * [FixedWidth](astropy.io.ascii.FixedWidth.html)
      * [FixedWidthData](astropy.io.ascii.FixedWidthData.html)
      * [FixedWidthHeader](astropy.io.ascii.FixedWidthHeader.html)
      * [FixedWidthNoHeader](astropy.io.ascii.FixedWidthNoHeader.html)
      * [FixedWidthSplitter](astropy.io.ascii.FixedWidthSplitter.html)
      * [FixedWidthTwoLine](astropy.io.ascii.FixedWidthTwoLine.html)
      * [FloatType](astropy.io.ascii.FloatType.html)
      * [HTML](astropy.io.ascii.HTML.html)
      * [InconsistentTableError](astropy.io.ascii.InconsistentTableError.html)
      * [IntType](astropy.io.ascii.IntType.html)
      * [Ipac](astropy.io.ascii.Ipac.html)
      * [Latex](astropy.io.ascii.Latex.html)
      * [Mesa](astropy.io.ascii.Mesa.html)
      * [Mrt](astropy.io.ascii.Mrt.html)
      * [NoHeader](astropy.io.ascii.NoHeader.html)
      * [NoType](astropy.io.ascii.NoType.html)
      * [NumType](astropy.io.ascii.NumType.html)
      * [ParameterError](astropy.io.ascii.ParameterError.html)
      * [QDP](astropy.io.ascii.QDP.html)
      * [RST](astropy.io.ascii.RST.html)
      * [Rdb](astropy.io.ascii.Rdb.html)
      * [SExtractor](astropy.io.ascii.SExtractor.html)
      * [StrType](astropy.io.ascii.StrType.html)
      * [Tab](astropy.io.ascii.Tab.html)
      * [TableOutputter](astropy.io.ascii.TableOutputter.html)
      * [Tdat](astropy.io.ascii.Tdat.html)
      * [WhitespaceSplitter](astropy.io.ascii.WhitespaceSplitter.html)
  + [VOTable Handling (`astropy.io.votable`)](../io/votable/index.html)
    - [Table element](../io/votable/table_element.html)
    - [COOSYS element](../io/votable/coosys_element.html)
    - [Reading and writing VO model annotations (MIVOT)](../io/votable/mivot_blocks.html)
    - [Reference/API](../io/votable/ref_api.html)
      * [from\_table](astropy.io.votable.from_table.html)
      * [is\_votable](astropy.io.votable.is_votable.html)
      * [parse](astropy.io.votable.parse.html)
      * [parse\_single\_table](astropy.io.votable.parse_single_table.html)
      * [validate](astropy.io.votable.validate.html)
      * [writeto](astropy.io.votable.writeto.html)
      * [Conf](astropy.io.votable.Conf.html)
      * [CooSys](astropy.io.votable.tree.CooSys.html)
      * [Element](astropy.io.votable.tree.Element.html)
      * [Field](astropy.io.votable.tree.Field.html)
      * [FieldRef](astropy.io.votable.tree.FieldRef.html)
      * [Group](astropy.io.votable.tree.Group.html)
      * [Info](astropy.io.votable.tree.Info.html)
      * [Link](astropy.io.votable.tree.Link.html)
      * [MivotBlock](astropy.io.votable.tree.MivotBlock.html)
      * [Param](astropy.io.votable.tree.Param.html)
      * [ParamRef](astropy.io.votable.tree.ParamRef.html)
      * [Resource](astropy.io.votable.tree.Resource.html)
      * [TableElement](astropy.io.votable.tree.TableElement.html)
      * [TimeSys](astropy.io.votable.tree.TimeSys.html)
      * [VOTableFile](astropy.io.votable.tree.VOTableFile.html)
      * [Values](astropy.io.votable.tree.Values.html)
      * [get\_converter](astropy.io.votable.converters.get_converter.html)
      * [table\_column\_to\_votable\_datatype](astropy.io.votable.converters.table_column_to_votable_datatype.html)
      * [Converter](astropy.io.votable.converters.Converter.html)
      * [check\_ucd](astropy.io.votable.ucd.check_ucd.html)
      * [parse\_ucd](astropy.io.votable.ucd.parse_ucd.html)
      * [coerce\_range\_list\_param](astropy.io.votable.util.coerce_range_list_param.html)
      * [convert\_to\_writable\_filelike](astropy.io.votable.util.convert_to_writable_filelike.html)
      * [make\_validation\_report](astropy.io.votable.validator.make_validation_report.html)
      * [check\_anyuri](astropy.io.votable.xmlutil.check_anyuri.html)
      * [check\_id](astropy.io.votable.xmlutil.check_id.html)
      * [check\_mime\_content\_type](astropy.io.votable.xmlutil.check_mime_content_type.html)
      * [check\_token](astropy.io.votable.xmlutil.check_token.html)
      * [fix\_id](astropy.io.votable.xmlutil.fix_id.html)
      * [validate\_schema](astropy.io.votable.xmlutil.validate_schema.html)
      * [add\_data\_origin\_info](astropy.io.votable.dataorigin.add_data_origin_info.html)
      * [extract\_data\_origin](astropy.io.votable.dataorigin.extract_data_origin.html)
      * [DataOrigin](astropy.io.votable.dataorigin.DataOrigin.html)
      * [DatasetOrigin](astropy.io.votable.dataorigin.DatasetOrigin.html)
      * [QueryOrigin](astropy.io.votable.dataorigin.QueryOrigin.html)
    - [`astropy.io.votable.exceptions`](../io/votable/api_exceptions.html)
  + [ECSV, HDF5, Parquet, PyArrow CSV, YAML (`astropy.io.misc`)](../io/misc.html)
    - [Reference/API](../io/misc_ref_api.html)
      * [fnpickle](astropy.io.misc.fnpickle.html)
      * [fnunpickle](astropy.io.misc.fnunpickle.html)
      * [read\_ecsv](astropy.io.misc.ecsv.read_ecsv.html)
      * [register\_ecsv\_table](astropy.io.misc.ecsv.register_ecsv_table.html)
      * [write\_ecsv](astropy.io.misc.ecsv.write_ecsv.html)
      * [ColumnECSV](astropy.io.misc.ecsv.ColumnECSV.html)
      * [ECSVEngine](astropy.io.misc.ecsv.ECSVEngine.html)
      * [ECSVEngineIoAscii](astropy.io.misc.ecsv.ECSVEngineIoAscii.html)
      * [ECSVEnginePandas](astropy.io.misc.ecsv.ECSVEnginePandas.html)
      * [ECSVEnginePyArrow](astropy.io.misc.ecsv.ECSVEnginePyArrow.html)
      * [ECSVHeader](astropy.io.misc.ecsv.ECSVHeader.html)
      * [read\_table\_hdf5](astropy.io.misc.hdf5.read_table_hdf5.html)
      * [write\_table\_hdf5](astropy.io.misc.hdf5.write_table_hdf5.html)
      * [convert\_pa\_table\_to\_astropy\_table](astropy.io.misc.pyarrow.csv.convert_pa_table_to_astropy_table.html)
      * [read\_csv](astropy.io.misc.pyarrow.csv.read_csv.html)
      * [dump](astropy.io.misc.yaml.dump.html)
      * [load](astropy.io.misc.yaml.load.html)
      * [load\_all](astropy.io.misc.yaml.load_all.html)
      * [AstropyDumper](astropy.io.misc.yaml.AstropyDumper.html)
      * [AstropyLoader](astropy.io.misc.yaml.AstropyLoader.html)
  + [Cosmological Calculations (`astropy.cosmology`)](../cosmology/index.html)
    - [Included Cosmology Realizations](../cosmology/realizations.html)
      * [available](astropy.cosmology.realizations.available.html)
      * [WMAP1](astropy.cosmology.realizations.WMAP1.html)
      * [WMAP3](astropy.cosmology.realizations.WMAP3.html)
      * [WMAP5](astropy.cosmology.realizations.WMAP5.html)
      * [WMAP7](astropy.cosmology.realizations.WMAP7.html)
      * [WMAP9](astropy.cosmology.realizations.WMAP9.html)
      * [Planck13](astropy.cosmology.realizations.Planck13.html)
      * [Planck15](astropy.cosmology.realizations.Planck15.html)
      * [Planck18](astropy.cosmology.realizations.Planck18.html)
    - [Units and Equivalencies](../cosmology/units.html)
      * [dimensionless\_redshift](astropy.cosmology.units.dimensionless_redshift.html)
      * [redshift\_distance](astropy.cosmology.units.redshift_distance.html)
      * [redshift\_hubble](astropy.cosmology.units.redshift_hubble.html)
      * [redshift\_temperature](astropy.cosmology.units.redshift_temperature.html)
      * [with\_H0](astropy.cosmology.units.with_H0.html)
      * [with\_redshift](astropy.cosmology.units.with_redshift.html)
    - [Cosmology I/O & Convert](../cosmology/io/index.html)
      * [Cosmology I/O Details](../cosmology/io/details.html)
      * [Built-in Cosmology To/From Formats](../cosmology/io/builtin.html)
      * [Custom Cosmology I/O formats](../cosmology/io/custom.html)
      * [CosmologyFromFormat](astropy.cosmology.io.CosmologyFromFormat.html)
      * [CosmologyRead](astropy.cosmology.io.CosmologyRead.html)
      * [CosmologyToFormat](astropy.cosmology.io.CosmologyToFormat.html)
      * [CosmologyWrite](astropy.cosmology.io.CosmologyWrite.html)
    - [Traits](../cosmology/traits.html)
      * [BaryonComponent](astropy.cosmology.traits.BaryonComponent.html)
      * [CriticalDensity](astropy.cosmology.traits.CriticalDensity.html)
      * [CurvatureComponent](astropy.cosmology.traits.CurvatureComponent.html)
      * [DarkEnergyComponent](astropy.cosmology.traits.DarkEnergyComponent.html)
      * [DarkMatterComponent](astropy.cosmology.traits.DarkMatterComponent.html)
      * [HubbleParameter](astropy.cosmology.traits.HubbleParameter.html)
      * [MatterComponent](astropy.cosmology.traits.MatterComponent.html)
      * [NeutrinoComponent](astropy.cosmology.traits.NeutrinoComponent.html)
      * [PhotonComponent](astropy.cosmology.traits.PhotonComponent.html)
      * [ScaleFactor](astropy.cosmology.traits.ScaleFactor.html)
      * [TemperatureCMB](astropy.cosmology.traits.TemperatureCMB.html)
      * [TotalComponent](astropy.cosmology.traits.TotalComponent.html)
    - [For Developers](../cosmology/dev.html)
    - [Reference/API](../cosmology/ref_api.html)
      * [z\_at\_value](astropy.cosmology.z_at_value.html)
      * [cosmology\_equal](astropy.cosmology.cosmology_equal.html)
      * [Cosmology](astropy.cosmology.Cosmology.html)
      * [CosmologyError](astropy.cosmology.CosmologyError.html)
      * [FlatCosmologyMixin](astropy.cosmology.FlatCosmologyMixin.html)
      * [FLRW](astropy.cosmology.FLRW.html)
      * [FlatFLRWMixin](astropy.cosmology.FlatFLRWMixin.html)
      * [LambdaCDM](astropy.cosmology.LambdaCDM.html)
      * [FlatLambdaCDM](astropy.cosmology.FlatLambdaCDM.html)
      * [wCDM](astropy.cosmology.wCDM.html)
      * [FlatwCDM](astropy.cosmology.FlatwCDM.html)
      * [w0waCDM](astropy.cosmology.w0waCDM.html)
      * [Flatw0waCDM](astropy.cosmology.Flatw0waCDM.html)
      * [w0wzCDM](astropy.cosmology.w0wzCDM.html)
      * [Flatw0wzCDM](astropy.cosmology.Flatw0wzCDM.html)
      * [wpwaCDM](astropy.cosmology.wpwaCDM.html)
      * [FlatwpwaCDM](astropy.cosmology.FlatwpwaCDM.html)
      * [Parameter](astropy.cosmology.Parameter.html)
      * [default\_cosmology](astropy.cosmology.default_cosmology.html)
  + [Convolution and Filtering (`astropy.convolution`)](../convolution/index.html)
    - [Using the Convolution Functions](../convolution/using.html)
    - [Convolution Kernels](../convolution/kernels.html)
    - [Convolving with Unnormalized Kernels](../convolution/non_normalized_kernels.html)
    - [Reference/API](../convolution/ref_api.html)
      * [convolve](astropy.convolution.convolve.html)
      * [convolve\_fft](astropy.convolution.convolve_fft.html)
      * [convolve\_models](astropy.convolution.convolve_models.html)
      * [convolve\_models\_fft](astropy.convolution.convolve_models_fft.html)
      * [discretize\_model](astropy.convolution.discretize_model.html)
      * [interpolate\_replace\_nans](astropy.convolution.interpolate_replace_nans.html)
      * [kernel\_arithmetics](astropy.convolution.kernel_arithmetics.html)
      * [AiryDisk2DKernel](astropy.convolution.AiryDisk2DKernel.html)
      * [Box1DKernel](astropy.convolution.Box1DKernel.html)
      * [Box2DKernel](astropy.convolution.Box2DKernel.html)
      * [CustomKernel](astropy.convolution.CustomKernel.html)
      * [Gaussian1DKernel](astropy.convolution.Gaussian1DKernel.html)
      * [Gaussian2DKernel](astropy.convolution.Gaussian2DKernel.html)
      * [Kernel](astropy.convolution.Kernel.html)
      * [Kernel1D](astropy.convolution.Kernel1D.html)
      * [Kernel2D](astropy.convolution.Kernel2D.html)
      * [KernelArithmeticError](astropy.convolution.KernelArithmeticError.html)
      * [KernelError](astropy.convolution.KernelError.html)
      * [KernelSizeError](astropy.convolution.KernelSizeError.html)
      * [Model1DKernel](astropy.convolution.Model1DKernel.html)
      * [Model2DKernel](astropy.convolution.Model2DKernel.html)
      * [Moffat2DKernel](astropy.convolution.Moffat2DKernel.html)
      * [RickerWavelet1DKernel](astropy.convolution.RickerWavelet1DKernel.html)
      * [RickerWavelet2DKernel](astropy.convolution.RickerWavelet2DKernel.html)
      * [Ring2DKernel](astropy.convolution.Ring2DKernel.html)
      * [Tophat2DKernel](astropy.convolution.Tophat2DKernel.html)
      * [Trapezoid1DKernel](astropy.convolution.Trapezoid1DKernel.html)
      * [TrapezoidDisk2DKernel](astropy.convolution.TrapezoidDisk2DKernel.html)
  + [IERS data access (`astropy.utils.iers`)](../utils/iers.html)
  + [Data Visualization (`astropy.visualization`)](../visualization/index.html)
    - [Plotting Astropy objects in Matplotlib](../visualization/matplotlib_integration.html)
    - [Making plots with world coordinates (WCSAxes)](../visualization/wcsaxes/index.html)
      * [Initializing axes with world coordinates](../visualization/wcsaxes/initializing_axes.html)
      * [Plotting images and contours](../visualization/wcsaxes/images_contours.html)
      * [Ticks, tick labels, and grid lines](../visualization/wcsaxes/ticks_labels_grid.html)
      * [Overplotting markers and artists](../visualization/wcsaxes/overlays.html)
      * [Overlaying coordinate systems](../visualization/wcsaxes/overlaying_coordinate_systems.html)
      * [Slicing Multidimensional Data](../visualization/wcsaxes/slicing_datacubes.html)
      * [Controlling Axes](../visualization/wcsaxes/controlling_axes.html)
      * [Initializing WCSAxes with custom transforms](../visualization/wcsaxes/generic_transforms.html)
      * [Using a custom frame](../visualization/wcsaxes/custom_frames.html)
      * [add\_beam](astropy.visualization.wcsaxes.add_beam.html)
      * [add\_scalebar](astropy.visualization.wcsaxes.add_scalebar.html)
      * [custom\_ucd\_coord\_meta\_mapping](astropy.visualization.wcsaxes.custom_ucd_coord_meta_mapping.html)
      * [Conf](astropy.visualization.wcsaxes.Conf.html)
      * [CoordinateHelper](astropy.visualization.wcsaxes.CoordinateHelper.html)
      * [CoordinatesMap](astropy.visualization.wcsaxes.CoordinatesMap.html)
      * [Quadrangle](astropy.visualization.wcsaxes.Quadrangle.html)
      * [SphericalCircle](astropy.visualization.wcsaxes.SphericalCircle.html)
      * [WCSAxes](astropy.visualization.wcsaxes.WCSAxes.html)
      * [WCSAxesSubplot](astropy.visualization.wcsaxes.WCSAxesSubplot.html)
      * [BaseFrame](astropy.visualization.wcsaxes.frame.BaseFrame.html)
      * [EllipticalFrame](astropy.visualization.wcsaxes.frame.EllipticalFrame.html)
      * [RectangularFrame](astropy.visualization.wcsaxes.frame.RectangularFrame.html)
      * [RectangularFrame1D](astropy.visualization.wcsaxes.frame.RectangularFrame1D.html)
      * [Spine](astropy.visualization.wcsaxes.frame.Spine.html)
    - [Image stretching and normalization](../visualization/normalization.html)
    - [Choosing Histogram Bins](../visualization/histogram.html)
    - [Creating color RGB images](../visualization/rgb.html)
    - [Reference/API](../visualization/ref_api.html)
      * [hist](astropy.visualization.hist.html)
      * [imshow\_norm](astropy.visualization.imshow_norm.html)
      * [imshow\_simple\_norm](astropy.visualization.imshow_simple_norm.html)
      * [make\_lupton\_rgb](astropy.visualization.make_lupton_rgb.html)
      * [make\_rgb](astropy.visualization.make_rgb.html)
      * [quantity\_support](astropy.visualization.quantity_support.html)
      * [simple\_norm](astropy.visualization.simple_norm.html)
      * [time\_support](astropy.visualization.time_support.html)
      * [AsinhStretch](astropy.visualization.AsinhStretch.html)
      * [AsymmetricPercentileInterval](astropy.visualization.AsymmetricPercentileInterval.html)
      * [BaseInterval](astropy.visualization.BaseInterval.html)
      * [BaseStretch](astropy.visualization.BaseStretch.html)
      * [BaseTransform](astropy.visualization.BaseTransform.html)
      * [CompositeStretch](astropy.visualization.CompositeStretch.html)
      * [CompositeTransform](astropy.visualization.CompositeTransform.html)
      * [ContrastBiasStretch](astropy.visualization.ContrastBiasStretch.html)
      * [HistEqStretch](astropy.visualization.HistEqStretch.html)
      * [ImageNormalize](astropy.visualization.ImageNormalize.html)
      * [LinearStretch](astropy.visualization.LinearStretch.html)
      * [LogStretch](astropy.visualization.LogStretch.html)
      * [LuptonAsinhStretch](astropy.visualization.LuptonAsinhStretch.html)
      * [LuptonAsinhZscaleStretch](astropy.visualization.LuptonAsinhZscaleStretch.html)
      * [ManualInterval](astropy.visualization.ManualInterval.html)
      * [MinMaxInterval](astropy.visualization.MinMaxInterval.html)
      * [MplQuantityConverter](astropy.visualization.MplQuantityConverter.html)
      * [PercentileInterval](astropy.visualization.PercentileInterval.html)
      * [PowerDistStretch](astropy.visualization.PowerDistStretch.html)
      * [PowerStretch](astropy.visualization.PowerStretch.html)
      * [SimpleNorm](astropy.visualization.SimpleNorm.html)
      * [SinhStretch](astropy.visualization.SinhStretch.html)
      * [SqrtStretch](astropy.visualization.SqrtStretch.html)
      * [SquaredStretch](astropy.visualization.SquaredStretch.html)
      * [SymmetricInterval](astropy.visualization.SymmetricInterval.html)
      * [ZScaleInterval](astropy.visualization.ZScaleInterval.html)
      * [imshow\_norm](astropy.visualization.mpl_normalize.imshow_norm.html)
      * [imshow\_simple\_norm](astropy.visualization.mpl_normalize.imshow_simple_norm.html)
      * [simple\_norm](astropy.visualization.mpl_normalize.simple_norm.html)
      * [ImageNormalize](astropy.visualization.mpl_normalize.ImageNormalize.html)
      * [SimpleNorm](astropy.visualization.mpl_normalize.SimpleNorm.html)
  + [Astrostatistics Tools (`astropy.stats`)](../stats/index.html)
    - [Robust Statistical Estimators](../stats/robust.html)
      * [sigma\_clip](astropy.stats.sigma_clipping.sigma_clip.html)
      * [sigma\_clipped\_stats](astropy.stats.sigma_clipping.sigma_clipped_stats.html)
      * [SigmaClip](astropy.stats.sigma_clipping.SigmaClip.html)
      * [SigmaClippedStats](astropy.stats.sigma_clipping.SigmaClippedStats.html)
      * [biweight\_location](astropy.stats.biweight.biweight_location.html)
      * [biweight\_midcorrelation](astropy.stats.biweight.biweight_midcorrelation.html)
      * [biweight\_midcovariance](astropy.stats.biweight.biweight_midcovariance.html)
      * [biweight\_midvariance](astropy.stats.biweight.biweight_midvariance.html)
      * [biweight\_scale](astropy.stats.biweight.biweight_scale.html)
    - [Circular Statistics](../stats/circ.html)
      * [circcorrcoef](astropy.stats.circstats.circcorrcoef.html)
      * [circmean](astropy.stats.circstats.circmean.html)
      * [circmoment](astropy.stats.circstats.circmoment.html)
      * [circstd](astropy.stats.circstats.circstd.html)
      * [circvar](astropy.stats.circstats.circvar.html)
      * [rayleightest](astropy.stats.circstats.rayleightest.html)
      * [vonmisesmle](astropy.stats.circstats.vonmisesmle.html)
      * [vtest](astropy.stats.circstats.vtest.html)
    - [Ripley’s K Function Estimators](../stats/ripley.html)
    - [Reference/API](../stats/ref_api.html)
      * [binned\_binom\_proportion](astropy.stats.binned_binom_proportion.html)
      * [binom\_conf\_interval](astropy.stats.binom_conf_interval.html)
      * [bootstrap](astropy.stats.bootstrap.html)
      * [cdf\_from\_intervals](astropy.stats.cdf_from_intervals.html)
      * [fold\_intervals](astropy.stats.fold_intervals.html)
      * [histogram\_intervals](astropy.stats.histogram_intervals.html)
      * [interval\_overlap\_length](astropy.stats.interval_overlap_length.html)
      * [kuiper](astropy.stats.kuiper.html)
      * [kuiper\_false\_positive\_probability](astropy.stats.kuiper_false_positive_probability.html)
      * [kuiper\_two](astropy.stats.kuiper_two.html)
      * [mad\_std](astropy.stats.mad_std.html)
      * [median\_absolute\_deviation](astropy.stats.median_absolute_deviation.html)
      * [poisson\_conf\_interval](astropy.stats.poisson_conf_interval.html)
      * [signal\_to\_noise\_oir\_ccd](astropy.stats.signal_to_noise_oir_ccd.html)
      * [biweight\_location](astropy.stats.biweight_location.html)
      * [biweight\_midcorrelation](astropy.stats.biweight_midcorrelation.html)
      * [biweight\_midcovariance](astropy.stats.biweight_midcovariance.html)
      * [biweight\_midvariance](astropy.stats.biweight_midvariance.html)
      * [biweight\_scale](astropy.stats.biweight_scale.html)
      * [sigma\_clip](astropy.stats.sigma_clip.html)
      * [sigma\_clipped\_stats](astropy.stats.sigma_clipped_stats.html)
      * [jackknife\_resampling](astropy.stats.jackknife_resampling.html)
      * [jackknife\_stats](astropy.stats.jackknife_stats.html)
      * [circcorrcoef](astropy.stats.circcorrcoef.html)
      * [circmean](astropy.stats.circmean.html)
      * [circmoment](astropy.stats.circmoment.html)
      * [circstd](astropy.stats.circstd.html)
      * [circvar](astropy.stats.circvar.html)
      * [rayleightest](astropy.stats.rayleightest.html)
      * [vonmisesmle](astropy.stats.vonmisesmle.html)
      * [vtest](astropy.stats.vtest.html)
      * [bayesian\_blocks](astropy.stats.bayesian_blocks.html)
      * [calculate\_bin\_edges](astropy.stats.calculate_bin_edges.html)
      * [freedman\_bin\_width](astropy.stats.freedman_bin_width.html)
      * [histogram](astropy.stats.histogram.html)
      * [knuth\_bin\_width](astropy.stats.knuth_bin_width.html)
      * [scott\_bin\_width](astropy.stats.scott_bin_width.html)
      * [akaike\_info\_criterion](astropy.stats.akaike_info_criterion.html)
      * [akaike\_info\_criterion\_lsq](astropy.stats.akaike_info_criterion_lsq.html)
      * [bayesian\_info\_criterion](astropy.stats.bayesian_info_criterion.html)
      * [bayesian\_info\_criterion\_lsq](astropy.stats.bayesian_info_criterion_lsq.html)
      * [SigmaClip](astropy.stats.SigmaClip.html)
      * [SigmaClippedStats](astropy.stats.SigmaClippedStats.html)
      * [Events](astropy.stats.Events.html)
      * [FitnessFunc](astropy.stats.FitnessFunc.html)
      * [PointMeasures](astropy.stats.PointMeasures.html)
      * [RegularEvents](astropy.stats.RegularEvents.html)
      * [RipleysKEstimator](astropy.stats.RipleysKEstimator.html)
  + [Masked Values and Quantities (`astropy.utils.masked`)](../utils/masked/index.html)
    - [combine\_masks](astropy.utils.masked.combine_masks.html)
    - [get\_data\_and\_mask](astropy.utils.masked.get_data_and_mask.html)
    - [MaskableShapedLikeNDArray](astropy.utils.masked.MaskableShapedLikeNDArray.html)
    - [Masked](astropy.utils.masked.Masked.html)
    - [MaskedNDArray](astropy.utils.masked.MaskedNDArray.html)
    - [bincount](astropy.utils.masked.function_helpers.bincount.html)
    - [broadcast\_arrays](astropy.utils.masked.function_helpers.broadcast_arrays.html)
    - [broadcast\_to](astropy.utils.masked.function_helpers.broadcast_to.html)
    - [choose](astropy.utils.masked.function_helpers.choose.html)
    - [copyto](astropy.utils.masked.function_helpers.copyto.html)
    - [count\_nonzero](astropy.utils.masked.function_helpers.count_nonzero.html)
    - [full\_like](astropy.utils.masked.function_helpers.full_like.html)
    - [insert](astropy.utils.masked.function_helpers.insert.html)
    - [interp](astropy.utils.masked.function_helpers.interp.html)
    - [lexsort](astropy.utils.masked.function_helpers.lexsort.html)
    - [nanargmax](astropy.utils.masked.function_helpers.nanargmax.html)
    - [nanargmin](astropy.utils.masked.function_helpers.nanargmin.html)
    - [nancumprod](astropy.utils.masked.function_helpers.nancumprod.html)
    - [nancumsum](astropy.utils.masked.function_helpers.nancumsum.html)
    - [nanmax](astropy.utils.masked.function_helpers.nanmax.html)
    - [nanmean](astropy.utils.masked.function_helpers.nanmean.html)
    - [nanmedian](astropy.utils.masked.function_helpers.nanmedian.html)
    - [nanmin](astropy.utils.masked.function_helpers.nanmin.html)
    - [nanpercentile](astropy.utils.masked.function_helpers.nanpercentile.html)
    - [nanprod](astropy.utils.masked.function_helpers.nanprod.html)
    - [nanquantile](astropy.utils.masked.function_helpers.nanquantile.html)
    - [nanstd](astropy.utils.masked.function_helpers.nanstd.html)
    - [nansum](astropy.utils.masked.function_helpers.nansum.html)
    - [nanvar](astropy.utils.masked.function_helpers.nanvar.html)
    - [ones\_like](astropy.utils.masked.function_helpers.ones_like.html)
    - [piecewise](astropy.utils.masked.function_helpers.piecewise.html)
    - [place](astropy.utils.masked.function_helpers.place.html)
    - [put](astropy.utils.masked.function_helpers.put.html)
    - [select](astropy.utils.masked.function_helpers.select.html)
    - [zeros\_like](astropy.utils.masked.function_helpers.zeros_like.html)
  + [SAMP (Simple Application Messaging Protocol) (`astropy.samp`)](../samp/index.html)
    - [Starting and Stopping a SAMP Hub Server](../samp/example_hub.html)
    - [Sending and Receiving Tables and Images over SAMP](../samp/example_table_image.html)
    - [Communication between Integrated Clients Objects](../samp/example_clients.html)
    - [Embedding a SAMP Hub in a GUI](../samp/advanced_embed_samp_hub.html)
    - [Reference/API](../samp/ref_api.html)
      * [safe\_xmlrpc\_loads](astropy.samp.safe_xmlrpc_loads.html)
      * [Conf](astropy.samp.Conf.html)
      * [SAMPClient](astropy.samp.SAMPClient.html)
      * [SAMPClientError](astropy.samp.SAMPClientError.html)
      * [SAMPHubError](astropy.samp.SAMPHubError.html)
      * [SAMPHubProxy](astropy.samp.SAMPHubProxy.html)
      * [SAMPHubServer](astropy.samp.SAMPHubServer.html)
      * [SAMPIntegratedClient](astropy.samp.SAMPIntegratedClient.html)
      * [SAMPMsgReplierWrapper](astropy.samp.SAMPMsgReplierWrapper.html)
      * [SAMPProxyError](astropy.samp.SAMPProxyError.html)
      * [SAMPWarning](astropy.samp.SAMPWarning.html)
      * [SAMPXXEServerProxy](astropy.samp.SAMPXXEServerProxy.html)
      * [WebProfileDialog](astropy.samp.WebProfileDialog.html)
  + [Configuration System (`astropy.config`)](../config/index.html)
    - [Astropy’s Default Configuration File](../config/astropy_config.html)
    - [Reference/API](../config/ref_api.html)
      * [create\_config\_file](astropy.config.create_config_file.html)
      * [generate\_config](astropy.config.generate_config.html)
      * [get\_cache\_dir](astropy.config.get_cache_dir.html)
      * [get\_cache\_dir\_path](astropy.config.get_cache_dir_path.html)
      * [get\_config](astropy.config.get_config.html)
      * [get\_config\_dir](astropy.config.get_config_dir.html)
      * [get\_config\_dir\_path](astropy.config.get_config_dir_path.html)
      * [reload\_config](astropy.config.reload_config.html)
      * [temporary\_cache\_dir\_path](astropy.config.temporary_cache_dir_path.html)
      * [temporary\_config\_dir\_path](astropy.config.temporary_config_dir_path.html)
      * [ConfigItem](astropy.config.ConfigItem.html)
      * [ConfigNamespace](astropy.config.ConfigNamespace.html)
      * [InvalidConfigurationItemWarning](astropy.config.InvalidConfigurationItemWarning.html)
      * [set\_temp\_cache](astropy.config.set_temp_cache.html)
      * [set\_temp\_config](astropy.config.set_temp_config.html)
  + [I/O Registry (`astropy.io.registry`)](../io/registry.html)
    - [Reference/API](../io/registry_ref_api.html)
      * [delay\_doc\_updates](astropy.io.registry.delay_doc_updates.html)
      * [get\_formats](astropy.io.registry.get_formats.html)
      * [get\_reader](astropy.io.registry.get_reader.html)
      * [get\_writer](astropy.io.registry.get_writer.html)
      * [identify\_format](astropy.io.registry.identify_format.html)
      * [read](astropy.io.registry.read.html)
      * [register\_identifier](astropy.io.registry.register_identifier.html)
      * [register\_reader](astropy.io.registry.register_reader.html)
      * [register\_writer](astropy.io.registry.register_writer.html)
      * [unregister\_identifier](astropy.io.registry.unregister_identifier.html)
      * [unregister\_reader](astropy.io.registry.unregister_reader.html)
      * [unregister\_writer](astropy.io.registry.unregister_writer.html)
      * [write](astropy.io.registry.write.html)
      * [UnifiedIORegistry](astropy.io.registry.UnifiedIORegistry.html)
      * [UnifiedInputRegistry](astropy.io.registry.UnifiedInputRegistry.html)
      * [UnifiedOutputRegistry](astropy.io.registry.UnifiedOutputRegistry.html)
      * [UnifiedReadWrite](astropy.io.registry.UnifiedReadWrite.html)
      * [UnifiedReadWriteMethod](astropy.io.registry.UnifiedReadWriteMethod.html)
      * [IORegistryError](astropy.io.registry.IORegistryError.html)
  + [I/O Typing (`astropy.io.typing`)](../io/typing.html)
    - [ReadableFileLike](astropy.io.typing.ReadableFileLike.html)
    - [WriteableFileLike](astropy.io.typing.WriteableFileLike.html)
  + [Logging system](../logging.html)
    - [AstropyLogger](astropy.logger.AstropyLogger.html)
    - [Conf](astropy.logger.Conf.html)
    - [LoggingError](astropy.logger.LoggingError.html)
  + [Python warnings system](../warnings.html)
  + [Astropy Core Package Utilities (`astropy.utils`)](../utils/index.html)
    - [Downloadable Data Management (`astropy.utils.data`)](../utils/data.html)
    - [Reference/API](../utils/ref_api.html)
      * [make\_function\_with\_signature](astropy.utils.codegen.make_function_with_signature.html)
      * [HomogeneousList](astropy.utils.collections.HomogeneousList.html)
      * [color\_print](astropy.utils.console.color_print.html)
      * [human\_file\_size](astropy.utils.console.human_file_size.html)
      * [human\_time](astropy.utils.console.human_time.html)
      * [isatty](astropy.utils.console.isatty.html)
      * [print\_code\_line](astropy.utils.console.print_code_line.html)
      * [terminal\_size](astropy.utils.console.terminal_size.html)
      * [ProgressBar](astropy.utils.console.ProgressBar.html)
      * [ProgressBarOrSpinner](astropy.utils.console.ProgressBarOrSpinner.html)
      * [Spinner](astropy.utils.console.Spinner.html)
      * [data\_info\_factory](astropy.utils.data_info.data_info_factory.html)
      * [dtype\_info\_name](astropy.utils.data_info.dtype_info_name.html)
      * [BaseColumnInfo](astropy.utils.data_info.BaseColumnInfo.html)
      * [DataInfo](astropy.utils.data_info.DataInfo.html)
      * [MixinInfo](astropy.utils.data_info.MixinInfo.html)
      * [ParentDtypeInfo](astropy.utils.data_info.ParentDtypeInfo.html)
      * [deprecated](astropy.utils.decorators.deprecated.html)
      * [deprecated\_attribute](astropy.utils.decorators.deprecated_attribute.html)
      * [deprecated\_renamed\_argument](astropy.utils.decorators.deprecated_renamed_argument.html)
      * [format\_doc](astropy.utils.decorators.format_doc.html)
      * [classproperty](astropy.utils.decorators.classproperty.html)
      * [lazyproperty](astropy.utils.decorators.lazyproperty.html)
      * [sharedmethod](astropy.utils.decorators.sharedmethod.html)
      * [diff\_values](astropy.utils.diff.diff_values.html)
      * [report\_diff\_values](astropy.utils.diff.report_diff_values.html)
      * [where\_not\_allclose](astropy.utils.diff.where_not_allclose.html)
      * [AstropyBackwardsIncompatibleChangeWarning](astropy.utils.exceptions.AstropyBackwardsIncompatibleChangeWarning.html)
      * [AstropyDeprecationWarning](astropy.utils.exceptions.AstropyDeprecationWarning.html)
      * [AstropyPendingDeprecationWarning](astropy.utils.exceptions.AstropyPendingDeprecationWarning.html)
      * [AstropyUserWarning](astropy.utils.exceptions.AstropyUserWarning.html)
      * [AstropyWarning](astropy.utils.exceptions.AstropyWarning.html)
      * [DuplicateRepresentationWarning](astropy.utils.exceptions.DuplicateRepresentationWarning.html)
      * [Conf](astropy.utils.iers.Conf.html)
      * [IERS](astropy.utils.iers.IERS.html)
      * [IERSDegradedAccuracyWarning](astropy.utils.iers.IERSDegradedAccuracyWarning.html)
      * [IERSRangeError](astropy.utils.iers.IERSRangeError.html)
      * [IERSStaleWarning](astropy.utils.iers.IERSStaleWarning.html)
      * [IERSWarning](astropy.utils.iers.IERSWarning.html)
      * [IERS\_A](astropy.utils.iers.IERS_A.html)
      * [IERS\_Auto](astropy.utils.iers.IERS_Auto.html)
      * [IERS\_B](astropy.utils.iers.IERS_B.html)
      * [LeapSeconds](astropy.utils.iers.LeapSeconds.html)
      * [earth\_orientation\_table](astropy.utils.iers.earth_orientation_table.html)
      * [find\_current\_module](astropy.utils.introspection.find_current_module.html)
      * [isinstancemethod](astropy.utils.introspection.isinstancemethod.html)
      * [minversion](astropy.utils.introspection.minversion.html)
      * [resolve\_name](astropy.utils.introspection.resolve_name.html)
      * [enable\_merge\_strategies](astropy.utils.metadata.enable_merge_strategies.html)
      * [merge](astropy.utils.metadata.merge.html)
      * [common\_dtype](astropy.utils.metadata.common_dtype.html)
      * [MetaAttribute](astropy.utils.metadata.MetaAttribute.html)
      * [MetaData](astropy.utils.metadata.MetaData.html)
      * [MergeNpConcatenate](astropy.utils.metadata.MergeNpConcatenate.html)
      * [MergePlus](astropy.utils.metadata.MergePlus.html)
      * [MergeStrategy](astropy.utils.metadata.MergeStrategy.html)
      * [MergeConflictError](astropy.utils.metadata.MergeConflictError.html)
      * [MergeConflictWarning](astropy.utils.metadata.MergeConflictWarning.html)
      * [dtype\_bytes\_or\_chars](astropy.utils.misc.dtype_bytes_or_chars.html)
      * [find\_api\_page](astropy.utils.misc.find_api_page.html)
      * [format\_exception](astropy.utils.misc.format_exception.html)
      * [indent](astropy.utils.misc.indent.html)
      * [isiterable](astropy.utils.misc.isiterable.html)
      * [online\_help](astropy.utils.misc.online_help.html)
      * [silence](astropy.utils.misc.silence.html)
      * [JsonCustomEncoder](astropy.utils.misc.JsonCustomEncoder.html)
      * [NumpyRNGContext](astropy.utils.misc.NumpyRNGContext.html)
      * [lex](astropy.utils.parsing.lex.html)
      * [yacc](astropy.utils.parsing.yacc.html)
      * [ThreadSafeParser](astropy.utils.parsing.ThreadSafeParser.html)
      * [ScienceState](astropy.utils.state.ScienceState.html)
      * [check\_broadcast](astropy.utils.shapes.check_broadcast.html)
      * [simplify\_basic\_index](astropy.utils.shapes.simplify_basic_index.html)
      * [unbroadcast](astropy.utils.shapes.unbroadcast.html)
      * [IncompatibleShapeError](astropy.utils.shapes.IncompatibleShapeError.html)
      * [NDArrayShapeMethods](astropy.utils.shapes.NDArrayShapeMethods.html)
      * [ShapedLikeNDArray](astropy.utils.shapes.ShapedLikeNDArray.html)
      * [system\_info](astropy.utils.system_info.system_info.html)
      * [cache\_contents](astropy.utils.data.cache_contents.html)
      * [cache\_total\_size](astropy.utils.data.cache_total_size.html)
      * [check\_download\_cache](astropy.utils.data.check_download_cache.html)
      * [check\_free\_space\_in\_dir](astropy.utils.data.check_free_space_in_dir.html)
      * [clear\_download\_cache](astropy.utils.data.clear_download_cache.html)
      * [compute\_hash](astropy.utils.data.compute_hash.html)
      * [download\_file](astropy.utils.data.download_file.html)
      * [download\_files\_in\_parallel](astropy.utils.data.download_files_in_parallel.html)
      * [export\_download\_cache](astropy.utils.data.export_download_cache.html)
      * [get\_cached\_urls](astropy.utils.data.get_cached_urls.html)
      * [get\_file\_contents](astropy.utils.data.get_file_contents.html)
      * [get\_free\_space\_in\_dir](astropy.utils.data.get_free_space_in_dir.html)
      * [get\_pkg\_data\_contents](astropy.utils.data.get_pkg_data_contents.html)
      * [get\_pkg\_data\_filename](astropy.utils.data.get_pkg_data_filename.html)
      * [get\_pkg\_data\_filenames](astropy.utils.data.get_pkg_data_filenames.html)
      * [get\_pkg\_data\_fileobj](astropy.utils.data.get_pkg_data_fileobj.html)
      * [get\_pkg\_data\_fileobjs](astropy.utils.data.get_pkg_data_fileobjs.html)
      * [get\_pkg\_data\_path](astropy.utils.data.get_pkg_data_path.html)
      * [get\_readable\_fileobj](astropy.utils.data.get_readable_fileobj.html)
      * [import\_download\_cache](astropy.utils.data.import_download_cache.html)
      * [import\_file\_to\_cache](astropy.utils.data.import_file_to_cache.html)
      * [is\_url](astropy.utils.data.is_url.html)
      * [is\_url\_in\_cache](astropy.utils.data.is_url_in_cache.html)
      * [CacheDamaged](astropy.utils.data.CacheDamaged.html)
      * [CacheMissingWarning](astropy.utils.data.CacheMissingWarning.html)
      * [Conf](astropy.utils.data.Conf.html)
      * [check\_anyuri](astropy.utils.xml.check.check_anyuri.html)
      * [check\_id](astropy.utils.xml.check.check_id.html)
      * [check\_mime\_content\_type](astropy.utils.xml.check.check_mime_content_type.html)
      * [check\_token](astropy.utils.xml.check.check_token.html)
      * [fix\_id](astropy.utils.xml.check.fix_id.html)
      * [get\_xml\_encoding](astropy.utils.xml.iterparser.get_xml_encoding.html)
      * [get\_xml\_iterator](astropy.utils.xml.iterparser.get_xml_iterator.html)
      * [xml\_readlines](astropy.utils.xml.iterparser.xml_readlines.html)
      * [unescape\_all](astropy.utils.xml.unescaper.unescape_all.html)
      * [validate\_schema](astropy.utils.xml.validate.validate_schema.html)
      * [XMLWriter](astropy.utils.xml.writer.XMLWriter.html)
  + [Environment variables](../environment_variables.html)
  + [Astropy Glossary](../glossary.html)
* [Contributing](../index_dev.html)
* [Project Details](../index_project_details.html)
  + [What’s New](../whatsnew/index.html)
    - [What’s New in Astropy 8.0?](../whatsnew/8.0.html)
  + [Full Changelog](../changelog.html)
  + [LTS Backport Policy](../lts_policy.html)
  + [Known Issues](../known_issues.html)
  + [Authors and Credits](../credits.html)
  + [Impact and Health](../impact_health.html)
  + [Licenses](../license.html)

* [User Guide](../index_user_docs.html)
* [World Coordinate System (`astropy.wcs`)](../wcs/index.html)
* [Reference/API](../wcs/reference_api.html)
* fit\_wcs\_from\_points

fit\_wcs\_from\_points[#](#fit-wcs-from-points "Link to this heading")
======================================================================

astropy.wcs.utils.fit\_wcs\_from\_points(*xy*, *world\_coords*, *proj\_point='center'*, *projection='TAN'*, *sip\_degree=None*)[[source]](../_modules/astropy/wcs/utils.html#fit_wcs_from_points)[#](#astropy.wcs.utils.fit_wcs_from_points "Link to this definition")
:   Given two matching sets of coordinates on detector and sky,
    compute the WCS.

    Fits a WCS object to matched set of input detector and sky coordinates.
    Optionally, a SIP can be fit to account for geometric
    distortion. Returns an [`WCS`](astropy.wcs.WCS.html#astropy.wcs.WCS "astropy.wcs.WCS") object with the best fit
    parameters for mapping between input pixel and sky coordinates.

    The projection type (default ‘TAN’) can passed in as a string, one of
    the valid three-letter projection codes - or as a WCS object with
    projection keywords already set. Note that if an input WCS has any
    non-polynomial distortion, this will be applied and reflected in the
    fit terms and coefficients. Passing in a WCS object in this way essentially
    allows it to be refit based on the matched input coordinates and projection
    point, but take care when using this option as non-projection related
    keywords in the input might cause unexpected behavior.

    Parameters:
    :   **xy**([`numpy.ndarray`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray "(in NumPy v2.5)"), [`numpy.ndarray`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray "(in NumPy v2.5)")) [`tuple`](https://docs.python.org/3/builtins/stdtypes.html#tuple "(in Python v3.15)")
        :   x & y pixel coordinates. These should be in FITS convention, starting
            from (1,1) as the center of the bottom-left pixel.

        **world\_coords**[`SkyCoord`](astropy.coordinates.SkyCoord.html#astropy.coordinates.SkyCoord "astropy.coordinates.SkyCoord")
        :   Skycoord object with world coordinates.

        **proj\_point**‘center’ or ~astropy.coordinates.SkyCoord`
        :   Defaults to ‘center’, in which the geometric center of input world
            coordinates will be used as the projection point. To specify an exact
            point for the projection, a Skycoord object with a coordinate pair can
            be passed in. For consistency, the units and frame of these coordinates
            will be transformed to match `world_coords` if they don’t.

        **projection**[`str`](https://docs.python.org/3/builtins/stdtypes.html#str "(in Python v3.15)") or [`WCS`](astropy.wcs.WCS.html#astropy.wcs.WCS "astropy.wcs.WCS")
        :   Three letter projection code, of any of standard projections defined
            in the FITS WCS standard. Optionally, a WCS object with projection
            keywords set may be passed in.

        **sip\_degree**[`None`](https://docs.python.org/3/builtins/constants.html#None "(in Python v3.15)") or [`int`](https://docs.python.org/3/builtins/functions.html#int "(in Python v3.15)")
        :   If set to a non-zero integer value, will fit SIP of degree
            `sip_degree` to model geometric distortion. Defaults to None, meaning
            no distortion corrections will be fit.

    Returns:
    :   **wcs**[`WCS`](astropy.wcs.WCS.html#astropy.wcs.WCS "astropy.wcs.WCS")
        :   The best-fit WCS to the points given.

    Notes

    * The fiducial point for the spherical projection can be set to ‘center’
      to use the mean position of input sky coordinates, or as an
      [`SkyCoord`](astropy.coordinates.SkyCoord.html#astropy.coordinates.SkyCoord "astropy.coordinates.SkyCoord") object.
    * Units in all output WCS objects will always be in degrees.
    * If the coordinate frame differs between [`SkyCoord`](astropy.coordinates.SkyCoord.html#astropy.coordinates.SkyCoord "astropy.coordinates.SkyCoord")
      objects passed in for `world_coords` and `proj_point`, the frame for
      `world_coords` will override as the frame for the output WCS.
    * If a WCS object is passed in to `projection` the CD/PC matrix will
      be used as an initial guess for the fit. If this is known to be
      significantly off and may throw off the fit, set to the identity matrix
      (for example, by doing wcs.wcs.pc = [(1., 0.,), (0., 1.)])

[previous

celestial\_frame\_to\_wcs](astropy.wcs.utils.celestial_frame_to_wcs.html "previous page")
[next

is\_proj\_plane\_distorted](astropy.wcs.utils.is_proj_plane_distorted.html "next page")

[Edit](https://github.com/astropy/astropy/edit/main/astropy/wcs/utils.py#L1063)

© Copyright 2011–2026, The Astropy Developers.

[Code of Conduct](https://astropy.org/code_of_conduct.html)

Updated on 15 Oct 2026
, built with [Sphinx
8.2.3](http://sphinx-doc.org/)

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
- https://docs.astropy.org/en/stable/_modules/astropy/wcs/utils.html#fit_wcs_from_points
- https://docs.astropy.org/en/stable/api/astropy.config.ConfigItem.html
- https://docs.astropy.org/en/stable/api/astropy.config.ConfigNamespace.html
- https://docs.astropy.org/en/stable/api/astropy.config.InvalidConfigurationItemWarning.html
- https://docs.astropy.org/en/stable/api/astropy.config.create_config_file.html
- https://docs.astropy.org/en/stable/api/astropy.config.generate_config.html
- https://docs.astropy.org/en/stable/api/astropy.config.get_cache_dir.html
- https://docs.astropy.org/en/stable/api/astropy.config.get_cache_dir_path.html
- https://docs.astropy.org/en/stable/api/astropy.config.get_config.html
- https://docs.astropy.org/en/stable/api/astropy.config.get_config_dir.html
- https://docs.astropy.org/en/stable/api/astropy.config.get_config_dir_path.html
- https://docs.astropy.org/en/stable/api/astropy.config.reload_config.html
- https://docs.astropy.org/en/stable/api/astropy.config.set_temp_cache.html
- https://docs.astropy.org/en/stable/api/astropy.config.set_temp_config.html
- https://docs.astropy.org/en/stable/api/astropy.config.temporary_cache_dir_path.html
- https://docs.astropy.org/en/stable/api/astropy.config.temporary_config_dir_path.html
- https://docs.astropy.org/en/stable/api/astropy.constants.Constant.html
- https://docs.astropy.org/en/stable/api/astropy.constants.EMConstant.html
- https://docs.astropy.org/en/stable/api/astropy.convolution.AiryDisk2DKernel.html
- https://docs.astropy.org/en/stable/api/astropy.convolution.Box1DKernel.html
- https://docs.astropy.org/en/stable/api/astropy.convolution.Box2DKernel.html
- https://docs.astropy.org/en/stable/api/astropy.convolution.CustomKernel.html
- https://docs.astropy.org/en/stable/api/astropy.convolution.Gaussian1DKernel.html
- https://docs.astropy.org/en/stable/api/astropy.convolution.Gaussian2DKernel.html
- https://docs.astropy.org/en/stable/api/astropy.convolution.Kernel.html
- https://docs.astropy.org/en/stable/api/astropy.convolution.Kernel1D.html
- https://docs.astropy.org/en/stable/api/astropy.convolution.Kernel2D.html
- https://docs.astropy.org/en/stable/api/astropy.convolution.KernelArithmeticError.html
- https://docs.astropy.org/en/stable/api/astropy.convolution.KernelError.html
- https://docs.astropy.org/en/stable/api/astropy.convolution.KernelSizeError.html
- https://docs.astropy.org/en/stable/api/astropy.convolution.Model1DKernel.html
- https://docs.astropy.org/en/stable/api/astropy.convolution.Model2DKernel.html
- https://docs.astropy.org/en/stable/api/astropy.convolution.Moffat2DKernel.html
- https://docs.astropy.org/en/stable/api/astropy.convolution.RickerWavelet1DKernel.html
- https://docs.astropy.org/en/stable/api/astropy.convolution.RickerWavelet2DKernel.html
- https://docs.astropy.org/en/stable/api/astropy.convolution.Ring2DKernel.html
- https://docs.astropy.org/en/stable/api/astropy.convolution.Tophat2DKernel.html
- https://docs.astropy.org/en/stable/api/astropy.convolution.Trapezoid1DKernel.html
- https://docs.astropy.org/en/stable/api/astropy.convolution.TrapezoidDisk2DKernel.html
- https://docs.astropy.org/en/stable/api/astropy.convolution.convolve.html
- https://docs.astropy.org/en/stable/api/astropy.convolution.convolve_fft.html
- https://docs.astropy.org/en/stable/api/astropy.convolution.convolve_models.html
- https://docs.astropy.org/en/stable/api/astropy.convolution.convolve_models_fft.html
- https://docs.astropy.org/en/stable/api/astropy.convolution.discretize_model.html
- https://docs.astropy.org/en/stable/api/astropy.convolution.interpolate_replace_nans.html
- https://docs.astropy.org/en/stable/api/astropy.convolution.kernel_arithmetics.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.AffineTransform.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.AltAz.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.Angle.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.Attribute.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.BarycentricMeanEcliptic.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.BarycentricTrueEcliptic.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.BaseAffineTransform.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.BaseBodycentricRepresentation.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.BaseCoordinateFrame.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.BaseDifferential.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.BaseEclipticFrame.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.BaseGeodeticRepresentation.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.BaseRADecFrame.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.BaseRepresentation.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.BaseRepresentationOrDifferential.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.BaseSphericalCosLatDifferential.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.BaseSphericalDifferential.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.BoundsError.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.CIRS.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.CartesianDifferential.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.CartesianRepresentation.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.CartesianRepresentationAttribute.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.CompositeTransform.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.ConvertError.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.CoordinateAttribute.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.CoordinateFrameInfo.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.CoordinateMatchResult.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.CoordinateSearchResult.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.CoordinateTransform.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.CustomBarycentricEcliptic.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.CylindricalDifferential.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.CylindricalRepresentation.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.DifferentialAttribute.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.Distance.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.DynamicMatrixTransform.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.EarthLocation.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.EarthLocationAttribute.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.FK4.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.FK4NoETerms.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.FK5.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.FunctionTransform.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.FunctionTransformWithFiniteDifference.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.GCRS.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.GRS80GeodeticRepresentation.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.Galactic.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.GalacticLSR.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.Galactocentric.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.GenericFrame.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.GeocentricMeanEcliptic.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.GeocentricTrueEcliptic.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.HADec.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.HCRS.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.HeliocentricEclipticIAU76.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.HeliocentricMeanEcliptic.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.HeliocentricTrueEcliptic.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.ICRS.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.ITRS.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.IllegalHourError.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.IllegalHourWarning.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.IllegalMinuteError.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.IllegalMinuteWarning.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.IllegalSecondError.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.IllegalSecondWarning.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.LSR.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.LSRD.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.LSRK.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.Latitude.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.Longitude.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.NonRotationTransformationError.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.NonRotationTransformationWarning.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.PhysicsSphericalDifferential.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.PhysicsSphericalRepresentation.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.PrecessedGeocentric.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.QuantityAttribute.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.RadialDifferential.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.RadialRepresentation.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.RangeError.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.RepresentationMapping.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.SkyCoord.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.SkyCoord.html#astropy.coordinates.SkyCoord
- https://docs.astropy.org/en/stable/api/astropy.coordinates.SkyCoordInfo.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.SkyOffsetFrame.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.SpectralCoord.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.SpectralQuantity.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.SphericalCosLatDifferential.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.SphericalDifferential.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.SphericalRepresentation.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.StaticMatrixTransform.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.StokesCoord.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.StokesSymbol.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.Supergalactic.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.TEME.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.TETE.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.TimeAttribute.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.TransformGraph.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.UnitSphericalCosLatDifferential.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.UnitSphericalDifferential.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.UnitSphericalRepresentation.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.UnknownSiteException.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.WGS72GeodeticRepresentation.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.WGS84GeodeticRepresentation.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.angular_separation.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.cartesian_to_spherical.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.concatenate.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.concatenate_representations.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.custom_stokes_symbol_mapping.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.galactocentric_frame_defaults.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.get_body.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.get_body_barycentric.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.get_body_barycentric_posvel.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.get_constellation.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.get_icrs_coordinates.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.get_sun.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.golden_spiral_grid.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.is_rotation_or_reflection.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.make_transform_graph_docs.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.match_coordinates_3d.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.match_coordinates_sky.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.offset_by.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.position_angle.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.rotation_matrix.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.search_around_3d.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.search_around_sky.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.solar_system_ephemeris.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.spherical_to_cartesian.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.uniform_spherical_random_surface.html
- https://docs.astropy.org/en/stable/api/astropy.coordinates.uniform_spherical_random_volume.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.Cosmology.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.CosmologyError.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.FLRW.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.FlatCosmologyMixin.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.FlatFLRWMixin.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.FlatLambdaCDM.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.Flatw0waCDM.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.Flatw0wzCDM.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.FlatwCDM.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.FlatwpwaCDM.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.LambdaCDM.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.Parameter.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.cosmology_equal.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.default_cosmology.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.io.CosmologyFromFormat.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.io.CosmologyRead.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.io.CosmologyToFormat.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.io.CosmologyWrite.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.realizations.Planck13.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.realizations.Planck15.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.realizations.Planck18.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.realizations.WMAP1.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.realizations.WMAP3.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.realizations.WMAP5.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.realizations.WMAP7.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.realizations.WMAP9.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.realizations.available.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.traits.BaryonComponent.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.traits.CriticalDensity.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.traits.CurvatureComponent.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.traits.DarkEnergyComponent.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.traits.DarkMatterComponent.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.traits.HubbleParameter.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.traits.MatterComponent.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.traits.NeutrinoComponent.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.traits.PhotonComponent.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.traits.ScaleFactor.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.traits.TemperatureCMB.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.traits.TotalComponent.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.units.dimensionless_redshift.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.units.redshift_distance.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.units.redshift_hubble.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.units.redshift_temperature.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.units.with_H0.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.units.with_redshift.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.w0waCDM.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.w0wzCDM.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.wCDM.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.wpwaCDM.html
- https://docs.astropy.org/en/stable/api/astropy.cosmology.z_at_value.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.AASTex.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.AllType.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.BaseData.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.BaseHeader.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.BaseInputter.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.BaseOutputter.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.BaseReader.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.BaseSplitter.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.Basic.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.BasicData.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.BasicHeader.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.Cds.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.Column.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.CommentedHeader.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.Conf.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.ContinuationLinesInputter.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.Csv.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.Daophot.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.DefaultSplitter.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.Ecsv.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.FastBasic.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.FastCommentedHeader.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.FastCsv.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.FastNoHeader.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.FastRdb.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.FastTab.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.FixedWidth.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.FixedWidthData.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.FixedWidthHeader.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.FixedWidthNoHeader.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.FixedWidthSplitter.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.FixedWidthTwoLine.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.FloatType.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.HTML.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.InconsistentTableError.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.IntType.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.Ipac.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.Latex.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.Mesa.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.Mrt.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.NoHeader.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.NoType.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.NumType.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.ParameterError.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.QDP.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.RST.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.Rdb.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.SExtractor.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.StrType.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.Tab.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.TableOutputter.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.Tdat.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.WhitespaceSplitter.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.convert_numpy.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.get_read_trace.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.get_reader.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.get_writer.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.read.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.set_guess.html
- https://docs.astropy.org/en/stable/api/astropy.io.ascii.write.html
- https://docs.astropy.org/en/stable/api/astropy.io.misc.ecsv.ColumnECSV.html
- https://docs.astropy.org/en/stable/api/astropy.io.misc.ecsv.ECSVEngine.html
- https://docs.astropy.org/en/stable/api/astropy.io.misc.ecsv.ECSVEngineIoAscii.html
- https://docs.astropy.org/en/stable/api/astropy.io.misc.ecsv.ECSVEnginePandas.html
- https://docs.astropy.org/en/stable/api/astropy.io.misc.ecsv.ECSVEnginePyArrow.html
- https://docs.astropy.org/en/stable/api/astropy.io.misc.ecsv.ECSVHeader.html
- https://docs.astropy.org/en/stable/api/astropy.io.misc.ecsv.read_ecsv.html
- https://docs.astropy.org/en/stable/api/astropy.io.misc.ecsv.register_ecsv_table.html
- https://docs.astropy.org/en/stable/api/astropy.io.misc.ecsv.write_ecsv.html
- https://docs.astropy.org/en/stable/api/astropy.io.misc.fnpickle.html
- https://docs.astropy.org/en/stable/api/astropy.io.misc.fnunpickle.html
- https://docs.astropy.org/en/stable/api/astropy.io.misc.hdf5.read_table_hdf5.html
- https://docs.astropy.org/en/stable/api/astropy.io.misc.hdf5.write_table_hdf5.html
- https://docs.astropy.org/en/stable/api/astropy.io.misc.pyarrow.csv.convert_pa_table_to_astropy_table.html
- https://docs.astropy.org/en/stable/api/astropy.io.misc.pyarrow.csv.read_csv.html
- https://docs.astropy.org/en/stable/api/astropy.io.misc.yaml.AstropyDumper.html
- https://docs.astropy.org/en/stable/api/astropy.io.misc.yaml.AstropyLoader.html
- https://docs.astropy.org/en/stable/api/astropy.io.misc.yaml.dump.html
- https://docs.astropy.org/en/stable/api/astropy.io.misc.yaml.load.html
- https://docs.astropy.org/en/stable/api/astropy.io.misc.yaml.load_all.html
- https://docs.astropy.org/en/stable/api/astropy.io.registry.IORegistryError.html
- https://docs.astropy.org/en/stable/api/astropy.io.registry.UnifiedIORegistry.html
- https://docs.astropy.org/en/stable/api/astropy.io.registry.UnifiedInputRegistry.html
- https://docs.astropy.org/en/stable/api/astropy.io.registry.UnifiedOutputRegistry.html
- https://docs.astropy.org/en/stable/api/astropy.io.registry.UnifiedReadWrite.html
- https://docs.astropy.org/en/stable/api/astropy.io.registry.UnifiedReadWriteMethod.html
- https://docs.astropy.org/en/stable/api/astropy.io.registry.delay_doc_updates.html
- https://docs.astropy.org/en/stable/api/astropy.io.registry.get_formats.html
- https://docs.astropy.org/en/stable/api/astropy.io.registry.get_reader.html
- https://docs.astropy.org/en/stable/api/astropy.io.registry.get_writer.html
- https://docs.astropy.org/en/stable/api/astropy.io.registry.identify_format.html
- https://docs.astropy.org/en/stable/api/astropy.io.registry.read.html
- https://docs.astropy.org/en/stable/api/astropy.io.registry.register_identifier.html
- https://docs.astropy.org/en/stable/api/astropy.io.registry.register_reader.html
- https://docs.astropy.org/en/stable/api/astropy.io.registry.register_writer.html
- https://docs.astropy.org/en/stable/api/astropy.io.registry.unregister_identifier.html
- https://docs.astropy.org/en/stable/api/astropy.io.registry.unregister_reader.html
- https://docs.astropy.org/en/stable/api/astropy.io.registry.unregister_writer.html
- https://docs.astropy.org/en/stable/api/astropy.io.registry.write.html
- https://docs.astropy.org/en/stable/api/astropy.io.typing.ReadableFileLike.html
- https://docs.astropy.org/en/stable/api/astropy.io.typing.WriteableFileLike.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.Conf.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.converters.Converter.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.converters.get_converter.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.converters.table_column_to_votable_datatype.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.dataorigin.DataOrigin.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.dataorigin.DatasetOrigin.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.dataorigin.QueryOrigin.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.dataorigin.add_data_origin_info.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.dataorigin.extract_data_origin.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.from_table.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.is_votable.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.parse.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.parse_single_table.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.tree.CooSys.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.tree.Element.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.tree.Field.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.tree.FieldRef.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.tree.Group.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.tree.Info.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.tree.Link.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.tree.MivotBlock.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.tree.Param.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.tree.ParamRef.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.tree.Resource.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.tree.TableElement.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.tree.TimeSys.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.tree.VOTableFile.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.tree.Values.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.ucd.check_ucd.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.ucd.parse_ucd.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.util.coerce_range_list_param.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.util.convert_to_writable_filelike.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.validate.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.validator.make_validation_report.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.writeto.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.xmlutil.check_anyuri.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.xmlutil.check_id.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.xmlutil.check_mime_content_type.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.xmlutil.check_token.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.xmlutil.fix_id.html
- https://docs.astropy.org/en/stable/api/astropy.io.votable.xmlutil.validate_schema.html
- https://docs.astropy.org/en/stable/api/astropy.logger.AstropyLogger.html
- https://docs.astropy.org/en/stable/api/astropy.logger.Conf.html
- https://docs.astropy.org/en/stable/api/astropy.logger.LoggingError.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.CompoundModel.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.Fittable1DModel.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.Fittable2DModel.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.FittableModel.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.InputParameterError.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.Model.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.ModelDefinitionError.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.Parameter.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.ParameterError.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.bind_bounding_box.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.bind_compound_bounding_box.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.bounding_box.CompoundBoundingBox.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.bounding_box.ModelBoundingBox.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.compose_models_with_units.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.custom_model.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.fitting.DogBoxLSQFitter.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.fitting.FitInfoArrayContainer.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.fitting.Fitter.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.fitting.FittingWithOutlierRemoval.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.fitting.JointFitter.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.fitting.LMLSQFitter.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.fitting.LevMarLSQFitter.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.fitting.LinearLSQFitter.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.fitting.ModelLinearityError.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.fitting.ModelsError.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.fitting.SLSQPLSQFitter.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.fitting.SimplexLSQFitter.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.fitting.TRFLSQFitter.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.fitting.parallel_fit_dask.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.fix_inputs.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.AiryDisk2D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.ArcCosine1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.ArcSine1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.ArcTangent1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Box1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Box2D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Const1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Const2D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Cosine1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Disk2D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Ellipse2D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Exponential1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Gaussian1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Gaussian2D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.GeneralSersic2D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.KingProjectedAnalytic1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Linear1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Logarithmic1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Lorentz1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Lorentz2D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Moffat1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Moffat2D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Multiply.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Planar2D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.RedshiftScaleFactor.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.RickerWavelet1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.RickerWavelet2D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Ring2D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Scale.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Sersic1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Sersic2D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Shift.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Sine1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Tangent1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Trapezoid1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.TrapezoidDisk2D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.functional_models.Voigt1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.is_separable.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.mappings.Identity.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.mappings.Mapping.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.mappings.UnitsMapping.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.optimizers.Optimization.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.optimizers.SLSQP.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.optimizers.Simplex.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.physical_models.BlackBody.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.physical_models.Drude1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.physical_models.NFW.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.physical_models.Plummer1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.polynomial.Chebyshev1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.polynomial.Chebyshev2D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.polynomial.Hermite1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.polynomial.Hermite2D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.polynomial.InverseSIP.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.polynomial.Legendre1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.polynomial.Legendre2D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.polynomial.OrthoPolynomialBase.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.polynomial.Polynomial1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.polynomial.Polynomial2D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.polynomial.PolynomialModel.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.polynomial.SIP.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.powerlaws.BrokenPowerLaw1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.powerlaws.ExponentialCutoffPowerLaw1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.powerlaws.LogParabola1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.powerlaws.PowerLaw1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.powerlaws.Schechter1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.powerlaws.SmoothlyBrokenPowerLaw1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.AffineTransformation2D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Conic.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Cylindrical.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.HEALPix.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2SkyProjection.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_AIR.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_AIT.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_ARC.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_AZP.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_Airy.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_BON.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_BonneEqualArea.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_CAR.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_CEA.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_COBEQuadSphericalCube.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_COD.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_COE.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_COO.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_COP.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_CSC.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_CYP.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_ConicEqualArea.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_ConicEquidistant.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_ConicOrthomorphic.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_ConicPerspective.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_CylindricalEqualArea.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_CylindricalPerspective.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_Gnomonic.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_HEALPix.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_HEALPixPolar.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_HPX.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_HammerAitoff.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_MER.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_MOL.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_Mercator.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_Molleweide.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_PAR.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_PCO.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_Parabolic.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_PlateCarree.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_Polyconic.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_QSC.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_QuadSphericalCube.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_SFL.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_SIN.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_STG.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_SZP.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_SansonFlamsteed.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_SlantOrthographic.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_SlantZenithalPerspective.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_Stereographic.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_TAN.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_TSC.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_TangentialSphericalCube.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_XPH.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_ZEA.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_ZenithalEqualArea.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_ZenithalEquidistant.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Pix2Sky_ZenithalPerspective.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Projection.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.PseudoConic.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.PseudoCylindrical.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.QuadCube.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2PixProjection.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_AIR.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_AIT.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_ARC.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_AZP.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_Airy.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_BON.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_BonneEqualArea.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_CAR.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_CEA.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_COBEQuadSphericalCube.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_COD.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_COE.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_COO.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_COP.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_CSC.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_CYP.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_ConicEqualArea.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_ConicEquidistant.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_ConicOrthomorphic.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_ConicPerspective.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_CylindricalEqualArea.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_CylindricalPerspective.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_Gnomonic.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_HEALPix.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_HEALPixPolar.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_HPX.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_HammerAitoff.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_MER.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_MOL.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_Mercator.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_Molleweide.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_PAR.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_PCO.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_Parabolic.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_PlateCarree.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_Polyconic.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_QSC.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_QuadSphericalCube.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_SFL.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_SIN.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_STG.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_SZP.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_SansonFlamsteed.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_SlantOrthographic.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_SlantZenithalPerspective.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_Stereographic.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_TAN.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_TSC.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_TangentialSphericalCube.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_XPH.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_ZEA.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_ZenithalEqualArea.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_ZenithalEquidistant.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Sky2Pix_ZenithalPerspective.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.projections.Zenithal.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.rotations.EulerAngleRotation.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.rotations.RotateCelestial2Native.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.rotations.RotateNative2Celestial.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.rotations.Rotation2D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.rotations.RotationSequence3D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.rotations.SphericalRotationSequence.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.separability_matrix.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.separable.is_separable.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.separable.separability_matrix.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.spline.Spline1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.spline.SplineExactKnotsFitter.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.spline.SplineInterpolateFitter.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.spline.SplineSmoothingFitter.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.spline.SplineSplrepFitter.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.statistic.leastsquare.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.statistic.leastsquare_1d.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.statistic.leastsquare_2d.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.statistic.leastsquare_3d.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.tabular.Tabular1D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.tabular.Tabular2D.html
- https://docs.astropy.org/en/stable/api/astropy.modeling.tabular.tabular_model.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.BitFlagNameMap.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.CCDData.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.Conf.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.Covariance.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.Cutout2D.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.FlagCollection.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.IncompatibleUncertaintiesException.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.InvalidBitFlag.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.InverseVariance.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.MissingDataAssociationException.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.NDArithmeticMixin.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.NDData.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.NDDataArray.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.NDDataBase.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.NDDataRef.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.NDIOMixin.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.NDSlicingMixin.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.NDUncertainty.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.NoOverlapError.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.PartialOverlapError.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.StdDevUncertainty.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.UnknownUncertainty.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.VarianceUncertainty.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.add_array.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.bitfield_to_boolean_mask.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.bitmask.BitFlagNameMap.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.bitmask.InvalidBitFlag.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.bitmask.bitfield_to_boolean_mask.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.bitmask.extend_bit_flag_map.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.bitmask.interpret_bit_flags.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.block_reduce.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.block_replicate.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.extend_bit_flag_map.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.extract_array.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.fits_ccddata_reader.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.fits_ccddata_writer.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.interpret_bit_flags.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.overlap_slices.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.reshape_as_blocks.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.subpixel_indices.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.support_nddata.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.utils.Cutout2D.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.utils.NoOverlapError.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.utils.PartialOverlapError.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.utils.add_array.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.utils.extract_array.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.utils.overlap_slices.html
- https://docs.astropy.org/en/stable/api/astropy.nddata.utils.subpixel_indices.html
- https://docs.astropy.org/en/stable/api/astropy.samp.Conf.html
- https://docs.astropy.org/en/stable/api/astropy.samp.SAMPClient.html
- https://docs.astropy.org/en/stable/api/astropy.samp.SAMPClientError.html
- https://docs.astropy.org/en/stable/api/astropy.samp.SAMPHubError.html
- https://docs.astropy.org/en/stable/api/astropy.samp.SAMPHubProxy.html
- https://docs.astropy.org/en/stable/api/astropy.samp.SAMPHubServer.html
- https://docs.astropy.org/en/stable/api/astropy.samp.SAMPIntegratedClient.html
- https://docs.astropy.org/en/stable/api/astropy.samp.SAMPMsgReplierWrapper.html
- https://docs.astropy.org/en/stable/api/astropy.samp.SAMPProxyError.html
- https://docs.astropy.org/en/stable/api/astropy.samp.SAMPWarning.html
- https://docs.astropy.org/en/stable/api/astropy.samp.SAMPXXEServerProxy.html
- https://docs.astropy.org/en/stable/api/astropy.samp.WebProfileDialog.html
- https://docs.astropy.org/en/stable/api/astropy.samp.safe_xmlrpc_loads.html
- https://docs.astropy.org/en/stable/api/astropy.stats.Events.html
- https://docs.astropy.org/en/stable/api/astropy.stats.FitnessFunc.html
- https://docs.astropy.org/en/stable/api/astropy.stats.PointMeasures.html
- https://docs.astropy.org/en/stable/api/astropy.stats.RegularEvents.html
- https://docs.astropy.org/en/stable/api/astropy.stats.RipleysKEstimator.html
- https://docs.astropy.org/en/stable/api/astropy.stats.SigmaClip.html
- https://docs.astropy.org/en/stable/api/astropy.stats.SigmaClippedStats.html
- https://docs.astropy.org/en/stable/api/astropy.stats.akaike_info_criterion.html
- https://docs.astropy.org/en/stable/api/astropy.stats.akaike_info_criterion_lsq.html
- https://docs.astropy.org/en/stable/api/astropy.stats.bayesian_blocks.html
- https://docs.astropy.org/en/stable/api/astropy.stats.bayesian_info_criterion.html
- https://docs.astropy.org/en/stable/api/astropy.stats.bayesian_info_criterion_lsq.html
- https://docs.astropy.org/en/stable/api/astropy.stats.binned_binom_proportion.html
- https://docs.astropy.org/en/stable/api/astropy.stats.binom_conf_interval.html
- https://docs.astropy.org/en/stable/api/astropy.stats.biweight.biweight_location.html
- https://docs.astropy.org/en/stable/api/astropy.stats.biweight.biweight_midcorrelation.html
- https://docs.astropy.org/en/stable/api/astropy.stats.biweight.biweight_midcovariance.html
- https://docs.astropy.org/en/stable/api/astropy.stats.biweight.biweight_midvariance.html
- https://docs.astropy.org/en/stable/api/astropy.stats.biweight.biweight_scale.html
- https://docs.astropy.org/en/stable/api/astropy.stats.biweight_location.html
- https://docs.astropy.org/en/stable/api/astropy.stats.biweight_midcorrelation.html
- https://docs.astropy.org/en/stable/api/astropy.stats.biweight_midcovariance.html
- https://docs.astropy.org/en/stable/api/astropy.stats.biweight_midvariance.html
- https://docs.astropy.org/en/stable/api/astropy.stats.biweight_scale.html
- https://docs.astropy.org/en/stable/api/astropy.stats.bootstrap.html
- https://docs.astropy.org/en/stable/api/astropy.stats.calculate_bin_edges.html
- https://docs.astropy.org/en/stable/api/astropy.stats.cdf_from_intervals.html
- https://docs.astropy.org/en/stable/api/astropy.stats.circcorrcoef.html
- https://docs.astropy.org/en/stable/api/astropy.stats.circmean.html
- https://docs.astropy.org/en/stable/api/astropy.stats.circmoment.html
- https://docs.astropy.org/en/stable/api/astropy.stats.circstats.circcorrcoef.html
- https://docs.astropy.org/en/stable/api/astropy.stats.circstats.circmean.html
- https://docs.astropy.org/en/stable/api/astropy.stats.circstats.circmoment.html
- https://docs.astropy.org/en/stable/api/astropy.stats.circstats.circstd.html
- https://docs.astropy.org/en/stable/api/astropy.stats.circstats.circvar.html
- https://docs.astropy.org/en/stable/api/astropy.stats.circstats.rayleightest.html
- https://docs.astropy.org/en/stable/api/astropy.stats.circstats.vonmisesmle.html
- https://docs.astropy.org/en/stable/api/astropy.stats.circstats.vtest.html
- https://docs.astropy.org/en/stable/api/astropy.stats.circstd.html
- https://docs.astropy.org/en/stable/api/astropy.stats.circvar.html
- https://docs.astropy.org/en/stable/api/astropy.stats.fold_intervals.html
- https://docs.astropy.org/en/stable/api/astropy.stats.freedman_bin_width.html
- https://docs.astropy.org/en/stable/api/astropy.stats.histogram.html
- https://docs.astropy.org/en/stable/api/astropy.stats.histogram_intervals.html
- https://docs.astropy.org/en/stable/api/astropy.stats.interval_overlap_length.html
- https://docs.astropy.org/en/stable/api/astropy.stats.jackknife_resampling.html
- https://docs.astropy.org/en/stable/api/astropy.stats.jackknife_stats.html
- https://docs.astropy.org/en/stable/api/astropy.stats.knuth_bin_width.html
- https://docs.astropy.org/en/stable/api/astropy.stats.kuiper.html
- https://docs.astropy.org/en/stable/api/astropy.stats.kuiper_false_positive_probability.html
- https://docs.astropy.org/en/stable/api/astropy.stats.kuiper_two.html
- https://docs.astropy.org/en/stable/api/astropy.stats.mad_std.html
- https://docs.astropy.org/en/stable/api/astropy.stats.median_absolute_deviation.html
- https://docs.astropy.org/en/stable/api/astropy.stats.poisson_conf_interval.html
- https://docs.astropy.org/en/stable/api/astropy.stats.rayleightest.html
- https://docs.astropy.org/en/stable/api/astropy.stats.scott_bin_width.html
- https://docs.astropy.org/en/stable/api/astropy.stats.sigma_clip.html
- https://docs.astropy.org/en/stable/api/astropy.stats.sigma_clipped_stats.html
- https://docs.astropy.org/en/stable/api/astropy.stats.sigma_clipping.SigmaClip.html
- https://docs.astropy.org/en/stable/api/astropy.stats.sigma_clipping.SigmaClippedStats.html
- https://docs.astropy.org/en/stable/api/astropy.stats.sigma_clipping.sigma_clip.html
- https://docs.astropy.org/en/stable/api/astropy.stats.sigma_clipping.sigma_clipped_stats.html
- https://docs.astropy.org/en/stable/api/astropy.stats.signal_to_noise_oir_ccd.html
- https://docs.astropy.org/en/stable/api/astropy.stats.vonmisesmle.html
- https://docs.astropy.org/en/stable/api/astropy.stats.vtest.html
- https://docs.astropy.org/en/stable/api/astropy.table.BST.html
- https://docs.astropy.org/en/stable/api/astropy.table.Column.html
- https://docs.astropy.org/en/stable/api/astropy.table.ColumnGroups.html
- https://docs.astropy.org/en/stable/api/astropy.table.ColumnInfo.html
- https://docs.astropy.org/en/stable/api/astropy.table.Conf.html
- https://docs.astropy.org/en/stable/api/astropy.table.JSViewer.html
- https://docs.astropy.org/en/stable/api/astropy.table.MaskedColumn.html
- https://docs.astropy.org/en/stable/api/astropy.table.NdarrayMixin.html
- https://docs.astropy.org/en/stable/api/astropy.table.PprintIncludeExclude.html
- https://docs.astropy.org/en/stable/api/astropy.table.QTable.html
- https://docs.astropy.org/en/stable/api/astropy.table.Row.html
- https://docs.astropy.org/en/stable/api/astropy.table.SCEngine.html
- https://docs.astropy.org/en/stable/api/astropy.table.SerializedColumn.html
- https://docs.astropy.org/en/stable/api/astropy.table.SortedArray.html
- https://docs.astropy.org/en/stable/api/astropy.table.StringTruncateWarning.html
- https://docs.astropy.org/en/stable/api/astropy.table.Table.html
- https://docs.astropy.org/en/stable/api/astropy.table.TableAttribute.html
- https://docs.astropy.org/en/stable/api/astropy.table.TableColumns.html
- https://docs.astropy.org/en/stable/api/astropy.table.TableFormatter.html
- https://docs.astropy.org/en/stable/api/astropy.table.TableGroups.html
- https://docs.astropy.org/en/stable/api/astropy.table.TableMergeError.html
- https://docs.astropy.org/en/stable/api/astropy.table.TableReplaceWarning.html
- https://docs.astropy.org/en/stable/api/astropy.table.dstack.html
- https://docs.astropy.org/en/stable/api/astropy.table.hstack.html
- https://docs.astropy.org/en/stable/api/astropy.table.join.html
- https://docs.astropy.org/en/stable/api/astropy.table.join_distance.html
- https://docs.astropy.org/en/stable/api/astropy.table.join_skycoord.html
- https://docs.astropy.org/en/stable/api/astropy.table.notebook_backends.classic.html
- https://docs.astropy.org/en/stable/api/astropy.table.notebook_backends.ipydatagrid.html
- https://docs.astropy.org/en/stable/api/astropy.table.represent_mixins_as_columns.html
- https://docs.astropy.org/en/stable/api/astropy.table.setdiff.html
- https://docs.astropy.org/en/stable/api/astropy.table.unique.html
- https://docs.astropy.org/en/stable/api/astropy.table.vstack.html
- https://docs.astropy.org/en/stable/api/astropy.time.AstropyDatetimeLeapSecondWarning.html
- https://docs.astropy.org/en/stable/api/astropy.time.Conf.html
- https://docs.astropy.org/en/stable/api/astropy.time.OperandTypeError.html
- https://docs.astropy.org/en/stable/api/astropy.time.ScaleValueError.html
- https://docs.astropy.org/en/stable/api/astropy.time.Time.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeBase.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeBesselianEpoch.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeBesselianEpochString.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeCxcSec.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeDatetime.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeDatetime64.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeDecimalYear.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeDelta.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeDeltaDatetime.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeDeltaFormat.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeDeltaJD.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeDeltaMissingUnitWarning.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeDeltaNumeric.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeDeltaQuantityString.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeDeltaSec.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeEpochDate.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeEpochDateString.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeFITS.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeFormat.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeFromEpoch.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeGPS.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeGalexSec.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeISO.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeISOT.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeInfo.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeInfoBase.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeJD.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeJulianEpoch.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeJulianEpochString.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeMJD.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeNumeric.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimePlotDate.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeString.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeUnique.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeUnix.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeUnixTai.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeYMDHMS.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimeYearDayTime.html
- https://docs.astropy.org/en/stable/api/astropy.time.TimezoneInfo.html
- https://docs.astropy.org/en/stable/api/astropy.time.update_leap_seconds.html
- https://docs.astropy.org/en/stable/api/astropy.timeseries.BasePeriodogram.html
- https://docs.astropy.org/en/stable/api/astropy.timeseries.BaseTimeSeries.html
- https://docs.astropy.org/en/stable/api/astropy.timeseries.BinnedTimeSeries.html
- https://docs.astropy.org/en/stable/api/astropy.timeseries.BoxLeastSquares.html
- https://docs.astropy.org/en/stable/api/astropy.timeseries.BoxLeastSquaresResults.html
- https://docs.astropy.org/en/stable/api/astropy.timeseries.LombScargle.html
- https://docs.astropy.org/en/stable/api/astropy.timeseries.LombScargleMultiband.html
- https://docs.astropy.org/en/stable/api/astropy.timeseries.TimeSeries.html
- https://docs.astropy.org/en/stable/api/astropy.timeseries.aggregate_downsample.html
- https://docs.astropy.org/en/stable/api/astropy.timeseries.autocheck_required_columns.html
- https://docs.astropy.org/en/stable/api/astropy.timeseries.io.kepler_fits_reader.html
- https://docs.astropy.org/en/stable/api/astropy.uncertainty.Distribution.html
- https://docs.astropy.org/en/stable/api/astropy.uncertainty.normal.html
- https://docs.astropy.org/en/stable/api/astropy.uncertainty.poisson.html
- https://docs.astropy.org/en/stable/api/astropy.uncertainty.uniform.html
- https://docs.astropy.org/en/stable/api/astropy.units.CompositeUnit.html
- https://docs.astropy.org/en/stable/api/astropy.units.Decibel.html
- https://docs.astropy.org/en/stable/api/astropy.units.DecibelUnit.html
- https://docs.astropy.org/en/stable/api/astropy.units.Dex.html
- https://docs.astropy.org/en/stable/api/astropy.units.DexUnit.html
- https://docs.astropy.org/en/stable/api/astropy.units.Equivalency.html
- https://docs.astropy.org/en/stable/api/astropy.units.FunctionQuantity.html
- https://docs.astropy.org/en/stable/api/astropy.units.FunctionUnitBase.html
- https://docs.astropy.org/en/stable/api/astropy.units.IrreducibleUnit.html
- https://docs.astropy.org/en/stable/api/astropy.units.LogQuantity.html
- https://docs.astropy.org/en/stable/api/astropy.units.LogUnit.html
- https://docs.astropy.org/en/stable/api/astropy.units.MagUnit.html
- https://docs.astropy.org/en/stable/api/astropy.units.Magnitude.html
- https://docs.astropy.org/en/stable/api/astropy.units.NamedUnit.html
- https://docs.astropy.org/en/stable/api/astropy.units.PhysicalType.html
- https://docs.astropy.org/en/stable/api/astropy.units.PrefixUnit.html
- https://docs.astropy.org/en/stable/api/astropy.units.Quantity.html
- https://docs.astropy.org/en/stable/api/astropy.units.QuantityInfo.html
- https://docs.astropy.org/en/stable/api/astropy.units.QuantityInfoBase.html
- https://docs.astropy.org/en/stable/api/astropy.units.SpecificTypeQuantity.html
- https://docs.astropy.org/en/stable/api/astropy.units.StructuredUnit.html
- https://docs.astropy.org/en/stable/api/astropy.units.Unit.html
- https://docs.astropy.org/en/stable/api/astropy.units.UnitBase.html
- https://docs.astropy.org/en/stable/api/astropy.units.UnitConversionError.html
- https://docs.astropy.org/en/stable/api/astropy.units.UnitParserWarning.html
- https://docs.astropy.org/en/stable/api/astropy.units.UnitPrefix.html
- https://docs.astropy.org/en/stable/api/astropy.units.UnitScaleError.html
- https://docs.astropy.org/en/stable/api/astropy.units.UnitTypeError.html
- https://docs.astropy.org/en/stable/api/astropy.units.UnitsError.html
- https://docs.astropy.org/en/stable/api/astropy.units.UnitsWarning.html
- https://docs.astropy.org/en/stable/api/astropy.units.UnrecognizedUnit.html
- https://docs.astropy.org/en/stable/api/astropy.units.add_enabled_aliases.html
- https://docs.astropy.org/en/stable/api/astropy.units.add_enabled_equivalencies.html
- https://docs.astropy.org/en/stable/api/astropy.units.add_enabled_units.html
- https://docs.astropy.org/en/stable/api/astropy.units.allclose.html
- https://docs.astropy.org/en/stable/api/astropy.units.beam_angular_area.html
- https://docs.astropy.org/en/stable/api/astropy.units.brightness_temperature.html
- https://docs.astropy.org/en/stable/api/astropy.units.cds.enable.html
- https://docs.astropy.org/en/stable/api/astropy.units.def_physical_type.html
- https://docs.astropy.org/en/stable/api/astropy.units.def_unit.html
- https://docs.astropy.org/en/stable/api/astropy.units.dimensionless_angles.html
- https://docs.astropy.org/en/stable/api/astropy.units.doppler_optical.html
- https://docs.astropy.org/en/stable/api/astropy.units.doppler_radio.html
- https://docs.astropy.org/en/stable/api/astropy.units.doppler_redshift.html
- https://docs.astropy.org/en/stable/api/astropy.units.doppler_relativistic.html
- https://docs.astropy.org/en/stable/api/astropy.units.format.Base.html
- https://docs.astropy.org/en/stable/api/astropy.units.format.CDS.html
- https://docs.astropy.org/en/stable/api/astropy.units.format.Console.html
- https://docs.astropy.org/en/stable/api/astropy.units.format.FITS.html
- https://docs.astropy.org/en/stable/api/astropy.units.format.Generic.html
- https://docs.astropy.org/en/stable/api/astropy.units.format.Latex.html
- https://docs.astropy.org/en/stable/api/astropy.units.format.LatexInline.html
- https://docs.astropy.org/en/stable/api/astropy.units.format.OGIP.html
- https://docs.astropy.org/en/stable/api/astropy.units.format.Unicode.html
- https://docs.astropy.org/en/stable/api/astropy.units.format.VOUnit.html
- https://docs.astropy.org/en/stable/api/astropy.units.format.get_format.html
- https://docs.astropy.org/en/stable/api/astropy.units.get_current_unit_registry.html
- https://docs.astropy.org/en/stable/api/astropy.units.get_physical_type.html
- https://docs.astropy.org/en/stable/api/astropy.units.imperial.enable.html
- https://docs.astropy.org/en/stable/api/astropy.units.isclose.html
- https://docs.astropy.org/en/stable/api/astropy.units.logarithmic.html
- https://docs.astropy.org/en/stable/api/astropy.units.magnetic_flux_field.html
- https://docs.astropy.org/en/stable/api/astropy.units.mass_energy.html
- https://docs.astropy.org/en/stable/api/astropy.units.molar_mass_amu.html
- https://docs.astropy.org/en/stable/api/astropy.units.parallax.html
- https://docs.astropy.org/en/stable/api/astropy.units.physical.PhysicalType.html
- https://docs.astropy.org/en/stable/api/astropy.units.physical.def_physical_type.html
- https://docs.astropy.org/en/stable/api/astropy.units.physical.get_physical_type.html
- https://docs.astropy.org/en/stable/api/astropy.units.pixel_scale.html
- https://docs.astropy.org/en/stable/api/astropy.units.plate_scale.html
- https://docs.astropy.org/en/stable/api/astropy.units.quantity_input.html
- https://docs.astropy.org/en/stable/api/astropy.units.set_enabled_aliases.html
- https://docs.astropy.org/en/stable/api/astropy.units.set_enabled_equivalencies.html
- https://docs.astropy.org/en/stable/api/astropy.units.set_enabled_units.html
- https://docs.astropy.org/en/stable/api/astropy.units.spectral.html
- https://docs.astropy.org/en/stable/api/astropy.units.spectral_density.html
- https://docs.astropy.org/en/stable/api/astropy.units.temperature.html
- https://docs.astropy.org/en/stable/api/astropy.units.temperature_energy.html
- https://docs.astropy.org/en/stable/api/astropy.units.thermodynamic_temperature.html
- https://docs.astropy.org/en/stable/api/astropy.units.zero_point_flux.html
- https://docs.astropy.org/en/stable/api/astropy.utils.codegen.make_function_with_signature.html
- https://docs.astropy.org/en/stable/api/astropy.utils.collections.HomogeneousList.html
- https://docs.astropy.org/en/stable/api/astropy.utils.console.ProgressBar.html
- https://docs.astropy.org/en/stable/api/astropy.utils.console.ProgressBarOrSpinner.html
- https://docs.astropy.org/en/stable/api/astropy.utils.console.Spinner.html
- https://docs.astropy.org/en/stable/api/astropy.utils.console.color_print.html
- https://docs.astropy.org/en/stable/api/astropy.utils.console.human_file_size.html
- https://docs.astropy.org/en/stable/api/astropy.utils.console.human_time.html
- https://docs.astropy.org/en/stable/api/astropy.utils.console.isatty.html
- https://docs.astropy.org/en/stable/api/astropy.utils.console.print_code_line.html
- https://docs.astropy.org/en/stable/api/astropy.utils.console.terminal_size.html
- https://docs.astropy.org/en/stable/api/astropy.utils.data.CacheDamaged.html
- https://docs.astropy.org/en/stable/api/astropy.utils.data.CacheMissingWarning.html
- https://docs.astropy.org/en/stable/api/astropy.utils.data.Conf.html
- https://docs.astropy.org/en/stable/api/astropy.utils.data.cache_contents.html
- https://docs.astropy.org/en/stable/api/astropy.utils.data.cache_total_size.html
- https://docs.astropy.org/en/stable/api/astropy.utils.data.check_download_cache.html
- https://docs.astropy.org/en/stable/api/astropy.utils.data.check_free_space_in_dir.html
- https://docs.astropy.org/en/stable/api/astropy.utils.data.clear_download_cache.html
- https://docs.astropy.org/en/stable/api/astropy.utils.data.compute_hash.html
- https://docs.astropy.org/en/stable/api/astropy.utils.data.download_file.html
- https://docs.astropy.org/en/stable/api/astropy.utils.data.download_files_in_parallel.html
- https://docs.astropy.org/en/stable/api/astropy.utils.data.export_download_cache.html
- https://docs.astropy.org/en/stable/api/astropy.utils.data.get_cached_urls.html
- https://docs.astropy.org/en/stable/api/astropy.utils.data.get_file_contents.html
- https://docs.astropy.org/en/stable/api/astropy.utils.data.get_free_space_in_dir.html
- https://docs.astropy.org/en/stable/api/astropy.utils.data.get_pkg_data_contents.html
- https://docs.astropy.org/en/stable/api/astropy.utils.data.get_pkg_data_filename.html
- https://docs.astropy.org/en/stable/api/astropy.utils.data.get_pkg_data_filenames.html
- https://docs.astropy.org/en/stable/api/astropy.utils.data.get_pkg_data_fileobj.html
- https://docs.astropy.org/en/stable/api/astropy.utils.data.get_pkg_data_fileobjs.html
- https://docs.astropy.org/en/stable/api/astropy.utils.data.get_pkg_data_path.html
- https://docs.astropy.org/en/stable/api/astropy.utils.data.get_readable_fileobj.html
- https://docs.astropy.org/en/stable/api/astropy.utils.data.import_download_cache.html
- https://docs.astropy.org/en/stable/api/astropy.utils.data.import_file_to_cache.html
- https://docs.astropy.org/en/stable/api/astropy.utils.data.is_url.html
- https://docs.astropy.org/en/stable/api/astropy.utils.data.is_url_in_cache.html
- https://docs.astropy.org/en/stable/api/astropy.utils.data_info.BaseColumnInfo.html
- https://docs.astropy.org/en/stable/api/astropy.utils.data_info.DataInfo.html
- https://docs.astropy.org/en/stable/api/astropy.utils.data_info.MixinInfo.html
- https://docs.astropy.org/en/stable/api/astropy.utils.data_info.ParentDtypeInfo.html
- https://docs.astropy.org/en/stable/api/astropy.utils.data_info.data_info_factory.html
- https://docs.astropy.org/en/stable/api/astropy.utils.data_info.dtype_info_name.html
- https://docs.astropy.org/en/stable/api/astropy.utils.decorators.classproperty.html
- https://docs.astropy.org/en/stable/api/astropy.utils.decorators.deprecated.html
- https://docs.astropy.org/en/stable/api/astropy.utils.decorators.deprecated_attribute.html
- https://docs.astropy.org/en/stable/api/astropy.utils.decorators.deprecated_renamed_argument.html
- https://docs.astropy.org/en/stable/api/astropy.utils.decorators.format_doc.html
- https://docs.astropy.org/en/stable/api/astropy.utils.decorators.lazyproperty.html
- https://docs.astropy.org/en/stable/api/astropy.utils.decorators.sharedmethod.html
- https://docs.astropy.org/en/stable/api/astropy.utils.diff.diff_values.html
- https://docs.astropy.org/en/stable/api/astropy.utils.diff.report_diff_values.html
- https://docs.astropy.org/en/stable/api/astropy.utils.diff.where_not_allclose.html
- https://docs.astropy.org/en/stable/api/astropy.utils.exceptions.AstropyBackwardsIncompatibleChangeWarning.html
- https://docs.astropy.org/en/stable/api/astropy.utils.exceptions.AstropyDeprecationWarning.html
- https://docs.astropy.org/en/stable/api/astropy.utils.exceptions.AstropyPendingDeprecationWarning.html
- https://docs.astropy.org/en/stable/api/astropy.utils.exceptions.AstropyUserWarning.html
- https://docs.astropy.org/en/stable/api/astropy.utils.exceptions.AstropyWarning.html
- https://docs.astropy.org/en/stable/api/astropy.utils.exceptions.DuplicateRepresentationWarning.html
- https://docs.astropy.org/en/stable/api/astropy.utils.iers.Conf.html
- https://docs.astropy.org/en/stable/api/astropy.utils.iers.IERS.html
- https://docs.astropy.org/en/stable/api/astropy.utils.iers.IERSDegradedAccuracyWarning.html
- https://docs.astropy.org/en/stable/api/astropy.utils.iers.IERSRangeError.html
- https://docs.astropy.org/en/stable/api/astropy.utils.iers.IERSStaleWarning.html
- https://docs.astropy.org/en/stable/api/astropy.utils.iers.IERSWarning.html
- https://docs.astropy.org/en/stable/api/astropy.utils.iers.IERS_A.html
- https://docs.astropy.org/en/stable/api/astropy.utils.iers.IERS_Auto.html
- https://docs.astropy.org/en/stable/api/astropy.utils.iers.IERS_B.html
- https://docs.astropy.org/en/stable/api/astropy.utils.iers.LeapSeconds.html
- https://docs.astropy.org/en/stable/api/astropy.utils.iers.earth_orientation_table.html
- https://docs.astropy.org/en/stable/api/astropy.utils.introspection.find_current_module.html
- https://docs.astropy.org/en/stable/api/astropy.utils.introspection.isinstancemethod.html
- https://docs.astropy.org/en/stable/api/astropy.utils.introspection.minversion.html
- https://docs.astropy.org/en/stable/api/astropy.utils.introspection.resolve_name.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.MaskableShapedLikeNDArray.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.Masked.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.MaskedNDArray.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.combine_masks.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.function_helpers.bincount.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.function_helpers.broadcast_arrays.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.function_helpers.broadcast_to.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.function_helpers.choose.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.function_helpers.copyto.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.function_helpers.count_nonzero.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.function_helpers.full_like.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.function_helpers.insert.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.function_helpers.interp.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.function_helpers.lexsort.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.function_helpers.nanargmax.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.function_helpers.nanargmin.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.function_helpers.nancumprod.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.function_helpers.nancumsum.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.function_helpers.nanmax.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.function_helpers.nanmean.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.function_helpers.nanmedian.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.function_helpers.nanmin.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.function_helpers.nanpercentile.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.function_helpers.nanprod.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.function_helpers.nanquantile.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.function_helpers.nanstd.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.function_helpers.nansum.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.function_helpers.nanvar.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.function_helpers.ones_like.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.function_helpers.piecewise.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.function_helpers.place.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.function_helpers.put.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.function_helpers.select.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.function_helpers.zeros_like.html
- https://docs.astropy.org/en/stable/api/astropy.utils.masked.get_data_and_mask.html
- https://docs.astropy.org/en/stable/api/astropy.utils.metadata.MergeConflictError.html
- https://docs.astropy.org/en/stable/api/astropy.utils.metadata.MergeConflictWarning.html
- https://docs.astropy.org/en/stable/api/astropy.utils.metadata.MergeNpConcatenate.html
- https://docs.astropy.org/en/stable/api/astropy.utils.metadata.MergePlus.html
- https://docs.astropy.org/en/stable/api/astropy.utils.metadata.MergeStrategy.html
- https://docs.astropy.org/en/stable/api/astropy.utils.metadata.MetaAttribute.html
- https://docs.astropy.org/en/stable/api/astropy.utils.metadata.MetaData.html
- https://docs.astropy.org/en/stable/api/astropy.utils.metadata.common_dtype.html
- https://docs.astropy.org/en/stable/api/astropy.utils.metadata.enable_merge_strategies.html
- https://docs.astropy.org/en/stable/api/astropy.utils.metadata.merge.html
- https://docs.astropy.org/en/stable/api/astropy.utils.misc.JsonCustomEncoder.html
- https://docs.astropy.org/en/stable/api/astropy.utils.misc.NumpyRNGContext.html
- https://docs.astropy.org/en/stable/api/astropy.utils.misc.dtype_bytes_or_chars.html
- https://docs.astropy.org/en/stable/api/astropy.utils.misc.find_api_page.html
- https://docs.astropy.org/en/stable/api/astropy.utils.misc.format_exception.html
- https://docs.astropy.org/en/stable/api/astropy.utils.misc.indent.html
- https://docs.astropy.org/en/stable/api/astropy.utils.misc.isiterable.html
- https://docs.astropy.org/en/stable/api/astropy.utils.misc.online_help.html
- https://docs.astropy.org/en/stable/api/astropy.utils.misc.silence.html
- https://docs.astropy.org/en/stable/api/astropy.utils.parsing.ThreadSafeParser.html
- https://docs.astropy.org/en/stable/api/astropy.utils.parsing.lex.html
- https://docs.astropy.org/en/stable/api/astropy.utils.parsing.yacc.html
- https://docs.astropy.org/en/stable/api/astropy.utils.shapes.IncompatibleShapeError.html
- https://docs.astropy.org/en/stable/api/astropy.utils.shapes.NDArrayShapeMethods.html
- https://docs.astropy.org/en/stable/api/astropy.utils.shapes.ShapedLikeNDArray.html
- https://docs.astropy.org/en/stable/api/astropy.utils.shapes.check_broadcast.html
- https://docs.astropy.org/en/stable/api/astropy.utils.shapes.simplify_basic_index.html
- https://docs.astropy.org/en/stable/api/astropy.utils.shapes.unbroadcast.html
- https://docs.astropy.org/en/stable/api/astropy.utils.state.ScienceState.html
- https://docs.astropy.org/en/stable/api/astropy.utils.system_info.system_info.html
- https://docs.astropy.org/en/stable/api/astropy.utils.xml.check.check_anyuri.html
- https://docs.astropy.org/en/stable/api/astropy.utils.xml.check.check_id.html
- https://docs.astropy.org/en/stable/api/astropy.utils.xml.check.check_mime_content_type.html
- https://docs.astropy.org/en/stable/api/astropy.utils.xml.check.check_token.html
- https://docs.astropy.org/en/stable/api/astropy.utils.xml.check.fix_id.html
- https://docs.astropy.org/en/stable/api/astropy.utils.xml.iterparser.get_xml_encoding.html
- https://docs.astropy.org/en/stable/api/astropy.utils.xml.iterparser.get_xml_iterator.html
- https://docs.astropy.org/en/stable/api/astropy.utils.xml.iterparser.xml_readlines.html
- https://docs.astropy.org/en/stable/api/astropy.utils.xml.unescaper.unescape_all.html
- https://docs.astropy.org/en/stable/api/astropy.utils.xml.validate.validate_schema.html
- https://docs.astropy.org/en/stable/api/astropy.utils.xml.writer.XMLWriter.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.AsinhStretch.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.AsymmetricPercentileInterval.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.BaseInterval.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.BaseStretch.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.BaseTransform.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.CompositeStretch.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.CompositeTransform.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.ContrastBiasStretch.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.HistEqStretch.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.ImageNormalize.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.LinearStretch.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.LogStretch.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.LuptonAsinhStretch.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.LuptonAsinhZscaleStretch.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.ManualInterval.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.MinMaxInterval.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.MplQuantityConverter.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.PercentileInterval.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.PowerDistStretch.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.PowerStretch.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.SimpleNorm.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.SinhStretch.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.SqrtStretch.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.SquaredStretch.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.SymmetricInterval.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.ZScaleInterval.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.hist.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.imshow_norm.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.imshow_simple_norm.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.make_lupton_rgb.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.make_rgb.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.mpl_normalize.ImageNormalize.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.mpl_normalize.SimpleNorm.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.mpl_normalize.imshow_norm.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.mpl_normalize.imshow_simple_norm.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.mpl_normalize.simple_norm.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.quantity_support.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.simple_norm.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.time_support.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.wcsaxes.Conf.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.wcsaxes.CoordinateHelper.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.wcsaxes.CoordinatesMap.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.wcsaxes.Quadrangle.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.wcsaxes.SphericalCircle.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.wcsaxes.WCSAxes.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.wcsaxes.WCSAxesSubplot.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.wcsaxes.add_beam.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.wcsaxes.add_scalebar.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.wcsaxes.custom_ucd_coord_meta_mapping.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.wcsaxes.frame.BaseFrame.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.wcsaxes.frame.EllipticalFrame.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.wcsaxes.frame.RectangularFrame.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.wcsaxes.frame.RectangularFrame1D.html
- https://docs.astropy.org/en/stable/api/astropy.visualization.wcsaxes.frame.Spine.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.Auxprm.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.Celprm.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.DistortionLookupTable.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.FITSFixedWarning.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.InconsistentAxisTypesError.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.InvalidCoordinateError.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.InvalidPrjParametersError.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.InvalidSubimageSpecificationError.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.InvalidTabularParametersError.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.InvalidTransformError.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.NoConvergence.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.NoSolutionError.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.NoWcsKeywordsFoundError.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.NonseparableSubimageCoordinateSystemError.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.Prjprm.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.SingularMatrixError.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.Sip.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.Tabprm.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.WCS.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.WCS.html#astropy.wcs.WCS
- https://docs.astropy.org/en/stable/api/astropy.wcs.WCSBase.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.WcsError.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.Wcsprm.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.Wtbarr.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.find_all_wcs.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.get_include.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.utils.add_stokes_axis_to_wcs.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.utils.celestial_frame_to_wcs.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.utils.custom_frame_to_wcs_mappings.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.utils.custom_wcs_to_frame_mappings.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.utils.is_proj_plane_distorted.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.utils.local_partial_pixel_derivatives.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.utils.non_celestial_pixel_scales.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.utils.obsgeo_to_frame.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.utils.pixel_to_pixel.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.utils.pixel_to_skycoord.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.utils.proj_plane_pixel_area.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.utils.proj_plane_pixel_scales.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.utils.skycoord_to_pixel.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.utils.wcs_to_celestial_frame.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.validate.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.wcsapi.BaseHighLevelWCS.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.wcsapi.BaseLowLevelWCS.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.wcsapi.BaseWCSWrapper.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.wcsapi.HighLevelWCSMixin.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.wcsapi.HighLevelWCSWrapper.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.wcsapi.SlicedLowLevelWCS.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.wcsapi.deserialize_class.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.wcsapi.high_level_objects_to_values.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.wcsapi.sanitize_slices.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.wcsapi.validate_physical_types.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.wcsapi.values_to_high_level_objects.html
- https://docs.astropy.org/en/stable/api/astropy.wcs.wcsapi.wcs_info_str.html
- https://docs.astropy.org/en/stable/changelog.html
- https://docs.astropy.org/en/stable/config/astropy_config.html
- https://docs.astropy.org/en/stable/config/index.html
- https://docs.astropy.org/en/stable/config/ref_api.html
- https://docs.astropy.org/en/stable/constants/index.html
- https://docs.astropy.org/en/stable/convolution/index.html
- https://docs.astropy.org/en/stable/convolution/kernels.html
- https://docs.astropy.org/en/stable/convolution/non_normalized_kernels.html
- https://docs.astropy.org/en/stable/convolution/ref_api.html
- https://docs.astropy.org/en/stable/convolution/using.html
- https://docs.astropy.org/en/stable/coordinates/angles.html
- https://docs.astropy.org/en/stable/coordinates/apply_space_motion.html
- https://docs.astropy.org/en/stable/coordinates/common_errors.html
- https://docs.astropy.org/en/stable/coordinates/definitions.html
- https://docs.astropy.org/en/stable/coordinates/example_gallery_index.html
- https://docs.astropy.org/en/stable/coordinates/example_gallery_plot_galactocentric_frame.html
- https://docs.astropy.org/en/stable/coordinates/example_gallery_plot_mars_coordinate_frame.html
- https://docs.astropy.org/en/stable/coordinates/example_gallery_plot_obs_planning.html
- https://docs.astropy.org/en/stable/coordinates/example_gallery_plot_sgr_coordinate_frame.html
- https://docs.astropy.org/en/stable/coordinates/example_gallery_rv_to_gsr.html
- https://docs.astropy.org/en/stable/coordinates/formatting.html
- https://docs.astropy.org/en/stable/coordinates/frames.html
- https://docs.astropy.org/en/stable/coordinates/galactocentric.html
- https://docs.astropy.org/en/stable/coordinates/index.html
- https://docs.astropy.org/en/stable/coordinates/inplace.html
- https://docs.astropy.org/en/stable/coordinates/matchsep.html
- https://docs.astropy.org/en/stable/coordinates/ref_api.html
- https://docs.astropy.org/en/stable/coordinates/remote_methods.html
- https://docs.astropy.org/en/stable/coordinates/representations.html
- https://docs.astropy.org/en/stable/coordinates/satellites.html
- https://docs.astropy.org/en/stable/coordinates/skycoord.html
- https://docs.astropy.org/en/stable/coordinates/solarsystem.html
- https://docs.astropy.org/en/stable/coordinates/spectralcoord.html
- https://docs.astropy.org/en/stable/coordinates/stokescoord.html
- https://docs.astropy.org/en/stable/coordinates/transforming.html
- https://docs.astropy.org/en/stable/coordinates/velocities.html
- https://docs.astropy.org/en/stable/cosmology/dev.html
- https://docs.astropy.org/en/stable/cosmology/index.html
- https://docs.astropy.org/en/stable/cosmology/io/builtin.html
- https://docs.astropy.org/en/stable/cosmology/io/custom.html
- https://docs.astropy.org/en/stable/cosmology/io/details.html
- https://docs.astropy.org/en/stable/cosmology/io/index.html
- https://docs.astropy.org/en/stable/cosmology/realizations.html
- https://docs.astropy.org/en/stable/cosmology/ref_api.html
- https://docs.astropy.org/en/stable/cosmology/traits.html
- https://docs.astropy.org/en/stable/cosmology/units.html
- https://docs.astropy.org/en/stable/credits.html
- https://docs.astropy.org/en/stable/environment_variables.html
- https://docs.astropy.org/en/stable/glossary.html
- https://docs.astropy.org/en/stable/impact_health.html
- https://docs.astropy.org/en/stable/importing_astropy.html
- https://docs.astropy.org/en/stable/index.html
- https://docs.astropy.org/en/stable/index_dev.html
- https://docs.astropy.org/en/stable/index_getting_started.html
- https://docs.astropy.org/en/stable/index_project_details.html
- https://docs.astropy.org/en/stable/index_user_docs.html
- https://docs.astropy.org/en/stable/install.html
- https://docs.astropy.org/en/stable/io/ascii/base_classes.html
- https://docs.astropy.org/en/stable/io/ascii/ecsv.html
- https://docs.astropy.org/en/stable/io/ascii/extension_classes.html
- https://docs.astropy.org/en/stable/io/ascii/fast_ascii_io.html
- https://docs.astropy.org/en/stable/io/ascii/fixed_width_gallery.html
- https://docs.astropy.org/en/stable/io/ascii/index.html
- https://docs.astropy.org/en/stable/io/ascii/read.html
- https://docs.astropy.org/en/stable/io/ascii/ref_api.html
- https://docs.astropy.org/en/stable/io/ascii/write.html
- https://docs.astropy.org/en/stable/io/fits/api/cards.html
- https://docs.astropy.org/en/stable/io/fits/api/diff.html
- https://docs.astropy.org/en/stable/io/fits/api/files.html
- https://docs.astropy.org/en/stable/io/fits/api/hdulists.html
- https://docs.astropy.org/en/stable/io/fits/api/hdus.html
- https://docs.astropy.org/en/stable/io/fits/api/headers.html
- https://docs.astropy.org/en/stable/io/fits/api/images.html
- https://docs.astropy.org/en/stable/io/fits/api/index.html
- https://docs.astropy.org/en/stable/io/fits/api/tables.html
- https://docs.astropy.org/en/stable/io/fits/api/tiled_compression.html
- https://docs.astropy.org/en/stable/io/fits/api/verification.html
- https://docs.astropy.org/en/stable/io/fits/appendix/faq.html
- https://docs.astropy.org/en/stable/io/fits/appendix/header_transition.html
- https://docs.astropy.org/en/stable/io/fits/appendix/history.html
- https://docs.astropy.org/en/stable/io/fits/index.html
- https://docs.astropy.org/en/stable/io/fits/usage/cloud.html
- https://docs.astropy.org/en/stable/io/fits/usage/headers.html
- https://docs.astropy.org/en/stable/io/fits/usage/image.html
- https://docs.astropy.org/en/stable/io/fits/usage/misc.html
- https://docs.astropy.org/en/stable/io/fits/usage/scripts.html
- https://docs.astropy.org/en/stable/io/fits/usage/table.html
- https://docs.astropy.org/en/stable/io/fits/usage/unfamiliar.html
- https://docs.astropy.org/en/stable/io/fits/usage/verification.html
- https://docs.astropy.org/en/stable/io/misc.html
- https://docs.astropy.org/en/stable/io/misc_ref_api.html
- https://docs.astropy.org/en/stable/io/overview.html
- https://docs.astropy.org/en/stable/io/registry.html
- https://docs.astropy.org/en/stable/io/registry_ref_api.html
- https://docs.astropy.org/en/stable/io/typing.html
- https://docs.astropy.org/en/stable/io/unified.html
- https://docs.astropy.org/en/stable/io/unified_image.html
- https://docs.astropy.org/en/stable/io/unified_table.html
- https://docs.astropy.org/en/stable/io/unified_table_fits.html
- https://docs.astropy.org/en/stable/io/unified_table_hdf5.html
- https://docs.astropy.org/en/stable/io/unified_table_parquet.html
- https://docs.astropy.org/en/stable/io/unified_table_text.html
- https://docs.astropy.org/en/stable/io/unified_table_votable.html
- https://docs.astropy.org/en/stable/io/votable/api_exceptions.html
- https://docs.astropy.org/en/stable/io/votable/coosys_element.html
- https://docs.astropy.org/en/stable/io/votable/index.html
- https://docs.astropy.org/en/stable/io/votable/mivot_blocks.html
- https://docs.astropy.org/en/stable/io/votable/ref_api.html
- https://docs.astropy.org/en/stable/io/votable/table_element.html
- https://docs.astropy.org/en/stable/known_issues.html
- https://docs.astropy.org/en/stable/license.html
- https://docs.astropy.org/en/stable/logging.html
- https://docs.astropy.org/en/stable/lts_policy.html
- https://docs.astropy.org/en/stable/modeling/add-units.html
- https://docs.astropy.org/en/stable/modeling/compound-models.html
- https://docs.astropy.org/en/stable/modeling/example-fitting-constraints.html
- https://docs.astropy.org/en/stable/modeling/example-fitting-line.html
- https://docs.astropy.org/en/stable/modeling/example-fitting-model-sets.html
- https://docs.astropy.org/en/stable/modeling/fitting.html
- https://docs.astropy.org/en/stable/modeling/index.html
- https://docs.astropy.org/en/stable/modeling/jointfitter.html
- https://docs.astropy.org/en/stable/modeling/models.html
- https://docs.astropy.org/en/stable/modeling/new-fitter.html
- https://docs.astropy.org/en/stable/modeling/new-model.html
- https://docs.astropy.org/en/stable/modeling/parallel-fitting.html
- https://docs.astropy.org/en/stable/modeling/parameters.html
- https://docs.astropy.org/en/stable/modeling/performance.html
- https://docs.astropy.org/en/stable/modeling/physical_models.html
- https://docs.astropy.org/en/stable/modeling/polynomial_models.html
- https://docs.astropy.org/en/stable/modeling/powerlaw_models.html
- https://docs.astropy.org/en/stable/modeling/predef_models1D.html
- https://docs.astropy.org/en/stable/modeling/predef_models2D.html
- https://docs.astropy.org/en/stable/modeling/reference_api.html
- https://docs.astropy.org/en/stable/modeling/spline_models.html
- https://docs.astropy.org/en/stable/modeling/units.html
- https://docs.astropy.org/en/stable/nddata/bitmask.html
- https://docs.astropy.org/en/stable/nddata/ccddata.html
- https://docs.astropy.org/en/stable/nddata/covariance.html
- https://docs.astropy.org/en/stable/nddata/decorator.html
- https://docs.astropy.org/en/stable/nddata/index.html
- https://docs.astropy.org/en/stable/nddata/mixins/index.html
- https://docs.astropy.org/en/stable/nddata/mixins/ndarithmetic.html
- https://docs.astropy.org/en/stable/nddata/mixins/ndio.html
- https://docs.astropy.org/en/stable/nddata/mixins/ndslicing.html
- https://docs.astropy.org/en/stable/nddata/nddata.html
- https://docs.astropy.org/en/stable/nddata/ref_api.html
- https://docs.astropy.org/en/stable/nddata/subclassing.html
- https://docs.astropy.org/en/stable/nddata/utils.html
- https://docs.astropy.org/en/stable/samp/advanced_embed_samp_hub.html
- https://docs.astropy.org/en/stable/samp/example_clients.html
- https://docs.astropy.org/en/stable/samp/example_hub.html
- https://docs.astropy.org/en/stable/samp/example_table_image.html
- https://docs.astropy.org/en/stable/samp/index.html
- https://docs.astropy.org/en/stable/samp/ref_api.html
- https://docs.astropy.org/en/stable/stats/circ.html
- https://docs.astropy.org/en/stable/stats/index.html
- https://docs.astropy.org/en/stable/stats/ref_api.html
- https://docs.astropy.org/en/stable/stats/ripley.html
- https://docs.astropy.org/en/stable/stats/robust.html
- https://docs.astropy.org/en/stable/table/access_table.html
- https://docs.astropy.org/en/stable/table/construct_table.html
- https://docs.astropy.org/en/stable/table/dataframes.html
- https://docs.astropy.org/en/stable/table/implementation_details.html
- https://docs.astropy.org/en/stable/table/index.html
- https://docs.astropy.org/en/stable/table/indexing.html
- https://docs.astropy.org/en/stable/table/masking.html
- https://docs.astropy.org/en/stable/table/mixin_columns.html
- https://docs.astropy.org/en/stable/table/modify_table.html
- https://docs.astropy.org/en/stable/table/operations.html
- https://docs.astropy.org/en/stable/table/pandas.html
- https://docs.astropy.org/en/stable/table/ref_api.html
- https://docs.astropy.org/en/stable/table/table_and_dataframes.html
- https://docs.astropy.org/en/stable/time/index.html
- https://docs.astropy.org/en/stable/time/ref_api.html
- https://docs.astropy.org/en/stable/timeseries/analysis.html
- https://docs.astropy.org/en/stable/timeseries/bls.html
- https://docs.astropy.org/en/stable/timeseries/data_access.html
- https://docs.astropy.org/en/stable/timeseries/index.html
- https://docs.astropy.org/en/stable/timeseries/initializing.html
- https://docs.astropy.org/en/stable/timeseries/io.html
- https://docs.astropy.org/en/stable/timeseries/lombscargle.html
- https://docs.astropy.org/en/stable/timeseries/lombscarglemb.html
- https://docs.astropy.org/en/stable/timeseries/masking.html
- https://docs.astropy.org/en/stable/timeseries/pandas.html
- https://docs.astropy.org/en/stable/timeseries/ref_api.html
- https://docs.astropy.org/en/stable/timeseries/times.html
- https://docs.astropy.org/en/stable/uncertainty/index.html
- https://docs.astropy.org/en/stable/units/combining_and_defining.html
- https://docs.astropy.org/en/stable/units/constants_versions.html
- https://docs.astropy.org/en/stable/units/conversion.html
- https://docs.astropy.org/en/stable/units/decomposing_and_composing.html
- https://docs.astropy.org/en/stable/units/equivalencies.html
- https://docs.astropy.org/en/stable/units/format.html
- https://docs.astropy.org/en/stable/units/index.html
- https://docs.astropy.org/en/stable/units/logarithmic_units.html
- https://docs.astropy.org/en/stable/units/physical_types.html
- https://docs.astropy.org/en/stable/units/quantity.html
- https://docs.astropy.org/en/stable/units/ref_api.html
- https://docs.astropy.org/en/stable/units/standard_units.html
- https://docs.astropy.org/en/stable/units/structured_units.html
- https://docs.astropy.org/en/stable/units/type_hints.html
- https://docs.astropy.org/en/stable/utils/data.html
- https://docs.astropy.org/en/stable/utils/iers.html
- https://docs.astropy.org/en/stable/utils/index.html
- https://docs.astropy.org/en/stable/utils/masked/index.html
- https://docs.astropy.org/en/stable/utils/ref_api.html
- https://docs.astropy.org/en/stable/visualization/histogram.html
- https://docs.astropy.org/en/stable/visualization/index.html
- https://docs.astropy.org/en/stable/visualization/matplotlib_integration.html
- https://docs.astropy.org/en/stable/visualization/normalization.html
- https://docs.astropy.org/en/stable/visualization/ref_api.html
- https://docs.astropy.org/en/stable/visualization/rgb.html
- https://docs.astropy.org/en/stable/visualization/wcsaxes/controlling_axes.html
- https://docs.astropy.org/en/stable/visualization/wcsaxes/custom_frames.html
- https://docs.astropy.org/en/stable/visualization/wcsaxes/generic_transforms.html
- https://docs.astropy.org/en/stable/visualization/wcsaxes/images_contours.html
- https://docs.astropy.org/en/stable/visualization/wcsaxes/index.html
- https://docs.astropy.org/en/stable/visualization/wcsaxes/initializing_axes.html
- https://docs.astropy.org/en/stable/visualization/wcsaxes/overlaying_coordinate_systems.html
- https://docs.astropy.org/en/stable/visualization/wcsaxes/overlays.html
- https://docs.astropy.org/en/stable/visualization/wcsaxes/slicing_datacubes.html
- https://docs.astropy.org/en/stable/visualization/wcsaxes/ticks_labels_grid.html
- https://docs.astropy.org/en/stable/warnings.html
- https://docs.astropy.org/en/stable/wcs/creating_planetary_wcs.html
- https://docs.astropy.org/en/stable/wcs/example_create_imaging.html
- https://docs.astropy.org/en/stable/wcs/example_cube_wcs.html
- https://docs.astropy.org/en/stable/wcs/history.html
- https://docs.astropy.org/en/stable/wcs/index.html
- https://docs.astropy.org/en/stable/wcs/legacy_interface.html
- https://docs.astropy.org/en/stable/wcs/loading_from_fits.html
- https://docs.astropy.org/en/stable/wcs/reference_api.html
- https://docs.astropy.org/en/stable/wcs/relax.html
- https://docs.astropy.org/en/stable/wcs/supported_projections.html
- https://docs.astropy.org/en/stable/wcs/validation.html
- https://docs.astropy.org/en/stable/wcs/wcsapi.html
- https://docs.astropy.org/en/stable/wcs/wcstools.html
- https://docs.astropy.org/en/stable/whatsnew/8.0.html
- https://docs.astropy.org/en/stable/whatsnew/index.html
- https://docs.python.org/3/builtins/constants.html#None
- https://docs.python.org/3/builtins/functions.html#int
- https://docs.python.org/3/builtins/stdtypes.html#str
- https://docs.python.org/3/builtins/stdtypes.html#tuple
- https://github.com/astropy/astropy
- https://github.com/astropy/astropy/edit/main/astropy/wcs/utils.py#L1063
- https://learn.astropy.org/
- https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html#numpy.ndarray
- https://photutils.readthedocs.io
- https://reproject.readthedocs.io
- https://specreduce.readthedocs.io
- https://specutils.readthedocs.io
