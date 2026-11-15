"""
mock_server.py — SPHEREx Viewer API sahte sunucusu.

Gerçek S3 veya TAP çağrısı yapmaz; sabit/sentetik verilerle yanıt verir.
Alan D (arayüz) ve Alan A (veri işleme), Alan C sunucusu hazır olmadan
bu sunucuyla geliştirme ve entegrasyon testleri yapabilir.

Çalıştırma:
    uvicorn c_sunucu.api.mock_server:app --reload --port 8000

Bağımlılıklar (pyproject.toml veya requirements.txt'e ekle):
    fastapi>=0.111
    uvicorn[standard]>=0.29
    numpy>=1.26
    Pillow>=10.3        # thumbnail PNG üretimi için
    pydantic>=2.6
"""
from __future__ import annotations

import base64
import io
import time
from typing import Optional

import numpy as np
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Pydantic modelleri (OpenAPI sözleşmesiyle birebir eşleşir)
# ---------------------------------------------------------------------------

class Target(BaseModel):
    id: str
    name: str
    ra_j2000: float
    dec_j2000: float
    n_frames: int
    n_passes: int


class Frame(BaseModel):
    frame_id: str
    target_id: str
    detector: str
    pass_: int = Field(alias="pass")
    mjd_avg: float
    sps_epa: float
    s3_key: str

    model_config = {"populate_by_name": True}


class WindowData(BaseModel):
    image: list[float]
    flags: list[float]
    variance: list[float]
    zodi: list[float]


class Window(BaseModel):
    frame_id: str
    x0: int
    y0: int
    width: int
    height: int
    data: WindowData


class Thumbnail(BaseModel):
    frame_id: str
    png_base64: str


class Status(BaseModel):
    healthy: bool
    version: str
    cache_fill_pct: float
    last_error: Optional[str]


# ---------------------------------------------------------------------------
# Sabit hedef kataloğu
# ---------------------------------------------------------------------------

_TARGETS: list[Target] = [
    Target(
        id="barnard",
        name="Barnard's Star",
        ra_j2000=269.4521,
        dec_j2000=4.6933,
        n_frames=48,
        n_passes=6,
    ),
    Target(
        id="eps_indi_b",
        name="ε Indi B",
        ra_j2000=330.8408,
        dec_j2000=-56.7858,
        n_frames=36,
        n_passes=4,
    ),
    Target(
        id="wise0855",
        name="WISE J085510.83-071442.5",
        ra_j2000=133.7951,
        dec_j2000=-7.2451,
        n_frames=24,
        n_passes=3,
    ),
    Target(
        id="rw_aur",
        name="RW Aurigae",
        ra_j2000=74.7571,
        dec_j2000=30.4015,
        n_frames=60,
        n_passes=8,
    ),
    Target(
        id="r_dra",
        name="R Draconis",
        ra_j2000=273.3608,
        dec_j2000=68.0417,
        n_frames=72,
        n_passes=9,
    ),
]

_TARGET_INDEX: dict[str, Target] = {t.id: t for t in _TARGETS}


# ---------------------------------------------------------------------------
# Sabit kare (frame) kataloğu
#
# Her hedef için 3 temsili kare tanımlanmıştır. Gerçek sunucu bunları
# S3 manifest dosyasından okuyacaktır; sahte sunucu bunları bellekte tutar.
# ---------------------------------------------------------------------------

def _make_frames(target_id: str, base_mjd: float) -> list[Frame]:
    """Verilen hedef için 3 sabit kare üretir."""
    detectors = ["D1", "D2", "D3"]
    frames = []
    for i, det in enumerate(detectors):
        frame_id = f"{target_id}_{det}_p1_{i:04d}"
        frames.append(
            Frame.model_validate(
                {
                    "frame_id": frame_id,
                    "target_id": target_id,
                    "detector": det,
                    "pass": 1,
                    "mjd_avg": base_mjd + i * 0.5,
                    "sps_epa": 42.75 + i * 10.0,
                    "s3_key": (
                        f"cal/v01/{target_id}/"
                        f"spx_{frame_id}_cal.fits"
                    ),
                }
            )
        )
    return frames


