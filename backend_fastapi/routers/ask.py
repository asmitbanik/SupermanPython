from fastapi import APIRouter, HTTPException
from models.ask import AskRequest, AskResponse

router = APIRouter(prefix="/ask", tags=["ask"])

@router.post("/", response_model=AskResponse)
async def ask_endpoint(req: AskRequest):
    # TODO: Retrieve context, augment query, call LLM, return answer
    return AskResponse(answer="Not implemented", citations=[])
