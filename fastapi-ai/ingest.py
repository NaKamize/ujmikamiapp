import os
import uuid

import chromadb
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
CHROMA_HOST = os.environ.get("CHROMA_HOST", "chroma-db")
CHROMA_PORT = int(os.environ.get("CHROMA_PORT", "8000"))
COLLECTION_NAME = "portfolio_projects"
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

# Most docs in ./data are hands-on project write-ups; a few (like the CV) span
# both project and academic content and are tagged "both" so agent.py's
# intent-filtered retrieval surfaces them for either intent.
CATEGORY_OVERRIDES = {
    "cv.md": "both",
}


def load_documents():
    loader = DirectoryLoader(DATA_DIR, glob="**/*.md", loader_cls=TextLoader)
    return loader.load()


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)
    for chunk in chunks:
        filename = os.path.basename(chunk.metadata.get("source", ""))
        chunk.metadata["category"] = CATEGORY_OVERRIDES.get(filename, "project")
    return chunks


def main():
    documents = load_documents()
    print(f"Loaded {len(documents)} document(s) from {DATA_DIR}")

    chunks = split_documents(documents)
    print(f"Split into {len(chunks)} chunk(s)")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
    )
    vectors = embeddings.embed_documents([chunk.page_content for chunk in chunks])

    client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    client.delete_collection(COLLECTION_NAME)
    collection = client.get_or_create_collection(COLLECTION_NAME)

    collection.add(
        ids=[str(uuid.uuid4()) for _ in chunks],
        documents=[chunk.page_content for chunk in chunks],
        embeddings=vectors,
        metadatas=[chunk.metadata for chunk in chunks],
    )
    print(f"Seeded {len(chunks)} chunk(s) into Chroma collection '{COLLECTION_NAME}'")


if __name__ == "__main__":
    main()
