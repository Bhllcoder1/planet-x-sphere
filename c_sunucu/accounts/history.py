"""
history.py — Arama/görüntüleme geçmişi.

Her görüntüleme olayı: target_id, frame_id, x0, y0, zaman damgası, URL.
Kullanıcı başına en fazla 100 giriş (eski girişler çıkarılır, FIFO).
Depolama: L2_CACHE_DIR/history/{user_id}_{tarih}.json (tek dosya, günlük)
"""
from __future__ import annotations

import asyncio
import json
import logging
import pathlib
import re
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from urllib.parse import urlencode

import aiofiles

logger = logging.getLogger(__name__)

# Kullanıcı başına maksimum giriş sayısı
_MAX_ENTRIES: int = 100

# user_id doğrulama deseni: yalnızca alfanümerik, tire ve alt çizgi
_SAFE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{1,128}$")


def _sanitize_user_id(user_id: str) -> str:
    """user_id'nin güvenli olduğunu doğrular; geçersizse ValueError yükseltir.

    Path traversal saldırılarını önlemek için kullanıcı kimliği yalnızca
    ``[A-Za-z0-9_-]`` karakterlerinden oluşabilir, en fazla 128 karakter.

    Args:
        user_id: Doğrulanacak kullanıcı kimliği dizesi.

    Returns:
        Orijinal user_id (geçerliyse).

    Raises:
        ValueError: user_id geçersiz karakterler veya boyut içeriyorsa.
    """
    if not _SAFE_ID_RE.match(user_id):
        raise ValueError(
            f"Geçersiz user_id: '{user_id}'. "
            "Yalnızca harf, rakam, '-' ve '_' kabul edilir; en fazla 128 karakter."
        )
    return user_id


@dataclass(frozen=True)
class HistoryEntry:
    """Tek bir görüntüleme olayının değiştirilemez (frozen) kaydı.

    Attributes:
        id:        UUID4 formatında benzersiz giriş kimliği.
        user_id:   Girişi oluşturan kullanıcının kimliği.
        target_id: SPHEREx hedef tanımlayıcısı.
        frame_id:  SPHEREx kare tanımlayıcısı.
        x0:        Pencerenin sol sütunu (0 tabanlı piksel).
        y0:        Pencerenin üst satırı (0 tabanlı piksel).
        width:     Pencere genişliği (piksel).
        height:    Pencere yüksekliği (piksel).
        timestamp: ISO 8601 UTC zaman damgası.
        share_url: Paylaşım için sorgu dizesi.
    """

    id: str
    user_id: str
    target_id: str
    frame_id: str
    x0: int
    y0: int
    width: int
    height: int
    timestamp: str
    share_url: str


