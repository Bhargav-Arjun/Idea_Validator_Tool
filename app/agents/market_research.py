# app/agents/market_research.py

from autogen import AssistantAgent
from typing import List, Dict
from app.rag.embedder import embed_text
from app.rag.vector_db import retrieve_vectors
from app.utils.query_builder import build_queries
from app.llm.openrouter_client import openrouter_completion
from app.utils.logger import logger
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

SERP_API_KEY = os.getenv("7dfcdb86c75e55fc01dbc937a965662ceed559ab")  # or Tavily

class MarketResearchAgent(AssistantAgent):
    """
    1. Receives cleaned idea JSON from IdeaValidatorAgent.
    2. Attempts VectorDB retrieval.
    3. If results below threshold → triggers live web search.
    4. Returns list[dict] docs → RelevanceFilterAgent.
    """

    def __init__(self, name="MarketResearchAgent", top_k: int = 5, min_hits: int = 2):
        super().__init__(name=name)
        self.top_k = top_k        # how many to retrieve from DB
        self.min_hits = min_hits  # if fewer docs than this → search web

    # ---------- PUBLIC ENTRYPOINT ----------
    def run(self, validated_idea: Dict) -> Dict:
        """
        validated_idea comes from IdeaValidatorAgent
        Expected keys: cleaned_idea, target_audience, etc.
        """
        idea_text = validated_idea["cleaned_idea"]

        # 1️⃣ Vector DB retrieval
        docs = self._retrieve_from_db(idea_text)

        # 2️⃣ If not enough material → trigger web search
        if len(docs) < self.min_hits:
            logger.info("Insufficient docs in VectorDB → running live search")
            docs += self._internet_search(idea_text)

        # 3️⃣ Package payload
        return {
            "source_type": "vector_db" if len(docs) >= self.min_hits else "mixed",
            "docs": docs
        }

    # ---------- INTERNAL METHODS ----------
    def _retrieve_from_db(self, idea_text: str) -> List[Dict]:
        embedding = embed_text(idea_text)
        results = retrieve_vectors(embedding, top_k=self.top_k)
        logger.debug(f"VectorDB hits: {len(results)}")
        return results  # List[{"content": str, "metadata": {...}}]

    def _internet_search(self, idea_text: str) -> List[Dict]:
        queries = build_queries(idea_text)  # e.g. product keywords, competitor phrases
        aggregated_docs = []

        for q in queries:
            try:
                resp = self._serper_search(q)
                aggregated_docs.extend(resp)
            except Exception as e:
                logger.error(f"Search error for '{q}': {e}")

        return aggregated_docs

    # ---------- EXTERNAL API ----------
    def _serper_search(self, query: str) -> List[Dict]:
        url = "https://serper.dev/search"
        headers = {"X-API-KEY": SERP_API_KEY, "Content-Type": "application/json"}
        payload = {"q": query, "num": 10}

        r = httpx.post(url, json=payload, headers=headers, timeout=30)
        r.raise_for_status()
        data = r.json()

        # Normalize to common doc schema
        docs = []
        for item in data.get("organic", []):
            docs.append(
                {
                    "content": item["snippet"],
                    "metadata": {
                        "title": item["title"],
                        "link": item["link"],
                        "source": "web"
                    }
                }
            )
        return docs
