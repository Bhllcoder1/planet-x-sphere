"""Set up the NEW workspace: backup old id/state files, create 12 lists and 18 tags, write ids.json for the new workspace."""
import json
import re
import shutil
import sys
import time
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
key = re.search(r"pk_\d+_[A-Za-z0-9]+", Path(r"$CLICKUP_TOKEN_FILE").read_text(encoding="utf-8-sig")).group(0)
S = requests.Session()
S.mount("https://", HTTPAdapter(max_retries=Retry(total=8, connect=8, read=0, status=0, backoff_factor=1.5, allowed_methods=None)))
H = {"Authorization": key, "Content-Type": "application/json"}
API = "https://api.clickup.com/api/v2"


def get(path):
    r = S.get(API + path, headers=H, timeout=60)
    r.raise_for_status()
    return r.json()


def post(path, body):
    return S.post(API + path, headers=H, data=json.dumps(body, ensure_ascii=False).encode("utf-8"), timeout=60)


teams = get("/team")["teams"]
assert len(teams) == 1, f"expected exactly one workspace, got {len(teams)}"
team = teams[0]
print("workspace:", team["id"], team["name"])
spaces = get(f"/team/{team['id']}/space?archived=false")["spaces"]
print("spaces:", [(s["name"], s["id"]) for s in spaces])
space = spaces[0]
feat = space.get("features", {})
print("using space:", space["name"], space["id"], "| features:", {k: (v or {}).get("enabled") for k, v in feat.items()})
existing = get(f"/space/{space['id']}/list?archived=false")["lists"]
print("existing folderless lists:", [(x["name"], x["task_count"]) for x in existing])

# backup the state of the old (YAZGIT) workspace
for n in ("ids.json", "uploaded.json", "updated.json", "roles_applied.json"):
    p = HERE / n
    b = HERE / n.replace(".json", "_yazgit.json")
    if p.exists() and not b.exists():
        shutil.copy2(p, b)
        print("backed up", n)

NAMES = {
    "00": "00 Kararlar, Kapsam ve Riskler", "01": "01 Veri Erişimi ve Ortam (Stage 0)", "02": "02 Görüntü İşleme Hattı",
    "03": "03 Konum, Merkezleme ve Astrometri", "04": "04 Veri Analizi: Geçişler, Hareket ve Değişenler",
    "05": "05 Görüntüleyici ve Arayüz", "06": "06 Sunucu, Kiralama ve Yayın", "07": "07 Testler ve Doğrulama",
    "08": "08 Hedef Raporları (5 Yarışma Hedefi)", "09": "09 Sunum, Dokümantasyon ve Dürüstlük Raporu",
    "10": "10 Site İçeriği ve Gereksinimleri", "11": "11 Kullanıcılar, Geçmiş, Çıktılar ve UI/UX",
}
have = {x["name"]: x["id"] for x in existing}
lists = {}
for k, name in NAMES.items():
    if name in have:
        lists[k] = have[name]
        continue
    r = post(f"/space/{space['id']}/list", {"name": name})
    r.raise_for_status()
    lists[k] = r.json()["id"]
    print("list", k, lists[k])
    time.sleep(0.4)

TAGS = {"görüntü-işleme": "#1565c0", "veri-analizi": "#1565c0", "astrometri": "#1565c0", "arayüz": "#6a1b9a", "sunucu": "#ef6c00",
        "test": "#455a64", "rapor": "#455a64", "karar": "#455a64", "demo-5-gün": "#c62828", "sonra": "#9e9e9e",
        "model-opus": "#ad1457", "model-sonnet": "#00838f", "model-haiku": "#558b2f", "kullanıcı-bakışı": "#f9a825",
        "kişi-a": "#2e7d32", "kişi-b": "#1565c0", "kişi-c": "#ef6c00", "kişi-d": "#6a1b9a"}
for name, bg in TAGS.items():
    r = post(f"/space/{space['id']}/tag", {"tag": {"name": name, "tag_fg": "#ffffff", "tag_bg": bg}})
    print("tag", name, r.status_code)
    time.sleep(0.3)

ids = {"team": team["id"], "space": space["id"], "folder": None, "lists": lists}
(HERE / "ids.json").write_text(json.dumps(ids, ensure_ascii=False, indent=1), encoding="utf-8")
for n in ("uploaded.json", "updated.json", "roles_applied.json"):
    (HERE / n).write_text("{}", encoding="utf-8")
print("new ids.json written; state files reset")
