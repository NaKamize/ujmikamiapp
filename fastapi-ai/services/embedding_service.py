import logging
from typing import Optional

from langchain_huggingface import HuggingFaceEmbeddings

from config.settings import settings

logger = logging.getLogger(__name__)


class EmbeddingServiceError(Exception):
    """Raised when embedding generation fails."""


class EmbeddingService:
    """Async wrapper around HuggingFaceEmbeddings.

    The underlying computation is CPU-bound (no real network I/O), but LangChain's
    aembed_* methods still offload it to a thread pool so the event loop isn't blocked
    while the model runs.
    """

    def __init__(self, model_name: Optional[str] = None) -> None:
        self._model_name = model_name or settings.embedding_model
        self._embeddings = HuggingFaceEmbeddings(
            model_name=self._model_name,
            model_kwargs={"device": "cpu"},
        )

    async def embed_query(self, text: str) -> list[float]:
        try:
            return await self._embeddings.aembed_query(text)
        except Exception as exc:
            logger.exception("Failed to embed query text")
            raise EmbeddingServiceError("Failed to embed query text") from exc

    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        try:
            return await self._embeddings.aembed_documents(texts)
        except Exception as exc:
            logger.exception("Failed to embed %d document chunk(s)", len(texts))
            raise EmbeddingServiceError("Failed to embed document chunks") from exc


embedding_service = EmbeddingService()
