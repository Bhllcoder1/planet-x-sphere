import json, glob, numpy as np
D = r'stage0\data\C'
R = {}
for f in sorted(glob.glob(D + r'\results_*_mast.json')):
    R.update(json.load(open(f)))
AM = R.pop('A', None) if False else None
RA_M = json.load(open(D + r'\results_A_mast.json'))['A']
for f in sorted(glob.glob(D + r'\results_?.json')):
    R.update(json.load(open(f)))      # ESA-based results (frame A) override MAST ones
print('Gaia source per frame:', {e: R[e].get('gaia_source') for e in R})
print('A with MAST Gaia: median dx,dy', RA_M['median_dx_px'], RA_M['median_dy_px'], 'N', RA_M['n_match_2px'], 'sigma', RA_M['robust_sigma_dx_px'], RA_M['robust_sigma_dy_px'])
L = []
def p(s=''):
    L.append(s)
eps = sorted(R)
p('| frame | obsid | UTC (MJD-AVG) | N Gaia sel / in window | N detections (centroided) | N matched (<=2 px) |')
p('|---|---|---|---|---|---|')
for e in eps:
    r = R[e]
    p(f"| {e} | {r['obsid']} | {r['date']} ({r['mjd']:.4f}) | {r['n_gaia_sel']} / {r['n_gaia_inwin']} | {r['n_centroided']} | {r['n_match_2px']} (raw, no shift: {r['n_match_raw_2px_noshift']}) |")
p()
p('Measured offset (centroid minus Gaia projected through header WCS; median over matched stars), px = detector pixels, 6.15 arcsec/px')
p()
p('| frame | median dx px | median dy px | dx arcsec | dy arcsec | dRA*cos(dec) arcsec | dDec arcsec | robust sigma dx, dy (px) | s.e.m. dx, dy (px) | |offset| arcsec |')
p('|---|---|---|---|---|---|---|---|---|---|')
for e in eps:
    r = R[e]
    mag = np.hypot(r['median_dRAcosd_arcsec'], r['median_dDec_arcsec'])
    p(f"| {e} | {r['median_dx_px']:+.4f} | {r['median_dy_px']:+.4f} | {r['median_dx_arcsec']:+.3f} | {r['median_dy_arcsec']:+.3f} | {r['median_dRAcosd_arcsec']:+.3f} | {r['median_dDec_arcsec']:+.3f} | {r['robust_sigma_dx_px']:.3f}, {r['robust_sigma_dy_px']:.3f} | {r['sem_dx_px']:.4f}, {r['sem_dy_px']:.4f} | {mag:.3f} |")
p()
p('Fits to the offset field (3 sigma clipped, positions centred on window centre; scale = dimensionless px/px; rot = radians, x->y)')
p()
p('| frame | model | tx px | ty px | scale | rot rad | per-axis RMS px (arcsec) | kept/N | held-out robust per-axis px |')
p('|---|---|---|---|---|---|---|---|---|')
for e in eps:
    f = R[e]['fits']
    for k in ('shift', 'sim', 'affine'):
        q = f[k]['params']
        if k == 'shift':
            sc, rt = '-', '-'
        elif k == 'sim':
            sc, rt = f'{q[2]:+.2e}', f'{q[3]:+.2e}'
        else:
            sc, rt = f'(a={q[2]:+.1e}, b={q[3]:+.1e}, c={q[4]:+.1e}, d={q[5]:+.1e})', '-'
        p(f"| {e} | {k} | {q[0]:+.4f} | {q[1]:+.4f} | {sc} | {rt} | {f[k]['rms_peraxis_px']:.4f} ({f[k]['rms_peraxis_arcsec']:.3f}) | {f[k]['n_kept']}/{f[k]['n']} | {f['heldout_robust_peraxis_px'][k]:.4f} |")
