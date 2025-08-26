import os
import numpy as np
try:
    import faiss  # type: ignore
except Exception:
    faiss = None  # graceful degradation if FAISS is not installed
import json
from config import VECTOR_DIR
from typing import List, Dict

class FaissService:
    def __init__(self):
        os.makedirs(VECTOR_DIR, exist_ok=True)

    def _paths(self, repo: str):
        safe = repo.replace('/', '__')
        return (
            os.path.join(VECTOR_DIR, f"{safe}.faiss"),
            os.path.join(VECTOR_DIR, f"{safe}.meta.jsonl"),
            os.path.join(VECTOR_DIR, f"{safe}.vecs.npy"),
        )

    async def upsert(self, repo: str, vectors: np.ndarray, meta: List[Dict]):
        idx_path, meta_path, vec_path = self._paths(repo)
        if vectors.size == 0:
            return 0, 0
        if faiss is None:
            # Cannot persist vectors without FAISS installed
            return 0, 0
        Vn = vectors.astype('float32')
        dim = Vn.shape[1]
        index = faiss.IndexFlatIP(dim)
        index.add(Vn)
        faiss.write_index(index, idx_path)
        with open(meta_path, 'w', encoding='utf-8') as f:
            for m in meta:
                f.write(json.dumps(m, ensure_ascii=False) + '\n')
        np.save(vec_path, vectors)
        return len(meta), len(meta)

    async def search(self, repo: str, query_vec: np.ndarray, top_k: int):
        idx_path, meta_path, vec_path = self._paths(repo)
        if faiss is None:
            return []
        if not (os.path.exists(idx_path) and os.path.exists(meta_path) and os.path.exists(vec_path)):
            return []
        index = faiss.read_index(idx_path)
        meta = [json.loads(line) for line in open(meta_path, 'r', encoding='utf-8') if line.strip()]
        q = query_vec.astype('float32')[None, :]
        D, I = index.search(q, top_k)
        hits = []
        for rank, i in enumerate(I[0].tolist()):
            if 0 <= i < len(meta):
                m = dict(meta[i])
                m['rank'] = rank
                m['score'] = float(D[0][rank])
                m['_vec_index'] = int(i)
                hits.append(m)
        return hits

    def vectors_for_repo(self, repo: str) -> np.ndarray:
        """Load vectors array for a repo (float32)."""
        _, _, vec_path = self._paths(repo)
        if not os.path.exists(vec_path):
            return np.empty((0, 0), dtype='float32')
        return np.load(vec_path).astype('float32')
