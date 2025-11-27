# tavily_client.py
import os
import requests
import certifi
from typing import List, Dict

class TavilyClient:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY not set.")
        self.base = "https://api.tavily.ai/v1"
        # Use certifi CA bundle explicitly
        self.verify = certifi.where()

    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        endpoint = f"{self.base}/search"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"query": query, "max_results": max_results}

        try:
            resp = requests.post(endpoint, json=payload, headers=headers, timeout=30, verify=self.verify)
            resp.raise_for_status()
        except requests.exceptions.SSLError:
            # let caller handle SSLError (so they can attempt No-SNI fallback)
            raise
        except requests.exceptions.RequestException as e:
            raise RuntimeError("Network error when contacting Tavily: " + str(e)) from e

        data = resp.json()
        results = []
        for r in data.get("results", [])[:max_results]:
            results.append({
                "title": r.get("title") or r.get("headline") or "Untitled",
                "url": r.get("url"),
                "content": r.get("content") or r.get("snippet") or ""
            })
        return results
