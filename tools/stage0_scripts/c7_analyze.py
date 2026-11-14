"""Stage-0 test C: header WCS vs Gaia DR3 + predicted aberration, for 3 SPHEREx L2 frames of the Barnard's Star field."""
import warnings, json, sys
import numpy as np
from astropy.io import fits
from astropy.table import Table
from astropy.time import Time
from astropy.wcs import WCS
from astropy.wcs.utils import proj_plane_pixel_scales
from astropy.coordinates import SkyCoord, get_body_barycentric_posvel, get_body_barycentric, CartesianRepresentation
import astropy.units as u
from astropy.stats import sigma_clipped_stats
from photutils.background import Background2D, MedianBackground
from photutils.detection import DAOStarFinder
from scipy.spatial import cKDTree
warnings.filterwarnings('ignore')

D = r'stage0\data\C'
FITMASK = 0x3C028E44
CENMASK = FITMASK | (1 << 1) | (1 << 7)
C_KMS = 299792.458
GMAX, GMIN, RUWEMAX = 17.0, 11.0, 1.4
ISO_ARCSEC = 20.0      # no other Gaia G<18 within this radius (3.3 px)
DET_ISO_PX = 3.5       # no other detection within this radius
FWHM = 2.5
out = {}
rows_md = []


def com5(sub, mask, xi, yi):
    """5x5 centre of mass (iterated 3x), reject if any masked/non-finite pixel in the box. returns x,y,flux or None."""
    ny, nx = sub.shape
    for _ in range(3):
        if xi < 2 or yi < 2 or xi > nx - 3 or yi > ny - 3:
            return None
        b = sub[yi - 2:yi + 3, xi - 2:xi + 3]
        m = mask[yi - 2:yi + 3, xi - 2:xi + 3]
        if m.any() or not np.isfinite(b).all():
            return None
        wgt = np.clip(b, 0, None)
        s = wgt.sum()
        if s <= 0:
            return None
        yy, xx = np.mgrid[-2:3, -2:3]
        cx = (wgt * xx).sum() / s; cy = (wgt * yy).sum() / s
        xn, yn = xi + int(round(cx)), yi + int(round(cy))
        if (xn, yn) == (xi, yi):
            return xi + cx, yi + cy, s
        xi, yi = xn, yn
    return xi + cx, yi + cy, s


def robust(a):
    a = np.asarray(a)
    med = np.median(a)
    return med, 1.4826 * np.median(np.abs(a - med))


def fit_model(x, y, dx, dy, kind, clip=3.0, niter=6):
    """kind: 'shift' | 'sim' (shift+rot+scale) | 'affine'. x,y centred coords (px). returns params, residuals, keep mask."""
    keep = np.ones(len(x), bool)
    for _ in range(niter):
        if kind == 'shift':
            A = np.zeros((2 * keep.sum(), 2)); A[:keep.sum(), 0] = 1; A[keep.sum():, 1] = 1
        elif kind == 'sim':
            n = keep.sum(); A = np.zeros((2 * n, 4))
            A[:n, 0] = 1; A[:n, 2] = x[keep]; A[:n, 3] = -y[keep]
            A[n:, 1] = 1; A[n:, 2] = y[keep]; A[n:, 3] = x[keep]
        else:
            n = keep.sum(); A = np.zeros((2 * n, 6))
            A[:n, 0] = 1; A[:n, 2] = x[keep]; A[:n, 3] = y[keep]
            A[n:, 1] = 1; A[n:, 4] = x[keep]; A[n:, 5] = y[keep]
        b = np.concatenate([dx[keep], dy[keep]])
        p, *_ = np.linalg.lstsq(A, b, rcond=None)
        res = predict(p, x, y, kind)
        rx, ry = dx - res[0], dy - res[1]
        r = np.hypot(rx, ry)
        s = 1.4826 * np.median(r[keep]) / 1.1774 if keep.sum() > 5 else r.std()   # 2D Rayleigh: median = 1.1774 sigma
        newkeep = r < clip * 1.5 * s if s > 0 else keep
        if (newkeep == keep).all():
            break
        keep = newkeep
    rx, ry = dx - res[0], dy - res[1]
    return p, rx, ry, keep


def predict(p, x, y, kind):
    if kind == 'shift':
        return np.full_like(x, p[0]), np.full_like(x, p[1])
    if kind == 'sim':
        return p[0] + p[2] * x - p[3] * y, p[1] + p[2] * y + p[3] * x
    return p[0] + p[2] * x + p[3] * y, p[1] + p[4] * x + p[5] * y


