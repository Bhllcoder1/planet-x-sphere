"""
test_skybot.py — IMCCE SkyBoT etiketleme testleri (Görev 04-09).
"""
import sys
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT / "c_sunucu") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "c_sunucu"))

from api.skybot import (
    angular_distance_arcsec,
    mjd_to_jd,
    parse_skybot_dec,
    parse_skybot_ra,
    tag_candidates,
)


def test_mjd_to_jd():
    """MJD'den JD'ye dönüşüm: JD = MJD + 2400000.5."""
    mjd = 60000.0
    jd = mjd_to_jd(mjd)
    assert jd == 2460000.5


def test_parse_skybot_ra_and_dec():
    """HMS ve DMS koordinat dizelerinin dereceye dönüştürülmesini doğrular."""
    ra_str = "12 00 00.00"  # 12h = 180 derece
    dec_pos = "+45 00 00.0"
    dec_neg = "-30 30 00.0"

    assert parse_skybot_ra(ra_str) == 180.0
    assert parse_skybot_dec(dec_pos) == 45.0
    assert parse_skybot_dec(dec_neg) == -30.5


def test_matching_with_asteroid():
    """Bilinen asteroit ile 3 px (~18.6") içinde eşleşen adaya 'olası: {ad}' etiketi verilir."""
    mock_skybot_data = [
        {
            "Name": "20 Massalia",
            "RA (hms)": "12 00 00.00",
            "DEC (dms)": "+00 00 00.0",
            "VMag": 10.9,
            "Err": 0.02,
        }
    ]

    candidates = [
        # Tam konumda aday (mesafe ~ 0)
        {"id": "cand_1", "ra": 180.0, "dec": 0.0},
        # 10 arcsec uzakta aday (10" < 18.6", eşleşmeli)
        {"id": "cand_2", "ra": 180.002, "dec": 0.0},
        # 100 arcsec uzakta aday (100" > 18.6", eşleşmemeli)
        {"id": "cand_3", "ra": 180.03, "dec": 0.0},
    ]

    tagged = tag_candidates(candidates, mock_skybot_data)

    assert tagged[0]["skybot_tag"] == "olası: 20 Massalia"
    assert tagged[0]["skybot_matched"] is True

    assert tagged[1]["skybot_tag"] == "olası: 20 Massalia"
    assert tagged[1]["skybot_matched"] is True

    assert tagged[2]["skybot_tag"] == "aday"
    assert tagged[2]["skybot_matched"] is False


def test_skybot_service_down_fallback():
    """SkyBoT servisi erişilemez olduğunda (None) akış çökmez, 'untagged' etiketi verilir."""
    candidates = [{"id": "cand_1", "ra": 180.0, "dec": 0.0}]
    tagged = tag_candidates(candidates, skybot_data=None)

    assert len(tagged) == 1
    assert tagged[0]["skybot_tag"] == "untagged"
    assert tagged[0]["skybot_matched"] is False
