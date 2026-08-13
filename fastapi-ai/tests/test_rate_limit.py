import pytest
from fastapi import HTTPException

from api.rate_limit import RateLimiter


class _FakeClient:
    def __init__(self, host):
        self.host = host


class _FakeRequest:
    def __init__(self, host="1.2.3.4", forwarded_for=None):
        self.client = _FakeClient(host)
        self.headers = {"x-forwarded-for": forwarded_for} if forwarded_for else {}


class _FakeClock:
    def __init__(self, start=0.0):
        self.now = start

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += seconds


def test_allows_requests_within_the_limit():
    limiter = RateLimiter(max_requests=3, window_seconds=60)
    request = _FakeRequest()

    for _ in range(3):
        limiter(request)  # should not raise


def test_blocks_the_request_that_exceeds_the_limit():
    limiter = RateLimiter(max_requests=2, window_seconds=60)
    request = _FakeRequest()

    limiter(request)
    limiter(request)

    with pytest.raises(HTTPException) as exc_info:
        limiter(request)

    assert exc_info.value.status_code == 429
    assert "Retry-After" in exc_info.value.headers


def test_old_hits_age_out_of_the_window():
    clock = _FakeClock()
    limiter = RateLimiter(max_requests=1, window_seconds=10, clock=clock)
    request = _FakeRequest()

    limiter(request)
    with pytest.raises(HTTPException):
        limiter(request)

    clock.advance(10.01)
    limiter(request)  # the first hit has aged out, so this is allowed again


def test_clients_are_tracked_independently():
    limiter = RateLimiter(max_requests=1, window_seconds=60)

    limiter(_FakeRequest(host="1.1.1.1"))
    limiter(_FakeRequest(host="2.2.2.2"))  # different client, own budget


def test_x_forwarded_for_is_preferred_over_direct_client_host():
    limiter = RateLimiter(max_requests=1, window_seconds=60)

    limiter(_FakeRequest(host="10.0.0.1", forwarded_for="9.9.9.9"))
    with pytest.raises(HTTPException):
        limiter(_FakeRequest(host="10.0.0.2", forwarded_for="9.9.9.9"))


def test_x_forwarded_for_uses_first_hop_when_chained():
    limiter = RateLimiter(max_requests=1, window_seconds=60)

    limiter(_FakeRequest(forwarded_for="9.9.9.9, 10.0.0.1"))
    with pytest.raises(HTTPException):
        limiter(_FakeRequest(forwarded_for="9.9.9.9, 10.0.0.2"))
