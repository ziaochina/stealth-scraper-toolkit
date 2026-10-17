"""
Unit Tests for StealthScraperEngine
"""
from unittest.mock import MagicMock
from stealth_scraper.engine import StealthScraperEngine

def test_engine_init():
    engine = StealthScraperEngine()
    assert engine.metrics["requests"] == 0

def test_engine_fetch_mocked_success():
    engine = StealthScraperEngine()
    mock_session = MagicMock()
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.text = "<html>Mock Content</html>"
    mock_session.get.return_value = mock_resp

    data = engine.fetch("https://example.com", session=mock_session)
    assert data == "<html>Mock Content</html>"
    assert engine.metrics["success"] == 1
    assert engine.metrics["requests"] == 1
