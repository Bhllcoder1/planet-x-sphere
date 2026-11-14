---
source: https://irsa.ipac.caltech.edu/docs/program_interface/TAP.html
fetched: 2026-11-14
status: 200
---

IRSA VO TAP Documentation

IRSA VO Table Access Protocol (TAP) Instructions
------------------------------------------------

IRSA offers program-friendly interfaces to all of its catalogs. An
Application Programming Interface (API) allows access to IRSA catalogs
(within a script or on the command line) without the need to go
through a browser. IRSA accepts three kinds of APIs for catalogs [(**more on IRSA's Catalog Search APIs**).](https://irsa.ipac.caltech.edu/docs/program_interface/api_catalogs.html)

This page describes IRSA's implementation of the International Virtual Observatory Alliance ([**IVOA**](https://www.ivoa.net/))'s Table Access
Protocol, or [**TAP**](https://www.ivoa.net/documents/TAP). IRSA's TAP supports many features of IVOA's Astronomical Data
Query
Language [**ADQL**](https://www.ivoa.net/documents/latest/ADQL.html).
It facilitates a rich variety of customized searches, including cone,
box, polygon, and all-sky, and it offers the option of uploading a
table containing multiple positions so that the user can search
multiple sky regions in a single query. The output can be returned in
various formats,
including  [**VO
Table**](https://www.ivoa.net/documents/VOTable),  [**IPAC
table**](https://irsa.ipac.caltech.edu/applications/DDGEN/Doc/ipac_tbl.html), and FITS.

**Page contents:**

* [TAP services from Python](#tap_python)
* [TAP services from the command line](#tap_cmdline)
* [Catalog & column names](#cats_cols)
* [Constructing a TAP query](#construct_query)
* [Examples](#examples)

Using IRSA TAP services from Python
-----------------------------------

An introduction to running TAP queries from Python is
available [here](astropy_TAP.html), and various additional
examples can be found in the [IRSA Python
Notebook Tutorials](/docs/notebooks/). Once you are set up to run TAP
queries from Python, you can return to this page for a guide to
customizing queries to meet your specific search requirements.

Using IRSA TAP services from the command line
---------------------------------------------

Below are examples of a cone search with center at (RA=66.76957 deg, Dec=26.10453 deg)
and radius 0.01 deg against the 2MASS Point Source Catalog ("fp\_psc") using the commonly available
command-line tools [**curl**](https://curl.haxx.se/) and [**wget**](https://www.gnu.org/software/wget/).
Coordinates and angular sizes are always measured in decimal degrees.
The results table, which will be written to the file "out.xml", is by default in VOTable format.

Using curl:

* ***curl -o out.xml** "https://irsa.ipac.caltech.edu/TAP/sync?QUERY=SELECT+\*+FROM+fp\_psc+WHERE+CONTAINS(POINT(ra,dec),CIRCLE(66.76957,26.10453,0.01))=1"*

Using wget:

* ***wget -O out.xml** "https://irsa.ipac.caltech.edu/TAP/sync?QUERY=SELECT+\*+FROM+fp\_psc+WHERE+CONTAINS(POINT(ra,dec),CIRCLE(66.76957,26.10453,0.01))=1"*

Curl is preferred as it handles table upload more easily. Note the "+"
signs which indicate spaces within a URL. These will
be omitted in the descriptions below for clarity. They are not
needed when using the ["-F" option](https://curl.se/docs/manpage.html#--form), as in [examples](#examples) 8 and 9 below.

A detailed description of the full query syntax is given below, but
to help the reader get started, we give here a heuristic description
of the query.

- The beginning of the URL, from "https" through "TAP/sync?",
  specifies the TAP service being queried.
- The QUERY begins with the instruction to SELECT all columns ("\*")
  FROM the catalog whose ID string is "fp\_psc". This clause indicates
  how the **columns** of the
  results set are related to the columns of the catalog. (As can be
  found by following the links in the [Catalog &
  column names](#cats_cols) section below, this catalog is the 2MASS Point
  Source Catalog.)
- The QUERY then specifies a constraint (WHERE) that determines
  which **rows** from the
  catalog contribute to the results table. In this case, the
  constraint is a geometric one (CONTAINS) that specifies a circular
  region (CIRCLE) on the sky with center at (RA=66.76957 deg,
  Dec=26.10453 deg) and radius of 0.01 degrees. The CONTAINS function
  returns 1, meaning "true", when evaluated at a POINT that is within
  the specified CIRCLE. This function is evaluated at POINTs
  corresponding to the RA and Dec values (the values of the "ra" and
  "dec" columns) of every row in the catalog, and the "=1" means that
  only those rows for which the function value is 1 contribute to the
  results table.
- No value is specified for the FORMAT parameter, so the results will
  be returned in VOTable format. The FORMAT parameter is described in
  the [FORMAT](#format) section below (see
  also [example 2](#examples)).

A detailed description of the syntax can be found in
the [Constructing a TAP query](#construct_query) section
and several examples of various types of queries are given in
the [Examples](#examples) section. All of these queries
are presented as URLs that can be run and downloaded from the
command line. Alternatively, all of these queries can also be run
from Python as described in the [Using IRSA TAP
services from Python](#tap_python) section above.

How do I get IRSA's Catalog Names and Column Names?
---------------------------------------------------

Ready to go and just need the IRSA catalog and/or column names? See
the sections labeled "[table](#table)" and
"[columns](#columns)" in blue, below. You can also explore
the table and column names interactively
[here](/applications/Gator).

Constructing a TAP Query
------------------------

The syntax for the TAP query depends upon whether you make a
synchronous or asynchronous query. A successful synchronous query is
straightforward; it runs until it has obtained the results you
requested and then provides you with those results. This form of query
either completes or times out within 5 minutes and is suitable for
simple searches of small areas. An asynchronous query, in contrast,
lasts only long enough to kick off a background job and provide you with
links you can click to monitor the progress of that job and
eventually to retrieve the results. This form of query will not
directly provide the results to you. The timeout limit for
asynchronous queries is 3 days.

For both forms of the TAP query,
the main parameters are
**[QUERY](#query)**, **[FORMAT](#format)** (optional), and
**[UPLOAD](#upload)** (for table upload), described
below.

**For synchronous calls (small-area searches):**

* *https://irsa.ipac.caltech.edu/TAP/**sync**?QUERY=**[{QUERY}](#query)**&FORMAT=**[{FORMAT}](#format)**&UPLOAD=**[{UPLOAD}](#upload)***

**For asynchronous calls (large searches):**

* *https://irsa.ipac.caltech.edu/TAP/**async**?QUERY=**[{QUERY}](#query)**&FORMAT=**[{FORMAT}](#format)**&UPLOAD=**[{UPLOAD}](#upload)***

You will be given a web address that you can use to check on
your job. For example, if the address is:

* *https://irsa.ipac.caltech.edu/TAP/async/35*

Then you can check the progress of your job by checking the
"phase" associated with this job:

* *https://irsa.ipac.caltech.edu/TAP/async/35/phase*

This will return either QUEUED, EXECUTING, COMPLETED, ERROR, or ABORT. When the job is completed, you get your results like this:

* *https://irsa.ipac.caltech.edu/TAP/async/35/results/result*

---

### QUERY:

The QUERY clause follows this pattern:

QUERY=SELECT **[{columns}](#columns)** FROM **[{table}](#table)** WHERE **[{geometric constraint}](#geometricconstraint)** AND (**[{sql constraints}](#sqlconstraints)**) **[{order by}](#orderby)****[{group by}](#groupby)** **[{having}](#having)**

In particular,

- the query contains at most one geometric constraint.
- the operator between geometric constraint and sql constraints, if both exist, is 'AND'.
- multiple sql constraints are grouped together and enclosed within parentheses.

|  |  |
| --- | --- |
| **keyword** | **description** |
| **columns** | Comma-separated list of column names, or functions of columns to be returned.  Supported functions are those that are both defined in [ADQL 2.0](https://www.ivoa.net/documents/ADQL/2.0) and implemented by database software providers Oracle (IRSA catalogs) or PostgreSQL (other IRSA tables).  **Examples (just for illustration -- don't run without constraints):**  1. Output all columns.   * *SELECT \**   2. Output selected columns.   * *SELECT ra,dec,j\_m*   3. Output the date of observation from the main 2MASS catalog, but round to the nearest day.   * *SELECT round(jdate, 0) FROM fp\_psc*   4. Rename the output column returned by "round(jdate,0)" to rounded\_jdate.   * *SELECT round(jdate, 0) as rounded\_jdate FROM fp\_psc*   5. Prefix the ra with the table name. This is advisable when performing operations on multiple tables.   * *SELECT fp\_psc.ra FROM fp\_psc*   6. Limit the number of rows in the results table. This can be done either with a "SELECT TOP" command within the "QUERY" clause or by means of the [MAXREC](#maxrec) parameter. If both "TOP" and "MAXREC" are present, the number of rows returned is no more than the minimum of the two limits. If the value of "MAXREC" is less than the number of records matching the search criteria, the value of the "QUERY\_STATUS" element of a votable response will be OVERFLOW.   * *QUERY=SELECT+TOP+5+ra+FROM+fp\_psc*  * *QUERY=SELECT+ra+FROM+fp\_psc&MAXREC=5*   **Note on Column Names:** To get the available column names, say for the catalog "fp\_psc" (retrieving the catalog table name is described in the following section):   * *curl -o out.xml "https://irsa.ipac.caltech.edu/TAP/sync?QUERY=SELECT+\*+FROM+TAP\_SCHEMA.columns+WHERE+table\_name='fp\_psc'"*   Column names can also be browsed interactively [here](/applications/Gator/). |
| **table** | Specifies the catalog table to search.  **Example (just for illustration):**  Select all columns from the COSMOS Photometry catalog.   * *SELECT \* FROM cosmos\_phot*   **Note on Catalog Table Names:** To obtain the string needed for the "table" parameter, you can download a VOTable of IRSA's available catalogs. The string needed is in the column labeled "table\_name". There is also a useful column called "description".   * *curl -o out.xml "https://irsa.ipac.caltech.edu/TAP/sync?QUERY=SELECT+\*+FROM+TAP\_SCHEMA.tables"*     **Some Popular Catalogs**     |  |  | | --- | --- | | **table\_name** | **Description** | | **allwise\_p3as\_psd** | AllWISE Source Catalog | | **fp\_psc** | 2MASS Point Source Catalog | | **glimpse\_s07** | GLIMPSE I Spring 07 Catalog (Spitzer) | | **cosmos\_phot** | COSMOS Photometry Catalog | | **iraspsc** | IRAS Point Source Catalog | |
| **geometric constraint** | The geometric constraint is typically a CONTAINS function (= 1 for true) operating on a POINT and a shape. Note that only a single geometric constraint is supported per query. Please see [tip](#tip) below.  The POINT's two elements must be (possibly qualified) names of columns of an IRSA catalog, or aliases of such columns.  There are three supported shape functions: CIRCLE, BOX, and POLYGON. All coordinates and angular sizes are in decimal degrees. Shape arguments may be constants or names/aliases of columns. Binary arithmetic expressions, i.e. "A op B" where "A" and "B" are constants and "op" is one of '+', '-', '\*', and '/', may be supplied in many places where constants are expected. Depending on how the call is made, a '+' might have to be encoded as "%2B". For more examples of how common characters can be encoded in URLs, see the table on [this page](/docs/program_interface/objstr.html).  **Note:** In the case of POLYGON, the region searched is the convex hull of the supplied coordinates. This is a departure from the ADQL specification, which calls for support of arbitrary polygons.  As of ADQL version 2.1, specifying a coordinate system in geometry constructors is [deprecated](https://www.ivoa.net/documents/ADQL/20180112/PR-ADQL-2.1-20180112.html#tth_sEc4.2.4). IRSA catalogs use equatorial coordinates with ra and dec usually consistent with the J2000 system. If another coordinate system such as ICRS was used in the catalog creation, the search will assume the search parameters are ICRS.  Circle  This requires the coordinates of the center and the radius. A 1-degree cone search around M101 would be:   * *SELECT \* FROM fp\_psc WHERE CONTAINS(POINT(ra,dec),CIRCLE(210.80225,54.34894,1.0))=1*   Box  This requires the coordinates of the center of the box, the width, and the height. The box will be aligned with the coordinate system. A 1 degree by 1 degree box around M101 would be:   * *SELECT \* FROM fp\_psc WHERE CONTAINS(POINT(ra,dec),BOX(210.80225,54.34894,1.0,1.0))=1*   Polygon  This requires the concatenated coordinates of the vertices of the polygon. A triangle search around M101 would be:   * *SELECT \* FROM fp\_psc WHERE CONTAINS(POINT(ra,dec),POLYGON(209.80225,53.34894,209.80225,55.34894,211.80225,54.34894))=1*   **Tip:**  As mentioned above, no more than one geometric constraint is supported per query. Therefore, queries like the one below, in which the user tries to query two locations on the sky at once, will not succeed. Users wishing to query more than one location on the sky must submit multiple queries. For example, this query will fail...   * *SELECT \* FROM fp\_psc WHERE (CONTAINS(POINT(ra,dec),CIRCLE(210.80225,54.34894,1.0))=1 OR CONTAINS(POINT(ra,dec),CIRCLE( 110.52208,44.49843,1.0))=1)*   ...but the combined results of these two queries will provide the desired data:   * *SELECT \* FROM fp\_psc WHERE CONTAINS(POINT(ra,dec),CIRCLE(210.80225,54.34894,1.0))=1*  * *SELECT \* FROM fp\_psc WHERE CONTAINS(POINT(ra,dec),CIRCLE(110.52208,44.49843,1.0))=1* |
| **sql constraints** | SQL constraints are filters expressible in ADQL 2.0.  **Note:** If the WHERE clause contains a geometric constraint as well as multiple SQL constraints, the SQL constraints must be grouped together and enclosed within parenthesis.  **Examples:**  Query the 2MASS Point Source Catalog, and return all columns for records that fall within a certain time range.   * *SELECT \* FROM fp\_psc WHERE (jdate>=2451500 and jdate<=2451700)*   Perform a 1-degree cone search around M101, restricting to records that fall within a certain time range.   * *SELECT \* FROM fp\_psc WHERE CONTAINS(POINT(ra,dec),CIRCLE(210.80225,54.34894,1.0))=1 and (jdate>=2451500 and jdate<=2451700)* |
| **order by** | A comma-separated list of column names specifying which to use for sorting the output table rows, in order of priority.  **Example:**  Query the 2MASS Point Source Catalog. Return all columns for records within a specified time range, and order the results by the observation date. If multiple records have identical observation dates, then order by right ascension.   * *SELECT \* FROM fp\_psc WHERE (jdate>=2451500 and jdate<=2451700) order by jdate, ra* |
| **group by** | Groups the returned records by the specified columns, which allows you to perform functions on that group. **Example:**  Query the 2MASS Point Source Catalog. Return all columns for records within a specified time range, and group the records by date.   * *SELECT \* FROM fp\_psc WHERE (jdate>=2451500 and jdate<=2451700) group by jdate* |
| **having** | Constrains selections after an aggregate function such as "group by". Quicker than a WHERE since it acts on the smaller group. **Example:**  Query the 2MASS Point Source Catalog. Return all columns for records within a specified time range, group the records by date, then select those in the group with a certain brightness.   * *SELECT \* FROM fp\_psc WHERE (jdate>=2451500 and jdate<=2451700) group by jdate having j\_m < 8*   Note: Other ADQL 2.0 functions may also be implemented, but this page is not meant to be a complete description of SQL functions. |

---

### MAXREC:

Limit the number of rows in the results table. This can be done either with a "SELECT TOP" command within the "QUERY" clause (please see [columns](#columns)) or by means of the "MAXREC" parameter. Only "MAXREC" triggers the OVERFLOW indicator.

* *QUERY=SELECT+ra+FROM+fp\_psc&MAXREC=5*

To retrieve only the highest ranked N rows meeting the search criteria, specify both (1) a ranking or sort order (via SQL's "ORDER BY" keyword), and (2) the limit N (via either SQL's "SELECT TOP" or the "MAXREC" parameter).

* *QUERY=SELECT+ra,dec,DISTANCE(POINT(ra,dec),POINT(210.80225,54.34894))+as+my\_dist+FROM+fp\_psc+WHERE+CONTAINS(POINT(ra,dec),CIRCLE(210.80225,54.34894,1.0))=1+ORDER+BY+my\_dist,ra&MAXREC=10&FORMAT=HTML*

* *QUERY=SELECT+TOP+10+ra,dec,DISTANCE(POINT(ra,dec),POINT(210.80225,54.34894))+as+my\_dist+FROM+fp\_psc+WHERE+CONTAINS(POINT(ra,dec),CIRCLE(210.80225,54.34894,1.0))=1+ORDER+BY+my\_dist,ra&FORMAT=HTML*

---

### FORMAT:

The TAP service will by default return a VOTable. Other formats may be requested via the FORMAT keyword. The supported output formats are:

|  |  |
| --- | --- |
| **keyword** | **description** |
| VOTABLE | VO Table - a type of XML |
| CSV | Comma Separated Value table |
| TSV | Tab Separated Value table |
| IPAC\_TABLE | IPAC Table Format |
| HTML | HyperText Markup Language |
| FITS | Flexible Image Transport System Binary Table |

---

### UPLOAD:

UPLOAD={**[name](#name)**},{**[URI](#URI)**}

|  |  |
| --- | --- |
| **keyword** | **description** |
| **name** | The name of the table within TAP for the purposes of the present query (e.g. my\_favorite\_quasars). Prefix this name with TAP\_UPLOAD to refer to columns in the query (e.g. TAP\_UPLOAD.my\_favorite\_quasars.ra). See Example 8 below.  The uploaded table may be in VOTABLE, IPAC\_TABLE, TSV, or CSV format. |
| **URI** | The location of the table to upload. If it is an http or https URL, then the TAP service will attempt to fetch it over the network. A file from your local host may be added to the query as multipart/form-data using a `file`-type input element such as the [-F option](https://curl.se/docs/manpage.html#--form) of curl. Use `param:tag` as the URI, where `tag` is a name of your choosing that you will use in a separate `-F "tag=@path_to_file"` argument to curl. See Example 8 below. |

---

Examples
--------

1. **Cone Search**

   * *https://irsa.ipac.caltech.edu/TAP/sync?QUERY=SELECT+\*+FROM+fp\_psc+WHERE+CONTAINS(POINT(ra,dec),CIRCLE(210.80225,54.34894,1.0))=1*
2. **Cone Search returning a FITS table file**

   * *https://irsa.ipac.caltech.edu/TAP/sync?QUERY=SELECT+\*+FROM+fp\_psc+WHERE+CONTAINS(POINT(ra,dec),CIRCLE(210.80225,54.34894,1.0))=1&format=fits*
3. **Cone Search with only ra, dec, and date rounded to the nearest day**

* *https://irsa.ipac.caltech.edu/TAP/sync?QUERY=SELECT+ra,dec,round(jdate,0)+as+rounded\_jdate+FROM+fp\_psc+WHERE+CONTAINS(POINT(ra,dec),CIRCLE(210.80225,54.34894,1.0))=1*

4. **Cone Search with a date filter, ordered by date**

   * *https://irsa.ipac.caltech.edu/TAP/sync?QUERY=SELECT+\*+FROM+fp\_psc+WHERE+CONTAINS(POINT(ra,dec),CIRCLE(210.80225,54.34894,1.0))=1+and+(jdate>=2451500+and+jdate<=2451700)+order+by+jdate*
5. **Cone Search with a distance column, ordered by distance (measured in arcsec)**

   * *https://irsa.ipac.caltech.edu/TAP/sync?QUERY=SELECT+ra,dec,DISTANCE(POINT(ra,dec),POINT(210.80225,54.34894))+as+my\_dist+FROM+fp\_psc+WHERE+CONTAINS(POINT(ra,dec),CIRCLE(210.80225,54.34894,1.0))=1+ORDER+BY+my\_dist,ra,dec*
6. **Box Search**

   * *https://irsa.ipac.caltech.edu/TAP/sync?QUERY=SELECT+\*+FROM+fp\_psc+WHERE+CONTAINS(POINT(ra,dec),BOX(210.80225,54.34894,1.0,1.0))=1*
7. **Polygon Search**

   * *https://irsa.ipac.caltech.edu/TAP/sync?QUERY=SELECT+\*+FROM+fp\_psc+WHERE+CONTAINS(POINT(ra,dec),POLYGON(209.80225,53.34894,209.80225,55.34894,211.80225,54.34894))=1*
8. **Upload local file**

   If you upload a VOTable "upload.vo" with columns "ra" and "dec",
   this command will run a match for each row of your table against
   objects in the 2MASS catalog. Note that the POINT clause refers to
   columns from the catalog and the CIRCLE clause to columns from the
   uploaded table.

   * *curl -o fp\_psc.xml -F "UPLOAD=my\_table,param:table" -F "table=@upload.vo" -F "QUERY=SELECT fp\_psc.ra, fp\_psc.dec FROM fp\_psc WHERE CONTAINS(POINT(ra,dec), CIRCLE(TAP\_UPLOAD.my\_table.ra, TAP\_UPLOAD.my\_table.dec, 0.01)) =1" https://irsa.ipac.caltech.edu/TAP/sync*

   If you upload an IPAC table "upload.tbl" with columns "my\_ra2",
   "my\_dec2", and "my\_radius2", this command will run a match for each row of your table
   against objects in the 2MASS catalog, returning an IPAC table.

   * *curl -o fp\_psc.tbl -F "UPLOAD=my\_table,param:table\_param" -F "table\_param=@upload.tbl" -F "FORMAT=IPAC\_TABLE" -F "QUERY=SELECT fp\_psc.ra, fp\_psc.dec FROM fp\_psc WHERE CONTAINS(POINT(ra,dec), CIRCLE(TAP\_UPLOAD.my\_table.my\_ra2, TAP\_UPLOAD.my\_table.my\_dec2, TAP\_UPLOAD.my\_table.my\_radius2)) =1" https://irsa.ipac.caltech.edu/TAP/sync*

   Note that the name of the uploaded table is omitted from the FROM
   clause in the previous examples. This is a supported shortcut, but if
   you wish to introduce an alias for the upload table, you must include
   the uploaded table's name in the FROM clause to do so.

   * *curl -o fp\_psc.tbl -F "UPLOAD=my\_table,param:my\_param" -F "my\_param=@upload.tbl" -F "FORMAT=IPAC\_TABLE" -F "QUERY=SELECT cat\_table.ra, cat\_table.dec FROM TAP\_UPLOAD.my\_table AS my\_table, fp\_psc AS cat\_table WHERE CONTAINS(POINT(ra,dec), CIRCLE(my\_table.my\_ra, my\_table.my\_dec, 0.01)) =1" https://irsa.ipac.caltech.edu/TAP/sync*
9. **Upload remote file**
   This will run a simple cone search on WISE and pipe it directly into a cross match with 2MASS.
   * *curl -o fp\_psc.xml -F "UPLOAD=my\_table,https://irsa.ipac.caltech.edu/SCS?table=allwise\_p3as\_psd&RA=210.80225&DEC=54.34894&SR=0.01" -F "QUERY=SELECT fp\_psc.ra, fp\_psc.dec FROM fp\_psc WHERE CONTAINS(POINT(ra,dec), CIRCLE(TAP\_UPLOAD.my\_table.ra, TAP\_UPLOAD.my\_table.dec, 0.01)) =1" https://irsa.ipac.caltech.edu/TAP/sync*
10. **Asynchronous Cone Search**

    Submit the query, using curl's "-v" option.

    * *curl -v "https://irsa.ipac.caltech.edu/TAP/async?QUERY=SELECT+\*+FROM+fp\_psc+WHERE+CONTAINS(POINT(ra,dec),CIRCLE(210.80225,54.34894,1.0))=1"*

    The output should include a line like:

    * *> Location: https://irsa.ipac.caltech.edu/TAP/async/10*

    Check the progress of the job.

    * *curl "https://irsa.ipac.caltech.edu/TAP/async/10/phase"*

    This query completes fairly quickly, so you should see "COMPLETED". To get the results:

    * *curl -o fp\_psc.xml "https://irsa.ipac.caltech.edu/TAP/async/10/results/result"*

## Links found on page

- https://curl.haxx.se/
- https://curl.se/docs/manpage.html#--form
- https://irsa.ipac.caltech.edu/applications/DDGEN/Doc/ipac_tbl.html
- https://irsa.ipac.caltech.edu/applications/Gator
- https://irsa.ipac.caltech.edu/applications/Gator/
- https://irsa.ipac.caltech.edu/docs/notebooks/
- https://irsa.ipac.caltech.edu/docs/program_interface/api_catalogs.html
- https://irsa.ipac.caltech.edu/docs/program_interface/astropy_TAP.html
- https://irsa.ipac.caltech.edu/docs/program_interface/objstr.html
- https://www.gnu.org/software/wget/
- https://www.ivoa.net/
- https://www.ivoa.net/documents/ADQL/2.0
- https://www.ivoa.net/documents/ADQL/20180112/PR-ADQL-2.1-20180112.html#tth_sEc4.2.4
- https://www.ivoa.net/documents/TAP
- https://www.ivoa.net/documents/VOTable
- https://www.ivoa.net/documents/latest/ADQL.html
