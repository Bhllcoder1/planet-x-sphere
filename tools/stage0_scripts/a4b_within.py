"""Within-(pass,detector) roll test: per target, the detector with most frames; up to 6 frames per pass spread evenly in MJD. Extra reads beyond the 20-frame diverse set."""
import sys, json, os, numpy as np, collections
sys.path.insert(0, r"stage0\scripts")
from concurrent.futures import ThreadPoolExecutor
import a4_headers as A
for t in sys.argv[1:]:
    fr = A.load(t); sci = [f for f in fr if f["producttype"] == "science"]; A.passes(sci)
    cnt = collections.Counter(f["det"] for f in sci); det = cnt.most_common(1)[0][0]
    ch = []
    for p in sorted(set(f["pass"] for f in sci)):
        g = sorted([f for f in sci if f["pass"] == p and f["det"] == det], key=lambda f: f["mjd"])
        idx = sorted(set(np.linspace(0, len(g) - 1, min(6, len(g))).round().astype(int))) if g else []
        ch += [g[i] for i in idx]
    print(t, "det", det, "frames", len(ch), flush=True)
    with ThreadPoolExecutor(4) as ex: res = list(ex.map(A.read, ch))
    for r, f in zip(res, ch): r["pass"], r["det"], r["mjd"], r["collection"], r["procver"] = f["pass"], f["det"], f["mjd"], f["collection"], f["procver"]
    json.dump(res, open(os.path.join(A.D, f"headers2_{t}.json"), "w"), indent=1)
    print(t, "errors", sum("error" in r for r in res), flush=True)
