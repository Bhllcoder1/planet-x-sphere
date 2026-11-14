---
source: https://ar5iv.arxiv.org/html/1509.00677
fetched: 2026-11-14
status: 200
---

[1509.00677] Performance analysis of the Least-Squares estimator in
Astrometry

Performance analysis of the Least-Squares estimator in
AstrometryNote: To be submitted to PASP
==============================================================================================

Rodrigo A. Lobos, Jorge F. Silva
Affiliation: Departamento de
Ingeniería Eléctrica, Facultad de Ciencias Físicas y
Matemáticas,
  
Universidad de Chile, Beauchef 850, Santiago, Chile
Email: [rlobos, josilva @ing.uchile.cl](mailto:rlobos,%20josilva%20@ing.uchile.cl)
  
Rene A. Mendez
Affiliation: Departamento de Astronomía, Facultad de Ciencias
Físicas y Matemáticas,
  
Universidad de Chile, Casilla 36-D,
Santiago, Chile
Email: [rmendez@u.uchile.cl](mailto:rmendez@u.uchile.cl)
  
Marcos Orchard
Affiliation: Departamento de
Ingeniería Eléctrica, Facultad de Ciencias Físicas y
Matemáticas,
  
Universidad de Chile, Beauchef 850, Santiago, Chile
Email: [morchard@ing.uchile.cl](mailto:morchard@ing.uchile.cl)

###### Abstract