_FRAMES_BY_TARGET: dict[str, list[Frame]] = {
    "barnard":    _make_frames("barnard",    60310.100),
    "eps_indi_b": _make_frames("eps_indi_b", 60312.200),
    "wise0855":   _make_frames("wise0855",   60314.300),
    "rw_aur":     _make_frames("rw_aur",     60316.400),
    "r_dra":      _make_frames("r_dra",      60318.500),
}

_FRAME_INDEX: dict[str, Frame] = {
    f.frame_id: f
    for frames in _FRAMES_BY_TARGET.values()
    for f in frames
}


# ---------------------------------------------------------------------------
# Sentetik piksel verisi üretimi (numpy, seed=42)
# ---------------------------------------------------------------------------

_RNG = np.random.default_rng(seed=42)


def _synth_array(width: int, height: int, low: float, high: float) -> list[float]:
    """row-major düzleştirilmiş float32 liste döndürür."""
    arr = _RNG.uniform(low, high, size=(height, width)).astype(np.float32)
    return arr.flatten().tolist()


def _synth_flags(width: int, height: int) -> list[float]:
    """Çoğunluğu 0, az bir kısmı 1 veya 2 olan bayrak dizisi."""
    arr = _RNG.choice([0, 1, 2], size=(height, width), p=[0.92, 0.06, 0.02])
    return arr.astype(np.float32).flatten().tolist()


# ---------------------------------------------------------------------------
# Thumbnail PNG üretimi
# ---------------------------------------------------------------------------

def _make_thumbnail_png(frame_id: str, size: int = 64) -> str:
    """
    64×64 piksel sentetik PNG döndürür (base64 kodlu).

    PIL/Pillow mevcut değilse son çare olarak standart kütüphane tabanlı
    1×1 şeffaf PNG kullanılır; bu durumda alan D'nin kendi küçük resmini
    görüntüleyemeyeceği göreceli olarak bellidir.
    """
    # Kare kimliğinden belirleyici bir tohum türet
    seed = sum(ord(c) for c in frame_id) % (2**31)
    rng = np.random.default_rng(seed=seed)
    pixels = rng.integers(0, 256, size=(size, size), dtype=np.uint8)

    try:
        from PIL import Image  # type: ignore[import-untyped]

        img = Image.fromarray(pixels, mode="L")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode("ascii")
    except ImportError:
        # Pillow yüklü değil — minimal geçerli 1×1 piksel gri PNG döndür
        # RFC 2083 §12.14 örnek küçük PNG (sıkıştırılmış, standart)
        MINIMAL_1X1_GRAY_PNG = (
            b"\x89PNG\r\n\x1a\n"             # imza
            b"\x00\x00\x00\rIHDR"            # IHDR chunk uzunluğu
            b"\x00\x00\x00\x01"              # genişlik=1
            b"\x00\x00\x00\x01"              # yükseklik=1
            b"\x08\x00\x00\x00\x00"          # 8-bit gri, sıkıştırma/filtre/interlace
            b":~\x9bU"                        # IHDR CRC
            b"\x00\x00\x00\nIDATx\x9cc`\x00\x00\x00\x02\x00\x01"
            b"\xe2!\xbc3"                     # IDAT CRC
            b"\x00\x00\x00\x00IEND\xaeB`\x82"
        )
        return base64.b64encode(MINIMAL_1X1_GRAY_PNG).decode("ascii")


# ---------------------------------------------------------------------------
# FastAPI uygulaması
# ---------------------------------------------------------------------------

