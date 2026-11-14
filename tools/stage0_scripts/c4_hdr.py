import sys, warnings
from astropy.io import fits
from astropy.wcs import WCS
import numpy as np
warnings.filterwarnings('ignore')
BASE = 's3://nasa-irsa-spherex/dr1/level2/'
def url(rel):
    return BASE + rel
rel = sys.argv[1]
ra, dec = 269.452, 4.693
with fits.open(url(rel), fsspec_kwargs={'anon': True}, lazy_load_hdus=True) as h:
    h.info()
    hd = h['IMAGE'].header
    for k in ['NAXIS1', 'NAXIS2', 'RADESYS', 'EQUINOX', 'CTYPE1', 'CTYPE2', 'CRVAL1', 'CRVAL2', 'CRPIX1', 'CRPIX2', 'A_ORDER', 'MJD-AVG', 'MJD-BEG', 'MJD-END', 'DATE-OBS', 'DETECTOR', 'OBSID', 'WCSAXES', 'WCSNAME', 'WCSVERS', 'VERSION', 'PROCVER', 'ASTRRMS1', 'ASTRRMS2', 'ASTRNSRC', 'ASTRNSTR', 'ASTRSIG1', 'ASTRSIG2', 'CD1_1', 'CD1_2', 'CD2_1', 'CD2_2', 'NEXPREF', 'CRDER1', 'CRDER2']:
        print(k, hd.get(k))
    print(repr(hd)[:6000])
    w = WCS(hd)
    print('pix of Barnard (0-based):', w.all_world2pix(ra, dec, 0, tolerance=1e-8, maxiter=50))
