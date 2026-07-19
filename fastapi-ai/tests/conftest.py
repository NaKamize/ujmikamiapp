import chromadb
import langchain_huggingface
import langchain_ollama
import langchain_openai


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
        yield


class _FakeAzureChatOpenAI:
    def __init__(self, *args, **kwargs):
        pass

    async def ainvoke(self, *args, **kwargs):
        raise RuntimeError("AzureChatOpenAI.ainvoke must be mocked per-test")

    async def astream(self, *args, **kwargs):
        raise RuntimeError("AzureChatOpenAI.astream must be mocked per-test")
        yield


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


class _FakeEphemeralClient:
    def __init__(self, *args, **kwargs):
        pass

    def get_or_create_collection(self, name):
        raise RuntimeError("chromadb EphemeralClient must be mocked per-test")

    def delete_collection(self, name):
        raise RuntimeError("chromadb EphemeralClient must be mocked per-test")

    def heartbeat(self):
        raise RuntimeError("chromadb EphemeralClient must be mocked per-test")


langchain_huggingface.HuggingFaceEmbeddings = _FakeEmbeddings
langchain_ollama.ChatOllama = _FakeChatOllama
langchain_openai.AzureChatOpenAI = _FakeAzureChatOpenAI
chromadb.AsyncHttpClient = _fake_async_http_client
chromadb.EphemeralClient = _FakeEphemeralClient
