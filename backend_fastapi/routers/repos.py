from fastapi import APIRouter
from models.repos import RepoListResponse

router = APIRouter(prefix="/repos", tags=["repos"])

@router.get("/", response_model=RepoListResponse)
async def list_repos():
    # TODO: List indexed repos and their status
    return RepoListResponse(repos=[])
