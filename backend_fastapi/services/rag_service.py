import numpy as np
import hashlib
from services.github_service import GitHubService
from services.chunking_service import chunk_docs
from services.faiss_service import FaissService
from services.gemini_service import GeminiService

try:
    import tiktoken
    _enc = tiktoken.get_encoding("cl100k_base")
except Exception:
    _enc = None

MAX_CONTEXT_TOKENS = 3500

def _tok_count(text: str) -> int:
    if _enc is None:
        return max(1, len(text.split()))
    try:
        return len(_enc.encode(text))
    except Exception:
        return max(1, len(text.split()))

def _sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8", errors="ignore")).hexdigest()

def _dedupe_hits(hits):
    seen = set(); out = []
    for h in hits:
        key = f"{h.get('path','')}:{h.get('chunk_idx', h.get('idx',''))}:{_sha1(h.get('text',''))}"
        if key in seen:
            continue
        seen.add(key); out.append(h)
    return out

def _limit_per_path(hits, per_path: int = 2):
    counts = {}; out = []
    for h in hits:
        p = h.get('path','')
        c = counts.get(p, 0)
        if c < per_path:
            out.append(h); counts[p] = c + 1
    return out

def _pack_context(hits, question: str):
    header = "Context:\n"
    qpart = f"\n\nQuestion: {question}\nProvide a clear, concise answer with citations (file paths)."
    budget = MAX_CONTEXT_TOKENS - (_tok_count(header) + _tok_count(qpart))
    if budget < 512:
        budget = 512
    out_text = []; used = []; used_tokens = 0
    for h in hits:
        snippet = (h.get('text','') or '').strip()
        if not snippet:
            continue
        block = f"\n---\n# {h.get('path','unknown')} (chunk {h.get('chunk_idx', h.get('idx','?'))})\n{snippet}\n"
        need = _tok_count(block)
        if used_tokens + need > budget:
            break
        out_text.append(block); used.append(h); used_tokens += need
    return "".join(out_text), used

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
        if not qvec:
            return {"answer": "Query embedding failed. Check LLM config.", "citations": []}
        qvec = np.asarray(qvec, dtype="float32")
        hits = await self.faiss.search(repo, qvec, top_k)
        if not hits:
            return {"answer": "Index is empty or repo not indexed yet. Please index the repo first.", "citations": []}

        # MMR reranking on the returned candidate set using stored vectors
        V = self.faiss.vectors_for_repo(repo)
        cand = [h for h in hits if V.size != 0 and h.get('_vec_index') is not None]
        selected = []
        lambda_mul = 0.5
        if cand:
            q = qvec / (np.linalg.norm(qvec) + 1e-12)
            cand_idx = [h['_vec_index'] for h in cand]
            cand_vecs = V[cand_idx]
            cand_vecs = cand_vecs / (np.linalg.norm(cand_vecs, axis=1, keepdims=True) + 1e-12)
            chosen = []
            remaining = list(range(len(cand)))
            # pick the best by similarity first
            sims = cand_vecs @ q
            if len(remaining) > 0:
                first = int(np.argmax(sims))
                chosen.append(first)
                remaining.remove(first)
            while remaining and len(chosen) < min(len(cand), top_k):
                best_i = None
                best_score = -1e9
                for ridx in remaining:
                    sim_q = float(sims[ridx])
                    sim_div = 0.0
                    for cidx in chosen:
                        sim_div = max(sim_div, float(cand_vecs[ridx] @ cand_vecs[cidx]))
                    score = lambda_mul * sim_q - (1 - lambda_mul) * sim_div
                    if score > best_score:
                        best_score = score
                        best_i = ridx
                chosen.append(best_i)
                remaining.remove(best_i)
            selected = [cand[i] for i in chosen]
        if not selected:
            selected = hits

        hits = _dedupe_hits(selected)
        hits = _limit_per_path(hits, per_path=2)
        ctx_text, used = _pack_context(hits, question)
        answer = await self.gemini.generate(question, ctx_text)
        citations = [{
            "path": h.get("path",""),
            "rank": h.get("rank",0),
            "score": h.get("score",0.0),
            "line_start": h.get("line_start"),
            "line_end": h.get("line_end"),
        } for h in used]
        return {"answer": answer or "No answer generated.", "citations": citations}
