from __future__ import annotations

"""
Sağlık kontrol uç noktaları.

GET /health  → sunucu durumu (ok / degraded)
GET /status  → önbellek istatistikleri
"""

import logging
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])


# ---------------------------------------------------------------------------
# Yanıt modelleri
# ---------------------------------------------------------------------------


class HealthResponse(BaseModel, frozen=True):
    """GET /health yanıt gövdesi."""

    status: str = Field(..., examples=["ok", "degraded"])
    l2_cache_exists: bool
    timestamp: str = Field(..., description="ISO-8601 UTC zaman damgası")


class CacheStats(BaseModel, frozen=True):
    """GET /status yanıt gövdesi."""

    status: str = Field(..., examples=["ok", "degraded"])
    l0_cache_exists: bool
    l1_cache_exists: bool
    l2_cache_exists: bool
    l2_file_count: int
    timestamp: str


# ---------------------------------------------------------------------------
# Yardımcı
# ---------------------------------------------------------------------------


def _utc_now() -> str:
    """Şimdiki zamanı ISO-8601 UTC biçiminde döndürür."""
    return datetime.now(tz=timezone.utc).isoformat()


def _dir_exists(path: str | None) -> bool:
    """Dizin yolunun var olup olmadığını kontrol eder."""
    if not path:
        return False
    return Path(path).is_dir()


def _count_files(path: str | None) -> int:
    """Dizindeki dosyaların sayısını döndürür; dizin yoksa 0."""
    if not path:
        return 0
    p = Path(path)
    if not p.is_dir():
        return 0
    return sum(1 for _ in p.iterdir() if _.is_file())


# ---------------------------------------------------------------------------
# Uç noktalar
# ---------------------------------------------------------------------------


@router.get("/health", response_model=HealthResponse, summary="Sunucu sağlık kontrolü")
async def health(request: Request) -> HealthResponse:
    """
    Sunucunun çalışır durumda olup olmadığını kontrol eder.

    L2 önbellek dizini yoksa durum `degraded` olarak döner; aksi hâlde `ok`.
    """
    settings = request.app.state.settings
    l2_exists = _dir_exists(settings.l2_cache_dir)

    status = "ok" if l2_exists else "degraded"
    if status == "degraded":
        logger.warning("L2 önbellek dizini bulunamadı: %s", settings.l2_cache_dir)

    return HealthResponse(
        status=status,
        l2_cache_exists=l2_exists,
        timestamp=_utc_now(),
    )


@router.get("/status", response_model=CacheStats, summary="Önbellek istatistikleri")
async def status(request: Request) -> CacheStats:
    """
    L0, L1 ve L2 önbellek dizinlerinin varlığını ve L2 dosya sayısını döndürür.
    """
    settings = request.app.state.settings

    l0_exists = _dir_exists(settings.l0_cache_dir)
    l1_exists = _dir_exists(settings.l1_cache_dir)
    l2_exists = _dir_exists(settings.l2_cache_dir)
    l2_count = _count_files(settings.l2_cache_dir)

    all_ok = l0_exists and l1_exists and l2_exists
    overall = "ok" if all_ok else "degraded"

    logger.debug(
        "Önbellek durumu: l0=%s l1=%s l2=%s dosya_sayısı=%d",
        l0_exists,
        l1_exists,
        l2_exists,
        l2_count,
    )

    return CacheStats(
        status=overall,
        l0_cache_exists=l0_exists,
        l1_cache_exists=l1_exists,
        l2_cache_exists=l2_exists,
        l2_file_count=l2_count,
        timestamp=_utc_now(),
    )
