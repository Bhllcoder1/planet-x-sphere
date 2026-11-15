"""
profile.py — Profil ve geçmiş API uç noktaları.

GET  /profile/me              → mevcut kullanıcı bilgisi
GET  /profile/history         → son 50 geçmiş girişi
POST /profile/history         → yeni giriş ekle
DELETE /profile/history       → tüm geçmişi temizle
GET  /profile/history/restore → URL parametrelerinden giriş oluştur (11-07)

Kimlik doğrulama: tüm uç noktalar HTTP-only çerez oturumu ile korunur
(``get_current_user`` bağımlılığı, ``api.routes.auth`` modülünden).
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from accounts.history import HistoryEntry, HistoryRepository, new_entry
from accounts.session import Session
from api.routes.auth import _get_user_repo, get_current_user
from accounts.user_repo import UserRepository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/profile", tags=["profile"])


# ---------------------------------------------------------------------------
# Fabrika — geçmiş deposu
# ---------------------------------------------------------------------------


def _get_history_repo(request: Request) -> HistoryRepository:
    """İstek durumundan HistoryRepository nesnesi üretir.

    Args:
        request: FastAPI istek nesnesi; ``app.state.settings.l2_cache_dir`` okunur.

    Returns:
        HistoryRepository örneği.
    """
    settings = request.app.state.settings
    return HistoryRepository(Path(settings.l2_cache_dir))


# ---------------------------------------------------------------------------
# Pydantic yanıt/istek modelleri
# ---------------------------------------------------------------------------


class MeResponse(BaseModel, frozen=True):
    """GET /profile/me yanıt modeli."""

    user_id: str = Field(..., description="UUID4 kullanıcı kimliği")
    username: str = Field(..., description="Kullanıcı adı")
    display_name: str = Field(..., description="Görünen ad")
    role: str = Field(..., description="Kullanıcı rolü: jury | team | admin")
    created_at: Optional[str] = Field(
        default=None,
        description="Hesap oluşturulma tarihi (ISO 8601 UTC); model desteklemiyorsa null",
    )


class HistoryEntryOut(BaseModel, frozen=True):
    """Tek bir geçmiş girişi çıktı modeli."""

    id: str = Field(..., description="UUID4 giriş kimliği")
    user_id: str = Field(..., description="Girişi oluşturan kullanıcının kimliği")
    target_id: str = Field(..., description="SPHEREx hedef tanımlayıcısı")
    frame_id: str = Field(..., description="SPHEREx kare tanımlayıcısı")
    x0: int = Field(..., description="Pencerenin sol sütunu (0 tabanlı piksel)")
    y0: int = Field(..., description="Pencerenin üst satırı (0 tabanlı piksel)")
    width: int = Field(..., description="Pencere genişliği (piksel)")
    height: int = Field(..., description="Pencere yüksekliği (piksel)")
    timestamp: str = Field(..., description="ISO 8601 UTC zaman damgası")
    share_url: str = Field(..., description="Paylaşım sorgu dizesi")


class AddHistoryRequest(BaseModel, frozen=True):
    """POST /profile/history istek gövdesi."""

    target_id: str = Field(
        ..., min_length=1, max_length=200, description="SPHEREx hedef ID"
    )
    frame_id: str = Field(
        ..., min_length=1, max_length=200, description="SPHEREx kare ID"
    )
    x0: int = Field(..., ge=0, description="Pencerenin sol sütunu (piksel)")
    y0: int = Field(..., ge=0, description="Pencerenin üst satırı (piksel)")
    width: int = Field(
        default=100, ge=1, le=4096, description="Pencere genişliği (piksel)"
    )
    height: int = Field(
        default=100, ge=1, le=4096, description="Pencere yüksekliği (piksel)"
    )


class HistoryListOut(BaseModel, frozen=True):
    """GET /profile/history yanıt zarfı."""

    items: list[HistoryEntryOut] = Field(..., description="Geçmiş girişleri")
    total: int = Field(..., description="Döndürülen giriş sayısı")


class ClearOut(BaseModel, frozen=True):
    """DELETE /profile/history yanıt zarfı."""

    deleted: int = Field(..., description="Silinen giriş sayısı")


class RestoreOut(BaseModel, frozen=True):
    """GET /profile/history/restore yanıt modeli."""

    entry_id: str = Field(..., description="Oluşturulan geçmiş girişinin UUID4 kimliği")
    share_url: str = Field(
        ...,
        description=(
            "Görüntüleme penceresini paylaşmak için URL sorgu dizesi "
            "(?target=...&frame=...&x=...&y=...&w=...&h=...)"
        ),
    )


# ---------------------------------------------------------------------------
# Yardımcı
# ---------------------------------------------------------------------------


def _to_out(entry: HistoryEntry) -> HistoryEntryOut:
    """HistoryEntry → HistoryEntryOut dönüşümü; yeni nesne oluşturur (değiştirmez).

    Args:
        entry: Dönüştürülecek HistoryEntry nesnesi.

    Returns:
        Yeni HistoryEntryOut nesnesi.
    """
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
    "/me",
    response_model=MeResponse,
    summary="Mevcut kullanıcı bilgisi",
)
async def get_me(
    request: Request,
    session: Annotated[Session, Depends(get_current_user)],
    repo: Annotated[UserRepository, Depends(_get_user_repo)],
) -> MeResponse:
    """Giriş yapmış kullanıcının profil bilgilerini döndürür.

    Oturum çerezinden kimlik doğrulaması yapılır. Kullanıcı bilgileri
    UserRepository'den çekilir.

    Args:
        request: FastAPI istek nesnesi.
        session: Çerezden doğrulanmış oturum nesnesi.
        repo:    Kullanıcı deposu bağımlılığı.

    Returns:
        Kullanıcının user_id, username, display_name ve role bilgilerini içeren yanıt.

    Raises:
        HTTPException 401: Geçerli oturum bulunamazsa.
        HTTPException 404: Oturumdaki kullanıcı artık mevcut değilse.
    """
    user = repo.find_by_username(session.username)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Oturumdaki kullanıcı artık bulunamıyor.",
        )

    return MeResponse(
        user_id=user.id,
        username=user.username,
        display_name=user.display_name,
        role=user.role,
        # User modeli created_at alanını desteklememektedir; None döner.
        created_at=None,
    )


@router.get(
    "/history",
    response_model=HistoryListOut,
    summary="Son geçmiş girişlerini listele",
)
async def list_history(
    request: Request,
    session: Annotated[Session, Depends(get_current_user)],
    limit: int = Query(default=50, ge=1, le=100, description="Döndürülecek maksimum giriş sayısı"),
) -> HistoryListOut:
    """Kullanıcının son ``limit`` geçmiş girişini döndürür.

    Varsayılan limit 50'dir; 1–100 arasında ayarlanabilir.

    Args:
        request: FastAPI istek nesnesi.
        session: Çerezden doğrulanmış oturum nesnesi.
        limit:   Döndürülecek maksimum giriş sayısı.

    Returns:
        Geçmiş girişleri listesi ve toplam sayı.

    Raises:
        HTTPException 401: Geçerli oturum bulunamazsa.
    """
    repo = _get_history_repo(request)
    entries = await repo.get_all(session.user_id, limit=limit)
    return HistoryListOut(items=[_to_out(e) for e in entries], total=len(entries))


@router.post(
    "/history",
    response_model=HistoryEntryOut,
    status_code=201,
    summary="Yeni geçmiş girdisi ekle",
)
async def add_history(
    body: AddHistoryRequest,
    request: Request,
    session: Annotated[Session, Depends(get_current_user)],
) -> HistoryEntryOut:
    """Yeni bir görüntüleme olayını kullanıcının geçmişine kaydeder.

    UUID4 kimliği ve UTC zaman damgası otomatik atanır.
    Paylaşım URL'si ``target_id``, ``frame_id`` ve pencere parametrelerinden üretilir.

    Args:
        body:    İstek gövdesi (target_id, frame_id, x0, y0, width, height).
        request: FastAPI istek nesnesi.
        session: Çerezden doğrulanmış oturum nesnesi.

    Returns:
        Oluşturulan geçmiş girdisi.

    Raises:
        HTTPException 401: Geçerli oturum bulunamazsa.
    """
    entry = new_entry(
        user_id=session.user_id,
        target_id=body.target_id,
        frame_id=body.frame_id,
        x0=body.x0,
        y0=body.y0,
        width=body.width,
        height=body.height,
    )
    repo = _get_history_repo(request)
    await repo.add(session.user_id, entry)
    logger.info(
        "Geçmiş girdisi eklendi: user=%r target=%r frame=%r entry_id=%r",
        session.user_id,
        body.target_id,
        body.frame_id,
        entry.id,
    )
    return _to_out(entry)


@router.delete(
    "/history",
    response_model=ClearOut,
    summary="Tüm geçmişi temizle",
)
async def clear_history(
    request: Request,
    session: Annotated[Session, Depends(get_current_user)],
) -> ClearOut:
    """Kullanıcının geçmişteki tüm girişlerini siler.

    Silinen giriş sayısını ``{deleted: N}`` biçiminde döndürür.

    Args:
        request: FastAPI istek nesnesi.
        session: Çerezden doğrulanmış oturum nesnesi.

    Returns:
        Silinen giriş sayısı.

    Raises:
        HTTPException 401: Geçerli oturum bulunamazsa.
    """
    repo = _get_history_repo(request)
    deleted = await repo.clear(session.user_id)
    logger.info(
        "Geçmiş temizlendi: user=%r silinen=%d",
        session.user_id,
        deleted,
    )
    return ClearOut(deleted=deleted)


@router.get(
    "/history/restore",
    response_model=RestoreOut,
    summary="URL parametrelerinden geçmiş girdisi oluştur",
)
async def restore_from_url(
    request: Request,
    session: Annotated[Session, Depends(get_current_user)],
    target: str = Query(..., min_length=1, max_length=200, description="SPHEREx hedef tanımlayıcısı"),
    frame: str = Query(..., min_length=1, max_length=200, description="SPHEREx kare tanımlayıcısı"),
    x: int = Query(..., ge=0, description="Pencerenin sol sütunu (0 tabanlı piksel)"),
    y: int = Query(..., ge=0, description="Pencerenin üst satırı (0 tabanlı piksel)"),
    w: int = Query(default=100, ge=1, le=4096, description="Pencere genişliği (piksel)"),
    h: int = Query(default=100, ge=1, le=4096, description="Pencere yüksekliği (piksel)"),
) -> RestoreOut:
    """URL sorgu parametrelerinden geçmiş girdisi oluşturur ve kaydeder.

    Paylaşılan bir URL'den (?target=&frame=&x=&y=&w=&h=) ziyaret geri yüklemesi
    yapar: parametreler geçerliyse geçmişe yeni giriş ekler ve oluşturulan
    girişin kimliği ile paylaşım URL'sini döndürür.

    Sorgu parametreleri:
        target: SPHEREx hedef tanımlayıcısı (zorunlu, boş olamaz).
        frame:  SPHEREx kare tanımlayıcısı (zorunlu, boş olamaz).
        x:      Pencerenin sol sütunu (zorunlu, >= 0).
        y:      Pencerenin üst satırı (zorunlu, >= 0).
        w:      Pencere genişliği (varsayılan 100, 1–4096 arası).
        h:      Pencere yüksekliği (varsayılan 100, 1–4096 arası).

    Returns:
        Oluşturulan girişin ``entry_id`` ve ``share_url`` alanlarını içeren yanıt.

    Raises:
        HTTPException 400: Parametreler boş veya geçersiz değer içeriyorsa.
        HTTPException 401: Geçerli oturum bulunamazsa.
    """
    # Pydantic/FastAPI Query kısıtlamaları (min_length, ge, le) çoğu geçersiz
    # girişi 422 ile yakalar. Ek semantik doğrulama: boşluk-only değerler reddedilir.
    if not target.strip():
        raise HTTPException(
            status_code=400,
            detail="'target' parametresi boş veya yalnızca boşluk içeremez.",
        )
    if not frame.strip():
        raise HTTPException(
            status_code=400,
            detail="'frame' parametresi boş veya yalnızca boşluk içeremez.",
        )

    entry = new_entry(
        user_id=session.user_id,
        target_id=target.strip(),
        frame_id=frame.strip(),
        x0=x,
        y0=y,
        width=w,
        height=h,
    )
    repo = _get_history_repo(request)
    await repo.add(session.user_id, entry)
    logger.info(
        "URL'den geri yükleme: user=%r target=%r frame=%r entry_id=%r",
        session.user_id,
        target,
        frame,
        entry.id,
    )
    return RestoreOut(entry_id=entry.id, share_url=entry.share_url)


@router.get("/view", response_class=HTMLResponse, summary="Profil ve geçmiş HTML sayfası (Görev 11-09)")
async def get_profile_page() -> HTMLResponse:
    """d_site/pages/profile.html sayfasını döndürür."""
    # Find profile.html relative to repo root
    html_path = Path(__file__).resolve().parent.parent.parent / "d_site" / "pages" / "profile.html"
    if not html_path.exists():
        # Fallback if structure varies
        alt_path = Path("d_site/pages/profile.html")
        if alt_path.exists():
            html_path = alt_path
        else:
            raise HTTPException(status_code=404, detail="profile.html bulunamadı")
    return HTMLResponse(content=html_path.read_text(encoding="utf-8"))
