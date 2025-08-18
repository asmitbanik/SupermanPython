from typing import List, Dict
import requests, textwrap
from .config import GEN_MODEL, TOP_K, GEMINI_API_KEY
from .github_crawler import crawl_repo_incremental
from .chunker import chunk_docs
from .embeddings import embed_texts, embed_query
from .index_store import upsert, search

GEN_URL = "https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={key}"

SYSTEM = """You are an expert open-source developer.\nAnswer using ONLY the provided context. If the answer isn't in the context, say you don't know.\nInclude short code examples when helpful and cite file paths you used."""

def index_repository(repo: str) -> Dict:
    """
    Incremental indexing:
    - Get changed files since last SHA (or full on first run)
    - Chunk -> embed (batched) -> upsert into index
    """
    changed_files, head_sha = crawl_repo_incremental(repo)
    if not changed_files:
        return {"repo": repo, "indexed": 0, "updated": 0, "head": head_sha, "note": "No changes"}

    chunks = chunk_docs(changed_files)
    texts = [c["text"] for c in chunks]
    vecs  = embed_texts(texts)

    # minimal metadata
    meta = [{"key": c["key"], "path": c["path"], "chunk_idx": c["idx"], "text": c["text"]} for c in chunks]

    total, updated = upsert(repo, meta, vecs)
    return {"repo": repo, "indexed": len(chunks), "updated": updated, "total": total, "head": head_sha}

def _build_contents(question: str, contexts: List[Dict]) -> Dict:
    ctx = ""
    for c in contexts:
        snippet = c["text"].strip()[:2000]
        ctx += f"\n---\n# {c['path']} (chunk {c['chunk_idx']})\n{snippet}\n"
    prompt = textwrap.dedent(f"""
    {SYSTEM}

    Context:
    {ctx}

    Question: {question}

    Provide a clear, concise answer with citations (file paths).
    """).strip()
    return {"contents": [{"role": "user", "parts": [{"text": prompt}]}]}

def answer_question(repo: str, question: str, top_k: int = TOP_K) -> Dict:
    qvec = embed_query(question)
    hits = search(repo, qvec, top_k=top_k)
    if not hits:
        return {"answer": "Index is empty or repo not indexed yet. Please index the repo first.", "citations": []}

    payload = _build_contents(question, hits)
    url = GEN_URL.format(model=GEN_MODEL, key=GEMINI_API_KEY)
    r = requests.post(url, json=payload, timeout=120)
    r.raise_for_status()
    data = r.json()
    text = data["candidates"][0]["content"]["parts"][0]["text"]

    citations = [{"path": h["path"], "rank": h["rank"], "score": h["score"]} for h in hits]
    return {"answer": text, "citations": citations}
