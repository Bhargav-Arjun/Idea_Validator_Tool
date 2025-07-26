import os
import openai
from app.utils.config import get_settings

settings = get_settings()

# Load API key securely from .env
openai.api_key = settings.OPENAI_API_KEY

def generate_openai_response(prompt, model="gpt-3.5-turbo", temperature=0.7, max_tokens=1000):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"[OpenAI Error] {str(e)}"
