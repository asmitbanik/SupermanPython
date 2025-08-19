from pydantic import BaseModel
from typing import List

class RepoStatus(BaseModel):
    repo: str
    last_indexed: str
    head: str
    chunks: int

class RepoListResponse(BaseModel):
    repos: List[RepoStatus]
