"""Update the description of tasks that already exist on ClickUp (ids in uploaded.json) from tasks_XX.json.

Usage: python -I update_desc.py --dry      show how many tasks would change
       python -I update_desc.py            PUT the new markdown_description
Only the description is changed. Skips tasks whose text is already identical (state in updated.json).
The API key is read from the Desktop file and never printed.
"""
import hashlib
import json
import re
import sys
import time
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

HERE = Path(__file__).resolve().parent
KEYFILE = Path(r"$CLICKUP_TOKEN_FILE")
ids = json.loads((HERE / "ids.json").read_text(encoding="utf-8-sig"))
uploaded = json.loads((HERE / "uploaded.json").read_text(encoding="utf-8-sig"))
state_file = HERE / "updated.json"
state = json.loads(state_file.read_text(encoding="utf-8")) if state_file.exists() else {}

todo = []
for ll in sorted(ids["lists"]):
    f = HERE / f"tasks_{ll}.json"
    if not f.exists():
        continue
    for t in json.loads(f.read_text(encoding="utf-8-sig")):
        tid = uploaded.get(t["id"])
        if not tid:
            continue
        if ("--only-enriched" in sys.argv and "ARKA PLAN" not in t["description"]
                and "GÜNCELLEME" not in t["description"]):
            continue
        h = hashlib.sha1(t["description"].encode("utf-8")).hexdigest()
        if state.get(t["id"]) != h:
            todo.append((t, tid, h))
print(f"{len(todo)} tasks to update")
if "--dry" in sys.argv:
    sys.exit(0)

key = re.search(r"pk_\d+_[A-Za-z0-9]+", KEYFILE.read_text(encoding="utf-8-sig")).group(0)
S = requests.Session()
S.mount("https://", HTTPAdapter(max_retries=Retry(total=8, connect=8, read=0, status=0, backoff_factor=1.5, allowed_methods=None)))
H = {"Authorization": key, "Content-Type": "application/json"}
ok = 0
for t, tid, h in todo:
    body = {"markdown_description": t["description"]}
    for attempt in range(5):
        try:
            r = S.put(f"https://api.clickup.com/api/v2/task/{tid}", headers=H,
                      data=json.dumps(body, ensure_ascii=False).encode("utf-8"), timeout=60)
            if r.status_code == 429:
                time.sleep(15)
                continue
            break
        except requests.RequestException as e:
            print(f"net error {t['id']} attempt {attempt + 1}: {type(e).__name__}")
            time.sleep(8 * (attempt + 1))
            r = None
    if r is not None and r.status_code == 200:
        state[t["id"]] = h
        ok += 1
        state_file.write_text(json.dumps(state, indent=1), encoding="utf-8")
    else:
        print("FAIL", t["id"], getattr(r, "status_code", "no response"))
    time.sleep(0.7)
print(f"updated {ok} of {len(todo)}")