def earth_pos_au(t):
    return get_body_barycentric('earth', t).xyz.to(u.AU).value


EPS = sys.argv[1] if len(sys.argv) > 1 else 'ABC'
for ep in EPS:
    z = np.load(f'{D}\\frame_{ep}.npz')
    img, var, flg = z['img'].astype(float), z['var'].astype(float), z['flg']
    x0, y0 = int(z['x0']), int(z['y0'])
    hd = fits.Header.fromstring(open(f'{D}\\hdr_{ep}.txt').read(), sep='\n')
    w = WCS(hd)
    mjd = float(hd['MJD-AVG'])
    t = Time(mjd, format='mjd', scale='utc')
    scale = proj_plane_pixel_scales(w) * 3600.0
    R = {'ep': ep, 'rel': str(z['rel']), 'obsid': hd['OBSID'], 'mjd': mjd, 'date': hd['DATE-OBS'], 'x0': x0, 'y0': y0,
         'pixscale_arcsec': [float(s) for s in scale], 'FINAST': hd.get('FINAST'), 'MATCH_NSTARS': hd.get('MATCH_NSTARS'),
         'RADESYS': hd.get('RADESYS'), 'CTYPE1': hd['CTYPE1']}
    bad = ((flg & FITMASK) != 0) | ~np.isfinite(img) | ~np.isfinite(var) | (var <= 0)
    cbad = ((flg & CENMASK) != 0) | ~np.isfinite(img) | ~np.isfinite(var) | (var <= 0)
    R['frac_bad_fitmask'] = float(bad.mean())
    R['frac_SOURCE_flag'] = float(((flg >> 21) & 1).mean())
    bkg = Background2D(np.where(bad, np.nan, img), (64, 64), filter_size=3, mask=bad, exclude_percentile=50.0, bkg_estimator=MedianBackground())
    sub = img - bkg.background
    rms = float(bkg.background_rms_median)
    R['bkg_median'] = float(np.median(bkg.background)); R['rms_med'] = rms
    finder = DAOStarFinder(threshold=5 * rms, fwhm=FWHM)
    det = finder(np.where(bad, 0.0, sub), mask=bad)
    R['n_daofind'] = 0 if det is None else len(det)
    dets = []
    kx, ky = ('x_centroid', 'y_centroid') if 'x_centroid' in det.colnames else ('xcentroid', 'ycentroid')
    for r in det:
        c = com5(sub, cbad, int(round(r[kx])), int(round(r[ky])))
        if c is not None:
            dets.append(c)
    dets = np.array(dets)
    R['n_centroided'] = len(dets)
    dx_full = dets[:, 0] + x0; dy_full = dets[:, 1] + y0     # 0-based full-frame pixel coords
    dtree = cKDTree(np.c_[dx_full, dy_full])
    # detections' own isolation
    dd, _ = dtree.query(np.c_[dx_full, dy_full], k=2)
    det_iso = dd[:, 1] > DET_ISO_PX
    # ---------------- Gaia -------------
    import os
    gsrc = 'ESA gea.esac.esa.int TAP' if os.path.exists(f'{D}\\gaia_{ep}.fits') else 'MAST gaiadr3 TAP (mast.stsci.edu/vo-tap)'
    g = Table.read(f'{D}\\gaia_{ep}.fits' if os.path.exists(f'{D}\\gaia_{ep}.fits') else f'{D}\\gaiaM_{ep}.fits')
    if len(sys.argv) > 2 and sys.argv[2] == 'mast':
        gsrc = 'MAST gaiadr3 TAP (mast.stsci.edu/vo-tap)'; g = Table.read(f'{D}\\gaiaM_{ep}.fits')
    for cn in g.colnames:
        if hasattr(g[cn], 'filled'):
            g[cn] = g[cn].filled(np.nan) if g[cn].dtype.kind == 'f' else g[cn].filled(0)
    R['gaia_source'] = gsrc
    g = g[np.isfinite(g['pmra']) & np.isfinite(g['pmdec']) & (g['astrometric_params_solved'] > 3)] if False else g
    gall = g
    # isolation among ALL Gaia G<18 (including 2-parameter)
    sc_all = SkyCoord(np.array(gall['ra']) * u.deg, np.array(gall['dec']) * u.deg)
    idx, d2, _ = sc_all.match_to_catalog_sky(sc_all, nthneighbor=2)
    iso_gaia = d2.arcsec > ISO_ARCSEC
    sel = (np.array(gall['phot_g_mean_mag']) < GMAX) & (np.array(gall['phot_g_mean_mag']) > GMIN) & iso_gaia \
          & (np.array(gall['ruwe']) < RUWEMAX) & (np.array(gall['astrometric_params_solved']) > 3) \
          & np.isfinite(np.array(gall['pmra'], float)) & np.isfinite(np.array(gall['pmdec'], float))
    gs = gall[sel]
    R['n_gaia_rows'] = len(gall); R['n_gaia_sel'] = len(gs)
    plx = np.array(gs['parallax'], float); plx_f = np.where(np.isfinite(plx) & (plx > 0.05), plx, 0.05)
    c0 = SkyCoord(ra=np.array(gs['ra']) * u.deg, dec=np.array(gs['dec']) * u.deg,
                  pm_ra_cosdec=np.array(gs['pmra'], float) * u.mas / u.yr, pm_dec=np.array(gs['pmdec'], float) * u.mas / u.yr,
                  distance=(1000.0 / plx_f) * u.pc, radial_velocity=np.zeros(len(gs)) * u.km / u.s,
                  obstime=Time(2016.0, format='jyear'), frame='icrs')
    c1 = c0.apply_space_motion(new_obstime=t)    # proper motion only (barycentric); parallax added below
    ra1, dec1 = c1.ra.rad, c1.dec.rad
    X, Y, Zc = earth_pos_au(t)                  # Earth barycentric position (AU), ICRS equatorial
    pl = np.where(np.isfinite(plx), plx, 0.0) / 1000.0 / 3600.0 * np.pi / 180.0   # rad
    dra = pl * (X * np.sin(ra1) - Y * np.cos(ra1)) / np.cos(dec1)
    ddec = pl * (X * np.cos(ra1) * np.sin(dec1) + Y * np.sin(ra1) * np.sin(dec1) - Zc * np.cos(dec1))
    ra_par, dec_par = ra1 + dra, dec1 + ddec
    R['max_parallax_shift_mas'] = float(np.max(np.hypot(dra * np.cos(dec1), ddec)) * 206264806.0)
    R['max_pm_shift_mas'] = float(np.max(np.hypot(*(np.array([gs['pmra'], gs['pmdec']], float) * (mjd - 57388.0) / 365.25))))
    # ---------------- project ------------
    def proj(ra_rad, dec_rad):
        return np.array(w.all_world2pix(np.degrees(ra_rad), np.degrees(dec_rad), 0, tolerance=1e-8, maxiter=50))
    px, py = proj(ra_par, dec_par)
    px_np, py_np = proj(ra1, dec1)              # without parallax
    inwin = (px > x0 + 8) & (px < x0 + 1016) & (py > y0 + 8) & (py < y0 + 1016)
    R['n_gaia_inwin'] = int(inwin.sum())
    # raw 2 px match, no shift
    gtree = cKDTree(np.c_[px[inwin], py[inwin]])
    # coarse offset search: all detection-star offsets within 8 px, histogram peak
    pairs = gtree.query_ball_tree(dtree, 8.0)
    offs = []
    gi = np.where(inwin)[0]
    for k, lst in enumerate(pairs):
        for j in lst:
            offs.append((dx_full[j] - px[gi[k]], dy_full[j] - py[gi[k]]))
    offs = np.array(offs)
    H, xe, ye = np.histogram2d(offs[:, 0], offs[:, 1], bins=32, range=[[-8, 8], [-8, 8]])
    ix, iy = np.unravel_index(np.argmax(H), H.shape)
    pk = ((xe[ix] + xe[ix + 1]) / 2, (ye[iy] + ye[iy + 1]) / 2)
    bg_level = np.median(H)
    R['coarse_peak_px'] = [float(pk[0]), float(pk[1])]; R['coarse_peak_counts'] = int(H.max()); R['coarse_hist_median'] = float(bg_level)
    # refined: match around pk within 2 px, iterating the centre once on the median
    def do_match(cen, rad):
        tree = cKDTree(np.c_[dx_full, dy_full])
        d, j = tree.query(np.c_[px[gi] + cen[0], py[gi] + cen[1]], distance_upper_bound=rad)
        ok = np.isfinite(d)
        return gi[ok], j[ok]
    gm, dm = do_match((0, 0), 2.0)
    R['n_match_raw_2px_noshift'] = int(len(gm))
    cen = pk
    for _ in range(3):
        gm, dm = do_match(cen, 2.0)
        ok = det_iso[dm]
        mdx = dx_full[dm][ok] - px[gm][ok]; mdy = dy_full[dm][ok] - py[gm][ok]
        cen = (np.median(mdx), np.median(mdy))
    R['n_match_2px'] = int(len(mdx))
    # unique detection per star: ensure detection used once
    mx = dx_full[dm][ok]; my = dy_full[dm][ok]
    gmatch = gm[ok]
    # offsets relative to prediction (including parallax)
    odx = mx - px[gmatch]; ody = my - py[gmatch]
    xc, yc = px[gmatch] - (x0 + 512), py[gmatch] - (y0 + 512)       # centred coords
    med_dx, sig_dx = robust(odx); med_dy, sig_dy = robust(ody)
    N = len(odx)
    R['median_dx_px'] = float(med_dx); R['median_dy_px'] = float(med_dy)
    R['robust_sigma_dx_px'] = float(sig_dx); R['robust_sigma_dy_px'] = float(sig_dy)
    R['sem_dx_px'] = float(1.2533 * sig_dx / np.sqrt(N)); R['sem_dy_px'] = float(1.2533 * sig_dy / np.sqrt(N))
    # without parallax variant
    odx_np = mx - px_np[gmatch]; ody_np = my - py_np[gmatch]
    R['median_dx_noparallax'] = float(np.median(odx_np)); R['median_dy_noparallax'] = float(np.median(ody_np))
    # sky offsets (RA*, Dec arcsec) of measured centroid vs predicted: via WCS at matched stars
    wm = np.array(w.all_pix2world(mx, my, 0)); wp = np.array(w.all_pix2world(px[gmatch], py[gmatch], 0))
    dsky_ra = (wm[0] - wp[0] + 180) % 360 - 180
    dsky_ra = dsky_ra * np.cos(np.radians(wp[1])) * 3600.0
    dsky_de = (wm[1] - wp[1]) * 3600.0
    R['median_dRAcosd_arcsec'] = float(np.median(dsky_ra)); R['median_dDec_arcsec'] = float(np.median(dsky_de))
    R['median_dx_arcsec'] = float(med_dx * scale[0]); R['median_dy_arcsec'] = float(med_dy * scale[1])
    # fits
    fits_out = {}
    for kind in ('shift', 'sim', 'affine'):
        p, rx, ry, keep = fit_model(xc, yc, odx, ody, kind)
        rms_px = float(np.sqrt(np.mean(rx[keep] ** 2 + ry[keep] ** 2) / 2))   # per-axis RMS
        fits_out[kind] = {'params': [float(v) for v in p], 'rms_peraxis_px': rms_px, 'rms_peraxis_arcsec': rms_px * float(scale.mean()),
                          'n_kept': int(keep.sum()), 'n': int(N)}
        if kind == 'affine':
            # held-out RMS: 70/30 split
            rng = np.random.default_rng(1); idx_ = rng.permutation(N); ntr = int(0.7 * N)
            hh = {}
            for k2 in ('shift', 'sim', 'affine'):
                ptr, *_ = fit_model(xc[idx_[:ntr]], yc[idx_[:ntr]], odx[idx_[:ntr]], ody[idx_[:ntr]], k2)
                pr = predict(ptr, xc[idx_[ntr:]], yc[idx_[ntr:]], k2)
                rr = np.hypot(odx[idx_[ntr:]] - pr[0], ody[idx_[ntr:]] - pr[1])
                hh[k2] = float(1.4826 * np.median(rr) / 1.1774 / 1.0)   # per-axis robust sigma from median radial
            fits_out['heldout_robust_peraxis_px'] = hh
    R['fits'] = fits_out
    # position dependence: 3x3 grid medians
    grid = []
    gxi = np.clip(((px[gmatch] - x0) // (1024 / 3)).astype(int), 0, 2); gyi = np.clip(((py[gmatch] - y0) // (1024 / 3)).astype(int), 0, 2)
    for a in range(3):
        for b_ in range(3):
            m = (gxi == b_) & (gyi == a)       # a: y-row, b_: x-col
            if m.sum() >= 5:
                grid.append({'xcol': b_, 'yrow': a, 'n': int(m.sum()), 'mdx': float(np.median(odx[m])), 'mdy': float(np.median(ody[m]))})
    R['grid3x3'] = grid
    # ---------------- aberration prediction ------------
    pe, ve = get_body_barycentric_posvel('earth', t)
    v_earth = ve.xyz.to(u.km / u.s).value
    v_sc = np.array([hd['VX_SC'], hd['VY_SC'], hd['VZ_SC']], float)
    R['v_earth_kms'] = [float(v) for v in v_earth]; R['v_earth_speed'] = float(np.linalg.norm(v_earth))
    R['v_sc_kms'] = [float(v) for v in v_sc]; R['v_sc_speed'] = float(np.linalg.norm(v_sc))
    apex = v_earth / np.linalg.norm(v_earth)
    # use matched stars (propagated + parallax)
    # gmatch indexes gs rows directly
    ram, decm = ra_par[gmatch], dec_par[gmatch]
    n = np.c_[np.cos(decm) * np.cos(ram), np.cos(decm) * np.sin(ram), np.sin(decm)]

    def aberrate(n, v):
        b = v / C_KMS
        npb = n + b - n * (n @ b)[:, None]       # first order
        npb /= np.linalg.norm(npb, axis=1)[:, None]
        return np.arctan2(npb[:, 1], npb[:, 0]) % (2 * np.pi), np.arcsin(npb[:, 2])
    for label, v in (('earth', v_earth), ('earth+sc', v_earth + v_sc)):
        ra_a, dec_a = aberrate(n, v)
        pxa, pya = np.array(w.all_world2pix(np.degrees(ra_a), np.degrees(dec_a), 0, tolerance=1e-8, maxiter=50))
        ab_dx = pxa - px[gmatch]; ab_dy = pya - py[gmatch]
        dRA = ((ra_a - ram + np.pi) % (2 * np.pi) - np.pi) * np.cos(decm) * 206264.806
        dDE = (dec_a - decm) * 206264.806
        pa, _, _, _ = fit_model(xc, yc, ab_dx, ab_dy, 'affine', clip=1e9)
        R['aber_' + label] = {'median_dx_px': float(np.median(ab_dx)), 'median_dy_px': float(np.median(ab_dy)),
                              'median_dRAcosd_arcsec': float(np.median(dRA)), 'median_dDec_arcsec': float(np.median(dDE)),
                              'mag_arcsec': float(np.hypot(np.median(dRA), np.median(dDE))),
                              'range_dx_px': float(np.ptp(ab_dx)), 'range_dy_px': float(np.ptp(ab_dy)),
                              'affine_params': [float(v_) for v_ in pa]}
    # angle between star direction and apex (centre of window)
    nc = n.mean(axis=0); nc /= np.linalg.norm(nc)
    R['angle_star_apex_deg'] = float(np.degrees(np.arccos(nc @ apex)))
    R['expected_mag_earth_arcsec'] = float(np.linalg.norm(v_earth) / C_KMS * 206264.806 * np.sin(np.arccos(nc @ apex)))
    # compare to measured (sky vector)
    me = np.array([R['median_dRAcosd_arcsec'], R['median_dDec_arcsec']])
    for label in ('earth', 'earth+sc'):
        pr = np.array([R['aber_' + label]['median_dRAcosd_arcsec'], R['aber_' + label]['median_dDec_arcsec']])
        ang = np.degrees(np.arctan2(me[0] * pr[1] - me[1] * pr[0], me @ pr))
        R['cmp_' + label] = {'meas_mag_arcsec': float(np.linalg.norm(me)), 'pred_mag_arcsec': float(np.linalg.norm(pr)),
                             'angle_between_deg': float(ang), 'projection_of_meas_on_pred_arcsec': float(me @ pr / np.linalg.norm(pr)),
                             'meas_minus_pred_arcsec': [float(v) for v in me - pr]}
    out[ep] = R
    np.savez(f'{D}\\matched_{ep}.npz', mx=mx, my=my, px=px[gmatch], py=py[gmatch], gmag=np.array(gs['phot_g_mean_mag'])[gmatch],
             odx=odx, ody=ody)
    print(ep, 'done', N, flush=True)

json.dump(out, open(f'{D}\\results_{EPS}{"_mast" if len(sys.argv) > 2 else ""}.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
