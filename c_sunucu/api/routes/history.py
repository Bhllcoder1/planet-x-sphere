"""
history.py route — Arama geçmişi API'si.

GET    /history        → kullanıcının son 50 girişi (limit sorgu parametresi ile ayarlanabilir)
POST   /history        → yeni giriş ekle
DELETE /history        → tümünü temizle
GET    /history/{id}   → tek giriş

Kimlik doğrulama: tüm uç noktalar ``get_current_user`` bağımlılığı ile korunur.
Demo stub'ı ``Authorization: Bearer <user_id>`` başlığından kullanıcı kimliğini okur.
"""
from __future__ import annotations

import logging
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from accounts.history import (
    HistoryEntry,
    HistoryRepository,
    _sanitize_user_id,
    new_entry,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/history", tags=["history"])

# Tekil giriş araması için üst limit sabiti
_MAX_ENTRIES_SCAN: int = 100


# ---------------------------------------------------------------------------
# Kimlik doğrulama bağımlılığı
# ---------------------------------------------------------------------------


async def get_current_user(request: Request) -> str:
    """HTTP Authorization başlığından kullanıcı kimliğini çıkarır ve doğrular.

    Demo stub'ı: ``Authorization: Bearer <user_id>`` biçimini bekler.
    Gerçek uygulamada bu fonksiyon JWT imzasını doğrulayıp oturum bilgisini döner.

    Token değeri, path traversal saldırılarını engellemek için ``_sanitize_user_id``
    ile doğrulanır. Yalnızca ``[A-Za-z0-9_-]`` içeren, 1–128 karakter uzunluğundaki
    değerlere izin verilir.

    Args:
        request: FastAPI istek nesnesi.

    Returns:
        Doğrulanmış kullanıcı kimliği dizesi.

    Raises:
        HTTPException 401: Başlık eksik, token boş veya geçersiz biçimdeyse.
    """
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Kimlik doğrulama gerekli. 'Authorization: Bearer <token>' başlığı ekleyin.",
        )
    token = auth.removeprefix("Bearer ").strip()
    if not token:
        raise HTTPException(status_code=401, detail="Geçersiz ya da boş token.")
    try:
        _sanitize_user_id(token)
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Geçersiz token biçimi. Yalnızca harf, rakam, '-' ve '_' kabul edilir.",
        )
    return token


# ---------------------------------------------------------------------------
# Fabrika — depo nesnesi (FastAPI Depends ile enjekte edilir)
# ---------------------------------------------------------------------------


async def get_repo(request: Request) -> HistoryRepository:
    """FastAPI bağımlılığı olarak HistoryRepository nesnesi üretir.

    ``app.dependency_overrides`` ile testlerde kolayca geçersiz kılınabilir:

    .. code-block:: python

        app.dependency_overrides[get_repo] = lambda: HistoryRepository(tmp_path)

    Args:
        request: FastAPI istek nesnesi; ``app.state.settings.l2_cache_dir`` okunur.

    Returns:
        HistoryRepository örneği.
    """
    settings = request.app.state.settings
    return HistoryRepository(Path(settings.l2_cache_dir))


# ---------------------------------------------------------------------------
# Pydantic modelleri
# ---------------------------------------------------------------------------


class HistoryEntryOut(BaseModel, frozen=True):
    """API'ye dönen tek giriş modeli."""

    id: str
    user_id: str
    target_id: str
    frame_id: str
    x0: int
    y0: int
    width: int
    height: int
    timestamp: str = Field(..., description="ISO 8601 UTC zaman damgası")
    share_url: str = Field(..., description="Paylaşım sorgu dizesi")


class AddHistoryRequest(BaseModel, frozen=True):
    """POST /history istek gövdesi."""

    target_id: str = Field(..., min_length=1, max_length=200, description="SPHEREx hedef ID")
    frame_id: str = Field(..., min_length=1, max_length=200, description="SPHEREx kare ID")
    x0: int = Field(..., ge=0, description="Pencerenin sol sütunu (piksel)")
    y0: int = Field(..., ge=0, description="Pencerenin üst satırı (piksel)")
    width: int = Field(default=100, ge=1, le=4096, description="Pencere genişliği (piksel)")
    height: int = Field(default=100, ge=1, le=4096, description="Pencere yüksekliği (piksel)")


class HistoryListOut(BaseModel, frozen=True):
    """GET /history yanıt zarfı."""

    items: list[HistoryEntryOut]
    total: int = Field(..., description="Döndürülen giriş sayısı")


class ClearOut(BaseModel, frozen=True):
    """DELETE /history yanıt zarfı."""

    deleted: int = Field(..., description="Silinen giriş sayısı")


# ---------------------------------------------------------------------------
# Yardımcı
# ---------------------------------------------------------------------------


