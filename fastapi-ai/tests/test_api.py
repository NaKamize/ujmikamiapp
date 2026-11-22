from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

import api.routes as routes_module
from api.rate_limit import chat_rate_limiter
from config.settings import settings
from main import app
from services.chroma_service import ChromaServiceError


class _FakeMessage:
    def __init__(self, content):
        self.content = content


async def _fake_astream(inputs, stream_mode=None):
    for node, content in [
        ("retrieve_context", ""),
        ("synthesize_response", "Hello "),
        ("synthesize_response", "world"),
    ]:
        yield _FakeMessage(content), {"langgraph_node": node}


class _FakeGraph:
    def astream(self, inputs, stream_mode=None):
        return _fake_astream(inputs, stream_mode=stream_mode)


class _FakeFailingGraph:
    def astream(self, inputs, stream_mode=None):
        async def gen():
            raise ConnectionError("Connection refused")
            yield  # pragma: no cover - unreachable, keeps this an async generator

        return gen()


@pytest.fixture(autouse=True)
def fake_graph(monkeypatch):
    monkeypatch.setattr(routes_module, "graph", _FakeGraph())


@pytest.fixture(autouse=True)
def reset_chat_rate_limiter():
    chat_rate_limiter._hits.clear()
    yield
    chat_rate_limiter._hits.clear()


def test_health():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_chroma_health(monkeypatch):
    fake_chroma = AsyncMock()
    fake_chroma.heartbeat.return_value = 12345
    monkeypatch.setattr(routes_module, "chroma_service", fake_chroma)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/chroma/health")

    assert response.status_code == 200
    assert response.json() == {"heartbeat": 12345}


async def test_chroma_health_returns_503_on_failure(monkeypatch):
    fake_chroma = AsyncMock()
    fake_chroma.heartbeat.side_effect = ChromaServiceError("down")
    monkeypatch.setattr(routes_module, "chroma_service", fake_chroma)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/chroma/health")

    assert response.status_code == 503


async def test_chat_streams_only_synthesize_response_tokens():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/v1/chat", json={"query": "What is Jozef's background?"})

    assert response.status_code == 200
    assert response.text == "Hello world"


async def test_chat_streams_error_message_on_agent_failure(monkeypatch):
    monkeypatch.setattr(routes_module, "graph", _FakeFailingGraph())

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/v1/chat", json={"query": "anything"})

    assert response.status_code == 200
    assert "agent error" in response.text


def test_chat_rejects_missing_query_field():
    client = TestClient(app)
    response = client.post("/api/v1/chat", json={})
    assert response.status_code == 422


def test_chat_rejects_empty_query_string():
    client = TestClient(app)
    response = client.post("/api/v1/chat", json={"query": ""})
    assert response.status_code == 422


def test_chat_rejects_query_over_max_length():
    client = TestClient(app)
    oversized_query = "x" * (settings.chat_max_query_length + 1)
    response = client.post("/api/v1/chat", json={"query": oversized_query})
    assert response.status_code == 422


async def test_chat_rate_limits_after_too_many_requests():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        for _ in range(settings.chat_rate_limit_requests):
            response = await client.post("/api/v1/chat", json={"query": "hi"})
            assert response.status_code == 200

        response = await client.post("/api/v1/chat", json={"query": "one too many"})

    assert response.status_code == 429
    assert "Retry-After" in response.headers


async def test_chat_rate_limit_tracks_clients_independently():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        for _ in range(settings.chat_rate_limit_requests):
            response = await client.post(
                "/api/v1/chat", json={"query": "hi"}, headers={"x-forwarded-for": "1.1.1.1"}
            )
            assert response.status_code == 200

        # A different client IP has its own budget and isn't blocked by the one above.
        response = await client.post(
            "/api/v1/chat", json={"query": "hi"}, headers={"x-forwarded-for": "2.2.2.2"}
        )

    assert response.status_code == 200
