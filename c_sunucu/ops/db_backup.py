"""
db_backup.py — Geçmiş ve kullanıcı verisi yedekleme/geri yükleme.

"Veritabanı" iki kaynaktan oluşur:
  1. Geçmiş JSON dizini: {L2_CACHE_DIR}/history/
  2. Kullanıcı seed dosyası: {USERS_SEED_FILE}

Yedek biçimi .tar.gz arşividir; arşiv içindeki kök isimler sabittir:
  history/        — geçmiş JSON dosyaları
  users_seed.json — kullanıcı seed dosyası

Kullanım:
    python -m c_sunucu.ops.db_backup backup --out /tmp/spherex_backup.tar.gz
    python -m c_sunucu.ops.db_backup restore --from /tmp/spherex_backup.tar.gz
"""
from __future__ import annotations

import argparse
import logging
import os
import pathlib
import tarfile
import time
from typing import Optional

logger = logging.getLogger(__name__)

# Arşiv içindeki sabit kök isimler
_HISTORY_ARC_NAME = "history"
_SEED_ARC_NAME = "users_seed.json"


# ---------------------------------------------------------------------------
# Ortam yardımcıları
# ---------------------------------------------------------------------------


def _default_cache_dir() -> pathlib.Path:
    """
    L2_CACHE_DIR ortam değişkeninden önbellek kök dizinini döndürür.

    Returns:
        Ortam değişkeni yoksa ``cache/l2`` döner.
    """
    return pathlib.Path(os.environ.get("L2_CACHE_DIR", "cache/l2"))


def _default_seed_file() -> pathlib.Path:
    """
    USERS_SEED_FILE ortam değişkeninden kullanıcı seed dosyasının yolunu döndürür.

    Returns:
        Ortam değişkeni yoksa ``c_sunucu/accounts/users_seed.json`` döner.
    """
    return pathlib.Path(
        os.environ.get("USERS_SEED_FILE", "c_sunucu/accounts/users_seed.json")
    )


# ---------------------------------------------------------------------------
# backup
# ---------------------------------------------------------------------------


def backup(
    out_path: pathlib.Path,
    cache_dir: Optional[pathlib.Path] = None,
    seed_file: Optional[pathlib.Path] = None,
) -> pathlib.Path:
    """
    Geçmiş dizinini ve kullanıcı seed dosyasını .tar.gz arşivi olarak dışa aktarır.

    Arşive eklenen öğeler:
      - ``{cache_dir}/history/``    → arşivde ``history/`` olarak
      - ``{seed_file}``             → arşivde ``users_seed.json`` olarak

    Her iki kaynak da yoksa ``FileNotFoundError`` yükseltilir ve yarım kalan
    arşiv silini.

    Args:
        out_path:  Oluşturulacak .tar.gz dosyasının tam yolu.
        cache_dir: L2 önbellek kök dizini; ``None`` ise ortam değişkeninden alınır.
        seed_file: Kullanıcı seed JSON dosyası; ``None`` ise ortam değişkeninden alınır.

    Returns:
        Oluşturulan arşiv dosyasının yolu.

    Raises:
        FileNotFoundError: Yedeklenecek hiçbir kaynak bulunamazsa.
        tarfile.TarError:  Arşiv oluşturma sırasında beklenmedik hata oluşursa.
    """
    if cache_dir is None:
        cache_dir = _default_cache_dir()
    if seed_file is None:
        seed_file = _default_seed_file()

    out_path = pathlib.Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    history_dir = cache_dir / "history"
    added = 0

    try:
        with tarfile.open(out_path, "w:gz") as tar:
            # --- Geçmiş dizini ---
            if history_dir.is_dir():
                tar.add(history_dir, arcname=_HISTORY_ARC_NAME)
                file_count = sum(1 for p in history_dir.rglob("*") if p.is_file())
                added += file_count
                logger.info(
                    "Yedeklendi: geçmiş dizini → arşiv:%s (%d dosya)",
                    _HISTORY_ARC_NAME,
                    file_count,
                )
            else:
                logger.warning(
                    "Geçmiş dizini bulunamadı: %s — atlandı", history_dir
                )

            # --- Seed dosyası ---
            if seed_file.is_file():
                tar.add(seed_file, arcname=_SEED_ARC_NAME)
                added += 1
                logger.info(
                    "Yedeklendi: seed dosyası → arşiv:%s", _SEED_ARC_NAME
                )
            else:
                logger.warning(
                    "Seed dosyası bulunamadı: %s — atlandı", seed_file
                )
    except Exception:
        # Arşiv oluşturma başarısız olursa yarım kalan dosyayı temizle
        out_path.unlink(missing_ok=True)
        raise

    if added == 0:
        out_path.unlink(missing_ok=True)
        raise FileNotFoundError(
            f"Yedeklenecek hiçbir kaynak bulunamadı. "
            f"history_dir={history_dir!r}, seed_file={seed_file!r}"
        )

    size_kb = out_path.stat().st_size // 1024
    logger.info(
        "Yedekleme tamamlandı: %s — %d öğe, %d KB",
        out_path,
        added,
        size_kb,
    )
    return out_path


# ---------------------------------------------------------------------------
# restore
# ---------------------------------------------------------------------------


