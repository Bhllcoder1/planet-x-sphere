import json, sys
for r in json.load(open(sys.argv[1])):
    print("CACHE", r["cache"], r["block"], "filesize", r["filesize"], "open", r["open"])
    for n in ["IMAGE", "VARIANCE", "ZODI", "FLAGS"]:
        d = r[n]
        print("  ", n, "hdr", d["hdr_access"], "win", d["window"], "window_bytes", d["nbytes_window"], "mean", d["mean"])
