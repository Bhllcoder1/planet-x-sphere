import json
import numpy as np
B = r"stage0\data\B"
r = json.load(open(B + r"\lat_ra1m.json"))
def pc(a):
    a = np.array(a); return f"n={len(a)} p50={np.percentile(a,50):.2f}s p95={np.percentile(a,95):.2f}s min={a.min():.2f} max={a.max():.2f} mean={a.mean():.2f}"
fr = [x["t"] for x in r if x["kind"] == "frame"]
print("S3 readahead 1 MiB: frame-window (IMAGE+VARIANCE+ZODI+FLAGS, 100x100) latency:", pc(fr))
print("  excluding first window of each file:", pc([x["t"] for x in r if x["kind"] == "frame" and x["win"] > 0]))
for n in ["IMAGE", "VARIANCE", "ZODI", "FLAGS"]:
    h = [x for x in r if x["kind"] == "hdu" and x["hdu"] == n]
    print(" ", n, pc([x["t"] for x in h]), "| GETs/window mean", np.mean([x["n_get"] for x in h]), "bytes/window mean", int(np.mean([x["bytes"] for x in h])), "max", max(x["bytes"] for x in h))
op = [x for x in r if x["kind"] == "open"]
print("  open+4 header reads per file:", [(round(x["t"], 1), x["n_get"], x["bytes"]) for x in op], pc([x["t"] for x in op]))
tot = sum(x["bytes"] for x in r if x["kind"] in ("hdu", "open"))
print("  total bytes on wire (30 frame-windows + 5 opens):", tot, " per frame-window (hdu only):", int(np.mean([sum(y["bytes"] for y in r if y["kind"] == "hdu" and y["file"] == x["file"] and y["win"] == x["win"]) for x in r if x["kind"] == "frame"])))
c = json.load(open(B + r"\cut_lat.json")); c2 = json.load(open(B + r"\cut_retry.json"))
ok = [(x["t"], x["bytes"]) for x in c if x["status"] == 200]
ok += [(x["t"], x["bytes"]) for x in c2 if x["status"] == 200]
print("cutouts: requests total", len(c) + len(c2), "HTTP 200:", len(ok), "HTTP 503:", sum(1 for x in c + c2 if x["status"] == 503))
print("  latency of 200s", pc([a for a, b in ok]), " bytes", sorted(set(b for a, b in ok)))
print("  all request times incl 503:", pc([x["t"] for x in c + c2]))
