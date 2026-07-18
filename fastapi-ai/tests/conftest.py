"""
Patches the heavy/network-dependent clients (HF embeddings model download, Ollama,
Chroma's async HTTP handshake) before services/*.py are ever imported, so `pytest`
never touches the network or loads a real ML model. Individual tests monkeypatch the
services module-level singletons (e.g. agents.nodes.llm_service) further to control
return values and simulate failures.
"""
import chromadb
import langchain_huggingface
import langchain_ollama


class _FakeEmbeddings:
    def __init__(self, *args, **kwargs):
        pass

    async def aembed_query(self, text):
        raise RuntimeError("HuggingFaceEmbeddings.aembed_query must be mocked per-test")

    async def aembed_documents(self, texts):
        raise RuntimeError("HuggingFaceEmbeddings.aembed_documents must be mocked per-test")


class _FakeChatOllama:
    def __init__(self, *args, **kwargs):
        pass

    async def ainvoke(self, *args, **kwargs):
        raise RuntimeError("ChatOllama.ainvoke must be mocked per-test")

    async def astream(self, *args, **kwargs):
        raise RuntimeError("ChatOllama.astream must be mocked per-test")
        yield  # pragma: no cover - unreachable, keeps this an async generator for typing


class _FakeAsyncCollection:
    async def query(self, *args, **kwargs):
        raise RuntimeError("Chroma collection.query must be mocked per-test")

    async def add(self, *args, **kwargs):
        raise RuntimeError("Chroma collection.add must be mocked per-test")


class _FakeAsyncClient:
    async def get_or_create_collection(self, name):
        raise RuntimeError("chromadb AsyncHttpClient must be mocked per-test")

    async def delete_collection(self, name):
        raise RuntimeError("chromadb AsyncHttpClient must be mocked per-test")

    async def heartbeat(self):
        raise RuntimeError("chromadb AsyncHttpClient must be mocked per-test")


async def _fake_async_http_client(*args, **kwargs):
    return _FakeAsyncClient()


langchain_huggingface.HuggingFaceEmbeddings = _FakeEmbeddings
langchain_ollama.ChatOllama = _FakeChatOllama
chromadb.AsyncHttpClient = _fake_async_http_client
