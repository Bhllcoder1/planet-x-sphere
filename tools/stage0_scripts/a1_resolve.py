import sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
from astropy.coordinates import SkyCoord
import astropy.units as u
from astroquery.gaia import Gaia
for n in ["Barnard's Star","eps Indi","RW Aur","R Dra"]:
    c=SkyCoord.from_name(n)
    print(n,repr(c.ra.deg),repr(c.dec.deg))
    q=f"SELECT TOP 4 source_id,ra,dec,pmra,pmdec,parallax,phot_g_mean_mag,ref_epoch FROM gaiadr3.gaia_source WHERE 1=CONTAINS(POINT('ICRS',ra,dec),CIRCLE('ICRS',{c.ra.deg},{c.dec.deg},0.05)) ORDER BY phot_g_mean_mag"
    try:
        t=Gaia.launch_job(q).get_results(); print(t)
    except Exception as e: print("GAIA FAIL",type(e).__name__,str(e)[:200])
