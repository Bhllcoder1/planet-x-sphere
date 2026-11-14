"""Build s0_A.md from data/A/frames_*.json and headers_*.json (whatever exists)."""
import json, os, glob, collections, statistics as st
import numpy as np
D = r"stage0\data\A"
OUT = r"stage0\s0_A.md"
TARGETS = ["Barnard", "EpsInd_A", "EpsInd_B", "WISE0855", "RWAur", "RDra"]
L = ["# Stage 0 test A: coverage, headers, roll (real data)", "",
     "Scripts: stage0\\scripts\\a1_resolve.py, a1b_epsindB.py (positions), a2_tap.py (TAP), a4_headers.py (S3 headers), a5_report.py (this file).",
     "Raw: stage0\\data\\A\\tap_*.csv, frames_*.json, headers_*.json.", "",
     "Method notes: SIMBAD was unreachable (cds.unistra.fr 404 page) so positions come from Sesame (SkyCoord.from_name, other server) + Gaia DR3 (epoch 2016, pm) [VERIFIED by this run: a1_resolve.py, a1b_epsindB.py]. "
     "WISE 0855 position was taken from the task (pm -8118,+680 mas/yr assumed from literature, NOT VERIFIED here). Query point = position propagated to 2026.0. "
     "IRSA TAP rejects INTERSECTS(CIRCLE,poly) and OR of CONTAINS (BAD_REQUEST), so ONE CONTAINS(POINT,poly) per target is used, not a 0.1 deg radius [VERIFIED: a2_tap.py log]. "
     "Footprints are ~3.5 deg wide, so the point-vs-0.1deg difference only matters at frame edges (not tested). Detector = directory digit in the uri; no detector column exists in spherex.plane [VERIFIED: a0_schema.py]. "
     "MJD = mid of time_bounds_lower/upper. Pass = MJD cluster, gap > 30 d.", ""]
