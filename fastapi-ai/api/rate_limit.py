import time
from collections import defaultdict, deque
from collections.abc import Callable

from fastapi import HTTPException, Request


class RateLimiter:
    """Fixed-window request counter: at most `max_requests` per client per
    `window_seconds`, oldest hits aging out of the window on each call."""

    def __init__(
        self,
        max_requests: int,
        window_seconds: float,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._max_requests = max_requests
        self._window_seconds = window_seconds
        self._clock = clock
        self._hits: dict[str, deque[float]] = defaultdict(deque)

    @staticmethod
    def _client_key(request: Request) -> str:
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        return request.client.host if request.client else "unknown"

    def __call__(self, request: Request) -> None:
        key = self._client_key(request)
        now = self._clock()
        hits = self._hits[key]

        while hits and now - hits[0] > self._window_seconds:
            hits.popleft()

        if len(hits) >= self._max_requests:
            retry_after = max(0.0, self._window_seconds - (now - hits[0]))
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please slow down and try again shortly.",
                headers={"Retry-After": str(int(retry_after) + 1)},
            )

        hits.append(now)


def _build_chat_rate_limiter() -> RateLimiter:
    from config.settings import settings

    return RateLimiter(
        max_requests=settings.chat_rate_limit_requests,
        window_seconds=settings.chat_rate_limit_window_seconds,
    )


chat_rate_limiter = _build_chat_rate_limiter()
