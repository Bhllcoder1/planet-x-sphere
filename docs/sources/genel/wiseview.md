---
source: http://byw.tools/wiseview
fetched: 2026-11-14
status: 200
---

Settings
Links
Help
About

Right ascension and declination

Field of View (arcseconds)

W1W2W1+W2Band[s]

Apply defaults

Sliding window ( yrs)

Blink interval ( ms)

Zoom ()

Min - max pixel values:

Stretch Linearity ()

Invert pixel values

Maximize dynamic range

Separate scan directions

Use only NEOWISE imagery

Skip middle epochs

Skip duplicate windows

Smooth by scan direction

Border epoch 0

Gaia DR3 overlay

Difference imaging

Shift and add

Synthetic Object

Synthetic Object

*WiseView is operated by the [American Museum of Natural History](https://www.amnh.org/)*

*WiseView is designed for Chrome, and has known issues in IE*

[LegacySurvey Sky Viewer](http://legacysurvey.org/viewer#NGC%203413)
[Simbad](http://simbad.u-strasbg.fr/simbad/sim-fcoo)
[Vizier](http://vizier.u-strasbg.fr/viz-bin/VizieR)
Nearest Zooniverse Subjects:

...

Help
====

See our [tutorial video for Wiseview-V1](https://www.youtube.com/watch?v=23hXbfh1_aA) by Guillaume Colin. V1 Cheat Sheet down below.

Wiseview is designed for quick visualization of moving objects in unWISE images. It is built for Chrome, and may have Surprise Bugs in other browsers.

To get started, enter your coordinates, in either degrees decimal or sexegesiaml h:m:s d:m:s format, into the top text bar. Sexegesimal coordinates may be separated by colons (1:2:3.45), spaces (1 2 3.45), or letter designators (1h2m3.45s).

Choose how large of an image (***Field of view***) to display, in arcseconds. The image can be scaled up or down with the ***Zoom*** slider, and the animation made faster by reducing the ***Blink interval*** slider. Wiseview can display either the W1 or W2 bands in greyscal, or W1+W2 in a colored image where red gets W2, blue gets W1, and green gets the average of W1 and W2.

The plusses, minuses, and periods (+, -, .) between the sidebar and the unWISE images are the ***epoch legend***. They show which epochs are added (+), subtracted (-), or not used (.) in the current frame. A ***dashed border*** appears whenever the animation resets to help visually distinguish when moving objects are truly moving in a consistent direction, and not hopping back halfway through the animation. The dashed border may be disabled in advanced settings.

***Click on the image to move***. Click and drag to open a new tab with a different field of view. Hold down the control key (Windows) or command key (Mac) to open tabs in the background with Chrome. New tabs can also be used to get coordinates when there are multiple interesting areas within a large field of view.

| V1 Mode | V2 Equivalent Settings |
| --- | --- |
|  | Check "Invert pixel values" and "Skip duplicate windows" (or hit Defaults) |
| time-resolved | Move Window slider all the way left |
| full-depth | Move Window slider all the way right (or visit legacysurvey.org/viewer) |
| **window-\*-year** | **Default**, move Window slider somewhere in the middle |
| pre-post | Check "Skip middle epochs" |
| window-\*-year-para... | Check "Separate scan directions" |
| parallax-enhancing | Check "Separate scan directions" and move the Window slider all the way right |
| swindow-\*-year | Check "Difference imaging" |
| shift-and-add | Not yet implemented |
| parallax-cancelling-\* | Not implemented |

About
=====

Images sourced by [unWISE](http://unwise.me)[1,2,3] (top) and [Pan-STARRS](https://panstarrs.stsci.edu/) (bottom).

unWISE images are then stretched with [astropy.visualization.AsinhStretch](http://docs.astropy.org/en/stable/api/astropy.visualization.AsinhStretch.html#astropy.visualization.AsinhStretch), where the "Linear" slider controls the "a" parameter. "Trim Bright" changes the maximum intensity before stretching. In "percent" mode, "Trim Bright" scales to the "Trim Bright" percentile, whereas "fixed" sets an absolute maximum intensity. For example, "percent" with "99.5" caps the intensity to that of the 99.5th percentile pixel, whereas "fixed" with "1000" caps it at 1000. "adapt" attempts to find good minimum and maximum values automatically, and does not take a "Trim Bright" input.

To replicate legacy wiseview behavior, use either "fixed" or "percent" (instead of legacy "Brighten"), and set "linear" = 1.

Band W1 and W2 correspond to WISE bands. "Bands W1+W2" displays a color image where W1 is blue and W2 is red.

This site is authored by Dan Caselden and Paul Westin. For questions, you may contact this gmail address: dancaselden

[1] unWISE AllWISE: <http://adsabs.harvard.edu/abs/2014AJ....147..108L>

[2] unWISE NEO1: <http://adsabs.harvard.edu/abs/2017AJ....153...38M>

[3] unWISE NEO2: <http://adsabs.harvard.edu/abs/2017arXiv170506746M>

Loading...

## Links found on page

- http://adsabs.harvard.edu/abs/2014AJ....147..108L
- http://adsabs.harvard.edu/abs/2017AJ....153...38M
- http://adsabs.harvard.edu/abs/2017arXiv170506746M
- http://docs.astropy.org/en/stable/api/astropy.visualization.AsinhStretch.html#astropy.visualization.AsinhStretch
- http://legacysurvey.org/viewer#NGC%203413
- http://simbad.u-strasbg.fr/simbad/sim-fcoo
- http://unwise.me
- http://vizier.u-strasbg.fr/viz-bin/VizieR
- https://panstarrs.stsci.edu/
- https://ps1images.stsci.edu/cgi-bin/ps1cutouts
- https://www.amnh.org/
- https://www.youtube.com/watch?v=23hXbfh1_aA
