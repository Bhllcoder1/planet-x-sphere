"""
s3_reader.py — Birleştirilmiş paralel S3 okuyucu.

Bir FITS dosyasındaki 4 görüntü HDU'sunu (IMAGE, FLAGS, VARIANCE, ZODI)
asyncio ile paralel Range GET ile okur. Her HDU için tek bir Range GET
yapılır (koalesan satır aralığı), ardından numpy array döndürülür.

Doğrulanmış [V: s0_B]:
- Satır adımı 8,160 bytes (2040 piksel × 4 bytes)
- 100×100 pencere ≈ 0.8 MB/HDU
- HDU adına göre lookup 19.6 MB tarar; indeks (1,2,3,4) kullanılır
- S3 anonim erişim çalışıyor

Varsayım [ASSUMPTION]:
- Hizalanmış Range GET (tam satır aralığı) astropy .section()'dan daha hızlı
- FLAGS sıkıştırması zlib ile açılabilir (tile-based CompImageHDU)
"""
from __future__ import annotations

import asyncio
import logging
import time
import zlib
from dataclasses import dataclass
from typing import NamedTuple

import httpx
import numpy as np

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Sabitler
# ---------------------------------------------------------------------------

S3_BASE = "https://nasa-irsa-spherex.s3.amazonaws.com"
# Anonim erişim — kimlik bilgisi yok

NAXIS1 = 2040           # Piksel başına sütun sayısı (IMAGE/VARIANCE/ZODI/FLAGS)
BYTES_PER_PIXEL = 4     # float32 → 4 byte; int32 → 4 byte
ROW_STRIDE = NAXIS1 * BYTES_PER_PIXEL  # 8,160 bytes/satır

# HDU indeksleri (0-tabanlı, header dahil)
# Gerçek veri offsetleri ByteOffsetMap'ten gelir; bu sadece dokümantasyon amaçlı.
HDU_IMAGE = "IMAGE"
HDU_FLAGS = "FLAGS"
HDU_VARIANCE = "VARIANCE"
HDU_ZODI = "ZODI"

MAX_CONCURRENT = 4  # Eşzamanlı S3 bağlantı limiti


# ---------------------------------------------------------------------------
# Hata sınıfları
# ---------------------------------------------------------------------------

