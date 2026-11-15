"""08-13: Bes hedef karsılastırma tablosu.
[PARTIAL] — gercek veri H-xx gerekiyor.
"""
from __future__ import annotations
import json
from pathlib import Path

TARGETS = [
    {"name": "Barnard Yildizi", "frames": 358, "passes": 3,  "file": "barnard.json"},
    {"name": "eps Indi B",      "frames": 458, "passes": 4,  "file": "epsilon_indi.json"},
    {"name": "WISE 0855",       "frames": None, "passes": None, "file": "wise0855.json"},
    {"name": "RW Aurigae",      "frames": None, "passes": None, "file": "rw_aur.json"},
    {"name": "R Draconis",      "frames": None, "passes": None, "file": "r_dra.json"},
]


def load_target(base_dir: Path, filename: str) -> dict | None:
    p = base_dir / filename
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def build_table(base_dir: Path | None = None) -> str:
    if base_dir is None:
        base_dir = Path(r"C:\Users\behlu\reports\targets")
    lines = [
        "| Hedef | Kareler | Gecisler | Kapsam | Zorlanmis Fotometri | Hareket |",
        "|---|---|---|---|---|---|",
    ]
    for t in TARGETS:
        data = load_target(base_dir, t["file"])
        frames = str(t["frames"]) if t["frames"] else "bilinmiyor (TAP basarisiz)"
        passes = str(t["passes"]) if t["passes"] else "bilinmiyor"
        cov   = data.get("coverage_status",   "bekliyor") if data else "bekliyor (H-xx)"
        phot  = data.get("forced_phot_status", "bekliyor") if data else "bekliyor (H-xx)"
        motion = data.get("motion_status",    "bekliyor") if data else "bekliyor (H-xx)"
        lines.append(
            f"| {t['name']} | {frames} | {passes} | {cov} | {phot} | {motion} |"
        )
    return "\n".join(lines)


def main() -> None:
    out_path = Path(__file__).parent / "08-13-comparison.md"
    out_path.write_text(
        f"# Bes Hedef Karsılastırma Tablosu\n\n"
        f"[PARTIAL] H-xx bekleniyor.\n\n"
        f"{build_table()}\n",
        encoding="utf-8",
    )
    print(f"Yazildi: {out_path}")


if __name__ == "__main__":
    main()
