from langgraph.graph import END, StateGraph

from agents.nodes import retrieve_context, synthesize_response
from agents.state import AgentState


def build_graph():
    graph_builder = StateGraph(AgentState)
    graph_builder.add_node("retrieve_context", retrieve_context)
    graph_builder.add_node("synthesize_response", synthesize_response)

    graph_builder.set_entry_point("retrieve_context")
    graph_builder.add_edge("retrieve_context", "synthesize_response")
    graph_builder.add_edge("synthesize_response", END)

    return graph_builder.compile()


graph = build_graph()
