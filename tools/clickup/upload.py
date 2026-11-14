"""Upload tasks_XX.json to the ClickUp lists of folder 'planet x sphere'.

Usage: python -I upload.py --dry      validate only, no network
       python -I upload.py            create tasks (skips ids already in uploaded.json)
The API key is read from the Desktop file and never printed.
"""
import json
import re
import sys
import time
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
KEYFILE = Path(r"$CLICKUP_TOKEN_FILE")
ALLOWED_TAGS = {"görüntü-işleme", "veri-analizi", "astrometri", "arayüz", "sunucu", "test", "rapor",
                "karar", "demo-5-gün", "sonra", "model-opus", "model-sonnet", "model-haiku",
                "kullanıcı-bakışı", "kişi-a", "kişi-b", "kişi-c", "kişi-d"}
ids = json.loads((HERE / "ids.json").read_text(encoding="utf-8-sig"))
done_file = HERE / "uploaded.json"
done = json.loads(done_file.read_text(encoding="utf-8")) if done_file.exists() else {}


def validate(t, ll):
    errs = []
    for k in ("id", "name", "priority", "tags", "est_hours", "description"):
        if k not in t:
            errs.append(f"missing {k}")
    if errs:
        return errs
    if not re.fullmatch(rf"{ll}-\d\d", t["id"]):
        errs.append("bad id")
    if not t["name"].startswith(f"[{t['id']}]"):
        errs.append("name must start with [id]")
    if t["priority"] not in (1, 2, 3, 4):
        errs.append("priority")
    bad = set(t["tags"]) - ALLOWED_TAGS
    if bad:
        errs.append(f"tags {bad}")
    if sum(x.startswith("model-") for x in t["tags"]) != 1:
        errs.append("need exactly one model-* tag")
    if not (0.25 <= float(t["est_hours"]) <= 8):
        errs.append("est_hours")
    if len(t["description"]) < 300:
        errs.append("description too short")
    return errs


tasks = []
problems = 0
for ll in sorted(ids["lists"]):
    f = HERE / f"tasks_{ll}.json"
    if not f.exists():
        print(f"MISSING {f.name}")
        continue
    arr = json.loads(f.read_text(encoding="utf-8-sig"))
    seen = set()
    for t in arr:
        e = validate(t, ll)
        if t.get("id") in seen:
            e.append("duplicate id")
        seen.add(t.get("id"))
        if e:
            problems += 1
            print("PROBLEM", t.get("id"), e)
        tasks.append((ll, t))
    print(f"list {ll}: {len(arr)} tasks")
print(f"total {len(tasks)} tasks, {problems} problems")

if "--dry" in sys.argv:
    sys.exit(0 if problems == 0 else 1)
if problems:
    print("fix problems first")
    sys.exit(1)

key = re.search(r"pk_\d+_[A-Za-z0-9]+", KEYFILE.read_text(encoding="utf-8-sig")).group(0)
H = {"Authorization": key, "Content-Type": "application/json"}
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

S = requests.Session()
# Retry only failures that happen before the request is sent (connect/handshake resets); never re-send after a read error.
S.mount("https://", HTTPAdapter(max_retries=Retry(total=8, connect=8, read=0, status=0, backoff_factor=1.5, allowed_methods=None)))
created = 0

# Reconcile: pick up tasks that already exist on the server (e.g. a request whose reply was lost).
for ll in sorted({ll for ll, _ in tasks}):
    page = 0
    server = {}
    while True:
        rr = S.get(f"https://api.clickup.com/api/v2/list/{ids['lists'][ll]}/task",
                          headers=H, params={"page": page, "include_closed": "true"}, timeout=60)
        rr.raise_for_status()
        ts = rr.json().get("tasks", [])
        for x in ts:
            server[x["name"]] = x["id"]
        if len(ts) < 100:
            break
        page += 1
    for l2, t in tasks:
        if l2 == ll and t["id"] not in done and t["name"] in server:
            done[t["id"]] = server[t["name"]]
            print("reconciled existing", t["id"])
done_file.write_text(json.dumps(done, ensure_ascii=False, indent=1), encoding="utf-8")

for ll, t in tasks:
    if t["id"] in done:
        continue
    body = {
        "name": t["name"],
        "markdown_description": t["description"],
        "priority": t["priority"],
        "tags": t["tags"],
        "time_estimate": int(float(t["est_hours"]) * 3600 * 1000),
    }
    def existing_id(list_id, name):
        """Return the id of a task with this exact name already in the list (avoids duplicates after a dropped reply)."""
        page = 0
        while True:
            rr = S.get(f"https://api.clickup.com/api/v2/list/{list_id}/task",
                              headers=H, params={"page": page, "include_closed": "true"}, timeout=60)
            rr.raise_for_status()
            ts = rr.json().get("tasks", [])
            for x in ts:
                if x["name"] == name:
                    return x["id"]
            if len(ts) < 100:
                return None
            page += 1

    r = None
    new_id = None
    for attempt in range(5):
        try:
            r = S.post(f"https://api.clickup.com/api/v2/list/{ids['lists'][ll]}/task",
                              headers=H, data=json.dumps(body, ensure_ascii=False).encode("utf-8"), timeout=60)
            if r.status_code == 429:
                time.sleep(15)
                continue
            if r.status_code == 200:
                new_id = r.json()["id"]
            break
        except requests.RequestException as e:
            print(f"net error on {t['id']} (attempt {attempt + 1}): {type(e).__name__}")
            time.sleep(10 * (attempt + 1))
            try:
                found = existing_id(ids["lists"][ll], t["name"])
            except requests.RequestException:
                found = None
            if found:
                new_id = found
                break
    if new_id:
        done[t["id"]] = new_id
        created += 1
        done_file.write_text(json.dumps(done, ensure_ascii=False, indent=1), encoding="utf-8")
    else:
        print("FAIL", t["id"], getattr(r, "status_code", "no response"), (r.text[:200] if r is not None else ""))
    time.sleep(0.8)
print(f"created {created}, total uploaded {len(done)}")