summary = {}
summary_w = {}
for t in TARGETS:
    fp = os.path.join(D, f"frames_{t}.json")
    L.append(f"## {t}")
    if not os.path.exists(fp):
        L += ["NOT COMPLETED: IRSA TAP query for this target failed (sync: read timeouts at 400 s, HTTP 502 Proxy Error, connection reset; async submit also 502; a TOP-5 variant also 502/timeout/reset) after several retries over >60 min [VERIFIED: data/a2_log*.txt, a2_retry_*.txt, a2b_*.txt, a2d_top.py output]. Frame count UNKNOWN [NOT VERIFIED]; absence of frames is NOT implied.", ""]; continue
    F = json.load(open(fp)); sci = F["science"]
    L.append(f"TAP rows {F['all_rows']}, science frames {len(sci)} [VERIFIED by this run: a2_tap.py]")
    if not sci:
        L += ["**0 frames** cover this target [VERIFIED: a2_tap.py].", ""]; continue
    dets = sorted(set(f["det"] for f in sci))
    L += ["", "Frames per release/collection x detector (provenance_version in brackets):", "",
          "| collection | procver | " + " | ".join(f"D{d}" for d in dets) + " | total |", "|---|---|" + "---|" * (len(dets) + 1)]
    g = collections.Counter((f["collection"], f["procver"], f["det"]) for f in sci)
    for (c, v) in sorted(set((f["collection"], f["procver"]) for f in sci)):
        row = [g[(c, v, d)] for d in dets]
        L.append(f"| {c} | {v} | " + " | ".join(map(str, row)) + f" | {sum(row)} |")
    pv = collections.Counter(f["provenance_version"] for f in sci)
    L.append(""); L.append(f"provenance_version (pipeline): {dict(pv)}")
    L += ["", "Passes (gap > 30 d):", "", "| pass | MJD min | MJD max | n | " + " | ".join(f"D{d}" for d in dets) + " |", "|---|---|---|---|" + "---|" * len(dets)]
    npass = max(f["pass"] for f in sci) + 1
    for p in range(npass):
        fs = [f for f in sci if f["pass"] == p]
        c = collections.Counter(f["det"] for f in fs)
        L.append(f"| {p} | {min(f['mjd'] for f in fs):.2f} | {max(f['mjd'] for f in fs):.2f} | {len(fs)} | " + " | ".join(str(c[d]) for d in dets) + " |")
    L.append(f"\nEpochs (passes): **{npass}**")
    hp = os.path.join(D, f"headers_{t}.json")
    if not os.path.exists(hp):
        L += ["Headers: NOT COMPLETED", ""]; continue
    h2p = os.path.join(D, f"headers2_{t}.json")
    H = json.load(open(hp)); ok = [h for h in H if "error" not in h]; bad = [h for h in H if "error" in h]
    L += ["", f"### Headers ({len(ok)} read ok, {len(bad)} failed)"]
    for h in bad: L.append(f"- FAILED {h['uri']}: {h['error']}")
    if not ok: L.append(""); continue
    sip = [h for h in ok if str(h.get("IMG_CTYPE1", "")).endswith("-SIP")]
    L.append(f"- CTYPE1 values: {dict(collections.Counter(h['IMG_CTYPE1'] for h in ok))}; CTYPE2: {dict(collections.Counter(h['IMG_CTYPE2'] for h in ok))}")
    L.append(f"- '-SIP' in IMAGE CTYPE: {len(sip)}/{len(ok)}; A_ORDER: {dict(collections.Counter(h['IMG_A_ORDER'] for h in ok))}; B_ORDER: {dict(collections.Counter(h['IMG_B_ORDER'] for h in ok))}; AP_ORDER: {dict(collections.Counter(h['IMG_AP_ORDER'] for h in ok))}")
    L.append(f"- FINAST: {dict(collections.Counter(h['IMG_FINAST'] if h['IMG_FINAST'] is not None else h['PRI_FINAST'] for h in ok))} (IMAGE hdr / else primary); RADESYS {dict(collections.Counter(h['IMG_RADESYS'] or h['PRI_RADESYS'] for h in ok))}; EQUINOX {dict(collections.Counter(h['IMG_EQUINOX'] or h['PRI_EQUINOX'] for h in ok))}")
    xp = [h['IMG_XPOSURE'] if h['IMG_XPOSURE'] is not None else h['PRI_XPOSURE'] for h in ok]; xp = [x for x in xp if x is not None]
    L.append(f"- XPOSURE: min {min(xp) if xp else None}, max {max(xp) if xp else None}; MJD-AVG present in IMAGE: {sum(h['IMG_MJD-AVG'] is not None for h in ok)}, in primary: {sum(h['PRI_MJD-AVG'] is not None for h in ok)}")
    L.append(f"- PA/survey-like keyword names in IMAGE: {sorted(set(k for h in ok for k in h['pa_like_keys_img']))}; SPS_EPA values by pass: " + str({p: dict(collections.Counter(h['pa_like_keys_img'].get('SPS_EPA') for h in ok if h['pass'] == p)) for p in sorted(set(h['pass'] for h in ok))}))
    L.append("- NOTE: keyword SPS_PA_ECL does NOT exist in these headers if absent from the list above; the actual name is SPS_EPA.")
    L.append(f"- PA/survey-like keywords, primary (first 3 distinct): {list(dict(collections.Counter(json.dumps(h['pa_like_keys_pri'], sort_keys=True) for h in ok)).items())[:3]}")
    L.append(f"- HDUs: {ok[0]['hdus']}; PC/CD keys: {ok[0]['has_pc']}; SIP keys: {ok[0]['has_A']}")
    L += ["", "Roll = position angle (deg E of N) of the image +y axis from WCS (astropy all_pix2world incl. SIP, 50 px step at centre):", "",
          "| pass | det | n | pa_y min | pa_y max | spread | std |", "|---|---|---|---|---|---|---|"]
    gp = collections.defaultdict(list)
    for h in ok: gp[(h["pass"], h["det"])].append(h["pa_y"])
    def spread(a):  # circular-safe spread
        a = np.array(a); c = np.angle(np.exp(1j*np.radians(a)).mean(), deg=True)
        d = (a - c + 180) % 360 - 180; return d.min() + c, d.max() + c, d.max() - d.min(), float(d.std())
    mx = 0
    for (p, d), a in sorted(gp.items()):
        lo, hi, sp, sd = spread(a); mx = max(mx, sp)
        L.append(f"| {p} | D{d} | {len(a)} | {lo%360:.3f} | {hi%360:.3f} | {sp:.3f} | {sd:.3f} |")
    L.append(f"\nMax within-(pass,detector) spread: **{mx:.3f} deg**")
    pm = {}
    for p in sorted(set(k[0] for k in gp)):
        a = [h["pa_y"] for h in ok if h["pass"] == p]
        pm[p] = float(np.angle(np.exp(1j*np.radians(a)).mean(), deg=True) % 360)
        L.append(f"- pass {p} (all detectors) mean pa_y {pm[p]:.3f}, spread {spread(a)[2]:.3f}, std {spread(a)[3]:.3f}, n={len(a)}")
    ps = sorted(pm)
    for i in range(len(ps)):
        for j in range(i+1, len(ps)):
            dd = (pm[ps[j]] - pm[ps[i]] + 180) % 360 - 180
            L.append(f"- pass {ps[i]} vs {ps[j]}: mean difference {dd:.3f} deg (|diff| - 180 = {abs(dd)-180:.3f})")
    # fold by 180 deg so a 0/180 flip does not hide the intra-survey spread
    bycol = collections.defaultdict(list)
    for h in ok: bycol[h["collection"]].append(h["pa_y"] % 180)
    L.append("- per collection, pa_y folded mod 180 (removes the PA flip): " + ", ".join(f"{c}: min {min(a):.2f} max {max(a):.2f} (n={len(a)})" for c, a in bycol.items()))
    h2p = os.path.join(D, f"headers2_{t}.json")
    if os.path.exists(h2p):
        H2 = [h for h in json.load(open(h2p)) if "error" not in h]
        L += ["", f"Within-pass test (extra reads, one detector D{H2[0]['det'] if H2 else '?'}, up to 6 frames/pass spread in MJD; n={len(H2)}):", "", "| pass | n | MJD span (d) | pa_y min | pa_y max | spread | std | SPS_EPA | collections |", "|---|---|---|---|---|---|---|---|---|"]
        for p in sorted(set(h["pass"] for h in H2)):
            g = [h for h in H2 if h["pass"] == p]; a = [h["pa_y"] for h in g]; lo, hi, sp, sd = spread(a)
            L.append(f"| {p} | {len(g)} | {max(h['mjd'] for h in g)-min(h['mjd'] for h in g):.1f} | {lo%360:.3f} | {hi%360:.3f} | {sp:.3f} | {sd:.3f} | {sorted(set(h['pa_like_keys_img'].get('SPS_EPA') for h in g))} | {sorted(set(h['collection'] for h in g))} |")
            summary_w.setdefault(t, []).append(sp)
        mm = {p: float(np.angle(np.exp(1j*np.radians([h['pa_y'] for h in H2 if h['pass']==p])).mean(), deg=True) % 360) for p in sorted(set(h['pass'] for h in H2))}
        pl = sorted(mm)
        for i in range(len(pl)):
            for j in range(i+1, len(pl)):
                dd = (mm[pl[j]] - mm[pl[i]] + 180) % 360 - 180
                L.append(f"- (same detector) pass {pl[i]} vs {pl[j]}: {dd:.3f} deg; deviation from exactly 180: {abs(abs(dd)-180):.3f} deg")
    # per-detector comparison between passes, using ALL header reads (diverse set + within-pass extension), dedup by uri
    allh = {h["uri"]: h for h in ok}
    if os.path.exists(h2p):
        for h in H2: allh[h["uri"]] = h
    cell = collections.defaultdict(list)
    for h in allh.values(): cell[(h["pass"], h["det"])].append(h["pa_y"])
    cm = {k: float(np.angle(np.exp(1j*np.radians(v)).mean(), deg=True) % 360) for k, v in cell.items()}
    L += ["", f"Per-detector pass-to-pass comparison (mean pa_y per cell; n = header-read frames in the cell; {len(allh)} distinct frames):", "",
          "| det | pass A (n, mean) | pass B (n, mean) | SPS_EPA A/B | diff B-A | diff mod 360 minus 180 (opposite) / diff (same orientation) |", "|---|---|---|---|---|---|"]
    epa = {}
    for h in allh.values(): epa.setdefault(h["pass"], set()).add(h["pa_like_keys_img"].get("SPS_EPA"))
    for d in sorted(set(k[1] for k in cell)):
        ps_ = sorted(p for (p, dd) in cell if dd == d)
        for i in range(len(ps_)):
            for j in range(i+1, len(ps_)):
                a, b = ps_[i], ps_[j]
                dd_ = (cm[(b, d)] - cm[(a, d)] + 180) % 360 - 180
                opp = abs(dd_) > 90
                resid = (abs(dd_) - 180) if opp else dd_
                L.append(f"| D{d} | {a} (n={len(cell[(a,d)])}, {cm[(a,d)]:.3f}) | {b} (n={len(cell[(b,d)])}, {cm[(b,d)]:.3f}) | {sorted(epa[a])}/{sorted(epa[b])} | {dd_:.3f} | {'opposite: ' if opp else 'same: '}{resid:+.3f} |")
    span = [(p, min(f['mjd'] for f in sci if f['pass']==p), max(f['mjd'] for f in sci if f['pass']==p)) for p in range(npass)]
    L += ["", "Pass duration (days, MJD-mid min to max of ALL TAP frames): " + ", ".join(f"pass {p}: {b-a:.1f} d ({a:.1f}-{b:.1f})" for p, a, b in span), ""]
    summary[t] =(len(sci), npass, len(sip), len(ok), mx)
L += ["## Plan questions", ""]
for t, (n, npass, s, o, mx) in summary.items():
    L.append(f"- {t}: {n} frames, {npass} passes, SIP {s}/{o}, max within pass/detector roll spread in 20-frame set {mx:.3f} deg (n/detector/pass is 1-2: weak); within-pass extension spreads per pass: {[round(float(x),3) for x in summary_w.get(t, [])]}")
open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
print("\n".join(L))
