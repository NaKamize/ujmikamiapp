import asyncio
import logging
import uuid
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.logging import configure_logging
from config.settings import settings
from services.chroma_service import chroma_service
from services.embedding_service import embedding_service

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent / "data"

CATEGORY_OVERRIDES = {
    "cv.md": "both",
}


def load_documents():
    loader = DirectoryLoader(str(DATA_DIR), glob="**/*.md", loader_cls=TextLoader)
    return loader.load()


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(documents)
    for chunk in chunks:
        filename = Path(chunk.metadata.get("source", "")).name
        chunk.metadata["category"] = CATEGORY_OVERRIDES.get(filename, "project")
    return chunks


async def run_ingest() -> None:
    """Embed data/*.md and (re)seed the Chroma collection."""
    documents = load_documents()
    logger.info("Loaded %d document(s) from %s", len(documents), DATA_DIR)

    chunks = split_documents(documents)
    logger.info("Split into %d chunk(s)", len(chunks))

    vectors = await embedding_service.embed_documents([chunk.page_content for chunk in chunks])

    await chroma_service.reseed_collection(
        collection_name=settings.chroma_collection_name,
        ids=[str(uuid.uuid4()) for _ in chunks],
        documents=[chunk.page_content for chunk in chunks],
        embeddings=vectors,
        metadatas=[chunk.metadata for chunk in chunks],
    )
    logger.info("Seeded %d chunk(s) into Chroma collection '%s'", len(chunks), settings.chroma_collection_name)


if __name__ == "__main__":
    configure_logging()
    asyncio.run(run_ingest())