We characterize the performance of the widely-used least-squares
estimator in astrometry in terms of a comparison with the Cramér-Rao lower
variance bound. In this inference context the performance of the
least-squares estimator does not offer a closed-form expression, but a
new result is presented (Theorem [1](#Thmtheorem1 "Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) where
both the bias and the mean-square-error of the least-squares estimator
are bounded and approximated analytically, in the latter case in terms
of a nominal value and an interval around it. From the predicted
nominal value we analyze how efficient is the least-squares estimator
in comparison with the minimum variance Cramér-Rao bound. Based on our
results, we show that, for the high signal-to-noise ratio regime, the
performance of the least-squares estimator is significantly poorer
than the Cramér-Rao bound, and we characterize this gap analytically. On
the positive side, we show that for the challenging low
signal-to-noise regime (attributed to either a weak astronomical
signal or a noise-dominated condition) the least-squares estimator is
near optimal, as its performance asymptotically approaches the
Cramér-Rao bound. However, we also demonstrate that, in general, there is
no unbiased estimator for the astrometric position that can precisely
reach the Cramér-Rao bound. We validate our theoretical analysis through
simulated digital-detector observations under typical observing
conditions. We show that the nominal value for the
mean-square-error of the least-squares estimator (obtained from our
theorem) can be used as a benchmark indicator of the expected
statistical performance of the least-squares method under a wide range
of conditions. Our results are valid for an idealized linear
(one-dimensional) array detector where intra-pixel response changes
are neglected, and where flat-fielding is achieved with very high
accuracy.

###### Keywords:

Astrometry, parameter estimation, Cramér-Rao bound,
Least-Squares estimator, performance analysis.

I Motivation
------------

Astrometry, that branch of observational astronomy that deals with the
precise and accurate estimation of angular positions of light-emitting
(usually point-like) sources projected against the celestial sphere,
is the oldest technique employed in the study of the heavens
([Høg 2009](#bib.bib16); [Reffert 2009](#bib.bib42); [Høg 2011](#bib.bib17)). Repeated measurements of
positions, spread over time, allow a determination of the motions and
distances of theses sources, with astrophysical implications on
dynamical studies of stellar systems and the Milky Way as a
whole. With the advent of solid-state detectors and all-digital
techniques applied to radio-interferometry and specialized ground- and
space-based missions, astrometry has been revolutionized in recent
years, as we have entered a high-precision era in which this technique
has started to play an increasingly important role in all areas of
astronomy, astrophysics ([van Altena 2013](#bib.bib48)), and cosmology
([Lattanzi 2012](#bib.bib25)).

Current technology, based on two-dimensional discrete digital
detectors (such as charged coupled devices - CCDs), record a
(noisy) image (on an array of photo-sensitive pixels) of celestial
sources, from which it is possible to estimate both their astrometry
and photometry, simultaneously ([Howell 2006](#bib.bib19)). The
inference problem associated to the determination of these quantities
is at the core of the astrometric endeavor described previously.

A number of techniques have been proposed to estimate the location and
flux of celestial sources as recorded on digital detectors. In this
context, estimators based on the use of a least-squares error function
(LS hereafter) have been widely adopted
([Stetson 1987](#bib.bib44); [King 1983](#bib.bib24); [Alard &
Lupton 1998](#bib.bib2); [Honeycutt 1992](#bib.bib18); [Cameron
et al. 2006](#bib.bib7)). The
use of this type of decision rule has been traditionally justified
through heuristic reasons and because they are conceptually
straightforward to formulate based on the observation model of these
problems. Indeed, the LS approach was the classical method used when
the observations were obtained with analog devices
([van Altena &
Auer 1975](#bib.bib47); [Auer &
van Altena 1978](#bib.bib3)) (which corresponds to a Gaussian noise
model for the observations, different from that of modern digital
detectors, which is characterized instead by a Poisson statistics)
and, consequently, the LS method was naturally adopted from the
analogous to the digital observational setting111
See footnote
11 in Section [III.1](#S3.SS1 "III.1 Non achievability ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")..

In contemporary astrometry (Gaia, for instance), stellar positions
will be obtained by optimizing a likelihood function (see, e.g.,
[Lindegren 2000](#bib.bib28), which uses the equivalent of our
equations ([5](#S2.E5 "In II.1 Astrometry and photometry based on a photon integrating device ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) and ([13](#S3.E13 "In III.1 Non achievability ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) in
Sections [II.1](#S2.SS1 "II.1 Astrometry and photometry based on a photon integrating device ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry") and [III.1](#S3.SS1 "III.1 Non achievability ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")
respectively), not by LS. Nevertheless, since LS methods offer
computationally efficient implementations and have shown reasonable
performance ([Lee &
van Altena 1983](#bib.bib26); [Stone 1989](#bib.bib45)) they are still widely
used in astrometry either on general-purpose software packages for the
analysis of digital images such as DAOPHOT ([Stetson 1987](#bib.bib44)),
or on dedicated pipelines, such as that adopted in the Sloan Digital
Sky Survey survey (SDSS hereafter,
[Lupton et al. 2001](#bib.bib30); [Lupton 2007](#bib.bib31)). For example, in DAOPHOT astrometry
(and photometry) are obtained through a two-step process which
involves a LS minimization of a trial function (e.g., a bi-dimensional
Gaussian, see [Stetson 1987](#bib.bib44), equivalent to
our one-dimensional case in equation ([16](#S3.E16 "In III.1 Non achievability ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")),
Section [III.1](#S3.SS1 "III.1 Non achievability ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")), and then applying a correction by means
of an empirically determined look-up table (also computed performing a
LS on a set of high signal-to-noise ratio images distributed over the
field of view of the image, see
[Stetson 1987](#bib.bib44)). This last step accounts for
the fact that the PSF of the image under analysis may not be exactly
Gaussian. The SDSS pipeline ([Lupton et al. 2001](#bib.bib30)) obtains its
centroids also through a two-step process: First it fits a
Karhunen-Loève transform (KL transform hereafter222
Also
referred to as “principal component analysis”, “proper orthogonal
decomposition”, “empirical orthogonal functions” (a term used in
meteorology and geophysics), or the Hotelling transform, see
[Gray &
Davisson 2010](#bib.bib15)., see, e.g., [Najim 2008](#bib.bib37)) to a set of
isolated bright stars in the field-of-view of the image, and then it
uses the base functions determined in this way, to fit the astrometry
and photometry for the object(s) under consideration using a LS
minimization scheme (see [Lupton 2007](#bib.bib31)). Both
codes, DAOPHOT and the SDSS pipeline have been extensively used and
tested by the astronomical community, giving very reliable results
(see, e.g., [Pier et al. 2003](#bib.bib39); [Becker et al. 2007](#bib.bib5)).

Considering that LS methods are still in use in astrometry, and driven
by the increase in the intrinsic precision available by the new
detectors and instrumental settings, and by the fact that CCDs will
likely continue to be the detector of choice for the focal-plane in
science-quality imaging application at optical wavelengths for both
space- as well as ground-borne programs333
See, e.g.,
http://www.bnl.gov/cosmo2013/, it is timely to re-visit the
pertinence of the use of LS estimators. Indeed, in the digital
setting, where we observe discrete samples (or counts) on a photon
integrating device, there is no formal justification that the LS
approach is optimal in the sense of minimizing the mean-square-error
(MSE) of the parameter estimation, in particular for astrometry, which
is the focus of this work.

The question of optimality (in some statistical sense) has always been
in the interest of the astronomical community, in particular the idea
of characterizing fundamental performance bounds that can be used to
analyze the efficiency of the adopted estimation schemes. In this
context, we can mention some seminal works on the use of the
celebrated Cramér-Rao (CR hereafter) bound in astronomy by
[Lindegren 1978](#bib.bib27); [Jakobsen et al. 1992](#bib.bib20); [Zaccheo
et al. 1995](#bib.bib50); [Adorf 1996](#bib.bib1); and
[Bastian 2004](#bib.bib4). The CR bound is a minimum variance (MV) bound
for the family of unbiased estimators
([Rao 1945](#bib.bib40); [Cramér 1946](#bib.bib10)). In
astrometry and photometry this bound has offered meaningful
closed-form expressions that can be used to analyze the complexity of
the inference task, and its dependency on key observational and design
parameters such as the position of the object in the array, the
intensity of the object, the signal-to-noise ratio (SNR hereafter),
and the resolution of the instrument
([Winick 1986](#bib.bib49); [Perryman
et al. 1989](#bib.bib38); [Lindegren 2010](#bib.bib29); [Mendez
et al. 2013](#bib.bib34); [Mendez
et al. 2014](#bib.bib35)).
In particular, for photometry, [Perryman
et al. 1989](#bib.bib38) used the CR bound
to show that the LS estimator is a good estimator, achieving a
performance close to the limit in a wide range of observational
regimes, and approaching very closely the bound at low SNR. In
astrometry, on the other hand, [Mendez
et al. 2013](#bib.bib34); [Mendez
et al. 2014](#bib.bib35) have
recently studied the structure of this bound and have analyzed its
dependency with respect to important observational parameters, under
realistic astronomical observing conditions. In those works,
closed-form expressions for the bound were derived in a number of
important settings (high spatial resolution, low and high SNR), and
their trends were explored across angular resolution and the position
of the object in the array. As an interesting outcome, the analysis
of the CR bound allows us to find the optimal pixel resolution of the
array for a given setting, as well as providing formal justification
to some heuristic techniques commonly used to improve performance in
astrometry, like dithering for undersampled images
([Mendez
et al. 2013](#bib.bib34), Sec. 3.3).

The specific problem of evaluating the existence of an estimator that
achieves the CR bound has not been covered in the literature, and
remains an interesting open problem. On this, [Mendez
et al. 2013](#bib.bib34) have
empirically assessed (using numerical simulations) the performance of
two LS methods and the maximum-likelihood (ML hereafter) estimator,
showing that their variances follow very closely the CR limit in some
specific regimes. In this paper, we analyze in detail the performance
of the LS estimator with respect to the CR bound, with the goal of
finding concrete regimes, if any, where this estimator approaches the
CR bound and, consequently, where it can be considered an efficient
solution to the astrometric problem. This application is a challenging
one, because estimators based on a LS type of objective function do
not have a closed-form expression in astrometry. In fact, this
estimation approach corresponds to a non linear regression problem,
where the resulting estimator is implicitly defined. As a result, no
expressions for the performance of the LS estimator can be obtained
analytically.
To address this issue, our main result (Theorem
[1](#Thmtheorem1 "Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry"), Section [III.2](#S3.SS2 "III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) derives
expressions that bound and approximate the variance of the LS
estimator. Our approach is based on the work by [So et al. 2013](#bib.bib43), where
the authors tackle the problem of approximating the bias and MSE of
general estimators that are the solution of an optimization
problem. In [Fessler 1996](#bib.bib11) another methodology is given to
approximate the variance and mean of implicitly defined estimators,
which has been applied to medical imaging and acoustic source
localization ([Raykar et al. 2005](#bib.bib41)).

The main result of our paper is a refined version of the result
presented in [So et al. 2013](#bib.bib43), where one of their key assumptions,
which is not applicable in our estimation problem, is reformulated. In
this process, we derive lower and upper bounds for the MSE performance
of the LS estimator. Using these bounds, we analyze how closely the
performance of the LS estimator approaches the CR bound across
different observational regimes. We show that for high SNR there is a
considerable gap between the CR bound and the performance of the LS
estimator. Remarkably, we show that for the more challenging low SNR
observational regime (weak astronomical sources), the LS estimator is
near optimal, as its performance is arbitrarily close to the CR bound.

The paper is organized as follows. Section [II](#S2 "II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry") introduces
the problem, notation, as well as some preliminary results. Section
[III](#S3 "III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry") represents the main contribution, where Theorem
[1](#Thmtheorem1 "Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry") and its interpretation are introduced.
Section [IV](#S4 "IV Numerical analysis of the LS estimator ‣ Performance analysis of the Least-Squares estimator in
Astrometry") shows numerical analyses of the
performance of LS estimator under different observational regimes.
Finally Section [V](#S5 "V Summary and Final Remarks ‣ Performance analysis of the Least-Squares estimator in
Astrometry") provides a summary of our results, and
some final remarks.

II Introduction and preliminaries
---------------------------------

In this section we introduce the problem of astrometry
as well as concepts and definitions that will be used throughout the
paper. For simplicity, we focus on the 1-D scenario of a linear array
detector, as it captures the key conceptual elements of the
problem444
This analysis can be extended to the 2-D case as
shown in [Mendez
et al. 2013](#bib.bib34)..

### II.1 Astrometry and photometry based on a photon integrating device

The specific problem of interest is the inference of the position of a
point source. This source is parameterized by two scalar quantities,
the position of the object xc∈ℝx\_{c}\in\mathbb{R} in the
array555
This is of course related to an angular position in the
sky, measured in arcsec, through the “plate-scale”, which is an
optical design feature determined by the instrument plus telescope
configuration., and its intensity (or brightness, or flux) that we
denote by F~∈ℝ+\tilde{F}\in\mathbb{R}^{+}. These two parameters induce a
probability μxc,F~\mu\_{x\_{c},\tilde{F}} over an observation space that we
denote by 𝕏\mathbb{X}. More precisely, given a point source
represented by the pair (xc,F~)(x\_{c},\tilde{F}), it creates a nominal
intensity profile in a photon integrating device, typically a CCD,
which can be generally written as:

|  |  |  |  |
| --- | --- | --- | --- |
|  | F~xc,F~(x)=F~⋅ϕ⁡(x−xc,σ),\tilde{F}\_{x\_{c},\tilde{F}}(x)=\tilde{F}\cdot\phi(x-x\_{c},\sigma), |  | (1) |

where ϕ⁡(x−xc,σ)\phi(x-x\_{c},\sigma) denotes the one dimensional normalized
point spread function (PSF) evaluated on the pixel coordinate x−xcx-x\_{c},
and where σ\sigma is a generic parameter that determines the width
(or spread) of the light distribution on the detector (typically a
function of wavelength and the quality of the observing site, see
Section [IV](#S4 "IV Numerical analysis of the LS estimator ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) (see [Mendez
et al. 2013](#bib.bib34); [Mendez
et al. 2014](#bib.bib35) for
more details).

The profile in equation ([1](#S2.E1 "In II.1 Astrometry and photometry based on a photon integrating device ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) is not observed directly, but
through three sources of perturbations: First, an additive background
which accounts for the photon emissions of the open (diffuse) sky and
the contributions from the noise of the instrument itself (the
read-out noise and dark-current ([Gilliland 1992](#bib.bib13); [Tyson 1986](#bib.bib46)))
modeled by B~i\tilde{B}\_{i} in equation ([2](#S2.E2 "In II.1 Astrometry and photometry based on a photon integrating device ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")). Second, an
intrinsic uncertainty between the aggregated intensity (the nominal
object brightness plus the background) and the actual measurements,
denoted by IiI\_{i} in what follows, which is modeled by independent
random variables that obey a Poisson probability law. And, finally, we
need to consider the spatial quantization process associated with the
pixel-resolution of the detector as specified by gi(xc)g\_{i}(x\_{c}) in
equations ([2](#S2.E2 "In II.1 Astrometry and photometry based on a photon integrating device ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) and ([3](#S2.E3 "In II.1 Astrometry and photometry based on a photon integrating device ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry"))666
Note
that pixel-convolved point-spread function gi(xc)g\_{i}(x\_{c}) is sometimes
referred to as the the ”pixel response function”.. Including
these three effects, we have a countable collection of independent and
not identically distributed random variables (observations or counts)
{Ii:i∈ℤ}\left\{I\_{i}:i\in\mathbb{Z}\right\}, where Ii∼Poisson(λi(xc,F~))I\_{i}\sim Poisson(\lambda\_{i}(x\_{c},\tilde{F})), driven by the expected intensity
at each pixel element ii, given by:

|  |  |  |  |
| --- | --- | --- | --- |
|  | λi(xc,F~)≡𝔼⁡{Ii}=F~⋅gi(xc)⏟≡F~i(xc,F~)+B~i,∀i∈ℤ\lambda\_{i}(x\_{c},\tilde{F})\equiv\mathbb{E}\{I\_{i}\}=\underbrace{\tilde{F}\cdot g\_{i}(x\_{c})}\_{\equiv\tilde{F}\_{i}(x\_{c},\tilde{F})}+\tilde{B}\_{i},~\forall i\in\mathbb{Z} |  | (2) |

and,

|  |  |  |  |
| --- | --- | --- | --- |
|  | gi(xc)≡∫xi−Δx/2xi+Δx/2ϕ⁡(x−xc,σ)𝑑x,∀i∈ℤ,g\_{i}(x\_{c})\equiv\int^{x\_{i}+\Delta x/2}\_{x\_{i}-\Delta x/2}\phi(x-x\_{c},\sigma)\,dx,\ \forall i\in\mathbb{Z}, |  | (3) |

where 𝔼\mathbb{E} represents the expectation value of the argument,
and {xi:i∈ℤ}\left\{x\_{i}:i\in\mathbb{Z}\right\} denotes the standard
uniform quantization of the real line-array with resolution Δx>0\Delta x>0, i.e., xi+1−xi=Δxx\_{i+1}-x\_{i}=\Delta x for all i∈ℤi\in\mathbb{Z}. In
practice, the detector has a finite collection of measured elements
(or pixels) x1,…,xnx\_{1},...,x\_{n}, then a basic assumption here is that we
have a good coverage of the object of interest, in the sense that for
a given position xcx\_{c}:

|  |  |  |  |
| --- | --- | --- | --- |
|  | ∑i=1ngi(xc)≈∑i∈ℤgi(xc)=∫−∞∞ϕ⁡(x−xc,σ)𝑑x=1.\sum\_{i=1}^{n}g\_{i}(x\_{c})\approx\sum\_{i\in\mathbb{Z}}g\_{i}(x\_{c})=\int\_{-\infty}^{\infty}\phi(x-x\_{c},\sigma)\,dx=1. |  | (4) |

Note that equation ([3](#S2.E3 "In II.1 Astrometry and photometry based on a photon integrating device ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) adopts the idealized
situation where every pixel has the exact same response function
(equal to unity), or, equivalently, that our flat-field process has
been achieved with minimal uncertainty. It also assumes that the
intra-pixel response is uniform. The latter is more important in the
severely undersampled regime (see, e.g.,
[Adorf 1996](#bib.bib1)) which is not explored in this
paper. However a relevant aspect of data calibration is achieving a
proper flat-fielding which can affect the correctness of our
analysis and the form of the adopted likelihood function (see
below).

At the end, the likelihood of the joint random observation vector
In=(I1,..,In)I^{n}=(I\_{1},..,I\_{n}) (with values in ℕn\mathbb{N}^{n}), given the source
parameters (xc,F~)(x\_{c},\tilde{F}), is given by:

|  |  |  |  |
| --- | --- | --- | --- |
|  | L(In;xc,F~)=fλ1(xc,F~)(I1)⋅fλ2(xc,F~)(I2)⋯fλn(xc,F~)(In),∀In∈ℕn,L(I^{n};x\_{c},\tilde{F})=f\_{\lambda\_{1}(x\_{c},\tilde{F})}(I\_{1})\cdot f\_{\lambda\_{2}(x\_{c},\tilde{F})}(I\_{2})\cdots f\_{\lambda\_{n}(x\_{c},\tilde{F})}(I\_{n}),\ \forall I^{n}\in\mathbb{N}^{n}, |  | (5) |

where fλ(x)=e−λ⋅λxx!f\_{\lambda}(x)=\frac{e^{-\lambda}\cdot\lambda^{x}}{x!} denotes
the probability mass function (pmf) of the Poisson law
([Gray &
Davisson 2010](#bib.bib15)). We emphasize that equation ([5](#S2.E5 "In II.1 Astrometry and photometry based on a photon integrating device ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry"))
assumes that the observations (contained in the individual pixels,
denoted by the index ii) are independent (although not identically
distributed, since they follow λi\lambda\_{i}). Of course, this is only
an approximation to the real situation since it implies, in
particular, that we are neglecting any electronic defects or
features in the device such as, e.g., the cross-talk present in
multi-port CCDs ([Freyhammer et al. 2001](#bib.bib14)), or read-out correlations such as
the odd-even column effect in IR detectors ([Mason 2007](#bib.bib32)), as well
as calibration or data reduction deficiencies (e.g., due to
inadequate flat-fielding ([Gawiser et al. 2006](#bib.bib12))) that may alter this
idealized detection process. A serious attempt is done by
manufacturers and observatories to minimize the impact of these
defects, either by an appropriate electronic design, or by adjusting
the detector operational regimes (e.g., cross-talk can be reduced to
less than 1 part in 10410^{4} by adjusting the readout speed and by a
proper reduction process, [Freyhammer et al. 2001](#bib.bib14)). In essence, we are
considering an ideal detector that would satisfy the proposed
likelihood function given by equation ([5](#S2.E5 "In II.1 Astrometry and photometry based on a photon integrating device ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")), in real
detectors the likelihood function could be considerably more
complex777
Actually, in a real situation we may not even be
able to write such a function due to our imperfect
characterization or limited knowledge of the detector device..

We can formulate the astrometric and photometric estimation task, as
the problem of characterizing a decision rule τn():ℕn→Θ\tau\_{n}():\mathbb{N}^{n}\rightarrow\Theta, with Θ=ℝ2\Theta=\mathbb{R}^{2} being a parameter
space, where given an observation InI^{n} the parameters to be estimated
are (x^c(In),F~^(In))=τn(In)(\hat{x}\_{c}(I^{n}),\hat{\tilde{F}}(I^{n}))=\tau\_{n}(I^{n}). In other
words, τn(In)\tau\_{n}(I^{n}) gives us a prescription (or statistics) that
would allow us to estimate the underlying parameters (xc,F~)(x\_{c},\tilde{F})
(the estimated parameters are denoted by
(x^c,F~^)(\hat{x}\_{c},\hat{\tilde{F}})) from the available data vector InI^{n}.

In the simplest scenario, in which one is interested in determining a
single (unknown) parameter θ\theta (e.g., in our case either xcx\_{c} or
F~\tilde{F}, assuming that all other parameters are perfectly well
known), a commonly used decision rule adopted in statistics to
estimate this parameter (the estimation being θ^\hat{\theta}) is to
consider the prescription of minimum variance (denoted by VarVar),
given by:

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  | θ^()\displaystyle\hat{\theta}() | ≡\displaystyle\equiv | arg⁡minα⁡Var(α⁡(In))\displaystyle\arg\min\_{\alpha}Var(\alpha(I^{n})) |  | (6) |
|  |  | =\displaystyle= | arg⁡minα𝔼In∼fθn(α⁡(In)−θ)2\displaystyle\arg\min\_{\alpha}\mathbb{E}\_{I^{n}\sim f\_{\theta}^{n}}\left(\alpha(I^{n})-\theta\right)^{2} |  |

where “arg⁡min\arg\min” represents the argument that minimizes the
expression, while α\alpha is a generic variable representing the
parameter to be determined. Note that in the last equality we have
assumed that θ^()\hat{\theta}() is an unbiased estimator of the parameter
(i.e., that 𝔼⁡(θ^)=θ\mathbb{E}(\hat{\theta})=\theta), so that under this rule
we are implicitly minimizing the MSE of the estimate with respect to
the hidden true parameter θ\theta.

Unfortunately, the general solution of equation ([6](#S2.E6 "In II.1 Astrometry and photometry based on a photon integrating device ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) is
intractable, as in principle it requires the knowledge of θ\theta,
which is the essence of the inference problem. An additional issue
with equation ([6](#S2.E6 "In II.1 Astrometry and photometry based on a photon integrating device ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) is that, by itself, it does not provide
an analytical expression that tells us how to compute θ^\hat{\theta} in
terms of InI^{n}888
In many cases one can propose an “educated
guess” for θ^\hat{\theta} (e.g., a function of some sort) which is
trained with a (“good”) subset of the data itself (thus
approximately removing the ambiguity that the true parameter
θ\theta is, in fact, unknown). This heuristic approach is adopted,
e.g., in the SDSS pipeline trough the use of the KL transform, which
is a good approximation to a matched filter (also known as the
“North filter”, see e.g., [Gray &
Davisson 2010](#bib.bib15)).. Fortunately,
there are performance bounds that characterize how far can we be from
the theoretical solution in equation ([6](#S2.E6 "In II.1 Astrometry and photometry based on a photon integrating device ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")), and even
scenarios where the optimal solution can be achieved in a closed-form
(see Section [III.1](#S3.SS1 "III.1 Non achievability ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry") and
Appendix [A](#A1 "Appendix A Proof of Proposition ‣ Performance analysis of the Least-Squares estimator in
Astrometry")). One of the most
significant results in this field is the CR minimum variance bound
which will be further explained below.

### II.2 The Cramér-Rao bound

The CR bound offers a performance bound on the variance of the family
of unbiased estimators.
More precisely, let {Ii}i=1n\left\{I\_{i}\right\}\_{i=1}^{n} be a collection of
independent observations that follow a parametric pmf
fθ¯f\_{\bar{\theta}} defined on ℕ\mathbb{N}. The parameters to be
estimated from (I1,I2,…,In)(I\_{1},I\_{2},...,I\_{n})
will be denoted in general by the vector
θ¯=(θ1,θ2,…,θm)∈Θ=ℝm\bar{\theta}=(\theta\_{1},\theta\_{2},...,\theta\_{m})\in\Theta=\mathbb{R}^{m}. Let τn(In):ℕn→Θ\tau\_{n}(I^{n}):\mathbb{N}^{n}\rightarrow\Theta be
an unbiased estimator999
In the sense that, for all
θ¯∈Θ\bar{\theta}\in\Theta, 𝔼In∼fθ¯n{τn(In)}=θ¯\mathbb{E}\_{I^{n}\sim f^{n}\_{\bar{\theta}}}\left\{\tau\_{n}(I^{n})\right\}=\bar{\theta}. of
θ¯\bar{\theta}, and L(In;θ¯)=fθ¯(I1)⋅fθ¯(I2)⋯fθ¯(In)L(I^{n};\bar{\theta})=f\_{\bar{\theta}}(I\_{1})\cdot f\_{\bar{\theta}}(I\_{2})\cdots f\_{\bar{\theta}}(I\_{n}) be the likelihood
of the observation
In∈ℕnI^{n}\in\mathbb{N}^{n} given θ¯∈Θ\bar{\theta}\in\Theta. Then, the CR
bound ([Rao 1945](#bib.bib40); [Cramér 1946](#bib.bib10))
establishes that if:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝔼In∼fθ¯n{∂ln⁡L⁡(In,θ¯)∂θi}=0,∀i∈{1,…,m},\mathbb{E}\_{I^{n}\sim f^{n}\_{\bar{\theta}}}\left\{\frac{\partial\ln L(I^{n};\bar{\theta})}{\partial\theta\_{i}}\right\}=0,\;\;\forall i\in\left\{1,\ldots,m\right\}, |  | (7) |

then,

|  |  |  |  |
| --- | --- | --- | --- |
|  | Var(τn(In)i)≥[ℐθ¯(n)−1]i,i,Var(\tau\_{n}(I^{n})\_{i})\geq[\mathcal{I}\_{\bar{\theta}}(n)^{-1}]\_{i,i}, |  | (8) |

where ℐθ¯(n)\mathcal{I}\_{\bar{\theta}}(n) is the Fisher information
matrix given by:

|  |  |  |  |
| --- | --- | --- | --- |
|  | [ℐθ¯(n)]i,j=𝔼In∼fθ¯n{∂ln⁡L⁡(In,θ¯)∂θi⋅∂ln⁡L⁡(In,θ¯)∂θj}∀i,j∈{1,…,m}.[\mathcal{I}\_{\bar{\theta}}(n)]\_{i,j}=\mathbb{E}\_{I^{n}\sim f^{n}\_{\bar{\theta}}}\left\{\frac{\partial\ln L(I^{n};\bar{\theta})}{\partial\theta\_{i}}\cdot\frac{\partial\ln L(I^{n};\bar{\theta})}{\partial\theta\_{j}}\right\}\;\;\forall i,j\in\left\{1,\ldots,m\right\}. |  | (9) |

In particular, for the scalar case (m=1m=1), we have that for all
θ∈Θ\theta\in\Theta:

|  |  |  |  |
| --- | --- | --- | --- |
|  | minτn(⋅)∈𝒯n⁡Var(τn(In))≥ℐθ(n)−1=𝔼In∼fθn{[(dln⁡L(In,θ)dθ)2]}−1,\min\_{\tau\_{n}(\cdot)\in\mathcal{T}^{n}}Var(\tau\_{n}(I^{n}))\geq\mathcal{I}\_{\theta}(n)^{-1}=\mathbb{E}\_{I^{n}\sim f^{n}\_{\theta}}\left\{\left[\left(\frac{d\ln L(I^{n};{\theta})}{d\theta}\right)^{2}\right]\right\}^{-1}, |  | (10) |

where 𝒯n\mathcal{T}^{n} is the collection of unbiased estimators and
In∼fθnI^{n}\sim f^{n}\_{\theta}.

Returning to our problem in Section [II.1](#S2.SS1 "II.1 Astrometry and photometry based on a photon integrating device ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry"),
[Mendez
et al. 2013](#bib.bib34); [Mendez
et al. 2014](#bib.bib35) have characterized and analyzed the CR
bound for the isolated problem of astrometry and photometry,
respectively, as well as the joint problem of photometry and
astrometry. Particularly, we highlight the following results, which
will be used later on:

###### Proposition 1

([Mendez
et al. 2014](#bib.bib35))
Let us assume that xc∈ℝx\_{c}\in\mathbb{R} is fixed and known,
and we want to estimate F~\tilde{F} (fixed but unknown) from
In∼f(xc,F~)I^{n}\sim f\_{(x\_{c},\tilde{F})} in equation ([5](#S2.E5 "In II.1 Astrometry and photometry based on a photon integrating device ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")). In this
scalar parametric context, the Fisher information is given by:

|  |  |  |  |
| --- | --- | --- | --- |
|  | ℐF~(n)=∑i=1ngi(xc)F~gi(xc)+B~i,\mathcal{I}\_{\tilde{F}}(n)=\sum\_{i=1}^{n}\frac{g\_{i}(x\_{c})}{\tilde{F}g\_{i}(x\_{c})+\tilde{B}\_{i}}, |  | (11) |

which from equation ([10](#S2.E10 "In II.2 The Cramér-Rao bound ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) induces a MV bound for
the photometry estimation problem. On the other hand,
if F~∈ℝ+\tilde{F}\in\mathbb{R}^{+} is fixed and known, and we
want to estimate xcx\_{c} (fixed but unknown) from In∼f(xc,F~)I^{n}\sim f\_{(x\_{c},\tilde{F})} in equation ([5](#S2.E5 "In II.1 Astrometry and photometry based on a photon integrating device ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")), then the
Fisher information is given by:

|  |  |  |  |
| --- | --- | --- | --- |
|  | ℐxc(n)=∑i=1n(F~dgi(xc)dxc)2F~gi(xc)+B~i≡1σCR2,\mathcal{I}\_{x\_{c}}(n)=\sum\_{i=1}^{n}\frac{\left(\tilde{F}\frac{dg\_{i}(x\_{c})}{dx\_{c}}\right)^{2}}{\tilde{F}g\_{i}(x\_{c})+\tilde{B}\_{i}}\equiv\frac{1}{\sigma\_{CR}^{2}}, |  | (12) |

which from equation ([10](#S2.E10 "In II.2 The Cramér-Rao bound ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) induces a MV bound for
the astrometric estimation problem, and where
σCR2≡ℐxc(n)−1\sigma\_{CR}^{2}\equiv\mathcal{I}\_{x\_{c}}(n)^{-1} denotes the
(astrometric) CR bound.

At this point it is relevant to study if there is any practical
estimator that achieves the CR bound presented in
equations ([11](#S2.E11 "In Proposition 1 ‣ II.2 The Cramér-Rao bound ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) and ([12](#S2.E12 "In Proposition 1 ‣ II.2 The Cramér-Rao bound ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) for the
photometry and astrometry problem, respectively. For the photometric
case, [Perryman
et al. 1989](#bib.bib38) has shown that the
classical LS estimator is near-optimal, in the sense that its variance
is close to the CR bound for a wide range of experimental regimes, and
furthermore, in the low SNR regime, when F~gi(xc)≪B~i\tilde{F}g\_{i}(x\_{c})\ll\tilde{B}\_{i}, its variance (determined in closed-form) asymptotically
achieves the MV bound ℐF~(n)−1\mathcal{I}\_{\tilde{F}}(n)^{-1} in
equation ([11](#S2.E11 "In Proposition 1 ‣ II.2 The Cramér-Rao bound ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")). This is a formal justification for
the goodness of the LS as a method for doing isolated photometry in
the setting presented in Section [II.1](#S2.SS1 "II.1 Astrometry and photometry based on a photon integrating device ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry"). An
equivalent analysis has not been conducted for the astrometric
problem, which is the focus of the next section of this work.

III Achievability analysis of the Cramér-Rao bound in astrometry
----------------------------------------------------------------

We first evaluate if the CR bound for the astrometric problem,
σCR2\sigma\_{CR}^{2} from equation ([12](#S2.E12 "In Proposition 1 ‣ II.2 The Cramér-Rao bound ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")), can possibly be
achieved by any unbiased estimator. Then, we focus on the widely used
LS estimation approach, to evaluate its performance in comparison with
the astrometric MV bound presented in Proposition
[1](#Thmpreposition1 "Proposition 1 ‣ II.2 The Cramér-Rao bound ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry").

### III.1 Non achievability

Concerning achievability, we demonstrate that for astrometry (i.e.,
assuming F~\tilde{F} is known) there is no estimator that achieves the
CR bound in any observational regime101010
However, in
Section [3](#Thmremark3 "Remark 3 ‣ III.3 Analysis and interpretation of Theorem ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry") we demonstrate that in the low SNR
limit the LS estimator can asymptotically approach the CR
bound.. The log-likelihood function associated to
equation ([5](#S2.E5 "In II.1 Astrometry and photometry based on a photon integrating device ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) in this case is given by:

|  |  |  |  |
| --- | --- | --- | --- |
|  | ln⁡L⁡(In,xc)=∑i=1n(Ii⋅ln⁡λi(xc)−λi(xc)−ln⁡Ii!),\ln L(I^{n};x\_{c})={\sum\_{i=1}^{n}\left(I\_{i}\cdot\ln\lambda\_{i}(x\_{c})-\lambda\_{i}(x\_{c})-\ln I\_{i}!\right)}, |  | (13) |

and we have the following result:

###### Proposition 2

For any fixed and unknown parameter xc∈ℝx\_{c}\in\mathbb{R}, and
any unbiased estimator τn\tau\_{n}

|  |  |  |  |
| --- | --- | --- | --- |
|  | Var(τn(In))>σCR2,Var(\tau\_{n}(I^{n}))>\sigma\_{CR}^{2}, |  | (14) |

where InI^{n} follows a Poisson pmf (fλ⁡(xc)≡fxcf\_{\lambda(x\_{c})}\equiv f\_{x\_{c}} hereafter, to shorten notation) from
equation ([5](#S2.E5 "In II.1 Astrometry and photometry based on a photon integrating device ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")). (The proof is presented in
Appendix [A](#A1 "Appendix A Proof of Proposition ‣ Performance analysis of the Least-Squares estimator in
Astrometry")).

The non-achievability condition imposed by
Proposition [2](#Thmpreposition2 "Proposition 2 ‣ III.1 Non achievability ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry") supports the adoption of alternative criteria for position estimation, being ML and the
classical LS two of the most commonly adopted approaches. The ML
estimate of the position τML(In)\tau\_{ML}(I^{n}) is obtained through the
following rule:

|  |  |  |  |
| --- | --- | --- | --- |
|  | τML(In)=arg⁡maxα∈ℝ⁡ln⁡L⁡(In,α),\tau\_{ML}(I^{n})=\arg\max\_{\alpha\in\mathbb{R}}\ln L(I^{n};\alpha), |  | (15) |

where “arg⁡max\arg\max” represents the argument that maximizes the
expression, while α\alpha is a generic variable representing the
astrometric position. Imposing the first order condition on this
optimization problem, it reduces to satisfying the condition dln⁡L⁡(In,xc)dxc=0\frac{d\ln L(I^{n};x\_{c})}{dx\_{c}}=0, and, consequently, we can work with the
general expression given by
equation ([A2](#A1.E2 "In Appendix A Proof of Proposition ‣ Performance analysis of the Least-Squares estimator in
Astrometry")). We note that a
well-known statistical result indicates that in the case of
independent and identically distributed samples the ML approach is
asymptotically unbiased and efficient (i.e., it achieves the CR bound
when the number of observations goes to infinity ([Kay 1993](#bib.bib21), Chapter
7.5)). However for the (still independent) but
non-identically distributed setting of astrometry described by
equation ([5](#S2.E5 "In II.1 Astrometry and photometry based on a photon integrating device ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")), this asymptotic result, to the best of our
knowledge, has not been proven, and remains an open problem.

On the other hand, a version of the LS estimator (given the model
presented in Section [II.1](#S2.SS1 "II.1 Astrometry and photometry based on a photon integrating device ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) corresponds to the
solution of:

|  |  |  |  |
| --- | --- | --- | --- |
|  | τLS(In)=arg⁡minα∈ℝ⁡∑i=1n(Ii−λi(α))2⏟≡J⁡(In,α),\tau\_{LS}(I^{n})=\arg\min\_{\alpha\in\mathbb{R}}\underbrace{\sum\_{i=1}^{n}\left(I\_{i}-\lambda\_{i}(\alpha)\right)^{2}}\_{\equiv J(I^{n},\alpha)}, |  | (16) |

with λi(α)=F~gi(α)+B~i\lambda\_{i}(\alpha)=\tilde{F}g\_{i}(\alpha)+\tilde{B}\_{i} and where
gi(⋅)g\_{i}(\cdot) is given by equation ([3](#S2.E3 "In II.1 Astrometry and photometry based on a photon integrating device ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry"))111111
Note
that if we had assumed a detection process subject to a purely
Gaussian noise with an rms of σ\sigma, then the probability mass
function for each individual observation would have been given by
fλ(x)=12πσe−(x−λ)22σ2f\_{\lambda}(x)=\frac{1}{\sqrt{2\pi}\sigma}e^{-}\frac{(x-\lambda)^{2}}{2\sigma^{2}}. In this case the
log-likelihood function (i.e., the equivalent of
equation ([13](#S3.E13 "In III.1 Non achievability ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry"))) would be given by ln⁡L⁡(In,xc)=−nln⁡(2πσ)−12σ2∑i=1n(Ii−λi(xc))2\ln L(I^{n};x\_{c})=-n\ln(\sqrt{2\pi}\sigma)-\frac{1}{2\sigma^{2}}\sum\_{i=1}^{n}\left(I\_{i}-\lambda\_{i}(x\_{c})\right)^{2}. Therefore, in this scenario, finding
the maximum of the log-likelihood would be the same as finding the
minimum of the LS, as in
equation ([16](#S3.E16 "In III.1 Non achievability ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")). This is a well-established
result, described in many statistical books..

In a previous paper ([Mendez
et al. 2013](#bib.bib34), Section 5), we have carried out
numerical simulations using equations ([15](#S3.E15 "In III.1 Non achievability ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry"))
and ([16](#S3.E16 "In III.1 Non achievability ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")), and have demonstrated that both
approaches are reasonable. However, an inspection of [Mendez
et al. 2013](#bib.bib34) suggests that the LS method exhibits a loss of
optimality at high-SNR in comparison with either the (Poisson
variance-) weighted LS or the ML method. This motivates a deeper study
of the LS method, to properly understand its behavior and limitations
in terms of its MSE and possible statistical bias, which is the focus
of the following Section.

### III.2 Bounding the performance of the Least-Squares estimator

The solution to equation ([16](#S3.E16 "In III.1 Non achievability ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) is non-linear
(see Figure [7](#A3.F7 "Figure 7 ‣ Performance analysis of the Least-Squares estimator in
Astrometry")), and it does not have a closed-form expression.
Consequently, a number of iterative approaches have been adopted (see,
e.g., [Stetson 1987](#bib.bib44); [Mighell 2005](#bib.bib36)) to solve or
approximate τLS(In)\tau\_{LS}(I^{n}). Hence as τLS(In)\tau\_{LS}(I^{n}) is implicit,
it is not possible to compute its mean, its variance, nor its
estimation error directly. We also note that, since we will be
mainly analyzing the behavior of τLS(In)\tau\_{LS}(I^{n}), none of the
caveats concerning the properness of the likelihood function
(equation ([5](#S2.E5 "In II.1 Astrometry and photometry based on a photon integrating device ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry"))) raised in
Section [II.1](#S2.SS1 "II.1 Astrometry and photometry based on a photon integrating device ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry") are relevant in what follows,
except for what concerns the adequacy of equation ([2](#S2.E2 "In II.1 Astrometry and photometry based on a photon integrating device ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")),
which we take as a valid description of the underlying flux
distribution.

The problem of computing the MSE of an estimator that is the solution
of an optimization problem has been recently addressed by
[So et al. 2013](#bib.bib43) using a general framework. Their basic idea was to
provide sufficient conditions on the objective function, in our case
J⁡(In,α)J(I^{n},\alpha), to derive a good approximation for
𝔼In∼fxc{(τLS(In)−xc)2}\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{\left(\tau\_{LS}(I^{n})-x\_{c}\right)^{2}\right\}. Based on this idea, we provide below a
refined result (specialized to our astrometry problem), which relaxes
one of the idealized assumptions proposed in [So et al. 2013](#bib.bib43), and which is not strictly satisfied in our
problem (see Remark [2](#Thmremark2 "Remark 2 ‣ III.3 Analysis and interpretation of Theorem ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry") in Section [III.3](#S3.SS3 "III.3 Analysis and interpretation of Theorem ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")). As a
consequence, our result offers upper and lower bounds for the bias and
MSE of τLS(In)\tau\_{LS}(I^{n}), respectively.

###### Theorem 1

Let us consider a fixed and unknown parameter xc∈ℝx\_{c}\in\mathbb{R}, and that In∼fxcI^{n}\sim f\_{x\_{c}}. In addition, let us
define the residual random variable121212
As a short hand
notation: J′(In,xc)≡dJ(In,α)dα|α=xcJ^{\prime}(I^{n},x\_{c})\equiv\frac{dJ(I^{n},\alpha)}{d\alpha}|\_{\alpha=x\_{c}}, and J′′(In,xc)≡d2J(In,α)d2α|α=xcJ^{\prime\prime}(I^{n},x\_{c})\equiv\frac{d^{2}J(I^{n},\alpha)}{d^{2}\alpha}|\_{\alpha=x\_{c}}. W⁡(In,α)≡J′′(In,α)−𝔼In∼fxc{J′′(In,α)}𝔼In∼fxc{J′′(In,α)}W(I^{n},\alpha)\equiv\frac{J^{\prime\prime}(I^{n},\alpha)-\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{J^{\prime\prime}(I^{n},\alpha)\right\}}{\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{J^{\prime\prime}(I^{n},\alpha)\right\}}. If there exists δ∈(0,1)\delta\in(0,1) such that
ℙ⁡(W⁡(In,xc)∈(−δ,δ))=1\mathbb{P}(W(I^{n},x\_{c})\in(-\delta,\delta))=1, then:

|  |  |  |  |
| --- | --- | --- | --- |
|  | |𝔼In∼fxc{τLS(In)}−xc|≤ϵ⁡(δ),\displaystyle\left|\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{\tau\_{LS}(I^{n})\right\}-x\_{c}\right|\leq\epsilon(\delta), |  | (17) |
|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝔼In∼fxc{(τLS(In)−xc)2}∈(σLS2(n)(1+δ)2,σLS2(n)(1−δ)2),\displaystyle\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{\left(\tau\_{LS}(I^{n})-x\_{c}\right)^{2}\right\}\in\left(\frac{\sigma^{2}\_{LS}(n)}{(1+\delta)^{2}},\frac{\sigma^{2}\_{LS}(n)}{(1-\delta)^{2}}\right), |  | (18) |

where

|  |  |  |  |
| --- | --- | --- | --- |
|  | σLS2(n)≡𝔼In∼fxc{J′(In,xc)2}(𝔼In∼fxc{J′′(In,xc)})2\displaystyle\sigma^{2}\_{LS}(n)\equiv\frac{\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{J^{\prime}(I^{n},x\_{c})^{2}\right\}}{\left(\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{J^{\prime\prime}(I^{n},x\_{c})\right\}\right)^{2}} |  | (19) |

and

|  |  |  |  |
| --- | --- | --- | --- |
|  | ϵ⁡(δ)≡𝔼In∼fxc{|J′(In,xc)|}𝔼In∼fxc{J′′(In,xc)}⋅δ1−δ.\displaystyle\epsilon(\delta)\equiv\frac{\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{\left|J^{\prime}(I^{n},x\_{c})\right|\right\}}{\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{J^{\prime\prime}(I^{n},x\_{c})\right\}}\cdot\frac{\delta}{1-\delta}. |  | (20) |

(The proof is presented in Appendix
[B](#A2 "Appendix B Proof of Theorem ‣ Performance analysis of the Least-Squares estimator in
Astrometry")).

### III.3 Analysis and interpretation of Theorem [1](#Thmtheorem1 "Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in Astrometry")

###### Remark 1

Theorem [1](#Thmtheorem1 "Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry") is obtained under a bounded
condition (with probability one) over the
random variable W⁡(In,xc)W(I^{n},x\_{c}). To verify whether this condition is
actually met, it is therefore important to derive an explicit
expression for W⁡(In,xc)W(I^{n},x\_{c}). Starting from
equation ([16](#S3.E16 "In III.1 Non achievability ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) it follows that:

|  |  |  |
| --- | --- | --- |
|  | J′′(In,α)=2∑i=1n[(dλi(α)dα)2+(λi(α)−Ii)⋅d2λi(α)d2α]J^{\prime\prime}(I^{n},\alpha)=2\sum\_{i=1}^{n}\left[\left(\frac{d\lambda\_{i}(\alpha)}{d\alpha}\right)^{2}+(\lambda\_{i}(\alpha)-I\_{i})\cdot\frac{d^{2}\lambda\_{i}(\alpha)}{d^{2}\alpha}\right] |  |

and, consequently, 𝔼In∼fxc{J′′(In,xc)}=2∑i=1n(dλi(α)dα|α=xc)2\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{J^{\prime\prime}(I^{n},x\_{c})\right\}=2\sum\_{i=1}^{n}\left(\frac{d\lambda\_{i}(\alpha)}{d\alpha}|\_{\alpha=x\_{c}}\right)^{2}. Therefore:

|  |  |  |  |
| --- | --- | --- | --- |
|  | W⁡(In,xc)=∑i=1n(λi(xc)−Ii)⋅[λi′′(xc)/∑j=1n(λj′(xc))2].W(I^{n},x\_{c})=\sum\_{i=1}^{n}(\lambda\_{i}(x\_{c})-I\_{i})\cdot\left[\lambda\_{i}^{\prime\prime}(x\_{c})/\sum\_{j=1}^{n}(\lambda\_{j}^{\prime}(x\_{c}))^{2}\right]. |  | (21) |

Then, W⁡(In,xc)W(I^{n},x\_{c}) is not bounded almost surely, since IiI\_{i} could
take any value in ℕ\mathbb{N} with non-zero probability. However,
𝔼In∼fxc{W⁡(In,xc)}=0\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{W(I^{n},x\_{c})\right\}=0, and
its variance in closed-form is:

|  |  |  |  |
| --- | --- | --- | --- |
|  | Var(W⁡(In,xc))=∑i=1nλi(xc)⋅[(λi′′(xc))2/(∑j=1n(λj′(xc))2)2].Var(W(I^{n},x\_{c}))=\sum\_{i=1}^{n}\lambda\_{i}(x\_{c})\cdot\left[(\lambda\_{i}^{\prime\prime}(x\_{c}))^{2}/\left(\sum\_{j=1}^{n}(\lambda\_{j}^{\prime}(x\_{c}))^{2}\right)^{2}\right]. |  | (22) |

From this, we can evaluate how far we are from the bounded assumption
of Theorem [1](#Thmtheorem1 "Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry"). To do this, we can resort to
Markov’s inequality ([Cover &
Thomas 2006](#bib.bib9)), where
ℙ⁡(W⁡(In,xc)∉(−ρ,ρ))≤Var(W⁡(In,xc))/ρ2\mathbb{P}(W(I^{n},x\_{c})\notin(-\rho,\rho))\leq Var(W(I^{n},x\_{c}))/\rho^{2}. Then, for any ϵ∈(0,1)\epsilon\in(0,1), we can
characterize a critical δ⁡(ϵ)>0\delta(\epsilon)>0 such that
ℙ⁡(W⁡(In,xc)∈(−δ⁡(ϵ),δ⁡(ϵ)))>1−ϵ\mathbb{P}(W(I^{n},x\_{c})\in(-\delta(\epsilon),\delta(\epsilon)))>1-\epsilon. Using this result
and Theorem [1](#Thmtheorem1 "Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry"), we can bound the conditional
bias and conditional MSE of τLS(In)\tau\_{LS}(I^{n}) using
equations ([17](#S3.E17 "In Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry"))
and ([18](#S3.E18 "In Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")), respectively. In Section
[IV](#S4 "IV Numerical analysis of the LS estimator ‣ Performance analysis of the Least-Squares estimator in
Astrometry"), we conduct a numerical analysis, where it is
shown that the bounded assumption for W⁡(In,xc)W(I^{n},x\_{c}) is indeed satisfied
for a number of important realistic experimental settings in
astrometry (with very high probability).

###### Remark 2

Concerning the MSE of the LS estimator,
equation ([18](#S3.E18 "In Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) offers a lower and
upper bound in terms of a nominal value
σLS2(n)\sigma^{2}\_{LS}(n) (given by equation ([19](#S3.E19 "In Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry"))), and an
interval around it.
In the interesting regime where δ≪1\delta\ll 1 (this regime approaches
the ideal case δ=0\delta=0 studied by [So et al. 2013](#bib.bib43) in which case the
variable W⁡(In,xc)W(I^{n},x\_{c}) becomes deterministic), we have that
τLS(⋅)\tau\_{LS}(\cdot) is an unbiased estimator, as shown by
equation ([17](#S3.E17 "In Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")), and, furthermore:

|  |  |  |
| --- | --- | --- |
|  | Var(τLS(In))=𝔼In∼fxc{(τLS(In)−xc)2}=σLS2(n)≥σCR2,Var(\tau\_{LS}(I^{n}))=\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{\left(\tau\_{LS}(I^{n})-x\_{c}\right)^{2}\right\}=\sigma^{2}\_{LS}(n)\geq\sigma\_{CR}^{2}, |  |

from
equations ([18](#S3.E18 "In Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry"))
and ([10](#S2.E10 "In II.2 The Cramér-Rao bound ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")). Thus, it is interesting to provide an
explicit expression for σLS2(n)\sigma^{2}\_{LS}(n) which will be valid
for the MSE of the LS method in this regime. First we note
that, J′(In,xc)=2⋅(∑i=1ndλi(xc)dxc⋅(λi(xc)−Ii))J^{\prime}(I^{n},x\_{c})=2\cdot\left(\sum\_{i=1}^{n}\frac{d\lambda\_{i}(x\_{c})}{dx\_{c}}\cdot(\lambda\_{i}(x\_{c})-I\_{i})\right), and
therefore:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | (J′(In,xc))2=\displaystyle(J^{\prime}(I^{n},x\_{c}))^{2}= |  | 4⋅(∑i=1n∑j=1,j≠in(IiIj−Iiλj−Ijλi+λiλj)⋅dλidxc⋅dλjdxc)\displaystyle 4\cdot\left(\sum\_{i=1}^{n}\sum\_{j=1,j\neq i}^{n}(I\_{i}I\_{j}-I\_{i}\lambda\_{j}-I\_{j}\lambda\_{i}+\lambda\_{i}\lambda\_{j})\cdot\frac{d\lambda\_{i}}{dx\_{c}}\cdot\frac{d\lambda\_{j}}{dx\_{c}}\right) |  |
|  |  |  | +4⋅(∑i=1n(Ii2−2Iiλi+λi2)⋅(dλidxc)2).\displaystyle+4\cdot\left(\sum\_{i=1}^{n}(I\_{i}^{2}-2I\_{i}\lambda\_{i}+\lambda\_{i}^{2})\cdot\left(\frac{d\lambda\_{i}}{dx\_{c}}\right)^{2}\right). |  |

Therefore 𝔼In∼fxc{J′(In,xc)2}=4⋅∑i=1nλi(xc)⋅(λi′(xc))2\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{J^{\prime}(I^{n},x\_{c})^{2}\right\}=4\cdot\sum\_{i=1}^{n}\lambda\_{i}(x\_{c})\cdot(\lambda\_{i}^{\prime}(x\_{c}))^{2}, which implies that:

|  |  |  |  |
| --- | --- | --- | --- |
|  | σLS2(n)=∑i=1nλi(xc)⋅(λi′(xc))2(∑i=1n(λi′(xc))2)2=∑i=1n(F~gi(xc)+B~i)⋅(gi′(xc))2(F~∑i=1n(gi′(xc))2)2.\sigma^{2}\_{LS}(n)=\frac{\sum\_{i=1}^{n}\lambda\_{i}(x\_{c})\cdot(\lambda\_{i}^{\prime}(x\_{c}))^{2}}{\left(\sum\_{i=1}^{n}(\lambda\_{i}^{\prime}(x\_{c}))^{2}\right)^{2}}=\frac{\sum\_{i=1}^{n}(\tilde{F}g\_{i}(x\_{c})+\tilde{B}\_{i})\cdot(g\_{i}^{\prime}(x\_{c}))^{2}}{\left(\tilde{F}\sum\_{i=1}^{n}(g\_{i}^{\prime}(x\_{c}))^{2}\right)^{2}}. |  | (23) |

In the next section, we provide a numerical analysis to
compare the predictions of
equation ([23](#S3.E23 "In Remark 2 ‣ III.3 Analysis and interpretation of Theorem ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) with the CR bound
computed through equation ([12](#S2.E12 "In Proposition 1 ‣ II.2 The Cramér-Rao bound ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")). We also
analyze if
this nominal value is representative of the performance of the LS estimator.

###### Remark 3

(Idealized Low SNR regime)
Following the ideal scenario where δ≪1\delta\ll 1, we explore
the weak signal case in which F~gi(xc)≪B~i\tilde{F}g\_{i}(x\_{c})\ll\tilde{B}\_{i} considering a constant background across the
pixels, i.e., B~i=B~\tilde{B}\_{i}=\tilde{B} for all ii. Then
adopting equation ([23](#S3.E23 "In Remark 2 ‣ III.3 Analysis and interpretation of Theorem ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) we have that:

|  |  |  |  |
| --- | --- | --- | --- |
|  | σLS2(n)≈B~F~2∑i=1n(gi′(xc))2.\sigma^{2}\_{LS}(n)\approx\frac{\tilde{B}}{\tilde{F}^{2}\sum\_{i=1}^{n}(g\_{i}^{\prime}(x\_{c}))^{2}}. |  | (24) |

On the other hand, from equation ([12](#S2.E12 "In Proposition 1 ‣ II.2 The Cramér-Rao bound ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) we
have that ℐxc(n)≈F~2/B~∑i=1n(gi′(xc))2\mathcal{I}\_{x\_{c}}(n)\approx{\tilde{F}^{2}}/{\tilde{B}}\sum\_{i=1}^{n}(g\_{i}^{\prime}(x\_{c}))^{2}.
Remarkably in this context,
the LS estimator is optimal in the sense that it approaches
the CR bound asymptotically when a weak signal is
observed131313
Recall that, according to
Section [III.1](#S3.SS1 "III.1 Non achievability ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry"), we have demonstrated that the
CR can not be exactly reached in astrometry.. This results
is consistent with the numerical simulations in [Mendez
et al. 2013](#bib.bib34).141414
We note that this asymptotic
result can be considered the astrometric counterpart of
what has been shown in photometry by [Perryman
et al. 1989](#bib.bib38),
where the LS estimator also approaches the CR bound in the
low SNR regime.

###### Remark 4

(Idealized High SNR regime)
For the high SNR regime, assuming again that δ≪1\delta\ll 1, we
consider the case where F~gi(xc)≫B~i\tilde{F}g\_{i}(x\_{c})\gg\tilde{B}\_{i} for all
ii. In this case:

|  |  |  |  |
| --- | --- | --- | --- |
|  | σLS2(n)≈[F~(∑i=1ngi′(xc)2)2∑i=1ngi(xc)gi′(xc)2]−1 and σCR2≈[F~∑i=1n(gi′(xc))2/gi(xc)]−1.\sigma^{2}\_{LS}(n)\approx\left[\tilde{F}\frac{\left(\sum\_{i=1}^{n}g\_{i}^{\prime}(x\_{c})^{2}\right)^{2}}{\sum\_{i=1}^{n}g\_{i}(x\_{c})g\_{i}^{\prime}(x\_{c})^{2}}\right]^{-1}\mbox{ and }\sigma\_{CR}^{2}\approx\left[\tilde{F}\sum\_{i=1}^{n}(g\_{i}^{\prime}(x\_{c}))^{2}/g\_{i}(x\_{c})\right]^{-1}. |  | (25) |

Therefore, in this strong signal scenario, there is no match
between the variance of the LS estimator and the CR bound, and
consequently, we have that σLS2(n)>σCR2\sigma^{2}\_{LS}(n)>\sigma\_{CR}^{2}.
To provide more insight on the nature of this performance gap,
in the next proposition we offer a closed-form expression for
this mismatch in the high-resolution scenario where the source
is oversampled, and the size of the pixel is a small fraction
of the width parameter σ\sigma of the PSF in
equation ([1](#S2.E1 "In II.1 Astrometry and photometry based on a photon integrating device ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")).

###### Proposition 3

Assuming the idealized high SNR regime, if we have a Gaussian-like PSF
and Δx/σ≪1\Delta x/\sigma\ll 1, then:

|  |  |  |  |
| --- | --- | --- | --- |
|  | σLS2(n)σCR2≈833>1.\frac{\sigma^{2}\_{LS}(n)}{\sigma\_{CR}^{2}}\approx\frac{8}{3\sqrt{3}}>1. |  | (26) |

(The proof is presented in Appendix [C](#A3 "Appendix C Proof of Proposition ‣ Performance analysis of the Least-Squares estimator in
Astrometry")).

Equation ([26](#S3.E26 "In Proposition 3 ‣ Remark 4 ‣ III.3 Analysis and interpretation of Theorem ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) shows that there is a very
significant performance gap between the CR bound and the MSE of the LS
estimator in the high SNR regime. This result should motivate the
exploration of alternative estimators that could approach more closely
the CR bound in this regime.

IV Numerical analysis of the LS estimator
-----------------------------------------

In this section we explore the implications of Theorem
[1](#Thmtheorem1 "Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry") in astrometry through the use of
simulated observations. First, we analyze if the bounded condition
over W⁡(In,α)W(I^{n},\alpha) adopted in Theorem [1](#Thmtheorem1 "Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")
is a valid assumption for the type of settings considered in
astronomical observations. After that, we compare
how efficient is the LS estimator proposed in
equation ([16](#S3.E16 "In III.1 Non achievability ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) as a function of the SNR and
pixel resolution, adopting for that purpose Theorem
[1](#Thmtheorem1 "Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry") and Proposition
[1](#Thmpreposition1 "Proposition 1 ‣ II.2 The Cramér-Rao bound ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry").

To perform our simulations, we adopt some realistic design variables
and astronomical observing conditions to model the problem
([Mendez
et al. 2013](#bib.bib34); [Mendez
et al. 2014](#bib.bib35)). For the PSF, various analytical and
semi-empirical forms have been proposed, see for instance the
ground-based model in [King 1971](#bib.bib23) and the space-based model in
[Bendinelli
et al. 1987](#bib.bib6). For our analysis, we adopt in
equation ([3](#S2.E3 "In II.1 Astrometry and photometry based on a photon integrating device ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) the Gaussian PSF where ϕ(x,σ)=12πσe−12⋅(xσ)2\phi(x,\sigma)=\frac{1}{\sqrt{2\pi}\,\sigma}e^{-\frac{1}{2}\cdot\left(\frac{x}{\sigma}\right)^{2}}, and where
σ\sigma is the width of the PSF, assumed to be known. This PSF has
been found to be a good representation for typical astrometric-quality
ground-based data ([Mendez
et al. 2010](#bib.bib33)). In terms of nomenclature, the
FWHM≡22ln⁡2σFWHM\equiv 2\sqrt{2\ln 2}\,\,\sigma, measured in arcsec, denotes
the Full-Width at Half-Maximum (FWHMFWHM) parameter, which is an
overall indicator of the image quality at the observing site
([Chromey 2010](#bib.bib8))151515
In our simulations we fix the
value of FWHMFWHM to a constant value. However, in many cases the
image quality changes as a function of position in the field-of-view
due to optical distortions, specially important in large focal plane
arrays. For example, in the case of the SDSS (which consists of
30 CCDs of 20482 pix2 each, covering 2°.3 on the sky at
a resolution of 0.396 arcsec/pix), the FWHMFWHM may vary up to 15%
from center to corner of one detector
([Lupton et al. 2001](#bib.bib30)). The impact on the CR bound of
these changes has been discussed in some detail by
[Mendez
et al. 2014](#bib.bib35)..

The background profile, represented by {B~i,i=1,..,n}\left\{\tilde{B}\_{i},i=1,..,n\right\}, is a function of several variables, like the
wavelength of the observations, the moon phase (which contributes
significantly to the diffuse sky background), the quality of the
observing site, and the specifications of the instrument itself. We
will consider a uniform background across pixels underneath the PSF,
i.e., Bi~=B~\tilde{B\_{i}}=\tilde{B} for all ii. To characterize the
magnitude of B~\tilde{B}, it is important to first mention that the
detector does not measure photon counts (or, actually, photo-e−e^{-})
directly, but a discrete variable in “Analog to Digital Units
(ADUs)” of the instrument, which is a linear proportion of the photon
counts ([Gilliland 1992](#bib.bib13)). This linear proportion is characterized
by the gain of the instrument GG in units of e−e^{-}/ADU. GG is just a
scaling factor, where we can define F≡F~/GF\equiv\tilde{F}/G and B≡B~/GB\equiv\tilde{B}/G as the brightness of the object and background,
respectively, in the specific ADUs of the instrument. Then, the
background (in ADUs) depends on the pixel size Δx\Delta x as follows
([Mendez
et al. 2013](#bib.bib34)):

|  |  |  |  |
| --- | --- | --- | --- |
|  | B=fs⋅Δx+D+RON2GADU,B=f\_{s}\cdot\Delta x+\frac{D+RON^{2}}{G}\;\;\mbox{ADU}, |  | (27) |

where fsf\_{s} is the (diffuse) sky background in ADU/arcsec (if Δx\Delta x is measured in arcsec), while DD and RONRON, both measured in
e−e^{-}, model the dark-current and read-out-noise of the detector on
each pixel, respectively. Note that the first component in
equation ([27](#S4.E27 "In IV Numerical analysis of the LS estimator ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) is attributed to the site, and
its effect is proportional to the pixel size. On the other hand, the
second component is attributed to errors of the integrating device
(detector), and it is pixel-size independent. This distinction is
central when analyzing the performance as a function of the pixel
resolution of the array (see details in
[Mendez
et al. 2013](#bib.bib34)). More important is the fact that in
typical ground-based astronomical observation, long exposure times are
considered, which implies that the background is dominated by diffuse
light coming from the sky (the first term in the RHS of
equation ([27](#S4.E27 "In IV Numerical analysis of the LS estimator ‣ Performance analysis of the Least-Squares estimator in
Astrometry"))), and not from the detector
([Mendez
et al. 2013](#bib.bib34), Sec. 4).

For the experimental conditions, we consider the scenario of a
ground-based station located at a good site with clear atmospheric
conditions and the specifications of current science-grade CCDs, where
fs=1502.5f\_{s}=1502.5 ADU/arcsec, D=0D=0 e−e^{-}, RON=5RON=5 e−e^{-},
FWHM=1FWHM=1 arcsec and G=2G=2 e−e^{-}/ADU (with these values B=313B=313 ADU for
Δx=0.2\Delta x=0.2 arcsec using
equation ([27](#S4.E27 "In IV Numerical analysis of the LS estimator ‣ Performance analysis of the Least-Squares estimator in
Astrometry"))). In terms of scenarios of
analysis, we explore different pixel resolutions for the CCD array
Δx∈[0.1,0.7]\Delta x\in[0.1,0.7] measured in arcsec. Note that a change in
Δx\Delta x will be reflected upon the limits of the integral to
compute the pixel response function gi(xc)g\_{i}(x\_{c}) (see
equation ([3](#S2.E3 "In II.1 Astrometry and photometry based on a photon integrating device ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry"))) as well as in the calculation of the
background level per pixel B~i\tilde{B}\_{i}, according to
equation ([27](#S4.E27 "In IV Numerical analysis of the LS estimator ‣ Performance analysis of the Least-Squares estimator in
Astrometry")). Therefore, a change in Δx\Delta x is not only a design feature of the detector device, but it implies
also a change in the distribution of the background underneath the
PSF. The impact of this covariant device-and-atmosphere change in the
CR bound is explained in detail in [Mendez
et al. 2013](#bib.bib34).

In our simulations, we also consider different signal strengths
F~∈{1 080,3 224,20 004,60 160}\tilde{F}\in\left\{1\,080,3\,224,20\,004,60\,160\right\}161616
These are the same values explored in [Mendez
et al. 2013](#bib.bib34)., measured in photo-e−e^{-}, corresponding to
SNR ∈∼{12,33,120,230}\in\sim\left\{12,33,120,230\right\}
respectively171717
For a given F~\tilde{F} and fsf\_{s} there is a
weak dependency of SNR on the pixel size Δx\Delta x, see
equation (28) in [Mendez
et al. 2013](#bib.bib34).. Note that increasing
F~\tilde{F} implies increasing the SNR of the problem, which can be
approximately measured by the ratio F~/B~≡F/B\tilde{F}/\tilde{B}\equiv F/B181818
We note that while the ratio F~/B~\tilde{F}/\tilde{B} can
be used as a proxy for SNR, in what follows we have used the exact
expression to compute this quantity, as given by equation (28) in
[Mendez
et al. 2013](#bib.bib34).. On a given detector plus telescope setting,
these different SNR scenarios can be obtained by changing
appropriately the exposure time (open shutter) that generates the
image.

### IV.1 Analyzing the bounded condition over W⁡(In,α)W(I^{n},\alpha)

To validate how realistic is the bounded assumption over W⁡(In,α)W(I^{n},\alpha) in our problem, we first evaluate the variance of W⁡(In,xc)W(I^{n},x\_{c}) from equation ([22](#S3.E22 "In Remark 1 ‣ III.3 Analysis and interpretation of Theorem ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")), this is presented
in Figure [1](#A3.F1 "Figure 1 ‣ Performance analysis of the Least-Squares estimator in
Astrometry") for different SNR regimes and pixel resolutions
in the array. Overall, the magnitudes are very small considering the
admissible range (0,1)(0,1) for W⁡(In,xc)W(I^{n},x\_{c}) stipulated in Theorem
[1](#Thmtheorem1 "Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry"). Also, given that W⁡(In,xc)W(I^{n},x\_{c}) has zero
mean, the bounded condition will happen with high
probability. Complementing this, Figure [2](#A3.F2 "Figure 2 ‣ Performance analysis of the Least-Squares estimator in
Astrometry") presents the
critical δ\delta across different pixel resolutions and SNR
regimes191919
These values were computed empirically (from
frequency counts) using 5 0005\,000 realizations of the random variable
W⁡(In,xc)W(I^{n},x\_{c}) for the different SNR regimes and pixel
resolutions.. For this, we fix a small value of ϵ\epsilon
(=10−3=10^{-3} in this case), and calculate δ\delta such that
W⁡(In,xc)∈(−δ,δ)W(I^{n},x\_{c})\in(-\delta,\delta) with probability 1−ϵ1-\epsilon. From
the curves obtained, we can say that the bounded assumption is holding
(values of δ\delta in (0,1)(0,1)) for a wide range of representative
experimental conditions and, consequently, we can use Theorem
[1](#Thmtheorem1 "Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry") to provide a range on the performance of
the LS estimator. Note that the idealized condition of δ≈0\delta\approx 0 is realized only for the very high SNR regime (strong signals).

### IV.2 Performance Analysis of the LS estimator

We adopt equation ([18](#S3.E18 "In Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) which provides an
admissible range for the MSE performance of the LS estimator. For that
we use the critical δ\delta obtained in Figure [2](#A3.F2 "Figure 2 ‣ Performance analysis of the Least-Squares estimator in
Astrometry"). These
curves for the different SNR regimes and pixel resolutions are shown
in Figure [3](#A3.F3 "Figure 3 ‣ Performance analysis of the Least-Squares estimator in
Astrometry"). Following the trend reported in
Figure [2](#A3.F2 "Figure 2 ‣ Performance analysis of the Least-Squares estimator in
Astrometry"), the nominal value σLS2\sigma\_{LS}^{2} is a precise
indicator for the LS estimator performance for strong signals
(matching the idealized conditions stated in Remark
[4](#Thmremark4 "Remark 4 ‣ III.3 Analysis and interpretation of Theorem ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")), while on the other hand, Theorem
[1](#Thmtheorem1 "Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry") does not indicate whether σLS2\sigma\_{LS}^{2}
is accurate or not for low SNR, as we deviate from the idealized case
elaborated in Remark [3](#Thmremark3 "Remark 3 ‣ III.3 Analysis and interpretation of Theorem ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry"). Nevertheless, we will
see, based on some complementary empirical results reported in what
follows, that even for low SNR, the nominal σLS2\sigma\_{LS}^{2} predicts
the performance of the LS estimator quite well.

Assuming for a moment the idealized case in which δ≪1\delta\ll 1, we can
reduce the performance analysis to measuring the gap between the
nominal value predicted by Theorem [1](#Thmtheorem1 "Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")
(equation ([19](#S3.E19 "In Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry"))), and the CR bound in Proposition
[1](#Thmpreposition1 "Proposition 1 ‣ II.2 The Cramér-Rao bound ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry"). Figure [4](#A3.F4 "Figure 4 ‣ Performance analysis of the Least-Squares estimator in
Astrometry") shows the
relative difference given by e%=σLS2−σCR2σCR2⋅100e\_{\%}=\frac{\sigma\_{LS}^{2}-\sigma\_{CR}^{2}}{\sigma\_{CR}^{2}}\cdot 100. From
the figure we can clearly see that, in the low SNR regime, the
relative performance differences tends to zero and, consequently, the
LS estimator approaches the CR bound, and it is therefore an efficient
estimator. This matches what has been stated in Remark
[3](#Thmremark3 "Remark 3 ‣ III.3 Analysis and interpretation of Theorem ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry"). On the other hand for high SNR, we observe a
performance gap that is non negligible (up to ≈27%\approx 27\% relative
difference above the CR for F~=60 160\tilde{F}=60\,160 e−e^{-}, and ≈15%\approx 15\% above the CR for F~=20 004\tilde{F}=20\,004 e−e^{-} for Δx=0.2\Delta x=0.2 arcsec). This is consistent with what has been argued in Remark
[4](#Thmremark4 "Remark 4 ‣ III.3 Analysis and interpretation of Theorem ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry"). Note that in this regime, the idealized
scenario in which δ≪1\delta\ll 1 is valid (see Figure [2](#A3.F2 "Figure 2 ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) and,
thus, 𝔼In∼fxc{(τLS(In)−xc)2}≈σLS2\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{\left(\tau\_{LS}(I^{n})-x\_{c}\right)^{2}\right\}\approx\sigma\_{LS}^{2}, which is not
strictly the case for the low SNR regime (although see
Figure [6](#A3.F6 "Figure 6 ‣ Performance analysis of the Least-Squares estimator in
Astrometry"), and the discussion that follows).

To refine the relative performance analysis presented in
Figure [4](#A3.F4 "Figure 4 ‣ Performance analysis of the Least-Squares estimator in
Astrometry"), Figure [5](#A3.F5 "Figure 5 ‣ Performance analysis of the Least-Squares estimator in
Astrometry") shows the feasible range
(predicted by Theorem [1](#Thmtheorem1 "Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) of performance gap
considering the critical δ\delta obtained in Figure [2](#A3.F2 "Figure 2 ‣ Performance analysis of the Least-Squares estimator in
Astrometry").
We report four cases, from very low to very high SNR
regimes, to illustrate the trends. From this figure, we can see that
the deviations from the nominal value are quite significant for the
low SNR regime, and that, from this perspective, the range obtained
from Theorem [1](#Thmtheorem1 "Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry") is not sufficiently small to
conclude about the goodness of the LS estimator in this context. On
the other hand, in the high SNR regime, the nominal comparison can be
considered quite precise.

The results of the previous paragraph motivate an empirical analysis
to estimate the performance of the LS estimator empirically from the
data, with the goal of resolving the low SNR regime illustrated in
Figure [5](#A3.F5 "Figure 5 ‣ Performance analysis of the Least-Squares estimator in
Astrometry"). For this purpose, 1 0001\,000 realizations were
considered for all the SNR regimes and pixel sizes, and the
performance of the LS estimator was computed using the empirical
MSE. We used a large number of samples to guarantee convergence to the
true MSE error as a consequence of the law of large numbers
([Gray &
Davisson 2010](#bib.bib15)). Remarkably, we observe in all cases that the
estimated performance matches quite tightly the nominal
σLS2\sigma\_{LS}^{2} characterized by Theorem [1](#Thmtheorem1 "Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry").
We illustrate this in Figure [6](#A3.F6 "Figure 6 ‣ Performance analysis of the Least-Squares estimator in
Astrometry"), which considers the most
critical low SNR regime202020
Similar results were obtained in the
other regimes, not reported here for the sake of brevity..
Consequently, from this numerical analysis, we can resolve the
ambiguity present in the low SNR regime, and conclude that the
comparison with the nominal result reported in Figure [4](#A3.F4 "Figure 4 ‣ Performance analysis of the Least-Squares estimator in
Astrometry"), and
the derived conclusion about the LS estimator in the low and high SNR
regimes, can be considered valid. Our simulations also show that the
LS estimator is unbiased. Overall, these results suggests that Theorem
[1](#Thmtheorem1 "Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry") could be improved, perhaps by imposing
milder sufficient conditions, in order to prove that σLS2\sigma\_{LS}^{2}
is indeed a precise indicator of the MSE of the LS estimator at any
SNR regime.

For completeness, we show in Figure [7](#A3.F7 "Figure 7 ‣ Performance analysis of the Least-Squares estimator in
Astrometry") the behavior of
the log-likelihood function (computed using equation ([13](#S3.E13 "In III.1 Non achievability ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")))
and the LS function J⁡(In,xc)J(I^{n},x\_{c}) (computed using
equation ([16](#S3.E16 "In III.1 Non achievability ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry"))) for our two extreme SNR cases
of our numerical simulations, namely SNR= 12 and SNR= 230. In these
figures the true astrometric position is at xc=80x\_{c}=80 arcsec (= 400 pix
with Δx\Delta x = 0.2 arcsec). These figures clearly show
(particularly the one at low SNR) the non-linear nature of both
objective functions.

V Summary and Final Remarks
---------------------------

Our work provides results to characterize the performance of the
widely used LS estimator as applied to the problem of astrometry when
derived from digital discrete array detectors. The main result
(Theorem [1](#Thmtheorem1 "Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) provides in closed-form a
nominal value (σLS2(n)\sigma^{2}\_{LS}(n)), and a range around it, for the MSE
of the LS estimator as well as its bias. From the predicted nominal
value, we analyzed how efficient is the LS estimator in comparison
with the MV CR bound. In particular, we show that the LS estimator is
efficient in the regime of low SNR (a point source with a weak
signal), in the sense that it approximates very closely the CR
bound. On the other hand, we show that at high SNR there is a
significant gap in the performance of the LS estimator with respect to
the MV bound. We believe that this sub-optimal behavior is caused by
the Poissonian nature of the detection process, in which the variance
per pixel increases as the signal itself. Since the LS method is very
sensitive to outliers, the large excursions caused by the large pixel
intensity variance at high SNR make the LS method less efficient (from
the point of view of its MSE), than allowed by the CR bound. These
performance analyses complement and match what has been observed in
photometric estimation, where only in the low SNR regime the LS
estimator has been shown to asymptotically achieve the CR bound.

While our results are valid for an idealized linear (one-dimensional)
array detector where intra-pixel response changes are neglected, and
where flat-fielding is achieved with very high accuracy, our findings
should motivate the exploration of alternative estimators in the high
SNR observational regime. Regarding this last point, we note that an
inspection of [Mendez
et al. 2013](#bib.bib34) suggests that either a
(Poisson variance-) weighted LS or a ML approach do not exhibit this
loss of optimality at high-SNR, and should be preferred to the
unweighted LS analyzed in this paper. This effect is clearly
illustrated in Figure [8](#A3.F8 "Figure 8 ‣ Performance analysis of the Least-Squares estimator in
Astrometry"), where we present a
comparison between the standard deviation of the LS and ML methods
derived from numerical simulations in the very high SNR regime
(where the gap between CR and the LS is most significant). Motivated
by these results, a detailed analysis of the ML method will be
presented in a forthcoming paper.

VI Acknowledgments
------------------

We are indebted to an anonymous referee that read the draft carefully
and in great detail, providing us with several suggestions and
comments that have improved the legibility of the text
significantly. In particular his/her suggestions have lead to the
introduction of Figures 7, 8 and the corresponding discussion in the
body of the paper.

This material is based on work supported by a grant from
CONICYT-Chile, Fondecyt # 1151213. In addition, the work of
J. F. Silva and M. Orchard is supported by the Advanced Center for
Electrical and Electronic Engineering, Basal Project
FB0008. J. F. Silva acknowledges support from a CONICYT-Fondecyt grant
# 1140840 , and R. A. Mendez acknowledges support from Project
IC120009 Millennium Institute of Astrophysics (MAS) of the Iniciativa
Científica Milenio del Ministerio de Economía, Fomento y
Turismo de Chile. R.A.M also acknowledges ESO/Chile for hosting him
during his sabbatical-leave during 2014.

Appendix A Proof of Proposition [2](#Thmpreposition2 "Proposition 2 ‣ III.1 Non achievability ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

We use the well-known fact that the CR bound is achieved by an
unbiased estimator, if and only if, the following decomposition holds
([Kendall
et al. 1999](#bib.bib22), pp. 12)

|  |  |  |  |
| --- | --- | --- | --- |
|  | dln⁡L(In,θ)dθ=A⁡(θ,n)⋅(f⁡(In)−θ),\frac{d\ln L(I^{n};\theta)}{d\theta}=A(\theta,n)\cdot(f(I^{n})-\theta), |  | (A1) |

where L⁡(In,θ)L(I^{n};\theta) is the likelihood of the observation In∈ℕnI^{n}\in\mathbb{N}^{n} given θ\theta, A⁡(θ,n)A(\theta,n) is a function of θ\theta
and nn alone (i.e., it does dot depend on the data), while f⁡(In)f(I^{n})
is a function of the data exclusively (i.e., it does not depend on the
parameter). Furthermore, if the achievability condition in
equation ([A1](#A1.E1 "In Appendix A Proof of Proposition ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) is satisfied, then
A⁡(θ,n)=ℐθ(n)A(\theta,n)=\mathcal{I}\_{\theta}(n), and f⁡(In)f(I^{n}) is an unbiased
estimator of θ\theta that achieves the CR bound.

The proof follows by contradiction, assuming that
equation ([A1](#A1.E1 "In Appendix A Proof of Proposition ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) holds. First using
equation ([5](#S2.E5 "In II.1 Astrometry and photometry based on a photon integrating device ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")), we have that:

|  |  |  |  |
| --- | --- | --- | --- |
|  | dln⁡L⁡(In,xc)dxc=∑i=1n[Iiλi(xc)⋅dλi(xc)dxc−dλi(xc)dxc]=∑i=1nIiλi(xc)⋅dλi(xc)dxc,\displaystyle\frac{d\ln L(I^{n};x\_{c})}{dx\_{c}}=\sum\_{i=1}^{n}\left[\frac{I\_{i}}{\lambda\_{i}(x\_{c})}\cdot\frac{d\lambda\_{i}(x\_{c})}{dx\_{c}}-\frac{d\lambda\_{i}(x\_{c})}{dx\_{c}}\right]=\sum\_{i=1}^{n}\frac{I\_{i}}{\lambda\_{i}(x\_{c})}\cdot\frac{d\lambda\_{i}(x\_{c})}{dx\_{c}}, |  | (A2) |

the last equality comes from the fact that ∑i=1ngi(xc)=1\sum\_{i=1}^{n}g\_{i}(x\_{c})=1
from the assumption in equation ([4](#S2.E4 "In II.1 Astrometry and photometry based on a photon integrating device ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")). Then replacing
equations ([A2](#A1.E2 "In Appendix A Proof of Proposition ‣ Performance analysis of the Least-Squares estimator in
Astrometry"))
and ([12](#S2.E12 "In Proposition 1 ‣ II.2 The Cramér-Rao bound ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) in
equation ([A1](#A1.E1 "In Appendix A Proof of Proposition ‣ Performance analysis of the Least-Squares estimator in
Astrometry")):

|  |  |  |  |
| --- | --- | --- | --- |
|  | f⁡(In)=∑i=1nIiF~gi(xc)+B~i⋅dgi(xc)dxcF~∑i=1n1F~gi(xc)+B~i⋅(dgi(xc)dxc)2+xc,\displaystyle f(I^{n})=\sum\_{i=1}^{n}\frac{\frac{I\_{i}}{\tilde{F}g\_{i}(x\_{c})+\tilde{B}\_{i}}\cdot\frac{dg\_{i}(x\_{c})}{dx\_{c}}}{\tilde{F}\sum\_{i=1}^{n}\frac{1}{\tilde{F}g\_{i}(x\_{c})+\tilde{B}\_{i}}\cdot\left(\frac{dg\_{i}(x\_{c})}{dx\_{c}}\right)^{2}}+x\_{c}, |  | (A3) |

which contradicts the assumption that f⁡(In)f(I^{n}) should be a function of
the data alone. Furthermore, if we consider the extreme high SNR
regime, where F~gi(xc)≫B~i\tilde{F}g\_{i}(x\_{c})\gg\tilde{B}\_{i} for all ii, and
the low SNR regime, where F~gi(xc)≪B~i\tilde{F}g\_{i}(x\_{c})\ll\tilde{B}\_{i} for all
ii, it follows that:

|  |  |  |  |
| --- | --- | --- | --- |
|  | f⁡(In)=∑i=1nIi⋅dln⁡gi(xc)dxc⋅[F~∑i=1n(dgi(xc)dxc)2/gi(xc)]−1+xcf(I^{n})=\sum\_{i=1}^{n}I\_{i}\cdot\frac{d\ln g\_{i}(x\_{c})}{dx\_{c}}\cdot\left[\tilde{F}\sum\_{i=1}^{n}\left(\frac{dg\_{i}(x\_{c})}{dx\_{c}}\right)^{2}/g\_{i}(x\_{c})\right]^{-1}+x\_{c} |  | (A4) |

and

|  |  |  |  |
| --- | --- | --- | --- |
|  | f⁡(In)=∑i=1nIiB~i⋅dgi(xc)dxc⋅[F~∑i=1n(dgi(xc)dxc)2/B~i]−1+xc,f(I^{n})=\sum\_{i=1}^{n}\frac{I\_{i}}{\tilde{B}\_{i}}\cdot\frac{dg\_{i}(x\_{c})}{dx\_{c}}\cdot\left[\tilde{F}\sum\_{i=1}^{n}\left(\frac{dg\_{i}(x\_{c})}{dx\_{c}}\right)^{2}/\tilde{B}\_{i}\right]^{-1}+x\_{c}, |  | (A5) |

respectively. Therefore a contradiction remains even in these extreme
SNR regimes.

Appendix B Proof of Theorem [1](#Thmtheorem1 "Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

The approach of [So et al. 2013](#bib.bib43) uses the fact that the
objective function J⁡(In,α)J(I^{n},\alpha) in
equation ([16](#S3.E16 "In III.1 Non achievability ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) is two times
differentiable, which is satisfied in our context. As a
short-hand, if we denote by x^c\hat{x}\_{c} the LS estimator
solution τLS(In)\tau\_{LS}(I^{n}), then the first order necessary
condition for a local optimum requires that J′(In,x^c)≡dJ(In,α)dα|α=x^c=0J^{\prime}(I^{n},\hat{x}\_{c})\equiv\frac{dJ(I^{n},\alpha)}{d\alpha}|\_{\alpha=\hat{x}\_{c}}=0. The other key assumption in
[So et al. 2013](#bib.bib43) is that x^c\hat{x}\_{c} is in a close neighborhood
of the true value xcx\_{c}. In our case, this has to do with the
quality of the pixel-based data used for the inference, which
we assume it offers a good estimation of the position (see,
e.g., [King 1983](#bib.bib24); [Stone 1989](#bib.bib45)). Then using a first
order Taylor expansion of J′(In,x^c)J^{\prime}(I^{n},\hat{x}\_{c}) around xcx\_{c},
the following key approximation can be adopted ([So et al. 2013](#bib.bib43), their
equation (4)):

|  |  |  |  |
| --- | --- | --- | --- |
|  | 0=J′(In,x^c)=J′(In,xc)+(x^c−xc)⋅J′′(In,xc)⇔(xc−x^c)=J′(In,xc)J′′(In,xc),0=J^{\prime}(I^{n},\hat{x}\_{c})=J^{\prime}(I^{n},x\_{c})+(\hat{x}\_{c}-x\_{c})\cdot J^{\prime\prime}(I^{n},x\_{c})\Leftrightarrow(x\_{c}-\hat{x}\_{c})=\frac{J^{\prime}(I^{n},x\_{c})}{J^{\prime\prime}(I^{n},x\_{c})}, |  | (B1) |

where J′′(In,xc)≡d2J(In,α)d2α|α=xcJ^{\prime\prime}(I^{n},x\_{c})\equiv\frac{d^{2}J(I^{n},\alpha)}{d^{2}\alpha}|\_{\alpha=x\_{c}}. If we consider In∼fxcI^{n}\sim f\_{x\_{c}},
then from equation ([B1](#A2.E1 "In Appendix B Proof of Theorem ‣ Performance analysis of the Least-Squares estimator in
Astrometry")):

|  |  |  |  |
| --- | --- | --- | --- |
|  | xc−τLS(In)=J′(In,xc)J′′(In,xc).x\_{c}-\tau\_{LS}(I^{n})=\frac{J^{\prime}(I^{n},x\_{c})}{J^{\prime\prime}(I^{n},x\_{c})}. |  | (B2) |

The second step in the approximation proposed by
[So et al. 2013](#bib.bib43) is to bound J′(In,xc)J′′(In,xc)\frac{J^{\prime}(I^{n},x\_{c})}{J^{\prime\prime}(I^{n},x\_{c})}
by J′(In,xc)𝔼In∼fxc{J′′(In,xc)}\frac{J^{\prime}(I^{n},x\_{c})}{\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{J^{\prime\prime}(I^{n},x\_{c})\right\}}. For that we introduce the residual
variable W⁡(In,α)W(I^{n},\alpha) where J′′(In,xc)=𝔼In∼fxc{J′′(In,xc)}(1+W⁡(In,xc))J^{\prime\prime}(I^{n},x\_{c})=\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{J^{\prime\prime}(I^{n},x\_{c})\right\}(1+W(I^{n},x\_{c})). Using the fact that W⁡(In,α)W(I^{n},\alpha) is
bounded almost surely (see Remark [1](#Thmremark1 "Remark 1 ‣ III.3 Analysis and interpretation of Theorem ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry"), and
Section [IV.1](#S4.SS1 "IV.1 Analyzing the bounded condition over 
          
            
              W
              
                
                  
                  
                  
                
                
                  (
                  
                    
                    I
                    n
                  
                  ,
                  α
                  ) ‣ IV Numerical analysis of the LS estimator ‣ Performance analysis of the Least-Squares estimator in
Astrometry")):

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  | |J′(In,xc)𝔼In∼fxc{J′′(In,xc)}−J′(In,xc)J′′(In,xc)|\displaystyle\left|\frac{J^{\prime}(I^{n},x\_{c})}{\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{J^{\prime\prime}(I^{n},x\_{c})\right\}}-\frac{J^{\prime}(I^{n},x\_{c})}{J^{\prime\prime}(I^{n},x\_{c})}\right| | =\displaystyle= | |J′(In,xc)𝔼In∼fxc{J′′(In,xc)}⋅[1−11+W⁡(In,xc)]|\displaystyle\left|\frac{J^{\prime}(I^{n},x\_{c})}{\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{J^{\prime\prime}(I^{n},x\_{c})\right\}}\cdot\left[1-\frac{1}{1+W(I^{n},x\_{c})}\right]\right| |  | (B3) |
|  |  | ≤\displaystyle\leq | |J′(In,xc)𝔼In∼fxc{J′′(In,xc)}|⋅maxw∈(−δ,δ)⁡|1−11+w|\displaystyle\left|\frac{J^{\prime}(I^{n},x\_{c})}{\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{J^{\prime\prime}(I^{n},x\_{c})\right\}}\right|\cdot\max\_{w\in(-\delta,\delta)}\left|1-\frac{1}{1+w}\right| |  |
|  |  | ≤\displaystyle\leq | |J′(In,xc)|𝔼In∼fxc{J′′(In,xc)}⋅δ1−δ,\displaystyle\frac{\left|J^{\prime}(I^{n},x\_{c})\right|}{\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{J^{\prime\prime}(I^{n},x\_{c})\right\}}\cdot\frac{\delta}{1-\delta}, |  |

the last step uses the fact that 𝔼In∼fxc{J′′(In,xc)}≥0\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{J^{\prime\prime}(I^{n},x\_{c})\right\}\geq 0 (see Remark
[1](#Thmremark1 "Remark 1 ‣ III.3 Analysis and interpretation of Theorem ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")). On the other hand, Jensen’s inequality
([Cover &
Thomas 2006](#bib.bib9)) guarantees that:

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  | |𝔼In∼fxc{J′(In,xc)}𝔼In∼fxc{J′′(In,xc)}−𝔼In∼fxc{J′(In,xc)J′′(In,xc)}|\displaystyle\left|\frac{\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{J^{\prime}(I^{n},x\_{c})\right\}}{\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{J^{\prime\prime}(I^{n},x\_{c})\right\}}-\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{\frac{J^{\prime}(I^{n},x\_{c})}{J^{\prime\prime}(I^{n},x\_{c})}\right\}\right| | ≤\displaystyle\leq | 𝔼In∼fxc{|J′(In,xc)𝔼In∼fxc{J′′(In,xc)}−J′(In,xc)J′′(In,xc)|}\displaystyle\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{\left|\frac{J^{\prime}(I^{n},x\_{c})}{\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{J^{\prime\prime}(I^{n},x\_{c})\right\}}-\frac{J^{\prime}(I^{n},x\_{c})}{J^{\prime\prime}(I^{n},x\_{c})}\right|\right\} |  | (B4) |
|  |  | ≤\displaystyle\leq | 𝔼In∼fxc{|J′(In,xc)|}𝔼In∼fxc{J′′(In,xc)}⋅δ1−δ,\displaystyle\frac{\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{\left|J^{\prime}(I^{n},x\_{c})\right|\right\}}{\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{J^{\prime\prime}(I^{n},x\_{c})\right\}}\cdot\frac{\delta}{1-\delta}, |  |

where the last inequality comes from
equation ([B3](#A2.E3 "In Appendix B Proof of Theorem ‣ Performance analysis of the Least-Squares estimator in
Astrometry")). Then we use that J′(In,xc)=2⋅∑i=1n(λi(xc)−Ii)⋅dλi(xc)dxcJ^{\prime}(I^{n},x\_{c})=2\cdot\sum\_{i=1}^{n}(\lambda\_{i}(x\_{c})-I\_{i})\cdot\frac{d\lambda\_{i}(x\_{c})}{dx\_{c}}, and consequently 𝔼In∼fxc{J′(In,xc)}=0\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{J^{\prime}(I^{n},x\_{c})\right\}=0. Then from
equations ([B4](#A2.E4 "In Appendix B Proof of Theorem ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) and ([B2](#A2.E2 "In Appendix B Proof of Theorem ‣ Performance analysis of the Least-Squares estimator in
Astrometry")), we have
that:

|  |  |  |  |
| --- | --- | --- | --- |
|  | |xc−𝔼In∼fxc{τLS(In)}|≤𝔼In∼fxc{|J′(In,xc)|}𝔼In∼fxc{J′′(In,xc)}⋅δ1−δ,\left|x\_{c}-\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{\tau\_{LS}(I^{n})\right\}\right|\leq\frac{\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{\left|J^{\prime}(I^{n},x\_{c})\right|\right\}}{\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{J^{\prime\prime}(I^{n},x\_{c})\right\}}\cdot\frac{\delta}{1-\delta}, |  | (B5) |

which leads to equation ([17](#S3.E17 "In Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")).

Concerning the MSE, from the hypothesis on W⁡(In,xc)W(I^{n},x\_{c}) we have that:

|  |  |  |  |
| --- | --- | --- | --- |
|  | J′(In,xc)2𝔼In∼fxc{J′′(In,xc)}2(1+δ)2≤(J′(In,xc)J′′(In,xc))2≤J′(In,xc)2𝔼In∼fxc{J′′(In,xc)}2(1−δ)2,\frac{J^{\prime}(I^{n},x\_{c})^{2}}{\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{J^{\prime\prime}(I^{n},x\_{c})\right\}^{2}(1+\delta)^{2}}\leq\left(\frac{J^{\prime}(I^{n},x\_{c})}{J^{\prime\prime}(I^{n},x\_{c})}\right)^{2}\leq\frac{J^{\prime}(I^{n},x\_{c})^{2}}{\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{J^{\prime\prime}(I^{n},x\_{c})\right\}^{2}(1-\delta)^{2}}, |  | (B6) |

almost surely. Then taking the expected value in
equation ([B6](#A2.E6 "In Appendix B Proof of Theorem ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) and using
equation ([B2](#A2.E2 "In Appendix B Proof of Theorem ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) for the central term, it follows
that:

|  |  |  |
| --- | --- | --- |
|  | 𝔼In∼fxc{J′(In,xc)2}𝔼In∼fxc{J′′(In,xc)}2(1+δ)2≤𝔼In∼fxc{(xc−τLS(In))2}≤𝔼In∼fxc{J′(In,xc)2}𝔼In∼fxc{J′′(In,xc)}2(1−δ)2,\frac{\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{J^{\prime}(I^{n},x\_{c})^{2}\right\}}{\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{J^{\prime\prime}(I^{n},x\_{c})\right\}^{2}(1+\delta)^{2}}\leq\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{\left(x\_{c}-\tau\_{LS}(I^{n})\right)^{2}\right\}\\ \leq\frac{\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{J^{\prime}(I^{n},x\_{c})^{2}\right\}}{\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\left\{J^{\prime\prime}(I^{n},x\_{c})\right\}^{2}(1-\delta)^{2}}, |  |

which concludes the result.

Appendix C Proof of Proposition [3](#Thmpreposition3 "Proposition 3 ‣ Remark 4 ‣ III.3 Analysis and interpretation of Theorem ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Recalling from equation ([3](#S2.E3 "In II.1 Astrometry and photometry based on a photon integrating device ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) that
gi(xc)=∫xi−Δx2xi+Δx2ϕ⁡(x−xc,σ)𝑑xg\_{i}(x\_{c})=\int\_{x\_{i}-\frac{\Delta x}{2}}^{x\_{i}+\frac{\Delta x}{2}}\phi(x-x\_{c},\sigma)\,dx and assuming a Gaussian PSF of the form
ϕ⁡(x,σ)=12πσexp⁡(−x22σ2)\phi(x,\sigma)=\frac{1}{\sqrt{2\pi}\,\sigma}\exp{\left(\frac{-x^{2}}{2\sigma^{2}}\right)} (see
Section [IV](#S4 "IV Numerical analysis of the LS estimator ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) by the mean value theorem and the
hypothesis of small pixel (Δx/σ≪1\Delta x/\sigma\ll 1), it is possible to
state that:

|  |  |  |  |
| --- | --- | --- | --- |
|  | gi(xc)≈ϕ⁡(xi−xc,σ)⋅Δx,g\_{i}(x\_{c})\approx\phi(x\_{i}-x\_{c},\sigma)\cdot\Delta x, |  | (C1) |

and then we have that:

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  | dgi(xc)dxc\displaystyle\frac{dg\_{i}(x\_{c})}{dx\_{c}} | ≈\displaystyle\approx | (xi−xc)σ2⋅12πσexp⁡(−(xi−xc)22σ2)⋅Δx\displaystyle\frac{(x\_{i}-x\_{c})}{\sigma^{2}}\cdot\frac{1}{\sqrt{2\pi}\,\sigma}\exp\left(\frac{-(x\_{i}-x\_{c})^{2}}{2\sigma^{2}}\right)\cdot\Delta x |  | (C2) |
|  |  | =\displaystyle= | (xi−xc)σ2⋅ϕ⁡(xi−xc,σ)⋅Δx.\displaystyle\frac{(x\_{i}-x\_{c})}{\sigma^{2}}\cdot\phi(x\_{i}-x\_{c},\sigma)\cdot\Delta x. |  |

With the above approximation we have that:

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  | ∑i=1n(dgi(xc)dxc)2gi(xc)\displaystyle\sum\_{i=1}^{n}\left(\frac{dg\_{i}(x\_{c})}{dx\_{c}}\right)^{2}g\_{i}(x\_{c}) | ≈\displaystyle\approx | ∑i=1n((xi−xc)σ2⋅ϕ⁡(xi−xc,σ)⋅Δx)2⋅ϕ⁡(xi−xc,σ)⋅Δx\displaystyle\sum\_{i=1}^{n}\left(\frac{(x\_{i}-x\_{c})}{\sigma^{2}}\cdot\phi(x\_{i}-x\_{c},\sigma)\cdot\Delta x\right)^{2}\cdot\phi(x\_{i}-x\_{c},\sigma)\cdot\Delta x |  | (C3) |
|  |  | ≈\displaystyle\approx | Δx223πσ6⋅∑i=1n(xi−xc)212πσ3exp⁡(−(xi−xc)22(σ3)2)⋅Δx.\displaystyle\frac{\Delta x^{2}}{2\sqrt{3}\pi\sigma^{6}}\cdot\sum\_{i=1}^{n}(x\_{i}-x\_{c})^{2}\frac{1}{\sqrt{2\pi}\frac{\sigma}{\sqrt{3}}}\exp\left(\frac{-(x\_{i}-x\_{c})^{2}}{2\left(\frac{\sigma}{\sqrt{3}}\right)^{2}}\right)\cdot\Delta x. |  |

The term inside the summation in equation ([C3](#A3.E3 "In Appendix C Proof of Proposition ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) can
be approximated by an integral due to the small-pixel
hypothesis. Assuming that the source is well sampled by the detector
(see Section [II.1](#S2.SS1 "II.1 Astrometry and photometry based on a photon integrating device ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry"), equation ([4](#S2.E4 "In II.1 Astrometry and photometry based on a photon integrating device ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry"))) we
can obtain that:

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  | ∑i=1n(dgi(xc)dxc)2gi(xc)\displaystyle\sum\_{i=1}^{n}\left(\frac{dg\_{i}(x\_{c})}{dx\_{c}}\right)^{2}g\_{i}(x\_{c}) | ≈\displaystyle\approx | Δx223πσ6∫−∞+∞(x−xc)212πσ3exp⁡(−(x−xc)22(σ3)2)𝑑x\displaystyle\frac{\Delta x^{2}}{2\sqrt{3}\pi\sigma^{6}}\int\_{-\infty}^{+\infty}(x-x\_{c})^{2}\frac{1}{\sqrt{2\pi}\frac{\sigma}{\sqrt{3}}}\exp\left(\frac{-(x-x\_{c})^{2}}{2\left(\frac{\sigma}{\sqrt{3}}\right)^{2}}\right)dx |  | (C4) |
|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  | =\displaystyle= | Δx223πσ6⋅σ23=Δx263πσ4,\displaystyle\frac{\Delta x^{2}}{2\sqrt{3}\pi\sigma^{6}}\cdot\frac{\sigma^{2}}{3}=\frac{\Delta x^{2}}{6\sqrt{3}\pi\sigma^{4}}, |  | (C5) |

where equation ([C5](#A3.E5 "In Appendix C Proof of Proposition ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) follows from the fact that the
term inside the integral in equation ([C4](#A3.E4 "In Appendix C Proof of Proposition ‣ Performance analysis of the Least-Squares estimator in
Astrometry"))
corresponds to the second moment of a normal random variable of mean
xcx\_{c} and variance σ23\frac{\sigma^{2}}{3}.

By the same set of arguments used to approximate
∑i=1n(dgi(xc)dxc)2gi(xc)\sum\_{i=1}^{n}\left(\frac{dg\_{i}(x\_{c})}{dx\_{c}}\right)^{2}g\_{i}(x\_{c}) in
equation ([C5](#A3.E5 "In Appendix C Proof of Proposition ‣ Performance analysis of the Least-Squares estimator in
Astrometry")), we have that:

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  | ∑i=1n(dgi(xc)dxc)2\displaystyle\sum\_{i=1}^{n}\left(\frac{dg\_{i}(x\_{c})}{dx\_{c}}\right)^{2} | ≈\displaystyle\approx | ∑i=1n((xi−xc)σ2⋅ϕ⁡(xi−xc,σ)⋅Δx)2\displaystyle\sum\_{i=1}^{n}\left(\frac{(x\_{i}-x\_{c})}{\sigma^{2}}\cdot\phi(x\_{i}-x\_{c},\sigma)\cdot\Delta x\right)^{2} |  | (C6) |
|  |  | ≈\displaystyle\approx | Δx2πσ5⋅∑i=1n(xi−xc)212πσ2exp⁡(−(xi−xc)22(σ2)2)⋅Δx\displaystyle\frac{\Delta x}{2\sqrt{\pi}\sigma^{5}}\cdot\sum\_{i=1}^{n}(x\_{i}-x\_{c})^{2}\frac{1}{\sqrt{2\pi}\frac{\sigma}{\sqrt{2}}}\exp\left(\frac{-(x\_{i}-x\_{c})^{2}}{2\left(\frac{\sigma}{\sqrt{2}}\right)^{2}}\right)\cdot\Delta x |  |
|  |  | ≈\displaystyle\approx | Δx2πσ5∫−∞+∞(x−xc)212πσ2exp⁡(−(x−xc)22(σ2)2)𝑑x\displaystyle\frac{\Delta x}{2\sqrt{\pi}\sigma^{5}}\int\_{-\infty}^{+\infty}(x-x\_{c})^{2}\frac{1}{\sqrt{2\pi}\frac{\sigma}{\sqrt{2}}}\exp\left(\frac{-(x-x\_{c})^{2}}{2\left(\frac{\sigma}{\sqrt{2}}\right)^{2}}\right)dx |  |
|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  | ≈\displaystyle\approx | Δx2πσ5⋅σ22=Δx4πσ3,\displaystyle\frac{\Delta x}{2\sqrt{\pi}\sigma^{5}}\cdot\frac{\sigma^{2}}{2}=\frac{\Delta x}{4\sqrt{\pi}\sigma^{3}}, |  | (C7) |

where equation ([C7](#A3.E7 "In Appendix C Proof of Proposition ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) follows from the fact that the term
inside the integral in equation ([C6](#A3.E6 "In Appendix C Proof of Proposition ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) is the second
moment of a normal random variable of mean xcx\_{c} and variance
σ22\frac{\sigma^{2}}{\sqrt{2}}.

Finally, for ∑i=1n(dgi(xc)dxc)2⋅1gi(xc)\sum\_{i=1}^{n}\left(\frac{dg\_{i}(x\_{c})}{dx\_{c}}\right)^{2}\cdot\frac{1}{g\_{i}(x\_{c})} we proceed again in the same way, namely:

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  | ∑i=1n(dgi(xc)dxc)21gi(xc)\displaystyle\sum\_{i=1}^{n}\left(\frac{dg\_{i}(x\_{c})}{dx\_{c}}\right)^{2}\frac{1}{g\_{i}(x\_{c})} | ≈\displaystyle\approx | ∑i=1n((xi−xc)σ2⋅ϕ⁡(xi−xc,σ)⋅Δx)21ϕ⁡(xi−xc,σ)⋅Δx\displaystyle\sum\_{i=1}^{n}\left(\frac{(x\_{i}-x\_{c})}{\sigma^{2}}\cdot\phi(x\_{i}-x\_{c},\sigma)\cdot\Delta x\right)^{2}\frac{1}{\phi(x\_{i}-x\_{c},\sigma)\cdot\Delta x} |  | (C8) |
|  |  | ≈\displaystyle\approx | 1σ4∑i=1n(xi−xc)212πσexp⁡(−(xi−xc)22σ2)Δx\displaystyle\frac{1}{\sigma^{4}}\sum\_{i=1}^{n}(x\_{i}-x\_{c})^{2}\frac{1}{\sqrt{2\pi}\sigma}\exp\left(\frac{-(x\_{i}-x\_{c})^{2}}{2\sigma^{2}}\right)\Delta x |  |
|  |  | ≈\displaystyle\approx | 1σ4∫−∞+∞(x−xc)22πσexp⁡(−(x−xc)22σ2)𝑑x\displaystyle\frac{1}{\sigma^{4}}\int\_{-\infty}^{+\infty}\frac{(x-x\_{c})^{2}}{\sqrt{2\pi}\sigma}\exp\left(\frac{-(x-x\_{c})^{2}}{2\sigma^{2}}\right)dx |  |
|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  | ≈\displaystyle\approx | 1σ4⋅σ2=1σ2,\displaystyle\frac{1}{\sigma^{4}}\cdot\sigma^{2}=\frac{1}{\sigma^{2}}, |  | (C9) |

where equation ([C9](#A3.E9 "In Appendix C Proof of Proposition ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) follows from the fact that the term
inside the integral in equation ([C8](#A3.E8 "In Appendix C Proof of Proposition ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) corresponds to the
second moment of a normal random variable of mean xcx\_{c} and variance
σ2\sigma^{2}.

Then adopting equations ([C5](#A3.E5 "In Appendix C Proof of Proposition ‣ Performance analysis of the Least-Squares estimator in
Astrometry")), ([C7](#A3.E7 "In Appendix C Proof of Proposition ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) and
([C9](#A3.E9 "In Appendix C Proof of Proposition ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) in equations ([23](#S3.E23 "In Remark 2 ‣ III.3 Analysis and interpretation of Theorem ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) and
([12](#S2.E12 "In Proposition 1 ‣ II.2 The Cramér-Rao bound ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")), respectively,
and assuming a uniform background underneath the PSF, we have that:

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  | σLS2\displaystyle\sigma\_{LS}^{2} | =\displaystyle= | ∑i=1n(dgi(xc)dxc)2gi(xc)F~(∑i=1n(dgi(xc)dxc)2)2+B~F~2∑i=1n(dgi(xc)dxc)2\displaystyle\frac{\sum\_{i=1}^{n}\left(\frac{dg\_{i}(x\_{c})}{dx\_{c}}\right)^{2}g\_{i}(x\_{c})}{\tilde{F}\left(\sum\_{i=1}^{n}\left(\frac{dg\_{i}(x\_{c})}{dx\_{c}}\right)^{2}\right)^{2}}+\frac{\tilde{B}}{\tilde{F}^{2}\sum\_{i=1}^{n}\left(\frac{dg\_{i}(x\_{c})}{dx\_{c}}\right)^{2}} |  | (C10) |
|  |  | ≈\displaystyle\approx | Δx263πσ4F~(Δx4πσ3)2+B~F~2Δx4πσ3\displaystyle\frac{\frac{\Delta x^{2}}{6\sqrt{3}\pi\sigma^{4}}}{\tilde{F}\left(\frac{\Delta x}{4\sqrt{\pi}\sigma^{3}}\right)^{2}}+\frac{\tilde{B}}{\tilde{F}^{2}\frac{\Delta x}{4\sqrt{\pi}\sigma^{3}}} |  |
|  |  | =\displaystyle= | σ2F~[833+4π1ΔxσB~F~]≈σ2F~833\displaystyle\frac{\sigma^{2}}{\tilde{F}}\left[\frac{8}{3\sqrt{3}}+4\sqrt{\pi}\frac{1}{\frac{\Delta x}{\sigma}}\frac{\tilde{B}}{\tilde{F}}\right]\approx\frac{\sigma^{2}}{\tilde{F}}\frac{8}{3\sqrt{3}} |  |

and,

|  |  |  |  |
| --- | --- | --- | --- |
|  | σCR2=1∑i=1n(F~dgi(xc)dxc)2F~gi(xc)+B~=1F~∑i=1n(dgi(xc)dxc)21gi(xc)≈σ2F~.\sigma\_{CR}^{2}=\frac{1}{\sum\_{i=1}^{n}\frac{\left(\tilde{F}\frac{dg\_{i}(x\_{c})}{dx\_{c}}\right)^{2}}{\tilde{F}g\_{i}(x\_{c})+\tilde{B}}}=\frac{1}{\tilde{F}\sum\_{i=1}^{n}\left(\frac{dg\_{i}(x\_{c})}{dx\_{c}}\right)^{2}\frac{1}{g\_{i}(x\_{c})}}\approx\frac{\sigma^{2}}{\tilde{F}}. |  | (C11) |

In the last step in equation ([C10](#A3.E10 "In Appendix C Proof of Proposition ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) and the last step
in equation ([C11](#A3.E11 "In Appendix C Proof of Proposition ‣ Performance analysis of the Least-Squares estimator in
Astrometry")), we have used the assumption that
F~≫B~\tilde{F}\gg\tilde{B}. We note that the last step in
equation ([C11](#A3.E11 "In Appendix C Proof of Proposition ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) corresponds to the second line of
equation (45) in [Mendez
et al. 2013](#bib.bib34).

References
----------

* Adorf (1996)

  Adorf, H.-M. 1996, in Astronomical Data Analysis Software and
  Systems V, Vol. 101, 13
* Alard &
  Lupton (1998)
   Alard, C., & Lupton, R. H. 1998,
  AJ, 503, 325
* Auer &
  van Altena (1978)
   Auer, L., & van Altena, W. 1978,
  AJ, 83, 531
* Bastian (2004)
   Bastian, U. 2004. GAIA technical
  note, GAIA-C3-TN-ARI-BAS-020
  (http://www.cosmos.esa.int/web/gaia/public-dpac-documents). Available
  at
  http://www.rssd.esa.int/SYS/docs/ll\_transfers/project=PUBDB&id=2939027.pdf
  (last accessed on April 2015).
* Becker et al. (2007)
   Becker, A. C., Silvestri,
  N. M., Owen, R. E., Ivezić, Ž., & Lupton, R. H. 2007,
  PASP, 119, 1462
* Bendinelli
  et al. (1987)
   Bendinelli, O., Parmeggiani, G.,
  Piccioni, A., & Zavatti, F. 1987, AJ, 94, 1095
* Cameron
  et al. (2006)

  Cameron, A. C., et al. 2006, MNRAS,
  373, 799
* Chromey (2010)

  Chromey, F. R. 2010, To measure the sky: an introduction to observational
  astronomy (Cambridge University Press)
* Cover &
  Thomas (2006)

  Cover, T. M., & Thomas, J. A. 2006, Elements of Information Theory (second
  ed.) (Wiley Interscience, New York)
* Cramér (1946)

  Cramér, H. 1946, Scandinavian Actuarial Journal, 1946, 85
* Fessler (1996)

  Fessler, J. A. 1996, Image Processing, IEEE Transactions on, 5, 493
* Gawiser et al. (2006)
   Gawiser, E., van Dokkum,
  P. G., Herrera, D., et al. 2006, ApJS, 162, 1
* Gilliland (1992)
   Gilliland, R. L. 1992, in Astronomical Society of the Pacific
  Conference Series, Vol. 23, Astronomical CCD Observing and Reduction
  Techniques, ed. S. B. Howell, 68
* Freyhammer et al. (2001)
   Freyhammer, L. M.,
  Andersen, M. I., Arentoft, T., Sterken, C., & Nørregaard,
  P. 2001, Experimental Astronomy, 12, 147
* Gray &
  Davisson (2010)
   Gray, R. M., & Davisson, L. D. 2010,
  An Introduction to Statistical Signal Processing, Cambridge
  University Press
* Høg (2009)

  Høg, E. 2009, Experimental Astronomy, 25, 225
* Høg (2011)

  Høg, E. 2011, Baltic Astronomy, 20, 221
* Honeycutt (1992)

  Honeycutt, R. K. 1992, PASP,
  435
* Howell (2006)

  Howell, S. B. 2006, Handbook of CCD astronomy, Vol. 5 (Cambridge University
  Press)
* Jakobsen et al. (1992)

  Jakobsen, P., Greenfield, P., & Jedrzejewski, R. 1992, A&A, 253, 329
* Kay (1993)
   Kay, S. M. 1993, Fundamentals of
  Statistical Signal Processing, Volume I: Estimation Theory. Prentice
  Hall, New Jersey.
* Kendall
  et al. (1999)

  Kendall, M., Stuart, A., Ord, J., & Arnold, S. 1999, Vol. 2A: Classical
  inference and the linear model (London [etc.]: Arnold [etc.])
* King (1971)

  King, I. R. 1971, PASP, 199
* King (1983)

  King, I. R. 1983, PASP, 163
* Lattanzi (2012)

  Lattanzi, M. 2012, Mem. Soc. Astron. Italiana, 83, 1033
* Lee &
  van Altena (1983)

  Lee, J.-F., & van Altena, W. 1983, AJ, 88, 1683
* Lindegren (1978)

  Lindegren, L. 1978, in IAU Colloq. 48: Modern Astrometry, Vol. 1, 197
* Lindegren (2000)
   Lindegren, L. 2000, Gaia technical
  report Gaia-LL-032
* Lindegren (2010)
   Lindegren, L. 2010, ISSI Scientific Reports Series, 9, 279
* Lupton et al. (2001)
   Lupton, R., Gunn, J. E.,
  Ivezić, Z., Knapp, G. R., & Kent, S. 2001, Astronomical Data
  Analysis Software and Systems X, 238, 269
* Lupton (2007)
   Lupton, R. 2007, Statistical
  Challenges in Modern Astronomy IV, 371, 160
* Mason (2007)
   Mason, E. 2008, in The 2007 ESO
  Instrument Calibration Workshop, Kaufer, A., & Kerber, F. (eds.),
  Springer-Verlag, Berlin, 107
* Mendez
  et al. (2010)

  Mendez, R. A., Costa, E., Pedreros, M. H., Moyano, M., Altmann, M., &
  Gallart, C. 2010, PASP,
  122, 853
* Mendez
  et al. (2013)

  Mendez, R. A., Silva, J. F., & Lobos, R. 2013, PASP, 125, pp. 580
* Mendez
  et al. (2014)

  Mendez, R. A., Silva, J. F., Orostica, R., & Lobos, R. 2014, PASP, 126, 798
* Mighell (2005)

  Mighell, K. J. 2005, MNRAS, 361,
  861
* Najim (2008)
   Najim, M. 2008, Modeling, Estimation
  and Optimal Filtering in Signal Processing, Chapter A,
  335-340. Available at
  http://onlinelibrary.wiley.com/book/10.1002/9780470611104, last
  accessed on June 26th, 2015.
* Perryman
  et al. (1989)

  Perryman, M., Jakobsen, P., Colina, L., Lelievre, G., Macchetto, F., Nieto, J.,
  & Serego Alighieri, S. 1989, A&A, 215, 195
* Pier et al. (2003)
   Pier, J. R., Munn, J. A.,
  Hindsley, R. B., et al. 2003, AJ, 125, 1559
* Rao (1945)

  Rao, C. R. 1945, Bulletin of the Calcutta Mathematical Society, 37,
  81
* Raykar et al. (2005)
   Raykar, V. C.,
  Kozintsev, I. V., & Lienhart, R. 2005, Speech and Audio Processing,
  IEEE Transactions on, 13, 70
* Reffert (2009)

  Reffert, S. 2009, New A Rev., 53, 329
* So et al. (2013)

  So, H., Chan, Y., Ho, K., & Chen, Y. 2013, Signal Processing Magazine, IEEE,
  30, 162
* Stetson (1987)

  Stetson, P. B. 1987, PASP,
  191
* Stone (1989)

  Stone, R. C. 1989, AJ, 97, 1227
* Tyson (1986)

  Tyson, J. A. 1986, Journal of the Optical Society of America A, 3, 2131
* van Altena &
  Auer (1975)

  van Altena, W., & Auer, L. 1975, in Image Processing Techniques in Astronomy
  (Springer), 411
* van Altena (2013)

  van Altena, W. F. 2013, Astrometry for Astrophysics: Methods, Models, and
  Applications (Cambridge University Press)
* Winick (1986)

  Winick, K. A. 1986, J. Opt. Soc. Am. A, 3, 1809
* Zaccheo
  et al. (1995)

  Zaccheo, T., Gonsalves, R., Ebstein, S., & Nisenson, P. 1995, ApJ, 439, L43

Figure 1: Variance of the residual random variable W⁡(In,xc)W(I^{n},x\_{c})
(dimensionless) as given by equation ([22](#S3.E22 "In Remark 1 ‣ III.3 Analysis and interpretation of Theorem ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")),
as a function of the pixel resolution Δx\Delta x arcsec for
different realistic SNR scenarios (function of F~\tilde{F})
encountered in ground-based astronomical observations. Since the
admissible range for δ\delta is the interval (0,1), the small
computed values indicates that the bounded assumption in Theorem 1
can be considered as valid under these conditions.

Figure 2: Numerical computation of the critical δ\delta
(dimensionless) such that P⁡(W⁡(In,xc)∈(−δ,δ))>1−10−3P(W(I^{n},x\_{c})\in(-\delta,\delta))>1-10^{-3}. In all the scenarios (SNR, and
Δx\Delta x), 5 0005\,000 realizations of the random variable W⁡(In,xc)W(I^{n},x\_{c}) are used to estimate the probability distribution for
W⁡(In,xc)W(I^{n},x\_{c}), and δ\delta, from frequency counts. As δ\delta
decreases, we have a smaller bias (see
equations ([17](#S3.E17 "In Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) and ([20](#S3.E20 "In Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry"))) and a
narrower range for the MSE of the LS estimator
(equation ([18](#S3.E18 "In Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry"))).

Figure 3: Range of the MSE performance (in milli-arcsec2 = mas2)
for the LS method in astrometry predicted by
Theorem [1](#Thmtheorem1 "Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")
(equations ([18](#S3.E18 "In Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) and
([19](#S3.E19 "In Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry"))). Results are reported for different representative
values of F~\tilde{F} and across different pixel sizes: (From
top-left to bottom-right) F~=1 080\tilde{F}=1\,080 e-; F~=3 224\tilde{F}=3\,224 e-; F~=20 004\tilde{F}=20\,004 e-; F~=60 160\tilde{F}=60\,160 e-.

Figure 4: Relative performance differences between σLS2\sigma\_{LS}^{2} in
Theorem [1](#Thmtheorem1 "Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry") (equation ([19](#S3.E19 "In Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry"))) and
the CR bound σCR2\sigma\_{CR}^{2} in Proposition
[1](#Thmpreposition1 "Proposition 1 ‣ II.2 The Cramér-Rao bound ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")
(equation ([12](#S2.E12 "In Proposition 1 ‣ II.2 The Cramér-Rao bound ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry"))). Results are reported for different
SNR and pixel sizes. A significant performance gap between the LS
technique and the CR bound is found for FWHMFWHM/Δx<1\Delta x<1 (good
sampling of the PSF) at high SNR, indicating that, in this regime,
the LS method is sub-optimal, in agreement with
Proposition [3](#Thmpreposition3 "Proposition 3 ‣ Remark 4 ‣ III.3 Analysis and interpretation of Theorem ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry") (see also
equation ([26](#S3.E26 "In Proposition 3 ‣ Remark 4 ‣ III.3 Analysis and interpretation of Theorem ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry"))). This gap becomes
monotonically smaller as the SNR decreases.

Figure 5: Relative performance differences between the range of
performance (σLS2(n)(1+δ)2,σLS2(n)(1−δ)2)\left(\frac{\sigma\_{LS}^{2}(n)}{(1+\delta)^{2}},\frac{\sigma\_{LS}^{2}(n)}{(1-\delta)^{2}}\right) stipulated in
Theorem [1](#Thmtheorem1 "Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry") for the LS estimator
(equations ([18](#S3.E18 "In Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) and ([19](#S3.E19 "In Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")))
and the CR bound σCR2\sigma\_{CR}^{2} in
Proposition [1](#Thmpreposition1 "Proposition 1 ‣ II.2 The Cramér-Rao bound ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")
(equation ([12](#S2.E12 "In Proposition 1 ‣ II.2 The Cramér-Rao bound ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry"))). Results are reported for
different F~\tilde{F} and across different pixel sizes: (From
top-left to bottom-right) F~=1 080\tilde{F}=1\,080 e-;
F~=3 224\tilde{F}=3\,224 e-; F~=20 004\tilde{F}=20\,004 e-;
F~=60 160\tilde{F}=60\,160 e-. The 0% level corresponds to having
achieved the CR bound. Note that as the SNR decreases, the bias
(see equations ([17](#S3.E17 "In Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) and ([20](#S3.E20 "In Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")),
and the possible range for the MSE of the LS method (see
equations ([18](#S3.E18 "In Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry"))) increase (see also
Figure [2](#A3.F2 "Figure 2 ‣ Performance analysis of the Least-Squares estimator in
Astrometry")).

Figure 6: Comparison between the nominal value σLS2\sigma\_{LS}^{2}, the
performance range (σLS2(n)(1+δ)2,σLS2(n)(1−δ)2)\left(\frac{\sigma\_{LS}^{2}(n)}{(1+\delta)^{2}},\frac{\sigma\_{LS}^{2}(n)}{(1-\delta)^{2}}\right) stipulated in Theorem
[1](#Thmtheorem1 "Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry"), and the empirical estimation of
𝔼In∼fxc{(τLS(In)−xc)2}\mathbb{E}\_{I^{n}\sim f\_{x\_{c}}}\{\left(\tau\_{LS}(I^{n})-x\_{c}\right)^{2}\} from simulations for a low SNR regime of
F~=1 080\tilde{F}=1\,080 e-. The fact that the simulations follow
closely the nominal value, even at low SNR, justifies the use of
σLS\sigma\_{LS} as given by equations ([19](#S3.E19 "In Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) and
([23](#S3.E23 "In Remark 2 ‣ III.3 Analysis and interpretation of Theorem ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) as a benchmark of the LS method at any
SNR.

Figure 7: Example behavior of the likelihood function ln⁡L⁡(In,xc)\ln L(I^{n},x\_{c})
(upper row) and LS function J⁡(In,xc)J(I^{n},x\_{c}) (lower row) for two
particular realizations with low SNR= 12 (left column) and high SNR=
230 (right column), for a target centered at xc=80x\_{c}=80 arcsec (for a
pixel size of Δx=0.2\Delta x=0.2 arcsec). All the other parameters are
those described in Section [IV](#S4 "IV Numerical analysis of the LS estimator ‣ Performance analysis of the Least-Squares estimator in
Astrometry"). The figures show
(particularly the ones at low SNR) the non-linear nature of both
objective functions.

Figure 8: Comparison of the MSE\sqrt{MSE} derived from numerical
simulations using the ML (open circles, equation ([13](#S3.E13 "In III.1 Non achievability ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")))
and the LS method (open squares,
equation ([16](#S3.E16 "In III.1 Non achievability ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry"))) for a high SNR= 230 (see,
e.g., right column of Figure [7](#A3.F7 "Figure 7 ‣ Performance analysis of the Least-Squares estimator in
Astrometry")), where the optimality
loss (performance gap, ∼\sim15% in this case) of the LS method
(Proposition [3](#Thmpreposition3 "Proposition 3 ‣ Remark 4 ‣ III.3 Analysis and interpretation of Theorem ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry")) in this regime is clearly
seen. The solid line is the nominal σLS(n)\sigma\_{LS}(n) derived from
our theorem (equation ([19](#S3.E19 "In Theorem 1 ‣ III.2 Bounding the performance of the Least-Squares estimator ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry"))), while the dashed line is the
CR limit, σCR\sigma\_{CR}, given by equation ([12](#S2.E12 "In Proposition 1 ‣ II.2 The Cramér-Rao bound ‣ II Introduction and preliminaries ‣ Performance analysis of the Least-Squares estimator in
Astrometry")). As
we have shown (Section ([III.1](#S3.SS1 "III.1 Non achievability ‣ III Achievability analysis of the Cramér-Rao bound in astrometry ‣ Performance analysis of the Least-Squares estimator in
Astrometry"))), the CR limit can not
be reached in our astrometric setting, but our ML simulations (open
circles) show that they can follow very closely this limit (see also
[Mendez
et al. 2013](#bib.bib34)). A detailed analytical study of the
optimality of the ML method will be presented in a forthcoming
paper.

[◄](/html/1509.00676)
[![ar5iv homepage](/assets/ar5iv.png)](/)
[Feeling  
lucky?](/feeling_lucky)
[Conversion  
report](/log/1509.00677)
[Report  
an issue](https://github.com/dginev/ar5iv/issues/new?template=improve-article--arxiv-id-.md&title=Improve+article+1509.00677)
[View original  
on arXiv](https://arxiv.org/abs/1509.00677)[►](/html/1509.00678)

[Copyright](https://arxiv.org/help/license)
[Privacy Policy](https://arxiv.org/help/policies/privacy_policy)

Generated by [LaTeXML![Mascot Sammy](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAsAAAAOCAYAAAD5YeaVAAAAAXNSR0IArs4c6QAAAAZiS0dEAP8A/wD/oL2nkwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB9wKExQZLWTEaOUAAAAddEVYdENvbW1lbnQAQ3JlYXRlZCB3aXRoIFRoZSBHSU1Q72QlbgAAAdpJREFUKM9tkL+L2nAARz9fPZNCKFapUn8kyI0e4iRHSR1Kb8ng0lJw6FYHFwv2LwhOpcWxTjeUunYqOmqd6hEoRDhtDWdA8ApRYsSUCDHNt5ul13vz4w0vWCgUnnEc975arX6ORqN3VqtVZbfbTQC4uEHANM3jSqXymFI6yWazP2KxWAXAL9zCUa1Wy2tXVxheKA9YNoR8Pt+aTqe4FVVVvz05O6MBhqUIBGk8Hn8HAOVy+T+XLJfLS4ZhTiRJgqIoVBRFIoric47jPnmeB1mW/9rr9ZpSSn3Lsmir1fJZlqWlUonKsvwWwD8ymc/nXwVBeLjf7xEKhdBut9Hr9WgmkyGEkJwsy5eHG5vN5g0AKIoCAEgkEkin0wQAfN9/cXPdheu6P33fBwB4ngcAcByHJpPJl+fn54mD3Gg0NrquXxeLRQAAwzAYj8cwTZPwPH9/sVg8PXweDAauqqr2cDjEer1GJBLBZDJBs9mE4zjwfZ85lAGg2+06hmGgXq+j3+/DsixYlgVN03a9Xu8jgCNCyIegIAgx13Vfd7vdu+FweG8YRkjXdWy329+dTgeSJD3ieZ7RNO0VAXAPwDEAO5VKndi2fWrb9jWl9Esul6PZbDY9Go1OZ7PZ9z/lyuD3OozU2wAAAABJRU5ErkJggg==)](http://dlmf.nist.gov/LaTeXML/) oxide

## Links found on page

- http://dlmf.nist.gov/LaTeXML/
- https://ar5iv.arxiv.org/
- https://ar5iv.arxiv.org/feeling_lucky
- https://ar5iv.arxiv.org/html/1509.00676
- https://ar5iv.arxiv.org/html/1509.00678
- https://ar5iv.arxiv.org/land_of_honey_and_milk
- https://ar5iv.arxiv.org/log/1509.00677
- https://arxiv.org/abs/1509.00677
- https://arxiv.org/help/license
- https://arxiv.org/help/policies/privacy_policy
- https://github.com/dginev/ar5iv/issues/new?template=improve-article--arxiv-id-.md&title=Improve+article+1509.00677
