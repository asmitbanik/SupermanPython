from fastapi import APIRouter
from models.repos import RepoListResponse, RepoStatus
from config import VECTOR_DIR
import os, json

router = APIRouter(prefix="/repos", tags=["repos"])

@router.get("/", response_model=RepoListResponse)
async def list_repos():
    repos = []
    for fname in os.listdir(VECTOR_DIR):
        if fname.endswith('.meta.jsonl'):
            repo = fname.replace('.meta.jsonl', '').replace('__', '/')
            meta_path = os.path.join(VECTOR_DIR, fname)
            try:
                with open(meta_path, 'r', encoding='utf-8') as f:
                    lines = [json.loads(line) for line in f if line.strip()]
                chunks = len(lines)
                last_indexed = lines[0]["key"] if lines else ""
                head = lines[0]["path"] if lines else ""
                repos.append(RepoStatus(repo=repo, last_indexed=last_indexed, head=head, chunks=chunks))
            except Exception:
                continue
    return RepoListResponse(repos=repos)
