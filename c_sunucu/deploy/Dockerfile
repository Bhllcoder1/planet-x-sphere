# =============================================================================
# Dockerfile — Planet-X Sphere API Sunucusu
# Çok aşamalı (multi-stage) yapı: küçük son imaj, hızlı katman önbelleği
# =============================================================================

# -----------------------------------------------------------------------------
# Aşama 1: bağımlılıklar
# Sadece Python paketlerini kurar; uygulama kodu bu aşamaya kopyalanmaz.
# Bu sayede bağımlılıklar değişmediği sürece bu katman önbellekten kullanılır.
# -----------------------------------------------------------------------------
FROM python:3.13-slim AS deps

WORKDIR /app

# Önce sadece requirements.txt kopyala — kod değiştiğinde bu katman yeniden
# oluşturulmaz; bağımlılıklar değiştiğinde oluşturulur.
COPY c_sunucu/requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# -----------------------------------------------------------------------------
# Aşama 2: uygulama (son imaj)
# deps aşamasından yalnızca kurulu paketleri kopyalar; pip ve build araçları
# son imaja dahil edilmez → daha küçük saldırı yüzeyi.
# -----------------------------------------------------------------------------
FROM python:3.13-slim

# Ortam değişkenleri
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Sistem bağımlılıkları (libgomp: numpy OpenBLAS için)
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgomp1 curl \
    && rm -rf /var/lib/apt/lists/*

# Sadece kurulu Python paketlerini önceki aşamadan al
COPY --from=deps /usr/local/lib/python3.13/site-packages \
                 /usr/local/lib/python3.13/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin

# Uygulama kaynak kodunu kopyala
COPY c_sunucu/ .

# Önbellek dizinleri dışarıda tutulur (volume ile bağlanır)
# /data/cache → S3 tile önbelleği; konteyner yeniden başlatılsa bile korunur
VOLUME ["/data/cache"]

# Uygulama portu
EXPOSE 8000

# Sağlık kontrolü: API /health endpoint'ini 30 saniyede bir kontrol eder
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Çalıştırıcı: uvicorn, production modunda, single-worker (Caddy önünde)
# Birden fazla worker için Gunicorn + uvicorn.workers.UvicornWorker kullanın
CMD ["uvicorn", "api.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--no-access-log"]
