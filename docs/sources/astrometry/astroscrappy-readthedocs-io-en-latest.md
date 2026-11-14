---
source: https://astroscrappy.readthedocs.io/en/latest/
fetched: 2026-11-14
status: 200
---

ASTROSCRAPPY — astroscrappy v1.1.1.dev6+g2dfdc15

[astroscrappy:docs](# "Documentation Home")


* [Index](genindex.html "General Index")
* [Modules](py-modindex.html "Module Index")

### Navigation

* [next »](api/astroscrappy.detect_cosmics.html "detect_cosmics")
* [astroscrappy v1.1.1.dev6+g2dfdc15](#)
  »

ASTROSCRAPPY[¶](#astroscrappy "Permalink to this headline")
===========================================================

astroscrappy Package[¶](#module-astroscrappy "Permalink to this headline")
--------------------------------------------------------------------------

### Astro-SCRAPPY: The Speedy Cosmic Ray Annihilation Package in Python[¶](#astro-scrappy-the-speedy-cosmic-ray-annihilation-package-in-python "Permalink to this headline")

An optimized cosmic ray detector

Author
:   Curtis McCully

Astro-SCRAPPY is designed to detect cosmic rays in images (numpy arrays),
originally based on Pieter van Dokkum’s L.A.Cosmic algorithm.

Much of this was originally adapted from cosmics.py written by Malte Tewes.
I have ported all of the slow functions to Cython/C, and optimized
where I can. This is designed to be as fast as possible so some of the
readability has been sacrificed, specifically in the C code.

L.A.Cosmic = LAplacian Cosmic ray detection

If you use this code, please cite the Zendo DOI: <https://zenodo.org/record/1482019>

Please cite the original paper which can be found at:
<http://www.astro.yale.edu/dokkum/lacosmic/>

van Dokkum 2001, PASP, 113, 789, 1420
(article : <http://adsabs.harvard.edu/abs/2001PASP..113.1420V>)

This code requires Cython, preferably version >= 0.21.

Parallelization is achieved using OpenMP. This code should compile (although
the Cython files may have issues) using a compiler that does not support OMP,
e.g. clang.

#### Notes[¶](#notes "Permalink to this headline")

There are some differences from original LACosmic:

> * Automatic recognition of saturated stars.
>   This avoids treating such stars as large cosmic rays.
> * I have tried to optimize all of the code as much as possible while
>   maintaining the integrity of the algorithm. One of the key speedups is to
>   use a separable median filter instead of the true median filter. While these
>   are not identical, they produce comparable results and the separable version
>   is much faster.
> * This implementation is much faster than the Python by as much as a factor of
>   28 depending on the given parameters.
>   This implementation is much faster than the original IRAF version, by a factor
>   of ~90.

Note that arrays always must be C-contiguous, thus all loops are y outer, x inner.
This follows the Pyfits convention.

scipy is required for certain tests to pass, but the code itself does not depend on
scipy.

### Functions[¶](#functions "Permalink to this headline")

|  |  |
| --- | --- |
| [`detect_cosmics`](api/astroscrappy.detect_cosmics.html#astroscrappy.detect_cosmics "astroscrappy.detect_cosmics")(indat[, inmask, inbkg, ...]) | Detect cosmic rays in a numpy array. |

### Page Contents

* [ASTROSCRAPPY](#)
  + [astroscrappy Package](#module-astroscrappy)
    - [Astro-SCRAPPY: The Speedy Cosmic Ray Annihilation Package in Python](#astro-scrappy-the-speedy-cosmic-ray-annihilation-package-in-python)
      * [Notes](#notes)
    - [Functions](#functions)

[Page Source](_sources/index.rst.txt)  
[Back to Top](#)

© Copyright 2021, Curtis McCully.  
Created using [Sphinx](http://www.sphinx-doc.org/en/stable/) 4.3.0.  
Last built 23 Nov 2021.

## Links found on page

- http://adsabs.harvard.edu/abs/2001PASP..113.1420V
- http://www.astro.yale.edu/dokkum/lacosmic/
- http://www.astropy.org
- http://www.sphinx-doc.org/en/stable/
- https://astroscrappy.readthedocs.io/en/latest/_sources/index.rst.txt
- https://astroscrappy.readthedocs.io/en/latest/api/astroscrappy.detect_cosmics.html
- https://astroscrappy.readthedocs.io/en/latest/api/astroscrappy.detect_cosmics.html#astroscrappy.detect_cosmics
- https://astroscrappy.readthedocs.io/en/latest/genindex.html
- https://astroscrappy.readthedocs.io/en/latest/py-modindex.html
- https://zenodo.org/record/1482019
