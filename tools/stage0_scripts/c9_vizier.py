"""Alternative Gaia DR3 source: MAST Gaia DR3 TAP (STScI) -- a different service from the ESA archive.
usage: c9_vizier.py test | c9_vizier.py EP  (EP in A,B,C -> data\\C\\gaiaM_EP.fits with the ESA column names)
(file name kept from an earlier VizieR attempt: CDS VizieR TAP timed out on connect, see s0_C.md)"""
import sys, time, os, warnings
import numpy as np, requests
from astropy.io import fits
from astropy.table import Table, vstack, unique
from astropy.wcs import WCS
warnings.filterwarnings('ignore')
D = r'stage0\data\C'
URL = 'https://mast.stsci.edu/vo-tap/api/v0.1/gaiadr3/sync'
COLS = 'source_id, ra, dec, parallax, parallax_error, pmra, pmdec, phot_g_mean_mag, ruwe, ref_epoch, astrometric_params_solved'


def tap(q, timeout=90):
    import io
    from astropy.io.votable import parse_single_table
    r = requests.post(URL, data=dict(REQUEST='doQuery', LANG='ADQL', FORMAT='votable', MAXREC='2000000', QUERY=q), timeout=timeout)
    if r.status_code != 200:
        raise RuntimeError(f'HTTP {r.status_code} {r.text[:300]}')
    if b'value="OVERFLOW"' in r.content:
        print('WARNING: OVERFLOW (truncated result)', flush=True)
    return parse_single_table(io.BytesIO(r.content)).to_table()


if sys.argv[1] == 'test':
    for q in ["SELECT TOP 3 " + COLS + " FROM dbo.gaia_source WHERE 1=CONTAINS(POINT('ICRS',ra,dec),CIRCLE('ICRS',269.452,4.693,0.05))"]:
        t0 = time.time()
        try:
            t = tap(q)
            print('OK %.1fs' % (time.time() - t0)); t.pprint_all(max_lines=40)
        except Exception as e:
            print('ERR', ascii(repr(e))[:500], flush=True)
    sys.exit()

ep = sys.argv[1]
PS = 6.2 / 3600.0
z = np.load(f'{D}\\frame_{ep}.npz')
hd = fits.Header.fromstring(open(f'{D}\\hdr_{ep}.txt').read(), sep='\n')
w = WCS(hd)
x0, y0 = int(z['x0']), int(z['y0'])
tabs = []
t_end = time.time() + 8 * 60
for qx in (256, 768):
    for qy in (256, 768):
        cf = f'{D}\\mchunk_{ep}_{qx}_{qy}.fits'
        if os.path.exists(cf):
            tabs.append(Table.read(cf)); continue
        r0, d0 = [float(v) for v in w.all_pix2world(float(x0 + qx), float(y0 + qy), 0)]
        rad = 256 * 1.4143 * PS + 0.01
        q = (f"SELECT {COLS} FROM dbo.gaia_source WHERE 1=CONTAINS(POINT('ICRS',ra,dec),CIRCLE('ICRS',{r0:.6f},{d0:.6f},{rad:.4f})) "
             f"AND phot_g_mean_mag<18")
        for attempt in range(3):
            if time.time() > t_end:
                break
            try:
                t = tap(q, 150)
                print(ep, qx, qy, 'rows', len(t), flush=True)
                t.write(cf, overwrite=True); tabs.append(t); break
            except Exception as e:
                print(ep, qx, qy, 'attempt', attempt, 'ERR', ascii(repr(e))[:200], flush=True)
                time.sleep(5)
        else:
            print(ep, qx, qy, 'GAVE UP', flush=True)
if tabs:
    t = unique(vstack(tabs), keys='source_id')
    print(ep, 'dedup rows', len(t), 'tiles', len(tabs), flush=True)
    t.write(f'{D}\\gaiaM_{ep}.fits', overwrite=True)
