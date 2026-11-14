"""10 cutout requests (5 files x 2 centres), sequential (1 in flight), size 0.05 deg, gzip=false."""
import json, time, os, sys
import numpy as np
import requests
cands = json.load(open(r"stage0\data\B\cands.json"))
files = [cands[i] for i in (4, 0, 2, 3, 1)]
OUT = r"stage0\data\B\cut"
os.makedirs(OUT, exist_ok=True)
res = []
s = requests.Session()
n = 0
for fi, c in enumerate(files):
    ra, dec = c["ra"], c["dec"]
    cen = {"A": (ra, dec), "B": (ra + 0.012 / np.cos(np.radians(dec)), dec + 0.008)}
    for tag, (r_, d_) in cen.items():
        url = f"https://irsa.ipac.caltech.edu/{c['key'].replace('dr1/', 'ibe/data/spherex/dr1/', 1)}"
        params = {"center": f"{r_:.6f},{d_:.6f}", "size": "0.05", "gzip": "false"}
        t = time.perf_counter(); n += 1
        try:
            r = s.get(url, params=params, timeout=300)
            dt = time.perf_counter() - t
            fn = os.path.join(OUT, f"f{fi}_{tag}.fits")
            if r.status_code == 200:
                open(fn, "wb").write(r.content)
            res.append(dict(file=fi, tag=tag, status=r.status_code, t=dt, bytes=len(r.content), ctype=r.headers.get("content-type"),
                            center=params["center"], url=r.url, fn=fn))
        except Exception as e:
            res.append(dict(file=fi, tag=tag, status="EXC", err=repr(e)[:200], t=time.perf_counter() - t))
        print(res[-1], flush=True)
json.dump(res, open(r"stage0\data\B\cut_lat.json", "w"), indent=1)
print("requests made:", n)