app = FastAPI(
    title="SPHEREx Viewer API (mock)",
    version="0.1.0",
    description=(
        "Gerçek S3 veya TAP çağrısı yapmayan sahte sunucu. "
        "Alan D ve Alan A için geliştirme ortamı sağlar."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

_SERVER_START = time.time()


# ---------------------------------------------------------------------------
# Uç noktalar
# ---------------------------------------------------------------------------

@app.get(
    "/targets",
    response_model=list[Target],
    summary="Tüm bilim hedeflerini listele",
    tags=["targets"],
)
def list_targets() -> list[Target]:
    """Beş önceden tanımlı SPHEREx hedefini sabit sırada döndürür."""
    return _TARGETS


@app.get(
    "/targets/{target_id}/frames",
    response_model=list[Frame],
    summary="Bir hedef için kare manifestini listele",
    tags=["targets", "frames"],
)
def list_frames(
    target_id: str,
    detector: Optional[str] = Query(default=None, description="Dedektör filtresi"),
    pass_: Optional[int] = Query(default=None, alias="pass", ge=1, description="Geçiş numarası filtresi"),
) -> list[Frame]:
    if target_id not in _TARGET_INDEX:
        raise HTTPException(
            status_code=404,
            detail=f"Hedef '{target_id}' bulunamadı.",
        )
    frames = _FRAMES_BY_TARGET[target_id]
    if detector is not None:
        frames = [f for f in frames if f.detector == detector]
    if pass_ is not None:
        frames = [f for f in frames if f.pass_ == pass_]
    return frames


@app.get(
    "/frames/{frame_id}/window",
    response_model=Window,
    summary="Bir kareden piksel penceresi al",
    tags=["frames"],
)
def get_window(
    frame_id: str,
    x0: int = Query(default=0, ge=0, description="Sol kenar (piksel, 0-tabanlı)"),
    y0: int = Query(default=0, ge=0, description="Alt kenar (piksel, 0-tabanlı)"),
    width: int = Query(default=100, ge=1, le=2048, description="Pencere genişliği"),
    height: int = Query(default=100, ge=1, le=2048, description="Pencere yüksekliği"),
    hdus: str = Query(
        default="image,flags,variance,zodi",
        description="Virgülle ayrılmış katman listesi",
    ),
) -> Window:
    if frame_id not in _FRAME_INDEX:
        raise HTTPException(
            status_code=404,
            detail=f"Kare '{frame_id}' bulunamadı.",
        )

    requested = {h.strip().lower() for h in hdus.split(",")}
    valid_hdus = {"image", "flags", "variance", "zodi"}
    invalid = requested - valid_hdus
    if invalid:
        raise HTTPException(
            status_code=422,
            detail=f"Geçersiz katman adları: {sorted(invalid)}. "
                   f"Geçerli değerler: {sorted(valid_hdus)}.",
        )

    n = width * height
    data = WindowData(
        image=_synth_array(width, height, low=0.1, high=5.0) if "image" in requested else [0.0] * n,
        flags=_synth_flags(width, height) if "flags" in requested else [0.0] * n,
        variance=_synth_array(width, height, low=1e-4, high=1e-2) if "variance" in requested else [0.0] * n,
        zodi=_synth_array(width, height, low=0.5, high=2.0) if "zodi" in requested else [0.0] * n,
    )

    return Window(
        frame_id=frame_id,
        x0=x0,
        y0=y0,
        width=width,
        height=height,
        data=data,
    )


@app.get(
    "/frames/{frame_id}/thumbnail",
    response_model=Thumbnail,
    summary="Kare için küçük resim PNG'si al",
    tags=["frames"],
)
def get_thumbnail(frame_id: str) -> Thumbnail:
    if frame_id not in _FRAME_INDEX:
        raise HTTPException(
            status_code=404,
            detail=f"Kare '{frame_id}' bulunamadı.",
        )
    return Thumbnail(
        frame_id=frame_id,
        png_base64=_make_thumbnail_png(frame_id),
    )


@app.get(
    "/status",
    response_model=Status,
    summary="Sunucu durumunu sorgula",
    tags=["targets"],
)
def get_status() -> Status:
    uptime = time.time() - _SERVER_START
    # Sentetik önbellek doluluk yüzdesi: zamanla logaritmik artış, 80'de doyum
    fill = min(80.0, uptime / 60.0 * 10.0)
    return Status(
        healthy=True,
        version="0.1.0",
        cache_fill_pct=round(fill, 1),
        last_error=None,
    )
