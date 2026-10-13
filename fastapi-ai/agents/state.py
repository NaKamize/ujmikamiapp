from typing import List, Literal, Optional, TypedDict

Intent = Literal["project", "academic", "career", "both"]


class AgentState(TypedDict):
    question: str
    intent: Intent
    context: List[str]
    response: str
    error: Optional[str]
    conversation_context: List[str]


def initial_state(question: str, conversation_context: Optional[List[str]] = None) -> AgentState:
    return AgentState(
        question=question,
        intent="both",
        context=[],
        response="",
        error=None,
        conversation_context=list(conversation_context or []),
    )
