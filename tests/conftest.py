"""
pytest conftest.py — planet-x-sphere test ortamı.

Sabit tohum: numpy, random modülleri SEED=42 ile başlatılır.
Gerçek veri: tests/fixtures/real/ dizini (git'te değil; .gitignore'da).
Sentetik veri: tests/fixtures/synthetic/ dizini (git'te; küçük boyutlu).
Manifest: tests/fixtures/manifest_example.json
"""
import json
import pathlib
import random
import numpy as np
import pytest

SEED = 42
FIXTURES = pathlib.Path(__file__).parent / "fixtures"
REAL_DATA = FIXTURES / "real"
SYNTHETIC_DATA = FIXTURES / "synthetic"


@pytest.fixture(autouse=True)
def fixed_seed():
    """Her test için sabit tohum (42) uygular."""
    random.seed(SEED)
    np.random.seed(SEED)
    yield


@pytest.fixture
def synthetic_window():
    """100×100 sentetik float32 pencere döndürür."""
    rng = np.random.default_rng(SEED)
    return rng.standard_normal((100, 100)).astype(np.float32)


@pytest.fixture
def manifest_example():
    """Örnek manifest sözlüğünü döndürür."""
    path = FIXTURES / "manifest_example.json"
    return json.loads(path.read_text(encoding="utf-8"))
