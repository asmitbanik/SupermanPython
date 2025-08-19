from fastapi import APIRouter, HTTPException
from models.index import IndexRequest, IndexResponse
from services.rag_service import RAGService

router = APIRouter(prefix="/index", tags=["index"])
rag = RAGService()

@router.post("/", response_model=IndexResponse)
async def index_endpoint(req: IndexRequest):
    result = await rag.index_repo(req.repo)
    return IndexResponse(**result)
