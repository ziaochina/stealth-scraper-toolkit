"""
Production Stealth Scraper Engine
Encapsulates TLS fingerprint impersonation, retry backoff, and metric tracking.
"""
import time
import logging
from typing import Optional, Dict, Any
from .fingerprint import BrowserProfile
from .ratelimit import TokenBucketRateLimiter

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class StealthScraperEngine:
    def __init__(self, browser_profile: str = "chrome124", max_rps: float = 5.0):
        self.profile = BrowserProfile.get_profile(browser_profile)
        self.rate_limiter = TokenBucketRateLimiter(rate=max_rps, capacity=max_rps * 2)
        self.metrics = {"requests": 0, "success": 0, "errors": 0, "retries": 0}

    def fetch(self, url: str, max_retries: int = 3, session: Optional[Any] = None) -> Optional[str]:
        """
        Executes an anti-bot protected GET request.
        Supports dependency-injected session or lazy curl_cffi session.
        """
        self.metrics["requests"] += 1
        
        # Rate limit token acquisition
        while not self.rate_limiter.acquire():
            time.sleep(0.05)

        for attempt in range(1, max_retries + 1):
            try:
                if session is None:
                    try:
                        from curl_cffi import requests
                        session = requests.Session(impersonate=self.profile["impersonate"])
                    except ImportError:
                        import urllib.request
                        req = urllib.request.Request(url, headers=self.profile["headers"])
                        with urllib.request.urlopen(req, timeout=10) as resp:
                            data = resp.read().decode("utf-8")
                            self.metrics["success"] += 1
                            return data

                resp = session.get(url, headers=self.profile["headers"], timeout=15)
                if resp.status_code == 200:
                    self.metrics["success"] += 1
                    return resp.text
                elif resp.status_code in (403, 429):
                    self.metrics["retries"] += 1
                    wait = TokenBucketRateLimiter.calculate_backoff(attempt)
                    time.sleep(wait)
            except Exception as e:
                self.metrics["errors"] += 1
                if attempt == max_retries:
                    break
                time.sleep(1.0)
        return None
