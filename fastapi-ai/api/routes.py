import logging
from collections import defaultdict, deque
from collections.abc import AsyncIterator

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from agents.graph import graph
from agents.state import initial_state
from api.rate_limit import chat_rate_limiter
from api.schemas import ChatRequest, ChromaHealthResponse, HealthResponse
from services.chroma_service import ChromaServiceError, chroma_service

logger = logging.getLogger(__name__)

router = APIRouter()
RECENT_QUESTIONS_BY_CLIENT: dict[str, deque[str]] = defaultdict(lambda: deque(maxlen=5))


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/chroma/health", response_model=ChromaHealthResponse)
async def chroma_health() -> ChromaHealthResponse:
    try:
        heartbeat = await chroma_service.heartbeat()
    except ChromaServiceError as exc:
        logger.error("chroma_health: %s", exc)
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return ChromaHealthResponse(heartbeat=heartbeat)


async def _stream_answer_tokens(question: str, client_id: str | None = None) -> AsyncIterator[str]:
    history = list(RECENT_QUESTIONS_BY_CLIENT.get(client_id or "default", ())) if client_id else []
    state = initial_state(question, conversation_context=history)
    try:
        async for message, metadata in graph.astream(state, stream_mode="messages"):
            if metadata.get("langgraph_node") != "synthesize_response":
                continue
            if message.content:
                yield message.content
    finally:
        if client_id:
            history_list = RECENT_QUESTIONS_BY_CLIENT[client_id]
            history_list.append(question)
            while len(history_list) > 5:
                history_list.popleft()


@router.post("/api/v1/chat", dependencies=[Depends(chat_rate_limiter)])
async def chat(request: ChatRequest) -> StreamingResponse:
    logger.info("chat: received question=%r", request.query)
    client_id = request.headers.get("x-client-id") if hasattr(request, "headers") else None
    return StreamingResponse(_stream_answer_tokens(request.query, client_id), media_type="text/plain")
