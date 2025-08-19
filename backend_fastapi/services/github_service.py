import httpx
import logging
from config import GITHUB_TOKEN, HTTP_TIMEOUT
from typing import List, Dict, Optional

GITHUB_API = "https://api.github.com"

class GitHubService:
    def __init__(self):
        self.logger = logging.getLogger("GitHubService")
        self.headers = {"Accept": "application/vnd.github+json"}
        if GITHUB_TOKEN:
            self.headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    async def get_latest_commit(self, repo: str, branch_hint: str = "main") -> Optional[str]:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            for branch in (branch_hint, "master"):
                url = f"{GITHUB_API}/repos/{repo}/commits?sha={branch}&per_page=1"
                r = await client.get(url, headers=self.headers)
                if r.status_code == 200 and r.json():
                    return r.json()[0]["sha"]
            # fallback: get default branch
            url = f"{GITHUB_API}/repos/{repo}"
            r = await client.get(url, headers=self.headers)
            if r.status_code == 200:
                branch = r.json().get("default_branch", "main")
                url = f"{GITHUB_API}/repos/{repo}/commits?sha={branch}&per_page=1"
                r2 = await client.get(url, headers=self.headers)
                if r2.status_code == 200 and r2.json():
                    return r2.json()[0]["sha"]
        return None

    async def list_files(self, repo: str, branch: str) -> List[Dict]:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            url = f"{GITHUB_API}/repos/{repo}/git/trees/{branch}?recursive=1"
            r = await client.get(url, headers=self.headers)
            if r.status_code == 200:
                return [t for t in r.json().get("tree", []) if t.get("type") == "blob"]
        return []

    async def fetch_file(self, repo: str, path: str, branch: str) -> Optional[str]:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            url = f"https://raw.githubusercontent.com/{repo}/{branch}/{path}"
            r = await client.get(url, headers=self.headers)
            if r.status_code == 200:
                return r.text
        return None

    # Add more methods for incremental crawling, ETag/state management, etc.
