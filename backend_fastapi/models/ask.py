from pydantic import BaseModel
from typing import List

class AskRequest(BaseModel):
    repo: str
    question: str

class Citation(BaseModel):
    path: str
    rank: int
    score: float

class AskResponse(BaseModel):
    answer: str
    citations: List[Citation]
