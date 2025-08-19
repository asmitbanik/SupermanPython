from fastapi import APIRouter, HTTPException
from models.index import IndexRequest, IndexResponse

router = APIRouter(prefix="/index", tags=["index"])

@router.post("/", response_model=IndexResponse)
async def index_endpoint(req: IndexRequest):
    # TODO: Crawl repo, chunk, embed, upsert into vector DB
    return IndexResponse(repo=req.repo, indexed=0, updated=0, head="", note="Not implemented")
