"""
HDU byte-offset haritası (L1 önbelleği için).

Bir FITS dosyasının S3'teki HDU başlık ve veri başlangıç konumlarını saklar.
Warm okumada header taraması atlanır; sadece veri Range GET yapılır.

SPHEREx L2b dosya düzeni (PLAN_spherex_v3.md §2.4):
  PRIMARY=0, IMAGE=1, FLAGS=2, VARIANCE=3, ZODI=4, EPSF=5, WCS-WAVE=6
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

# SPHEREx L2b dosyasındaki standart HDU isimleri ve indeksleri.
HDU_NAMES: tuple[str, ...] = ("IMAGE", "FLAGS", "VARIANCE", "ZODI", "EPSF", "WCS-WAVE")
HDU_INDICES: tuple[int, ...] = (1, 2, 3, 4, 5, 6)  # PRIMARY=0


@dataclass(frozen=True)
class HduInfo:
    """Tek bir HDU'nun byte-offset ve boyut bilgisi."""

    name: str
    index: int
    header_start: int   # dosya başından FITS başlık bloğunun byte ofseti
    data_start: int     # dosya başından veri bloğunun byte ofseti
    naxis1: int         # sütun sayısı (piksel/satır)
    naxis2: int         # satır sayısı
    bitpix: int         # -32 = float32, 32 = int32, 16 = int16

    def to_dict(self) -> dict[str, Any]:
        """JSON serileştirme için sözlüğe dönüştürür."""
        return {
            "name": self.name,
            "index": self.index,
            "header_start": self.header_start,
            "data_start": self.data_start,
            "naxis1": self.naxis1,
            "naxis2": self.naxis2,
            "bitpix": self.bitpix,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "HduInfo":
        """JSON sözlüğünden HduInfo nesnesi oluşturur."""
        return cls(
            name=str(d["name"]),
            index=int(d["index"]),
            header_start=int(d["header_start"]),
            data_start=int(d["data_start"]),
            naxis1=int(d["naxis1"]),
            naxis2=int(d["naxis2"]),
            bitpix=int(d["bitpix"]),
        )


@dataclass(frozen=True)
class ByteOffsetMap:
    """
    Tek bir FITS dosyasının tüm HDU byte-offset haritası.

    Attributes:
        frame_id:  SPHEREx kare tanımlayıcısı.
        s3_key:    S3 nesne anahtarı (bucket hariç).
        file_size: Dosyanın toplam byte boyutu.
        hdus:      Tüm HDU bilgilerini içeren dondurulmuş demet.
    """

    frame_id: str
    s3_key: str
    file_size: int
    hdus: tuple[HduInfo, ...]

    def get_hdu(self, name: str) -> HduInfo:
        """
        İsme göre HDU bilgisi döndürür.

        Raises:
            KeyError: HDU ismi haritada bulunamazsa.
        """
        for h in self.hdus:
            if h.name == name:
                return h
        raise KeyError(f"HDU {name!r} not found in frame {self.frame_id!r}")

    def row_range(self, hdu_name: str, y0: int, y1: int) -> tuple[int, int]:
        """
        Belirtilen HDU için satır aralığına karşılık gelen byte aralığını
        döndürür; tek bir HTTP Range GET için kullanılır.

        Args:
            hdu_name: HDU ismi (örn. "IMAGE", "FLAGS").
            y0:       İlk satır (dahil, 0 tabanlı).
            y1:       Son satır (hariç, 0 tabanlı).

        Returns:
            (start_byte, end_byte) demeti; end_byte hariç.

        Raises:
            KeyError: HDU ismi haritada bulunamazsa.
            ValueError: Satır aralığı geçersizse.
        """
        if y0 < 0 or y1 < y0:
            raise ValueError(
                f"Invalid row range y0={y0}, y1={y1} for HDU {hdu_name!r}"
            )
        h = self.get_hdu(hdu_name)
        row_stride = h.naxis1 * abs(h.bitpix) // 8
        start = h.data_start + y0 * row_stride
        end = h.data_start + y1 * row_stride
        return start, end

    def to_dict(self) -> dict[str, Any]:
        """JSON serileştirme için sözlüğe dönüştürür."""
        return {
            "frame_id": self.frame_id,
            "s3_key": self.s3_key,
            "file_size": self.file_size,
            "hdus": [h.to_dict() for h in self.hdus],
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "ByteOffsetMap":
        """JSON sözlüğünden ByteOffsetMap nesnesi oluşturur."""
        return cls(
            frame_id=str(d["frame_id"]),
            s3_key=str(d["s3_key"]),
            file_size=int(d["file_size"]),
            hdus=tuple(HduInfo.from_dict(h) for h in d["hdus"]),
        )
