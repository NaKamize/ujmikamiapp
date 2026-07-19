import inspect
import logging
from typing import Any, Optional

import chromadb

from config.settings import settings

logger = logging.getLogger(__name__)


class ChromaServiceError(Exception):
    """Raised when the Chroma vector database is unreachable or returns an error."""


class ChromaService:
    """Async wrapper around a Chroma client.

    Two modes (settings.chroma_mode):
    - "http": chromadb.AsyncHttpClient against a separate Chroma server (local dev's
      chroma-db container).
    - "embedded": chromadb.EphemeralClient, in-process and in-memory; the app seeds
      it at startup (see main.py). Used on Azure, where a standalone Chroma server
      can't persist to Azure Files (SQLite WAL is incompatible with SMB).
    """

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        ssl: Optional[bool] = None,
        mode: Optional[str] = None,
    ) -> None:
        self._mode = mode or settings.chroma_mode
        self._host = host or settings.chroma_host
        self._port = port or settings.chroma_port
        self._ssl = settings.chroma_ssl if ssl is None else ssl
        self._client: Optional[Any] = None

    @staticmethod
    async def _call(func, *args, **kwargs):
        result = func(*args, **kwargs)
        if inspect.isawaitable(result):
            return await result
        return result

    async def _get_client(self) -> Any:
        if self._client is None:
            try:
                if self._mode == "embedded":
                    self._client = chromadb.EphemeralClient()
                else:
                    self._client = await chromadb.AsyncHttpClient(
                        host=self._host, port=self._port, ssl=self._ssl
                    )
            except Exception as exc:
                logger.exception("Failed to connect to Chroma (%s mode)", self._mode)
                raise ChromaServiceError(f"Could not connect to Chroma ({self._mode} mode)") from exc
        return self._client

    async def heartbeat(self) -> int:
        client = await self._get_client()
        try:
            return await self._call(client.heartbeat)
        except Exception as exc:
            logger.exception("Chroma heartbeat failed")
            raise ChromaServiceError("Chroma heartbeat failed") from exc

    async def query(
        self,
        collection_name: str,
        query_embedding: list[float],
        n_results: int = 5,
        where: Optional[dict[str, Any]] = None,
    ) -> list[str]:
        client = await self._get_client()
        try:
            collection = await self._call(client.get_or_create_collection, collection_name)
            results = await self._call(
                collection.query,
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where,
            )
        except Exception as exc:
            logger.exception("Chroma query failed for collection '%s'", collection_name)
            raise ChromaServiceError(f"Chroma query failed for collection '{collection_name}'") from exc

        documents = results.get("documents") or [[]]
        return documents[0]

    async def reseed_collection(
        self,
        collection_name: str,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict[str, Any]],
    ) -> None:
        client = await self._get_client()
        try:
            await self._call(client.delete_collection, collection_name)
        except Exception:
            logger.info("Collection '%s' did not exist yet, nothing to delete", collection_name)

        try:
            collection = await self._call(client.get_or_create_collection, collection_name)
            await self._call(
                collection.add,
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
            )
        except Exception as exc:
            logger.exception("Failed to reseed Chroma collection '%s'", collection_name)
            raise ChromaServiceError(f"Failed to reseed Chroma collection '{collection_name}'") from exc


chroma_service = ChromaService()
