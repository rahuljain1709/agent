# tavily_client.py  (REST fallback — works without Tavily SDK)
import os
import requests
from typing import List, Dict

class TavilyClient:
    """
    Minimal Tavily REST wrapper using requests.
    Uses environment variable TAVILY_API_KEY for the key.
    Replace the endpoint/path if Tavily's API differs — consult Tavily docs.
    """

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY is not set (env or constructor).")
        # Example base; change if Tavily uses another base URL
        self.base = "https://api.tavily.ai/v1"

    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Perform a search request and return simplified hits with title, url, content/snippet.
        """
        endpoint = f"{self.base}/search"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "query": query,
            "max_results": max_results,
            # add other parameters if tavily supports them (e.g. include_content)
        }

        resp = requests.post(endpoint, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        # Normalise response — adapt based on actual Tavily response structure
        results = []
        for r in data.get("results", [])[:max_results]:
            results.append({
                "title": r.get("title") or r.get("headline") or "Untitled",
                "url": r.get("url"),
                "content": r.get("content") or r.get("snippet") or ""
            })
        return results
