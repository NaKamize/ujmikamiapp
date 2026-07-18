import logging
from typing import Any, Optional

import chromadb
from chromadb.api.async_api import AsyncClientAPI

from config.settings import settings

logger = logging.getLogger(__name__)


class ChromaServiceError(Exception):
    """Raised when the Chroma vector database is unreachable or returns an error."""


class ChromaService:
    """Async wrapper around chromadb's AsyncHttpClient.

    Lazily connects on first use (creating the client requires an event loop, so it
    can't happen at import/module-load time) and caches the connection for reuse.
    """

    def __init__(self, host: Optional[str] = None, port: Optional[int] = None) -> None:
        self._host = host or settings.chroma_host
        self._port = port or settings.chroma_port
        self._client: Optional[AsyncClientAPI] = None

    async def _get_client(self) -> AsyncClientAPI:
        if self._client is None:
            try:
                self._client = await chromadb.AsyncHttpClient(host=self._host, port=self._port)
            except Exception as exc:
                logger.exception("Failed to connect to Chroma at %s:%s", self._host, self._port)
                raise ChromaServiceError(f"Could not connect to Chroma at {self._host}:{self._port}") from exc
        return self._client

    async def heartbeat(self) -> int:
        client = await self._get_client()
        try:
            return await client.heartbeat()
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
            collection = await client.get_or_create_collection(collection_name)
            results = await collection.query(
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
        """Delete (if present) and recreate a collection with fresh chunks. Used by ingest.py."""
        client = await self._get_client()
        try:
            await client.delete_collection(collection_name)
        except Exception:
            logger.info("Collection '%s' did not exist yet, nothing to delete", collection_name)

        try:
            collection = await client.get_or_create_collection(collection_name)
            await collection.add(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)
        except Exception as exc:
            logger.exception("Failed to reseed Chroma collection '%s'", collection_name)
            raise ChromaServiceError(f"Failed to reseed Chroma collection '{collection_name}'") from exc


chroma_service = ChromaService()
