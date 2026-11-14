import sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
from astroquery.gaia import Gaia
q="SELECT source_id,ra,dec,pmra,pmdec,parallax,phot_g_mean_mag FROM gaiadr3.gaia_source WHERE 1=CONTAINS(POINT('ICRS',ra,dec),CIRCLE('ICRS',330.8724,-56.7860,0.2)) AND pmra>3000 ORDER BY phot_g_mean_mag"
t=Gaia.launch_job(q).get_results(); t.pprint_all()
q="SELECT source_id,ra,dec,pmra,pmdec,parallax,phot_g_mean_mag FROM gaiadr3.gaia_source WHERE source_id IN (4472832130942575872,6412595290592307840)"
Gaia.launch_job(q).get_results().pprint_all()
