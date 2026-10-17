"""
Adaptive Token Bucket Rate Limiter with Exponential Jitter Backoff
"""
import time
import random
from typing import Optional

class TokenBucketRateLimiter:
    def __init__(self, rate: float = 5.0, capacity: float = 10.0):
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_refill = time.time()

    def acquire(self, tokens: float = 1.0) -> bool:
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_refill = now

        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    @staticmethod
    def calculate_backoff(attempt: int, base: float = 1.0, max_backoff: float = 16.0) -> float:
        backoff = min(max_backoff, base * (2 ** attempt))
        jitter = random.uniform(0.5, 1.5)
        return backoff * jitter
