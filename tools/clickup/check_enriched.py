"""Count, per list, how many tasks have the enriched sections, and flag URLs that are not in SOURCE_MAP.md."""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
smap = (HERE / "SOURCE_MAP.md").read_text(encoding="utf-8")
allowed = set(re.findall(r"https?://[^\s|)>\]]+", smap))
allowed = {u.rstrip(".,;") for u in allowed}
need = ["ARKA PLAN", "DİKKAT EDİLECEKLER", "KAYNAKLAR", "KABUL", "KANIT"]
tot_e = tot = 0
for f in sorted(HERE.glob("tasks_[0-9][0-9].json")):
    ll = f.stem.split("_")[1]
    cur = json.loads(f.read_text(encoding="utf-8-sig"))
    orig_f = HERE / f"tasks_{ll}.orig.json"
    n_orig = len(json.loads(orig_f.read_text(encoding="utf-8-sig"))) if orig_f.exists() else len(cur)
    enriched, missing, badurl = [], [], []
    for t in cur:
        d = t["description"]
        if all(k in d for k in need):
            enriched.append(t["id"])
            kay = d.split("KAYNAKLAR", 1)[1]
            for u in re.findall(r"https?://[^\s|)>\]]+", kay):
                u = u.rstrip(".,;*")
                if u not in allowed:
                    badurl.append((t["id"], u))
        else:
            missing.append(t["id"])
    tot_e += len(enriched)
    tot += len(cur)
    print(f"list {ll}: tasks {len(cur)} (orig {n_orig}), enriched {len(enriched)}, not enriched {len(missing)}"
          + (f" -> {','.join(missing)}" if missing and len(missing) < 15 else ""))
    for tid, u in badurl:
        print(f"   URL not in SOURCE_MAP: {tid} {u}")
print(f"TOTAL enriched {tot_e} of {tot}")
