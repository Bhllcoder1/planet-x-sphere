"""Create the area tags kişi-a..kişi-d in the ClickUp space and put the right one on every task (resumable).
The API key is read from the Desktop file and never printed."""
import json
import re
import sys
import time
import urllib.parse
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
ids = json.loads((HERE / "ids.json").read_text(encoding="utf-8-sig"))
uploaded = json.loads((HERE / "uploaded.json").read_text(encoding="utf-8-sig"))
assign = json.loads((HERE / "_gen" / "assignment_balanced.json").read_text(encoding="utf-8"))
state_file = HERE / "roles_applied.json"
state = json.loads(state_file.read_text(encoding="utf-8")) if state_file.exists() else {}
TAG = {"A": "kişi-a", "B": "kişi-b", "C": "kişi-c", "D": "kişi-d"}

key = re.search(r"pk_\d+_[A-Za-z0-9]+", Path(r"$CLICKUP_TOKEN_FILE").read_text(encoding="utf-8-sig")).group(0)
S = requests.Session()
S.mount("https://", HTTPAdapter(max_retries=Retry(total=8, connect=8, read=0, status=0, backoff_factor=1.5, allowed_methods=None)))
H = {"Authorization": key, "Content-Type": "application/json"}

for a, name in TAG.items():
    body = {"tag": {"name": name, "tag_fg": "#ffffff", "tag_bg": {"A": "#2e7d32", "B": "#1565c0", "C": "#ef6c00", "D": "#6a1b9a"}[a]}}
    r = S.post(f"https://api.clickup.com/api/v2/space/{ids['space']}/tag", headers=H,
               data=json.dumps(body, ensure_ascii=False).encode("utf-8"), timeout=60)
    print("tag", name, r.status_code)
    time.sleep(0.4)

ok = fail = 0
for tid, tcid in uploaded.items():
    want = TAG[assign[tid]]
    if state.get(tid) == want:
        continue
    old = state.get(tid)
    if old and old != want:  # moved to another area: remove the previous letter first
        try:
            S.delete(f"https://api.clickup.com/api/v2/task/{tcid}/tag/{urllib.parse.quote(old)}", headers=H, timeout=60)
        except requests.RequestException as e:
            print("net error removing old tag", tid, type(e).__name__)
        time.sleep(0.4)
    for attempt in range(5):
        try:
            r = S.post(f"https://api.clickup.com/api/v2/task/{tcid}/tag/{urllib.parse.quote(want)}", headers=H, timeout=60)
            if r.status_code == 429:
                time.sleep(15)
                continue
            break
        except requests.RequestException as e:
            print("net error", tid, type(e).__name__)
            time.sleep(8 * (attempt + 1))
            r = None
    if r is not None and r.status_code == 200:
        state[tid] = want
        ok += 1
        state_file.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
    else:
        fail += 1
        print("FAIL", tid, getattr(r, "status_code", "no response"), (r.text[:120] if r is not None else ""))
    time.sleep(0.6)
print(f"tagged {ok}, failed {fail}, total with role tag {len(state)}")
