from autogen import AssistantAgent
from typing import Dict, List, Union
from pathlib import Path
import openai
import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set your OpenAI API key (from .env)
openai.api_key = os.getenv("OPENAI_API_KEY")


class CompetitorAnalysisAgent(AssistantAgent):
    def __init__(self, name="CompetitorAnalysisAgent"):
        super().__init__(name=name)

    def run(self, user_idea: str, filtered_docs: List[Dict]) -> Union[str, Dict]:
        """
        Analyze competitors based on retrieved documents (RAG output).

        Args:
            user_idea (str): The user’s product or startup idea.
            filtered_docs (List[Dict]): List of document dicts with a 'content' key.

        Returns:
            str or dict: LLM-generated competitor analysis based on input idea and docs.
        """
        # Combine retrieved document content
        combined_docs = "\n".join(
            [f"- {doc['content']}" for doc in filtered_docs]
        )

        # Optional truncation (safety if docs are too large)
        MAX_DOC_LEN = 3000
        combined_docs = combined_docs[:MAX_DOC_LEN]

        # Load the prompt template from file
        prompt_path = Path(__file__).resolve().parent.parent / "prompts" / "competitor_analysis_prompt.txt"
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt file not found at: {prompt_path}")
        
        prompt_template = prompt_path.read_text(encoding="utf-8")

        # Fill the prompt
        prompt = prompt_template.format(
            idea=user_idea,
            docs=combined_docs
        )

        # Logging for debug
        logging.info("Generated prompt:\n%s", prompt)

        # === OpenAI ChatCompletion Call ===
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Or "gpt-3.5-turbo" if needed
                messages=[
                    {"role": "system", "content": "You are a startup idea validation expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            return f"❌ Error from OpenAI API: {e}"
