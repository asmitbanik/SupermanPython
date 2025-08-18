def chunk_text(text, chunk_size=500):
from typing import List, Dict
import re
import tiktoken
from .config import CHUNK_TOKENS, CHUNK_OVERLAP

MD_SPLIT = re.compile(r"(^|\n)#{1,6}\s|```", re.MULTILINE)
_enc = tiktoken.get_encoding("cl100k_base")

def _tok_count(text: str) -> int:
    return len(_enc.encode(text))

def _window(text: str, max_tokens: int, overlap: int) -> List[str]:
    ids = _enc.encode(text)
    out = []
    step = max(1, max_tokens - overlap)
    for start in range(0, len(ids), step):
        out.append(_enc.decode(ids[start:start+max_tokens]))
    return out

def smart_chunk(doc: Dict) -> List[Dict]:
    path, text = doc["path"], doc["text"]
    # split by md sections / code fences first
    segments = [s for s in MD_SPLIT.split(text) if s and not s.isspace()]
    if not segments:
        segments = [text]

    chunks = []
    idx = 0
    for seg in segments:
        if _tok_count(seg) <= CHUNK_TOKENS:
            chunks.append({"key": f"{path}:{idx}", "path": path, "idx": idx, "text": seg})
            idx += 1
        else:
            for w in _window(seg, CHUNK_TOKENS, CHUNK_OVERLAP):
                chunks.append({"key": f"{path}:{idx}", "path": path, "idx": idx, "text": w})
                idx += 1
    return chunks

def chunk_docs(docs: List[Dict]) -> List[Dict]:
    out = []
    for d in docs:
        out.extend(smart_chunk(d))
    return out
