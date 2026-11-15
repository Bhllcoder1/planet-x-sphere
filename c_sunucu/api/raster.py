"""
raster.py — R-k sunucu taraflı raster modu.

Referans frame'i (en düşük θ ile) seçer, diğer kareleri
en yakın komşu yeniden örnekleme ile hizalar.

k=4..8: yeniden örnekleme faktörü; daha yüksek k → daha iyi hizalama,
daha büyük çıktı boyutu.

θ_res: iki kare arasındaki açısal roll farkı (derece).
Rozet eşiği: θ_res > 0.68° → "R-k modu aktif" rozeti.

[V: s0_A] Barnard D2 θ_spread 0.72–1.42°; θ_res_max 0.68° için
31×31 pencere eşiği; bu eşik çoğu Barnard D2 geçiş çiftinde aşılır.
"""
from __future__ import annotations

import logging
from collections import Counter
from dataclasses import dataclass
from typing import List

import numpy as np

logger = logging.getLogger(__name__)

# Derece cinsinden eşik: 31×31 pencere Mode-N için üst sınır [V: PLAN §2.2]
THETA_RES_THRESHOLD: float = 0.68

# Varsayılan yeniden örnekleme faktörü (k=4..8 arası)
RASTER_K_DEFAULT: int = 4

# Geçerli k değerleri aralığı
RASTER_K_MIN: int = 4
RASTER_K_MAX: int = 8

# SPHEREx piksel ölçeği (arcsec/piksel) [NV; s0_A başlıklarından çıkarıldı]
SPHEREX_PIXEL_SCALE_ARCSEC: float = 6.2


@dataclass(frozen=True)
class RasterResult:
    """R-k yeniden örnekleme sonucu."""

    image: np.ndarray
    """float32, shape (H*k, W*k) — yeniden örneklenmiş görüntü."""

    reference_frame_id: str
    """Referans kare kimliği (en düşük θ_res'e sahip kare)."""

    theta_res_deg: float
    """Bu kare ile referans kare arasındaki açısal roll farkı (derece)."""

    badge: str
    """
    Görüntü rozeti.
    "mode-n"       → θ_res ≤ THETA_RES_THRESHOLD (Mode N geçerli)
    "rk-k=<k>"     → θ_res > THETA_RES_THRESHOLD (R-k modu aktif)
    """

    rk_active: bool
    """θ_res > THETA_RES_THRESHOLD ise True; bu karede R-k modu etkin."""


def nearest_neighbor_resample(arr: np.ndarray, k: int) -> np.ndarray:
    """
    En yakın komşu yeniden örnekleme ile arr'ı k× büyütür.

    Parameters
    ----------
    arr:
        Giriş dizisi, float32, shape (H, W).
    k:
        Büyütme faktörü. Geçerli aralık: 4..8.

    Returns
    -------
    np.ndarray
        float32, shape (H*k, W*k). Her piksel k×k blok olarak kopyalanır.

    Raises
    ------
    ValueError
        arr iki boyutlu değilse veya k geçerli aralık dışındaysa.
    """
    if arr.ndim != 2:
        raise ValueError(
            f"arr iki boyutlu olmalı; alınan shape: {arr.shape}"
        )
    if not (RASTER_K_MIN <= k <= RASTER_K_MAX):
        raise ValueError(
            f"k {RASTER_K_MIN}..{RASTER_K_MAX} aralığında olmalı; alınan: {k}"
        )
    # np.repeat satırları (axis=0) sonra sütunları (axis=1) k× çoğaltır.
    result = np.repeat(np.repeat(arr, k, axis=0), k, axis=1)
    return result.astype(np.float32)


def compute_theta_res(sps_epa_ref: float, sps_epa_target: float) -> float:
    """
    İki SPS_EPA değeri arasındaki açısal roll farkını hesaplar.

    SPHEREx SPS_EPA değerleri nominal olarak 0° veya 180° alır
    (dedektör yönelimi). Farkın modulo-180 üzerinden hesaplanması
    karşılıklı yönleri doğru biçimde işler.

    Parameters
    ----------
    sps_epa_ref:
        Referans karenin SPS_EPA değeri (derece).
    sps_epa_target:
        Hedef karenin SPS_EPA değeri (derece).

    Returns
    -------
    float
        [0, 90] aralığında açısal roll farkı (derece).

    Examples
    --------
    >>> compute_theta_res(0.0, 0.0)
    0.0
    >>> compute_theta_res(0.0, 180.0)
    0.0
    >>> compute_theta_res(0.0, 1.0)
    1.0
    >>> compute_theta_res(0.0, 90.0)
    90.0
    """
    diff = abs(sps_epa_ref - sps_epa_target) % 180.0
    return float(min(diff, 180.0 - diff))