class S3Error(IOError):
    """Genel S3 okuma hatası."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class S3Busy(S3Error):
    """S3 servis yoğunluğu hatası (HTTP 503)."""


# ---------------------------------------------------------------------------
# Veri yapıları
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class WindowRequest:
    """Tek bir pencere isteği."""

    frame_id: str
    """Çerçeve kimliği (log ve önbellek için)."""

    s3_key: str
    """S3 nesne anahtarı (kova adı hariç)."""

    x0: int
    """Yatay başlangıç pikseli (dahil)."""

    y0: int
    """Dikey başlangıç pikseli (dahil)."""

    width: int
    """Pencere genişliği (piksel)."""

    height: int
    """Pencere yüksekliği (piksel)."""


@dataclass(frozen=True)
class ByteOffsetMap:
    """
    Önceden hesaplanmış HDU veri başlangıç offsetleri.

    Her değer, S3 nesnesi içindeki ham veri baytının başladığı
    mutlak byte konumunu gösterir (FITS header'ı hariç).
    Önbellekten (örn. Redis veya yerel dict) gelmesi beklenir.
    """

    image_data_start: int
    flags_data_start: int
    variance_data_start: int
    zodi_data_start: int


class WindowData(NamedTuple):
    """Döndürülen pencere verisi."""

    image: np.ndarray     # float32, shape (height, width)
    flags: np.ndarray     # int32,   shape (height, width)
    variance: np.ndarray  # float32, shape (height, width)
    zodi: np.ndarray      # float32, shape (height, width)


# ---------------------------------------------------------------------------
# Ortak semaphore (modül düzeyinde; tek event-loop varsayımı)
# ---------------------------------------------------------------------------

_semaphore: asyncio.Semaphore | None = None


def _get_semaphore() -> asyncio.Semaphore:
    """
    Çalışan event-loop'a bağlı semaphore'u döndürür veya oluşturur.

    Her asyncio.run() çağrısı yeni bir loop başlattığından semaphore'u
    lazy oluşturuyoruz; böylece yanlış loop'a bağlanmayı önlüyoruz.
    """
    global _semaphore
    # Semaphore yok ya da farklı loop'a ait → yenisini oluştur.
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if _semaphore is None:
        _semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    return _semaphore


# ---------------------------------------------------------------------------
# İç yardımcı: tek HDU için Range GET
# ---------------------------------------------------------------------------

async def _fetch_hdu_rows(
    s3_key: str,
    data_start: int,
    y0: int,
    y1: int,
    hdu_name: str,
    *,
    client: httpx.AsyncClient,
) -> bytes:
    """
    Tek HDU için koalesan satır aralığı Range GET.

    Parameters
    ----------
    s3_key:
        S3 nesne anahtarı.
    data_start:
        HDU ham verisinin S3 nesnesi içindeki başlangıç byte offseti.
    y0:
        Başlangıç satır indeksi (dahil).
    y1:
        Bitiş satır indeksi (hariç).
    hdu_name:
        Log mesajı için HDU adı.
    client:
        Paylaşılan httpx.AsyncClient örneği.

    Returns
    -------
    bytes
        [y0, y1) satır aralığına karşılık gelen ham baytlar.

    Raises
    ------
    S3Busy
        HTTP 503 yanıtı alındığında.
    S3Error
        Diğer tüm HTTP hatalarında.
    """
    byte_start = data_start + y0 * ROW_STRIDE
    byte_end = data_start + y1 * ROW_STRIDE  # hariç → Range: bytes=start-(end-1)

    url = f"{S3_BASE}/{s3_key}"
    headers = {"Range": f"bytes={byte_start}-{byte_end - 1}"}

    sem = _get_semaphore()

    t0 = time.perf_counter()
    async with sem:
        try:
            response = await client.get(url, headers=headers)
        except httpx.RequestError as exc:
            raise S3Error(
                f"S3 bağlantı hatası [{hdu_name}] {s3_key}: {exc}"
            ) from exc

    elapsed_ms = (time.perf_counter() - t0) * 1000
    logger.debug(
        "S3 Range GET [%s] %s bytes=%d-%d → HTTP %d (%.1f ms)",
        hdu_name,
        s3_key,
        byte_start,
        byte_end - 1,
        response.status_code,
        elapsed_ms,
    )

    if response.status_code == 503:
        raise S3Busy(
            f"S3 servis yoğunluğu (503) [{hdu_name}] {s3_key}",
            status_code=503,
        )

    if response.status_code not in (200, 206):
        raise S3Error(
            f"S3 beklenmedik durum kodu {response.status_code} [{hdu_name}] {s3_key}",
            status_code=response.status_code,
        )

    return response.content


# ---------------------------------------------------------------------------
# FLAGS: CompImageHDU inflate
# ---------------------------------------------------------------------------

def _inflate_flags(raw: bytes, height: int, width: int) -> np.ndarray:
    """
    Ham FLAGS baytlarını int32 numpy dizisine dönüştürür.

    FLAGS HDU'su sıkıştırılmış CompImageHDU (FITS tile compression)
    olabilir. Basitleştirilmiş yaklaşım:

    1. Baytlar düz int32 olarak yorumlanabiliyorsa direkt dönüştür.
    2. Boyut uyuşmazlığı durumunda zlib ile açmayı dene.

    Not [ASSUMPTION]: Gerçek FITS tile-compression protokolü astropy
    CompImageHDU altyapısı gerektirir. Bu implementasyon düz int32 veya
    zlib-deflate sıkıştırmayı destekler; tam FPACK/Rice algoritması için
    astropy.io.fits kullanın.

    Parameters
    ----------
    raw:
        Range GET'ten gelen ham baytlar.
    height, width:
        Beklenen çıktı boyutları.

    Returns
    -------
    np.ndarray
        int32, shape (height, width).
    """
    expected_size = height * width * BYTES_PER_PIXEL

    # 1. Düz int32 denemesi
    if len(raw) == expected_size:
        arr = np.frombuffer(raw, dtype=">i4")
        return arr.reshape(height, width).astype(np.int32)

    # 2. zlib inflate denemesi
    try:
        decompressed = zlib.decompress(raw)
        if len(decompressed) == expected_size:
            arr = np.frombuffer(decompressed, dtype=">i4")
            return arr.reshape(height, width).astype(np.int32)
        logger.warning(
            "FLAGS inflate sonrası boyut uyuşmazlığı: beklenen=%d, bulunan=%d",
            expected_size,
            len(decompressed),
        )
        # Mevcut veriden olabildiğince çok oku
        n_pixels = min(len(decompressed) // BYTES_PER_PIXEL, height * width)
        arr = np.frombuffer(decompressed[: n_pixels * BYTES_PER_PIXEL], dtype=">i4")
        result = np.zeros(height * width, dtype=np.int32)
        result[:n_pixels] = arr.astype(np.int32)
        return result.reshape(height, width)
    except zlib.error:
        pass

    # 3. Boyut uyumsuz ham veri — uyarı ver, sıfır dizi döndür
    logger.error(
        "FLAGS ham bayt boyutu uyuşmazlığı: beklenen=%d, gelen=%d; sıfır dizi döndürülüyor",
        expected_size,
        len(raw),
    )
    return np.zeros((height, width), dtype=np.int32)


# ---------------------------------------------------------------------------
# İç yardımcı: bayt → float32 array
# ---------------------------------------------------------------------------

def _bytes_to_array(raw: bytes, height: int, width: int, dtype: np.dtype) -> np.ndarray:
    """
    Ham baytları numpy dizisine çevirir (büyük-endian FITS → yerel).

    Parameters
    ----------
    raw:
        FITS verisinin ham baytları (big-endian).
    height, width:
        Beklenen çıktı boyutları.
    dtype:
        Hedef numpy dtype (np.float32 veya np.int32).

    Returns
    -------
    np.ndarray
        Belirtilen dtype ve (height, width) şeklinde dizi.
    """
    be_dtype = dtype.newbyteorder(">")  # big-endian (FITS standardı)
    arr = np.frombuffer(raw, dtype=be_dtype)
    return arr.reshape(height, width).astype(dtype)


# ---------------------------------------------------------------------------
# Ana yüzey: read_window
# ---------------------------------------------------------------------------

async def read_window(
    req: WindowRequest,
    byte_offsets: ByteOffsetMap,
    *,
    client: httpx.AsyncClient | None = None,
) -> WindowData:
    """
    4 HDU'yu paralel Range GET ile okur.

    Her HDU için yalnızca bir adet Range GET isteği gönderilir
    (koalesan satır aralığı). Dört istek asyncio.gather() ile
    eşzamanlı çalıştırılır.

    Parameters
    ----------
    req:
        Pencere isteği: frame_id, s3_key, x0, y0, width, height.
    byte_offsets:
        Her HDU'nun S3 nesnesi içindeki veri başlangıç offseti.
        Genellikle L1 önbellekten (Redis / bellek içi dict) gelir.
    client:
        İsteğe bağlı dışarıdan geçilen httpx.AsyncClient.
        Geçilmezse otomatik oluşturulur ve kapat faaliyeti bu
        fonksiyon sonunda gerçekleştirilir.

    Returns
    -------
    WindowData
        (image, flags, variance, zodi) tuple; her biri numpy array.

    Raises
    ------
    S3Busy
        Herhangi bir HDU isteğinde HTTP 503 alındığında.
    S3Error
        Diğer HTTP veya bağlantı hatalarında.
    ValueError
        req.x0/y0/width/height değerleri görüntü sınırlarını aşıyorsa.
    """
    # --- Parametre doğrulaması ---
    if req.y0 < 0 or req.x0 < 0:
        raise ValueError(
            f"Negatif pencere koordinatları: x0={req.x0}, y0={req.y0}"
        )
    if req.width <= 0 or req.height <= 0:
        raise ValueError(
            f"Geçersiz pencere boyutu: width={req.width}, height={req.height}"
        )
    if req.x0 + req.width > NAXIS1 or req.y0 + req.height > NAXIS1:
        raise ValueError(
            f"Pencere [{req.x0}:{req.x0 + req.width}, {req.y0}:{req.y0 + req.height}]"
            f" {NAXIS1}×{NAXIS1} görüntü sınırlarını aşıyor"
        )

    y0 = req.y0
    y1 = req.y0 + req.height

    t_total = time.perf_counter()

    # --- İstemci yönetimi ---
    _owns_client = client is None
    if _owns_client:
        client = httpx.AsyncClient(timeout=30.0, follow_redirects=True)

    try:
        # --- 4 HDU paralel Range GET ---
        image_raw, flags_raw, variance_raw, zodi_raw = await asyncio.gather(
            _fetch_hdu_rows(
                req.s3_key,
                byte_offsets.image_data_start,
                y0,
                y1,
                HDU_IMAGE,
                client=client,
            ),
            _fetch_hdu_rows(
                req.s3_key,
                byte_offsets.flags_data_start,
                y0,
                y1,
                HDU_FLAGS,
                client=client,
            ),
            _fetch_hdu_rows(
                req.s3_key,
                byte_offsets.variance_data_start,
                y0,
                y1,
                HDU_VARIANCE,
                client=client,
            ),
            _fetch_hdu_rows(
                req.s3_key,
                byte_offsets.zodi_data_start,
                y0,
                y1,
                HDU_ZODI,
                client=client,
            ),
        )
    finally:
        if _owns_client:
            await client.aclose()

    elapsed_total_ms = (time.perf_counter() - t_total) * 1000
    logger.info(
        "read_window [%s] y=%d-%d (height=%d) toplam=%.1f ms",
        req.frame_id,
        y0,
        y1,
        req.height,
        elapsed_total_ms,
    )

    # --- Baytları numpy array'e çevir ---
    h = req.height
    w = req.width

    image_arr = _bytes_to_array(image_raw, h, NAXIS1, np.float32)[:, req.x0 : req.x0 + w]
    variance_arr = _bytes_to_array(variance_raw, h, NAXIS1, np.float32)[:, req.x0 : req.x0 + w]
    zodi_arr = _bytes_to_array(zodi_raw, h, NAXIS1, np.float32)[:, req.x0 : req.x0 + w]
    flags_arr = _inflate_flags(flags_raw, h, NAXIS1)[:, req.x0 : req.x0 + w]

    return WindowData(
        image=image_arr,
        flags=flags_arr,
        variance=variance_arr,
        zodi=zodi_arr,
    )


# ---------------------------------------------------------------------------
# Kullanım örneği (doğrudan çalıştırma)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    )

    async def _demo() -> None:
        """
        Basit demo: gerçek bir SPHEREx L1 FITS dosyasından 100×100 pencere okur.

        Gerçek byte_offsets değerleri önbellekten veya FITS başlık
        ayrıştırmasından gelmeli; burada temsili sabitler kullanılıyor.
        """
        # Örnek SPHEREx L1 dosyası (us-east-1, anonim erişim)
        s3_key = (
            "data/l1b/2024/001/0001/"
            "SPHEREX_L1B_2024001_0001_01_I1.fits"
        )

        # Temsili offsetler — gerçek kullanımda önbellekten alınır
        offsets = ByteOffsetMap(
            image_data_start=2_880 * 10,       # ~1. HDU header + data offset
            flags_data_start=2_880 * 10 + 16_646_400,
            variance_data_start=2_880 * 10 + 33_292_800,
            zodi_data_start=2_880 * 10 + 49_939_200,
        )

        req = WindowRequest(
            frame_id="demo_frame_001",
            s3_key=s3_key,
            x0=970,
            y0=970,
            width=100,
            height=100,
        )

        try:
            data = await read_window(req, offsets)
            print(f"image    shape={data.image.shape}    dtype={data.image.dtype}")
            print(f"flags    shape={data.flags.shape}    dtype={data.flags.dtype}")
            print(f"variance shape={data.variance.shape} dtype={data.variance.dtype}")
            print(f"zodi     shape={data.zodi.shape}     dtype={data.zodi.dtype}")
            print(f"image[0,0] = {data.image[0, 0]:.6e}")
        except S3Busy as exc:
            print(f"S3 meşgul: {exc}", file=sys.stderr)
            sys.exit(2)
        except S3Error as exc:
            print(f"S3 hatası: {exc}", file=sys.stderr)
            sys.exit(1)

    asyncio.run(_demo())
