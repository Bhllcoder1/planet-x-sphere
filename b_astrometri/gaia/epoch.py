"""03-07 prototype: barycentric space motion, then geometric observer parallax.

Gaia pmra is mu_alpha*cos(dec), in mas/year. Positions are ICRS degrees,
parallax is mas, catalogue epochs are Julian years (TCB), frame MJD is UTC.
This module consumes already selected sources; it does not query, match or
correct WCS. Radial velocity must be supplied explicitly, including an assumed 0.
"""
import numpy as np
import astropy.units as u
from astropy.coordinates import SkyCoord, get_body_barycentric
from astropy.table import Table
from astropy.time import Time


def _finite(*values):
    arrays = [np.asarray(value, dtype=float) for value in values]
    if any(np.any(np.ma.getmaskarray(value)) for value in values):
        raise ValueError("Masked astrometric inputs cannot be propagated")
    if any(not np.all(np.isfinite(value)) for value in arrays):
        raise ValueError("Astrometric inputs must be finite")
    return np.broadcast_arrays(*arrays)


def _sky(ra_deg, dec_deg):
    ra, dec = _finite(ra_deg, dec_deg)
    if np.any((ra < 0) | (ra >= 360)) or np.any(np.abs(dec) > 90):
        raise ValueError("Require 0 <= RA < 360 and -90 <= Dec <= 90 degrees")
    return ra, dec


def space_motion(ra_deg, dec_deg, pmra_masyr, pmdec_masyr, parallax_mas,
                 ref_epoch, mjd_utc, *, radial_velocity_kms):
    """Return barycentric SkyCoord at frame time, without observer parallax.

    The legacy Stage 0 distance floor is retained and explicit: parallaxes below
    0.05 mas use 0.05 mas for distance only. Unknown astrometry is rejected.
    Reference: https://docs.astropy.org/en/stable/coordinates/apply_space_motion.html
    """
    ra, dec = _sky(ra_deg, dec_deg)
    ra, dec, pmra, pmdec, parallax, epoch, rv = _finite(
        ra, dec, pmra_masyr, pmdec_masyr, parallax_mas, ref_epoch,
        radial_velocity_kms)
    _finite(mjd_utc)
    source = SkyCoord(ra=ra * u.deg, dec=dec * u.deg,
                      pm_ra_cosdec=pmra * u.mas / u.yr,
                      pm_dec=pmdec * u.mas / u.yr,
                      distance=(1000 / np.maximum(parallax, 0.05)) * u.pc,
                      radial_velocity=rv * u.km / u.s,
                      obstime=Time(epoch, format="jyear", scale="tcb"), frame="icrs")
    return source.apply_space_motion(new_obstime=Time(mjd_utc, format="mjd", scale="utc"))


def parallax_offsets(ra_deg, dec_deg, parallax_mas, observer_au):
    """Return (delta_RA*cos(dec), delta_Dec) in mas; observer is ICRS XYZ AU.

    This is the first-order tangent-plane term, not aberration or a GCRS
    transform. Apply it exactly once to barycentric propagated positions.
    """
    ra, dec = _sky(ra_deg, dec_deg)
    ra, dec, parallax = _finite(ra, dec, parallax_mas)
    xyz = np.asarray(observer_au, dtype=float)
    if xyz.shape != (3,) or not np.all(np.isfinite(xyz)):
        raise ValueError("observer_au must be one finite ICRS XYZ vector in AU")
    alpha, delta = np.deg2rad(ra), np.deg2rad(dec)
    x, y, z = xyz
    dra_cosdec = parallax * (x * np.sin(alpha) - y * np.cos(alpha))
    ddec = parallax * (x * np.cos(alpha) * np.sin(delta)
                       + y * np.sin(alpha) * np.sin(delta) - z * np.cos(delta))
    return dra_cosdec, ddec


def propagate_catalogue(catalogue, mjd_utc, *, radial_velocity_kms, observer_au=None):
    """Return a new source table, with barycentric and observer-shifted positions.

    By default the observer is Earth's centre, using Astropy's offline builtin
    ephemeris. Supply an explicit barycentric observer vector for a spacecraft.
    Negative finite parallaxes retain their signed observer displacement, as in
    the Stage 0 convention; the distance floor does not change that measured value.
    Unknown/masked inputs fail instead of becoming plausible zero-motion stars.
    """
    required = ("source_id", "ra", "dec", "pmra", "pmdec", "parallax", "ref_epoch")
    missing = set(required) - set(catalogue.colnames)
    if missing:
        raise ValueError(f"Missing Gaia columns: {sorted(missing)}")
    if not np.isscalar(mjd_utc) or not np.isfinite(mjd_utc):
        raise ValueError("One finite frame MJD is required")
    if np.any(np.ma.getmaskarray(catalogue["source_id"])):
        raise ValueError("Masked source_id cannot be propagated")
    moved = space_motion(*(catalogue[c] for c in required[1:]), mjd_utc,
                         radial_velocity_kms=radial_velocity_kms)
    if observer_au is None:
        time = Time(mjd_utc, format="mjd", scale="utc")
        observer_au = get_body_barycentric("earth", time, ephemeris="builtin").xyz.to_value(u.au)
        observer = "Earth barycentre position; builtin ephemeris"
    else:
        observer = "caller-supplied barycentric ICRS XYZ AU"
    ra, dec = moved.ra.deg, moved.dec.deg
    dra, ddec = parallax_offsets(ra, dec, catalogue["parallax"], observer_au)
    alpha, delta = np.deg2rad(ra), np.deg2rad(dec)
    direction = np.stack((np.cos(delta) * np.cos(alpha),
                          np.cos(delta) * np.sin(alpha), np.sin(delta)), axis=-1)
    # Cartesian observer subtraction stays well-conditioned at/crossing both poles.
    inverse_distance_au = np.deg2rad(np.asarray(catalogue["parallax"]) / 3_600_000)
    shifted = direction - inverse_distance_au[:, None] * np.asarray(observer_au)
    norm = np.linalg.norm(shifted, axis=-1)
    if np.any(~np.isfinite(norm) | (norm == 0)):
        raise ValueError("Observer displacement gives an undefined source direction")
    shifted /= norm[:, None]
    shifted_ra = np.rad2deg(np.arctan2(shifted[:, 1], shifted[:, 0])) % 360
    shifted_dec = np.rad2deg(np.arctan2(shifted[:, 2], np.hypot(shifted[:, 0], shifted[:, 1])))
    result = Table({"source_id": catalogue["source_id"],
                    "ra_bary_deg": ra, "dec_bary_deg": dec,
                    "ra_deg": shifted_ra,
                    "dec_deg": shifted_dec,
                    "parallax_dra_cosdec_mas": dra, "parallax_ddec_mas": ddec,
                    "distance_parallax_mas": np.maximum(catalogue["parallax"], 0.05),
                    "radial_velocity_kms": np.broadcast_to(radial_velocity_kms, ra.shape)})
    result.meta = {"mjd_utc": float(mjd_utc), "observer": observer,
                   "observer_au": np.asarray(observer_au).tolist(),
                   "parallax_model": "geometric observer displacement; tangent offsets first-order",
                   "uncertainty": "not propagated; no sigma claimed",
                   "distance_floor_mas": 0.05}
    return result
