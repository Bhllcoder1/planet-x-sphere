"""
auth.py — Kimlik doğrulama uç noktaları.

POST /auth/login  → çerez ayarla
POST /auth/logout → çerezi sil
GET  /auth/me     → mevcut kullanıcıyı döndür

Brute-force koruması: 5 başarısız deneme/dk/IP → 429 Too Many Requests.
Sliding-window sayacı bellekte tutulur; restart'ta sıfırlanır.
"""
from __future__ import annotations

import logging
import os
import pathlib
import time
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from accounts.session import SESSION_MAX_AGE, Session, session_store
from accounts.user_repo import UserRepository, _build_repo_from_env

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Ayarlar
# ---------------------------------------------------------------------------

COOKIE_NAME: str = os.environ.get("SESSION_COOKIE_NAME", "spherex_session")

# Brute-force: 5 başarısız deneme/60 saniye/IP → 429
FAIL_LIMIT = 5
FAIL_WINDOW = 60  # saniye

# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

router = APIRouter(prefix="/auth", tags=["auth"])

# ---------------------------------------------------------------------------
# Brute-force sayacı (bellek-içi sliding window)
# ---------------------------------------------------------------------------

# { ip_address: [(başarısız_deneme_zaman_damgası, ...), ...] }
_fail_log: dict[str, list[float]] = {}


def _check_rate_limit(ip: str) -> None:
    """IP başına başarısız giriş sayısını kontrol eder.

    FAIL_WINDOW saniye içinde FAIL_LIMIT'i aşan IP'ler 429 alır.

    Args:
        ip: İsteği gönderen IP adresi.

    Raises:
        HTTPException 429: Hız sınırı aşıldığında.
    """
    now = time.time()
    cutoff = now - FAIL_WINDOW

    # Eski girişleri temizle
    timestamps = _fail_log.get(ip, [])
    timestamps = [ts for ts in timestamps if ts > cutoff]
    _fail_log[ip] = timestamps

    if len(timestamps) >= FAIL_LIMIT:
        logger.warning(
            "Brute-force koruması devreye girdi — IP: %s, başarısız deneme: %d",
            ip,
            len(timestamps),
        )
        raise HTTPException(
            status_code=429,
            detail=(
                f"Çok fazla başarısız giriş denemesi. "
                f"{FAIL_WINDOW} saniye sonra tekrar deneyin."
            ),
        )


def _record_failure(ip: str) -> None:
    """IP için bir başarısız deneme zaman damgası kaydeder.

    Args:
        ip: Başarısız denemede bulunan IP adresi.
    """
    now = time.time()
    _fail_log.setdefault(ip, []).append(now)


def _clear_failures(ip: str) -> None:
    """Başarılı girişten sonra IP'nin başarısız deneme geçmişini sıfırlar.

    Args:
        ip: Başarıyla giriş yapan IP adresi.
    """
    _fail_log.pop(ip, None)


# ---------------------------------------------------------------------------
# İstek başına IP tespiti
# ---------------------------------------------------------------------------


def _get_client_ip(request: Request) -> str:
    """İstekten istemci IP adresini çıkarır.

    Önce X-Forwarded-For başlığına bakar (reverse proxy arkasında çalışırken),
    yoksa doğrudan bağlantı IP'sini kullanır.

    Args:
        request: FastAPI Request nesnesi.

    Returns:
        IP adresi dizesi; tespit edilemezse "unknown".
    """
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # Birden fazla proxy varsa listedeki ilk (gerçek istemci) IP'yi al
        return forwarded_for.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "unknown"


# ---------------------------------------------------------------------------
# Kullanıcı deposu bağımlılığı
# ---------------------------------------------------------------------------

_user_repo: UserRepository | None = None


def _get_user_repo() -> UserRepository:
    """Uygulama genelinde paylaşılan UserRepository singleton'ını döner.

    Returns:
        UserRepository örneği.
    """
    global _user_repo
    if _user_repo is None:
        _user_repo = _build_repo_from_env()
    return _user_repo


# ---------------------------------------------------------------------------
# Oturum bağımlılığı (diğer route'larda kullanılabilir)
# ---------------------------------------------------------------------------


