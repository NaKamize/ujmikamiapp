import logging
from collections.abc import AsyncIterator

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from agents.graph import graph
from agents.state import initial_state
from api.schemas import ChatRequest, ChromaHealthResponse, HealthResponse
from services.chroma_service import ChromaServiceError, chroma_service

logger = logging.getLogger(__name__)

router = APIRouter()


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


async def _stream_answer_tokens(question: str) -> AsyncIterator[str]:
    state = initial_state(question)
    try:
        async for message, metadata in graph.astream(state, stream_mode="messages"):
            if metadata.get("langgraph_node") != "synthesize_response":
                continue
            if message.content:
                yield message.content
    except Exception as exc:
        # Final safety net: individual nodes already catch their own service errors and
        # degrade gracefully, so reaching here means something genuinely unexpected happened.
        logger.exception("chat: unhandled error while streaming agent response")
        yield f"\n\n[agent error: {exc}]"


@router.post("/api/v1/chat")
async def chat(request: ChatRequest) -> StreamingResponse:
    logger.info("chat: received question=%r", request.query)
    return StreamingResponse(_stream_answer_tokens(request.query), media_type="text/plain")
