from astroquery.gaia import Gaia
base = "FROM gaiadr3.gaia_source WHERE 1=CONTAINS(POINT('ICRS',ra,dec), CIRCLE('ICRS',269.453,4.554,1.3)) AND phot_g_mean_mag<18"
for q in ["SELECT COUNT(*) AS n " + base,
          "SELECT TOP 5 source_id, ra, dec, parallax, parallax_error, pmra, pmdec, phot_g_mean_mag, ruwe, ref_epoch, astrometric_params_solved " + base]:
    try:
        j = Gaia.launch_job(q)
        print('OK', j.get_results(), flush=True)
    except Exception as e:
        print('ERR', repr(e)[:300], flush=True)
