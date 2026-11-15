from __future__ import annotations

"""
SPHEREx FastAPI uygulaması.

Kullanım:
    python -m api.main
    uvicorn api.main:app --reload
"""

import logging
import logging.config
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, AsyncGenerator

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from api.routes import (
    auth,
    export,
    fits_export,
    frames,
    health,
    history,
    profile,
    share,
    targets,
)

# ---------------------------------------------------------------------------
# Ayarlar
# ---------------------------------------------------------------------------


class Settings(BaseSettings):
    """
    Uygulama ayarları — .env dosyasından veya ortam değişkenlerinden okunur.

    Alanlar:
        app_env:       Ortam adı; 'development' veya 'production'.
        app_port:      Uvicorn dinleme portu.
        l0_cache_dir:  Ham veri önbellek dizini (manifest dosyaları burada).
        l1_cache_dir:  Ara işlem önbellek dizini.
        l2_cache_dir:  Önceden hesaplanmış çıktı dizini (.npy, .png).
    """

    app_env: str = Field(default="development", alias="APP_ENV")
    app_port: int = Field(default=8000, alias="APP_PORT")
    l0_cache_dir: str = Field(default="cache/l0", alias="L0_CACHE_DIR")
    l1_cache_dir: str = Field(default="cache/l1", alias="L1_CACHE_DIR")
    l2_cache_dir: str = Field(default="cache/l2", alias="L2_CACHE_DIR")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )


# ---------------------------------------------------------------------------
# Loglama
# ---------------------------------------------------------------------------


def _configure_logging(settings: Settings) -> None:
    """Uvicorn uyumlu loglama yapılandırmasını kurar."""
    level = "DEBUG" if settings.app_env == "development" else "INFO"
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "()": "uvicorn.logging.DefaultFormatter",
                    "fmt": "%(levelprefix)s %(asctime)s | %(name)s | %(message)s",
                    "use_colors": None,
                },
            },
            "handlers": {
                "default": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stderr",
                },
            },
            "root": {
                "handlers": ["default"],
                "level": level,
            },
        }
    )


# ---------------------------------------------------------------------------
# Lifespan
# ---------------------------------------------------------------------------


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Uygulama yaşam döngüsü yöneticisi.

    Başlangıçta L2 önbellek dizininin var olup olmadığını kontrol eder.
    """
    logger = logging.getLogger(__name__)
    settings: Settings = app.state.settings

    l2_path = Path(settings.l2_cache_dir)
    if not l2_path.is_dir():
        logger.warning(
            "L2 önbellek dizini bulunamadı: %s — sunucu degraded modda başlıyor",
            l2_path,
        )
    else:
        logger.info("L2 önbellek dizini mevcut: %s", l2_path)

    yield  # uygulama çalışıyor

    logger.info("SPHEREx API sunucusu kapatılıyor")


# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------


def _cors_origins(settings: Settings) -> list[str]:
    """
    Ortama göre izin verilen CORS kaynaklarını döndürür.

    Geliştirmede tüm kaynaklara izin verilir; üretimde kısıtlanır.
    """
    if settings.app_env == "development":
        return ["*"]
    return [
        "https://planet-x-sphere.pages.dev",
        "https://localhost:3000",
        "http://localhost:3000",
        "http://localhost:5173",
    ]


# ---------------------------------------------------------------------------
# Fabrika
# ---------------------------------------------------------------------------


def create_app(settings: Settings | None = None) -> FastAPI:
    """
    FastAPI uygulama örneği oluşturur ve yapılandırır.

    Args:
        settings: Özel ayar nesnesi; None ise ortam değişkenlerinden okunur.

    Returns:
        Yapılandırılmış FastAPI uygulaması.
    """
    if settings is None:
        settings = Settings()

    _configure_logging(settings)

    application = FastAPI(
        title="SPHEREx Planet-X API",
        description=(
            "NASA SPHEREx veri arşivine erişim sağlayan REST API. "
            "Önceden hesaplanmış kare pencereleri ve manifest uç noktaları."
        ),
        version="0.1.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # Ayarları uygulama durumuna bağla (route handler'lar request.app.state.settings ile erişir)
    application.state.settings = settings

    # CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=_cors_origins(settings),
        allow_credentials=True,
        allow_methods=["GET", "OPTIONS"],
        allow_headers=["*"],
    )

    # Route'ları kaydet
    application.include_router(health.router)
    application.include_router(targets.router)
    application.include_router(frames.router)
    application.include_router(auth.router)
    application.include_router(history.router)
    application.include_router(profile.router)
    application.include_router(share.router)
    application.include_router(export.router)
    application.include_router(fits_export.router)

    # Özel hata işleyicileri
    _register_error_handlers(application)

    return application


# ---------------------------------------------------------------------------
# Hata işleyicileri
# ---------------------------------------------------------------------------


def _register_error_handlers(app: FastAPI) -> None:
    """404 ve 500 HTTP hatalarını JSON olarak döndüren işleyicileri kaydeder."""

    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc: Any) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={
                "error": "not_found",
                "detail": "The requested resource was not found.",
                "path": str(request.url.path),
            },
        )

    @app.exception_handler(500)
    async def internal_error_handler(request: Request, exc: Any) -> JSONResponse:
        logging.getLogger(__name__).exception(
            "İşlenmeyen hata: %s %s", request.method, request.url.path
        )
        return JSONResponse(
            status_code=500,
            content={
                "error": "internal_server_error",
                "detail": "An unexpected error occurred. Please try again later.",
            },
        )


# ---------------------------------------------------------------------------
# Uygulama örneği (doğrudan uvicorn için)
# ---------------------------------------------------------------------------

app = create_app()

# ---------------------------------------------------------------------------
# Giriş noktası
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    _settings = Settings()
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=_settings.app_port,
        reload=_settings.app_env == "development",
        log_level="debug" if _settings.app_env == "development" else "info",
        access_log=True,
    )
