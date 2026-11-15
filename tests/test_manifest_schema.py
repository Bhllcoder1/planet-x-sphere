"""
test_manifest_schema.py — Manifest v2 şema ve örnek doğrulama testleri (Görev 02-11).
"""
import json
from pathlib import Path
import pytest
import jsonschema

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "contracts" / "manifest.schema.json"
EXAMPLE_PATH = REPO_ROOT / "contracts" / "manifest_example.json"


@pytest.fixture
def manifest_schema():
    assert SCHEMA_PATH.exists(), f"Schema file not found at {SCHEMA_PATH}"
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def manifest_example():
    assert EXAMPLE_PATH.exists(), f"Example file not found at {EXAMPLE_PATH}"
    with open(EXAMPLE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def test_schema_itself_is_valid():
    """Şemanın Draft 2020-12 meta-şemasına uygun olduğunu doğrular."""
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)
    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)


def test_manifest_example_validates(manifest_schema, manifest_example):
    """Örnek manifestin şemadan hatasız geçtiğini doğrular."""
    jsonschema.validate(instance=manifest_example, schema=manifest_schema)


def test_missing_required_top_level_fails(manifest_schema, manifest_example):
    """Zorunlu üst düzey alan eksikse şema doğrulamasının hata vermesi gerekir."""
    broken = dict(manifest_example)
    del broken["target"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=broken, schema=manifest_schema)


def test_missing_required_frame_field_fails(manifest_schema, manifest_example):
    """Kare nesnesinde zorunlu alan eksikse şema doğrulamasının hata vermesi gerekir."""
    broken = json.loads(json.dumps(manifest_example))
    del broken["frames"][0]["paths"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=broken, schema=manifest_schema)


def test_invalid_detector_fails(manifest_schema, manifest_example):
    """Geçersiz dedektör adı (ör. D9) verildiğinde şemanın hata vermesi gerekir."""
    broken = json.loads(json.dumps(manifest_example))
    broken["frames"][0]["detector"] = "D9"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=broken, schema=manifest_schema)


def test_invalid_schema_version_fails(manifest_schema, manifest_example):
    """Uyuşmayan schema_version verildiğinde istemci kontrolü için hata vermelidir."""
    broken = json.loads(json.dumps(manifest_example))
    broken["schema_version"] = "1.0.0"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=broken, schema=manifest_schema)
