"""Stage0 D: flag statistics on 10 whole frames (anonymous S3). Saves FLAGS+IMAGE as npy in data/D/frames."""
import csv, json, os, sys, time
import numpy as np
from astropy.io import fits
from scipy import ndimage as ndi

D = r"stage0\data\D"
OUT = os.path.join(D, "frames"); os.makedirs(OUT, exist_ok=True)
BITS = dict(TRANSIENT=0, OVERFLOW=1, SUR_ERROR=2, NONFUNC=6, DICHROIC=7, MISSING_DATA=9, HOT=10, COLD=11,
            NONLINEAR=15, PERSIST=17, OUTLIER=19, CROSSTALK=20, SOURCE=21, GHOST=22, GHOST_FPA=23,
            GHOST_EXT=24, STREAK=25, BLOOM=26, SNOWBALL=27, HALO=28, SATELLITE_HALO=29)
FIT = 0x3C028E44; BKG = 0x3C2A8E47
EXTRA = (1 << 22) | (1 << 23) | (1 << 24) | (1 << 25) | (1 << 20) | (1 << 0)

def rows(name):
    return list(csv.DictReader(open(os.path.join(D, f"frames_{name}.csv"), encoding="utf8")))

def pick(name, dets, n):
    rs = [r for r in rows(name) if r["quality_flag"] in ("", "0")]
    chosen = []
    for d in dets:
        c = [r for r in rs if r["energy_bandpassname"] == f"SPHEREx-D{d}"]
        if c:
            chosen.append(c[len(c) // 2])  # middle in time
    return chosen[:n]

sel = [("gc", r) for r in pick("gc", [1, 2, 3, 4, 5], 5)] + [("sparse_ecl", r) for r in pick("sparse_ecl", [6, 1, 2, 3, 4], 5)]
print(len(sel), "frames")
res = []
for fld, r in sel:
    key = r["uri"].replace("ibe/data/spherex/", "")
    tag = os.path.basename(key).replace(".fits", "")
    t0 = time.time()
    try:
        with fits.open(f"s3://nasa-irsa-spherex/{key}", fsspec_kwargs={"anon": True}, lazy_load_hdus=True) as h:
            fl = np.asarray(h["FLAGS"].data).astype(np.int64) & 0xFFFFFFFF
            im = np.asarray(h["IMAGE"].data).astype(np.float32)
            hdr = dict(h["IMAGE"].header)
        np.save(os.path.join(OUT, tag + "_flags.npy"), fl.astype(np.uint32))
        np.save(os.path.join(OUT, tag + "_image.npy"), im)
        json.dump({k: (v if isinstance(v, (int, float, str, bool)) else str(v)) for k, v in hdr.items() if k != "COMMENT" and k != "HISTORY"},
                  open(os.path.join(OUT, tag + "_hdr.json"), "w"))
        N = fl.size
        d = dict(field=fld, tag=tag, det=r["energy_bandpassname"], mjd=float(r["time_bounds_lower"]), ver=r["provenance_version"],
                 frac={b: float(((fl >> v) & 1).sum() / N) for b, v in BITS.items()})
        for nm, m in (("FIT", FIT), ("BKG", BKG), ("EXTRA", EXTRA), ("FIT+EXTRA", FIT | EXTRA), ("BKG+EXTRA", BKG | EXTRA)):
            d["frac"][nm] = float(((fl & m) != 0).sum() / N)
        d["frac"]["nonzero"] = float((fl != 0).sum() / N)
        d["frac"]["nan_image"] = float(np.isnan(im).sum() / N)
        for b in ("STREAK", "SATELLITE_HALO", "SNOWBALL", "OUTLIER"):
            lab, n = ndi.label(((fl >> BITS[b]) & 1).astype(bool), structure=np.ones((3, 3)))
            d["ncomp_" + b] = int(n)
            if n:
                sz = np.bincount(lab.ravel())[1:]
                d["maxcomp_" + b] = int(sz.max())
        res.append(d)
        print(tag, d["det"], "%.1fs" % (time.time() - t0), "STREAK", d["frac"]["STREAK"], "ncomp", d["ncomp_STREAK"], flush=True)
    except Exception as e:
        print("FAIL", tag, repr(e), flush=True)
json.dump(res, open(os.path.join(D, "flagstats.json"), "w"), indent=1)
