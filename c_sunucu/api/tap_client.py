"""
tap_client.py — Asenkron IRSA TAP istemcisi.

IRSA'nın TAP servisine async iş gönderir, 15 dk boyunca poll eder,
başarısız olursa backoff ile yeniden dener.

Doğrulanmış davranışlar [V: s0_A, s0_B]:
- Barnard sorgusu ~202 s sürdü; 5 dk sınırına yakın
- 3/6 hedef TAP başarısız (HTTP 502, zaman aşımı)
- INTERSECTS ve OR tabanlı sorgular BAD_REQUEST döndürür
- 'cloud_access' kolonu yok; S3 key = uri - 'ibe/data/spherex/'
"""
from __future__ import annotations

import asyncio
import logging
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Optional

import httpx

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Sabitler
# ---------------------------------------------------------------------------
TAP_BASE = "https://irsa.ipac.caltech.edu/TAP"
MAX_POLL_SECONDS = 900          # 15 dakika tavan [V: s0_A]
POLL_INTERVAL_SECONDS = 15      # sorgu aralığı
BACKOFF_SECONDS = (30, 60, 120) # 502/503 sonrası bekleme aralıkları (sn)

# VOTable XML ad alanları
_VOTABLE_NS = {
    "v": "http://www.ivoa.net/xml/VOTable/v1.3",
    "v1": "http://www.ivoa.net/xml/VOTable/v1.2",
    "v0": "http://www.ivoa.net/xml/VOTable/v1.1",
}


# ---------------------------------------------------------------------------
# Veri sınıfları
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class TapFrame:
    """TAP sorgusundan dönen tek kare kaydı."""
    frame_id: str       # planeid
    s3_key: str         # uri -> S3 key dönüşümü
    detector: str       # ipac_gid (dedektör tanımlayıcısı)
    mjd_avg: float      # lastmodified (yaklaşık MJD; gerçek MJD gelecek versiyonda)
    sps_epa: float      # artifactid'den türetilen SPS epa (henüz şema doğrulanmadı)
    content_length: int # contentlength


# ---------------------------------------------------------------------------
# İstisna sınıfları
# ---------------------------------------------------------------------------

class TapError(Exception):
    """TAP sorgusunda kurtarılamaz hata."""


class TapBusy(Exception):
    """TAP servisi meşgul; yeniden deneme önerilir."""


# ---------------------------------------------------------------------------
# Yardımcı fonksiyonlar
# ---------------------------------------------------------------------------

def _build_adql(ra: float, dec: float, collection: str) -> str:
    """
    Verilen koordinat ve koleksiyon için ADQL sorgusu üretir.

    CONTAINS(POINT, poly) formatı kullanılır. INTERSECTS ve OR
    operatörleri IRSA tarafından reddedildiğinden kullanılmaz [V: s0_A].
    """
    return (
        "SELECT spherex.plane.planeid, spherex.artifact.artifactid, "
        "spherex.artifact.uri, spherex.artifact.producttype, "
        "spherex.artifact.contentlength, spherex.plane.ipac_gid, "
        "spherex.plane.lastmodified "
        "FROM spherex.artifact "
        "JOIN spherex.plane "
        "  ON spherex.artifact.planeid = spherex.plane.planeid "
        f"WHERE 1=CONTAINS(POINT('ICRS',{ra:.6f},{dec:.6f}), spherex.plane.poly) "
        "AND spherex.artifact.producttype='science' "
        f"AND spherex.plane.collection='{collection}'"
    )


def _uri_to_s3_key(uri: str) -> str:
    """
    IRSA URI'sini S3 key'ine dönüştürür.

    Önek 'ibe/data/spherex/' çıkarılır. [V: s0_B §1]
    """
    prefix = "ibe/data/spherex/"
    if uri.startswith(prefix):
        return uri[len(prefix):]
    return uri


