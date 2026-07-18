from unittest.mock import MagicMock

import agent


def test_classify_intent_project():
    fake_llm = MagicMock()
    fake_llm.invoke.return_value = MagicMock(content="project")
    agent._llm = fake_llm

    state = {"question": "Tell me about the disaster tweets project", "intent": "both", "context": [], "response": ""}
    result = agent.classify_intent(state)

    assert result["intent"] == "project"


def test_classify_intent_academic():
    fake_llm = MagicMock()
    fake_llm.invoke.return_value = MagicMock(content="Academic")
    agent._llm = fake_llm

    state = {"question": "Tell me about the thesis", "intent": "both", "context": [], "response": ""}
    result = agent.classify_intent(state)

    assert result["intent"] == "academic"


def test_classify_intent_falls_back_to_both_on_unexpected_reply():
    fake_llm = MagicMock()
    fake_llm.invoke.return_value = MagicMock(content="something unexpected")
    agent._llm = fake_llm

    state = {"question": "hi", "intent": "both", "context": [], "response": ""}
    result = agent.classify_intent(state)

    assert result["intent"] == "both"


def test_retrieve_context_filters_by_intent_including_both_tagged_chunks():
    fake_collection = MagicMock()
    fake_collection.query.return_value = {"documents": [["chunk one", "chunk two"]]}
    fake_client = MagicMock()
    fake_client.get_or_create_collection.return_value = fake_collection
    agent._chroma_client = fake_client
    agent._embeddings = MagicMock(embed_query=MagicMock(return_value=[0.1, 0.2, 0.3]))

    state = {"question": "pyspark?", "intent": "project", "context": [], "response": ""}
    result = agent.retrieve_context(state)

    assert result["context"] == ["chunk one", "chunk two"]
    _, kwargs = fake_collection.query.call_args
    assert kwargs["where"] == {"category": {"$in": ["project", "both"]}}


def test_retrieve_context_no_filter_when_intent_is_both():
    fake_collection = MagicMock()
    fake_collection.query.return_value = {"documents": [[]]}
    fake_client = MagicMock()
    fake_client.get_or_create_collection.return_value = fake_collection
    agent._chroma_client = fake_client
    agent._embeddings = MagicMock(embed_query=MagicMock(return_value=[0.0]))

    state = {"question": "anything", "intent": "both", "context": [], "response": ""}
    agent.retrieve_context(state)

    _, kwargs = fake_collection.query.call_args
    assert kwargs["where"] is None


def test_synthesize_response_uses_context():
    fake_llm = MagicMock()
    fake_llm.invoke.return_value = MagicMock(content="Here is the answer.")
    agent._llm = fake_llm

    state = {"question": "q", "intent": "both", "context": ["fact one"], "response": ""}
    result = agent.synthesize_response(state)

    assert result["response"] == "Here is the answer."


def test_synthesize_response_handles_no_context():
    fake_llm = MagicMock()
    fake_llm.invoke.return_value = MagicMock(content="I don't have that information.")
    agent._llm = fake_llm

    state = {"question": "q", "intent": "both", "context": [], "response": ""}
    agent.synthesize_response(state)

    prompt_arg = fake_llm.invoke.call_args[0][0]
    assert "No matching context was found" in prompt_arg


def test_build_graph_has_expected_nodes():
    graph = agent.build_graph()
    node_names = set(graph.get_graph().nodes.keys())
    assert {"classify_intent", "retrieve_context", "synthesize_response"} <= node_names
