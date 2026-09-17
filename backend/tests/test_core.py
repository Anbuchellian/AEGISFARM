from app.services.risk import assess_risk
from app.services.response_engine import adaptive_retry


def test_high_risk():
    result = assess_risk(0.94, "North-West", "South-East")
    assert result.level == "HIGH"
    assert result.score > 65


def test_retry():
    result = adaptive_retry(None, "Wild Boar", "North-West", "AUDIO_DIRECTIONAL_A")
    assert result.strategy == "LIGHT_PLUS_AUDIO_B"
