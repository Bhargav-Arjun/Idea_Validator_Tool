# app/agents/differentiator.py

from autogen import AssistantAgent
from app.llm.openai_client import openai_completion  # ✅ updated import
from typing import Dict
from pathlib import Path
import json


class DifferentiatorAgent(AssistantAgent):
    def __init__(self, name="DifferentiatorAgent"):
        super().__init__(name=name)

    def run(self, user_idea: str, competitor_analysis: Dict) -> Dict:
        """
        Compare idea with competitors and generate differentiation suggestions.
        """
        # Load the prompt from .txt file
        prompt_path = Path(__file__).resolve().parent.parent / "prompts" / "differentiator_prompt.txt"
        prompt_template = prompt_path.read_text(encoding="utf-8")

        # Convert competitor and gap analysis to JSON strings
        competitors_json = json.dumps(competitor_analysis["identified_competitors"], indent=2)
        market_gaps_json = json.dumps(competitor_analysis["market_gaps"], indent=2)

        # Format final prompt
        prompt = prompt_template.format(
            idea=user_idea,
            competitors=competitors_json,
            market_gaps=market_gaps_json
        )

        # Get LLM response via OpenAI API
        response = openai_completion(prompt)
        return response
