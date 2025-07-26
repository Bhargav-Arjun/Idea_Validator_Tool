from fastapi import APIRouter, Request, HTTPException
from app.agents.orchestrator import IdeaOrchestratorAgent
from app.utils.rate_limiter import allow_request

router = APIRouter()
orchestrator = IdeaOrchestratorAgent()

@router.post("/validate_idea")
async def validate_idea(request: Request):
    data = await request.json()
    user_idea = data.get("idea", "")
    user_id = request.client.host  # or use user_id from token/session

    if not allow_request(user_id):
        raise HTTPException(status_code=429, detail="You’ve reached your daily limit (2 prompts/day).")

    response = orchestrator.run(user_idea)
    return response
