"""
politeness.py — Nezaket sınırları ve backoff.

IRSA politikası (gerçek sınırlar [NV]):
- S3: max 4 eşzamanlı Range GET [ASSUMPTION: güvenli; ölçülmedi]
- TAP async: 1 eşzamanlı iş açık tutulur (kuyruklama sonraki görevde)
- Kesit servisi: 1 eşzamanlı istek; 503 → 45 s bekle [V: s0_B §3]

İçerik:
- S3Semaphore: asyncio.Semaphore(4)
- TapSemaphore: asyncio.Semaphore(1)
- CutoutSemaphore: asyncio.Semaphore(1) + 503 backoff
- RateLimiter: IP başına dakikada N istek (varsayılan: 60/dk)
- FastAPI middleware: X-Rate-Limit-Remaining başlığı
"""
from __future__ import annotations

import asyncio
import logging
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Sabitler
# ---------------------------------------------------------------------------

CUTOUT_BACKOFF_SECONDS: float = 45.0  # 503 sonrası bekleme [V: s0_B §3]
S3_CONCURRENCY: int = 4               # [ASSUMPTION]
TAP_CONCURRENCY: int = 1
CUTOUT_CONCURRENCY: int = 1
DEFAULT_RATE_LIMIT: int = 60          # istek/dakika/IP

# ---------------------------------------------------------------------------
# Modül düzeyinde semaforlar — init_semaphores() çağrılana kadar None kalır
# ---------------------------------------------------------------------------

s3_semaphore: asyncio.Semaphore | None = None
tap_semaphore: asyncio.Semaphore | None = None
cutout_semaphore: asyncio.Semaphore | None = None


def init_semaphores() -> None:
    """
    Semaforları başlatır.

    FastAPI lifespan (startup) olayında çağrılmalıdır; asyncio
    olay döngüsü hazır olmadan çağrılırsa semaforlar yanlış döngüye
    bağlanabilir.
    """
    global s3_semaphore, tap_semaphore, cutout_semaphore
    s3_semaphore = asyncio.Semaphore(S3_CONCURRENCY)
    tap_semaphore = asyncio.Semaphore(TAP_CONCURRENCY)
    cutout_semaphore = asyncio.Semaphore(CUTOUT_CONCURRENCY)
    logger.info(
        "Semaforlar başlatıldı: S3=%d, TAP=%d, Cutout=%d",
        S3_CONCURRENCY,
        TAP_CONCURRENCY,
        CUTOUT_CONCURRENCY,
    )


def _require_semaphore(sem: asyncio.Semaphore | None, name: str) -> asyncio.Semaphore:
    """
    Semaforu doğrular ve döndürür.

    Raises:
        RuntimeError: Semafor henüz başlatılmamışsa.
    """
    if sem is None:
        raise RuntimeError(
            f"{name} semaphore is not initialized. "
            "Call init_semaphores() during application startup."
        )
    return sem


def get_s3_semaphore() -> asyncio.Semaphore:
    """S3 semaforunu döndürür."""
    return _require_semaphore(s3_semaphore, "S3")


def get_tap_semaphore() -> asyncio.Semaphore:
    """TAP semaforunu döndürür."""
    return _require_semaphore(tap_semaphore, "TAP")


def get_cutout_semaphore() -> asyncio.Semaphore:
    """Kesit servisi semaforunu döndürür."""
    return _require_semaphore(cutout_semaphore, "Cutout")


# ---------------------------------------------------------------------------
# Kesit servisi 503 backoff
# ---------------------------------------------------------------------------

_cutout_backoff_until: float = 0.0  # time.monotonic() cinsinden hedef an


async def wait_cutout_backoff() -> None:
    """
    503 yanıtı sonrası belirlenen backoff süresi dolana kadar bekler.

    Backoff yoksa veya dolmuşsa hemen döner.
    """
    remaining = _cutout_backoff_until - time.monotonic()
    if remaining > 0.0:
        logger.warning(
            "Kesit servisi backoff etkin: %.1f s bekleniyor (toplam %.0f s)",
            remaining,
            CUTOUT_BACKOFF_SECONDS,
        )
        await asyncio.sleep(remaining)


def record_cutout_503() -> None:
    """
    Kesit servisinden 503 alındığında çağrılır.

    Bir sonraki isteği en erken ``CUTOUT_BACKOFF_SECONDS`` saniye sonrasına
    erteler.  Birden fazla 503 gelirse backoff her seferinde sıfırlanır
    (en kötü durumu varsayar).
    """
    global _cutout_backoff_until
    _cutout_backoff_until = time.monotonic() + CUTOUT_BACKOFF_SECONDS
    logger.warning(
        "Kesit servisi 503 alındı; %.0f s backoff başlatıldı",
        CUTOUT_BACKOFF_SECONDS,
    )


