from typing import List, Literal, Optional, TypedDict

Intent = Literal["project", "academic", "both"]


class AgentState(TypedDict):
    question: str
    intent: Intent
    context: List[str]
    response: str
    error: Optional[str]


def initial_state(question: str) -> AgentState:
    return AgentState(question=question, intent="both", context=[], response="", error=None)
