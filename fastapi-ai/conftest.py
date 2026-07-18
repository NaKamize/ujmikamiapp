"""
Patches the heavy/network-dependent clients (HF embeddings model download,
Ollama, Chroma HTTP handshake) before agent.py/main.py are ever imported, so
`pytest` never touches the network or loads a real ML model. Individual tests
monkeypatch these fakes further to control return values.
"""
import chromadb
import langchain_huggingface
import langchain_ollama


class _FakeEmbeddings:
    def __init__(self, *args, **kwargs):
        pass

    def embed_query(self, text):
        raise RuntimeError("HuggingFaceEmbeddings.embed_query must be mocked per-test")

    def embed_documents(self, texts):
        raise RuntimeError("HuggingFaceEmbeddings.embed_documents must be mocked per-test")


class _FakeChatOllama:
    def __init__(self, *args, **kwargs):
        pass

    def invoke(self, *args, **kwargs):
        raise RuntimeError("ChatOllama.invoke must be mocked per-test")

    def astream(self, *args, **kwargs):
        raise RuntimeError("ChatOllama.astream must be mocked per-test")


class _FakeHttpClient:
    def __init__(self, *args, **kwargs):
        pass

    def get_or_create_collection(self, name):
        raise RuntimeError("chromadb.HttpClient must be mocked per-test")

    def heartbeat(self):
        raise RuntimeError("chromadb.HttpClient must be mocked per-test")


langchain_huggingface.HuggingFaceEmbeddings = _FakeEmbeddings
langchain_ollama.ChatOllama = _FakeChatOllama
chromadb.HttpClient = _FakeHttpClient