def select_reference_frame(sps_epas: List[float]) -> int:
    """
    SPS_EPA (0 veya 180) listesinden referans kare indeksini seçer.

    Strateji: en çok tekrar eden SPS_EPA yönelimini belirle; bu
    yönelime sahip ilk kareyi referans olarak döndür. Eşitlik
    durumunda 0° önceliklidir; liste boşsa ValueError fırlatılır.

    Parameters
    ----------
    sps_epas:
        Her kare için SPS_EPA değerlerinin listesi (derece).

    Returns
    -------
    int
        Referans kare indeksi (0 tabanlı).

    Raises
    ------
    ValueError
        sps_epas boşsa.
    """
    if not sps_epas:
        raise ValueError("sps_epas listesi boş olamaz.")

    # Her değeri 180° modülüne indirgeyerek karşılaştır (0 ve 180 eş değer)
    normalized = [round(v % 180.0, 6) for v in sps_epas]

    counts = Counter(normalized)
    # En çok tekrar eden değeri seç; eşitlikte küçük değer öncelikli
    dominant = max(counts, key=lambda v: (counts[v], -v))

    # Dominant yönelime sahip ilk kareyi referans al
    for idx, val in enumerate(normalized):
        if val == dominant:
            return idx

    # Bu noktaya asla ulaşılmamalı
    return 0  # pragma: no cover


def _build_badge(rk_active: bool, k: int) -> str:
    """
    Rozet dizesini oluşturur.

    Parameters
    ----------
    rk_active:
        R-k modunun etkin olup olmadığı.
    k:
        Yeniden örnekleme faktörü.

    Returns
    -------
    str
        "mode-n" veya "rk-k=<k>".
    """
    return f"rk-k={k}" if rk_active else "mode-n"


def apply_raster(
    frames: List[np.ndarray],
    sps_epas: List[float],
    frame_ids: List[str],
    k: int = RASTER_K_DEFAULT,
) -> List[RasterResult]:
    """
    Kare listesini R-k ile yeniden örnekler.

    Her kare için:
    1. Referans kareyi seç (dominant SPS_EPA yönelimi).
    2. θ_res = referans ile hedef arasındaki açısal roll farkı.
    3. Kareyi en yakın komşu ile k× büyüt.
    4. θ_res > THETA_RES_THRESHOLD ise "rk-k=<k>", değilse "mode-n" rozeti.

    Parameters
    ----------
    frames:
        Görüntü dizilerinin listesi; her biri float32, shape (H, W).
        Tüm kareler aynı boyutta olmalıdır.
    sps_epas:
        Her kare için SPS_EPA değeri (derece). `frames` ile aynı uzunlukta.
    frame_ids:
        Her kare için benzersiz kimlik dizesi. `frames` ile aynı uzunlukta.
    k:
        Yeniden örnekleme faktörü. Varsayılan: 4. Geçerli aralık: 4..8.

    Returns
    -------
    List[RasterResult]
        Her giriş karesi için bir RasterResult nesnesi.

    Raises
    ------
    ValueError
        Listeler farklı uzunluktaysa, frames boşsa veya k geçersizse.

    Notes
    -----
    [V: s0_A] Barnard D2 aynı geçiş θ_spread: 0.72° / 0.72° / 1.42°.
    Bu değerlerin tamamı THETA_RES_THRESHOLD (0.68°) değerini aşar;
    dolayısıyla Barnard D2 geçiş çiftlerinde R-k modu neredeyse her
    zaman aktif olur.

    ε Indi A D3: 1.08–3.84° → eşiği her zaman aşar.
    """
    n = len(frames)
    if n == 0:
        raise ValueError("frames listesi boş olamaz.")
    if len(sps_epas) != n:
        raise ValueError(
            f"sps_epas uzunluğu ({len(sps_epas)}) frames ile eşleşmiyor ({n})."
        )
    if len(frame_ids) != n:
        raise ValueError(
            f"frame_ids uzunluğu ({len(frame_ids)}) frames ile eşleşmiyor ({n})."
        )
    if not (RASTER_K_MIN <= k <= RASTER_K_MAX):
        raise ValueError(
            f"k {RASTER_K_MIN}..{RASTER_K_MAX} aralığında olmalı; alınan: {k}"
        )

    # Boyut tutarlılığı kontrolü
    ref_shape = frames[0].shape
    for i, f in enumerate(frames):
        if f.shape != ref_shape:
            raise ValueError(
                f"Kare {i} ({frame_ids[i]}) shape {f.shape} beklenen "
                f"{ref_shape} ile uyuşmuyor."
            )

    # Referans kare seç
    ref_idx = select_reference_frame(sps_epas)
    ref_epa = sps_epas[ref_idx]
    ref_id = frame_ids[ref_idx]

    logger.debug(
        "Referans kare: %s (SPS_EPA=%.2f°, indeks=%d)",
        ref_id,
        ref_epa,
        ref_idx,
    )

    results: List[RasterResult] = []
    for i, (frame, epa, fid) in enumerate(zip(frames, sps_epas, frame_ids)):
        theta_res = compute_theta_res(ref_epa, epa)
        rk_active = theta_res > THETA_RES_THRESHOLD
        badge = _build_badge(rk_active, k)

        resampled = nearest_neighbor_resample(frame.astype(np.float32), k)

        logger.debug(
            "Kare %s: θ_res=%.3f° rk_active=%s rozet='%s'",
            fid,
            theta_res,
            rk_active,
            badge,
        )

        results.append(
            RasterResult(
                image=resampled,
                reference_frame_id=ref_id,
                theta_res_deg=theta_res,
                badge=badge,
                rk_active=rk_active,
            )
        )

    return results
