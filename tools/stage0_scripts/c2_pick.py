from astropy.table import Table
import numpy as np
t = Table.read(r'stage0\data\C\tap_raw.csv', format='ascii.csv')
print(t.colnames)
for c in ['producttype', 'releasetype', 'datarelease', 'dataproducttype', 'calibrationlevel', 'pver']:
    print(c, set(map(str, t[c])))
t = t[np.array([str(u).endswith('.fits') for u in t['uri']])]
t['mjd'] = t['mjd'].astype(float)
print(len(t), t['mjd'].min(), t['mjd'].max())
# group by ~week of mjd
for r in t:
    pass
import collections
d = collections.OrderedDict()
for r in t:
    d.setdefault(int(r['mjd'] // 10) * 10, []).append(r)
for k, v in d.items():
    print(k, len(v), v[0]['uri'][-70:], v[0]['mjd'], v[0]['wlo'])
