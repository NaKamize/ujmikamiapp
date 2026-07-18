import os
import sys
from typing import List, Literal, TypedDict

import chromadb
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langgraph.graph import END, StateGraph

CHROMA_HOST = os.environ.get("CHROMA_HOST", "chroma-db")
CHROMA_PORT = int(os.environ.get("CHROMA_PORT", "8000"))
COLLECTION_NAME = "portfolio_projects"
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
OLLAMA_MODEL = "qwen2.5-coder:7b"

Intent = Literal["project", "academic", "both"]


class AgentState(TypedDict):
    question: str
    intent: Intent
    context: List[str]
    response: str


_llm = ChatOllama(base_url=OLLAMA_BASE_URL, model=OLLAMA_MODEL, temperature=0)
_embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL, model_kwargs={"device": "cpu"})
_chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)

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


def classify_intent(state: AgentState) -> AgentState:
    prompt = INTENT_PROMPT.format(question=state["question"])
    reply = _llm.invoke(prompt).content.strip().lower()

    if "both" in reply:
        intent: Intent = "both"
    elif "academic" in reply:
        intent = "academic"
    elif "project" in reply:
        intent = "project"
    else:
        intent = "both"

    return {**state, "intent": intent}


def retrieve_context(state: AgentState) -> AgentState:
    collection = _chroma_client.get_or_create_collection(COLLECTION_NAME)
    query_vector = _embeddings.embed_query(state["question"])

    # "both"-tagged chunks (e.g. the CV) span both categories, so they should
    # surface under either specific intent, not just an exact category match.
    where = {"category": {"$in": [state["intent"], "both"]}} if state["intent"] != "both" else None

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=5,
        where=where,
    )
    documents = results.get("documents") or [[]]
    return {**state, "context": documents[0]}


def synthesize_response(state: AgentState) -> AgentState:
    context_block = (
        "\n\n---\n\n".join(state["context"])
        if state["context"]
        else "No matching context was found for this intent."
    )
    prompt = SYNTHESIS_PROMPT.format(question=state["question"], context=context_block)
    reply = _llm.invoke(prompt).content
    return {**state, "response": reply}


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("classify_intent", classify_intent)
    graph.add_node("retrieve_context", retrieve_context)
    graph.add_node("synthesize_response", synthesize_response)

    graph.set_entry_point("classify_intent")
    graph.add_edge("classify_intent", "retrieve_context")
    graph.add_edge("retrieve_context", "synthesize_response")
    graph.add_edge("synthesize_response", END)

    return graph.compile()


graph = build_graph()


def run_agent(question: str) -> AgentState:
    return graph.invoke({"question": question, "intent": "both", "context": [], "response": ""})


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "What is Jozef's background in PySpark and AI?"
    result = run_agent(question)
    print(f"intent: {result['intent']}")
    print(f"context chunks: {len(result['context'])}")
    print("---")
    print(result["response"])
