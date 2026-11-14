import json, time, requests
B = r"stage0\data\B"
res = json.load(open(B + r"\cut_lat.json"))
s = requests.Session(); out = []
for r in res:
    if r["status"] == 200:
        continue
    print("first attempt body:", requests.get.__name__, r["status"], r["bytes"], flush=True)
    time.sleep(45)
    t = time.perf_counter()
    q = s.get(r["url"], timeout=300)
    dt = time.perf_counter() - t
    print("retry", r["file"], r["tag"], q.status_code, len(q.content), round(dt, 2), q.content[:60] if q.status_code != 200 else "", flush=True)
    if q.status_code == 200:
        open(r["fn"], "wb").write(q.content)
    out.append(dict(file=r["file"], tag=r["tag"], status=q.status_code, t=dt, bytes=len(q.content)))
json.dump(out, open(B + r"\cut_retry.json", "w"), indent=1)
