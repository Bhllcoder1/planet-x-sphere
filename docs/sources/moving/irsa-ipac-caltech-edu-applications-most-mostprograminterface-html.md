---
source: https://irsa.ipac.caltech.edu/applications/MOST/MOSTProgramInterface.html
fetched: 2026-11-14
status: 200
---

IRSA Catalog Search Form 

MOST Application Program Interface (API)
----------------------------------------

Note: A Python notebook showing how to interact with some of the MOST capabilities is available: [Python notebook](https://caltech-ipac.github.io/irsa-tutorials/most-queries).

The MOST API allows scripting of requests via a command-line call.
An example:

* *curl -o out.tbl "https://irsa.ipac.caltech.edu/cgi-bin/MOST/nph-most?catalog=wise\_merge&input\_type=name\_input&obj\_name=Victoria&obs\_begin=2014+05+01&obs\_end=2014+05+30&output\_mode=Brief"*

Calls when using orbital elements are slightly different for asteroids and comets:

Asteroid

* *curl -o out.tbl "https://irsa.ipac.caltech.edu/cgi-bin/MOST/nph-most?catalog=wise\_merge&obs\_begin=2010+01+01&obs\_end=2010+05+01&obj\_type=Asteroid&input\_type=manual\_input&body\_designation=TestAsteroid&epoch=55273.0&semimajor\_axis=2.684723515&eccentricity=0.33709263&inclination=11.1080776&arg\_perihelion=43.9047086&ascend\_node=327.9898280&mean\_anomaly=64.7389713&output\_mode=Brief"*

Comet

* *curl -o out.tbl "https://irsa.ipac.caltech.edu/cgi-bin/MOST/nph-most?catalog=wise\_merge&obs\_begin=2010+07+01&obs\_end=2010+08+01&obj\_type=Comet&input\_type=manual\_input&body\_designation=TestComet&epoch=55368.0&perih\_dist=1.49452503&eccentricity=0.53379824&inclination=12.87619139&arg\_perihelion=153.49099443&ascend\_node=113.21175889&perih\_time=2455424.64772&output\_mode=Brief"*

And similarly for MPC input:

Asteroid

* *curl -o out.tbl "https://irsa.ipac.caltech.edu/cgi-bin/MOST/nph-most?catalog=wise\_allsky\_4band&obj\_type=Asteroid&input\_type=mpc\_input&mpc\_data=00324+6.82+0.09+K103I+64.7389713+43.9047086+ 327.9898280+11.1080776+0.33709263+0.2240550+2.684723515+0+MPO344295+2289+63+ 1892-2015+0.50+M-v+38h+MPCLINUX+0000+(324)+Bamberga+20150614&output\_mode=Brief"*

Comet

* *curl -o out.tbl "https://irsa.ipac.caltech.edu/cgi-bin/MOST/nph-most?catalog=wise\_allsky\_4band&obj\_type=Comet&input\_type=mpc\_input&mpc\_data=PK10N010+2010+08+16.1477+1.494525+0.533798+153.4910+113.2118+12.8762+20100621+17.0+4.0+P/2010+N1+(WISE)+MPC+75712&output\_mode=Brief"*

**Adjustable keywords:**

|  |  |  |  |
| --- | --- | --- | --- |
| **keyword** | **required?** | **description** | **values** |
| catalog | required | Dataset catalog name. NOTE: Dataset needs to be moving-object search enabled. | Current moving-object enabled datasets:  2MASS: 2mass   Spitzer BCD: spitzer\_bcd   PTF: ptf   SOFIA: sofia   SPHEREx: spherex   ZTF: ztf   WISE/NEOWISE Merged: wise\_merge   WISE All-Sky 4-band: wise\_allsky\_4band  WISE 3band: wise\_allsky\_3band   WISE 2band: wise\_allsky\_2band   NEOWISE-R: wise\_neowiser   NEOWISE-R (By Year): wise\_neowiser\_yr1, etc. |
| outfmt | optional | Output format | Regular: Normal HTML  Full: Full HTML  Brief: ASCII table  VOTable: VO Table |
| obs\_begin | optional | Earliest observation date (UT) to include | yyyy+mm+dd+hh:mm:ss |
| obs\_end | optional | Latest observation date (UT) to include | yyyy+mm+dd+hh:mm:ss |
| ephem\_step | optional | ephemeris time step (day) | default=0.25 day |
| input\_type | required | Type of input | name\_input = by name or number   naifid\_input = by NAIF ID  mpc\_input = orbital elements in MPC format   manual\_input = orbital elements |
| obj\_name | required for name input | Name or numeric designation of object | e.g "324" or "Bamberga" (asteroid) or "29P" (comet) |
| obj\_naifid | required for NAIF ID input | Name or numeric designation of object | e.g 899 for Neptune |
| obj\_type | required for MPC input | Solar-system object type | Asteroid or Comet |
| obj\_type\_elm | obj\_type or obj\_type\_elm required for orbital elements input | Solar-system object type | Asteroid or Comet |
| mpc\_data | required for MPC input | MPC string | See [Gator Moving Object help page](/applications/Gator/GatorAid/irsa/moving.html). |
| semimajor\_axis/perih\_dist | required for orbital  elements input | Semi-major axis (asteroid) or  perihelion distance (comet) in AU | >0 |
| eccentricity | required for orbital  elements input | Eccentricity of orbit | 0.0-1.0 |
| inclination | required for orbital  elements input | Inclination of orbit (deg) | 0.0-180.0 |
| arg\_perihelion | required for orbital  elements input | Argument of perihelion (deg) | 0.0-360.0 |
| ascend\_node | required for orbital  elements input | Longitude of ascending node (deg) | 0.0-360.0 |
| mean\_anomaly/perih\_time | required for orbital  elements input | Mean anomaly (asteroid) in deg, or   perihelion time (comet) in  yyyy+mm+dd+hh:mm:ss | 0.0-360.0 for mean anomaly |
| body\_designation | required for orbital elements input | Designation for returned ephemeris | e.g. Bamberga |
| epoch | required for orbital  elements input | Epoch of coordinates in MJD  (Modified Julian Date) | e.g. 55203.0 for start of WISE mission |

## Links found on page

- https://caltech-ipac.github.io/irsa-tutorials/most-queries
- https://irsa.ipac.caltech.edu/applications/Gator/GatorAid/irsa/moving.html
