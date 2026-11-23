import logging
from typing import AsyncIterator, Optional

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_ollama import ChatOllama
from langchain_openai import AzureChatOpenAI

from config.settings import settings

logger = logging.getLogger(__name__)


class LLMServiceError(Exception):
    """Raised when the configured LLM backend is unreachable or returns an error."""


def _build_llm(provider: str, base_url: Optional[str], model: Optional[str]) -> BaseChatModel:
    if provider == "azure_openai":
        return AzureChatOpenAI(
            azure_endpoint=settings.azure_openai_endpoint,
            api_key=settings.azure_openai_api_key,
            azure_deployment=model or settings.azure_openai_deployment,
            api_version=settings.azure_openai_api_version,
        )
    if provider == "ollama":
        return ChatOllama(
            base_url=base_url or settings.ollama_base_url,
            model=model or settings.ollama_model,
            reasoning=settings.reasoning,
            temperature=settings.temperature,
            top_p=settings.top_p,
            top_k=settings.top_k,
            repeat_penalty=settings.repeat_penalty,
        )
    raise ValueError(f"Unknown LLM_PROVIDER {provider!r}; expected 'ollama' or 'azure_openai'")


class LLMService:
    """Async wrapper around the configured chat model (ChatOllama locally,
    AzureChatOpenAI when deployed), used for both one-shot calls and token streaming."""

    def __init__(
        self,
        provider: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
    ) -> None:
        self._llm = _build_llm(provider or settings.llm_provider, base_url, model)

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
