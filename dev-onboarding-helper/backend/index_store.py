import os, json
from typing import List, Dict, Tuple
import numpy as np
import faiss
from .config import DATA_DIR

def _repo_dir(repo: str) -> str:
    d = os.path.join(DATA_DIR, repo.replace("/", "__"))
    os.makedirs(d, exist_ok=True)
    return d

def _paths(repo: str) -> Tuple[str, str, str]:
    d = _repo_dir(repo)
    return (
        os.path.join(d, "index.faiss"),
        os.path.join(d, "meta.jsonl"),
        os.path.join(d, "vectors.npy"),
    )

def _normalize(V: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(V, axis=1, keepdims=True) + 1e-12
    return V / norms

def load_all(repo: str) -> Tuple[np.ndarray, List[Dict]]:
    _, meta_path, vec_path = _paths(repo)
    meta: List[Dict] = []
    if os.path.exists(meta_path):
        with open(meta_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    meta.append(json.loads(line))
    V = np.load(vec_path) if os.path.exists(vec_path) else np.empty((0, 0), dtype="float32")
    return V, meta

def save_all(repo: str, V: np.ndarray, meta: List[Dict]) -> None:
    idx_path, meta_path, vec_path = _paths(repo)
    if V.size == 0:
        # Nothing to save
        return
    Vn = _normalize(V.astype("float32"))
    dim = Vn.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(Vn)
    faiss.write_index(index, idx_path)
    with open(meta_path, "w", encoding="utf-8") as f:
        for m in meta:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")
    np.save(vec_path, V.astype("float32"))

def upsert(repo: str, new_meta: List[Dict], new_vecs: np.ndarray) -> Tuple[int, int]:
    """
    Merge/replace by key; rebuild FAISS once at the end.
    Returns (total_chunks, updated_chunks)
    """
    V, meta = load_all(repo)
    key_to_idx = {m["key"]: i for i, m in enumerate(meta)}

    if V.size == 0:
        meta = list(new_meta)
        V = new_vecs
        save_all(repo, V, meta)
        return len(meta), len(new_meta)

    V_list = [V]
    updated = 0
    for j, m in enumerate(new_meta):
        k = m["key"]
        if k in key_to_idx:
            i = key_to_idx[k]
            meta[i] = m
            V[i] = new_vecs[j]
            updated += 1
        else:
            meta.append(m)
            V_list.append(new_vecs[j:j+1])

    if len(V_list) > 1:
        V = np.vstack(V_list)

    save_all(repo, V, meta)
    return len(meta), updated

def load_faiss(repo: str):
    idx_path, meta_path, vec_path = _paths(repo)
    if not (os.path.exists(idx_path) and os.path.exists(meta_path) and os.path.exists(vec_path)):
        return None, []
    index = faiss.read_index(idx_path)
    meta = [json.loads(line) for line in open(meta_path, "r", encoding="utf-8") if line.strip()]
    return index, meta

def search(repo: str, qvec: np.ndarray, top_k: int) -> List[Dict]:
    index, meta = load_faiss(repo)
    if index is None:
        return []
    q = (qvec / (np.linalg.norm(qvec) + 1e-12)).astype("float32")[None, :]
    D, I = index.search(q, top_k)
    hits = []
    for rank, i in enumerate(I[0].tolist()):
        if 0 <= i < len(meta):
            m = dict(meta[i])
            m["rank"] = rank
            m["score"] = float(D[0][rank])
            hits.append(m)
    return hits
