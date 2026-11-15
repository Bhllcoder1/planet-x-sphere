"""
timing.py — Adım adım zamanlama logları ve GPU tetik raporu.

Her istek için fetch/compute/serialize sürelerini kaydeder.
GPU tetik koşulu: D9 p50 > 2.0 s olursa vast.ai GPU kiralama önerilir.

Kullanım örneği:
    timing = RequestTiming(frame_id="2025-01-15T12:00:00Z")
    with timing.measure("fetch"):
        data = s3_range_get(...)
    with timing.measure("compute"):
        result = numpy_process(data)
    with timing.measure("serialize"):
        payload = json.dumps(result)
    collector.record(timing)
    report = collector.gpu_report()
"""
from __future__ import annotations

import logging
import time
from collections import deque
from contextlib import contextmanager
from dataclasses import dataclass, field
from statistics import median
from typing import Generator

logger = logging.getLogger(__name__)


@dataclass
class RequestTiming:
    """Tek bir HTTP isteğinin adım adım zamanlama kayıtları."""

    frame_id: str = ""
    fetch_s: float = 0.0        # S3 Range GET süresi (saniye)
    compute_s: float = 0.0      # numpy işleme süresi (saniye)
    serialize_s: float = 0.0    # JSON/PNG serializasyon süresi (saniye)
    total_s: float = 0.0        # Toplam istek süresi (saniye)

    @contextmanager
    def measure(self, step: str) -> Generator[None, None, None]:
        """
        Belirtilen adımın süresini ölçer ve ilgili alana yazar.

        Args:
            step: Ölçülecek adım adı — 'fetch', 'compute' veya 'serialize'.

        Raises:
            ValueError: Bilinmeyen adım adı verilirse.

        Kullanım:
            with timing.measure('fetch'):
                data = s3_range_get(key)
        """
        allowed_steps = {"fetch", "compute", "serialize"}
        if step not in allowed_steps:
            raise ValueError(
                f"Bilinmeyen adım: '{step}'. "
                f"Geçerli adımlar: {allowed_steps}"
            )

        t0 = time.perf_counter()
        try:
            yield
        finally:
            elapsed = time.perf_counter() - t0
            setattr(self, f"{step}_s", elapsed)
            self.total_s = self.fetch_s + self.compute_s + self.serialize_s
            logger.debug(
                "zamanlama | frame=%s adım=%s süre=%.4fs",
                self.frame_id,
                step,
                elapsed,
            )

    def to_dict(self) -> dict:
        """Zamanlama verilerini dict olarak döndürür (JSON serializasyonu için)."""
        return {
            "frame_id": self.frame_id,
            "fetch_s": round(self.fetch_s, 4),
            "compute_s": round(self.compute_s, 4),
            "serialize_s": round(self.serialize_s, 4),
            "total_s": round(self.total_s, 4),
        }

    def gpu_trigger_check(self) -> bool:
        """
        D9 tetik koşulunu kontrol eder.

        Eşik: fetch_s > 2.0 saniye  [ASSUMPTION: D9 testi (01-05/01-06) sonrası güncellenecek]

        Returns:
            True ise vast.ai GPU kiralama tetiklenmeli.
        """
        triggered = self.fetch_s > 2.0
        if triggered:
            logger.warning(
                "GPU tetik: frame=%s fetch=%.4fs > 2.0s eşiği",
                self.frame_id,
                self.fetch_s,
            )
        return triggered


class TimingCollector:
    """
    Son N isteğin zamanlama istatistiklerini rolling window ile tutar.

    Thread-safety notu: Bu sınıf tek-thread FastAPI worker için tasarlanmıştır.
    Çok-thread ortamda deque thread-safe olduğundan okuma/yazma güvenlidir,
    ancak p50/p95 hesaplamaları atomik değildir.
    """

    def __init__(self, maxlen: int = 100) -> None:
        """
        Args:
            maxlen: Tutulacak maksimum kayıt sayısı (varsayılan: 100).
        """
        self._fetch_times: deque[float] = deque(maxlen=maxlen)
        self._total_times: deque[float] = deque(maxlen=maxlen)

    def record(self, timing: RequestTiming) -> None:
        """
        Yeni bir RequestTiming kaydını koleksiyona ekler.

        Args:
            timing: Kaydedilecek zamanlama nesnesi.
        """
        self._fetch_times.append(timing.fetch_s)
        self._total_times.append(timing.total_s)
        logger.debug(
            "collector | kayıt eklendi frame=%s toplam_kayıt=%d",
            timing.frame_id,
            len(self._fetch_times),
        )

    def p50(self) -> float:
        """
        fetch_s için 50. yüzdelik (medyan) değeri döndürür.

        Returns:
            Medyan fetch süresi; kayıt yoksa 0.0.
        """
        if not self._fetch_times:
            return 0.0
        return median(self._fetch_times)

    def p95(self) -> float:
        """
        fetch_s için 95. yüzdelik değeri döndürür.

        Returns:
            95. yüzdelik fetch süresi; kayıt yoksa 0.0.
        """
        if not self._fetch_times:
            return 0.0
        sorted_times = sorted(self._fetch_times)
        # Yüzdelik indeks hesabı (doğrusal interpolasyon olmadan nearest-rank)
        idx = max(0, int(len(sorted_times) * 0.95) - 1)
        return sorted_times[idx]

    def gpu_report(self) -> dict:
        """
        GPU tetik raporu döndürür.

        Tetik koşulu: fetch p50 > 2.0 saniye
        [ASSUMPTION: Eşik D9 testi (01-05/01-06) sonrası güncellenecek]

        Returns:
            Rapor dict'i; frontend/ops araçları tarafından okunabilir.
        """
        p50_val = self.p50()
        p95_val = self.p95()
        trigger = p50_val > 2.0

        return {
            "fetch_p50_s": round(p50_val, 4),
            "fetch_p95_s": round(p95_val, 4),
            "sample_count": len(self._fetch_times),
            "gpu_trigger": trigger,
            "recommendation": (
                "vast.ai GPU kiralama" if trigger else "CPU yeterli"
            ),
            "note": (
                "Eşik [ASSUMPTION]; D9 testi (01-05/01-06) sonrası güncellenecek"
            ),
        }


# ---------------------------------------------------------------------------
# Global singleton — uygulama genelinde tek kolektör
# ---------------------------------------------------------------------------
collector = TimingCollector()
