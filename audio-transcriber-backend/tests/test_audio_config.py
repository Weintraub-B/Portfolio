def test_config_constants():
    from app.stream_config import MIC_CONFIG
    assert "sample_rate" in MIC_CONFIG
