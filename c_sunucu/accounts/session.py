"""
session.py — Oturum yönetimi.

HTTP-only secure çerez ile oturum tokeni.
Tokenler bellekte tutulur (demo: kalıcılık yok, restart'ta silinir).
"""
from __future__ import annotations

import logging
import secrets
import time
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)

SESSION_MAX_AGE = 86400  # 24 saat (saniye)


@dataclass(frozen=True)
class Session:
    """Bellekte tutulan oturum nesnesi.

    Attributes:
        token:      URL-güvenli rastgele token dizesi.
        user_id:    Kullanıcının UUID4 kimliği.
        username:   Kullanıcı adı.
        created_at: Unix zaman damgası (float); oturumun oluşturulma anı.
    """

    token: str
    user_id: str
    username: str
    created_at: float

    def is_expired(self) -> bool:
        """Oturumun süresinin dolup dolmadığını döner.

        Returns:
            Oluşturulma anından bu yana SESSION_MAX_AGE saniye geçtiyse True.
        """
        return time.time() - self.created_at > SESSION_MAX_AGE


class SessionStore:
    """Bellek içi oturum deposu.

    Thread-safe değildir; demo/tek-işlemci kullanımı için yeterlidir.
    Üretim ortamında Redis veya benzeri kalıcı depo ile değiştirin.
    """

    def __init__(self) -> None:
        """Boş oturum sözlüğünü başlatır."""
        self._store: dict[str, Session] = {}

    def create(self, user_id: str, username: str) -> Session:
        """Yeni 32-byte güvenli token ile oturum oluşturur ve depoya kaydeder.

        Args:
            user_id:  Kullanıcının UUID4 kimliği.
            username: Kullanıcı adı.

        Returns:
            Oluşturulan Session nesnesi.
        """
        token = secrets.token_urlsafe(32)
        session = Session(
            token=token,
            user_id=user_id,
            username=username,
            created_at=time.time(),
        )
        self._store[token] = session
        logger.info(
            "Oturum oluşturuldu — kullanıcı: %s, token öneki: %s…",
            username,
            token[:8],
        )
        return session

    def get(self, token: str) -> Optional[Session]:
        """Token geçerli ve süresi dolmamışsa Session nesnesini döner.

        Süresi dolmuş bir token bulunursa otomatik olarak silinir.

        Args:
            token: Çerezden okunan oturum tokeni.

        Returns:
            Geçerli Session; token bilinmiyorsa veya süresi dolduysa None.
        """
        session = self._store.get(token)
        if session is None:
            return None
        if session.is_expired():
            del self._store[token]
            logger.info("Süresi dolmuş oturum silindi — token öneki: %s…", token[:8])
            return None
        return session

    def delete(self, token: str) -> None:
        """Belirtilen tokena ait oturumu siler.

        Token mevcut değilse sessizce devam eder.

        Args:
            token: Silinecek oturum tokeni.
        """
        if token in self._store:
            username = self._store[token].username
            del self._store[token]
            logger.info("Oturum silindi — kullanıcı: %s", username)

    def cleanup_expired(self) -> int:
        """Süresi dolmuş tüm oturumları siler.

        Returns:
            Silinen oturum sayısı.
        """
        expired_tokens = [
            token for token, session in self._store.items() if session.is_expired()
        ]
        for token in expired_tokens:
            del self._store[token]
        if expired_tokens:
            logger.info("Temizleme: %d süresi dolmuş oturum silindi.", len(expired_tokens))
        return len(expired_tokens)


# Singleton — tüm modüllerde bu örnek kullanılır
session_store = SessionStore()
