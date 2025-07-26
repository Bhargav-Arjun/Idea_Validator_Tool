# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as idea_router
from app.utils.rate_limiter import init_db
from app.utils.logger import logger

app = FastAPI(
    title="Idea Validator AI",
    description="A multi-agent tool that validates startup ideas using real-time research, embeddings, and LLMs.",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domain(s) in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(idea_router, prefix="/api")

# App startup event
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Initializing Vector DB and Usage DB...")
    init_db()
    logger.info("✅ Server is ready to accept requests.")