def _parse_votable(xml_bytes: bytes) -> list[TapFrame]:
    """
    VOTable XML içeriğini TapFrame listesine dönüştürür.

    Basit xml.etree.ElementTree ile parse edilir; lxml gerektirmez.
    Ad alanı (namespace) farklılıklarına karşı dayanıklıdır.
    """
    root = ET.fromstring(xml_bytes)

    # Ad alanını dinamik olarak tespit et
    ns_uri = ""
    if root.tag.startswith("{"):
        ns_uri = root.tag.split("}")[0].lstrip("{")
    ns = {"v": ns_uri} if ns_uri else {}

    def find_all(parent: ET.Element, tag: str) -> list[ET.Element]:
        """Ad alanına duyarsız eleman arama."""
        if ns_uri:
            return parent.findall(f".//{{{ns_uri}}}{tag}")
        return parent.findall(f".//{tag}")

    # Kolon sırasını bul
    fields = find_all(root, "FIELD")
    col_names = [f.get("name", f.get("ID", "")).lower() for f in fields]
    logger.debug("VOTable kolonları: %s", col_names)

    def _col(name: str) -> int:
        """Kolon indeksini döndürür; bulunamazsa -1."""
        for i, c in enumerate(col_names):
            if c == name:
                return i
        return -1

    idx_planeid      = _col("planeid")
    idx_artifactid   = _col("artifactid")
    idx_uri          = _col("uri")
    idx_contentlen   = _col("contentlength")
    idx_ipac_gid     = _col("ipac_gid")
    idx_lastmodified = _col("lastmodified")

    frames: list[TapFrame] = []
    for tr in find_all(root, "TR"):
        cells = [td.text or "" for td in find_all(tr, "TD")]
        if not cells:
            continue

        def cell(idx: int, default: str = "") -> str:
            if idx < 0 or idx >= len(cells):
                return default
            return (cells[idx] or "").strip()

        uri       = cell(idx_uri)
        s3_key    = _uri_to_s3_key(uri)
        frame_id  = cell(idx_planeid)
        detector  = cell(idx_ipac_gid)
        artifact  = cell(idx_artifactid)

        try:
            content_length = int(cell(idx_contentlen, "0"))
        except ValueError:
            content_length = 0

        try:
            mjd_avg = float(cell(idx_lastmodified, "0"))
        except ValueError:
            mjd_avg = 0.0

        # sps_epa: artifactid'de gömülü; şema netleşince ayrıştırılacak
        sps_epa = 0.0

        frames.append(TapFrame(
            frame_id=frame_id,
            s3_key=s3_key,
            detector=detector,
            mjd_avg=mjd_avg,
            sps_epa=sps_epa,
            content_length=content_length,
        ))

    logger.info("VOTable parse tamamlandı: %d kare bulundu", len(frames))
    return frames


# ---------------------------------------------------------------------------
# Async TAP çekirdeği
# ---------------------------------------------------------------------------

