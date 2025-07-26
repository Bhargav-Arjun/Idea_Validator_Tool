# Store logic placeholder 
# app/rag/storer.py

from app.rag.vector_db import add_to_vector_db
from app.rag.embedder import get_embedding
from app.utils.logger import logger

def store_final_idea(cleaned_idea: str, scorecard: dict):
    """
    Embeds and stores the idea + scorecard into vector DB for future retrieval.
    """
    logger.info("📥 Storing final idea into vector DB.")

    embedding = get_embedding(cleaned_idea)

    metadata = {
        "scorecard": scorecard,
        "idea": cleaned_idea
    }

    add_to_vector_db(embedding, metadata)
    logger.info("✅ Stored into vector DB.")
