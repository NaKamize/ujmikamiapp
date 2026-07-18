from agents.graph import build_graph


def test_build_graph_has_expected_nodes():
    graph = build_graph()
    node_names = set(graph.get_graph().nodes.keys())
    assert {"classify_intent", "retrieve_context", "synthesize_response"} <= node_names
