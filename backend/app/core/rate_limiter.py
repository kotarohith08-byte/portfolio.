"""
StudyChart AI - In-Memory & Redis-Compatible Rate Limiter.
"""

import time
from collections import defaultdict
from typing import Dict, List
from fastapi import Request
from app.core.errors import RateLimitExceededException

class InMemoryRateLimiter:
    def __init__(self):
        # Maps key (e.g. "auth:127.0.0.1" or "user_id:ai") -> list of timestamps
        self._history: Dict[str, List[float]] = defaultdict(list)

    def is_rate_limited(self, key: str, max_requests: int, window_seconds: int = 60) -> bool:
        now = time.time()
        window_start = now - window_seconds
        
        # Clean older requests
        self._history[key] = [t for t in self._history[key] if t > window_start]

        if len(self._history[key]) >= max_requests:
            return True

        self._history[key].append(now)
        return False

rate_limiter = InMemoryRateLimiter()

def check_rate_limit(request: Request, limit_type: str = "general", max_requests: int = 60, window_seconds: int = 60):
    client_ip = request.client.host if request.client else "unknown"
    key = f"{limit_type}:{client_ip}"
    if rate_limiter.is_rate_limited(key, max_requests=max_requests, window_seconds=window_seconds):
        raise RateLimitExceededException(
            message=f"Rate limit exceeded for {limit_type}. Allowed: {max_requests} requests per {window_seconds}s."
        )
