from tavily import Tavily

class TavilyClient:
    def __init__(self, api_key: str):
        self.client = Tavily(api_key)

    def search(self, query: str, max_results=5):
        response = self.client.search(
            query=query,
            max_results=max_results,
            include_content=True
        )
        hits = []
        for r in response.get("results", []):
            hits.append({
                "title": r.get("title"),
                "url": r.get("url"),
                "content": r.get("content") or r.get("snippet")
            })
        return hits
