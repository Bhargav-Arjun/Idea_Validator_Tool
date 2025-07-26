# Retrieval logic placeholder 
# app/rag/retriever.py

from app.rag.vector_db import search_vector_db
from app.utils.logger import logger

RELEVANCE_THRESHOLD = 0.75
MIN_DOC_COUNT = 2

def retrieve_or_trigger_search(user_idea: str, embedding: list):
    """
    Try retrieving from vector DB first. If insufficient, return None so we trigger web search.
    """
    logger.info("🔍 Checking vector DB for existing idea matches...")

    matches = search_vector_db(embedding, top_k=5)
    if not matches or len(matches) < MIN_DOC_COUNT:
        logger.info("📉 Not enough relevant matches found — triggering real-time web search.")
        return None, "trigger_search"

    relevant_docs = [
        doc for doc in matches if doc["score"] >= RELEVANCE_THRESHOLD
    ]

    if len(relevant_docs) < MIN_DOC_COUNT:
        logger.info("📉 Matching docs below threshold — triggering search.")
        return None, "trigger_search"

    logger.info(f"✅ Retrieved {len(relevant_docs)} docs from Vector DB.")
    return relevant_docs, "vector_db"
