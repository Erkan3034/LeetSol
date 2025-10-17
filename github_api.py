from typing import Optional, Dict, Any
import base64
import requests


class GitHubClient:
    def __init__(self, token: str, owner: str, repo: str) -> None:
        self.token = token
        self.owner = owner
        self.repo = repo
        self.base_url = f"https://api.github.com/repos/{owner}/{repo}"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "leetcode-sync-cli/1.0",
        })

    def get_file_sha(self, path: str) -> Optional[str]:
        resp = self.session.get(f"{self.base_url}/contents/{path}", timeout=30)
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, dict):
            return data.get("sha")
        return None

    def create_or_update_file(self, path: str, content: bytes, commit_message: str, sha: Optional[str] = None) -> Dict[str, Any]:
        encoded = base64.b64encode(content).decode("utf-8")
        payload: Dict[str, Any] = {
            "message": commit_message,
            "content": encoded,
            "branch": "main",
        }
        if sha:
            payload["sha"] = sha
        resp = self.session.put(f"{self.base_url}/contents/{path}", json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()


