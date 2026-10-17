"""
Unit Tests for BrowserProfile & Fingerprints
"""
from stealth_scraper.fingerprint import BrowserProfile

def test_chrome_profile():
    p = BrowserProfile.get_profile("chrome124")
    assert p["impersonate"] == "chrome124"
    assert "Sec-Ch-Ua" in p["headers"]
    assert "Chromium" in p["headers"]["Sec-Ch-Ua"]

def test_safari_profile():
    p = BrowserProfile.get_profile("safari17_0")
    assert p["impersonate"] == "safari17_0"
    assert "Accept" in p["headers"]

def test_fallback_profile():
    p = BrowserProfile.get_profile("unknown_browser")
    assert p["impersonate"] == "chrome124"
