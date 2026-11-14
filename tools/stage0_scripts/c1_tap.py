import requests, sys, io, time
from astropy.table import Table
URL = "https://irsa.ipac.caltech.edu/TAP/sync"
OUT = r'stage0\data\C'

def tap(q, timeout=90):
    t0 = time.time()
    r = requests.post(URL, data=dict(REQUEST='doQuery', LANG='ADQL', FORMAT='csv', QUERY=q), timeout=timeout)
    print("HTTP", r.status_code, "%.1fs" % (time.time()-t0), flush=True)
    r.raise_for_status()
    return Table.read(r.text.splitlines(), format='ascii.csv')

mode = sys.argv[1]
if mode == 'schema':
    t = tap("select table_name,column_name from TAP_SCHEMA.columns where table_name in ('spherex.artifact','spherex.plane')")
    t.pprint_all()
elif mode == 'q':
    ra, dec = float(sys.argv[2]), float(sys.argv[3])
    q = f"""select top 800 a.uri, a.producttype, a.releasetype, p.datarelease, p.dataproducttype, p.calibrationlevel, p.time_bounds_lower as mjd, p.energy_bounds_lower as wlo, p.energy_bounds_upper as whi, p.provenance_version as pver
from spherex.artifact a join spherex.plane p on a.planeid=p.planeid
where CONTAINS(POINT('ICRS',{ra},{dec}),p.poly)=1 order by p.time_bounds_lower"""
    t = tap(q, 150)
    print(len(t)); t.write(OUT + r'\tap_raw.csv', format='ascii.csv', overwrite=True)
    print(t[:5])
