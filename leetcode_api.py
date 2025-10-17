from typing import Any, Dict, List, Optional, Tuple
import requests


class LeetCodeClient:
    def __init__(self, session_token: str, csrf_token: str) -> None:
        self.session_token = session_token
        self.csrf_token = csrf_token
        self.base_url = "https://leetcode.com"
        self.session = requests.Session()
        # LeetCode expects both cookies and headers for auth'd GraphQL
        self.session.cookies.set("LEETCODE_SESSION", self.session_token, domain=".leetcode.com")
        self.session.cookies.set("csrftoken", self.csrf_token, domain=".leetcode.com")
        self.session.headers.update({
            "Referer": self.base_url,
            "x-csrftoken": self.csrf_token,
            "User-Agent": "leetcode-sync-cli/1.0",
        })

    def _graphql(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        payload = {"query": query, "variables": variables or {}}
        resp = self.session.post(f"{self.base_url}/graphql/", json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if "errors" in data and data["errors"]:
            raise RuntimeError(f"LeetCode GraphQL error: {data['errors']}")
        return data["data"]

    def fetch_accepted_submissions(self, limit: int = 20) -> List[Dict[str, Any]]:
        # Returns list of {id, title, titleSlug, timestamp}
        query = (
            "query recentAcSubmissions($limit:Int){" 
            "  recentAcSubmissionList(limit:$limit){ id title titleSlug timestamp }" 
            "}"
        )
        data = self._graphql(query, {"limit": limit})
        submissions = data.get("recentAcSubmissionList") or []
        # Normalize keys
        normalized: List[Dict[str, Any]] = []
        for item in submissions:
            normalized.append({
                "id": str(item.get("id")),
                "title": item.get("title"),
                "titleSlug": item.get("titleSlug"),
                "timestamp": item.get("timestamp"),
            })
        return normalized

    def get_submission_details(self, submission_id: str) -> Tuple[str, str, str, str]:
        """
        Returns tuple: (code, language_key, title_slug, difficulty)
        language_key example: 'python3', 'cpp', 'java'
        """
        query = (
            "query submissionDetails($submissionId:Int!){"
            "  submissionDetails(submissionId:$submissionId){"
            "    code lang question{ titleSlug difficulty }"
            "  }"
            "}"
        )
        data = self._graphql(query, {"submissionId": int(submission_id)})
        details = data.get("submissionDetails") or {}
        code = details.get("code") or ""
        lang = details.get("lang") or ""
        question = details.get("question") or {}
        title_slug = question.get("titleSlug") or ""
        difficulty = question.get("difficulty") or "Unknown"
        return code, lang, title_slug, difficulty


