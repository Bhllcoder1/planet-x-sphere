---
source: https://ssd-api.jpl.nasa.gov/doc/sbwobs.html
fetched: 2026-11-14
status: 200
---

SB Observability API

* [![NASA Home](/images/transparent.gif)](https://www.nasa.gov/)
  [![JPL Home](/images/transparent.gif)](http://www.jpl.nasa.gov/)
  [![Caltech Home](/images/transparent.gif)](http://www.caltech.edu/)
* [![Home](/images/logo_gears.png)](/)

* [![Home](/images/api_logo.png)](/)
* * [About](/about/)
  * * [Documents](/doc/)

Small-Body Observability API
============================

**Version: 1.0** (2021 March)  
[change log](#change_log)

The Small-Body Observability API provides a method of determining small-bodies
that would be *optically* observable from a specified topocentric observatory
during the specified night (determined from a specified date) or observable via *radar* or
*radiotelescopes* during a specific time frame, meeting various user-specified constraints.

HTTP Request
------------

GET
`https://ssd-api.jpl.nasa.gov/sbwobs.api`

Example Query URLs
------------------

* `https://ssd-api.jpl.nasa.gov/sbwobs.api?mpc-code=F51&obs-time=2016-07-03` - observable objects from Pan-STARRS 1 (F51) on 2016-07-03.
* `https://ssd-api.jpl.nasa.gov/sbwobs.api?mpc-code=568&obs-time=2016-12-17&vmag-max=22&helio-min=1.5&glat-min=10` - observable objects from the Mauna Kea Observatory on 2016-12-17 with maximum visual magnitude 22, heliocentric range greater than 1.5 au, and minimum galactic latitude of 10 deg.
* `https://ssd-api.jpl.nasa.gov/sbwobs.api?mpc-code=F51&obs-time=2020-06-23&sb-group=neo&sb-kind=a&maxoutput=100&output-sort=vmag` - top 100 observable NEAs from Pan-STARRS 1 (F51) on 2020-06-23 based on their visual magnitude.

Query Parameters
----------------

### Observer Location Parameters

You may specify the observer location on the Earth (topocentric)
using either an MPC observatory code, geodetic coordinates
(latitude, longitude, and altitude) or the parallax.
For topocentric locations, you can specify “optical” or “radio/radar”
where “optical” implies the requirement that the Sun be below the horizon
and “radio/radar” does not.

For optical observations, `optical=true`, you may specify the observing time-period
using a single date/time (anytime when the Sun is down) from which the
start time is taken as the prior sunset time and the stop time is taken
as the following sunrise time.

For radio observations, `optical=false`, you must explicitly specify the observing
start and stop times where the time spanned is less than 24 hours and the
start time is before the stop time. A lower bound on the solar elongation is also required.

Location defined by MPC observatory code:

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| mpc-code | string | *none* | MPC observer location code (radar sites are also supported) |

Location defined by geodetic coordinates:

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| lat | number | *none* | geodetic latitude of observer (degrees, north-postive, [-90, 90]) |
| lon | number | *none* | geodetic latitude of observer (degrees, east-postive, [-180, 180]) |
| alt | number | `0` | altitude above the reference ellipsoid {WGS-84/GPS} (km) |

Location defined by parallax:

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| lon | number | *none* | geodetic latitude of observer (degrees, east-postive, [-180, 180]) |
| dxy | number | *none* | parallax constant perp. to Earth’s spin axis (au x 10^7) |
| dz | number | *none* | parallax constant along Earth’s spin axis (au x 10^7) |

### Observation Constraint Parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| obs-time | string | *none* | [**required**] date/time of the observing night UT (formatted as `YYYY-MM-DD[_hh:mm:ss]`) |
| obs-end | string | *none* | date/time when observation ends (optional, formatted as `YYYY-MM-DD[_hh:mm:ss]`) |
| optical | boolean | `true` | the Sun must be below the horizon |
| elong-min | number | *none* | minimum solar elongation: the angle between the target and the Sun w.r.t. observer, in degrees [0, 180] (**required** for `optical=false`) |
| elong-max | number | *none* | maximum solar elongation: the angle between the target and the Sun w.r.t. observer, in degrees [0, 180] (**required** for `optical=false`) |
| glat-min | number | *none* | minimum angular distance from the galactic plane (degrees, [0, 180]) |
| glat-max | number | *none* | maximum angular distance from the galactic plane (degrees, [0, 180]) |
| elev-min | number | `30` | minimum elevation angle (angle in degrees above the horizons, [0, 90]) [e.g., a value of `30` would exclude objects which never get at least 30-degrees above the horizon] |
| time-min | int | `0` | minimum number of minutes required for an exposure (e.g., `15`) [`0` implies no limit] |
| vmag-min | number | *none* | visual magnitude lower-bound (objects must be at least this bright) |
| vmag-max | number | *none* | visual magnitude upper-bound (objects must be at most this bright) |
| mag-required | boolean | `false` | require magnitude parameters |
| helio-min | number | *none* | limit to objects whose heliocentric distance (au) is at least this value |
| helio-max | number | *none* | limit to objects whose heliocentric distance (au) is at most this value |
| dist-min | number | *none* | limit to objects whose distance (au) from the observer is at least this value |
| dist-max | number | *none* | limit to objects whose distance (au) from the observer is at most this value |

### Output/Format Parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| fmt-ra-dec | boolean | true | use sexagesimal format for R.A. and dec. (if false, use decimal degrees) |
| maxoutput | int | *none* | maximum number of records to be returned |
| output-sort | string | *none* | sort records according to this variable. If `maxoutput` is specified, `output-sort` must be provided to specify how records are selected. Available options are: `name` (object name), `rise` (rise time), `trans` (transit time), `set` (set time), `maxt` (max. observable time), `ra` (right ascension), `dec` (declination), `vmag` (V-magnitude), `helio` (heliocentric range), `topo` (topocentric range), `oes` (solar elongation), `oem` (object-Earth-Moon angle), `glat` (galactic latitude) |
| output-sort-r | boolean | false | sort in descending order |

### SBDB Filter Constraints

Additional constraints on the orbital and physical parameters of the objects are available using the [SBDB Filter](sbdb_filter.html).

### Required Parameters

* observer (observer location) is specified using one of the following forms:
  + valid topocentric MPC 3-character code (e.g., `F51` but never `500` ‘geocentric’), or
  + geodetic coordinates: latitude, longitude, and altitude
    - latitude (`lat`) is specified in decimal degrees (north positive)
    - longitude (`lon`) is specified in decimal degrees (east positive)
    - altitude (`alt`) is specified in decimal kilometers (above the reference ellipsoid {WGS-84/GPS})
  + parallax:
    - geodetic latitude (`lon`) of observer (degrees, east-postive)
    - parallax constant perp. to Earth’s spin axis (`dxy`, au x 10^7)
    - parallax constant along Earth’s spin axis (`dz`, au x 10^7)

**NOTE:** a topocentric observer location must be specified. Geocentric observations are not supported.

* obs-time (date/time of observation)
  + this date/time is used to determine the corresponding night at the specified observer location
  + time (hh:mm:ss) is not necessary in most cases although it may be convenient to specify hours to ensure selection of the desired night

### NEO-Only Mode

To request only NEOs, add the field `sb-group=neo` to the query URL.

Data Output
-----------

> Please **always check** the JSON payload “signature” object for the API “version”.
> If the version does not match the version in this document (at the top),
> there is no guarantee that the format has not changed.
>
> Example "signature" object with "version" value "1.0":
> `"signature":{"version":"1.0","source":"NASA/JPL ... API"}`

A successful run of the SBWOBS code results in details related to the observer location (Summary Data)
and a table of observable objects (Observable Objects)

### Summary Data

These data relate to the specified observer location and date/time.

* Location details:
  + if the observatory code was specified via `mpc-code`, the field `location` contains the observatory or radar site name
  + if the observer location was specified via `lat`, `lon`, `alt`, those three parameters will be available in the JSON output.
* Observer constraints: contains any constraint specified in the “Observation Constraint Parametes” section
* `total_objects` - total number of observable small bodies.
* `shown_objects` - number of observable small bodies shown.
* `obs_constraints` - summary of user-defined observer constraints. Output fields match the fields described in the “Query Parameters” table.
* `sort_by` - (only when `output-sort` is defined) field used to sort observable bodies.
* `obs_night` - light conditions at the requested observation time (only for `optical=true`). The group contains the following fields:
  + `sun_set` - sunset time (UT).
  + `sun_rise` - sunrise time (UT).
  + `sun_set_az` - azimuth of sunset (deg).
  + `sun_rise_az` - azimuth of sunrise (deg).
  + `begin_astronomical` - begin astronomical twilight (UT).
  + `end_astronomical` - end astronomical twilight (UT).
  + `begin_civil` - begin civil twilight (UT).
  + `end_civil` - end civil twilight (UT).
  + `begin_nautical` - begin nautical twilight (UT).
  + `end_nautical` - end nautical twilight (UT).
  + `moon_rise` - Moon rise time (UT).
  + `moon_rise_phase` - Moon rise phase.
  + `moon_set` - Moon set time (UT).
  + `moon_set_phase` - Moon set phase.
  + `transit` - Moon transit time (UT).
  + `transit_phase` - Moon transit phase.
  + `begin_dark` - begin dark time (UT).
  + `mid_dark` - middle dark time (UT).
  + `end_dark` - end dark time (UT).
  + `dark_time` - total dark time duration (hh:mm).
* `sb_constraints` - constraints from the SBDB filter.
* `fields` - column headers for the `data` output array.
* `data` - list of observable objects in array form. Each row corresponds to a different small body and the columns are defined by the `fields` list:
  + Object designation
  + Full name of the object
  + Rise time (UT)
  + Transit time (UT)
  + Set time (UT)
  + Maximum time observable (hh:mm)
  + Right ascension (apparent)
  + Declination (apparent)
  + Visual magnitude
  + Helicentric range (au)
  + Topocentric range (au)
  + Object-Observer-Sun angle (elongation, deg)
  + Object-Observer-Moon angle (deg)
  + Galactic latitude (deg)

Additional notes:

* Rise, Transit, and Set Times are the UT times of each event (shown as “**hh:mm**”, where “**hh**“=hours, “**mm**“=minutes,
  “**\***” indicates the event occurs when not dark, and “**…**” indicates the object never sets while dark). Rise/Set events are relative to the maximum zenith distance and NOT the horizon.
* For comets, a trailing “N”=nuclear magnitude and “T”=total magnitude.

### Example Output

The following query

`https://ssd-api.jpl.nasa.gov/sbwobs.api?sb-kind=a&sb-group=neo&mpc-code=F51&obs-time=2020-06-24&elev-min=30&time-min=10&vmag-max=25&helio-min=0.5&optical=true&fmt-ra-dec=true&mag-required=true`

returns the output:

```
{
   "signature" : {
      "source" : "NASA/JPL Small-Body Observability API",
      "version" : "1.0"
   },
   "location" : "Pan-STARRS 1, Haleakala",
   "obs_constraints" : {
      "elev-min" : "30",
      "fmt-ra-dec" : "true",
      "helio-min" : "0.5",
      "mag-required" : "true",
      "mpc-code" : "F51",
      "obs-time" : "2020-06-24",
      "optical" : "true",
      "time-min" : "10",
      "vmag-max" : "25"
   },
   "obs_night" : {
      "begin_astronomical" : "2020-06-24 14:20",
      "begin_civil" : "2020-06-24 15:20",
      "begin_dark" : "2020-06-24 06:32",
      "begin_nautical" : "2020-06-24 14:50",
      "dark_time" : "07:47",
      "end_astronomical" : "2020-06-24 06:32",
      "end_civil" : "2020-06-24 05:32",
      "end_dark" : "2020-06-24 14:20",
      "end_nautical" : "2020-06-24 06:02",
      "mid_dark" : "2020-06-24 10:26",
      "moon_rise" : "2020-06-24 19:04 ",
      "moon_rise_phase" : "0.15",
      "moon_set" : "2020-06-24 07:42 ",
      "moon_set_phase" : "0.10",
      "sun_rise" : "2020-06-24 15:44",
      "sun_rise_az" : "64.5",
      "sun_set" : "2020-06-24 05:07",
      "sun_set_az" : "295.5",
      "transit" : "2020-06-24 00:54 ",
      "transit_phase" : "0.09"
   },
   "sb_constraints" : {
      "sb-group" : "neo",
      "sb-kind" : "a"
   },
   "total_objects" : "3054",
   "shown_objects" : "3054",
   "fields" : [
      "Designation",
      "Full name",
      "Rise time",
      "Transit time",
      "Set time",
      "Max. time observable",
      "R.A.",
      "Dec.",
      "Vmag",
      "Helio. range (au)",
      "Topo.range (au)",
      "Object-Observer-Sun (deg)",
      "Object-Observer-Moon (deg)",
      "Galactic latitude (deg)"
   ],
   "data" : [
      ["887","887 Alinda (A918 AA)","12:42","16:17*","19:52*","01:37","00:05:53","-07 27'21\"","18.7","2.52","2.22","94.97","133.3","-67.54"],
      ["1221","1221 Amor (1932 EA1)","09:41","13:40","17:40*","04:38","21:28:25","+05 33'55\"","19.7","1.65","0.845","124.59","153.4","-30.92"],
      ...
    ]
}

```

HTTP Response Codes
-------------------

All errors are returned via appropriate HTTP response codes.

| HTTP Code | Description | Typical Usage |
| --- | --- | --- |
| 200 | OK | normal successful result |
| 400 | Bad Request | the request contained invalid keywords, content, or results are invalid: details returned |
| 405 | Method Not Allowed | the request used an incorrect method (see the [HTTP Request](#request) section) |
| 500 | Internal Server Error | the database is not available at the time of the request |
| 503 | Service Unavailable | the server is currently unable to handle the request due to a temporary overloading or maintenance of the server, which will likely be alleviated after some delay |

Change Log
----------

### Version 1.0 (2021 March)

* Initial release

* [Privacy](http://www.jpl.nasa.gov/copyrights.php)
* |
* [Image Policy](http://www.jpl.nasa.gov/imagepolicy)

* [Privacy](http://www.jpl.nasa.gov/copyrights.php)
* [Image Policy](http://www.jpl.nasa.gov/imagepolicy)

|  |  |
| --- | --- |
| Site Manager : | Ryan Park |
| Webmaster : | Alan Chamberlin |
| URS Clearance : | CL#16-5242 |

## Links found on page

- http://www.caltech.edu/
- http://www.enable-javascript.com
- http://www.jpl.nasa.gov/
- http://www.jpl.nasa.gov/copyrights.php
- http://www.jpl.nasa.gov/imagepolicy
- https://ssd-api.jpl.nasa.gov/
- https://ssd-api.jpl.nasa.gov/about/
- https://ssd-api.jpl.nasa.gov/doc/
- https://ssd-api.jpl.nasa.gov/doc/sbdb_filter.html
- https://www.nasa.gov/
