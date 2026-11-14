import numpy as np
from astropy.table import Table, join
D = r'stage0\data\C'
e = Table.read(D + r'\gaia_A.fits'); m = Table.read(D + r'\gaiaM_A.fits')
for t in (e, m):
    for cn in t.colnames:
        if hasattr(t[cn], 'filled') and t[cn].dtype.kind == 'f':
            t[cn] = t[cn].filled(np.nan)
print('ESA rows', len(e), 'MAST rows', len(m))
j = join(e, m, keys='source_id', table_names=['e', 'm'])
print('common ids', len(j))
idE = set(e['source_id']); idM = set(m['source_id'])
# restrict to stars in the region both queries cover: ids only in one
print('only ESA', len(idE - idM), 'only MAST', len(idM - idE))
for c in ['ra', 'dec', 'parallax', 'pmra', 'pmdec', 'phot_g_mean_mag', 'ruwe', 'ref_epoch', 'astrometric_params_solved']:
    a = np.array(j[c + '_e'], float); b = np.array(j[c + '_m'], float)
    ok = np.isfinite(a) & np.isfinite(b)
    d = (a - b)[ok]
    print(c, 'max|diff|', np.max(np.abs(d)) if len(d) else None, 'n_nan_mismatch', int((np.isfinite(a) != np.isfinite(b)).sum()))
print('ESA ref_epoch', set(e['ref_epoch'])); print('MAST ref_epoch', set(m['ref_epoch']))
# brightness of the only-in-one sets
for name, ids, t in (('only ESA', idE - idM, e), ('only MAST', idM - idE, m)):
    s = np.isin(t['source_id'], list(ids))
    print(name, 'G range', np.nanmin(t['phot_g_mean_mag'][s]) if s.any() else None, 'n G<17:', int((t['phot_g_mean_mag'][s] < 17).sum()))
