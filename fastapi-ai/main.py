import os
from collections.abc import AsyncIterator

import chromadb
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from agent import graph

app = FastAPI(title="ujmikamiapp AI service")

CHROMA_HOST = os.environ.get("CHROMA_HOST", "chroma-db")
CHROMA_PORT = int(os.environ.get("CHROMA_PORT", "8000"))

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("CORS_ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOWED_ORIGINS,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)


class ChatRequest(BaseModel):
    query: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/chroma/health")
def chroma_health():
    client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    return {"heartbeat": client.heartbeat()}


async def stream_agent_response(question: str) -> AsyncIterator[str]:
    inputs = {"question": question, "intent": "both", "context": [], "response": ""}
    try:
        async for message, metadata in graph.astream(inputs, stream_mode="messages"):
            if metadata.get("langgraph_node") != "synthesize_response":
                continue
            if message.content:
                yield message.content
    except Exception as exc:
        yield f"\n\n[agent error: {exc}]"


@app.post("/api/v1/chat")
async def chat(request: ChatRequest):
    return StreamingResponse(stream_agent_response(request.query), media_type="text/plain")
