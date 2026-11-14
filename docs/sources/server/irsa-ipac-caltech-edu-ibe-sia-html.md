---
source: https://irsa.ipac.caltech.edu/ibe/sia.html
fetched: 2026-11-14
status: 200
---

IRSA Image Server - SIA v2 Queries

Simple Image Access v2 Queries
==============================

* [Overview](#overview)
* [Available datasets](#avail)
* [Metadata queries](#metadata)
* [Query Constraints](#constraints)
* [Examples](#examples)
* [Understanding the Results](#results)
* [Downloading Data](#download)
* [Getting Help](#help)

Overview
--------

The IRSA implementation of the [IVOA](http://www.ivoa.net) [SIA v2 specification](http://www.ivoa.net/documents/SIA/) allows users to query the majority of the IRSA holdings (see [table](#avail) below) through a single, standardized interface. All data set collections available through our SIA v2 service conform to a unified set of metadata; users are not expected to know or specify column names within the individual data sets. An overview of perform SIA v2 queries in IRSA is provided below - for full details, please see the [IVOA](http://www.ivoa.net) [SIA v2 specification](http://www.ivoa.net/documents/SIA/). IRSA's SIA v2 service can also be accessed from Python via [astroquery](https://astroquery.readthedocs.io/en/latest/ipac/irsa/irsa.html#image-and-spectra-searches).

Almost all of IRSA's imaging data sets are accessible via SIA v2. A few, however, can still only be accessed via [legacy APIs](/docs/program_interface/api_images.html#other); others are accessible via both.
**All new programmatic queries of IRSA imaging data sets should use the SIA v2 service rather than our older APIs whenever possible.**

Available datasets
------------------

Fetching data

Query Constraints
-----------------

An SIA v2 query returns
a table of files satisfying any number of constraints. By default,
queries return results from all datasets. IRSA's SIA v2
holdings contain almost a billion records, so searches without
constraints will time out. Commonly used constraints limit by position
(using the [POS](#POS) keyword), dataset (using
the [COLLECTION](#COLLECTION) keyword), and
calibration level (using the [CALIB](#CALIB)
keyword), as described below. In addition, the type of
output can be specified with
the [RESPONSEFORMAT](#RESPONSEFORMAT) keyword, and
the number of rows can be limited with
the [MAXREC](#MAXREC) keyword. The complete list
of parameters supported by IRSA's SIA v2 implementation is

* [BAND](#BAND)
* [CALIB](#CALIB)
* [CLOSEST](#CLOSEST)
* [COLLECTION](#COLLECTION)
* [DPTYPE](#DPTYPE)
* [EXPTIME](#EXPTIME)
* [FACILITY](#FACILITY)
* [FORMAT](#FORMAT)
* [FOV](#FOV)
* [ID](#ID)
* [INSTRUMENT](#INSTRUMENT)
* [MAXREC](#MAXREC)
* [POL](#POL)
* [POS](#POS)
* [RESPONSEFORMAT](#RESPONSEFORMAT)
* [SPATRES](#SPATRES)
* [SPECRP](#SPECRP)
* [TARGET](#TARGET)
* [TIME](#TIME)
* [TIMERES](#TIMERES)
* [UPLOAD](#UPLOAD)

BAND
:   The BAND parameter defines the
    wavelength interval(s) in meters to be searched for data. The interval can be
    open or closed, and is inclusive of the bounding values. A BAND constraint is satisfied if the interval
    intersects the wavelength coverage of the observation as returned in
    the em\_min, em\_max columns.

    Examples:

    1. Find data that intersects a J-band filter covering 1.154--1.316 micron:

       BAND=1.154e-6 1.316e-6
    2. Find data with wavelength longer than 1.4 micron:

       BAND=1.4e-6 Inf
    3. Find data with wavelength shorter than 1.4 micron:

       BAND=-Inf 1.4e-6
    4. Find data that includes 2.2 micron:

       BAND=2.2e-6

CALIB
:   The CALIB parameter
    identifies the calibration level of an observation.
    This is useful for distinguishing between raw,
    processed, and highly processed data that are all
    part of the same collection. The specific meaning
    for the different levels are specified in
    the [IVOA
    ObsCore](http://www.ivoa.net/documents/ObsCore/index.html) standard:

    * **Level 0**: Raw instrumental data, in a proprietary or internal data-provider defined format, that
      needs instrument specific tools to be handled.
    * **Level 1**: Instrumental data in a standard format (FITS, VOTable, SDFITS, ASDM, etc.) which
      could be manipulated with standard astronomical packages.
    * **Level 2**: Calibrated, science ready data with the instrument signature removed.
    * **Level 3**: Enhanced data products like mosaics, resampled or drizzled images, or heavily
      processed survey fields. Level 3 data products may represent the combination of data from
      multiple primary observations.
    * **Level 4**: Analysis data products generated after some scientific data manipulation or interpretation.

    Examples:

    * CALIB=1
    * CALIB=2
    * CALIB=3

CLOSEST
:   The CLOSEST parameter resembles
    the combination of an SQL `GROUP BY` with
    a `MIN` aggregate: images meeting the
    constraints of the query are divided into groups based on
    the values of fields specified by the user, and within
    each group only the image or images at the minimum
    distance from the query position are returned.

    CLOSEST=*field*[,*field*,...]
    where each *field* is one of the SIA parameters
    `COLLECTION`, `FACILITY`,
    `INSTRUMENT`, `DPTYPE`, and `TARGET`.

    If multiple images meeting those constraints are at the
    same minimal distance from the center, all of those images
    are returned.

    CLOSEST is supported only for
    queries with POS=CIRCLE. It is not
    supported for POS=RANGE
    or POS=POLYGON.

    When used with the [UPLOAD](#UPLOAD) param, the closest image
    or images per group are returned separately for each uploaded
    position. The `upload_row_id` column in the response
    links each row of the result with the uploaded position to which it corresponds.

    Examples:

    1. Find the closest image from each (facility, instrument)
       combination within 0.001 degrees of a position:

       ```
       wget -O results.vot "https://irsa.ipac.caltech.edu/SIA?POS=CIRCLE+174.617+54.714+0.001&CLOSEST=FACILITY,INSTRUMENT"
       ```
    2. Find the closest image from each collection within 0.0001
       degrees of a position:

       ```
       wget -O results.vot "https://irsa.ipac.caltech.edu/SIA?POS=CIRCLE+174.617+54.714+0.0001&CLOSEST=COLLECTION"
       ```
    3. Find the closest Spitzer image from each (facility, instrument)
       combination, using an uploaded table of positions and a constant radius of 0.001:

       ```

       curl -o results.vot \
         -F "COLLECTION=spitzer_sha" \
         -F "POS=CIRCLE my_positions.ra my_positions.dec 0.001" \
         -F "CLOSEST=FACILITY,INSTRUMENT" \
         -F "UPLOAD=my_positions,param:my_table" \
         -F "my_table=saved_positions.tbl" \
         https://irsa.ipac.caltech.edu/SIA
       ```

COLLECTION
:   The COLLECTION parameter identifies
    the group of data to which an observation belongs. Multiple collections can be queried in the same call by including more than one COLLECTION= clauses. For a complete set of valid options, see [the table of SIA2 COLLECTION names](#avail) above.

    Examples:

    * COLLECTION=spitzer\_sha
    * COLLECTION=wise\_allwise
    * COLLECTION=twomass\_allsky
    * COLLECTION=twomass\_allsky&COLLECTION=wise\_allwise

DPTYPE
:   The DPTYPE parameter specifies the type of data to be searched. The only values allowed here for SIA v2 queries are "image" and "cube."

    Examples:

    * DPTYPE=image
    * DPTYPE=cube

EXPTIME
:   The EXPTIME parameter identifies the range of exposure times to be searched. Values are assumed to be in units of seconds.

    Examples:

    1. Find data with exposure times between 60 and 180 seconds:

       EXPTIME=60 180
    2. Find data with exposure times longer than 30 seconds:

       EXPTIME=30 +Inf
    3. Find data with exposure times shorter than 5 minutes:

       EXPTIME=-Inf 300

FACILITY
:   The FACILITY parameter defines the name of the facility where the data were acquired.

    Examples:

    * FACILITY=Wide-field Infrared Survey Explorer
    * FACILITY=Spitzer Space Telescope
    * FACILITY=The 2 Micron All Sky Survey 1.3m Telescope at Cerro Tololo Inter-American Observatory

FORMAT
:   The FORMAT parameter constrains
    which data products are returned based on their data
    format, as listed in the access\_format column.

    Examples:

    * FORMAT=application/x-gzip
    * FORMAT=image/fits
    * FORMAT=text/plain

FOV
:   The FOV parameter identifies the range of the field of view to be searched. Values are assumed to be in units of decimal degrees.

    Examples:

    1. Find data with a field of view between 0.5 and 1 degrees:

       FOV=0.5 1.0
    2. Find data with a field of view larger than 0.1 degrees:

       FOV=0.1 +Inf
    3. Find data with a field of view smaller than 0.1 degrees:

       FOV=-Inf 0.1

ID
:   The ID parameter defines the identifier of the dataset. The values are strings and searches are case-insensitive.

    Examples:

    * ID=ivo://irsa.ipac/wise\_allwise/1640m061\_ac51
    * ID=ivo://irsa.ipac/twomass\_allsky/allsky/990114s/s082

INSTRUMENT
:   The INSTRUMENT parameter defines the name of the instrument on which the data were acquired.

    Examples:

    * INSTRUMENT=GALEX
    * INSTRUMENT=IRAC
    * INSTRUMENT=2MASS Survey Camera

MAXREC
:   The MAXREC parameter specifies the
    maximum number of records to retrieve. The default is
    unlimited. However, any jobs taking longer than 5 minutes will
    be canceled. For larger jobs, please
    use [TAP](/docs/program_interface/TAP.html).

    Examples:

    * MAXREC=0
    * MAXREC=100
    * MAXREC=1000000

POL
:   The POL parameter identifies polarization state to be matched in the data query.

    Examples:

    * POL=I
    * POL=LL
    * POL=V

    IRSA does not currently contain any data in which the polarization state has been populated.

POS
:   The POS parameter value must
    consist of a shape described by ICRS coordinates in
    decimal degrees. Only images which intersect that shape
    are candidates for the result set. Note that the
    constraint requires only that the shape and the image
    intersect; there is no requirement that the center or
    centroid of the image be contained in the shape.

    Examples:

    1. A circle with radius=1 degree centered on (164.7, -5.8):

       POS=circle 164.7 -5.8 1
    2. A polygon shape with corners at (164, -5), (165, -5), (164, -6):

       POS=polygon 164 -5 165 -5 165 -6 164 -6
    3. A region spanning RA=104 to 105 deg and Dec=-22 to -12 deg:

       POS=range 104 105 -22 -12

    The spatial extent of an image is approximated by
    connecting its corners with great circles to form a
    spherical convex polygon. The search region as defined by
    this service is also a spherical convex polygon (or a
    point). Spatial predicate evaluation is performed on pairs
    of spherical convex polygons without recourse to any
    performance motivated short-cuts. Nevertheless, the
    implementation uses floating point arithmetic and results
    are therefore not guaranteed to be mathematically
    exact. Note also that the spatial extent of an image with
    a non-gnomonic projection (or large distortion terms) may
    not be well approximated by the technique employed. The
    images currently being served, though, do have gnomonic or
    orthographic projections, and they also have small area
    and small distortion terms, so we believe our
    approximations are accurate enough to be useful.

RESPONSEFORMAT
:   The RESPONSEFORMAT
    parameter specifies what type of output the service
    will return. The default is VOTable, but many
    options are available:

    * FITS: [Flexible Image Transport System](https://fits.gsfc.nasa.gov/) (FITS binary table)
    * IPAC\_TABLE: [IPAC's Table Format](http://irsa.ipac.caltech.edu/applications/DDGEN/Doc/ipac_tbl.html)
    * HDF5: [Hierarchical Data Format v5](https://www.hdfgroup.org/)
    * VOTABLE: [IVOA VOTable](http://www.ivoa.net/Documents/VOTable/)
    * JSON: [JavaScript Object Notation](http://json.org)
    * CSV: Comma Separated Values (suitable for loading into spreadsheets)
    * TSV: Tab Separated Values (suitable for loading into spreadsheets)
    * TEXT: Plain text
    * HTML: HTML table suitable for embedding within another page
    * POSTGRES: SQL for loading the result into [Postgres](https://www.postgresql.org/)
    * SQLITE: SQL for loading the result into [SQLite](http://www.sqlite.org/)
    * ORACLE: SQL for loading the result into [Oracle](https://www.oracle.com/database/index.html)
    * DB: Raw SQLite database

    Examples:

    * RESPONSEFORMAT=FITS
    * RESPONSEFORMAT=JSON
    * RESPONSEFORMAT=TEXT

SPATRES
:   The SPATRES parameter identifies the range of spatial resolution to be searched. Values are assumed to be in units of arcsec.

    Examples:

    1. Find data with a spatial resolution between 0.1 and 1.0 arcsec:

       SPATRES=0.1 1.0
    2. Find data with a spatial resolution larger than 0.5 arcsec:

       SPATRES=0.5 +Inf
    3. Find data with a spatial resolution smaller than 1.0 arcsec:

       SPATRES=-Inf 1.0

SPECRP
:   The SPECRP parameter identifies the spectral resolving power to be used in the search. Values are unitless and the resolving power is assumed to be expressed as λ/Δλ.

    Examples:

    1. Find data with spectral resolving power between 500 and 5000:

       SPECRP=500 5000
    2. Find data with spectral resolving power higher than 10000:

       SPECRP=10000 +Inf
    3. Find data with spectral resolving power lower than 5000:

       SPECRP=-Inf 5000

TARGET
:   The TARGET parameter identifies the name of the target of the intended observation, if such exists. Many datasets (e.g. all-sky surveys) do not have target names associated with their observations.

TIME
:   The TIME parameter identifies the time boundaries in which an observation occurs. The TIME parameter values should be entered as numeric values in Modified Julian Date (MJD) format; time intervals can be either open or closed.

    Examples:

    1. Find data obtained between MJD=55123.456 and MJD=55123.789:

       TIME=55123.456 55123.789
    2. Find data obtained at MJD=55123.456:

       TIME=55123.456

TIMERES
:   The TIMERES parameter defines the temporal resolution to be searched. Values are assumed to be in units of seconds.

    Examples:

    1. Find data with a temporal resolution between 1.0 and 2.0 seconds:

       TIMERES=1.0 2.0
    2. Find data with a temporal resolution larger than 0.5 seconds:

       TIMERES=0.5 +Inf
    3. Find data with a temporal resolution smaller than 1.0 second:

       TIMERES=-Inf 1.0

UPLOAD
:   The UPLOAD parameter supports
    combining searches at multiple positions in a single
    request. As with the POS parameter which
    UPLOAD generalizes,
    all values are assumed to be in units of decimal degrees.

    Via the UPLOAD parameter, you
    can provide a table whose every row represents a different
    instance of the same shape: for instance, a table with
    columns `ra`, `dec`,
    and `radius`. Results for all positions
    represented in the uploaded table are returned in a single
    response. The
    `upload_row_id` column in the response table links each row of the response with the corresponding row of the uploaded table.

    `UPLOAD=name,URI`

    * `name`: the name by which you refer to the uploaded table
      in the POS parameter value.
    * `URI`: the location of the table to upload. To upload a
      local file, use `param:tag` as the URI, where `tag`
      is a name of your choosing that you will use in a separate
      `-F "tag=@path_to_file"` argument to curl (see examples below).
      To upload a remote file, provide an `http` or
      `https` URL.

    Valid upload formats are VOTable, CSV, TSV, and IPAC\_TABLE.

    UPLOAD is supported only for
    queries with POS=CIRCLE or
    POS=RANGE. It is not supported
    for POS=POLYGON.

    Examples:

    1. Upload a local IPAC table named 'my\_positions.tbl'
       that lives in the `upload_tables`
       subdirectory of the directory from which you are
       running this command. For each position in the upload
       table, search for NEOWISE-R images that intersect the
       circle centered at that position with radius 0.001
       decimal degrees:

       ```

       curl -o results.xml \
         -F "COLLECTION=neowiser" \
         -F "POS=CIRCLE my_table.ra my_table.dec 0.001" \
         -F "UPLOAD=my_table,param:my_path" \
         -F "my_path=@upload_tables/my_positions.tbl" \
         https://irsa.ipac.caltech.edu/SIA
       ```
    2. Upload a VOTable found at '/path/to/upload\_table.vot'
       on the host from which you are running this command.
       For each row in the upload table, search for NEOWISE-R
       images that intersect the circle whose center
       coordinates are the values of the table's
       `ra1` and `dec1` columns in that row
       and whose radius is the value of the `radius_small` column
       in that row:

       ```

       curl -o results.xml \
         -F "COLLECTION=neowiser" \
         -F "POS=CIRCLE my_positions.ra1 my_positions.dec1 my_positions.radius_small" \
         -F "UPLOAD=my_positions,param:my_table" \
         -F "my_table=@/path/to/upload_table.vot" \
         https://irsa.ipac.caltech.edu/SIA
       ```
    3. Use the remote-file syntax with an inner query to search for all
       SPHEREx quick release 2 images that are within 0.1
       degrees of the 2MASS sources returned from a cone
       search within 0.01 degree of ra=210.80225,
       dec=54.34894.
       (See [TAP](/docs/program_interface/TAP.html)
       for documentation of the TAP/sync and TAP/async
       endpoints.)

       ```

       curl -o results.xml \
       -F "COLLECTION=spherex_qr2" \
       -F "POS=CIRCLE my_table.ra my_table.dec 0.1"  \
       -F "UPLOAD=my_table,https://irsa.ipac.caltech.edu/TAP/sync?QUERY=SELECT+*+FROM+fp_psc+WHERE+CONTAINS(POINT(ra,dec),CIRCLE(210.80225,54.34894,0.01))=1&RESPONSEFORMAT=IPAC_TABLE"\
       https://irsa.ipac.caltech.edu/SIA
       ```
    4. Upload a CSV file with RA and Dec ranges defined by columns ra1, ra2, dec1, and dec2.
       Find the closest Euclid QR1 MER images for each source in the file and
       return the results in IPAC table format.

       ```

       curl -o results.tbl \
         -F "COLLECTION=euclid_DpdMerBksMosaic" \
         -F "POS=RANGE my_table.ra1 my_table.ra2 my_table.dec1 my_table.dec2" \
         -F "UPLOAD=my_table,param:my_file" \
         -F "my_file=@local_dir/source_positions.csv" \
         -F "RESPONSEFORMAT=IPAC_TABLE" \
         https://irsa.ipac.caltech.edu/SIA
       ```

Examples
--------

1. Search for ALLWISE images within 0.01 degrees of ra,dec =
   (164.7, -5.8). Return the result as in
   comma-separated value format.

   ```

               wget -O example1.csv "https://irsa.ipac.caltech.edu/SIA?COLLECTION=wise_allwise&POS=circle+164.7+-5.8+0.01&RESPONSEFORMAT=CSV"
   ```
2. Include 2MASS Allsky images in the query and write the results to an IPAC table.

   ```

               wget -O example2.tbl "https://irsa.ipac.caltech.edu/SIA?COLLECTION=wise_allwise&COLLECTION=twomass_allsky&POS=circle+164.7+-5.8+0.01&RESPONSEFORMAT=IPAC_TABLE"
   ```
3. Restrict the data to have wavelengths between 2 and 5 microns, and write the results to a VO Table.

   ```

               wget -O example3.vot "https://irsa.ipac.caltech.edu/SIA?COLLECTION=wise_allwise&COLLECTION=twomass_allsky&POS=circle+164.7+-5.8+0.01&BAND=2.0e-6+5.0e-6"
   ```

Understanding the Results
-------------------------

The results table identifies all files matching the search parameters of the query. Among these files may be calibrated science images, uncertainty maps, image masks, coverage maps, calibration files, and artifact tables. For some collections (e.g. `twomass_allsky`), multiple rows of a single artifact may be returned if that artifact applies to different images.

As mentioned above, results tables of SIA v2 queries all have the same set of columns no matter what combination of parameters and parameter values are specified in the queries. For detailed information about these columns, visit [https://irsa.ipac.caltech.edu/SIA?MAXREC=0](/SIA?MAXREC=0) and examine the contents of the `<RESOURCE type="results">` section of the VO Table output. It is also instructive to examine the results files from the example queries above, as they demonstrate how certain image metadata are represented by the unified columns here. For example, image metadata describing the name of the filter used in the observation can be found in the column named `energy_bandpassname`.

Downloading Data
----------------

The location for each file is provided in the `access_url` column. When downloading files via most browsers, you will be prompted with a "Save As" dialog box including a suggested file name. This prompt is achieved by means of an HTTP [Content-Disposition](http://www.ietf.org/rfc/rfc2183.txt) header containing the file name suggestion.

Command-line clients for web access, however, typically ignore this header by default. Unless instructed otherwise,
[wget](http://www.gnu.org/software/wget/) will derive a local file name from the URL (including the query string), and [curl](http://curl.haxx.se/) will write to standard out. To obtain shorter file names, one can explicitly specify a local file name:

wget
:   ```

    wget -O file <access_url>
    wget --output-document=file <access_url>
    ```

    For example:

    ```

    wget --output-document=myimage.fits "serverroot/data/wise/allwise/p3am_cdd/16/1640/1640m061_ac51/1640m061_ac51-w1-int-3.fits"
    ```

curl
:   ```

    curl -o file <access_url>
    curl --output file <access_url>
    curl <access_url> > file # uses the shell to redirect standard out to a file
    ```

One can also force both [wget](http://www.gnu.org/software/wget/) and [curl](http://curl.haxx.se/) to honor the file name
suggestion in the [Content-Disposition](http://www.ietf.org/rfc/rfc2183.txt) header:

wget
:   ```

    wget --content-disposition <access_url>
    ```

    For example:

    ```

    wget --content-disposition "serverroot/data/wise/allwise/p3am_cdd/16/1640/1640m061_ac51/1640m061_ac51-w1-int-3.fits"
    ```

    will download the remote file to a local file named 1640m061\_ac51-w1-int-3.fits.
    Note that the --content-disposition option is only available in
    [wget](http://www.gnu.org/software/wget/) versions 1.11.x or later.

curl
:   Using the -J/--remote-header-name option in conjunction with
    -O/--remote-name does the trick:

    ```

    curl -O -J "serverroot/data/wise/allwise/p3am_cdd/16/1640/1640m061_ac51/1640m061_ac51-w1-int-3.fits"
    ```

Getting Help
------------

If you've run into a problem, think you've found a bug, or simply have questions, please contact
[IRSA User Support](https://irsa.ipac.caltech.edu/docs/help_desk.html).

## Links found on page

- http://curl.haxx.se/
- http://irsa.ipac.caltech.edu/applications/DDGEN/Doc/ipac_tbl.html
- http://json.org
- http://www.gnu.org/software/wget/
- http://www.ietf.org/rfc/rfc2183.txt
- http://www.ivoa.net
- http://www.ivoa.net/Documents/VOTable/
- http://www.ivoa.net/documents/ObsCore/index.html
- http://www.ivoa.net/documents/SIA/
- http://www.sqlite.org/
- https://astroquery.readthedocs.io/en/latest/ipac/irsa/irsa.html#image-and-spectra-searches
- https://fits.gsfc.nasa.gov/
- https://irsa.ipac.caltech.edu/SIA?MAXREC=0
- https://irsa.ipac.caltech.edu/docs/help_desk.html
- https://irsa.ipac.caltech.edu/docs/program_interface/TAP.html
- https://irsa.ipac.caltech.edu/docs/program_interface/api_images.html#other
- https://www.hdfgroup.org/
- https://www.oracle.com/database/index.html
- https://www.postgresql.org/
