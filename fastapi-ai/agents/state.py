from typing import List, Optional, TypedDict


class AgentState(TypedDict):
    question: str
    context: List[str]
    response: str
    error: Optional[str]
    conversation_context: List[str]


def initial_state(question: str, conversation_context: Optional[List[str]] = None) -> AgentState:
    return AgentState(
        question=question,
        context=[],
        response="",
        error=None,
        conversation_context=list(conversation_context or []),
    )
