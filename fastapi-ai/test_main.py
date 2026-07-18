import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

import main


class _FakeMessage:
    def __init__(self, content):
        self.content = content


async def _fake_astream(inputs, stream_mode=None):
    for node, content in [
        ("classify_intent", "project"),
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
    monkeypatch.setattr(main, "graph", _FakeGraph())


def test_health():
    client = TestClient(main.app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chroma_health(monkeypatch):
    class _FakeClient:
        def __init__(self, *args, **kwargs):
            pass

        def heartbeat(self):
            return 12345

    monkeypatch.setattr(main.chromadb, "HttpClient", _FakeClient)

    client = TestClient(main.app)
    response = client.get("/chroma/health")
    assert response.status_code == 200
    assert response.json() == {"heartbeat": 12345}


async def test_chat_streams_only_synthesize_response_tokens():
    transport = ASGITransport(app=main.app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/v1/chat", json={"query": "What is Jozef's background?"})

    assert response.status_code == 200
    assert response.text == "Hello world"


async def test_chat_streams_error_message_on_agent_failure(monkeypatch):
    monkeypatch.setattr(main, "graph", _FakeFailingGraph())

    transport = ASGITransport(app=main.app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/v1/chat", json={"query": "anything"})

    assert response.status_code == 200
    assert "agent error" in response.text


def test_chat_rejects_missing_query_field():
    client = TestClient(main.app)
    response = client.post("/api/v1/chat", json={})
    assert response.status_code == 422
