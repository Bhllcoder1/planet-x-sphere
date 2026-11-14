"""Gaia DR3 cone queries (ESA TAP, async) tiling each frame window; G<18; adaptive splitting on server failure; deduplicated."""
import warnings, time, os, numpy as np
from astropy.io import fits
from astropy.table import Table, vstack, unique
from astropy.wcs import WCS
from astroquery.gaia import Gaia
warnings.filterwarnings('ignore')
D = r'stage0\data\C'
Gaia.ROW_LIMIT = -1
MAG = 18
PS = 6.2 / 3600.0


def fetch(ep, w, x0, y0, qx, qy, half):
    cf = f'{D}\\gchunk_{ep}_{qx}_{qy}_{half}.fits'
    old = f'{D}\\gchunk_{ep}_{qx}_{qy}.fits'
    if half == 256 and os.path.exists(old):
        return [Table.read(old)]
    if os.path.exists(cf):
        return [Table.read(cf)]
    r0, d0 = [float(v) for v in w.all_pix2world(float(x0 + qx), float(y0 + qy), 0)]
    rad = half * 1.4143 * PS + 0.01
    q = (f"SELECT source_id, ra, dec, parallax, parallax_error, pmra, pmdec, phot_g_mean_mag, ruwe, ref_epoch, astrometric_params_solved "
         f"FROM gaiadr3.gaia_source WHERE 1=CONTAINS(POINT('ICRS',ra,dec), CIRCLE('ICRS',{r0:.6f},{d0:.6f},{rad:.4f})) AND phot_g_mean_mag<{MAG}")
    for attempt in range(3):
        try:
            t = Gaia.launch_job_async(q, dump_to_file=False).get_results()
            print(ep, qx, qy, half, 'rows', len(t), flush=True)
            t.write(cf, overwrite=True)
            return [t]
        except Exception as e:
            print(ep, qx, qy, half, 'attempt', attempt, 'ERR', ascii(repr(e))[:120], flush=True)
            time.sleep(8)
    if half <= 64 or time.time() > DEADLINE:
        print(ep, qx, qy, half, 'GAVE UP (chunk missing)', flush=True)
        return []
    out = []
    h2 = half // 2
    for dx in (-h2, h2):
        for dy in (-h2, h2):
            out += fetch(ep, w, x0, y0, qx + dx, qy + dy, h2)
    return out


import sys
for ep in (sys.argv[1] if len(sys.argv) > 1 else 'ABC'):
    DEADLINE = time.time() + 8 * 60
    z = np.load(f'{D}\\frame_{ep}.npz')
    hd = fits.Header.fromstring(open(f'{D}\\hdr_{ep}.txt').read(), sep='\n')
    w = WCS(hd)
    tabs = []
    for qx in (256, 768):
        for qy in (256, 768):
            tabs += fetch(ep, w, int(z['x0']), int(z['y0']), qx, qy, 256)
    t = unique(vstack(tabs), keys='source_id')
    print(ep, 'N Gaia rows (dedup)', len(t), flush=True)
    t.write(f'{D}\\gaia_{ep}.fits', overwrite=True)
