from unittest.mock import AsyncMock, MagicMock, patch

import langchain_ollama
import langchain_openai
import pytest

from services.chroma_service import ChromaService, ChromaServiceError
from services.embedding_service import EmbeddingService, EmbeddingServiceError
from services.llm_service import LLMService, LLMServiceError


async def test_chroma_service_query_wraps_connection_errors():
    service = ChromaService()

    with patch("services.chroma_service.chromadb.AsyncHttpClient", side_effect=ConnectionError("refused")):
        with pytest.raises(ChromaServiceError):
            await service.query("some_collection", [0.1, 0.2])


async def test_chroma_service_query_returns_documents():
    service = ChromaService()

    fake_collection = AsyncMock()
    fake_collection.query.return_value = {"documents": [["a", "b"]]}
    fake_client = AsyncMock()
    fake_client.get_or_create_collection.return_value = fake_collection
    service._client = fake_client  # simulate an already-connected client

    result = await service.query("some_collection", [0.1, 0.2])

    assert result == ["a", "b"]


async def test_llm_service_invoke_wraps_errors():
    service = LLMService()
    service._llm = AsyncMock()
    service._llm.ainvoke.side_effect = ConnectionError("refused")

    with pytest.raises(LLMServiceError):
        await service.invoke("hello")


async def test_llm_service_invoke_returns_content():
    service = LLMService()
    fake_message = type("Msg", (), {"content": "hi there"})()
    service._llm = AsyncMock()
    service._llm.ainvoke.return_value = fake_message

    result = await service.invoke("hello")

    assert result == "hi there"


async def test_embedding_service_wraps_errors():
    service = EmbeddingService()
    service._embeddings = AsyncMock()
    service._embeddings.aembed_query.side_effect = RuntimeError("model not loaded")

    with pytest.raises(EmbeddingServiceError):
        await service.embed_query("hello")


def test_llm_service_defaults_to_ollama():
    service = LLMService()

    assert isinstance(service._llm, langchain_ollama.ChatOllama)


def test_llm_service_uses_azure_openai_when_selected():
    service = LLMService(provider="azure_openai")

    assert isinstance(service._llm, langchain_openai.AzureChatOpenAI)


def test_llm_service_rejects_unknown_provider():
    with pytest.raises(ValueError):
        LLMService(provider="bedrock")


async def test_chroma_service_embedded_mode_uses_sync_client():
    service = ChromaService(mode="embedded")

    fake_collection = MagicMock()
    fake_collection.query.return_value = {"documents": [["chunk"]]}
    fake_client = MagicMock()
    fake_client.get_or_create_collection.return_value = fake_collection
    service._client = fake_client

    result = await service.query("some_collection", [0.1])

    assert result == ["chunk"]
