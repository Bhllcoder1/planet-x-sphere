"""Scrape seed pages into one markdown file each (scrapling).

Usage: python -I scrape.py            -> seeds below
       python -I scrape.py URL [URL]  -> extra pages
TLS verification stays ON. Failures are written into the .md as FAILED, never hidden.
"""
import re
import sys
import datetime
from pathlib import Path
from urllib.parse import urlparse

from scrapling.fetchers import Fetcher

OUT = Path(__file__).resolve().parent.parent / "sources"
OUT.mkdir(exist_ok=True)

SEEDS = {
    "csa-neossat-dataset": "https://data.asc-csa.gc.ca/dataset/neossat",
    "github-neossat-tutorial": "https://github.com/asc-csa/NEOSSAT_Tutorial",
    "cadc-home": "https://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/en/",
    "csa-neossat-mission": "https://www.asc-csa.gc.ca/eng/satellites/neossat/",
    "mast-gaia": "https://archive.stsci.edu/missions-and-data/gaia",
    "wiseview": "http://byw.tools/wiseview",
    "irsa-euclid-clusters-tutorial": "https://caltech-ipac.github.io/irsa-tutorials/euclid-clusters-tutorial/",
    "irsa-spherex": "https://irsa.ipac.caltech.edu/Missions/spherex.html",
    # deeper pages, taken from the links on the IRSA SPHEREx page
    "irsa-spherex-docs-overview-dr1": "https://irsa.ipac.caltech.edu/data/SPHEREx/docs/overview_dr1.html",
    "irsa-spherex-docs-overview-qr": "https://irsa.ipac.caltech.edu/data/SPHEREx/docs/overview_qr.html",
    "irsa-spherex-docs-cutout-tool": "https://irsa.ipac.caltech.edu/data/SPHEREx/docs/cutout_tool.html",
    "irsa-spherex-docs-spectral-calibrations": "https://irsa.ipac.caltech.edu/data/SPHEREx/docs/spherex_spectral_calibrations.html",
    "irsa-spherex-docs-psfhdrerr": "https://irsa.ipac.caltech.edu/data/SPHEREx/docs/psfhdrerr.html",
    "irsa-tut-spherex-intro": "https://caltech-ipac.github.io/irsa-tutorials/spherex-intro/",
    "irsa-tut-spherex-cutouts": "https://caltech-ipac.github.io/irsa-tutorials/spherex-cutouts/",
    "irsa-tut-spherex-psf": "https://caltech-ipac.github.io/irsa-tutorials/spherex-psf/",
    "irsa-tut-spherex-mosaic": "https://caltech-ipac.github.io/irsa-tutorials/spherex-mosaic/",
    "irsa-tut-spherex-source-discovery": "https://caltech-ipac.github.io/irsa-tutorials/spherex-source-discovery-tool-demo/",
}


def slug(url: str) -> str:
    p = urlparse(url)
    s = re.sub(r"[^A-Za-z0-9]+", "-", f"{p.netloc}{p.path}").strip("-").lower()
    return s[:80] or "page"


def scrape(name: str, url: str) -> str:
    now = datetime.date.today().isoformat()
    try:
        r = Fetcher.get(url, timeout=45)
        md = r.markdown
        body = str(md() if callable(md) else md) if r.status == 200 else ""
        links = sorted({r.urljoin(h) for h in r.css("a::attr(href)").getall()
                        if h and not h.startswith(("#", "mailto:", "javascript:"))})
        head = f"---\nsource: {url}\nfetched: {now}\nstatus: {r.status}\n---\n\n"
        if not body.strip():
            return head + f"FAILED: HTTP {r.status}, empty body.\n"
        return head + body + "\n\n## Links found on page\n\n" + "\n".join(f"- {l}" for l in links) + "\n"
    except Exception as e:  # report, don't hide
        return f"---\nsource: {url}\nfetched: {now}\nstatus: error\n---\n\nFAILED: {type(e).__name__}: {e}\n"


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["--out"]:
        OUT = Path(args[1])
        OUT.mkdir(parents=True, exist_ok=True)
        args = args[2:]
    targets = dict(SEEDS) if not args else {slug(u): u for u in args}
    for name, url in targets.items():
        text = scrape(name, url)
        (OUT / f"{name}.md").write_text(text, encoding="utf-8")
        ok = "FAILED" not in text[:400]
        print(f"{'OK  ' if ok else 'FAIL'} {name}  ({len(text)} chars)")
