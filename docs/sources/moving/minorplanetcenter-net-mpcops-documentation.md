---
source: https://minorplanetcenter.net/mpcops/documentation/
fetched: 2026-11-14
status: 200
---

IAU Minor Planet Center

[The International Astronomical Union Minor Planet Center](/)
=============================================================

* [Home](/)
* [About](/about)
* [Contact](/mpcops/contact/)
* [Helpdesk](https://mpc-service.atlassian.net/servicedesk/customer/portals)

* [OBSERVERS](/iau/mpc.html)
  + [Ephemeris Service](/iau/MPEph/MPEph.html)
  + [MPChecker](/cgi-bin/checkmp.cgi)
  + [MPECs](javascript:void(0))
    - [Recent](/mpec/RecentMPECs.html)
    - [Search](/mpcops/mpecs/)
    - [Subscription Service](/mpcops/signup/mpecs/)
  + [NEO Confirmation](/iau/NEO/toconfirm_tabular.html)
  + [Possible Comet Confirmation](/iau/NEO/pccp_tabular.html)
  + [Report Cometary Activity](/mpcops/submissions/cometary/)
  + [Orbits/Observations Database](/db_search)
  + [MPC Explorer](https://data.minorplanetcenter.net/explorer)
  + [Orbital Elements](/iau/Ephemerides/EphemOrbEls.html)
    - [MPCORB](/iau/MPCORB.html)
    - [MPCAT](/iau/ECS/MPCAT/MPCAT.html)
    - [MPCUPDATE](/iau/ECS/MPCUPDATE/MPCUPDATE.html)
    - [Orbital Elements for Software](/iau/Ephemerides/SoftwareEls.html)
  + [Publications](javascript:void(0))
    - [Publications Overview](/iau/services/MPCServices.html)
    - [Publications Archive](/iau/ECS/MPCArchive/MPCArchive_TBL.html)
  + [NEO Services](/iau/NEO/TheNEOPage.html)
    - [Confirmation](/iau/NEO/toconfirm_tabular.html)
    - [Ratings](/iau/NEO/PossNEO.html)
    - [Observation Planning Aid](/cgi-bin/neaobs.cgi)
    - [NEOCP Followup Report Form](/neocp_followup_report/)
    - [NEOCP Followup Reports](/neocp_followup_reports/)
    - [NEOCP Recent Observations](/neocp_obs)
    - [NEOCP Plots](/mpcops/neocp/neocp_plots/)
    - [Current NEOCP Objects](/cgi-bin/cgipy/neocp_info/)
    - [Previous NEOCP Objects](/mpcops/neocp/neocp_prev_des/)
    - [NEO Recovery](/iau/recovery/recovery.html)
  + [Observations](javascript:void(0))
    - [WAMO](/wamo/wamo.html)
  + [Orbits](/mpcops/orbits/)
    - [Orbit Comparison Tool](https://data.minorplanetcenter.net/comparison/index.html)
    - [Request for archival astrometry](/mpcops/orbits/no-orbits-astrometry/)
  + [Other Observer Services](/iau/services/WebCSAccess.html)
    - [Observing Target List](/whatsup)
    - [Observing List Customizer](/iau/lists/Customize.html)
    - [Natural Satellite Ephemerides](/iau/NatSats/NaturalSatellites.html)
    - [New Object Ephemerides](/iau/MPEph/NewObjEphems.html)
    - [Processing Times](/iau/delays/neocp_delay.html)
    - [Submitting Pointing Information](/pointings)
    - [Search the Pointing Database](/mpcops/pointings/sky_coverage/)
  + [Identifications](javascript:void(0))
    - [Documentation](/mpcops/documentation/identifications/)
    - [Submission Format](/mpcops/documentation/identifications/submission-format/)
    - [Submit](/mpcops/submissions/identifications/)
  + [Observation Archive](/iau/ECS/MPCAT-OBS/MPCAT-OBS.html)
  + [Sky Coverage](/iau/SkyCoverage.html)
  + [Documentation](/iau/MPC_Documentation.html)
    - [MPC Submission Info](/iau/info/TechInfo.html)
    - [Astrometry Guide](https://docs.minorplanetcenter.net/mpc-ops-docs/astrometry/getting-started/)
    - [Artificial Satellites](/mpcops/documentation/artificial-satellites/)
    - [Submit Action Code](/submit_action_code)
    - [Other](/mpcops/documentation/)
  + [Lists and Plots](/iau/lists/Lists.html)
    - [Minor Planets](/iau/lists/MPLists.html)
    - [Comets](/iau/lists/CometLists.html)
    - [Observatory Codes](/iau/lists/ObsCodesF.html)
    - [Animations](/iau/Animations/Animations.html)
  + [Summaries](javascript:void(0))
    - [(Alpha) MPC Summary](https://data.minorplanetcenter.net/summary)
    - [Latest Published Data](/mpc/summary)
    - [Summary of PHA and NEA Discoveries](/iau/lists/YearlyBreakdown.html)
  + [Deprecated Webpages](/deprecated-pages.html)
* [DATA](/data)
* [NEWSLETTER](https://buttondown.com/MPC_newsletter)
* [STATUS](/mpcops/mpcstatus/)
* [DOCUMENTATION](/mpcops/documentation/)
* [EXTERNAL](/)
  + [MPC User Group (MUG)](https://mpcmug.astro.umd.edu/)
  + [IAWN](http://iawn.net/)
  + [SBN Annex](https://sbnmpc.astro.umd.edu/)
  + [WGSBN](https://www.wgsbn-iau.org/)
  + [Light Curve Database](http://alcdef.org)

MPC Documentation
=================

**Documentation Notice:**
Many of the pages here have been migrated to
<https://docs.minorplanetcenter.net>.
As of October 2026, this page will automatically redirect such pages to the new documentation.
For more information, please read our
[February 2026 Newsletter](https://minorplanetcenter.net/media/newsletters/MPC_Newsletter_Feb2026.pdf).

Content
-------

  

* [**Frequently Asked Questions (FAQs)**](#FAQs)
* [**Subscription to MPC Notification Services**](#subscription)
* **APIs**

+ [MPC APIs](#apis)

* **Replicated PostgreSQL tables**

+ [MPC's replicated postgreSQL tables](#replicatedtables)

* **Observations**

+ [MPC Guide to minor planet astrometry](#astrometryguide)
+ [Observations API](#apis)
+ [Negative observations protocol](#negativeobservations)
+ [Singletons and archival observations](#sarc)

* **ADES**

+ [Valid ADES values](#usefulists)
+ [ADES related documentation](#ades)

* **Designation System**

+ [Minor Planet Designations](#designations)
+ [Cometary Designations](https://www.minorplanetcenter.net/iau/lists/CometResolution.html)

* **Program codes and observatory codes**

+ [A new approach for program codes](#programcodes)
+ [List of program codes](#usefulists)
+ [List of observatory codes](#usefulists)
+ [How do I obtain an observatory code?](https://docs.minorplanetcenter.net/mpc-ops-docs/observatory-and-program-codes/observatory-codes/#how-do-i-get-an-observatory-code)
+ [Observatory codes API](#apis)

* **Orbits**

+ [Orbits API](#apis)
+ [Orbital elements](#orbitalelements)
+ [MPC\_ORB JSON](#orbitalelements)
+ [Orbit and Object Types](#orbitandobjecttype)

* **Identifications**

+ [Identifications](#identifications)

* **Others**

+ [Artificial Satellites](#artificialsatellites)
+ [Designations](#designations)
+ [Edgar Wilson Award](#edgarwilson)

  

---

Frequently Asked Questions (FAQs)
---------------------------------

* [List of FAQs](https://docs.minorplanetcenter.net/mpc-ops-docs/faqs/)

  

MPC Guide to minor planet astrometry
------------------------------------

* [How do I begin](https://docs.minorplanetcenter.net/mpc-ops-docs/astrometry/getting-started/)?
* [How do I report observations to the Minor Planet Center](https://docs.minorplanetcenter.net/mpc-ops-docs/astrometry/reporting-observations/)?
* [How do I get an observatory code](https://docs.minorplanetcenter.net/mpc-ops-docs/observatory-and-program-codes/observatory-codes/#how-do-i-get-an-observatory-code)?
* [How do I submit my astrometry to the MPC using Tycho Tracker](https://docs.minorplanetcenter.net/mpc-ops-docs/observations/tycho-tracker/)?

  

MPC APIs
--------

* ### Where Are My Observations (WAMO)

  [WAMO API](https://docs.minorplanetcenter.net/mpc-ops-docs/apis/wamo/) documentation.
  
* ### Submission Status

  [Submission Status API](https://docs.minorplanetcenter.net/mpc-ops-docs/apis/submission-status/) documentation.
  
* ### Designation Identifier

  [Designation Identifier API](https://docs.minorplanetcenter.net/mpc-ops-docs/apis/query-identifier/) documentation.
  
* ### Observations

  [Observations API](https://docs.minorplanetcenter.net/mpc-ops-docs/apis/get-obs/) documentation.
  
* ### NEOCP Observations

  [NEOCP Observations API](https://docs.minorplanetcenter.net/mpc-ops-docs/apis/get-obs-neocp/) documentation.
  
* ### Near-Duplicate Observations

  [Check Near-Duplicates (CND) API](https://docs.minorplanetcenter.net/mpc-ops-docs/apis/cnd/) documentation.
  
* ### Orbits

  [Orbits API](https://docs.minorplanetcenter.net/mpc-ops-docs/apis/get-orb/) documentation.
  
* ### Observatory Codes

  [Observatory Codes API](https://docs.minorplanetcenter.net/mpc-ops-docs/apis/obscodes/) documentation.
  
* ### MPECs

  [MPECs API](https://docs.minorplanetcenter.net/mpc-ops-docs/apis/mpecs/) documentation.
  
* ### Action Codes

  [Action Codes API](https://docs.minorplanetcenter.net/mpc-ops-docs/apis/action-codes/) documentation.
  
* ### Lists of Objects

  [List API](https://docs.minorplanetcenter.net/mpc-ops-docs/apis/list/) documentation.
  
* ### Magnitude Bands

  [Magnitude Band API](https://docs.minorplanetcenter.net/mpc-ops-docs/apis/mag-band/) documentation.
  
* ### Other APIs

  For other APIs, please see the [MPC Public Documentation Hub](https://docs.minorplanetcenter.net/mpc-ops-docs/apis/).

  

MPC's replicated postgreSQL tables
----------------------------------

* [Introduction and examples](https://docs.minorplanetcenter.net/mpc-ops-docs/data-and-services/replicated-tables-intro/)
* [Schema](/mpcops/documentation/replicated-tables-schema/)

  

ADES related documentation
--------------------------

* [Introduction](https://docs.minorplanetcenter.net/mpc-ops-docs/observations/ades-format/)
* [Valid ADES values](https://docs.minorplanetcenter.net/mpc-ops-docs/observations/valid-ades-values/)
* [GitHub repository](https://github.com/IAU-ADES/ADES-Master/)
* [Official format description](https://github.com/IAU-ADES/ADES-Master/blob/master/ADES_Description.pdf)

  

Program codes and observatory codes
-----------------------------------

* [Program Codes policy](/mpcops/documentation/program-codes-policy/)
* [Program Codes](https://docs.minorplanetcenter.net/mpc-ops-docs/observatory-and-program-codes/program-codes/)
* [Observatory codes](https://minorplanetcenter.net/iau/lists/ObsCodesF.html)

  

Singletons and archival observations
------------------------------------

* [Singletons and archival observations committee (SARC)](https://docs.minorplanetcenter.net/mpc-ops-docs/data-and-services/sarc/)

  

Negative observations protocol
------------------------------

* [Protocol for Negative Observations for Virtual Impactors](https://docs.minorplanetcenter.net/mpc-ops-docs/observations/negative-observations/)

  

Orbital elements
----------------

* [MPC\_ORB JSON](https://docs.minorplanetcenter.net/mpc-ops-docs/orbits/mpc-orb-json/)
* [Orbital elements in the *ele220* format](https://docs.minorplanetcenter.net/mpc-ops-docs/orbits/ele220-format/)
* [Standard export format for minor-planet orbits](https://minorplanetcenter.net/iau/info/MPOrbitFormat.html)

  

Orbit and Object Types
----------------------

Below are links to how the MPC categorizes orbit types and object types.

* [Orbit Type Definition](https://docs.minorplanetcenter.net/mpc-ops-docs/orbits/orbit-types/)
* [Object Type Definition](https://docs.minorplanetcenter.net/mpc-ops-docs/orbits/object-types/)

  

Identifications
---------------

* [Identifications](https://docs.minorplanetcenter.net/mpc-ops-docs/identifications/)

+ [Submission Format](https://docs.minorplanetcenter.net/mpc-ops-docs/identifications/submission-format/)
+ [Submit Identifications](/mpcops/submissions/identifications/)
+ [MPC criteria for accepting or rejecting identifications](https://docs.minorplanetcenter.net/mpc-ops-docs/identifications/acceptance-criteria/)

  

Artificial Satellites
---------------------

* [MPC Policy on Disposition and Distribution of Observations on Artificial Satellites](https://docs.minorplanetcenter.net/mpc-ops-docs/miscellaneous/artsat-obs-policy/)

  

Subscription to MPC Notification Services
-----------------------------------------

* To subscribe to receive Minor Planet Electronic Circulars
  (MPECs) or join the MPC Announcement Email List/Group please use
  this [link.](https://mpc-service.atlassian.net/servicedesk/customer/portal/18)

  

Different designations that the MPC can assign to minor planets, comets, and natural satellites
-----------------------------------------------------------------------------------------------

### Minor Planets

* [Provisional designation definition for minor planets](https://docs.minorplanetcenter.net/mpc-ops-docs/designations/provisional-designations/)

  

Edgar Wilson Award
------------------

* [Award Information](https://docs.minorplanetcenter.net/mpc-ops-docs/miscellaneous/edgar-wilson-award-information/)
* [Award Winners](https://docs.minorplanetcenter.net/mpc-ops-docs/miscellaneous/edgar-wilson-award-winners/)

* [Home](/)
* [About](/about)
* [Helpdesk](https://mpc-service.atlassian.net/servicedesk/customer/portals)
[![Center for Astrophysics | Harvard & Smithsonian](/images/CfA_Logo_Vertical_CMYK.png)](https://www.cfa.harvard.edu)

The Minor Planet Center is hosted by the Center for Astrophysics | Harvard & Smithsonian.
The Minor Planet Center is funded by NASA.

## Links found on page

- http://alcdef.org
- http://iawn.net/
- https://buttondown.com/MPC_newsletter
- https://data.minorplanetcenter.net/comparison/index.html
- https://data.minorplanetcenter.net/explorer
- https://data.minorplanetcenter.net/summary
- https://docs.minorplanetcenter.net
- https://docs.minorplanetcenter.net/mpc-ops-docs/apis/
- https://docs.minorplanetcenter.net/mpc-ops-docs/apis/action-codes/
- https://docs.minorplanetcenter.net/mpc-ops-docs/apis/cnd/
- https://docs.minorplanetcenter.net/mpc-ops-docs/apis/get-obs-neocp/
- https://docs.minorplanetcenter.net/mpc-ops-docs/apis/get-obs/
- https://docs.minorplanetcenter.net/mpc-ops-docs/apis/get-orb/
- https://docs.minorplanetcenter.net/mpc-ops-docs/apis/list/
- https://docs.minorplanetcenter.net/mpc-ops-docs/apis/mag-band/
- https://docs.minorplanetcenter.net/mpc-ops-docs/apis/mpecs/
- https://docs.minorplanetcenter.net/mpc-ops-docs/apis/obscodes/
- https://docs.minorplanetcenter.net/mpc-ops-docs/apis/query-identifier/
- https://docs.minorplanetcenter.net/mpc-ops-docs/apis/submission-status/
- https://docs.minorplanetcenter.net/mpc-ops-docs/apis/wamo/
- https://docs.minorplanetcenter.net/mpc-ops-docs/astrometry/getting-started/
- https://docs.minorplanetcenter.net/mpc-ops-docs/astrometry/reporting-observations/
- https://docs.minorplanetcenter.net/mpc-ops-docs/data-and-services/replicated-tables-intro/
- https://docs.minorplanetcenter.net/mpc-ops-docs/data-and-services/sarc/
- https://docs.minorplanetcenter.net/mpc-ops-docs/designations/provisional-designations/
- https://docs.minorplanetcenter.net/mpc-ops-docs/faqs/
- https://docs.minorplanetcenter.net/mpc-ops-docs/identifications/
- https://docs.minorplanetcenter.net/mpc-ops-docs/identifications/acceptance-criteria/
- https://docs.minorplanetcenter.net/mpc-ops-docs/identifications/submission-format/
- https://docs.minorplanetcenter.net/mpc-ops-docs/miscellaneous/artsat-obs-policy/
- https://docs.minorplanetcenter.net/mpc-ops-docs/miscellaneous/edgar-wilson-award-information/
- https://docs.minorplanetcenter.net/mpc-ops-docs/miscellaneous/edgar-wilson-award-winners/
- https://docs.minorplanetcenter.net/mpc-ops-docs/observations/ades-format/
- https://docs.minorplanetcenter.net/mpc-ops-docs/observations/negative-observations/
- https://docs.minorplanetcenter.net/mpc-ops-docs/observations/tycho-tracker/
- https://docs.minorplanetcenter.net/mpc-ops-docs/observations/valid-ades-values/
- https://docs.minorplanetcenter.net/mpc-ops-docs/observatory-and-program-codes/observatory-codes/#how-do-i-get-an-observatory-code
- https://docs.minorplanetcenter.net/mpc-ops-docs/observatory-and-program-codes/program-codes/
- https://docs.minorplanetcenter.net/mpc-ops-docs/orbits/ele220-format/
- https://docs.minorplanetcenter.net/mpc-ops-docs/orbits/mpc-orb-json/
- https://docs.minorplanetcenter.net/mpc-ops-docs/orbits/object-types/
- https://docs.minorplanetcenter.net/mpc-ops-docs/orbits/orbit-types/
- https://github.com/IAU-ADES/ADES-Master/
- https://github.com/IAU-ADES/ADES-Master/blob/master/ADES_Description.pdf
- https://minorplanetcenter.net/
- https://minorplanetcenter.net/about
- https://minorplanetcenter.net/cgi-bin/cgipy/neocp_info/
- https://minorplanetcenter.net/cgi-bin/checkmp.cgi
- https://minorplanetcenter.net/cgi-bin/neaobs.cgi
- https://minorplanetcenter.net/data
- https://minorplanetcenter.net/db_search
- https://minorplanetcenter.net/deprecated-pages.html
- https://minorplanetcenter.net/iau/Animations/Animations.html
- https://minorplanetcenter.net/iau/ECS/MPCAT-OBS/MPCAT-OBS.html
- https://minorplanetcenter.net/iau/ECS/MPCAT/MPCAT.html
- https://minorplanetcenter.net/iau/ECS/MPCArchive/MPCArchive_TBL.html
- https://minorplanetcenter.net/iau/ECS/MPCUPDATE/MPCUPDATE.html
- https://minorplanetcenter.net/iau/Ephemerides/EphemOrbEls.html
- https://minorplanetcenter.net/iau/Ephemerides/SoftwareEls.html
- https://minorplanetcenter.net/iau/MPCORB.html
- https://minorplanetcenter.net/iau/MPC_Documentation.html
- https://minorplanetcenter.net/iau/MPEph/MPEph.html
- https://minorplanetcenter.net/iau/MPEph/NewObjEphems.html
- https://minorplanetcenter.net/iau/NEO/PossNEO.html
- https://minorplanetcenter.net/iau/NEO/TheNEOPage.html
- https://minorplanetcenter.net/iau/NEO/pccp_tabular.html
- https://minorplanetcenter.net/iau/NEO/toconfirm_tabular.html
- https://minorplanetcenter.net/iau/NatSats/NaturalSatellites.html
- https://minorplanetcenter.net/iau/SkyCoverage.html
- https://minorplanetcenter.net/iau/delays/neocp_delay.html
- https://minorplanetcenter.net/iau/info/MPOrbitFormat.html
- https://minorplanetcenter.net/iau/info/TechInfo.html
- https://minorplanetcenter.net/iau/lists/CometLists.html
- https://minorplanetcenter.net/iau/lists/Customize.html
- https://minorplanetcenter.net/iau/lists/Lists.html
- https://minorplanetcenter.net/iau/lists/MPLists.html
- https://minorplanetcenter.net/iau/lists/ObsCodesF.html
- https://minorplanetcenter.net/iau/lists/YearlyBreakdown.html
- https://minorplanetcenter.net/iau/mpc.html
- https://minorplanetcenter.net/iau/recovery/recovery.html
- https://minorplanetcenter.net/iau/services/MPCServices.html
- https://minorplanetcenter.net/iau/services/WebCSAccess.html
- https://minorplanetcenter.net/media/newsletters/MPC_Newsletter_Feb2026.pdf
- https://minorplanetcenter.net/mpc/summary
- https://minorplanetcenter.net/mpcops/contact/
- https://minorplanetcenter.net/mpcops/documentation/
- https://minorplanetcenter.net/mpcops/documentation/artificial-satellites/
- https://minorplanetcenter.net/mpcops/documentation/identifications/
- https://minorplanetcenter.net/mpcops/documentation/identifications/submission-format/
- https://minorplanetcenter.net/mpcops/documentation/program-codes-policy/
- https://minorplanetcenter.net/mpcops/documentation/replicated-tables-schema/
- https://minorplanetcenter.net/mpcops/mpcstatus/
- https://minorplanetcenter.net/mpcops/mpecs/
- https://minorplanetcenter.net/mpcops/neocp/neocp_plots/
- https://minorplanetcenter.net/mpcops/neocp/neocp_prev_des/
- https://minorplanetcenter.net/mpcops/orbits/
- https://minorplanetcenter.net/mpcops/orbits/no-orbits-astrometry/
- https://minorplanetcenter.net/mpcops/pointings/sky_coverage/
- https://minorplanetcenter.net/mpcops/signup/mpecs/
- https://minorplanetcenter.net/mpcops/submissions/cometary/
- https://minorplanetcenter.net/mpcops/submissions/identifications/
- https://minorplanetcenter.net/mpec/RecentMPECs.html
- https://minorplanetcenter.net/neocp_followup_report/
- https://minorplanetcenter.net/neocp_followup_reports/
- https://minorplanetcenter.net/neocp_obs
- https://minorplanetcenter.net/pointings
- https://minorplanetcenter.net/submit_action_code
- https://minorplanetcenter.net/wamo/wamo.html
- https://minorplanetcenter.net/whatsup
- https://mpc-service.atlassian.net/servicedesk/customer/portal/18
- https://mpc-service.atlassian.net/servicedesk/customer/portals
- https://mpcmug.astro.umd.edu/
- https://sbnmpc.astro.umd.edu/
- https://www.cfa.harvard.edu
- https://www.minorplanetcenter.net/iau/lists/CometResolution.html
- https://www.wgsbn-iau.org/