def cutout_backoff_remaining() -> float:
    """
    Kalan backoff süresini saniye cinsinden döndürür.

    Returns:
        Pozitif değer: hâlâ bekleme var.
        0.0: backoff bitti ya da hiç başlamadı.
    """
    return max(0.0, _cutout_backoff_until - time.monotonic())


# ---------------------------------------------------------------------------
# Sliding-window hız sınırlayıcı veri yapısı
# ---------------------------------------------------------------------------

@dataclass
class _WindowState:
    """
    Tek bir IP için kayan pencere durumunu tutar.

    Attributes:
        timestamps: Son N saniyedeki istek zamanları (monotonic).
        lock:       Eşzamanlı güncellemeyi engelleyen asyncio kilidi.
    """

    timestamps: deque[float] = field(default_factory=deque)
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)


# ---------------------------------------------------------------------------
# FastAPI middleware
# ---------------------------------------------------------------------------

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    IP başına kayan pencere (sliding window) hız sınırlayıcı.

    Her IP için son ``window_seconds`` saniye içindeki istek sayısını izler.
    Sınır aşılırsa ``429 Too Many Requests`` döner ve ``Retry-After``
    başlığı ile bekleme süresini bildirir.

    Yanıt başlıkları:
        X-Rate-Limit-Limit:     Pencere başına izin verilen istek sayısı.
        X-Rate-Limit-Remaining: Kalan istek hakkı (en az 0).
        X-Rate-Limit-Reset:     Pencerenin sıfırlanacağı Unix zamanı (tam sayı).

    Args:
        app:              ASGI uygulaması.
        calls_per_minute: Dakika başına izin verilen istek sayısı.
    """

    _WINDOW_SECONDS: float = 60.0

    def __init__(
        self,
        app,
        calls_per_minute: int = DEFAULT_RATE_LIMIT,
    ) -> None:
        super().__init__(app)
        if calls_per_minute < 1:
            raise ValueError(
                f"calls_per_minute must be >= 1, got {calls_per_minute}"
            )
        self._limit = calls_per_minute
        self._states: dict[str, _WindowState] = defaultdict(_WindowState)

    # ------------------------------------------------------------------
    # Yardımcı yöntemler
    # ------------------------------------------------------------------

    @staticmethod
    def _client_ip(request: Request) -> str:
        """
        İstemci IP adresini döndürür.

        Önce ``X-Forwarded-For`` başlığına, yoksa doğrudan bağlantı
        adresine bakar.
        """
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        if request.client:
            return request.client.host
        return "unknown"

    def _prune_and_count(self, state: _WindowState, now: float) -> int:
        """
        Pencere dışı zaman damgalarını atar ve mevcut istek sayısını döndürür.

        Dış kilit (*state.lock*) zaten alınmış olmalıdır.
        """
        cutoff = now - self._WINDOW_SECONDS
        while state.timestamps and state.timestamps[0] <= cutoff:
            state.timestamps.popleft()
        return len(state.timestamps)

    # ------------------------------------------------------------------
    # Middleware giriş noktası
    # ------------------------------------------------------------------

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Her HTTP isteğini yakalar, hız sınırını uygular ve sonucu döndürür.

        429 yanıtına ``Retry-After`` başlığı eklenir.
        """
        ip = self._client_ip(request)
        state = self._states[ip]
        now = time.monotonic()
        wall_now = time.time()

        async with state.lock:
            count = self._prune_and_count(state, now)

            if count >= self._limit:
                # En eski damganın ne zaman dolacağını hesapla
                oldest = state.timestamps[0]
                retry_after = max(1, int(oldest + self._WINDOW_SECONDS - now) + 1)
                reset_at = int(wall_now + retry_after)

                logger.warning(
                    "Rate limit exceeded: ip=%s count=%d limit=%d retry_after=%ds",
                    ip,
                    count,
                    self._limit,
                    retry_after,
                )
                return JSONResponse(
                    status_code=429,
                    content={
                        "detail": "Too Many Requests",
                        "retry_after_seconds": retry_after,
                    },
                    headers={
                        "Retry-After": str(retry_after),
                        "X-Rate-Limit-Limit": str(self._limit),
                        "X-Rate-Limit-Remaining": "0",
                        "X-Rate-Limit-Reset": str(reset_at),
                    },
                )

            # Zaman damgasını kaydet
            state.timestamps.append(now)
            remaining = max(0, self._limit - count - 1)

        # Pencerenin sıfırlanacağı zamanı en eski damgadan hesapla
        async with state.lock:
            if state.timestamps:
                oldest = state.timestamps[0]
                reset_at = int(wall_now + max(0.0, oldest + self._WINDOW_SECONDS - now))
            else:
                reset_at = int(wall_now + self._WINDOW_SECONDS)

        response = await call_next(request)
        response.headers["X-Rate-Limit-Limit"] = str(self._limit)
        response.headers["X-Rate-Limit-Remaining"] = str(remaining)
        response.headers["X-Rate-Limit-Reset"] = str(reset_at)
        return response
