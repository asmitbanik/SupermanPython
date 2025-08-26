import re
from typing import List, Dict, Tuple
from config import CHUNK_TOKENS, CHUNK_OVERLAP

try:
    import tiktoken
    _enc = tiktoken.get_encoding("cl100k_base")
except ImportError:
    _enc = None

MD_SPLIT = re.compile(r"(^|\n)#{1,6}\s|```", re.MULTILINE)

def _tok_count(text: str) -> int:
    if _enc:
        return len(_enc.encode(text))
    return len(text.split())

def _window(text: str, max_tokens: int, overlap: int) -> List[str]:
    if not _enc:
        # fallback: naive split
        words = text.split()
        out = []
        step = max(1, max_tokens - overlap)
        for start in range(0, len(words), step):
            out.append(' '.join(words[start:start+max_tokens]))
        return out
    ids = _enc.encode(text)
    out = []
    step = max(1, max_tokens - overlap)
    for start in range(0, len(ids), step):
        out.append(_enc.decode(ids[start:start+max_tokens]))
    return out

def _line_span(doc_text: str, chunk_text: str, start_search: int) -> Tuple[int, int, int]:
    """Return (line_start, line_end, new_search_pos). If not found, guesses using counts."""
    pos = doc_text.find(chunk_text, start_search)
    if pos == -1:
        pos = doc_text.find(chunk_text)  # fallback
        if pos == -1:
            # Best-effort: approximate to beginning
            return 1, 1 + chunk_text.count('\n'), start_search
    line_start = doc_text.count('\n', 0, pos) + 1
    line_end = line_start + chunk_text.count('\n')
    return line_start, line_end, pos + len(chunk_text)

def smart_chunk(doc: Dict) -> List[Dict]:
    path, text = doc["path"], doc["text"]
    segments = [s for s in MD_SPLIT.split(text) if s and not s.isspace()]
    if not segments:
        segments = [text]
    chunks = []
    idx = 0
    search_pos = 0
    for seg in segments:
        if _tok_count(seg) <= CHUNK_TOKENS:
            ls, le, search_pos = _line_span(text, seg, search_pos)
            chunks.append({"key": f"{path}:{idx}", "path": path, "idx": idx, "text": seg, "line_start": ls, "line_end": le})
            idx += 1
        else:
            for w in _window(seg, CHUNK_TOKENS, CHUNK_OVERLAP):
                ls, le, search_pos = _line_span(text, w, search_pos)
                chunks.append({"key": f"{path}:{idx}", "path": path, "idx": idx, "text": w, "line_start": ls, "line_end": le})
                idx += 1
    return chunks

def chunk_docs(docs: List[Dict]) -> List[Dict]:
    out = []
    for d in docs:
        out.extend(smart_chunk(d))
    return out
