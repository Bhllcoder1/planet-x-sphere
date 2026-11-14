"""Offline 03-07 science checks; run with python -I -m unittest discover."""
import importlib.util
from pathlib import Path
import unittest

import numpy as np
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.table import Table, MaskedColumn
from astropy.time import Time

spec = importlib.util.spec_from_file_location("gaia_epoch", Path(__file__).with_name("epoch.py"))
epoch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(epoch)


def catalogue():
    return Table({"source_id": [1, 2], "ra": [269.452, 20.0], "dec": [4.693, 60.0],
                  "pmra": [-800., 100.], "pmdec": [10300., -20.],
                  "parallax": [548., 10.], "ref_epoch": [2016., 2015.5]})


class EpochTests(unittest.TestCase):
    def test_space_motion_matches_astropy_at_task_tolerance(self):
        cat = catalogue()
        expected = SkyCoord(ra=cat["ra"] * u.deg, dec=cat["dec"] * u.deg,
                            distance=1000 / cat["parallax"] * u.pc,
                            pm_ra_cosdec=cat["pmra"] * u.mas / u.yr,
                            pm_dec=cat["pmdec"] * u.mas / u.yr,
                            radial_velocity=[-110., 20.] * u.km / u.s,
                            obstime=Time(cat["ref_epoch"], format="jyear", scale="tcb"))
        expected = expected.apply_space_motion(new_obstime=Time(61000., format="mjd", scale="utc"))
        actual = epoch.space_motion(*(cat[c] for c in ("ra", "dec", "pmra", "pmdec", "parallax", "ref_epoch")),
                                    61000., radial_velocity_kms=[-110., 20.])
        self.assertLess(np.max(actual.separation(expected).deg), 1e-9)

    def test_pmra_is_cosine_weighted(self):
        start = Time(2016., format="jyear", scale="tcb")
        target = start + 1 * u.yr
        actual = epoch.space_motion(20., 60., 100., 0., 1., 2016., target.utc.mjd,
                                    radial_velocity_kms=0.)
        self.assertAlmostEqual((actual.ra.deg - 20.) * 3_600_000 * 0.5, 100., places=5)

    def test_parallax_sign_and_six_month_opposition(self):
        # alpha=90deg, delta=0: observer +/-X gives +/- parallax in RA*, no Dec shift.
        plus = epoch.parallax_offsets(90., 0., 500., [1., 0., 0.])
        minus = epoch.parallax_offsets(90., 0., 500., [-1., 0., 0.])
        np.testing.assert_allclose(plus, [500., 0.], atol=1e-9)
        np.testing.assert_allclose(minus, [-500., 0.], atol=1e-9)
        np.testing.assert_allclose(epoch.parallax_offsets(0., 0., 500., [0., 0., 1.]),
                                   [0., -500.], atol=1e-9)

    def test_parallax_matches_independent_tangent_vector(self):
        ra, dec, plx, observer = 123.4, -35.6, 548., np.array([0.3, -0.8, 0.2])
        a, d = np.deg2rad([ra, dec])
        # The observer displacement projects as -r onto east/north sky basis.
        east = np.array([-np.sin(a), np.cos(a), 0.])
        north = np.array([-np.cos(a) * np.sin(d), -np.sin(a) * np.sin(d), np.cos(d)])
        expected = -plx * np.array([observer @ east, observer @ north])
        actual = np.asarray(epoch.parallax_offsets(ra, dec, plx, observer))
        self.assertLess(np.max(np.abs(actual - expected)) / 1000., 1e-6)

    def test_parallax_against_observer_displacement_geometry(self):
        cat = catalogue()[1:]
        cat["pmra"] = [0.]
        cat["pmdec"] = [0.]
        cat["parallax"] = [100.]
        observer = np.array([0.3, -0.8, 0.2])
        result = epoch.propagate_catalogue(cat, 61000., radial_velocity_kms=0., observer_au=observer)
        source = SkyCoord(ra=cat["ra"] * u.deg, dec=cat["dec"] * u.deg,
                          distance=10. * u.pc)
        vector = source.cartesian.xyz.to_value(u.au)[:, 0] - observer
        expected = SkyCoord(x=vector[0] * u.au, y=vector[1] * u.au,
                            z=vector[2] * u.au, representation_type="cartesian").spherical
        actual = SkyCoord(result["ra_deg"] * u.deg, result["dec_deg"] * u.deg)
        geometric = SkyCoord(expected.lon, expected.lat)
        self.assertLess(actual.separation(geometric).arcsec[0], 1e-6)

    def test_geometric_parallax_at_and_across_both_poles(self):
        for dec in (89.999, 90., -89.999, -90.):
            for ra in (0., 123.4, 359.99999):
                with self.subTest(ra=ra, dec=dec):
                    cat = catalogue()[:1]
                    cat["ra"], cat["dec"] = [ra], [dec]
                    cat["pmra"], cat["pmdec"] = [0.], [0.]
                    cat["parallax"] = [548.]
                    observer = np.array([1., 0.5, 0.2])
                    result = epoch.propagate_catalogue(cat, 61000., radial_velocity_kms=0., observer_au=observer)
                    # Independent finite-distance Cartesian observer subtraction in AU.
                    source = SkyCoord(ra=ra * u.deg, dec=dec * u.deg,
                                      distance=(1000 / 548.) * u.pc)
                    xyz = source.cartesian.xyz.to_value(u.au) - observer
                    expected = SkyCoord(x=xyz[0] * u.au, y=xyz[1] * u.au,
                                        z=xyz[2] * u.au, representation_type="cartesian").spherical
                    actual = SkyCoord(result["ra_deg"] * u.deg, result["dec_deg"] * u.deg)
                    self.assertLess(actual.separation(SkyCoord(expected.lon, expected.lat)).arcsec[0], 1e-6)
                    self.assertTrue(0 <= result["ra_deg"][0] < 360)

    def test_ra_wrap(self):
        cat = catalogue()[:1]
        cat["ra"] = [359.99999]
        cat["dec"] = [0.]
        cat["pmra"] = [1000.]
        cat["pmdec"] = [0.]
        result = epoch.propagate_catalogue(cat, 61000., radial_velocity_kms=0., observer_au=[0., 0., 0.])
        self.assertGreater(result["ra_deg"][0], 0.)
        self.assertLess(result["ra_deg"][0], 0.01)

    def test_no_observer_parallax_at_barycentre_and_no_mutation(self):
        cat = catalogue()
        before = cat.copy()
        result = epoch.propagate_catalogue(cat, 61000., radial_velocity_kms=0., observer_au=[0., 0., 0.])
        np.testing.assert_allclose(result["ra_deg"], result["ra_bary_deg"], atol=1e-12, rtol=0)
        np.testing.assert_allclose(result["dec_deg"], result["dec_bary_deg"], atol=1e-12, rtol=0)
        self.assertTrue(all(np.all(cat[c] == before[c]) for c in cat.colnames))
        self.assertEqual(result.meta["uncertainty"], "not propagated; no sigma claimed")

    def test_distance_floor_does_not_replace_signed_observer_parallax(self):
        cat = catalogue()[:1]
        cat["parallax"] = [-0.2]
        result = epoch.propagate_catalogue(cat, 61000., radial_velocity_kms=0., observer_au=[1., 0., 0.])
        self.assertEqual(result["distance_parallax_mas"][0], 0.05)
        expected = epoch.parallax_offsets(result["ra_bary_deg"], result["dec_bary_deg"], [-0.2], [1., 0., 0.])
        np.testing.assert_allclose(result["parallax_dra_cosdec_mas"], expected[0])

    def test_missing_astrometry_and_bad_units_boundary(self):
        for column in ("pmra", "pmdec", "parallax", "ref_epoch"):
            cat = catalogue()
            cat[column][0] = np.nan
            with self.subTest(column=column), self.assertRaises(ValueError):
                epoch.propagate_catalogue(cat, 61000., radial_velocity_kms=0.)
        cat = catalogue()
        cat.replace_column("pmra", MaskedColumn(cat["pmra"], mask=[True, False]))
        with self.assertRaises(ValueError):
            epoch.propagate_catalogue(cat, 61000., radial_velocity_kms=0.)
        with self.assertRaises(TypeError):
            epoch.propagate_catalogue(catalogue(), 61000.)
        with self.assertRaises(ValueError):
            epoch.parallax_offsets(0., 91., 1., [1., 0., 0.])
        with self.assertRaises(ValueError):
            epoch.parallax_offsets(0., 0., 1., [np.nan, 0., 0.])

    def test_builtin_earth_observer_is_finite_offline(self):
        result = epoch.propagate_catalogue(catalogue(), 61000., radial_velocity_kms=0.)
        self.assertTrue(np.all(np.isfinite(result["ra_deg"])))
        self.assertIn("builtin", result.meta["observer"])
        self.assertGreater(np.max(np.abs(result["parallax_dra_cosdec_mas"])), 1.)


if __name__ == "__main__":
    unittest.main()
