from pydantic import BaseModel, Field

from config.settings import settings


class ChatRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        max_length=settings.chat_max_query_length,
        description="The visitor's question for the AI assistant.",
    )


class HealthResponse(BaseModel):
    status: str


class ChromaHealthResponse(BaseModel):
    heartbeat: int