async def _submit_job(
    client: httpx.AsyncClient,
    adql: str,
) -> str:
    """
    TAP async iş gönderir ve iş URL'ini döndürür.

    POST /async ile iş oluşturulur, ardından RUN fazına geçirilir.
    HTTP 502/503 durumunda TapBusy fırlatır.
    """
    submit_url = f"{TAP_BASE}/async"
    payload = {
        "LANG": "ADQL",
        "REQUEST": "doQuery",
        "QUERY": adql,
        "FORMAT": "votable",
    }
    logger.info("TAP async iş gönderiliyor: %s", submit_url)
    try:
        resp = await client.post(submit_url, data=payload, follow_redirects=False)
    except httpx.TimeoutException as exc:
        raise TapBusy(f"Submit timeout: {exc}") from exc
    except httpx.RequestError as exc:
        raise TapError(f"Submit request error: {exc}") from exc

    if resp.status_code in (502, 503):
        raise TapBusy(f"Submit HTTP {resp.status_code}: server busy")
    if resp.status_code not in (200, 201, 303):
        raise TapError(
            f"Submit failed with HTTP {resp.status_code}: {resp.text[:300]}"
        )

    # İş URL'i: Location header veya 200 body'de dönebilir
    job_url = resp.headers.get("Location", "")
    if not job_url:
        # Bazı TAP sunucuları 200 + XML body ile yanıt verir
        try:
            root = ET.fromstring(resp.content)
            job_id_el = root.find(".//{http://www.ivoa.net/xml/UWS/v1.0}jobId")
            if job_id_el is not None and job_id_el.text:
                job_url = f"{TAP_BASE}/async/{job_id_el.text.strip()}"
        except ET.ParseError:
            pass

    if not job_url:
        raise TapError("Submit succeeded but no job URL returned")

    # Göreli URL'yi mutlak yap
    if job_url.startswith("/"):
        base = str(client.base_url).rstrip("/") if client.base_url else TAP_BASE
        job_url = base + job_url

    logger.info("TAP iş oluşturuldu: %s", job_url)

    # Fazı RUN'a al
    phase_url = f"{job_url}/phase"
    try:
        run_resp = await client.post(phase_url, data={"PHASE": "RUN"})
    except httpx.RequestError as exc:
        raise TapError(f"Phase RUN request error: {exc}") from exc

    if run_resp.status_code not in (200, 303):
        raise TapError(
            f"Phase RUN failed with HTTP {run_resp.status_code}: {run_resp.text[:200]}"
        )

    logger.info("TAP iş çalıştırılıyor: %s", job_url)
    return job_url


async def _poll_job(
    client: httpx.AsyncClient,
    job_url: str,
) -> None:
    """
    TAP işi COMPLETED olana kadar poll eder.

    15 dakika içinde tamamlanmazsa TapBusy fırlatır.
    ERROR veya ABORTED durumunda TapError fırlatır.
    """
    phase_url = f"{job_url}/phase"
    deadline = time.monotonic() + MAX_POLL_SECONDS
    poll_count = 0

    while time.monotonic() < deadline:
        poll_count += 1
        elapsed = time.monotonic() - (deadline - MAX_POLL_SECONDS)
        logger.debug(
            "TAP poll #%d (%.0f s geçti): %s", poll_count, elapsed, phase_url
        )

        try:
            resp = await client.get(phase_url)
        except httpx.TimeoutException:
            logger.warning("TAP poll timeout, yeniden deneniyor...")
            await asyncio.sleep(POLL_INTERVAL_SECONDS)
            continue
        except httpx.RequestError as exc:
            raise TapError(f"Poll request error: {exc}") from exc

        if resp.status_code in (502, 503):
            logger.warning("TAP poll HTTP %d, yeniden deneniyor...", resp.status_code)
            await asyncio.sleep(POLL_INTERVAL_SECONDS)
            continue

        if resp.status_code != 200:
            raise TapError(f"Poll failed with HTTP {resp.status_code}: {resp.text[:200]}")

        phase = resp.text.strip().upper()
        logger.info("TAP iş fazı: %s (%.0f s geçti)", phase, elapsed)

        if phase == "COMPLETED":
            return
        if phase in ("ERROR", "ABORTED"):
            # Hata mesajını almaya çalış
            error_detail = ""
            try:
                err_resp = await client.get(job_url)
                if err_resp.status_code == 200:
                    root = ET.fromstring(err_resp.content)
                    msg_el = root.find(
                        ".//{http://www.ivoa.net/xml/UWS/v1.0}message"
                    )
                    if msg_el is not None and msg_el.text:
                        error_detail = msg_el.text.strip()
            except Exception:
                pass
            raise TapError(
                f"TAP job terminated with phase={phase}: {error_detail}"
            )
        if phase in ("PENDING", "QUEUED", "EXECUTING"):
            await asyncio.sleep(POLL_INTERVAL_SECONDS)
            continue

        # Bilinmeyen faz: bekle
        logger.warning("Bilinmeyen TAP fazı '%s', bekleniyor...", phase)
        await asyncio.sleep(POLL_INTERVAL_SECONDS)

    raise TapBusy(
        f"TAP job did not complete within {MAX_POLL_SECONDS}s: {job_url}"
    )