class HistoryRepository:
    """Kullanıcı başına geçmiş deposu (JSON dosyaları).

    Her kullanıcı için günlük tek bir JSON dosyası tutulur.
    Dosya yolu: cache_dir/history/{user_id}_{YYYY-MM-DD}.json

    Tasarım kararı (sadelik): _read_all yalnızca bugünün dosyasını okur.
    Önceki günlere ait girişler demo kapsamı dışında tutulur.
    """

    def __init__(self, cache_dir: pathlib.Path) -> None:
        """Depoyu başlatır.

        Args:
            cache_dir: L2 önbellek kök dizini (L2_CACHE_DIR).
        """
        self._cache_dir = cache_dir

    # ------------------------------------------------------------------
    # Genel API
    # ------------------------------------------------------------------

    async def add(self, user_id: str, entry: HistoryEntry) -> None:
        """Girdiyi kullanıcının geçmişine ekler.

        Mevcut girdi sayısı _MAX_ENTRIES sınırına ulaşırsa en eski girdiler
        (FIFO) çıkarılarak liste 100 girişe indirilir.

        Args:
            user_id: Girişin sahibi kullanıcının kimliği.
            entry:   Eklenecek HistoryEntry nesnesi.

        Raises:
            ValueError: user_id geçersiz karakterler içeriyorsa.
        """
        _sanitize_user_id(user_id)
        entries = await self._read_all(user_id)
        entries.append(entry)
        if len(entries) > _MAX_ENTRIES:
            entries = entries[-_MAX_ENTRIES:]
        await self._write(user_id, entries)
        logger.debug(
            "Geçmiş eklendi: user=%r entry_id=%r toplam=%d",
            user_id,
            entry.id,
            len(entries),
        )

    async def get_all(self, user_id: str, limit: int = 50) -> list[HistoryEntry]:
        """Kullanıcının son N geçmiş girişini döndürür.

        Args:
            user_id: Sorgulanacak kullanıcının kimliği.
            limit:   Döndürülecek maksimum giriş sayısı (varsayılan: 50).

        Returns:
            En yeni ``limit`` girişin listesi (zaman damgasına göre artan sıra).

        Raises:
            ValueError: user_id geçersiz karakterler içeriyorsa.
        """
        _sanitize_user_id(user_id)
        entries = await self._read_all(user_id)
        return entries[-limit:] if limit > 0 else list(entries)

    async def clear(self, user_id: str) -> int:
        """Kullanıcının tüm geçmişini temizler.

        Bugünün geçmiş dosyasına boş liste yazar; silinen giriş sayısını döner.

        Args:
            user_id: Geçmişi temizlenecek kullanıcının kimliği.

        Returns:
            Silinen giriş sayısı (temizlemeden önceki boyut).

        Raises:
            ValueError: user_id geçersiz karakterler içeriyorsa.
        """
        _sanitize_user_id(user_id)
        entries = await self._read_all(user_id)
        count = len(entries)
        await self._write(user_id, [])
        logger.info("Geçmiş temizlendi: user=%r silinen=%d", user_id, count)
        return count

    # ------------------------------------------------------------------
    # Yardımcı — dosya yolu
    # ------------------------------------------------------------------

    def _user_file(self, user_id: str, date: str | None = None) -> pathlib.Path:
        """Kullanıcı geçmiş dosyasının tam yolunu döndürür.

        user_id daha önce ``_sanitize_user_id`` ile doğrulanmış olmalıdır.

        Args:
            user_id: Doğrulanmış kullanıcı kimliği.
            date:    ``YYYY-MM-DD`` formatında tarih; None ise bugün kullanılır.

        Returns:
            ``cache_dir/history/{user_id}_{tarih}.json`` yolu.
        """
        if date is None:
            date = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
        return self._cache_dir / "history" / f"{user_id}_{date}.json"

    # ------------------------------------------------------------------
    # Dahili — async okuma/yazma
    # ------------------------------------------------------------------

    async def _read_all(self, user_id: str) -> list[HistoryEntry]:
        """Bugünün geçmiş dosyasından girişleri okur.

        Dosya yoksa boş liste döner. Bozuk JSON sessizce atlanır.

        Returns:
            Zaman damgasına göre artan sırada HistoryEntry listesi.
        """
        loop = asyncio.get_running_loop()
        path = self._user_file(user_id)

        exists = await loop.run_in_executor(None, path.exists)
        if not exists:
            return []

        try:
            async with aiofiles.open(path, "r", encoding="utf-8") as f:
                raw = await f.read()
            data = json.loads(raw)
            if not isinstance(data, list):
                return []
            entries = [HistoryEntry(**item) for item in data]
        except (json.JSONDecodeError, KeyError, TypeError, OSError) as exc:
            logger.warning("Geçmiş dosyası okunamadı (%s): %s", path, exc)
            return []

        entries.sort(key=lambda e: e.timestamp)
        return entries

    async def _write(self, user_id: str, entries: list[HistoryEntry]) -> None:
        """Girişleri bugünün dosyasına atomik olarak yazar.

        Önce geçici bir ``.tmp`` dosyasına yazar, ardından ``os.replace()``
        ile hedef konuma taşır. Dizin yoksa oluşturulur.

        Args:
            user_id:  Kullanıcının kimliği.
            entries:  Yazılacak HistoryEntry listesi.

        Raises:
            OSError: Dosya yazma veya taşıma işlemi başarısız olursa.
        """
        loop = asyncio.get_running_loop()
        path = self._user_file(user_id)

        # Dizin oluşturma — bloke edici çağrı executor'a taşınır
        await loop.run_in_executor(
            None, lambda: path.parent.mkdir(parents=True, exist_ok=True)
        )

        payload = json.dumps(
            [asdict(e) for e in entries],
            ensure_ascii=False,
            indent=2,
        )
        tmp_path = path.with_suffix(".tmp")
        try:
            async with aiofiles.open(tmp_path, "w", encoding="utf-8") as f:
                await f.write(payload)
            # Atomik yeniden adlandırma — bloke edici çağrı executor'a taşınır
            await loop.run_in_executor(None, tmp_path.replace, path)
        except OSError as exc:
            logger.error("Geçmiş dosyası yazılamadı (%s): %s", path, exc)
            raise


# ------------------------------------------------------------------
# URL yardımcısı
# ------------------------------------------------------------------


def build_share_url(
    target_id: str,
    frame_id: str,
    x0: int,
    y0: int,
    width: int = 100,
    height: int = 100,
) -> str:
    """Görüntüleme penceresini paylaşmak için sorgu dizesi oluşturur.

    Parametre değerleri ``urllib.parse.urlencode`` ile güvenli biçimde
    yüzde-kodlanır; bu sayede özel karakterler ve enjeksiyon girişimleri
    engellenir.

    Args:
        target_id: SPHEREx hedef tanımlayıcısı.
        frame_id:  SPHEREx kare tanımlayıcısı.
        x0:        Pencerenin sol sütunu (0 tabanlı piksel).
        y0:        Pencerenin üst satırı (0 tabanlı piksel).
        width:     Pencere genişliği (piksel).
        height:    Pencere yüksekliği (piksel).

    Returns:
        ``?target=...&frame=...&x=...&y=...&w=...&h=...`` biçiminde
        yüzde-kodlanmış URL sorgu dizesi.
    """
    return "?" + urlencode(
        {
            "target": target_id,
            "frame": frame_id,
            "x": x0,
            "y": y0,
            "w": width,
            "h": height,
        }
    )


def new_entry(
    user_id: str,
    target_id: str,
    frame_id: str,
    x0: int,
    y0: int,
    width: int = 100,
    height: int = 100,
) -> HistoryEntry:
    """Yeni bir HistoryEntry nesnesi oluşturur (UUID4 ve UTC zaman damgası ile).

    Args:
        user_id:   Girişin sahibi kullanıcının kimliği.
        target_id: SPHEREx hedef tanımlayıcısı.
        frame_id:  SPHEREx kare tanımlayıcısı.
        x0:        Pencerenin sol sütunu.
        y0:        Pencerenin üst satırı.
        width:     Pencere genişliği.
        height:    Pencere yüksekliği.

    Returns:
        Doldurulmuş HistoryEntry nesnesi.
    """
    return HistoryEntry(
        id=str(uuid.uuid4()),
        user_id=user_id,
        target_id=target_id,
        frame_id=frame_id,
        x0=x0,
        y0=y0,
        width=width,
        height=height,
        timestamp=datetime.now(tz=timezone.utc).isoformat(),
        share_url=build_share_url(target_id, frame_id, x0, y0, width, height),
    )