def get_current_user(request: Request) -> Session:
    """Çerezden token okuyarak geçerli oturum nesnesini döner.

    Diğer route'larda ``Depends(get_current_user)`` ile kullanılır.

    Args:
        request: FastAPI Request nesnesi.

    Returns:
        Geçerli Session nesnesi.

    Raises:
        HTTPException 401: Token yoksa veya geçersizse.
    """
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail="Oturum çerezi bulunamadı.")

    session = session_store.get(token)
    if session is None:
        raise HTTPException(
            status_code=401,
            detail="Oturum geçersiz veya süresi dolmuş. Lütfen tekrar giriş yapın.",
        )
    return session


# ---------------------------------------------------------------------------
# Yanıt modelleri
# ---------------------------------------------------------------------------


class LoginResponse(BaseModel):
    """Başarılı giriş yanıtı."""

    user_id: str
    username: str
    display_name: str
    role: str
    message: str = "Giriş başarılı."


class MeResponse(BaseModel):
    """Mevcut kullanıcı bilgisi yanıtı."""

    user_id: str
    username: str
    display_name: str
    role: str


class LogoutResponse(BaseModel):
    """Çıkış yanıtı."""

    message: str = "Çıkış yapıldı."


# ---------------------------------------------------------------------------
# Uç noktalar
# ---------------------------------------------------------------------------


@router.post("/login", response_model=LoginResponse)
async def login(
    request: Request,
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    repo: Annotated[UserRepository, Depends(_get_user_repo)],
) -> LoginResponse:
    """Kullanıcı adı ve şifreyle giriş yapar; HTTP-only oturum çerezi ayarlar.

    Form alanları:
        username: Kullanıcı adı.
        password: Şifre.

    Returns:
        Kullanıcı bilgilerini içeren JSON yanıtı.

    Raises:
        HTTPException 401: Kullanıcı adı veya şifre hatalıysa.
        HTTPException 429: Hız sınırı aşıldığında.
    """
    ip = _get_client_ip(request)

    # Hız sınırı kontrolü (başarısız sayacı aşıldıysa 429 fırlatır)
    _check_rate_limit(ip)

    user = repo.find_by_username(form_data.username)
    if user is None or not repo.verify_password(user, form_data.password):
        _record_failure(ip)
        # Kullanıcı adı veya şifre hatalı — hangi alanın yanlış olduğunu belli etme
        raise HTTPException(
            status_code=401,
            detail="Kullanıcı adı veya şifre hatalı.",
        )

    # Başarılı giriş — başarısız sayacı sıfırla
    _clear_failures(ip)

    session = session_store.create(user_id=user.id, username=user.username)

    response.set_cookie(
        key=COOKIE_NAME,
        value=session.token,
        max_age=SESSION_MAX_AGE,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
    )

    logger.info("Giriş başarılı — kullanıcı: %s, IP: %s", user.username, ip)

    return LoginResponse(
        user_id=user.id,
        username=user.username,
        display_name=user.display_name,
        role=user.role,
    )


@router.post("/logout", response_model=LogoutResponse)
async def logout(
    request: Request,
    response: Response,
) -> LogoutResponse:
    """Mevcut oturumu sonlandırır ve çerezi siler.

    Çerez mevcut değilse yine de 200 döner (idempotent).

    Returns:
        Çıkış mesajı.
    """
    token = request.cookies.get(COOKIE_NAME)
    if token:
        session_store.delete(token)

    # Çerezi tarayıcıdan sil
    response.delete_cookie(
        key=COOKIE_NAME,
        path="/",
        httponly=True,
        secure=True,
        samesite="lax",
    )

    return LogoutResponse()


@router.get("/me", response_model=MeResponse)
async def me(
    request: Request,
    current_session: Annotated[Session, Depends(get_current_user)],
    repo: Annotated[UserRepository, Depends(_get_user_repo)],
) -> MeResponse:
    """Mevcut giriş yapmış kullanıcının bilgilerini döner.

    Args:
        request:         FastAPI Request nesnesi.
        current_session: Çerezden doğrulanmış oturum (Depends ile enjekte edilir).
        repo:            UserRepository bağımlılığı.

    Returns:
        Kullanıcı bilgilerini içeren JSON yanıtı.

    Raises:
        HTTPException 401: Geçerli oturum bulunamazsa.
        HTTPException 404: Oturumdaki kullanıcı artık mevcut değilse.
    """
    user = repo.find_by_username(current_session.username)
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
    )