async def _fetch_result(
    client: httpx.AsyncClient,
    job_url: str,
) -> bytes:
    """
    Tamamlanan TAP işinin VOTable sonucunu indirir.

    HTTP 502/503 → TapBusy; diğer hatalar → TapError.
    """
    result_url = f"{job_url}/results/result"
    logger.info("TAP sonucu indiriliyor: %s", result_url)
    try:
        resp = await client.get(result_url, follow_redirects=True)
    except httpx.TimeoutException as exc:
        raise TapBusy(f"Result download timeout: {exc}") from exc
    except httpx.RequestError as exc:
        raise TapError(f"Result download request error: {exc}") from exc

    if resp.status_code in (502, 503):
        raise TapBusy(f"Result download HTTP {resp.status_code}: server busy")
    if resp.status_code != 200:
        raise TapError(
            f"Result download failed with HTTP {resp.status_code}: {resp.text[:200]}"
        )

    logger.info(
        "TAP sonucu indirildi: %d bayt", len(resp.content)
    )
    return resp.content


# ---------------------------------------------------------------------------
# Ana girdi noktası
# ---------------------------------------------------------------------------

async def query_frames(
    ra: float,
    dec: float,
    target_id: str,
    collection: str = "dr1",
    *,
    client: Optional[httpx.AsyncClient] = None,
) -> list[TapFrame]:
    """
    Verilen koordinatta kare listesini async TAP ile sorgular.

    Parametreler
    ------------
    ra : float
        Sağ açıklık (derece, ICRS).
    dec : float
        Sapma (derece, ICRS).
    target_id : str
        İzleme amaçlı hedef tanımlayıcısı (loglarda görünür).
    collection : str
        SPHEREx koleksiyonu (varsayılan: 'dr1').
    client : httpx.AsyncClient, isteğe bağlı
        Dışarıdan sağlanan HTTP istemcisi. Belirtilmezse kısa ömürlü
        bir istemci oluşturulur.

    Dönüş
    ------
    list[TapFrame]
        Koordinatta örtüşen kareler. Boş liste döndürmek geçerlidir.

    İstisnalar
    ----------
    TapBusy
        Servis meşgul veya 15 dk içinde yanıt gelmedi.
        Çağrıcı L0 önbellekten dönmelidir.
    TapError
        Kurtarılamaz hata (BAD_REQUEST, parse hatası vb.).
    """
    adql = _build_adql(ra, dec, collection)
    logger.info(
        "[%s] TAP sorgusu başlatılıyor: ra=%.4f dec=%.4f col=%s",
        target_id, ra, dec, collection,
    )
    logger.debug("[%s] ADQL: %s", target_id, adql)

    _owns_client = client is None
    if _owns_client:
        client = httpx.AsyncClient(timeout=60.0)

    try:
        for attempt, backoff in enumerate((*BACKOFF_SECONDS, None), start=1):
            try:
                job_url = await _submit_job(client, adql)
                await _poll_job(client, job_url)
                xml_bytes = await _fetch_result(client, job_url)
                frames = _parse_votable(xml_bytes)
                logger.info(
                    "[%s] TAP sorgusu tamamlandı: %d kare (deneme %d)",
                    target_id, len(frames), attempt,
                )
                return frames

            except TapBusy as exc:
                if backoff is None:
                    logger.error(
                        "[%s] TAP başarısız, yeniden deneme hakkı kalmadı: %s",
                        target_id, exc,
                    )
                    raise
                logger.warning(
                    "[%s] TapBusy (deneme %d/%d), %ds beklenecek: %s",
                    target_id, attempt, len(BACKOFF_SECONDS) + 1, backoff, exc,
                )
                await asyncio.sleep(backoff)

            except TapError:
                # Kurtarılamaz hata; yeniden deneme yok
                logger.exception("[%s] TapError — yeniden denenmiyor", target_id)
                raise

    finally:
        if _owns_client:
            await client.aclose()

    # Buraya normalde gelinmez; tip denetleyicisi için
    raise TapBusy("TAP query exhausted all retries")
