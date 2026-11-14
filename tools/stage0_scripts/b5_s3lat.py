"""30 window reads (5 files x 6 windows), each window = IMAGE+VARIANCE+ZODI+FLAGS 100x100, with GET logging."""
import sys, time, json
import numpy as np
import s3fs
from astropy.io import fits

LOG = []
_orig = s3fs.core.S3File._fetch_range
def _logged(self, start, end, **kw):
    t = time.perf_counter()
    b = _orig(self, start, end, **kw)
    LOG.append((int(start), int(end), len(b), time.perf_counter() - t))
    return b
s3fs.core.S3File._fetch_range = _logged
def take():
    global LOG
    l, LOG = LOG, []
    return dict(n_get=len(l), bytes=sum(x[2] for x in l))

cands = json.load(open(r"stage0\data\B\cands.json"))
star = cands[4]; others = cands[:4]
files = [cands[i] for i in (4, 0, 2, 3, 1)]
BLOCK = int(sys.argv[2]) if len(sys.argv) > 2 else 2**20
CT = sys.argv[3] if len(sys.argv) > 3 else "readahead"
rng = np.random.default_rng(7)
IDX = {"IMAGE": 1, "FLAGS": 2, "VARIANCE": 3, "ZODI": 4}   # by index: avoids name scan over all HDUs
res = []
for fi, c in enumerate(files):
    path = "s3://nasa-irsa-spherex/" + c["key"]
    t0 = time.perf_counter(); take()
    hdul = fits.open(path, fsspec_kwargs={"anon": True, "default_cache_type": CT, "default_block_size": BLOCK}, lazy_load_hdus=True)
    hdrs = {n: hdul[i].header for n, i in IDX.items()}   # forces header reads
    ho = take(); ho["t"] = time.perf_counter() - t0
    res.append(dict(kind="open", file=fi, key=c["key"], **ho))
    print("open", fi, ho, flush=True)
    for wi in range(6):
        x0 = int(rng.integers(50, 1890)); y0 = int(rng.integers(50, 1890))
        if fi == 0 and wi == 0:
            x0, y0 = int(c["x0"]) - 50, int(c["y0"]) - 50
        tf = time.perf_counter()
        for n in ["IMAGE", "VARIANCE", "ZODI", "FLAGS"]:
            take(); t = time.perf_counter()
            a = hdul[IDX[n]].section[y0:y0 + 100, x0:x0 + 100]
            dt = time.perf_counter() - t; g = take()
            assert a.shape == (100, 100)
            res.append(dict(kind="hdu", file=fi, win=wi, x0=x0, y0=y0, hdu=n, t=dt, **g))
        res.append(dict(kind="frame", file=fi, win=wi, t=time.perf_counter() - tf))
        print("frame", fi, wi, round(res[-1]["t"], 2), flush=True)
    hdul.close()
json.dump(res, open(sys.argv[1], "w"), indent=1)
