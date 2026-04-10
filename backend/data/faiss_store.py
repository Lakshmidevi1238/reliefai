"""
ReliefLink AI — FAISS Vector Store Wrapper
Manages a global FAISS instance for crisis embeddings used by the RAG pipeline.
"""
import logging
from typing import List, Optional

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

from backend.config import OPENAI_API_KEY, OPENAI_EMBEDDING_MODEL

logger = logging.getLogger(__name__)

# ── Module-level singletons ──────────────────────────────────
_faiss_store: Optional[FAISS] = None
_embeddings: Optional[OpenAIEmbeddings] = None


def _get_embeddings() -> Optional[OpenAIEmbeddings]:
    """Lazy-init the embeddings model."""
    global _embeddings
    if not OPENAI_API_KEY:
        return None
    if _embeddings is None:
        _embeddings = OpenAIEmbeddings(
            model=OPENAI_EMBEDDING_MODEL,
            openai_api_key=OPENAI_API_KEY,
        )
    return _embeddings


def initialize_store(documents: List[Document]) -> bool:
    """Create a fresh FAISS store from a list of Documents."""
    global _faiss_store
    emb = _get_embeddings()
    if emb is None:
        logger.warning("FAISS init skipped — no OpenAI API key.")
        return False
    try:
        _faiss_store = FAISS.from_documents(documents, emb)
        logger.info("FAISS store initialised with %d documents.", len(documents))
        return True
    except Exception as exc:
        logger.error("FAISS initialisation error: %s", exc)
        return False


def add_documents(documents: List[Document]) -> bool:
    """Add documents to an existing store (or create one if none exists)."""
    global _faiss_store
    emb = _get_embeddings()
    if emb is None:
        return False
    try:
        if _faiss_store is None:
            _faiss_store = FAISS.from_documents(documents, emb)
        else:
            _faiss_store.add_documents(documents)
        logger.info("Added %d documents to FAISS.", len(documents))
        return True
    except Exception as exc:
        logger.error("FAISS add_documents error: %s", exc)
        return False


def similarity_search(query: str, k: int = 4) -> List[Document]:
    """Return top-k similar documents for a query string."""
    if _faiss_store is None:
        return []
    try:
        return _faiss_store.similarity_search(query, k=k)
    except Exception as exc:
        logger.error("FAISS similarity_search error: %s", exc)
        return []


def get_retriever(k: int = 4):
    """Return a LangChain retriever backed by the FAISS store."""
    if _faiss_store is None:
        return None
    return _faiss_store.as_retriever(search_kwargs={"k": k})


def is_initialized() -> bool:
    """True if the FAISS store has been populated."""
    return _faiss_store is not None


def document_count() -> int:
    """Return the number of indexed documents (approximate)."""
    if _faiss_store is None:
        return 0
    try:
        return _faiss_store.index.ntotal
    except Exception:
        return 0
