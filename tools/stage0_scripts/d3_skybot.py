"""Stage0 D part 3: SkyBoT known movers vs IMAGE/FLAGS in saved whole frames."""
import glob, json, os, sys
import numpy as np, requests
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
import astropy.units as u
from astropy.stats import sigma_clipped_stats
from photutils.detection import DAOStarFinder
from scipy import ndimage as ndi

D = r"stage0\data\D"
F = os.path.join(D, "frames")
BITS = dict(TRANSIENT=0, OVERFLOW=1, SUR_ERROR=2, NONFUNC=6, DICHROIC=7, HOT=10, COLD=11, PERSIST=17, OUTLIER=19,
            CROSSTALK=20, SOURCE=21, GHOST=22, STREAK=25, BLOOM=26, SNOWBALL=27, HALO=28, SATELLITE_HALO=29)
PS = 6.15
want = sys.argv[1:]  # substrings of tags
URL = "https://ssp.imcce.fr/webservices/skybot/api/conesearch.php"

def bitsum(fl, x, y, r=3):
    x0, y0 = int(round(x)), int(round(y))
    sub = fl[max(0, y0 - r):y0 + r + 1, max(0, x0 - r):x0 + r + 1]
    return {b: float(((sub >> v) & 1).any(axis=None)) if False else int(((sub >> v) & 1).sum()) for b, v in BITS.items() if ((sub >> v) & 1).any()}

out = {}
for sub in want:
    tag = [os.path.basename(p)[:-10] for p in glob.glob(os.path.join(F, "*_flags.npy")) if sub in p][0]
    hd = json.load(open(os.path.join(F, tag + "_hdr.json")))
    hdr = fits.Header()
    for k, v in hd.items():
        try: hdr[k] = v
        except Exception: pass
    w = WCS(hdr)
    fl = np.load(os.path.join(F, tag + "_flags.npy")).astype(np.int64)
    im = np.load(os.path.join(F, tag + "_image.npy"))
    mjd = hd.get("MJD-AVG")
    ra0, dec0 = w.wcs_pix2world([[1019.5, 1019.5]], 0)[0]
    print("\n###", tag, "MJD-AVG", mjd, "center", ra0, dec0, "EXPTIME-ish", hd.get("EXPTIME"), hd.get("TELAPSE"), flush=True)
    r = requests.get(URL, params={"-ep": mjd + 2400000.5, "-ra": ra0, "-dec": dec0, "-rs": 3.0 * 3600, "-mime": "json",
                                  "-output": "all", "-observer": 500, "-filter": 0, "-objFilter": "100", "-refsys": "EQJ2000",
                                  "-from": "spherex_stage0"}, timeout=120)
    print("SkyBoT", r.status_code, r.url[:200])
    js = r.json()
    objs = js if isinstance(js, list) else []
    if not objs: print("RAW", str(js)[:300])
    print("n objects total in cone", len(objs))
    json.dump(js, open(os.path.join(D, tag + "_skybot.json"), "w"))
    # background + detections (whole frame)
    good = np.isfinite(im)
    m, med, sd = sigma_clipped_stats(im[good], sigma=3, maxiters=5)
    # local background via median filter on a coarse grid
    bkg = ndi.median_filter(np.where(good, im, med)[::4, ::4], size=15)
    bkg = ndi.zoom(bkg, 4, order=1)[:2040, :2040]
    res = np.where(good, im - bkg, 0.0)
    _, _, sd2 = sigma_clipped_stats(res[good], sigma=3, maxiters=5)
    fin = DAOStarFinder(threshold=5 * sd2, fwhm=2.5)
    src = fin(res)
    print("frame bkg sigma", sd2, "n DAO detections", 0 if src is None else len(src))
    cand = []
    for o in objs:
        try:
            _c = SkyCoord(o["RA (hms)"], o["DEC (dms)"], unit=(u.hourangle, u.deg)); ra = _c.ra.deg; dec = _c.dec.deg
            v = float(o["VMag (mag)"]); err = float(o["Err (arcsec)"])
        except Exception as e:
            continue
        x, y = w.wcs_world2pix([[ra, dec]], 0)[0]
        if -10 < x < 2050 and -10 < y < 2050:
            cand.append((v, err, o, x, y, ra, dec))
    print("in footprint:", len(cand), " V<17:", sum(c[0] < 17 for c in cand), " V<17 & err<30:", sum(c[0] < 17 and c[1] < 30 for c in cand),
          " err list(V<17):", sorted(round(c[1], 1) for c in cand if c[0] < 17)[:30])
    out[tag] = []
    for v, err, o, x, y, ra, dec in sorted(cand, key=lambda c: c[0]):
        if v >= 17.5: break
        rad = max(2.0, err / PS) + 3
        rec = dict(name=o.get("Name"), num=o.get("Num"), V=v, err_as=err, x=x, y=y, rad_px=rad,
                   mu_arcsec_h=(o.get("dRA (arcsec/h)"), o.get("dDEC (arcsec/h)")), flags_at_pred=bitsum(fl, x, y, 3) if 0 <= x < 2040 and 0 <= y < 2040 else None)
        dets = []
        if src is not None:
            for s in src:
                d = np.hypot(s["x_centroid"] - x, s["y_centroid"] - y)
                if d < rad:
                    dets.append(dict(x=float(s["x_centroid"]), y=float(s["y_centroid"]), d=float(d), peak=float(s["peak"]), snr=float(s["peak"] / sd2),
                                     sharp=float(s["sharpness"]), round1=float(s["roundness1"]), flags3=bitsum(fl, s["x_centroid"], s["y_centroid"], 3)))
        rec["dets"] = dets
        out[tag].append(rec)
        print(json.dumps(rec, default=str)[:900])
    # static-star flag comparison: all detections with SNR 8-50
    if src is not None:
        cnt = {b: 0 for b in BITS}; n = 0
        for s in src:
            snr = s["peak"] / sd2
            if 8 < snr < 60 and 5 < s["x_centroid"] < 2035 and 5 < s["y_centroid"] < 2035:
                n += 1
                for b, c in bitsum(fl, s["x_centroid"], s["y_centroid"], 3).items(): cnt[b] += 1
        print("STATIC-like detections SNR 8-60:", n, {b: round(c / max(n, 1), 3) for b, c in cnt.items() if c})
        out[tag + "_static"] = dict(n=n, frac={b: c / max(n, 1) for b, c in cnt.items() if c})
json.dump(out, open(os.path.join(D, "skybot_results.json"), "w"), indent=1, default=str)

