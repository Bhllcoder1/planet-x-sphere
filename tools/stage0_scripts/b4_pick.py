import csv, json, sys, time
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
rows = list(csv.DictReader(open(r"stage0\data\B\tap.csv", encoding="utf-8")))
rows = [r for r in rows if "/dr1/level2/" in r["uri"]]
print(len(rows))
def star(mjd):
    yr = 2000 + (float(mjd) - 51544.5) / 365.25
    dec0 = 4.69335; ra0 = 269.45207
    dec = dec0 + 10362.5e-3 / 3600 * (yr - 2000)
    ra = ra0 + (-797.8e-3 / 3600) / np.cos(np.radians(dec0)) * (yr - 2000)
    return ra, dec
out = []
# one candidate per (week-visit); spread over rows
step = max(1, len(rows) // 30)
for r in rows[::step][:30]:
    key = r["uri"].replace("ibe/data/spherex/", "")
    try:
        t = time.time()
        with fits.open("s3://nasa-irsa-spherex/" + key, fsspec_kwargs={"anon": True}) as h:
            hd = h["IMAGE"].header
            w = WCS(hd)
            ra, dec = star(r["time_bounds_lower"])
            x, y = w.all_world2pix(ra, dec, 0)
            out.append(dict(key=key, det=r["energy_bandpassname"], size=int(r["contentlength"]), mjd=r["time_bounds_lower"],
                            ra=ra, dec=dec, x0=float(x), y0=float(y), naxis=(hd["NAXIS1"], hd["NAXIS2"]), t=round(time.time() - t, 1)))
            print(out[-1], flush=True)
    except Exception as e:
        print("ERR", key, repr(e)[:200], flush=True)
json.dump(out, open(r"stage0\data\B\cands.json", "w"), indent=1)
