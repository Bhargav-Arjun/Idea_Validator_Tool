# app/llm/openai_client.py

import httpx
import os
from dotenv import load_dotenv

load_dotenv()

# Correct: Get API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in environment variables.")

def openai_completion(prompt: str, model: str = "gpt-4", temperature: float = 0.3):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
    }

    response = httpx.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
    response.raise_for_status()

    content = response.json()["choices"][0]["message"]["content"]

    try:
        return eval(content)  # Optional: replace with safer parsing method
    except:
        raise ValueError("Model did not return valid JSON.")
