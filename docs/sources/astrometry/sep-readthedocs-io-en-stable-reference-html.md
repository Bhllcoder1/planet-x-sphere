---
source: https://sep.readthedocs.io/en/stable/reference.html
fetched: 2026-11-14
status: 200
---

Reference/API — sep 1.4.1 documentation

[Skip to main content](#main-content)

Back to top


`Ctrl`+`K`

[sep 1.4.1 documentation](index.html)

* [Tutorial](tutorial.html)
* [Matched Filter (Convolution)](filter.html)
* [Aperture photometry](apertures.html)
* [Changelog](changelogs/changelog.html)
* [Reference/API](#)

Search
`Ctrl`+`K`

Search
`Ctrl`+`K`

* [Tutorial](tutorial.html)
* [Matched Filter (Convolution)](filter.html)
* [Aperture photometry](apertures.html)
* [Changelog](changelogs/changelog.html)
* [Reference/API](#)

Section Navigation

* [sep.Background](api/sep.Background.html)
* [sep.extract](api/sep.extract.html)

* [sep.sum\_circle](api/sep.sum_circle.html)
* [sep.sum\_circann](api/sep.sum_circann.html)
* [sep.sum\_ellipse](api/sep.sum_ellipse.html)
* [sep.sum\_ellipann](api/sep.sum_ellipann.html)

* [sep.kron\_radius](api/sep.kron_radius.html)
* [sep.flux\_radius](api/sep.flux_radius.html)
* [sep.winpos](api/sep.winpos.html)
* [sep.mask\_ellipse](api/sep.mask_ellipse.html)
* [sep.ellipse\_axes](api/sep.ellipse_axes.html)
* [sep.ellipse\_coeffs](api/sep.ellipse_coeffs.html)

* [sep.get\_extract\_pixstack](api/sep.get_extract_pixstack.html)
* [sep.set\_extract\_pixstack](api/sep.set_extract_pixstack.html)
* [sep.get\_sub\_object\_limit](api/sep.get_sub_object_limit.html)
* [sep.set\_sub\_object\_limit](api/sep.set_sub_object_limit.html)

* Reference/API

Reference/API[#](#reference-api "Link to this heading")
=======================================================

**Background estimation & source detection**

|  |  |
| --- | --- |
| [`sep.Background`](api/sep.Background.html#sep.Background "sep.Background")(data[, mask, maskthresh, bw, ...]) | Representation of spatially variable image background and noise. |
| [`sep.extract`](api/sep.extract.html#sep.extract "sep.extract")(data, thresh[, err, mask, ...]) | Extract sources from an image. |

**Aperture photometry**

|  |  |
| --- | --- |
| [`sep.sum_circle`](api/sep.sum_circle.html#sep.sum_circle "sep.sum_circle")(data, x, y, r[, err, var, ...]) | Sum data in circular aperture(s). |
| [`sep.sum_circann`](api/sep.sum_circann.html#sep.sum_circann "sep.sum_circann")(data, x, y, rin, rout[, ...]) | Sum data in circular annular aperture(s). |
| [`sep.sum_ellipse`](api/sep.sum_ellipse.html#sep.sum_ellipse "sep.sum_ellipse")(data, x, y, a, b, theta, r) | Sum data in elliptical aperture(s). |
| [`sep.sum_ellipann`](api/sep.sum_ellipann.html#sep.sum_ellipann "sep.sum_ellipann")(data, x, y, a, b, theta, ...) | Sum data in elliptical annular aperture(s). |

**Aperture utilities**

|  |  |
| --- | --- |
| [`sep.kron_radius`](api/sep.kron_radius.html#sep.kron_radius "sep.kron_radius")(data, x, y, a, b, theta, r) | Calculate Kron "radius" within an ellipse. |
| [`sep.flux_radius`](api/sep.flux_radius.html#sep.flux_radius "sep.flux_radius")(data, x, y, rmax, frac[, ...]) | Return radius of a circle enclosing requested fraction of total flux. |
| [`sep.winpos`](api/sep.winpos.html#sep.winpos "sep.winpos")(data, xinit, yinit, sig[, mask, ...]) | Calculate more accurate object centroids using 'windowed' algorithm. |
| [`sep.mask_ellipse`](api/sep.mask_ellipse.html#sep.mask_ellipse "sep.mask_ellipse")(arr, x, y, a, b, theta[, r]) | Mask ellipse(s) in an array. |
| [`sep.ellipse_axes`](api/sep.ellipse_axes.html#sep.ellipse_axes "sep.ellipse_axes")(cxx, cyy, cxy) | Convert from coefficient ellipse representation to ellipse axes and angle. |
| [`sep.ellipse_coeffs`](api/sep.ellipse_coeffs.html#sep.ellipse_coeffs "sep.ellipse_coeffs")(a, b, theta) | Convert from ellipse axes and angle to coefficient representation. |

**Low-level utilities**

|  |  |
| --- | --- |
| [`sep.get_extract_pixstack`](api/sep.get_extract_pixstack.html#sep.get_extract_pixstack "sep.get_extract_pixstack")() | Get the size in pixels of the internal pixel buffer used in extract(). |
| [`sep.set_extract_pixstack`](api/sep.set_extract_pixstack.html#sep.set_extract_pixstack "sep.set_extract_pixstack")(size) | Set the size in pixels of the internal pixel buffer used in extract(). |
| [`sep.get_sub_object_limit`](api/sep.get_sub_object_limit.html#sep.get_sub_object_limit "sep.get_sub_object_limit")() | Get the limit on the number of sub-objects when deblending in extract(). |
| [`sep.set_sub_object_limit`](api/sep.set_sub_object_limit.html#sep.set_sub_object_limit "sep.set_sub_object_limit")(limit) | Set the limit on the number of sub-objects when deblending in extract(). |

**Flags**

| Flag | Description |
| --- | --- |
| `sep.OBJ_MERGED` | object is result of deblending |
| `sep.OBJ_TRUNC` | object is truncated at image boundary |
| `sep.OBJ_SINGU` | x, y fully correlated in object |
| `sep.APER_TRUNC` | aperture truncated at image boundary |
| `sep.APER_HASMASKED` | aperture contains one or more masked pixels |
| `sep.APER_ALLMASKED` | aperture contains only masked pixels |
| `sep.APER_NONPOSITIVE` | aperture sum is negative in `kron_radius` |

To see if a given flag is set in `flags`:

```
is_merged = (flags & sep.OBJ_MERGED) != 0

```

Note

The coordinate convention in SEP is that (0, 0) corresponds to the
center of the first element of the data array. This agrees with the
0-based indexing in Python and C. However, note that
this differs from the FITS convention where the center of the first
element is at coordinates (1, 1). As Source Extractor deals with
FITS files, its outputs follow the FITS convention. Thus, the
coordinates from SEP will be offset from Source Extractor
coordinates by -1 in x and y.

[previous

Original Changelog](changelogs/original_changes.html "previous page")
[next

sep.Background](api/sep.Background.html "next page")

### This Page

* [Show Source](_sources/reference.rst.txt)

© Copyright 2014-2024, Peter Watson and contributors.

Created using [Sphinx](https://www.sphinx-doc.org/) 8.1.3.

Built with the [PyData Sphinx Theme](https://pydata-sphinx-theme.readthedocs.io/en/stable/index.html) 0.16.1.

## Links found on page

- https://pydata-sphinx-theme.readthedocs.io/en/stable/index.html
- https://sep.readthedocs.io/en/stable/_sources/reference.rst.txt
- https://sep.readthedocs.io/en/stable/apertures.html
- https://sep.readthedocs.io/en/stable/api/sep.Background.html
- https://sep.readthedocs.io/en/stable/api/sep.Background.html#sep.Background
- https://sep.readthedocs.io/en/stable/api/sep.ellipse_axes.html
- https://sep.readthedocs.io/en/stable/api/sep.ellipse_axes.html#sep.ellipse_axes
- https://sep.readthedocs.io/en/stable/api/sep.ellipse_coeffs.html
- https://sep.readthedocs.io/en/stable/api/sep.ellipse_coeffs.html#sep.ellipse_coeffs
- https://sep.readthedocs.io/en/stable/api/sep.extract.html
- https://sep.readthedocs.io/en/stable/api/sep.extract.html#sep.extract
- https://sep.readthedocs.io/en/stable/api/sep.flux_radius.html
- https://sep.readthedocs.io/en/stable/api/sep.flux_radius.html#sep.flux_radius
- https://sep.readthedocs.io/en/stable/api/sep.get_extract_pixstack.html
- https://sep.readthedocs.io/en/stable/api/sep.get_extract_pixstack.html#sep.get_extract_pixstack
- https://sep.readthedocs.io/en/stable/api/sep.get_sub_object_limit.html
- https://sep.readthedocs.io/en/stable/api/sep.get_sub_object_limit.html#sep.get_sub_object_limit
- https://sep.readthedocs.io/en/stable/api/sep.kron_radius.html
- https://sep.readthedocs.io/en/stable/api/sep.kron_radius.html#sep.kron_radius
- https://sep.readthedocs.io/en/stable/api/sep.mask_ellipse.html
- https://sep.readthedocs.io/en/stable/api/sep.mask_ellipse.html#sep.mask_ellipse
- https://sep.readthedocs.io/en/stable/api/sep.set_extract_pixstack.html
- https://sep.readthedocs.io/en/stable/api/sep.set_extract_pixstack.html#sep.set_extract_pixstack
- https://sep.readthedocs.io/en/stable/api/sep.set_sub_object_limit.html
- https://sep.readthedocs.io/en/stable/api/sep.set_sub_object_limit.html#sep.set_sub_object_limit
- https://sep.readthedocs.io/en/stable/api/sep.sum_circann.html
- https://sep.readthedocs.io/en/stable/api/sep.sum_circann.html#sep.sum_circann
- https://sep.readthedocs.io/en/stable/api/sep.sum_circle.html
- https://sep.readthedocs.io/en/stable/api/sep.sum_circle.html#sep.sum_circle
- https://sep.readthedocs.io/en/stable/api/sep.sum_ellipann.html
- https://sep.readthedocs.io/en/stable/api/sep.sum_ellipann.html#sep.sum_ellipann
- https://sep.readthedocs.io/en/stable/api/sep.sum_ellipse.html
- https://sep.readthedocs.io/en/stable/api/sep.sum_ellipse.html#sep.sum_ellipse
- https://sep.readthedocs.io/en/stable/api/sep.winpos.html
- https://sep.readthedocs.io/en/stable/api/sep.winpos.html#sep.winpos
- https://sep.readthedocs.io/en/stable/changelogs/changelog.html
- https://sep.readthedocs.io/en/stable/changelogs/original_changes.html
- https://sep.readthedocs.io/en/stable/filter.html
- https://sep.readthedocs.io/en/stable/index.html
- https://sep.readthedocs.io/en/stable/tutorial.html
- https://www.sphinx-doc.org/
