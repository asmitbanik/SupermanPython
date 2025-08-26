from typing import List, Dict, Tuple
import requests, textwrap, time, hashlib
from .config import GEN_MODEL, TOP_K, GEMINI_API_KEY
from .github_crawler import crawl_repo_incremental
from .chunker import chunk_docs
from .embeddings import embed_texts, embed_query
from .index_store import upsert, search

GEN_URL = "https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={key}"

SYSTEM = """You are an expert open-source developer.\nAnswer using ONLY the provided context. If the answer isn't in the context, say you don't know.\nInclude short code examples when helpful and cite file paths you used."""

# Optional tokenizer for better token budgeting
try:
    import tiktoken
    _enc = tiktoken.get_encoding("cl100k_base")
except Exception:  # pragma: no cover
    _enc = None

# Conservative context token budget to avoid overruns; leave room for generation
MAX_CONTEXT_TOKENS = 3500

def _tok_count(text: str) -> int:
    if _enc is None:
        # Fallback: approximate by whitespace tokens
        return max(1, len(text.split()))
    try:
        return len(_enc.encode(text))
    except Exception:
        return max(1, len(text.split()))

def _sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8", errors="ignore")).hexdigest()

def _dedupe_hits(hits: List[Dict]) -> List[Dict]:
    seen = set()
    out = []
    for h in hits:
        key = f"{h.get('path','')}:{h.get('chunk_idx', h.get('idx', ''))}:{_sha1(h.get('text',''))}"
        if key in seen:
            continue
        seen.add(key)
        out.append(h)
    return out

def _limit_per_path(hits: List[Dict], per_path: int = 2) -> List[Dict]:
    counts = {}
    out = []
    for h in hits:
        p = h.get("path", "")
        c = counts.get(p, 0)
        if c < per_path:
            out.append(h)
            counts[p] = c + 1
    return out

def _pack_context(hits: List[Dict], question: str) -> Tuple[str, List[Dict]]:
    """Greedily pack contexts under token budget; return packed text and used hits."""
    header = f"{SYSTEM}\n\nContext:\n"
    qpart = f"\n\nQuestion: {question}\n\nProvide a clear, concise answer with citations (file paths)."
    budget = MAX_CONTEXT_TOKENS

    # Roughly account for non-context tokens as well
    overhead = _tok_count(header) + _tok_count(qpart)
    if overhead >= budget:
        budget = max(512, MAX_CONTEXT_TOKENS)  # ensure some room

    out_text = []
    used = []
    used_tokens = 0
    for h in hits:
        snippet = (h.get("text", "") or "").strip()
        if not snippet:
            continue
        block = f"\n---\n# {h.get('path','unknown')} (chunk {h.get('chunk_idx', h.get('idx','?'))})\n{snippet}\n"
        need = _tok_count(block)
        if used_tokens + need > budget:
            break
        out_text.append(block)
        used.append(h)
        used_tokens += need

    return "".join(out_text), used

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
    # Apply dedupe and per-path cap before packing
    contexts = _dedupe_hits(contexts)
    contexts = _limit_per_path(contexts, per_path=2)
    ctx_text, _used = _pack_context(contexts, question)
    prompt = textwrap.dedent(
        f"""
        {SYSTEM}

        Context:
        {ctx_text}

        Question: {question}

        Provide a clear, concise answer with citations (file paths).
        """
    ).strip()
    return {"contents": [{"role": "user", "parts": [{"text": prompt}]}]}

def answer_question(repo: str, question: str, top_k: int = TOP_K) -> Dict:
    qvec = embed_query(question)
    hits = search(repo, qvec, top_k=top_k)
    if not hits:
        return {"answer": "Index is empty or repo not indexed yet. Please index the repo first.", "citations": []}

    payload = _build_contents(question, hits)
    url = GEN_URL.format(model=GEN_MODEL, key=GEMINI_API_KEY)

    # Resilient call with basic retries
    last_err = None
    for attempt in range(3):
        try:
            r = requests.post(url, json=payload, timeout=120)
            r.raise_for_status()
            data = r.json()
            # Safely extract text
            text = (
                data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "")
            )
            if not text:
                text = "I'm not confident from the provided context. Please index more files or refine the question."
            citations = [
                {"path": h.get("path", ""), "rank": h.get("rank", 0), "score": h.get("score", 0.0)}
                for h in hits
            ]
            return {"answer": text, "citations": citations}
        except Exception as e:  # pragma: no cover
            last_err = e
            time.sleep(1.2 * (attempt + 1))

    # Fallback if all retries failed
    msg = f"Generation failed after retries: {last_err}"
    citations = [
        {"path": h.get("path", ""), "rank": h.get("rank", 0), "score": h.get("score", 0.0)}
        for h in hits
    ]
    return {"answer": msg, "citations": citations}
