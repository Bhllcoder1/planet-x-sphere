"""
test_stack.py — D10 yığma birimi testi.

D10: 10 kare üzerinde medyan yığması.
Sentetik verilerle test: gürültü azalması doğrulanır.
"""
from __future__ import annotations

import numpy as np
import pytest


# ---------------------------------------------------------------------------
# Yardımcı: test kapsamında D10 medyan yığması
# ---------------------------------------------------------------------------

def _median_stack_d10(frames: list[np.ndarray]) -> np.ndarray:
    """
    D10 medyan yığması: ``frames`` listesindeki dizilerin eleman-bazlı
    medyanını alır ve sonucu float32 olarak döndürür.

    Parametreler
    ------------
    frames:
        Aynı şekil ve dtype'a sahip numpy dizilerinin listesi (en az 1 eleman).

    Fırlatır
    --------
    ValueError:
        ``frames`` boş ise.
    """
    if not frames:
        raise ValueError("D10 yığması için en az bir kare gereklidir.")
    result = np.median(frames, axis=0)
    return result.astype(np.float32)


# ---------------------------------------------------------------------------
# Testler
# ---------------------------------------------------------------------------

def test_median_stack_reduces_noise() -> None:
    """10 kare medyan yığması standart sapmayı azaltmalıdır."""
    rng = np.random.default_rng(42)
    frames: list[np.ndarray] = [
        rng.standard_normal((100, 100)).astype(np.float32) for _ in range(10)
    ]

    # Arrange
    single_std: float = float(np.std(frames[0]))

    # Act
    stack = _median_stack_d10(frames)

    # Assert
    stacked_std: float = float(np.std(stack))
    assert stacked_std < single_std * 0.6, (
        f"Gürültü azalmadı: {stacked_std:.3f} >= {single_std * 0.6:.3f}"
    )


def test_stack_returns_float32() -> None:
    """Yığma sonucu float32 dtype ile dönmeli."""
    rng = np.random.default_rng(42)
    frames: list[np.ndarray] = [
        rng.standard_normal((64, 64)).astype(np.float32) for _ in range(10)
    ]

    # Act
    stack = _median_stack_d10(frames)

    # Assert
    assert stack.dtype == np.float32, (
        f"Beklenen dtype float32, alınan: {stack.dtype}"
    )


def test_empty_stack_raises() -> None:
    """Boş kare listesi ValueError fırlatmalıdır."""
    # Act + Assert
    with pytest.raises(ValueError, match="en az bir kare"):
        _median_stack_d10([])


def test_stack_shape_matches_input(synthetic_window: np.ndarray) -> None:
    """Yığma sonucunun şekli girdi karelerinin şekliyle eşleşmeli."""
    rng = np.random.default_rng(42)
    # conftest.py'deki synthetic_window fixture'ını temel kare olarak kullan
    frames: list[np.ndarray] = [
        (synthetic_window + rng.standard_normal(synthetic_window.shape).astype(np.float32) * 0.1)
        for _ in range(10)
    ]

    # Act
    stack = _median_stack_d10(frames)

    # Assert
    assert stack.shape == synthetic_window.shape, (
        f"Şekil uyuşmazlığı: {stack.shape} != {synthetic_window.shape}"
    )
