from unittest.mock import AsyncMock

import agents.nodes as nodes_module
from agents.state import initial_state
from services.chroma_service import ChromaServiceError
from services.llm_service import LLMServiceError


async def test_retrieve_context_queries_without_intent_filter(monkeypatch):
    state = initial_state("pyspark?")

    fake_embeddings = AsyncMock()
    fake_embeddings.embed_query.return_value = [0.1, 0.2, 0.3]
    monkeypatch.setattr(nodes_module, "embedding_service", fake_embeddings)

    fake_chroma = AsyncMock()
    fake_chroma.query.return_value = ["chunk one", "chunk two"]
    monkeypatch.setattr(nodes_module, "chroma_service", fake_chroma)

    result = await nodes_module.retrieve_context(state)

    assert result["context"] == ["chunk one", "chunk two"]
    _, kwargs = fake_chroma.query.call_args
    assert kwargs["where"] is None


async def test_retrieve_context_no_filter_for_arbitrary_query(monkeypatch):
    state = initial_state("anything")

    fake_embeddings = AsyncMock()
    fake_embeddings.embed_query.return_value = [0.0]
    monkeypatch.setattr(nodes_module, "embedding_service", fake_embeddings)

    fake_chroma = AsyncMock()
    fake_chroma.query.return_value = []
    monkeypatch.setattr(nodes_module, "chroma_service", fake_chroma)

    await nodes_module.retrieve_context(state)

    _, kwargs = fake_chroma.query.call_args
    assert kwargs["where"] is None


async def test_retrieve_context_degrades_gracefully_on_chroma_failure(monkeypatch):
    state = initial_state("anything")

    fake_embeddings = AsyncMock()
    fake_embeddings.embed_query.return_value = [0.0]
    monkeypatch.setattr(nodes_module, "embedding_service", fake_embeddings)

    fake_chroma = AsyncMock()
    fake_chroma.query.side_effect = ChromaServiceError("connection refused")
    monkeypatch.setattr(nodes_module, "chroma_service", fake_chroma)

    result = await nodes_module.retrieve_context(state)

    assert result["context"] == []
    assert result["error"] == "connection refused"


async def test_synthesize_response_uses_context(monkeypatch):
    state = initial_state("q")
    state["context"] = ["fact one"]

    fake_llm = AsyncMock()
    fake_llm.invoke.return_value = "Here is the answer."
    monkeypatch.setattr(nodes_module, "llm_service", fake_llm)

    result = await nodes_module.synthesize_response(state)

    assert result["response"] == "Here is the answer."


async def test_synthesize_response_handles_no_context(monkeypatch):
    state = initial_state("q")

    fake_llm = AsyncMock()
    fake_llm.invoke.return_value = "I don't have that information."
    monkeypatch.setattr(nodes_module, "llm_service", fake_llm)

    await nodes_module.synthesize_response(state)

    prompt_arg = fake_llm.invoke.call_args[0][0]
    assert "No matching context was found" in prompt_arg


async def test_synthesize_response_degrades_gracefully_on_llm_failure(monkeypatch):
    state = initial_state("q")

    fake_llm = AsyncMock()
    fake_llm.invoke.side_effect = LLMServiceError("connection refused")
    monkeypatch.setattr(nodes_module, "llm_service", fake_llm)

    result = await nodes_module.synthesize_response(state)

    assert "temporarily unavailable" in result["response"]
    assert result["error"] == "connection refused"
