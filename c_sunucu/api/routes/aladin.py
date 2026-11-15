"""
aladin.py — Aladin Lite bağlam paneli ve harici kaynak bağlantıları (Görev 05-14).

GET /aladin/panel               -> Aladin Lite HTML panelini döner (HTMLResponse)
GET /aladin/links/{target_id}   -> Belirtilen hedefin SIMBAD, VizieR, Legacy Survey bağlantılarını döner
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional
from urllib.parse import quote

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/aladin", tags=["aladin"])

TARGETS: dict[str, dict] = {
    "barnard":    {"label": "Barnard's Star", "ra": 269.4521, "dec": 4.6933},
    "eps_indi_b": {"label": "eps Indi B",     "ra": 330.84,   "dec": -56.786},
    "wise0855":   {"label": "WISE 0855−0714", "ra": 129.0,    "dec": -11.0},
    "rw_aur":     {"label": "RW Aur",         "ra": 72.77,    "dec": 28.44},
    "r_dra":      {"label": "R Dra",          "ra": 267.4,    "dec": 65.6},
}


class ExternalLink(BaseModel):
    label: str
    href: str
    title: str


class TargetLinksResponse(BaseModel):
    target_id: str
    label: str
    ra: float
    dec: float
    links: list[ExternalLink]


def build_links(ra: float, dec: float) -> list[ExternalLink]:
    """RA ve Dec koordinatları için harici katalog bağlantılarını üretir."""
    ra_fmt = f"{ra:.5f}"
    dec_fmt = f"+{dec:.4f}" if dec >= 0 else f"{dec:.4f}"
    coord_str = quote(f"{ra_fmt}{dec_fmt}")
    return [
        ExternalLink(
            label="SIMBAD",
            href=f"https://simbad.cds.unistra.fr/simbad/sim-coo?Coord={coord_str}&CooFrame=FK5&CooEpoch=2000&CooEqui=2000&Radius=2&Radius.unit=arcmin&submit=submit+query",
            title="Query SIMBAD by coordinates",
        ),
        ExternalLink(
            label="VizieR",
            href=f"https://vizier.cds.unistra.fr/viz-bin/VizieR?-c={coord_str}&-c.rs=2",
            title="Query VizieR catalogues",
        ),
        ExternalLink(
            label="Legacy Survey",
            href=f"https://www.legacysurvey.org/viewer?ra={ra}&dec={dec}&zoom=12&layer=ls-dr10",
            title="Open in Legacy Survey Sky Viewer (DR10)",
        ),
    ]


@router.get("/panel", response_class=HTMLResponse)
async def get_aladin_panel() -> HTMLResponse:
    """Aladin Lite context panel HTML sayfasını sunar."""
    # REPO_ROOT: aladin.py -> routes -> api -> c_sunucu -> repo_root
    repo_root = Path(__file__).resolve().parent.parent.parent.parent
    panel_path = repo_root / "d_site" / "pages" / "aladin_panel.html"
    if not panel_path.exists():
        raise HTTPException(status_code=404, detail="Aladin panel HTML not found")
    return HTMLResponse(content=panel_path.read_text(encoding="utf-8"))


@router.get("/links/{target_id}", response_model=TargetLinksResponse)
async def get_target_links(
    target_id: str,
    ra: Optional[float] = Query(None, description="Override RA (derece)"),
    dec: Optional[float] = Query(None, description="Override Dec (derece)"),
) -> TargetLinksResponse:
    """Belirtilen hedefe ait koordinatlar ve harici bağlantıları döner."""
    tid = target_id.lower()
    if tid not in TARGETS and (ra is None or dec is None):
        raise HTTPException(
            status_code=404,
            detail=f"Target '{target_id}' not found and coordinates not provided",
        )

    tgt = TARGETS.get(tid, {"label": target_id, "ra": 0.0, "dec": 0.0})
    final_ra = ra if ra is not None else tgt["ra"]
    final_dec = dec if dec is not None else tgt["dec"]

    links = build_links(final_ra, final_dec)
    return TargetLinksResponse(
        target_id=target_id,
        label=tgt["label"],
        ra=final_ra,
        dec=final_dec,
        links=links,
    )
