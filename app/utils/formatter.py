# app/utils/formatter.py
import re

def format_idea(idea: str):
    # Remove extra spaces and newlines
    idea = re.sub(r'\s+', ' ', idea).strip()
    return idea