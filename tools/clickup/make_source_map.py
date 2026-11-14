"""Build clickup/SOURCE_MAP.md from the pages that were really fetched (status 200)."""
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
kb = pathlib.Path(__file__).resolve().parent.parent
rows = []
for d in sorted(kb.glob("sources*")):
    if not d.is_dir():
        continue
    for f in sorted(d.glob("*.md")):
        t = f.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"^source:\s*(\S+)", t, re.M)
        st = re.search(r"^status:\s*(\S+)", t, re.M)
        if not m or (st and st.group(1) != "200"):
            continue
        h = re.search(r"^#\s+(.+)$", t, re.M)
        rows.append((m.group(1), str(f.relative_to(kb)), h.group(1).strip()[:70] if h else ""))

out = [
    "# Source map (only pages that were actually fetched with status 200). Use ONLY these URLs, or mark others [NV].",
    "",
    "| URL | local file (read it for details) | page title |",
    "|---|---|---|",
]
out += [f"| {u} | {p} | {h} |" for u, p, h in rows]
out += [
    "",
    "## Other verified references (from research notes, read earlier)",
    "- IRSA TAP: https://irsa.ipac.caltech.edu/TAP/sync (research/notes_spherex.md)",
    "- SPHEREx Explanatory Supplement PDF: https://irsa.ipac.caltech.edu/data/SPHEREx/docs/SPHEREx_Expsupp.pdf (research2/notes_expsupp.md, page numbers inside)",
    "- IRSA cloud access: https://irsa.ipac.caltech.edu/cloud_access/ (research2/notes_server.md)",
    "- WiseView: http://byw.tools/wiseview (research/notes_gaia_wiseview.md)",
    "- SkyBoT API: https://ssp.imcce.fr/webservices/skybot/api/conesearch.php (stage0/s0_D.md)",
    "- Gaia ESA TAP: https://gea.esac.esa.int/tap-server/tap (research/notes_gaia_wiseview.md); MAST Gaia DR3 TAP was used in stage0/s0_C.md",
    "- NASA challenge text (pasted by the user; summarized in plan/SITE_SPEC.md)",
]
(kb / "clickup" / "SOURCE_MAP.md").write_text("\n".join(out), encoding="utf-8")
print(len(rows), "pages mapped")
