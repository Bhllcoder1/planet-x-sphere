---
source: https://astroalign.quatrope.org/en/latest/
fetched: 2026-11-14
status: 200
---

Astroalign documentation — astroalign 2.6.2 documentation

[astroalign](#)

* [Installation](installation.html)
* [Tutorial](tutorial.html)
* [Selecting regions with masking](mask.html)
* [Examples](examples.html)
* [Module API](api.html)

[astroalign](#)

* Astroalign documentation
* [View page source](_sources/index.rst.txt)

---

[![_images/logo-seal-dark-light.png](_images/logo-seal-dark-light.png)](_images/logo-seal-dark-light.png)

Astroalign documentation[](#astroalign-documentation "Link to this heading")
=============================================================================

**ASTROALIGN** is a python module that will try to register (align) two stellar astronomical images,
especially when there is no WCS information available.

It does so by finding similar 3-point asterisms (triangles) in both images and estimating the
affine transformation between them.

Generic registration routines try to match point features, using corner detection routines to make the point correspondence.
These generally fail for stellar astronomical images, since stars have very little stable structure and so, in general, indistinguishable from each other.
Asterism matching is more robust, and closer to the human way of matching stellar images.

Because of the geometric nature of its core algorithm, it is not greatly effected by point-spread function differences, seeing or atmospheric conditions.

You can find a Jupyter notebook example with the main features at <http://quatrope.github.io/astroalign>.

Note

It may not work, or work with special care, on images of extended objects with few point-like sources or in very crowded fields.

Note

If your images contain a large number of hot pixels, this may result in an incorrect registration.
Please refer to the tutorial for how to solve this problem using [CCDProc’s cosmic-ray remover](https://ccdproc.readthedocs.io/en/latest/api/ccdproc.cosmicray_lacosmic.html).

Citation[](#citation "Link to this heading")
---------------------------------------------

If you use astroalign in a scientific publication, we would appreciate
citations to the following paper:

> Astroalign: A Python module for astronomical image registration.
> Beroiz, M., Cabral, J. B., & Sanchez, B.
> Astronomy and Computing, Volume 32, July 2020, 100384.

Bibtex entry:

```
@article{BEROIZ2020100384,
title = "Astroalign: A Python module for astronomical image registration",
journal = "Astronomy and Computing",
volume = "32",
pages = "100384",
year = "2020",
issn = "2213-1337",
doi = "https://doi.org/10.1016/j.ascom.2020.100384",
url = "http://www.sciencedirect.com/science/article/pii/S221313372030038X",
author = "M. Beroiz and J.B. Cabral and B. Sanchez",
keywords = "Astronomy, Image registration, Python package",
abstract = "We present an algorithm implemented in the Astroalign Python module for image registration     in astronomy. Our module does not rely on WCS information and instead matches three-point asterisms (    triangles) on the images to find the most accurate linear transformation between them. It is especially     useful in the context of aligning images prior to stacking or performing difference image analysis.     Astroalign can match images of different point-spread functions, seeing, and atmospheric conditions."
}

```

**Full Publication:** <https://www.sciencedirect.com/science/article/pii/S221313372030038X>

Or cite the project itself from [ASCL](http://ascl.net/1906.001):

> Beroiz, M. I. (2019). Astroalign: Asterism-matching alignment of
> astronomical images. Astrophysics Source Code Library.

Bibtex:

```
@article{beroiz2019astroalign,
    title={Astroalign: Asterism-matching alignment of astronomical images},
    author={Beroiz, Martin I},
    journal={Astrophysics Source Code Library},
    year={2019}
}

```

### Guide:[](#guide "Link to this heading")

* [Installation](installation.html)
* [Tutorial](tutorial.html)
  + [A simple usage example](tutorial.html#a-simple-usage-example)
  + [Images with RGB channels](tutorial.html#images-with-rgb-channels)
  + [Mask Fill Value](tutorial.html#mask-fill-value)
  + [Finding the transformation](tutorial.html#finding-the-transformation)
  + [If you know the star-to-star correspondence](tutorial.html#if-you-know-the-star-to-star-correspondence)
  + [Applying a transformation to a set of points](tutorial.html#applying-a-transformation-to-a-set-of-points)
  + [Objects with `data` and `mask` property](tutorial.html#objects-with-data-and-mask-property)
* [Selecting regions with masking](mask.html)
  + [Masking out undesired regions](mask.html#masking-out-undesired-regions)
* [Examples](examples.html)
  + [Very few stars on the field](examples.html#very-few-stars-on-the-field)
  + [Faint stars](examples.html#faint-stars)
  + [Avoiding hot pixels and other CCD artifacts](examples.html#avoiding-hot-pixels-and-other-ccd-artifacts)
* [Module API](api.html)
  + [`MIN_MATCHES_FRACTION`](api.html#astroalign.MIN_MATCHES_FRACTION)
  + [`MaxIterError`](api.html#astroalign.MaxIterError)
  + [`NUM_NEAREST_NEIGHBORS`](api.html#astroalign.NUM_NEAREST_NEIGHBORS)
  + [`PIXEL_TOL`](api.html#astroalign.PIXEL_TOL)
  + [`apply_transform()`](api.html#astroalign.apply_transform)
  + [`estimate_transform()`](api.html#astroalign.estimate_transform)
  + [`find_transform()`](api.html#astroalign.find_transform)
  + [`matrix_transform()`](api.html#astroalign.matrix_transform)
  + [`register()`](api.html#astroalign.register)

Indices and tables[](#indices-and-tables "Link to this heading")
=================================================================

* [Index](genindex.html)
* [Search Page](search.html)

[Next](installation.html "Installation")

---

© Copyright 2017, Martin Beroiz.

Built with [Sphinx](https://www.sphinx-doc.org/) using a
[theme](https://github.com/readthedocs/sphinx_rtd_theme)
provided by [Read the Docs](https://readthedocs.org).

## Links found on page

- http://ascl.net/1906.001
- http://quatrope.github.io/astroalign
- https://astroalign.quatrope.org/en/latest/_images/logo-seal-dark-light.png
- https://astroalign.quatrope.org/en/latest/_sources/index.rst.txt
- https://astroalign.quatrope.org/en/latest/api.html
- https://astroalign.quatrope.org/en/latest/api.html#astroalign.MIN_MATCHES_FRACTION
- https://astroalign.quatrope.org/en/latest/api.html#astroalign.MaxIterError
- https://astroalign.quatrope.org/en/latest/api.html#astroalign.NUM_NEAREST_NEIGHBORS
- https://astroalign.quatrope.org/en/latest/api.html#astroalign.PIXEL_TOL
- https://astroalign.quatrope.org/en/latest/api.html#astroalign.apply_transform
- https://astroalign.quatrope.org/en/latest/api.html#astroalign.estimate_transform
- https://astroalign.quatrope.org/en/latest/api.html#astroalign.find_transform
- https://astroalign.quatrope.org/en/latest/api.html#astroalign.matrix_transform
- https://astroalign.quatrope.org/en/latest/api.html#astroalign.register
- https://astroalign.quatrope.org/en/latest/examples.html
- https://astroalign.quatrope.org/en/latest/examples.html#avoiding-hot-pixels-and-other-ccd-artifacts
- https://astroalign.quatrope.org/en/latest/examples.html#faint-stars
- https://astroalign.quatrope.org/en/latest/examples.html#very-few-stars-on-the-field
- https://astroalign.quatrope.org/en/latest/genindex.html
- https://astroalign.quatrope.org/en/latest/installation.html
- https://astroalign.quatrope.org/en/latest/mask.html
- https://astroalign.quatrope.org/en/latest/mask.html#masking-out-undesired-regions
- https://astroalign.quatrope.org/en/latest/search.html
- https://astroalign.quatrope.org/en/latest/tutorial.html
- https://astroalign.quatrope.org/en/latest/tutorial.html#a-simple-usage-example
- https://astroalign.quatrope.org/en/latest/tutorial.html#applying-a-transformation-to-a-set-of-points
- https://astroalign.quatrope.org/en/latest/tutorial.html#finding-the-transformation
- https://astroalign.quatrope.org/en/latest/tutorial.html#if-you-know-the-star-to-star-correspondence
- https://astroalign.quatrope.org/en/latest/tutorial.html#images-with-rgb-channels
- https://astroalign.quatrope.org/en/latest/tutorial.html#mask-fill-value
- https://astroalign.quatrope.org/en/latest/tutorial.html#objects-with-data-and-mask-property
- https://ccdproc.readthedocs.io/en/latest/api/ccdproc.cosmicray_lacosmic.html
- https://github.com/readthedocs/sphinx_rtd_theme
- https://readthedocs.org
- https://www.sciencedirect.com/science/article/pii/S221313372030038X
- https://www.sphinx-doc.org/
