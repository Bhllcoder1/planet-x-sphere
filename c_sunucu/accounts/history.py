"""
history.py — Arama/görüntüleme geçmişi.

Her görüntüleme olayı: target_id, frame_id, x0, y0, zaman damgası, URL.
Kullanıcı başına en fazla 100 giriş (eski girişler çıkarılır, FIFO).
Depolama: L2_CACHE_DIR/history/{user_id}_{tarih}.json
"""
from __future__ import annotations

import json
import logging
import pathlib
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Optional

import aiofiles

logger = logging.getLogger(__name__)

# Kullanıcı başına maksimum giriş sayısı
_MAX_ENTRIES: int = 100


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

    Her kullanıcı için günlük bir JSON dosyası tutulur.
    Dosya yolu: cache_dir/history/{user_id}_{YYYY-MM-DD}.json
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
        """
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
        """
        entries = await self._read_all(user_id)
        return entries[-limit:] if limit > 0 else list(entries)

    async def clear(self, user_id: str) -> int:
        """Kullanıcının tüm geçmişini temizler.

        Bugünün geçmiş dosyasına boş liste yazar; silinen giriş sayısını döner.

        Args:
            user_id: Geçmişi temizlenecek kullanıcının kimliği.

        Returns:
            Silinen giriş sayısı (temizlemeden önceki boyut).
        """
        entries = await self._read_all(user_id)
        count = len(entries)
        await self._write(user_id, [])
        logger.info("Geçmiş temizlendi: user=%r silinen=%d", user_id, count)
        return count

    # ------------------------------------------------------------------
    # Yardımcı — dosya yolu
    # ------------------------------------------------------------------

    def _user_file(self, user_id: str, date: Optional[str] = None) -> pathlib.Path:
        """Kullanıcı geçmiş dosyasının tam yolunu döndürür.

        Args:
            user_id: Kullanıcının kimliği.
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
        """Kullanıcının tüm geçmiş dosyalarından girişleri okur.

        Birden fazla tarihli dosya varsa hepsini okur, zaman damgasına göre
        artan sırayla birleştirir.

        Returns:
            Zaman damgasına göre sıralı HistoryEntry listesi.
        """
        history_dir = self._cache_dir / "history"
        if not history_dir.is_dir():
            return []

        all_entries: list[HistoryEntry] = []
        pattern = f"{user_id}_*.json"
        for path in sorted(history_dir.glob(pattern)):
            try:
                async with aiofiles.open(path, "r", encoding="utf-8") as f:
                    raw = await f.read()
                data = json.loads(raw)
                if isinstance(data, list):
                    for item in data:
                        all_entries.append(HistoryEntry(**item))
            except (json.JSONDecodeError, KeyError, TypeError, OSError) as exc:
                logger.warning("Geçmiş dosyası okunamadı (%s): %s", path, exc)
                continue

        all_entries.sort(key=lambda e: e.timestamp)
        return all_entries

    async def _write(self, user_id: str, entries: list[HistoryEntry]) -> None:
        """Girişleri bugünün dosyasına atomik olarak yazar.

        Önce geçici bir dosyaya yazar, ardından os.replace() ile yerleştirir.

        Args:
            user_id:  Kullanıcının kimliği.
            entries:  Yazılacak HistoryEntry listesi.
        """
        path = self._user_file(user_id)
        path.parent.mkdir(parents=True, exist_ok=True)

        payload = json.dumps(
            [asdict(e) for e in entries],
            ensure_ascii=False,
            indent=2,
        )
        tmp_path = path.with_suffix(".tmp")
        try:
            async with aiofiles.open(tmp_path, "w", encoding="utf-8") as f:
                await f.write(payload)
            tmp_path.replace(path)
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

    Args:
        target_id: SPHEREx hedef tanımlayıcısı.
        frame_id:  SPHEREx kare tanımlayıcısı.
        x0:        Pencerenin sol sütunu (0 tabanlı piksel).
        y0:        Pencerenin üst satırı (0 tabanlı piksel).
        width:     Pencere genişliği (piksel).
        height:    Pencere yüksekliği (piksel).

    Returns:
        ``?target=...&frame=...&x=...&y=...&w=...&h=...`` biçiminde URL sorgu dizesi.
    """
    return (
        f"?target={target_id}"
        f"&frame={frame_id}"
        f"&x={x0}"
        f"&y={y0}"
        f"&w={width}"
        f"&h={height}"
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
