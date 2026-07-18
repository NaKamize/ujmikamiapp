from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, description="The visitor's question for the AI assistant.")


class HealthResponse(BaseModel):
    status: str


class ChromaHealthResponse(BaseModel):
    heartbeat: int
