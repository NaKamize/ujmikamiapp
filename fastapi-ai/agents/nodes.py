import logging
import time

from agents.state import AgentState, Intent
from config.settings import settings
from services.chroma_service import ChromaServiceError, chroma_service
from services.embedding_service import EmbeddingServiceError, embedding_service
from services.llm_service import LLMServiceError, llm_service

logger = logging.getLogger(__name__)

INTENT_PROMPT = """You are the intent classifier for a portfolio website's AI assistant.
Decide which kind of information the visitor's question is asking about:

- "project": hands-on software engineering / machine learning projects, their
  implementation, tech stack, or results.
- "academic": academic research, publications, or theoretical/thesis work.
- "both": the question clearly spans both categories.

Respond with exactly one word: project, academic, or both. No punctuation, no explanation.

Question: {question}
Answer:"""

SYNTHESIS_PROMPT = """You are the AI assistant on Jozef Makis's portfolio website.
Answer the visitor's question using ONLY the context below. If the context does not
cover part of the question, say so honestly instead of inventing details.

Format the answer in clean markdown: a short direct answer first, then supporting
detail as headers/bullet points where it helps readability.

Question: {question}

Context:
{context}

Answer:"""


async def classify_intent(state: AgentState) -> AgentState:
    start = time.perf_counter()
    prompt = INTENT_PROMPT.format(question=state["question"])

    try:
        reply = (await llm_service.invoke(prompt)).strip().lower()
    except LLMServiceError as exc:
        logger.warning("classify_intent: LLM unavailable, defaulting to intent='both': %s", exc)
        return {**state, "intent": "both", "error": str(exc)}

    if "both" in reply:
        intent: Intent = "both"
    elif "academic" in reply:
        intent = "academic"
    elif "project" in reply:
        intent = "project"
    else:
        intent = "both"

    elapsed_ms = (time.perf_counter() - start) * 1000
    logger.info("classify_intent: question=%r -> intent=%r (%.0fms)", state["question"], intent, elapsed_ms)
    return {**state, "intent": intent}


async def retrieve_context(state: AgentState) -> AgentState:
    start = time.perf_counter()
    # "both"-tagged chunks (e.g. the CV) span both categories, so they should
    # surface under either specific intent, not just an exact category match.
    where = {"category": {"$in": [state["intent"], "both"]}} if state["intent"] != "both" else None

    try:
        query_vector = await embedding_service.embed_query(state["question"])
        documents = await chroma_service.query(
            collection_name=settings.chroma_collection_name,
            query_embedding=query_vector,
            n_results=5,
            where=where,
        )
    except (EmbeddingServiceError, ChromaServiceError) as exc:
        logger.warning("retrieve_context: retrieval unavailable, continuing with no context: %s", exc)
        return {**state, "context": [], "error": str(exc)}

    elapsed_ms = (time.perf_counter() - start) * 1000
    logger.info(
        "retrieve_context: intent=%r -> %d chunk(s) retrieved (%.0fms)",
        state["intent"],
        len(documents),
        elapsed_ms,
    )
    return {**state, "context": documents}


async def synthesize_response(state: AgentState) -> AgentState:
    start = time.perf_counter()

    if state["context"]:
        context_block = "\n\n---\n\n".join(state["context"])
    elif state.get("error"):
        context_block = "No context could be retrieved due to a temporary service issue."
    else:
        context_block = "No matching context was found for this intent."

    prompt = SYNTHESIS_PROMPT.format(question=state["question"], context=context_block)

    try:
        reply = await llm_service.invoke(prompt)
    except LLMServiceError as exc:
        logger.error("synthesize_response: LLM unavailable, returning fallback message: %s", exc)
        return {
            **state,
            "response": "Sorry, the AI assistant is temporarily unavailable. Please try again shortly.",
            "error": str(exc),
        }

    elapsed_ms = (time.perf_counter() - start) * 1000
    logger.info("synthesize_response: generated %d char response (%.0fms)", len(reply), elapsed_ms)
    return {**state, "response": reply}
