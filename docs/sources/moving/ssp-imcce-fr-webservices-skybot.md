---
source: https://ssp.imcce.fr/webservices/skybot/
fetched: 2026-11-14
status: 200
---

SkyBoT | LTE

×
![]()

SkyBoT
======

The Virtual Observatory Sky Body Tracker
----------------------------------------

#### Version: 3.0 2022-10-01

Presentation
------------

The SkyBoT (Sky Body Tracker) project has the ambition to provide to astronomers
a [VO-compliant](https://www.ivoa.net/) tool useful to prepare and to analyze
astronomical observations of solar system objects. The main usage of SkyBoT services
concerns the search for and identification of Solar System objects in astronomical images.

SkyBoT is [registered](http://vao.stsci.edu/keyword-search/?utf8=%E2%9C%93&search_field=all_fields&q=skybot)
in the IVOA registries under:

* ID: ivo://vopdc.obspm/imcce/skybot
* Title: Sky Body Tracker
* Short Name: SkyBoT

The SkyBoT services can be available through [various softwares](http://ivoa.net/astronomers/applications.html), in particular:

[Aladin](http://aladin.u-strasbg.fr/)
:   Implementation of SkyBoT which allows to resolve the name of the solar system objects, and to search for them
    in any astronomical image ([screenshot](demo/Aladin-FOV45n.png)).
    You can try it, without any installation process, with the
    [Aladin Java applet](http://aladin.u-strasbg.fr/java/nph-aladin.pl?-script=get+SkyBot.IMCCE%282014-06-01T21:02:32.0%29+12+52+47+%2B25+26+33+1deg;sync;get+aladin%28low%29&-from=LTE).
    If you have installed Aladin on your computer, you can access to the current release of SkyBoT via the dedicated tab in the server selector.
    You can also customize your access to SkyBoT by using a special [GLU](http://aladin.u-strasbg.fr/java/FAQ.htx#glu) entry.
    Download the [SkyBoT GLU record](GluFile/skybot2.dic), save it, adapt it, and restart Aladin with the following argument:
    aladin -glufile=skybot2.dic.

[Audela](http://audela.org/)
:   Implementation of SkyBoT which makes it possible to resolve the name of the solar system objects, to search for them in your
    own astronomical images, and to point them with your telescope ([screenshot](demo/Audela.png)).
    To access the SkytBoT service in Audela, open the "Virtual Observatory" panel.

[SAOImageDS9](http://ds9.si.edu/site/Home.html)
:   Implementation of SkyBoT which makes it possible to search for and to identify solar system objects
    in astronomical images (Menu: `Analysis -> Catalogs -> Database -> Skybot`).

[WCS Tools](http://tdc-www.harvard.edu/software/wcstools/)
:   Implementation of SkyBoT which makes it possible to search for solar system objects by using a command line program:
    [scat](http://tdc-www.harvard.edu/software/wcstools/scat/sskybot.html)

[astroquery](https://github.com/astropy/astroquery/pull/1353)
:   Implementation of Miriade and SkyBoT in the namespace `astroquery.imcce/astroquery.solarsystem.imcce`.

Solar system bodies
-------------------

The Solar System objects recognized by SkyBoT are the planets, their major satellites, the asteroids and the comets.
The most direct way to know which objects SkyBoT can search for and identify is to use the [SsODNet-Quaero](/webservices/ssodnet/) API.
For a given object, if the key `ephemeris` is set to `true` then positional ephemerides can be computed,
and thus SkyBoT will make it appear in the list if it is in the requested field of view. The full list of objects can be retrieved
by sending the request `?q=ephemeris:true` to the `search` end-point of the service.
[Check now](https://api.ssodnet.imcce.fr/quaero/1/sso/search?q=ephemeris:true).

The following figure and tables show how are classified the population of asteroids and comets, as defined
by the international community according to the characteristics of their orbits.

Graphical representation of population classes.

Show population table

Definition of population classes of asteroids  
a = semi-major axis, e = eccentriciy, p = period, R = resonnance x:y, e.g. 5:4, 4:3, 11:8, ...

| Population | Semi-major axis (AU) | Aphelion or Perihelion (AU) (\*) | Comment |
| Vulcanoid | 0.08 ≤ a < 0.21 |  | Yet to be discovered |
| NEA>Atira | 0.21 ≤ a < 1.0 | a(1+e) < 0.983 | Handful known |
| NEA>Aten | 0.21 ≤ a < 1.0 | a(1+e) ≥ 0.983 | ~6% of Near Earth Asteroids |
| NEA>Apollo | 1.0 < a < 2.0 | a(1-e) < 1.017 | ~62% of Near Earth Asteroids |
| NEA>Amor | 1.0 < a < 2.0 | 1.017 ≤ a(1-e) < 1.3 | ~32% of Near Earth Asteroids |
| Mars-Crosser>Deep | 1.0 < a < 2.0 | 1.3 ≤ a(1-e) ≤ 1.58 |  |
| Mars-Crosser>Shallow | 1.0 < a < 2.0 | 1.58 ≤ a(1-e) ≤ 1.666 |  |
| Hungaria | 1.0 < a < 2.0 | a(1-e) > 1.666 |  |
| MB>Inner | 2.0 ≤ a < 2.5 |  | Inner Main Belt |
| MB>Middle | 2.5 ≤ a < 2.82 |  | Middle Main Belt |
| MB>Outer | 2.82 ≤ a < 3.27 |  | Outer Main Belt |
| MB>Cybele | 3.27 ≤ a < 3.7 |  |  |
| MB>Hilda | 3.7 ≤ a < 4.6 |  |  |
| Trojan | 4.6 ≤ a < 5.5 |  | Jupiter Trojans (L4 and L5) |
| Centaur | 5.5 ≤ a < 30.1 |  |  |
| KBO>Classical | 30.1 ≤ a < 2000.0 |  | Kuiper belt |
| KBO>Detached | 30.1 ≤ a < 2000.0 | e ≥ 0.24 | Kuiper belt |
| KBO>SDO | 30.1 ≤ a < 2000.0 | a(1-e) ≤ 30.1\*2^(2/3) \* (1-0.24) | Kuiper belt |
| KBO>Classical>Inner | 30.1 ≤ a < 39.4 |  | Kuiper belt |
| KBO>Classical>Main | 39.4 ≤ a < 47.8 |  | Kuiper belt |
| KBO>Classical>Outer | 47.8 ≤ a < 2000.0 |  | Kuiper belt |
| KBO>Resonnant x:y | 30.1 ≤ a < 2000.0 | a - (30.1\*R^(2/3)) ≤ 0.35 | Kuiper belt |
| IOC | a ≥ 2000.0 |  | Inner Oort cloud |

Definition of population classes of comets

| Population | Orbital Period (year) | Eccentricity | Tisserand's invariant |
| Long-Period | P > 200 |  |  |
| Short-Period | P ≤ 200 |  |  |
| Short-Period>Jupiter-family |  | e < 1 | TJ > 2 |
| Short-Period>Halley-type |  | e < 1 | TJ ≤ 2 |

API
---

The SkyBoT Web service provides the following methods (HTTP + XML + SOAP + WSDL):

[SkyBoT Cone-Search](api/conesearch/)
:   This method allows you to search for and identify all the known solar system objects in a field of
    view of a given size (circle or box, up to 30°) at a given epoch (see SkyBoT Status method
    to know the covered period)

[SkyBoT Resolver](api/resolver/)
:   This method allows you to resolve the names of the solar system objects in their celestial
    coordinates at a given epoch (see SkyBoT Status method to know the covered period)

And the administrative method:

[SkyBoT Status](api/status/)
:   This method provides the actual status of the database and is useful to know the period of time covered by SkyBoT.
    [Check now!](api/status.php?-mime=html&-from=SSPDoc)

[SkyBoT Availability](api/getAvailability/)
:   This method provides the availability of the SkyBoT web-service.
    [Check now!](api/getAvailability.php?-mime=html&-from=SSPDoc)

Practical use
-------------

The SkyBoT cone-search method allows one to retrieve all the known solar system objects located in a time-stamped field of view.
This may be useful to identify sources in an astronomical image. The SkyBoT resolver method allows one to quickly compute the
ephemeris of any solar system objects at a given date. This may be useful to resolve the designation of a solar system object
in celestial coordinates, and to quickly know where it is located on the celestial sphere at a given epoch. However, it is
recommended to use the [SsODNet API](/webservices/ssodnet) for this.

The SkyBoT service is a SaaS which allows to access methods to search for and identify solar system objects through
SOAP requests or by using VO applications such as [Aladin](https://aladin.u-strasbg.fr/) or
[Topcat](http://www.star.bris.ac.uk/~mbt/topcat/). The underlying technology
(XML+SOAP+WSDL) being inherently interoperable, you can use them and implement them regardless
of what your favourite platform and operating system are. For that, you can freely download toolkits
[client](clients/) to help you to make the integration of the SkyBoT service seamless with your code.

The easiest way to implement SkyBoT is to use a non-interactive network downloader (e.g. `curl`,
`wget`) to send HTTP requests and to receive the result "on your desktop". Advanced users
may prefer to query SkyBoT directly through its API.

Scientific issues
-----------------

The SkyBoT service is described in [Berthier et al., 2006](https://ui.adsabs.harvard.edu/abs/2006ASPC..351..367B/abstract).
The core of SkyBoT is a database of pre-computed ephemeris of all of the known solar system objects (asteroids, planets,
natural satellites and comets) over a period which extends from the end of the XIXe century (1889-11-13) to the first half
of the XXIe century (2060-03-21). The ephemerides provided by SkyBoT are J2000 astrometric geocentric or topocentric
equatorial coordinates (right ascension and declination) at the requested epoch. SkyBoT can also provide J2000 mean heliocentric
equatorial rectangular coordinates (position and motion vector) throught the [Skbot3D API](/webservices/skybot3d).

SkyBoT can also provides ephemerides of solar system objects computed for space probes, such as the Rosetta, Kepler, TESS, or the
Earth-Sun L2 point. Please [contact us](mailto:vossp.lte@obspm.fr) if you have a special need that you will like to be
implemented in SkyBoT.

The right ascension and declination of the targets are computed by numerical integration of a two bodies problem perturbed by the 8 planets,
taking into account relativistic perturbations (post-newtonian approximation). The pre-computed orbits are calculated with the same algorithm,
with a sampling step of 1 day and a storage step in the SkyBoT database of 10 days. The dynamical properties of asteroids are
issued from the [ASTORB](https://asteroid.lowell.edu/main/) database (Lowell Observatory). The dynamical properties
of comets are issued from the [IMCCE cometary database](https://ftp.imcce.fr/pub/databases/cometpro/). The ephemeris of the
planets are computed using the [INPOP](https://www.imcce.fr/inpop) planetary theory. The ephemeris of the natural satellites
are computed using various orbital models, depending on the planetary system.

The accuracy of the ephemeris provided by SkyBoT are at the few tens of milli-arcseconds. Depending on the accuracy of asteroid and comet orbits -
which depends on the number and the orbital arc spanned by the observations that are fitted - the external accuracy of the ephemeris
can be hundreds or thousands of arcseconds in the worst cases. As a consequence, when checking the location of them in astronomical images,
it may occur huge errors on the position of some asteroids or comets, especially if they are not accurately known. It will fall within the
competence of the user to check and filter the objects before using the data provided by SkyBoT.

Technical issues
----------------

SkyBoT is powered by a dedicated hardware infrastructure composed of 10 computing elements. A master/slave system, composed of 1+4 servers,
insures the administration, the monitoring and the update of the SkyBoT database. The SkyBoT services run on 4 servers enhanced by a load
balancing and failover solution. The servers operate OpenSuse LEAP Linux distribution. The suite of SkyBoT softwares is written in PHP for the
services, and Fortran 2013 (using GNU compiler) and MPICH 2 for the parallelized computation of the ephemerides. The data (pre-computed
ephemerides) are stored, processed and secured thanks to the MyISAM storage engine of the [MariaDB](https://mariadb.org) database.
The monitoring of the system (hardware and software) is insures by NAGIOS and a home made administration/monitoring interface.

The SkyBoT database is updated weekly to include lately discovered bodies and to update the ephemerides of bodies (mainly asteroids)
of which orbits were improved. The hardware infrastructure of SkyBoT allows the service to be available all the time, even when the
update process runs. According to the number of asteroids to be updated (few hundreds to a few tens of thousands), you can be brought
to wait some time (few hours to two or three days) before being able to access the bodies recently discovered. For comets, the update
occurs weekly with the lately [discovered objects](http://www.cfa.harvard.edu/iau/Ephemerides/Comets/) published by the
[Minor Planet Center](http://www.cfa.harvard.edu/iau/mpc.html). For planets and natural satellites, the update occurs
when new orbital solutions are made available.

The SkyBoT service was designed and developed by IMCCE, now LTE (Observatoire de Paris / CNRS) as part of the IMCCE Virtual Observatory
project (2004-2012). It is supported by the [VO-Paris Data Centre](http://vo.obspm.fr/) and the
[french VO](http://www.france-ov.org/twiki/bin/view/). The SkyBoT service is hosted by the LTE,
and is accessible through HTTP query methods and a XML+SOAP+WSDL API.

User support
------------

If you are confronted with a bug, or if you would like to request improvements or special needs, please use the
[LTE Mantis Bug Tracker](https://mantisbt.imcce.fr/) (Quick access: use the *Report issue*
button in the portal menubar).

Each response sent back by the SkyBoT service contains a ticket number. This 18 digits number (e.g. 166134214081377735) identifies each
request. If you face with errors by using the SkyBoT service (it could occur that no relevant error message is returned), please report
us the ticket number corresponding to the problem. It will help you to anderstand and solve it, and you will help us to improve the service.

Notes to user
-------------

The use of the SkyBoT service to search for asteroids in an astronomical archive or in a recent image can present difficulties
of interpretation. The main issue may be: *is the source in my image the asteroid found by SkyBoT?*
To answer this question, it may be necessary to pay attention to the following:

* ensure that the magnitudes are compatible
* ensure that the ephemeris and the measured position uncertainties are compatible
* ensure that the accuracy of the epoch is compatible with respect to the target motion

This last point is mandatory because the uncertainty on the epoch can easily shift the computed position of
the body by several arcseconds because of its apparent motion on the celestial sphere (from few arcsec per hour
to several tens of arcsec per hours for main-belt objects, and more for Near-Earth asteroids). So please, be sure to
completely exploit the informations provided by the service (magnitude, error of position, angular velocity, etc).

The error of position of ephemerides provided by SkyBoT gives an estimation of the position uncertainty.
This error takes into account only the accuracy of the orbit. The errors which are coming from the computation,
the model and the reference frame are not taken into account. For asteroids, this error of position is computed
on the basis of the parameters CEU (absolute value of the current 1-σ ephemeris uncertainty) and CEUrate
(rate of change of CEU) resulting from ASTORB database.

**In any case, the LTE cannot be held for person in charge for a misuse or interpretation of the SkyBoT service.**

How to cite SkyBoT
------------------

If SkyBoT was helpful for your research work, the following acknowledgment would be appreciated:
"This research has made use of LTE SkyBoT VO tool", or cite the following article
[2006ASPC..351..367B](https://ui.adsabs.harvard.edu/abs/2006ASPC..351..367B/abstract).

Bibitem:
:   ```
    \bibitem[Berthier et al.(2006)]{2006ASPC..351..367B} Berthier, J., Vachier, F., Thuillot, W., Fernique, P., 
    Ochsenbein, F., Genova, F., Lainey, V., \& Arlot, J.-E.\ 2006, Astronomical Data Analysis Software and 
    Systems XV, 351, 367

    ```

Bibtex code:
:   ```

    @INPROCEEDINGS{2006ASPC..351..367B,
       author = {{Berthier}, J. and {Vachier}, F. and {Thuillot}, W. and {Fernique}, P. and 
                 {Ochsenbein}, F. and {Genova}, F. and {Lainey}, V. and {Arlot}, J.-E.},
        title = "{SkyBoT, a new VO service to identify Solar System objects}",
    booktitle = {Astronomical Data Analysis Software and Systems XV},
         year = 2006,
       series = {Astronomical Society of the Pacific Conference Series},
       volume = 351,
       editor = {{Gabriel}, C. and {Arviset}, C. and {Ponz}, D. and {Enrique}, S.},
        month = jul,
        pages = {367-+},
       adsurl = {http://adsabs.harvard.edu/abs/2006ASPC..351..367B},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
    }

    ```

## Links found on page

- http://aladin.u-strasbg.fr/
- http://aladin.u-strasbg.fr/java/FAQ.htx#glu
- http://aladin.u-strasbg.fr/java/nph-aladin.pl?-script=get+SkyBot.IMCCE%282014-06-01T21:02:32.0%29+12+52+47+%2B25+26+33+1deg;sync;get+aladin%28low%29&-from=LTE
- http://audela.org/
- http://ds9.si.edu/site/Home.html
- http://ivoa.net/astronomers/applications.html
- http://tdc-www.harvard.edu/software/wcstools/
- http://tdc-www.harvard.edu/software/wcstools/scat/sskybot.html
- http://vao.stsci.edu/keyword-search/?utf8=%E2%9C%93&search_field=all_fields&q=skybot
- http://vo.obspm.fr/
- http://www.cfa.harvard.edu/iau/Ephemerides/Comets/
- http://www.cfa.harvard.edu/iau/mpc.html
- http://www.france-ov.org/twiki/bin/view/
- http://www.star.bris.ac.uk/~mbt/topcat/
- https://aladin.u-strasbg.fr/
- https://api.ssodnet.imcce.fr/quaero/1/sso/search?q=ephemeris:true
- https://asteroid.lowell.edu/main/
- https://astroquery.readthedocs.io/en/latest/imcce/imcce.html
- https://ftp.imcce.fr/pub/databases/cometpro/
- https://github.com/astropy/astroquery/pull/1353
- https://mantisbt.imcce.fr/
- https://mariadb.org
- https://ssp.imcce.fr/webservices/skybot/GluFile/skybot2.dic
- https://ssp.imcce.fr/webservices/skybot/api/conesearch/
- https://ssp.imcce.fr/webservices/skybot/api/getAvailability.php?-mime=html&-from=SSPDoc
- https://ssp.imcce.fr/webservices/skybot/api/getAvailability/
- https://ssp.imcce.fr/webservices/skybot/api/resolver/
- https://ssp.imcce.fr/webservices/skybot/api/status.php?-mime=html&-from=SSPDoc
- https://ssp.imcce.fr/webservices/skybot/api/status/
- https://ssp.imcce.fr/webservices/skybot/clients/
- https://ssp.imcce.fr/webservices/skybot/demo/Aladin-FOV45n.png
- https://ssp.imcce.fr/webservices/skybot/demo/Audela.png
- https://ssp.imcce.fr/webservices/skybot3d
- https://ssp.imcce.fr/webservices/ssodnet
- https://ssp.imcce.fr/webservices/ssodnet/
- https://ui.adsabs.harvard.edu/abs/2006ASPC..351..367B/abstract
- https://www.imcce.fr/inpop
- https://www.ivoa.net/