def _to_out(entry: HistoryEntry) -> HistoryEntryOut:
    """HistoryEntry → HistoryEntryOut dönüşümü (veri kopyası oluşturur)."""
    return HistoryEntryOut(
        id=entry.id,
        user_id=entry.user_id,
        target_id=entry.target_id,
        frame_id=entry.frame_id,
        x0=entry.x0,
        y0=entry.y0,
        width=entry.width,
        height=entry.height,
        timestamp=entry.timestamp,
        share_url=entry.share_url,
    )


# ---------------------------------------------------------------------------
# Uç noktalar
# ---------------------------------------------------------------------------


@router.get(
    "",
    response_model=HistoryListOut,
    summary="Son geçmiş girişlerini listele",
)
async def list_history(
    limit: int = 50,
    user_id: str = Depends(get_current_user),
    repo: HistoryRepository = Depends(get_repo),
) -> HistoryListOut:
    """Kullanıcının son ``limit`` geçmiş girişini döndürür.

    Args:
        limit:   Döndürülecek maksimum giriş sayısı (1–100 arası).
        user_id: ``get_current_user`` bağımlılığından gelen kullanıcı kimliği.
        repo:    ``get_repo`` bağımlılığından gelen depo nesnesi.

    Returns:
        Geçmiş girişleri ve toplam sayı.

    Raises:
        HTTPException 422: ``limit`` 1–100 aralığının dışındaysa.
    """
    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=422,
            detail="'limit' parametresi 1 ile 100 arasında olmalıdır.",
        )
    entries = await repo.get_all(user_id, limit=limit)
    return HistoryListOut(items=[_to_out(e) for e in entries], total=len(entries))


@router.post(
    "",
    response_model=HistoryEntryOut,
    status_code=201,
    summary="Yeni geçmiş girdisi ekle",
)
async def add_history(
    body: AddHistoryRequest,
    user_id: str = Depends(get_current_user),
    repo: HistoryRepository = Depends(get_repo),
) -> HistoryEntryOut:
    """Yeni bir görüntüleme olayını geçmişe kaydeder.

    UUID4 kimliği ve UTC zaman damgası otomatik atanır.
    Paylaşım URL'si ``target_id``, ``frame_id`` ve pencere parametrelerinden üretilir.

    Args:
        body:    İstek gövdesi (target_id, frame_id, x0, y0, width, height).
        user_id: ``get_current_user`` bağımlılığından gelen kullanıcı kimliği.
        repo:    ``get_repo`` bağımlılığından gelen depo nesnesi.

    Returns:
        Oluşturulan HistoryEntryOut nesnesi.
    """
    entry = new_entry(
        user_id=user_id,
        target_id=body.target_id,
        frame_id=body.frame_id,
        x0=body.x0,
        y0=body.y0,
        width=body.width,
        height=body.height,
    )
    await repo.add(user_id, entry)
    logger.info(
        "Geçmiş girdisi eklendi: user=%r target=%r frame=%r entry_id=%r",
        user_id,
        body.target_id,
        body.frame_id,
        entry.id,
    )
    return _to_out(entry)


@router.delete(
    "",
    response_model=ClearOut,
    summary="Tüm geçmişi temizle",
)
async def clear_history(
    user_id: str = Depends(get_current_user),
    repo: HistoryRepository = Depends(get_repo),
) -> ClearOut:
    """Kullanıcının geçmişteki tüm girişlerini siler.

    Args:
        user_id: ``get_current_user`` bağımlılığından gelen kullanıcı kimliği.
        repo:    ``get_repo`` bağımlılığından gelen depo nesnesi.

    Returns:
        Silinen giriş sayısı.
    """
    deleted = await repo.clear(user_id)
    logger.info("Geçmiş temizlendi: user=%r silinen=%d", user_id, deleted)
    return ClearOut(deleted=deleted)


@router.get(
    "/{entry_id}",
    response_model=HistoryEntryOut,
    summary="Tek geçmiş girdisi",
)
async def get_history_entry(
    entry_id: str,
    user_id: str = Depends(get_current_user),
    repo: HistoryRepository = Depends(get_repo),
) -> HistoryEntryOut:
    """Kullanıcının geçmişinde belirli bir girişi ID'ye göre döndürür.

    Args:
        entry_id: Aranacak UUID4 giriş kimliği.
        user_id:  ``get_current_user`` bağımlılığından gelen kullanıcı kimliği.
        repo:     ``get_repo`` bağımlılığından gelen depo nesnesi.

    Returns:
        Eşleşen HistoryEntryOut nesnesi.

    Raises:
        HTTPException 404: Belirtilen ID'ye sahip giriş bulunamazsa.
    """
    # Demo ölçeğinde doğrusal arama yeterlidir (maks. 100 giriş).
    entries = await repo.get_all(user_id, limit=_MAX_ENTRIES_SCAN)
    for entry in entries:
        if entry.id == entry_id:
            return _to_out(entry)
    raise HTTPException(
        status_code=404,
        detail=f"Geçmiş girdisi bulunamadı: '{entry_id}'",
    )
