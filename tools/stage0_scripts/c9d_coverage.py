import numpy as np
from astropy.io import fits
from astropy.table import Table
from astropy.wcs import WCS
D = r'stage0\data\C'
z = np.load(D + r'\frame_A.npz'); x0, y0 = int(z['x0']), int(z['y0'])
w = WCS(fits.Header.fromstring(open(D + r'\hdr_A.txt').read(), sep='\n'))
e = Table.read(D + r'\gaia_A.fits'); m = Table.read(D + r'\gaiaM_A.fits')
ide, idm = set(map(int, e['source_id'])), set(map(int, m['source_id']))
for name, t, other in (('ESA only', e, idm), ('MAST only', m, ide)):
    s = np.array([int(i) not in other for i in t['source_id']])
    ra = np.array(t['ra'], float)[s]; dec = np.array(t['dec'], float)[s]
    x, y = w.all_world2pix(ra, dec, 0)
    inw = (x > x0 + 8) & (x < x0 + 1016) & (y > y0 + 8) & (y < y0 + 1016)
    g = np.array(t['phot_g_mean_mag'], float)[s]
    print(name, 'n', s.sum(), 'inside window', int(inw.sum()), 'inside window with G<17', int((inw & (g < 17)).sum()))
