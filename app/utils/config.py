
# app/utils/config.py

import os
from dotenv import load_dotenv

# Load .env file from root directory
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

CONFIG = {
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
    "OPENROUTER_API_KEY": os.getenv("OPENROUTER_API_KEY"),
    "ALLOWED_PROMPTS_PER_DAY": int(os.getenv("ALLOWED_PROMPTS_PER_DAY", 2))
}
