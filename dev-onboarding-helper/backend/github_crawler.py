from typing import List, Dict, Tuple, Optional
import os, json, time
import requests
from .config import GITHUB_TOKEN, DATA_DIR, HTTP_TIMEOUT

API_HOST = "https://api.github.com"
RAW_HOST = "https://raw.githubusercontent.com"

TEXT_EXTS = {
    ".md",".txt",".py",".js",".ts",".tsx",".jsx",".java",".go",".rs",".rb",".php",".cs",
    ".c",".h",".cpp",".hpp",".m",".mm",".kt",".scala",".sql",".sh",".yml",".yaml",".toml",".ini",".json"
}
MAX_FILE_BYTES = 300_000

def _repo_dir(repo: str) -> str:
    d = os.path.join(DATA_DIR, repo.replace("/", "__"))
    os.makedirs(d, exist_ok=True)
    return d

def _headers():
    h = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        h["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return h

def _session():
    s = requests.Session()
    s.headers.update(_headers())
    return s

def _is_text(path: str) -> bool:
    p = path.lower()
    return any(p.endswith(ext) for ext in TEXT_EXTS)

def get_latest_commit(repo: str, default_branch_hint: str = "main") -> Tuple[str, str]:
    """
    Returns (branch, latest_sha). Tries 'main' then 'master'.
    """
    s = _session()
    for branch in (default_branch_hint, "master"):
        r = s.get(f"{API_HOST}/repos/{repo}/commits?sha={branch}&per_page=1", timeout=HTTP_TIMEOUT)
        if r.status_code == 200 and r.json():
            return branch, r.json()[0]["sha"]
    # fallback: repo main info
    r = s.get(f"{API_HOST}/repos/{repo}", timeout=HTTP_TIMEOUT)
    r.raise_for_status()
    branch = r.json()["default_branch"]
    r2 = s.get(f"{API_HOST}/repos/{repo}/commits?sha={branch}&per_page=1", timeout=HTTP_TIMEOUT)
    r2.raise_for_status()
    return branch, r2.json()[0]["sha"]

def load_state(repo: str) -> Dict:
    path = os.path.join(_repo_dir(repo), "state.json")
    if os.path.exists(path):
        return json.load(open(path, "r", encoding="utf-8"))
    return {"last_sha": None, "etags": {}}

def save_state(repo: str, state: Dict):
    path = os.path.join(_repo_dir(repo), "state.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def list_tree(repo: str, branch: str) -> List[Dict]:
    s = _session()
    r = s.get(f"{API_HOST}/repos/{repo}/git/trees/{branch}?recursive=1", timeout=HTTP_TIMEOUT)
    if r.status_code != 200:
        # try other branch
        other = "master" if branch != "master" else "main"
        r = s.get(f"{API_HOST}/repos/{repo}/git/trees/{other}?recursive=1", timeout=HTTP_TIMEOUT)
    r.raise_for_status()
    return [t for t in r.json().get("tree", []) if t.get("type") == "blob" and _is_text(t["path"])]

def compare_commits(repo: str, base: str, head: str) -> List[str]:
    """Return changed file paths between base...head."""
    s = _session()
    r = s.get(f"{API_HOST}/repos/{repo}/compare/{base}...{head}", timeout=HTTP_TIMEOUT)
    if r.status_code == 404:
        # base is too old (gc), do full
        return []
    r.raise_for_status()
    files = r.json().get("files", [])
    return [f["filename"] for f in files if _is_text(f["filename"])]

def fetch_raw(repo: str, path: str, branch: str, etag_cache: Dict) -> Tuple[str, Optional[str], Dict]:
    """
    Returns (path, text_or_none_if_not_modified, etag_cache_updated).
    Uses ETag to avoid rate limit when unchanged (304).
    """
    s = requests.Session()
    s.headers.update(_headers())
    url = f"{RAW_HOST}/{repo}/{branch}/{path}"
    headers = {}
    if url in etag_cache:
        headers["If-None-Match"] = etag_cache[url]

    r = s.get(url, headers=headers, timeout=HTTP_TIMEOUT)
    if r.status_code == 304:
        return path, None, etag_cache
    if r.status_code != 200 or len(r.content) > MAX_FILE_BYTES:
        return path, "", etag_cache
    if "ETag" in r.headers:
        etag_cache[url] = r.headers["ETag"]
    text = r.text
    return path, text, etag_cache

def crawl_repo_incremental(repo: str) -> Tuple[List[Dict], str]:
    """
    Returns (changed_files_texts, new_head_sha).
    Each item: {"path": str, "text": str}
    Uses commit diff + ETag to minimize work.
    """
    state = load_state(repo)
    branch, head_sha = get_latest_commit(repo)
    last_sha = state.get("last_sha")
    etags = state.get("etags", {})

    changed_paths: List[str]
    if not last_sha:
        # First time: full listing
        blobs = list_tree(repo, branch)
        changed_paths = [b["path"] for b in blobs]
    else:
        changed_paths = compare_commits(repo, last_sha, head_sha)
        if not changed_paths:
            # No change or compare unavailable -> maybe nothing to do
            return [], head_sha

    out = []
    for p in changed_paths:
        path, text, etags = fetch_raw(repo, p, branch, etags)
        if text is None:
            # not modified
            continue
        if text.strip() != "":
            out.append({"path": path, "text": text})

    # persist new state
    state["last_sha"] = head_sha
    state["etags"] = etags
    save_state(repo, state)

    return out, head_sha
