"""
user_repo.py — Kullanıcı deposu.

10 sabit hesap; seed JSON dosyasından yüklenir.
Kayıt yok; şifreler bcrypt ile hash'lenir (12 round).
UUID4 ile kullanıcı ID'leri.
"""
from __future__ import annotations

import json
import logging
import os
import pathlib
import uuid
from dataclasses import dataclass, field
from typing import Optional

try:
    import bcrypt
except ImportError as exc:
    raise ImportError(
        "bcrypt paketi bulunamadı. 'pip install bcrypt' komutu ile kurun."
    ) from exc

logger = logging.getLogger(__name__)


class PasslibError(Exception):
    """Şifre hash/doğrulama işlemlerinde oluşan hataları sarar."""


@dataclass(frozen=True)
class User:
    """Kullanıcı modeli; değiştirilemez (frozen=True).

    Attributes:
        id: UUID4 formatında kullanıcı kimliği.
        username: Oturum açmak için kullanılan benzersiz kullanıcı adı.
        display_name: Arayüzde gösterilen isim.
        role: Kullanıcı rolü — "jury" | "team" | "admin".
        _password_hash: bcrypt ile üretilmiş şifre özeti; JSON yanıtına dahil edilmez.
    """

    id: str
    username: str
    display_name: str
    role: str
    _password_hash: str = field(repr=False, compare=False)


class UserRepository:
    """Kullanıcı deposu; başlatmada seed dosyasından yüklenir.

    Yeni kayıt desteği yoktur. Tüm hesaplar seed JSON dosyasında
    önceden tanımlanmıştır.
    """

    _ALLOWED_ROLES = frozenset({"jury", "team", "admin"})

    def __init__(self, seed_file: pathlib.Path) -> None:
        """Depoyu seed dosyasından başlatır.

        Args:
            seed_file: Kullanıcı verilerini içeren JSON dosyasının yolu.

        Raises:
            FileNotFoundError: Seed dosyası bulunamazsa.
            ValueError: JSON yapısı geçersizse veya alan eksikse.
        """
        self._users: dict[str, User] = {}
        self._load(seed_file)

    # ------------------------------------------------------------------
    # Yükleme
    # ------------------------------------------------------------------

    def _load(self, seed_file: pathlib.Path) -> None:
        """Seed dosyasını okur ve kullanıcıları belleğe yükler."""
        if not seed_file.exists():
            raise FileNotFoundError(
                f"Seed dosyası bulunamadı: {seed_file}. "
                "users_seed.json.example dosyasını kopyalayıp doldurun."
            )

        raw = seed_file.read_text(encoding="utf-8")
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Seed dosyası geçerli JSON değil: {exc}") from exc

        users_list = data.get("users")
        if not isinstance(users_list, list):
            raise ValueError("Seed dosyasında 'users' dizisi bulunamadı.")

        for entry in users_list:
            user = self._parse_entry(entry)
            if user.username in self._users:
                raise ValueError(
                    f"Seed dosyasında tekrar eden kullanıcı adı: '{user.username}'"
                )
            self._users[user.username] = user

        logger.info("Kullanıcı deposu yüklendi — %d hesap.", len(self._users))

    @staticmethod
    def _parse_entry(entry: dict) -> User:
        """Tek bir seed girişini doğrular ve User nesnesine dönüştürür."""
        required = ("id", "username", "display_name", "role", "password_hash")
        missing = [k for k in required if not entry.get(k)]
        if missing:
            raise ValueError(
                f"Seed girişinde eksik veya boş alan(lar): {missing}. "
                f"Giriş: {entry.get('username', '<bilinmiyor>')}"
            )

        role = entry["role"]
        if role not in UserRepository._ALLOWED_ROLES:
            raise ValueError(
                f"Geçersiz rol '{role}' — izin verilenler: {UserRepository._ALLOWED_ROLES}"
            )

        # UUID formatını doğrula
        try:
            uuid.UUID(entry["id"], version=4)
        except ValueError as exc:
            raise ValueError(
                f"Geçersiz UUID4 formatı: '{entry['id']}'"
            ) from exc

        return User(
            id=entry["id"],
            username=entry["username"],
            display_name=entry["display_name"],
            role=role,
            _password_hash=entry["password_hash"],
        )

    # ------------------------------------------------------------------
    # Sorgu
    # ------------------------------------------------------------------

    def find_by_username(self, username: str) -> Optional[User]:
        """Kullanıcı adına göre kullanıcı arar.

        Args:
            username: Aranacak kullanıcı adı.

        Returns:
            Bulunan User nesnesi; kullanıcı yoksa None.
        """
        user = self._users.get(username)
        if user is None:
            logger.warning("Kullanıcı bulunamadı.")
        return user

    def verify_password(self, user: User, plain_password: str) -> bool:
        """bcrypt ile şifre doğrular.

        Args:
            user: Şifresi doğrulanacak kullanıcı.
            plain_password: Düz metin şifre.

        Returns:
            Şifre doğruysa True, yanlışsa False.

        Raises:
            PasslibError: bcrypt işlemi beklenmeyen bir hata üretirse.
        """
        try:
            match = bcrypt.checkpw(
                plain_password.encode("utf-8"),
                user._password_hash.encode("utf-8"),
            )
        except Exception as exc:
            raise PasslibError(
                f"Şifre doğrulama sırasında beklenmeyen hata: {exc}"
            ) from exc

        if not match:
            logger.warning("Şifre doğrulama başarısız.")

        return match

    def list_users(self) -> list[User]:
        """Şifre hash'leri hariç kullanıcı listesini döner.

        Returns:
            Tüm User nesnelerinin listesi (sıralı, kullanıcı adına göre).
        """
        return sorted(self._users.values(), key=lambda u: u.username)


# ------------------------------------------------------------------
# Yardımcı
# ------------------------------------------------------------------

def hash_password(plain: str) -> str:
    """12-round bcrypt hash üretir.

    Args:
        plain: Hash'lenecek düz metin şifre.

    Returns:
        bcrypt hash dizesi.

    Raises:
        PasslibError: bcrypt işlemi başarısız olursa.
    """
    try:
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(plain.encode("utf-8"), salt).decode("utf-8")
    except Exception as exc:
        raise PasslibError(f"Şifre hash'leme başarısız: {exc}") from exc


def _build_repo_from_env() -> UserRepository:
    """Ortam değişkeninden seed dosyası yolunu okuyarak depo oluşturur.

    Ortam değişkeni: USERS_SEED_FILE
    Varsayılan: c_sunucu/accounts/users_seed.json

    Returns:
        UserRepository nesnesi.
    """
    seed_path = pathlib.Path(
        os.environ.get("USERS_SEED_FILE", "c_sunucu/accounts/users_seed.json")
    )
    return UserRepository(seed_path)
