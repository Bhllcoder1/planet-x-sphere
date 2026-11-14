---
source: https://dp1.lsst.io/processing/moving/ss_linking.html
fetched: 2026-11-14
status: 200
---

Small body tracklet linking and orbit fitting — DP1

[Skip to main content](#main-content)

Back to top


`Ctrl`+`K`

[![](../../_static/rubin-titlebar-imagotype-light.svg)![](../../_static/rubin-titlebar-imagotype-dark.svg)

DP1](../../index.html)

* [Overview](../../overview/index.html)
* [Data products](../../products/index.html)
* [Data processing](../index.html)
* [Data access](../../access/index.html)
* [Tutorials](../../tutorials/index.html)
* More
  + [How to cite Data Preview 1](../../citedp1.html)
  + [Rubin docs](https://www.lsst.io)

Search
`Ctrl`+`K`

* [GitHub](https://github.com/lsst/dp1_lsst_io "GitHub")

Search
`Ctrl`+`K`

* [Overview](../../overview/index.html)
* [Data products](../../products/index.html)
* [Data processing](../index.html)
* [Data access](../../access/index.html)
* [Tutorials](../../tutorials/index.html)
* [How to cite Data Preview 1](../../citedp1.html)
* [Rubin docs](https://www.lsst.io)

* [GitHub](https://github.com/lsst/dp1_lsst_io "GitHub")

Section Navigation

* [Pipeline graphs](../summary/index.html)

* [Instrument signature removal (ISR)](../isr/index.html)

* [Image calibration](../calibration/index.html)
  + [The Monster reference catalog](../calibration/monster.html)
  + [Photometric calibration](../calibration/photometric.html)
  + [Astrometric calibration](../calibration/astrometric.html)
  + [Point spread function (PSF) modeling](../calibration/psf.html)
  + [Background subtraction](../calibration/backgrounds.html)

* [Image coaddition](../coaddition/index.html)

* [Source detection and measurement](../detection/index.html)

* [Difference image analysis (DIA)](../dia/index.html)

* [Solar System processing (SSP)](index.html)
  + [Solar System prompt processing](ss_prompt.html)
  + [Small body tracklet linking and orbit fitting](#)
  + [Solar System data release processing](ss_drp.html)

* [Data processing](../index.html)
* [Solar System processing (SSP)](index.html)
* Small body tracklet linking and orbit fitting

Small body tracklet linking and orbit fitting[#](#small-body-tracklet-linking-and-orbit-fitting "Link to this heading")
=======================================================================================================================

![../../_images/LSST-HelioLinC3D-Infographic.png](../../_images/LSST-HelioLinC3D-Infographic.png)

The HelioLinC3D tracklet linking and orbit fitting package[#](#the-heliolinc3d-tracklet-linking-and-orbit-fitting-package "Link to this heading")
-------------------------------------------------------------------------------------------------------------------------------------------------

The Vera C. Rubin Observatory will detect millions of sources each night.
As part of the [Solar System prompt processing](ss_prompt.html) pipeline,
the goal of the HelioLinC3D software package is to discover asteroids amid this flood of data.
The algorithm identifies and links together little sequences of typically 6-20 sources that could comprise repeated detections of a new asteroid moving in its orbit around the Sun.
These sets of detections (called ‘linkages’) are formed in two stages.
First, ‘tracklets’ of observations are identified, where a tracklet comprises at least two images within a single night.
Next, tracklets from multiple nights are linked together.
LSST specifications state that a valid linkage must include at least three tracklets, each from a different night, and all within a 14-day period.
Each linkage meeting these criteria constitutes a candidate asteroid discovery.
After the full set of candidate linkages has been produced, they are culled and refined through orbit fitting and other analyses.
The final product is a purified set of thousands of non-overlapping linkages, each of which has an orbit-fit with sub-arcsecond astrometric residuals.
These linkages – each comprising a probable new asteroid discovery – are submitted to the [Minor Planet Center](https://minorplanetcenter.net) (MPC) for confirmation and publication.
The tracklet linking and orbit fitting procedure is illustrated in the infographic provided above.

The 24 hour processing cycle[#](#the-24-hour-processing-cycle "Link to this heading")
-------------------------------------------------------------------------------------

During operations, the tracklet linking and orbit fitting process will consist of the following steps that will repeat every 24 hours following nightly observing and before release of the Solar System Daily Data Products:

1. The nightly `DiaSource` catalog is ingested.
2. All stationary objects are removed from the nightly catalog of `DiaSources`. In addition, any individual sources that can be attributed to known moving objects with high-confidence orbits where the astrometric match between the individual source and a known object has very low uncertainty (SNR>=5) are also removed from the nightly catalog of `DiaSources`. In this manner, the moving object detections that are unattributed to any known sources are retrieved from the nightly `DiaSource` catalog to be passed to candidate tracklet identification.
3. All `DiaSources` detected on the previous night that have not been matched at a high confidence level (SNR>=5) to a known Object, DIAObject, SSObject, or an artifact, are analyzed for potential pairs that form tracklets. These tracklets span 5 - 90 minutes and consist of a minimum of 2 detections, which can be mostly spurious and have unlimited overlap.
4. Candidate tracklets are then passed to HelioLinC3D for linkage.
5. [HelioLinC3D](https://github.com/lsst-dm/heliolinc2) is run to produce linkages that include tracklets from at least three distinct nights within a period of 14 days, with unlimited overlap allowed. Each linkage must comprise at least three tracklets – that is, at least six distinct detections of the candidate asteroid.
6. The large catalog of overlapping linkages produced by HelioLinC3D is refined using [“Method of Herget” orbit fitting](https://www.projectpluto.com/herget.htm), producing a final set of non-overlapping, high-purity linkages that have sub-arcsecond astrometric residuals relative to the best-fit orbit – and still meet the requirement of including tracklets from at least three distinct nights within a 14-day time span.
7. Refined linkages are tested for associations to known objects. In this step, the short-arc orbits provided by the refined tracklet linkages are more confidently able to be associated with orbits of known objects than the individual sources tested for association prior to linking. Searches for (p)recoveries and isolated detections that can be linked to the refined linkages made by HelioLinC3D are performed. Rare false linkages are identified and rejected.
8. New discoveries and measurements of known objects are submitted to the Minor Planet Center (MPC) using the standard data-exchange protocols (e.g., the ADES format). The measurements of all `DiaSources` detected on the previous night that have been matched at a high level of confidence (SNR>=5) to a known SSObject are also submitted to the MPC.

This page was last modified on
2025-06-29.

[previous

Solar System prompt processing](ss_prompt.html "previous page")
[next

Solar System data release processing](ss_drp.html "next page")

On this page

* [The HelioLinC3D tracklet linking and orbit fitting package](#the-heliolinc3d-tracklet-linking-and-orbit-fitting-package)
* [The 24 hour processing cycle](#the-24-hour-processing-cycle)

[Edit on GitHub](https://github.com/lsst/dp1_lsst_io/edit/main/docs/processing/moving/ss_linking.rst)

© Copyright 2025 Association of Universities for Research in Astronomy, Inc. (AURA).

Created using [Sphinx](https://www.sphinx-doc.org/) 8.1.3.

Built with the [PyData Sphinx Theme](https://pydata-sphinx-theme.readthedocs.io/en/stable/index.html) 0.16.1.

## Links found on page

- https://dp1.lsst.io/access/index.html
- https://dp1.lsst.io/citedp1.html
- https://dp1.lsst.io/index.html
- https://dp1.lsst.io/overview/index.html
- https://dp1.lsst.io/processing/calibration/astrometric.html
- https://dp1.lsst.io/processing/calibration/backgrounds.html
- https://dp1.lsst.io/processing/calibration/index.html
- https://dp1.lsst.io/processing/calibration/monster.html
- https://dp1.lsst.io/processing/calibration/photometric.html
- https://dp1.lsst.io/processing/calibration/psf.html
- https://dp1.lsst.io/processing/coaddition/index.html
- https://dp1.lsst.io/processing/detection/index.html
- https://dp1.lsst.io/processing/dia/index.html
- https://dp1.lsst.io/processing/index.html
- https://dp1.lsst.io/processing/isr/index.html
- https://dp1.lsst.io/processing/moving/index.html
- https://dp1.lsst.io/processing/moving/ss_drp.html
- https://dp1.lsst.io/processing/moving/ss_prompt.html
- https://dp1.lsst.io/processing/summary/index.html
- https://dp1.lsst.io/products/index.html
- https://dp1.lsst.io/tutorials/index.html
- https://github.com/lsst-dm/heliolinc2
- https://github.com/lsst/dp1_lsst_io
- https://github.com/lsst/dp1_lsst_io/edit/main/docs/processing/moving/ss_linking.rst
- https://minorplanetcenter.net
- https://pydata-sphinx-theme.readthedocs.io/en/stable/index.html
- https://www.lsst.io
- https://www.projectpluto.com/herget.htm
- https://www.sphinx-doc.org/
