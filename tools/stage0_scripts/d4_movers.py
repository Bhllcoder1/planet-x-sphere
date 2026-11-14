"""Stage0 D part 3b: known asteroids (SkyBoT) vs saved IMAGE/FLAGS. Local-peak search at predicted position, static-star control."""
import glob, json, os, sys
import numpy as np, requests
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
import astropy.units as u
from scipy import ndimage as ndi

D = r"stage0\data\D"
F = os.path.join(D, "frames")
BITS = dict(TRANSIENT=0, OVERFLOW=1, SUR_ERROR=2, NONFUNC=6, DICHROIC=7, PERSIST=17, OUTLIER=19, CROSSTALK=20, SOURCE=21,
            GHOST=22, STREAK=25, BLOOM=26, SNOWBALL=27, HALO=28, SATELLITE_HALO=29)
FIT = 0x3C028E44; BKG = 0x3C2A8E47; EXTRA = (1 << 22) | (1 << 23) | (1 << 24) | (1 << 25) | (1 << 20) | (1 << 0)
URL = "https://ssp.imcce.fr/webservices/skybot/api/conesearch.php"
VMAX = 18.0

def core_stats(fl, x, y):
    """flags in the 3x3 core and 7x7 (+/-3 px) window around integer pixel (x,y)."""
    c = fl[y - 1:y + 2, x - 1:x + 2]; w = fl[y - 3:y + 4, x - 3:x + 4]
    d = dict(core={b: int(((c >> v) & 1).sum()) for b, v in BITS.items() if ((c >> v) & 1).any()},
             win={b: int(((w >> v) & 1).sum()) for b, v in BITS.items() if ((w >> v) & 1).any()})
    for nm, m in (("FIT", FIT), ("BKG", BKG), ("EXTRA", EXTRA)):
        d["core_" + nm] = int(((c & m) != 0).sum())
        d["core_any_nonSOURCE_" + nm] = int(((c & (m & ~(1 << 21))) != 0).sum())
    return d

tags = sorted({os.path.basename(p)[:-10] for p in glob.glob(os.path.join(F, "*_flags.npy"))})
sel = sys.argv[1:] or [""]
allres = {}
for tag in tags:
    if not any(s in tag for s in sel): continue
    hd = json.load(open(os.path.join(F, tag + "_hdr.json")))
    hdr = fits.Header()
    for k, v in hd.items():
        try: hdr[k] = v
        except Exception: pass
    w = WCS(hdr)
    fl = np.load(os.path.join(F, tag + "_flags.npy")).astype(np.int64)
    im = np.load(os.path.join(F, tag + "_image.npy"))
    mjd = hd["MJD-AVG"]
    ra0, dec0 = w.wcs_pix2world([[1019.5, 1019.5]], 0)[0]
    cache = os.path.join(D, tag + "_skybot.json")
    if os.path.exists(cache):
        js = json.load(open(cache))
    else:
        r = requests.get(URL, params={"-ep": mjd + 2400000.5, "-ra": ra0, "-dec": dec0, "-rs": 3.0 * 3600, "-mime": "json", "-output": "all",
                                      "-observer": 500, "-filter": 0, "-objFilter": "100", "-refsys": "EQJ2000", "-from": "spherex_stage0"}, timeout=180)
        js = r.json(); json.dump(js, open(cache, "w"))
    objs = js if isinstance(js, list) else []
    good = np.isfinite(im)
    med = np.nanmedian(im); bkg = ndi.median_filter(np.where(good, im, med)[::4, ::4], size=15)
    bkg = ndi.zoom(bkg, 4, order=1)[:2040, :2040]
    res = np.where(good, im - bkg, 0.0)
    sd = 1.4826 * np.nanmedian(np.abs(res[good] - np.nanmedian(res[good])))
    # all local peaks (static control pool)
    mx = ndi.maximum_filter(res, size=7)
    pk = np.argwhere((res == mx) & (res > 8 * sd))
    pk = pk[(pk[:, 0] > 5) & (pk[:, 0] < 2034) & (pk[:, 1] > 5) & (pk[:, 1] < 2034)]
    # predicted positions
    preds = []
    for o in objs:
        try:
            c = SkyCoord(o["RA (hms)"], o["DEC (dms)"], unit=(u.hourangle, u.deg)); v = float(o["VMag (mag)"]); err = float(o["Err (arcsec)"])
        except Exception: continue
        x, y = w.wcs_world2pix([[c.ra.deg, c.dec.deg]], 0)[0]
        preds.append((v, err, o, x, y))
    inside = [p for p in preds if 6 < p[3] < 2033 and 6 < p[4] < 2033]
    ss_xy = np.array([[p[3], p[4]] for p in preds]) if preds else np.zeros((0, 2))
    print(f"\n### {tag} MJD-AVG {mjd:.5f} sd={sd:.4f} nSkyBoT={len(objs)} inFootprint={len(inside)} V<{VMAX}: {sum(p[0] < VMAX for p in inside)} localpeaks>8sd={len(pk)}", flush=True)
    rec = []
    for v, err, o, x, y in sorted(inside, key=lambda p: p[0]):
        if v >= VMAX: break
        xi, yi = int(round(x)), int(round(y))
        win = res[yi - 4:yi + 5, xi - 4:xi + 5]
        iy, ix = np.unravel_index(np.argmax(win), win.shape)
        px, py = xi - 4 + ix, yi - 4 + iy
        peak = float(res[py, px]); snr = peak / sd; off = float(np.hypot(px - x, py - y))
        r = dict(name=o.get("Name"), num=o.get("Num"), V=v, err=err, x=float(x), y=float(y), peak=peak, snr=float(snr), offset_px=off,
                 mu=(o.get("dRA (arcsec/h)"), o.get("dDEC (arcsec/h)")), detected=bool(snr > 8 and off < 3.0))
        if r["detected"]:
            r.update(core_stats(fl, px, py))
        rec.append(r)
        print(json.dumps({k: (round(x_, 3) if isinstance(x_, float) else x_) for k, x_ in r.items() if k not in ("win",)}, default=str)[:700], flush=True)
    # static controls: local peaks away (>10 px) from every SkyBoT position (any V), peak within 0.5-2x of detected movers
    stat = []
    for r in rec:
        if not r["detected"]: continue
        for (py, px) in pk:
            if 0.5 * r["peak"] <= res[py, px] <= 2 * r["peak"] and (len(ss_xy) == 0 or np.min(np.hypot(ss_xy[:, 0] - px, ss_xy[:, 1] - py)) > 10):
                stat.append(core_stats(fl, px, py) | {"peak": float(res[py, px]), "x": int(px), "y": int(py)})
    allres[tag] = dict(movers=rec, n_static=len(stat), static=stat[:400])
    json.dump(allres, open(os.path.join(D, "movers_results_" + ("all" if not sys.argv[1:] else "sel") + ".json"), "w"), default=str)
    if stat:
        n = len(stat)
        print("STATIC controls (peak within 0.5-2x of movers):", n, "core3x3 pixels flagged any-of-mask (frac of stars with >=1 core pix):",
              {m: round(sum(s["core_" + m] > 0 for s in stat) / n, 3) for m in ("FIT", "BKG", "EXTRA")},
              "core bit presence:", {b: round(sum(b in s["core"] for s in stat) / n, 3) for b in BITS if any(b in s["core"] for s in stat)}, flush=True)
