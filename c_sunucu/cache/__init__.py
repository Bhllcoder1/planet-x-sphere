"""
Önbellek paketi: L0 / L1 / L2 önbellek katmanları ve byte-offset haritası.

Katman özeti
------------
L0 — Frame listeleri (TAP sonuçları JSON olarak).
     Bir hedef için bir kez indirilir, dondurulur.
     Dizin: ``L0_CACHE_DIR/{target_id}/frames.json``

L1 — Dosya başına byte-offset haritaları.
     HDU başlık ve veri başlangıç konumları JSON olarak saklanır;
     warm okumada HDU başlık taraması atlanır, doğrudan Range GET yapılır.
     Dizin: ``L1_CACHE_DIR/{frame_id}.json``

L2 — Önceden hesaplanmış pencere dosyaları (.npz) ve thumbnail PNG'ler.
     Her (frame_id, x0, y0, width, height) penceresi için numpy dizileri.
     Dizin: ``L2_CACHE_DIR/{frame_id}/{x0}_{y0}_{width}_{height}.npz``

Kullanım örneği
---------------
::

    from c_sunucu.cache import (
        CacheMiss,
        load_frames, save_frames,
        load_offset_map, save_offset_map,
        load_window, save_window,
        ByteOffsetMap, HduInfo,
    )
"""
from __future__ import annotations

from .l0_cache import (
    CacheMiss,
    FrameRecord,
    load_frames,
    save_frames,
)
from .byte_offset_map import (
    HduInfo,
    ByteOffsetMap,
    HDU_NAMES,
    HDU_INDICES,
)
from .l1_cache import (
    load_offset_map,
    save_offset_map,
    has_offset_map,
)
from .l2_cache import (
    WindowKey,
    WindowData,
    load_window,
    save_window,
    has_window,
    load_thumbnail,
    save_thumbnail,
)

__all__: list[str] = [
    # Hata sınıfı (tüm katmanlarda kullanılır)
    "CacheMiss",
    # L0 — frame listesi
    "FrameRecord",
    "load_frames",
    "save_frames",
    # Byte-offset haritası (L1 veri modeli)
    "HduInfo",
    "ByteOffsetMap",
    "HDU_NAMES",
    "HDU_INDICES",
    # L1 — byte-offset haritası I/O
    "load_offset_map",
    "save_offset_map",
    "has_offset_map",
    # L2 — pencere ve thumbnail
    "WindowKey",
    "WindowData",
    "load_window",
    "save_window",
    "has_window",
    "load_thumbnail",
    "save_thumbnail",
]
