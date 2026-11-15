"""08-13: Bes hedef karsılastırma tablosu.

Kapsam, zorlanmıs fotometri ve hareket durumunu tek tabloda toplar.
Gercek JSON dosyaları geldiginde load_target() otomatik doldurur;
yoksa 'bekliyor (TAP/H-xx)' gosterir.
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


def print_ascii_table(base_dir: Path | None = None) -> None:
    """Print a fixed-width ASCII comparison table to stdout."""
    assert len(TARGETS) == 5, f"Expected 5 targets, got {len(TARGETS)}"
    if base_dir is None:
        base_dir = Path(r"C:\Users\behlu\reports\targets")
    col_w = [20, 18, 10, 26, 22, 18]
    headers = ["Hedef", "Kareler", "Gecisler", "Kapsam", "Zorlanmis Fotometri", "Hareket"]
    sep = "+" + "+".join("-" * (w + 2) for w in col_w) + "+"
    def row(cells: list[str]) -> str:
        return "| " + " | ".join(c.ljust(col_w[i]) for i, c in enumerate(cells)) + " |"
    print(sep)
    print(row(headers))
    print(sep)
    for t in TARGETS:
        data = load_target(base_dir, t["file"])
        frames = str(t["frames"]) if t["frames"] else "bilinmiyor"
        passes = str(t["passes"]) if t["passes"] else "bilinmiyor"
        cov    = (data.get("coverage_status",   "bekliyor") if data else "bekliyor")[:26]
        phot   = (data.get("forced_phot_status", "bekliyor") if data else "bekliyor")[:22]
        motion = (data.get("motion_status",      "bekliyor") if data else "bekliyor")[:18]
        print(row([t["name"], frames, passes, cov, phot, motion]))
    print(sep)


def main() -> None:
    out_path = Path(__file__).parent / "08-13-comparison.md"
    out_path.write_text(
        "# Bes Hedef Karsılastırma Tablosu\n\n"
        "Kapsam/fotometri/hareket durumu. Gercek veri H-xx ile dolacak.\n\n"
        + build_table() + "\n",
        encoding="utf-8",
    )
    print(f"Yazildi: {out_path}")
    print_ascii_table()


if __name__ == "__main__":
    main()
