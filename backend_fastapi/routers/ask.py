from fastapi import APIRouter, HTTPException
from models.ask import AskRequest, AskResponse
from services.rag_service import RAGService

router = APIRouter(prefix="/ask", tags=["ask"])
rag = RAGService()

@router.post("/", response_model=AskResponse)
async def ask_endpoint(req: AskRequest):
    result = await rag.answer_question(req.repo, req.question)
    return AskResponse(**result)
