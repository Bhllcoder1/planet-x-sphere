import numpy as np
D = r'stage0\data\C'
for ep in 'ABC':
    z = np.load(f'{D}\\frame_{ep}.npz'); img = z['img']; var = z['var']; flg = z['flg']
    bad = ((flg & 0x3C028E44) != 0) | ~np.isfinite(img) | ~np.isfinite(var) | (var <= 0)
    print(ep, 'finite img', np.isfinite(img).mean(), 'finite var', np.isfinite(var).mean(), 'var>0', (var > 0).mean(), 'fitmask', ((flg & 0x3C028E44) != 0).mean(), 'bad total', bad.mean(), 'median var', np.nanmedian(var))
    for b in range(32):
        f = ((flg >> b) & 1).mean()
        if f > 0.05:
            print('   bit', b, round(float(f), 3))
