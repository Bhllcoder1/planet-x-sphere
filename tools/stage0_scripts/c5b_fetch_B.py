"""Fetch 1024x1024 windows (IMAGE, VARIANCE, FLAGS) + full IMAGE header from SPHEREx DR1 L2 frames on anonymous S3."""
import warnings, json
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
warnings.filterwarnings('ignore')
BASE = 's3://nasa-irsa-spherex/dr1/level2/'
OUT = r'stage0\data\C'
ra, dec = 269.452, 4.693
EPOCHS = {
    'A': ['2025W35_2A/l2b-v27-2026-231/1/level2_2025W35_2A_0233_1D1_spx_l2b-v27-2026-231.fits'],
    'B': ['2025W40_1A/l2b-v27-2026-239/1/level2_2025W40_1A_0353_1D1_spx_l2b-v27-2026-239.fits'],
    'C': ['2026W11_1A/l2b-v27-2026-232/1/level2_2026W11_1A_0444_1D1_spx_l2b-v27-2026-232.fits',
          '2026W11_1A/l2b-v27-2026-232/1/level2_2026W11_1A_0430_2D1_spx_l2b-v27-2026-232.fits',
          '2026W11_1A/l2b-v27-2026-232/1/level2_2026W11_1A_0511_1D1_spx_l2b-v27-2026-232.fits'],
}
W = 1024
for ep, cands in [('B', EPOCHS['B'])]:
    for rel in cands:
        with fits.open(BASE + rel, fsspec_kwargs={'anon': True}, lazy_load_hdus=True) as h:
            hd = h['IMAGE'].header
            w = WCS(hd)
            x, y = [float(v) for v in w.all_world2pix(ra, dec, 0, tolerance=1e-8, maxiter=50)]
            print(ep, rel[-45:], 'Barnard pix', round(x, 1), round(y, 1), flush=True)
            if not (0 < x < 2040 and 0 < y < 2040):
                continue
            x0 = int(min(max(x - W // 2, 0), 2040 - W)); y0 = int(min(max(y - W // 2, 0), 2040 - W))
            img = h['IMAGE'].section[y0:y0 + W, x0:x0 + W]
            var = h['VARIANCE'].section[y0:y0 + W, x0:x0 + W]
            flg = h['FLAGS'].section[y0:y0 + W, x0:x0 + W]
            np.savez(f'{OUT}\\frame_{ep}.npz', img=np.asarray(img, dtype='f4'), var=np.asarray(var, dtype='f4'),
                     flg=np.asarray(flg, dtype='i4'), x0=x0, y0=y0, rel=rel)
            open(f'{OUT}\\hdr_{ep}.txt', 'w').write(hd.tostring(sep='\n'))
            open(f'{OUT}\\hdrflags_{ep}.txt', 'w').write(h['FLAGS'].header.tostring(sep='\n'))
            print(ep, 'saved window x0,y0', x0, y0, img.shape, flush=True)
            break
