---
source: https://irsa.ipac.caltech.edu/applications/MOST/instructions.html
fetched: 2026-11-14
status: 200
---

MOST - Moving Object Search Tool Instructions

---

MOST - Moving Object Search Tool Instructions
---------------------------------------------

The Moving Object Search Tool (MOST) computes the orbit of a solar
system object and searches for images that covered the object's
predicted positions in select image archives housed by IRSA. Aids to
visualization include an orbit plot and links to display the FITS images.
It can serve as a "precovery" tool,
determining whether newly discovered objects were previously observed.

Also available is a
[Program Interface](/applications/MOST/MOSTProgramInterface.html) to MOST.

Note: A Python notebook showing how to interact with some of the MOST capabilities is available: [Python notebook](https://caltech-ipac.github.io/irsa-tutorials/most-queries).

#### Image Datasets and Search Parameters

MOST can query all phases of the WISE/NEOWISE
mission (select "wise\_merge" under **Image Dataset** for all),
Spitzer, PTF, ZTF, SOFIA, SPHEREx, and 2MASS. If the **Observation** time ranges
are left blank, it will use the entire length of the mission. This
could be a lengthy search, so **limiting the time range is usually
necessary**. This is especially important for WISE/NEOWISE
(i.e. wise\_merge to MOST) near the ecliptic poles where the coverage
can be very high. When a dataset is selected, an info box will give
information on the time range of the data.

For **Output Mode**, the "Regular" option is recommended. The full
option displays the full ephemeris and other products and requires some
scrolling.

#### Object Input

Solar system objects can be input by name, number, designation, or
NAIF ID number. Name resolution and ephemeris generation for known
objects is done via query to JPL's Horizon database.

There can be name ambiguities. For example, entering "WISE" is a
problem as there were many asteroids and comets discovered by the WISE
mission. Entering "Neptune" is unclear as there are ephemeris files
for both Neptune and the Neptune system barycenter. MOST will deliver
a messsage if there is an ambiguity. The message may contain suggested
NAIF ID's, e.g. "1003094:NID" for comet 317P/WISE or "899:NID" for
Neptune. NAIF ID's may be input directly as well. In a few cases,
there are satellites and asteroids with the same name, and you may
distinguish them by, e.g. "Europa:SAT" and "Europa:AST".

|  |
| --- |
| **EXAMPLES OF OBJECT INPUT:**   Asteroid 324 Bamberga:   "Bamberga" or "324"  Periodic comet P/29 Schwassmann-Wachmann 1:   "29P" or "P/29" (but not P29)  Non-periodic comet 337P/WISE:   "C/20010 N1"  Titan:   "Titan"  Neptune:   "899:NID" |

The ephemeris can also be calculated for comets or asteroids using
orbital elements supplied by the user, either individually or in the
Minor Planet Center (MPC) one-line format
([further information](/applications/Gator/GatorAid/irsa/moving.html)). But object name/number
input is best, as it will query JPL Horizons to get the osculating
orbital elements closest in time to the observations.

#### Additional Data Requests

Clicking on **Create Fits and DS9 Region Files Tarballs** will
pack the retrieved images and markers for the moving object (in DS9
region format) into separate tarballs. The image tarball could be
quite large for a large search, so leave this option off and see how
many images there will be first.

#### Output

MOST streams results to the browser as it goes, so don't exit the
output page until it completes.

The Regular output displays a plot of the orbital path, and a
table ("Images with a Matched Object Position") with the matched
images along with object parameters at the time. The table that is
displayed has links to download the images individually or display
them in the IRSA Viewer. However if the data have access
restrictions, e.g. ZTF, this will only work for authorized users who
have logged into the browser session. The display table columns are
described below.

**Column Key for Final Table**

| Column | Description |
| --- | --- |
| **Download/View** | Links to download or view the data. |
| **DS9 File** | Markers for the moving object in DS9 "region" format. |
| **Image ID** | A unique identifier for the image data, not necessarily the image file name. |
| **date\_obs** | Date (UTC) of the observation. |
| **time\_obs** | Time (UTC) of the midpoint of the observation. |
| **mjd\_obs** | Modified Julian Date (days) of the midpoint of the observation. |
| **ra\_obs** | Ephemeris prediction of the object's right ascension (deg, J2000). |
| **dec\_obs** | Ephemeris prediction of the object's declination (deg, J2000). |
| **r** | Heliocentric distance of the object (AU). |
| **Δ** | Geocentric distance of the object (AU). |
| **dist\_ctr** | Projected distance of the object from the center of the image (deg). |
| **phase** | Sun-Object-earth angle (deg). |
| **vmag** | Estimate of visual magnitude (from Horizons). |

An intermediate table, available in the Full output or via a link
called Image Metadata with a Matched Object Position, has the same
information as the final table and additional metadata from the
dataset. The keywords are described in the table
below and further information for some can be found in these links: [WISE/NEOWISE](http://wise2.ipac.caltech.edu/docs/release/allsky/expsup/sec2_4i.html), [2MASS](https://www.ipac.caltech.edu/2mass/releases/allsky/doc/sec2_4a.html), [PTF](https://irsa.ipac.caltech.edu/onlinehelp/ptf/#id=overview), [ZTF](https://irsa.ipac.caltech.edu/onlinehelp/ztf/#id=overview), and [Spitzer](https://sha.ipac.caltech.edu/applications/Spitzer/SHA/help/doc/api.html).

**Additional Columns in "Image Metadata with a Matched Object Position" Table**

| Column | Description |
| --- | --- |
| **General** | |
| **ra1, dec1, ra2, dec2 etc.** | Right ascension and declination of the 4 corners of the image (deg, J2000) |
| **match** | match = 1 indicates a matched image (added by MOST) |
| **WISE/NEOWISE** | |
| **crpix1, crpix2** | Center of image (pixels) |
| **crval1, crval2** | Center of image (deg, J2000) |
| **equinox** | Equinox of coordinates |
| **band** | WISE band number; 1 (3.4 microns), 2 (4.6 microns), 3 (12 microns), 4 (22 microns) |
| **scan\_id** | Identification of pole-to-pole orbit scan |
| **date\_obs** | Date and time of mid-point of frame observation, UTC |
| **mjd\_obs** | Modified Julian Date of mid-point of frame observation, UTC |
| **dtanneal** | Elapsed time in seconds since the last anneal |
| **moon\_sep** | The angular distance from the frame center to the Moon (deg) |
| **saa\_sep** | The angular distance from the frame center to South Atlantic Anomaly (SAA) boundary (deg) |
| **qual\_frame** | This integer indicates the quality score value for the Single-exposure image frameset, with values of 0 (poor quality), 5, or 10 (high quality) |
| **image\_set** | image\_set = 4 for 4band, 3 for 3band, 2 for 2band, and 6, 7 etc. for NEOWISE-R year 1, 2 etc. |
| **2MASS** | |
| **ordate** | UT date of reference (start of operations for the night) |
| **hemisphere** | N or S hemisphere |
| **scanno** | Nightly scan number |
| **fname** | FITS file name |
| **ut\_date** | UT date of scan (YYMMDD) |
| **ut** | UT time of scan (HH:MM:SS.SSS) |
| **telname** | Telescope location - Hopkins or CTIO |
| **mjd** | Modified Julian Date of observation |
| **ds** | ds = full for 2mass |
| **PTF** | |
| **obsdate** | Observation UT date/time YYYY-MM-DD HH:MM:SS.SSS |
| **obsmjd** | Modified Julian Date of observation |
| **nid** | Night database ID |
| **expid** | Exposure database ID |
| **ccdid** | CCD number (0...11) |
| **rfilename** | Raw-image filename |
| **pfilename** | Processed-image filename |
| **ZTF** | |
| **obsdate** | Observation UT date/time YYYY-MM-DD HH:MM:SS.SS |
| **obsjd** | Julian Date of observation (days) |
| **filefracday** | Observation date with fractional day YYYYMMDDdddddd |
| **field** | ZTF field number |
| **ccdid** | CCD number (1...16) |
| **qid** | Detector quadrant ID (1...4) |
| **rcid** | Readout channel ID (0...63) |
| **fid** | Filter ID |
| **filtercode** | Filter name (abbreviated) |
| **pid** | Science product ID |
| **nid** | Night ID |
| **expid** | Exposure ID |
| **itid** | Image type ID |
| **imgtypecode** | Single letter image type code |
| **Spitzer** | |
| **reqkey** | Spitzer Astronomical Observation Request number |
| **bcdid** | Post Basic Calibrated Data ID (Level 2 product search) |
| **reqmode** | Spitzer Astronomical Observation Request type |
| **wavelength** | Bandpass ID |
| **minwavelength** | Min wavelength (microns) |
| **maxwavelength** | Max wavelength (microns) |
| **time** | UT time of observation |
| **exposuretime** | Exposure time (sec) |
| **SOFIA** | |
| **proposal\_id** | SOFIA proposal identifier |
| **observationid** | Unique string for the observation |
| **productid** | File name |
| **planeid** | (internal use only) |
| **target\_name** | Target name |
| **target\_moving** | Positive if moving target |
| **instrument** | SOFIA instrument |
| **ra** | Right ascension (J2000) of the observation in deg |
| **dec** | Declination (J2000) of the observation in deg |
| **start\_date** | Date and time of start of observation, UTC |
| **end\_date** | Date and time of end of observation, UTC |
| **mjd\_start** | Modified Julian Date of start of observation |
| **mjd\_end** | Modified Julian Date of end of observation |
| **exposure\_time** | Exposure time in sec |
| **uri** | Path to file |
| **SPHEREx** | |
| **proposal\_id** | (currently null) |
| **observationid** | Unique string for the observation |
| **productid** | File name |
| **planeid** | (internal use only) |
| **target\_name** | Target name |
| **target\_moving** | Positive if moving target |
| **instrument** | SPHEREx detector |
| **ra** | Right ascension (J2000) of the observation in deg |
| **dec** | Declination (J2000) of the observation in deg |
| **start\_date** | Date and time of start of observation, UTC |
| **end\_date** | Date and time of end of observation, UTC |
| **mjd\_start** | Modified Julian Date of start of observation |
| **mjd\_end** | Modified Julian Date of end of observation |
| **exposure\_time** | Exposure time in sec |
| **uri** | Path to file |

  
Back to [Main Page](/applications/MOST).

## Links found on page

- http://wise2.ipac.caltech.edu/docs/release/allsky/expsup/sec2_4i.html
- https://caltech-ipac.github.io/irsa-tutorials/most-queries
- https://irsa.ipac.caltech.edu/applications/Gator/GatorAid/irsa/moving.html
- https://irsa.ipac.caltech.edu/applications/MOST
- https://irsa.ipac.caltech.edu/applications/MOST/MOSTProgramInterface.html
- https://irsa.ipac.caltech.edu/onlinehelp/ptf/#id=overview
- https://irsa.ipac.caltech.edu/onlinehelp/ztf/#id=overview
- https://sha.ipac.caltech.edu/applications/Spitzer/SHA/help/doc/api.html
- https://www.ipac.caltech.edu/2mass/releases/allsky/doc/sec2_4a.html
