# 🧠 Idea Validator AI

A multi-agent tool powered by GPT-4 that validates startup ideas using RAG (Retrieval-Augmented Generation), competitor research, and smart filtering logic.

### ⚙️ Stack:
- **Backend:** FastAPI
- **LLMs:** OpenAI GPT-4 (via `openai` package)
- **Vector DB:** Chroma / FAISS
- **RAG Pipeline:** Custom Agents + Autogen Framework
- **Rate Limiter:** SQLite (2 prompts per day)
- **API-based Tool Integration:** Ready for OpenAI Developer Tools

---

### 🛠 Features
- 🌐 Real-time internet search & semantic filtering
- 🕵️ Competitor detection & market gap analysis
- 🌟 Differentiator suggestions for USP
- 📊 Final scorecard with GO / NO-GO verdict
- 🛡️ Daily usage limit to control costs

---

### 📦 How to Run

```bash
# Install deps
pip install -r requirements.txt

# Setup .env file
OPENAI_API_KEY=your-key
ALLOWED_PROMPTS_PER_DAY=2

# Run the backend
bash startup.sh
