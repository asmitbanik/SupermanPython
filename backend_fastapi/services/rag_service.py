import numpy as np
from services.github_service import GitHubService
from services.chunking_service import chunk_docs
from services.faiss_service import FaissService
from services.gemini_service import GeminiService

class RAGService:
    def __init__(self):
        self.github = GitHubService()
        self.chunker = chunk_docs
        self.faiss = FaissService()
        self.gemini = GeminiService()

    async def index_repo(self, repo: str):
        branch = await self.github.get_latest_commit(repo)
        if not branch:
            return {"repo": repo, "indexed": 0, "updated": 0, "head": "", "note": "Repo not found"}
        files = await self.github.list_files(repo, branch)
        docs = []
        for f in files:
            path = f["path"]
            text = await self.github.fetch_file(repo, path, branch)
            if text:
                docs.append({"path": path, "text": text})
        chunks = self.chunker(docs)
        texts = [c["text"] for c in chunks]
        vecs = await self.gemini.embed_texts(texts) if texts else []
        if vecs:
            arr = np.asarray(vecs, dtype="float32")
            await self.faiss.upsert(repo, arr, chunks)
        return {"repo": repo, "indexed": len(chunks), "updated": len(chunks), "head": branch, "note": "Indexed"}

    async def answer_question(self, repo: str, question: str, top_k: int = 5):
        qvec = await self.gemini.embed_query(question)
        qvec = np.asarray(qvec, dtype="float32")
        hits = await self.faiss.search(repo, qvec, top_k)
        if not hits:
            return {"answer": "Index is empty or repo not indexed yet. Please index the repo first.", "citations": []}
        context = "\n".join([h["text"] for h in hits])
        answer = await self.gemini.generate(question, context)
        citations = [{"path": h["path"], "rank": h["rank"], "score": h["score"]} for h in hits]
        return {"answer": answer, "citations": citations}
