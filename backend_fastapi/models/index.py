from pydantic import BaseModel

class IndexRequest(BaseModel):
    repo: str

class IndexResponse(BaseModel):
    repo: str
    indexed: int
    updated: int
    head: str
    note: str = ""
