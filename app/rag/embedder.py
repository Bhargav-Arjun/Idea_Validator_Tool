# Embedding logic placeholder 
from openai import OpenAI
from dotenv import load_dotenv
import os
# app/utils/config.py

load_dotenv()
client = OpenAI(api_key=os.getenv("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"))

def embed_text(text: str):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def embed_batch(texts: list):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )
    return [r.embedding for r in response.data]
