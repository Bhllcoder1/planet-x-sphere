"""Read IMAGE-extension headers (S3, anon) for up to 20 frames per target. Output: data/A/headers.json, data/A/frames.json"""
import sys, csv, io, json, re, time, glob, os
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from astropy.io import fits
from astropy.wcs import WCS
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
D = r"stage0\data\A"
GAP = 30.0
KEYS = ["CTYPE1", "CTYPE2", "A_ORDER", "B_ORDER", "AP_ORDER", "BP_ORDER", "FINAST", "RADESYS", "EQUINOX",
        "MJD-AVG", "XPOSURE", "DETECTOR", "CRVAL1", "CRVAL2"]

def load(target):
    p = os.path.join(D, f"tap_{target}.csv")
    if not os.path.exists(p):
        return None
    rows = list(csv.DictReader(open(p, encoding="utf-8")))
    seen, out = set(), []
    for r in rows:
        if r["uri"] in seen:
            continue
        seen.add(r["uri"])
        m = re.match(r"ibe/data/spherex/([^/]+)/([^/]+)/([^/]+)/([^/]+)/(\d+)/", r["uri"])
        r["collection"] = m.group(1) if m else "?"
        r["level"] = m.group(2) if m else "?"
        r["week"] = m.group(3) if m else "?"
        r["procver"] = m.group(4) if m else "?"
        r["det"] = int(m.group(5)) if m else -1
        r["mjd"] = 0.5 * (float(r["time_bounds_lower"]) + float(r["time_bounds_upper"]))
        out.append(r)
    return out

def passes(frames):
    ms = sorted(set(f["mjd"] for f in frames))
    cid, c = {}, 0
    for i, m in enumerate(ms):
        if i and m - ms[i - 1] > GAP:
            c += 1
        cid[m] = c
    for f in frames:
        f["pass"] = cid[f["mjd"]]

def pick(frames, n=20):
    groups = {}
    for f in sorted(frames, key=lambda f: f["mjd"]):
        groups.setdefault((f["pass"], f["det"]), []).append(f)
    keys = sorted(groups)
    chosen, i = [], 0
    while len(chosen) < min(n, len(frames)):
        for k in keys:
            if i < len(groups[k]) and len(chosen) < n:
                chosen.append(groups[k][i])
        i += 1
    return chosen

def rolls(h):
    w = WCS(h)
    nx, ny = h.get("NAXIS1", 2040), h.get("NAXIS2", 2040)
    cx, cy = (nx - 1) / 2, (ny - 1) / 2
    d = 50.0
    pts = np.array([[cx, cy], [cx + d, cy], [cx, cy + d]])
    ra, dec = w.all_pix2world(pts[:, 0], pts[:, 1], 0)
    def pa(i):
        dra = ((ra[i] - ra[0] + 180) % 360 - 180) * np.cos(np.radians(dec[0]))
        return np.degrees(np.arctan2(dra, dec[i] - dec[0])) % 360
    return pa(2), pa(1)  # PA (E of N) of +y and +x pixel axes

def read(f):
    key = "nasa-irsa-spherex/" + f["uri"][len("ibe/data/spherex/"):]
    last = None
    for i in range(3):
        try:
            with fits.open("s3://" + key, fsspec_kwargs={"anon": True}, lazy_load_hdus=True) as hl:
                names = [x.name for x in hl]
                hi = hl["IMAGE"].header.copy()
                hp = hl[0].header.copy()
            res = {"uri": f["uri"], "hdus": names, "n_img_cards": len(hi)}
            for k in KEYS:
                res["IMG_" + k] = hi.get(k)
                res["PRI_" + k] = hp.get(k)
            res["pa_like_keys_img"] = {k: str(hi[k]) for k in hi if re.search(r"PA|SURVEY|ROLL|SPS", k)}
            res["pa_like_keys_pri"] = {k: str(hp[k]) for k in hp if re.search(r"PA|SURVEY|ROLL|SPS", k)}
            res["has_pc"] = [k for k in hi if k.startswith(("PC", "CD"))][:8]
            res["has_A"] = [k for k in hi if k.startswith(("A_", "B_", "AP_", "BP_"))][:10]
            pay, pax = rolls(hi)
            res["pa_y"], res["pa_x"] = float(pay), float(pax)
            return res
        except Exception as e:
            last = f"{type(e).__name__}: {str(e)[:200]}"
            time.sleep(2 * 2 ** i)
    return {"uri": f["uri"], "error": last}

if __name__ == "__main__":
    frames_out, hdr_out = {}, {}
    for t in sys.argv[1:] or ["Barnard", "EpsInd_A", "EpsInd_B", "WISE0855", "RWAur", "RDra"]:
        fr = load(t)
        if fr is None:
            print(t, "no TAP file"); continue
        sci = [f for f in fr if f["producttype"] == "science"]
        passes(sci)
        frames_out[t] = {"all_rows": len(fr), "science": sci}
        ch = pick(sci)
        print(t, len(fr), "rows;", len(sci), "science frames;", len(ch), "headers to read", flush=True)
        with ThreadPoolExecutor(4) as ex:
            hdr_out[t] = list(ex.map(read, ch))
        for r, f in zip(hdr_out[t], ch):
            r["pass"], r["det"], r["mjd"], r["collection"] = f["pass"], f["det"], f["mjd"], f["collection"]
            r["procver"] = f["procver"]
        print(t, "errors:", sum("error" in r for r in hdr_out[t]), flush=True)
        json.dump(frames_out[t], open(os.path.join(D, f"frames_{t}.json"), "w"), indent=1)
        json.dump(hdr_out[t], open(os.path.join(D, f"headers_{t}.json"), "w"), indent=1)
