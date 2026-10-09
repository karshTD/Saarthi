"""Shared-access-code gate and a small in-memory rate limiter for AI endpoints.

This is deliberately minimal: it stops casual abuse of a public demo (and of the LLM key),
it is not user authentication. The rate limiter is per-process, so with several workers
the effective limit is multiplied by the worker count.
"""
import secrets
import threading
import time
from collections import defaultdict, deque

from fastapi import Header, HTTPException, Request

from app.core.config import settings


def require_access_code(x_access_code: str | None = Header(default=None)) -> None:
    expected = settings.access_code
    if not expected:
        return
    if not x_access_code or not secrets.compare_digest(
        x_access_code.encode(), expected.encode()
    ):
        raise HTTPException(status_code=401, detail="Invalid or missing access code")


class RateLimiter:
    def __init__(self) -> None:
        self._hits: dict[str, deque[float]] = defaultdict(deque)
        self._lock = threading.Lock()

    def allow(self, key: str, limit: int, window: float = 60.0) -> bool:
        now = time.monotonic()
        with self._lock:
            hits = self._hits[key]
            while hits and now - hits[0] >= window:
                hits.popleft()
            if len(hits) >= limit:
                return False
            hits.append(now)
            return True

    def reset(self) -> None:
        with self._lock:
            self._hits.clear()


limiter = RateLimiter()


def _client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def rate_limit_ai(request: Request) -> None:
    limit = settings.ai_rate_limit_per_minute
    if limit <= 0:
        return
    if not limiter.allow(_client_ip(request), limit):
        raise HTTPException(
            status_code=429,
            detail="Too many AI requests. Please wait a minute and try again.",
            headers={"Retry-After": "60"},
        )
