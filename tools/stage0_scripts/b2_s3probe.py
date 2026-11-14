"""Probe 1 frame on S3: log every GET range issued by s3fs while reading windows."""
import sys, time, json, csv, io
import numpy as np
import s3fs
from astropy.io import fits

LOG = []
_orig = s3fs.core.S3File._fetch_range
def _logged(self, start, end, **kw):
    t = time.perf_counter()
    b = _orig(self, start, end, **kw)
    LOG.append((start, end, len(b), time.perf_counter() - t))
    return b
s3fs.core.S3File._fetch_range = _logged

def take():
    global LOG
    l, LOG = LOG, []
    return l

def summ(l):
    return dict(n_get=len(l), bytes=sum(x[2] for x in l), secs=round(sum(x[3] for x in l), 3))

def run(key, cache_type, block_size, x0=900, y0=900, n=100):
    path = f"s3://nasa-irsa-spherex/{key}"
    kw = {"anon": True, "default_cache_type": cache_type, "default_block_size": block_size}
    out = {"cache": cache_type, "block": block_size}
    t0 = time.perf_counter()
    take()
    hdul = fits.open(path, fsspec_kwargs=kw, lazy_load_hdus=True)
    out["open"] = summ(take()); out["open"]["t"] = round(time.perf_counter() - t0, 2)
    out["hdus"] = [(h.name, type(h).__name__) for h in hdul]
    out["filesize"] = hdul._file.size if hasattr(hdul._file, "size") else None
    for name in ["IMAGE", "VARIANCE", "ZODI", "FLAGS"]:
        t0 = time.perf_counter()
        h = hdul[name]
        hh = summ(take()); hh["t"] = round(time.perf_counter() - t0, 2)
        t0 = time.perf_counter()
        a = h.section[y0:y0 + n, x0:x0 + n]
        s = summ(take()); s["t"] = round(time.perf_counter() - t0, 2)
        out[name] = dict(hdr_access=hh, window=s, shape=a.shape, dtype=str(a.dtype),
                         nbytes_window=int(a.nbytes), mean=float(np.nanmean(a)),
                         hdu_nbytes_raw=int(h.header.get("NAXIS1", 0) * h.header.get("NAXIS2", 0) * abs(h.header.get("BITPIX", 0)) // 8))
        if name == "FLAGS":
            out[name]["zcmptype"] = h.header.get("ZCMPTYPE"); out[name]["ztile"] = (h.header.get("ZTILE1"), h.header.get("ZTILE2"))
    hdul.close()
    return out

if __name__ == "__main__":
    key = sys.argv[1]
    res = []
    for ct, bs in [("readahead", 5 * 2**20), ("none", 5 * 2**20), ("bytes", 64 * 1024)]:
        res.append(run(key, ct, bs))
    print(json.dumps(res, indent=1, default=str))
    json.dump(res, open(sys.argv[2], "w"), indent=1, default=str)
