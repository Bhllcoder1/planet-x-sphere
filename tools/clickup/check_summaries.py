"""Independent check of the ÖZET blocks (does not trust the agents' own checks)."""
import json
import random
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
D = Path(__file__).resolve().parent
MARK = "**ÖZET (sade dille)**"
BUL = ["**Ne yapıyoruz:**", "**Neden:**", "**Sana ne düşüyor:**", "**Bitti sayılır:**", "**Alan ve süre:**", "**Kapsam dışı:**"]
ALL_IDS = set()
cur_all, pre_all = {}, {}
for f in sorted(D.glob("tasks_[0-9][0-9].json")):
    ll = f.stem.split("_")[1]
    pre = D / f"tasks_{ll}.pre_summary.json"
    for t in json.loads(f.read_text(encoding="utf-8-sig")):
        cur_all[t["id"]] = t
        ALL_IDS.add(t["id"])
    if pre.exists():
        for t in json.loads(pre.read_text(encoding="utf-8-sig")):
            pre_all[t["id"]] = t

problems = defaultdict = {}
def bad(tid, msg):
    problems.setdefault(tid, []).append(msg)

AREA = {"kişi-a": "A", "kişi-b": "B", "kişi-c": "C", "kişi-d": "D"}
for tid, t in cur_all.items():
    d = t["description"]
    if not d.startswith(MARK):
        bad(tid, "özet bloğu yok")
        continue
    block, _, rest = d.partition("\n---")
    for b in BUL:
        if b not in block:
            bad(tid, f"eksik madde {b}")
    words = len(re.findall(r"\S+", block))
    if words > 125:
        bad(tid, f"blok uzun ({words} kelime)")
    p = pre_all.get(tid)
    if p is None:
        bad(tid, "yedek (pre_summary) yok")
    else:
        for k in ("id", "name", "priority", "tags", "est_hours"):
            if p[k] != t[k]:
                bad(tid, f"{k} değişmiş")
        if rest.lstrip("\n").strip() != p["description"].strip():
            bad(tid, "özetin altındaki metin değişmiş")
    # area letter and hours in the summary must match tags and est_hours
    m = re.search(r"\*\*Alan ve süre:\*\*(.*)", block)
    if m:
        line = m.group(1)
        letter = [AREA[x] for x in t["tags"] if x in AREA]
        if letter and not re.search(rf"\b{letter[0]}\b", line):
            bad(tid, f"alan harfi {letter[0]} özette yok: {line.strip()[:50]}")
        h = float(t["est_hours"])
        hs = {f"{h:g}", f"{h:.0f}", f"{h:.1f}"}
        if not any(x in line for x in hs):
            bad(tid, f"süre {h:g} saat özette yok: {line.strip()[:50]}")
    # task ids mentioned in 'Kapsam dışı' must exist and be mentioned somewhere in the task text
    m2 = re.search(r"\*\*Kapsam dışı:\*\*(.*)", block)
    if m2:
        for ref in re.findall(r"\b\d\d-\d\d\b", m2.group(1)):
            if ref not in ALL_IDS:
                bad(tid, f"Kapsam dışı: var olmayan görev {ref}")
            elif ref != tid and ref not in (rest + t["name"]):
                bad(tid, f"Kapsam dışı: {ref} görev metninde geçmiyor")
    # numbers in KABUL should (mostly) appear in 'Bitti sayılır'
    km = re.search(r"\*\*KABUL:\*\*(.*?)\n\n", rest, re.S)
    bm = re.search(r"\*\*Bitti sayılır:\*\*(.*)", block)
    if km and bm:
        nums = set(re.findall(r"\d+[.,]?\d*(?:e-?\d+)?", km.group(1)))
        nums = {n for n in nums if len(n) >= 2 or "." in n}
        if nums and not any(n in bm.group(1) for n in nums):
            bad(tid, f"KABUL sayıları ({', '.join(sorted(nums)[:4])}) 'Bitti sayılır'da yok")

n = len(cur_all)
ok = n - len(problems)
print(f"{n} görev kontrol edildi; sorunsuz {ok}; sorunlu {len(problems)}")
for tid in sorted(problems):
    print(" ", tid, "|", "; ".join(problems[tid])[:230])

rng = random.Random(5)
print("\n=== rastgele 8 örnek (AMAÇ | Ne yapıyoruz | Kapsam dışı) ===")
for tid in rng.sample(sorted(cur_all), 8):
    d = cur_all[tid]["description"]
    block, _, rest = d.partition("\n---")
    amac = re.search(r"\*\*AMAÇ:\*\*(.*?)\n\n", rest, re.S)
    ne = re.search(r"\*\*Ne yapıyoruz:\*\*(.*)", block)
    kd = re.search(r"\*\*Kapsam dışı:\*\*(.*)", block)
    print(f"\n[{tid}] {cur_all[tid]['name'][len(tid)+3:][:80]}")
    print("  AMAÇ:", (amac.group(1).strip() if amac else "(AMAÇ bölümü yok)")[:230])
    print("  ÖZET:", ne.group(1).strip()[:230] if ne else "?")
    print("  KAPSAM DIŞI:", kd.group(1).strip()[:200] if kd else "?")
