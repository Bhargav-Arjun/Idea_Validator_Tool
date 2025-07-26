# app/agents/relevance_filter.py

from autogen import AssistantAgent
from typing import List, Dict
from app.rag.embedder import embed_text, embed_batch
from app.utils.similarity import rank_by_cosine_similarity


class RelevanceFilterAgent(AssistantAgent):
    def __init__(self, name="RelevanceFilterAgent", top_k: int = 3):
        super().__init__(name=name)
        self.top_k = top_k

    def run(self, user_idea: str, docs: List[Dict]) -> Dict:
        """
        Filters and ranks documents based on similarity to user idea.
        Returns top K relevant documents.
        """
        # 1️⃣ Embed idea
        idea_embedding = embed_text(user_idea)

        # 2️⃣ Extract doc texts
        doc_texts = [doc["content"] for doc in docs]

        # 3️⃣ Embed all docs
        doc_embeddings = embed_batch(doc_texts)

        # 4️⃣ Cosine rank
        ranked = rank_by_cosine_similarity(idea_embedding, doc_embeddings, docs)

        # 5️⃣ Return top K
        return {"filtered_docs": ranked[:self.top_k]}