def restore(
    src_path: pathlib.Path,
    cache_dir: Optional[pathlib.Path] = None,
    seed_file: Optional[pathlib.Path] = None,
) -> int:
    """
    .tar.gz arşivinden geçmiş ve seed verilerini geri yükler.

    Mevcut dosyaların üzerine yazar.  Arşiv içindeki mutlak yollar ve
    ``..`` bileşenleri güvenlik gerekçesiyle atlanır.

    Args:
        src_path:  Geri yüklenecek .tar.gz arşivinin tam yolu.
        cache_dir: L2 önbellek kök dizini; ``None`` ise ortam değişkeninden alınır.
        seed_file: Seed dosyasının hedef yolu; ``None`` ise ortam değişkeninden alınır.

    Returns:
        Geri yüklenen dosya sayısı.

    Raises:
        FileNotFoundError: Arşiv dosyası bulunamazsa.
        tarfile.TarError:  Arşiv açılamazsa veya bozuk ise.
    """
    src_path = pathlib.Path(src_path)
    if not src_path.is_file():
        raise FileNotFoundError(f"Arşiv dosyası bulunamadı: {src_path}")

    if cache_dir is None:
        cache_dir = _default_cache_dir()
    if seed_file is None:
        seed_file = _default_seed_file()

    # Hedef dizinleri hazırla
    (cache_dir / "history").mkdir(parents=True, exist_ok=True)
    seed_file.parent.mkdir(parents=True, exist_ok=True)

    restored = 0

    with tarfile.open(src_path, "r:gz") as tar:
        for member in tar.getmembers():
            # Güvenlik: mutlak yolları ve '..' bileşenlerini reddet
            parts = pathlib.PurePosixPath(member.name).parts
            if member.name.startswith("/") or ".." in parts:
                logger.warning(
                    "Güvenli olmayan arşiv üyesi atlandı: %r", member.name
                )
                continue

            if member.name == _SEED_ARC_NAME:
                # Seed dosyasını hedef konumuna yaz
                f = tar.extractfile(member)
                if f is not None:
                    seed_file.write_bytes(f.read())
                    restored += 1
                    logger.info("Geri yüklendi: seed → %s", seed_file)

            elif member.name == _HISTORY_ARC_NAME or member.name.startswith(
                _HISTORY_ARC_NAME + "/"
            ):
                # Geçmiş dosyasını cache_dir altına yaz
                relative = pathlib.Path(*pathlib.PurePosixPath(member.name).parts)
                target = cache_dir / relative

                if member.isdir():
                    target.mkdir(parents=True, exist_ok=True)
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    f = tar.extractfile(member)
                    if f is not None:
                        target.write_bytes(f.read())
                        restored += 1
                        logger.debug(
                            "Geri yüklendi: %s → %s", member.name, target
                        )

    logger.info(
        "Geri yükleme tamamlandı: %s — %d dosya işlendi", src_path, restored
    )
    return restored


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    """
    Argparse CLI ayrıştırıcısını oluşturur.

    Alt komutlar:
      backup   — Verileri .tar.gz olarak yedekle
      restore  — Yedekten verileri geri yükle

    Returns:
        Yapılandırılmış ArgumentParser nesnesi.
    """
    parser = argparse.ArgumentParser(
        prog="db_backup",
        description=(
            "SPHEREx geçmiş ve kullanıcı verisi yedekleme/geri yükleme aracı.\n\n"
            "Yedeklenen kaynaklar:\n"
            "  - L2_CACHE_DIR/history/   (geçmiş JSON dosyaları)\n"
            "  - USERS_SEED_FILE         (kullanıcı seed JSON dosyası)"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # --- backup ---
    bp = sub.add_parser(
        "backup",
        help="Geçmiş ve seed verilerini .tar.gz olarak yedekle",
    )
    bp.add_argument(
        "--out",
        default=None,
        metavar="YOL",
        help=(
            "Çıktı .tar.gz dosya yolu. "
            "Belirtilmezse geçerli dizinde spherex_backup_<YYYYMMDD_HHMMSS>.tar.gz oluşturulur."
        ),
    )
    bp.add_argument(
        "--cache-dir",
        default=None,
        metavar="DİZİN",
        help="L2 önbellek kök dizini (varsayılan: L2_CACHE_DIR ortam değişkeni).",
    )
    bp.add_argument(
        "--seed-file",
        default=None,
        metavar="YOL",
        help="Kullanıcı seed dosyası (varsayılan: USERS_SEED_FILE ortam değişkeni).",
    )

    # --- restore ---
    rp = sub.add_parser(
        "restore",
        help="Yedekten verileri geri yükle",
    )
    rp.add_argument(
        "--from",
        dest="src",
        required=True,
        metavar="YOL",
        help="Geri yüklenecek .tar.gz arşiv dosyasının yolu.",
    )
    rp.add_argument(
        "--cache-dir",
        default=None,
        metavar="DİZİN",
        help="L2 önbellek kök dizini (varsayılan: L2_CACHE_DIR ortam değişkeni).",
    )
    rp.add_argument(
        "--seed-file",
        default=None,
        metavar="YOL",
        help="Seed dosyasının hedef yolu (varsayılan: USERS_SEED_FILE ortam değişkeni).",
    )

    return parser


def main() -> None:
    """
    CLI giriş noktası.

    Komut satırı argümanlarını ayrıştırır ve uygun işlemi (backup/restore) çalıştırır.
    Loglama seviyesi INFO olarak yapılandırılır.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    parser = _build_parser()
    args = parser.parse_args()

    cache_dir = pathlib.Path(args.cache_dir) if args.cache_dir else None
    seed_file = pathlib.Path(args.seed_file) if args.seed_file else None

    if args.command == "backup":
        if args.out is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            out_path = pathlib.Path(f"spherex_backup_{timestamp}.tar.gz")
        else:
            out_path = pathlib.Path(args.out)

        result = backup(out_path=out_path, cache_dir=cache_dir, seed_file=seed_file)
        print(f"Yedek oluşturuldu: {result}")

    elif args.command == "restore":
        count = restore(
            src_path=pathlib.Path(args.src),
            cache_dir=cache_dir,
            seed_file=seed_file,
        )
        print(f"Geri yükleme tamamlandı: {count} dosya işlendi.")


if __name__ == "__main__":
    main()
