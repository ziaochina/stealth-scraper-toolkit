"""
Unit Tests for TokenBucketRateLimiter
"""
import time
from stealth_scraper.ratelimit import TokenBucketRateLimiter

def test_token_bucket_acquire():
    limiter = TokenBucketRateLimiter(rate=10.0, capacity=2.0)
    assert limiter.acquire(1.0) is True
    assert limiter.acquire(1.0) is True
    assert limiter.acquire(1.0) is False

def test_backoff_calculation():
    b1 = TokenBucketRateLimiter.calculate_backoff(attempt=1, base=1.0)
    assert 0.5 <= b1 <= 4.0
    b3 = TokenBucketRateLimiter.calculate_backoff(attempt=3, base=1.0)
    assert b3 > b1
