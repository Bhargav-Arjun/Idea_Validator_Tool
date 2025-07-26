# app/agents/decision.py

from autogen import AssistantAgent
from app.rag.embedder import embed_text
from app.rag.vector_db import store_vector
from typing import Dict
from pathlib import Path
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")


class DecisionAgent(AssistantAgent):
    def __init__(self, name="DecisionAgent"):
        super().__init__(name=name)

    def run(self, user_idea: str, differentiation_data: Dict) -> Dict:
        """
        Final decision based on all agents. Stores result to Vector DB.
        """

        # Load prompt template from TXT file
        prompt_path = Path(__file__).resolve().parent.parent / "prompts" / "decision_score_prompt.txt"
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt file not found at: {prompt_path}")

        prompt_template = prompt_path.read_text(encoding="utf-8")

        # Format with actual data
        prompt = prompt_template.format(
            idea=user_idea,
            differentiation=differentiation_data
        )

        # LLM completion using OpenAI
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",  # or use "gpt-3.5-turbo"
                messages=[
                    {"role": "system", "content": "You are an expert business advisor who gives final decisions based on startup analyses."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            content = response['choices'][0]['message']['content']
        except Exception as e:
            content = f"❌ Error from OpenAI API: {e}"

        # Store in Vector DB
        idea_embedding = embed_text(user_idea)
        store_vector(embedding=idea_embedding, metadata=content)

        return content
