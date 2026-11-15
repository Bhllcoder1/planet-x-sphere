"""
test_aladin.py — Aladin Lite yan paneli ve harici katalog bağlantı testleri (Görev 05-14).
"""
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT / "c_sunucu") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "c_sunucu"))

from api.main import create_app
from api.routes.aladin import build_links, TARGETS


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


def test_build_links():
    """build_links fonksiyonu beklenen 3 harici katalog bağlantısını üretir."""
    links = build_links(269.4521, 4.6933)
    assert len(links) == 3
    labels = [l.label for l in links]
    assert "SIMBAD" in labels
    assert "VizieR" in labels
    assert "Legacy Survey" in labels

    for l in links:
        assert l.href.startswith("https://")


def test_aladin_links_endpoint_known_target(client):
    """Tanımlı hedefler (barnard, eps_indi_b vb.) için doğru yanıt ve linkler döner."""
    resp = client.get("/aladin/links/barnard")
    assert resp.status_code == 200
    data = resp.json()
    assert data["target_id"] == "barnard"
    assert data["label"] == "Barnard's Star"
    assert pytest.approx(data["ra"]) == 269.4521
    assert pytest.approx(data["dec"]) == 4.6933
    assert len(data["links"]) == 3


def test_aladin_links_endpoint_custom_coords(client):
    """Bilinmeyen bir hedef için URL'de ra ve dec verilirse 200 döner."""
    resp = client.get("/aladin/links/my_source?ra=120.5&dec=-30.25")
    assert resp.status_code == 200
    data = resp.json()
    assert data["target_id"] == "my_source"
    assert pytest.approx(data["ra"]) == 120.5
    assert pytest.approx(data["dec"]) == -30.25
    assert len(data["links"]) == 3


def test_aladin_links_endpoint_not_found(client):
    """Tanımsız hedef ve koordinat yoksa 404 döner."""
    resp = client.get("/aladin/links/unknown_target_xyz")
    assert resp.status_code == 404


def test_aladin_panel_endpoint(client):
    """GET /aladin/panel Aladin Lite HTML içeriğini döner."""
    resp = client.get("/aladin/panel")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    assert "aladin" in resp.text.lower()
    assert "lgplv3" in resp.text.lower()