p()
p('Position dependence: 3x3 grid of medians (dx, dy in px; n), grid row = y (bottom to top), col = x')
p()
for e in eps:
    p(f'Frame {e}:')
    p()
    p('| row\\col | x low | x mid | x high |')
    p('|---|---|---|---|')
    g = {(c['yrow'], c['xcol']): c for c in R[e]['grid3x3']}
    for row in range(3):
        cells = []
        for col in range(3):
            c = g.get((row, col))
            cells.append('-' if c is None else f"{c['mdx']:+.3f}, {c['mdy']:+.3f} (n={c['n']})")
        p(f'| y{row} | ' + ' | '.join(cells) + ' |')
    p()
p('Scatter versus Gaia G (robust per-axis sigma of the offsets about the median)')
p()
p('| frame | G 11-14 | G 14-15.5 | G 15.5-17 |')
p('|---|---|---|---|')
for e in eps:
    m = np.load(f'{D}\\matched_{e}.npz')
    cells = []
    for lo, hi in ((11, 14), (14, 15.5), (15.5, 17.01)):
        s = (m['gmag'] >= lo) & (m['gmag'] < hi)
        if s.sum() > 8:
            a = m['odx'][s]; b = m['ody'][s]
            sg = 0.5 * (1.4826 * np.median(abs(a - np.median(a))) + 1.4826 * np.median(abs(b - np.median(b))))
            cells.append(f'{sg:.3f} px (n={s.sum()}), median offset ({np.median(a):+.3f},{np.median(b):+.3f})')
        else:
            cells.append(f'n={s.sum()}')
    p(f'| {e} | ' + ' | '.join(cells) + ' |')
p()
p('Aberration prediction (first order, n\' = n + (v - n(n.v))/c, v/c exact from vectors; computed per matched star, projected through the header WCS) versus measured')
p()
p('| frame | Earth speed km/s | angle star-apex deg | expected |v|/c sin(theta) arcsec | predicted (Earth only): dRA*, dDec arcsec, mag | predicted (Earth + header spacecraft velocity): dRA*, dDec, mag | measured dRA*, dDec | angle meas vs pred (Earth only) |')
p('|---|---|---|---|---|---|---|---|')
for e in eps:
    r = R[e]
    a1, a2, c1 = r['aber_earth'], r['aber_earth+sc'], r['cmp_earth']
    p(f"| {e} | {r['v_earth_speed']:.2f} | {r['angle_star_apex_deg']:.1f} | {r['expected_mag_earth_arcsec']:.2f} | {a1['median_dRAcosd_arcsec']:+.2f}, {a1['median_dDec_arcsec']:+.2f}, {a1['mag_arcsec']:.2f} | {a2['median_dRAcosd_arcsec']:+.2f}, {a2['median_dDec_arcsec']:+.2f}, {a2['mag_arcsec']:.2f} | {r['median_dRAcosd_arcsec']:+.3f}, {r['median_dDec_arcsec']:+.3f} | {c1['angle_between_deg']:+.0f} |")
p()
p('Predicted differential aberration across the window (px range of the predicted shift over the matched stars) versus measured affine slopes (px per px)')
p()
p('| frame | predicted range dx, dy (px, Earth only) | predicted affine (a,b,c,d) Earth only | measured affine (a,b,c,d) | affine s.e. estimate per coefficient |')
p('|---|---|---|---|---|')
for e in eps:
    r = R[e]
    pa = r['aber_earth']['affine_params'][2:]
    ma = r['fits']['affine']['params'][2:]
    n = r['fits']['affine']['n_kept']
    se = 0.065 / (np.sqrt(n) * 295.0)    # sigma/(sqrt(N) * rms(x)); rms of x over a 1024 window = 295 px
    p(f"| {e} | {r['aber_earth']['range_dx_px']:.3f}, {r['aber_earth']['range_dy_px']:.3f} | " + ', '.join(f'{v:+.1e}' for v in pa) + ' | ' + ', '.join(f'{v:+.1e}' for v in ma) + f' | {se:.1e} |')
open(D + r'\tables.md', 'w', encoding='utf-8').write('\n'.join(L))
print('\n'.join(L))
