import logging
from typing import AsyncIterator, Optional

from langchain_ollama import ChatOllama

from config.settings import settings

logger = logging.getLogger(__name__)


class LLMServiceError(Exception):
    """Raised when the LLM (Ollama) is unreachable or returns an error."""


class LLMService:
    """Async wrapper around ChatOllama, used for both one-shot calls and token streaming."""

    def __init__(self, base_url: Optional[str] = None, model: Optional[str] = None) -> None:
        self._llm = ChatOllama(
            base_url=base_url or settings.ollama_base_url,
            model=model or settings.ollama_model,
            temperature=0,
        )

    async def invoke(self, prompt: str) -> str:
        try:
            result = await self._llm.ainvoke(prompt)
        except Exception as exc:
            logger.exception("LLM invoke failed")
            raise LLMServiceError("LLM invoke failed") from exc
        return result.content

    async def stream(self, prompt: str) -> AsyncIterator[str]:
        try:
            async for chunk in self._llm.astream(prompt):
                if chunk.content:
                    yield chunk.content
        except Exception as exc:
            logger.exception("LLM stream failed")
            raise LLMServiceError("LLM stream failed") from exc


llm_service = LLMService()
