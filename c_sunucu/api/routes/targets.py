from __future__ import annotations

"""
Hedef (target) uç noktaları.

GET /targets                        → tüm hedeflerin listesi
GET /targets/{target_id}            → tek hedef meta verisi
GET /targets/{target_id}/frames     → hedefe ait kare listesi (manifest)
"""

import json
import logging
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/targets", tags=["targets"])

# Proje kapsamındaki sabit hedef listesi
KNOWN_TARGETS: tuple[str, ...] = (
    "barnard",
    "eps_indi_b",
    "wise0855",
    "rwaur",
    "rdra",
)


# ---------------------------------------------------------------------------
# Yanıt modelleri
# ---------------------------------------------------------------------------


class TargetSummary(BaseModel, frozen=True):
    """Hedef özet bilgisi."""

    target_id: str
    display_name: str
    manifest_available: bool


class TargetListResponse(BaseModel, frozen=True):
    """GET /targets yanıt gövdesi."""

    targets: tuple[TargetSummary, ...]
    total: int


class FrameEntry(BaseModel, frozen=True):
    """Manifest içindeki tek kare kaydı."""

    frame_id: str
    band: str | None = None
    mjd: float | None = None
    ra: float | None = None
    dec: float | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


class TargetFramesResponse(BaseModel, frozen=True):
    """GET /targets/{target_id}/frames yanıt gövdesi."""

    target_id: str
    frames: tuple[FrameEntry, ...]
    total: int


class TargetDetail(BaseModel, frozen=True):
    """GET /targets/{target_id} yanıt gövdesi."""

    target_id: str
    display_name: str
    manifest_available: bool
    frame_count: int | None = None


# ---------------------------------------------------------------------------
# Yardımcı fonksiyonlar
# ---------------------------------------------------------------------------


def _display_name(target_id: str) -> str:
    """Hedef kimliğini insan-okunur görüntü adına dönüştürür."""
    return target_id.replace("_", " ").title()


def _manifest_path(l0_cache_dir: str, target_id: str) -> Path:
    """Hedef manifest dosyasının tam yolunu döndürür."""
    return Path(l0_cache_dir) / target_id / "manifest.json"


def _load_manifest(path: Path) -> list[dict[str, Any]]:
    """
    Manifest JSON dosyasını okur ve liste döndürür.

    Raises:
        FileNotFoundError: Dosya mevcut değilse.
        ValueError: JSON ayrıştırma başarısız olursa.
    """
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if isinstance(data, list):
        return data  # type: ignore[return-value]
    if isinstance(data, dict) and "frames" in data:
        return data["frames"]  # type: ignore[return-value]
    raise ValueError(f"Manifest biçimi tanınmıyor: {path}")


def _frame_entry_from_dict(raw: dict[str, Any]) -> FrameEntry:
    """Ham sözlükten FrameEntry nesnesi oluşturur."""
    known_keys = {"frame_id", "band", "mjd", "ra", "dec"}
    extra = {k: v for k, v in raw.items() if k not in known_keys}
    return FrameEntry(
        frame_id=str(raw.get("frame_id", "")),
        band=raw.get("band"),
        mjd=raw.get("mjd"),
        ra=raw.get("ra"),
        dec=raw.get("dec"),
        extra=extra,
    )


# ---------------------------------------------------------------------------
# Uç noktalar
# ---------------------------------------------------------------------------


@router.get("", response_model=TargetListResponse, summary="Tüm hedefleri listele")
async def list_targets(request: Request) -> TargetListResponse:
    """
    Proje kapsamındaki tüm hedefleri döndürür.

    Her hedef için manifest dosyasının var olup olmadığı kontrol edilir.
    """
    settings = request.app.state.settings
    summaries: list[TargetSummary] = []

    for tid in KNOWN_TARGETS:
        mpath = _manifest_path(settings.l0_cache_dir, tid)
        summaries.append(
            TargetSummary(
                target_id=tid,
                display_name=_display_name(tid),
                manifest_available=mpath.is_file(),
            )
        )

    return TargetListResponse(targets=tuple(summaries), total=len(summaries))


@router.get(
    "/{target_id}",
    response_model=TargetDetail,
    summary="Tek hedef ayrıntıları",
)
async def get_target(target_id: str, request: Request) -> TargetDetail:
    """
    Belirtilen hedefe ait meta veriyi döndürür.

    Hedef bilinmiyorsa 404 döner. Manifest yoksa frame_count None olarak döner.
    """
    if target_id not in KNOWN_TARGETS:
        raise HTTPException(status_code=404, detail=f"Target not found: {target_id}")

    settings = request.app.state.settings
    mpath = _manifest_path(settings.l0_cache_dir, target_id)
    manifest_available = mpath.is_file()
    frame_count: int | None = None

    if manifest_available:
        try:
            frames = _load_manifest(mpath)
            frame_count = len(frames)
        except Exception as exc:
            logger.warning("Manifest okunamadı (%s): %s", mpath, exc)

    return TargetDetail(
        target_id=target_id,
        display_name=_display_name(target_id),
        manifest_available=manifest_available,
        frame_count=frame_count,
    )


@router.get(
    "/{target_id}/frames",
    response_model=TargetFramesResponse,
    summary="Hedef kare listesi (manifest)",
)
async def get_target_frames(target_id: str, request: Request) -> TargetFramesResponse:
    """
    Hedefe ait kare listesini manifest dosyasından okuyarak döndürür.

    Manifest yoksa 503 döner; hedef bilinmiyorsa 404 döner.
    """
    if target_id not in KNOWN_TARGETS:
        raise HTTPException(status_code=404, detail=f"Target not found: {target_id}")

    settings = request.app.state.settings
    mpath = _manifest_path(settings.l0_cache_dir, target_id)

    if not mpath.is_file():
        logger.warning("Manifest bulunamadı: %s", mpath)
        raise HTTPException(
            status_code=503,
            detail=f"Cache not ready: manifest missing for target '{target_id}'",
        )

    try:
        raw_frames = _load_manifest(mpath)
    except ValueError as exc:
        logger.error("Manifest ayrıştırma hatası (%s): %s", mpath, exc)
        raise HTTPException(
            status_code=503,
            detail="Cache not ready: manifest parse error",
        ) from exc
    except OSError as exc:
        logger.error("Manifest okuma hatası (%s): %s", mpath, exc)
        raise HTTPException(
            status_code=503,
            detail="Cache not ready: manifest read error",
        ) from exc

    entries = tuple(_frame_entry_from_dict(r) for r in raw_frames)
    return TargetFramesResponse(
        target_id=target_id,
        frames=entries,
        total=len(entries),
    )
