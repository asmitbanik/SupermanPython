import numpy as np
import pytest
from services.rag_service import RAGService

class DummyGitHub:
    async def get_latest_commit(self, repo: str, branch_hint: str = "main"):
        return "dummysha"
    async def list_files(self, repo: str, branch: str):
        return [{"path": "README.md", "type": "blob"}]
    async def fetch_file(self, repo: str, path: str, branch: str):
        return "# Title\nThis repo demonstrates auth via JWT.\n```python\ndef login(): pass\n```"

class DummyGemini:
    async def embed_texts(self, texts):
        # 2D list of fixed-size vectors
        return [[0.1, 0.2, 0.3] for _ in texts]
    async def embed_query(self, text):
        return [0.1, 0.2, 0.3]
    async def generate(self, question: str, context: str):
        return f"Answer: based on context len={len(context)}"

@pytest.mark.asyncio
async def test_rag_end_to_end(tmp_path):
    rag = RAGService()
    # inject dummies
    rag.github = DummyGitHub()
    rag.gemini = DummyGemini()
    # index
    res = await rag.index_repo("owner/repo")
    assert res["indexed"] > 0
    # ask
    ans = await rag.answer_question("owner/repo", "How auth works?", top_k=3)
    assert "answer" in ans and isinstance(ans["citations"], list)
