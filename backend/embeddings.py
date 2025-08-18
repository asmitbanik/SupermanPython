def embed_text(text):
from typing import List
import time
import requests
import numpy as np
from .config import GEMINI_API_KEY, EMBED_MODEL, HTTP_TIMEOUT

EMBED_URL = f"https://generativelanguage.googleapis.com/v1/{EMBED_MODEL}:batchEmbedContents?key={GEMINI_API_KEY}"

def _batch_payload(texts: List[str]):
    # batchEmbedContents expects list of "requests": [{model, content:{parts:[{text}]}}...]
    return {
        "requests": [
            {"model": EMBED_MODEL, "content": {"parts":[{"text": t}]}}
            for t in texts
        ]
    }

def _embed_batch(texts: List[str]) -> np.ndarray:
    r = requests.post(EMBED_URL, json=_batch_payload(texts), timeout=HTTP_TIMEOUT)
    r.raise_for_status()
    data = r.json()  # { responses: [{embedding:{values:[..]}} ...] }
    vecs = [resp["embedding"]["values"] for resp in data["responses"]]
    return np.asarray(vecs, dtype="float32")

def embed_texts(texts: List[str], batch_size: int = 48, max_retries: int = 5) -> np.ndarray:
    out = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        for attempt in range(max_retries):
            try:
                out.append(_embed_batch(batch))
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                time.sleep(1.2 * (attempt + 1))
    return np.vstack(out)

def embed_query(text: str) -> np.ndarray:
    return embed_texts([text])[0]
