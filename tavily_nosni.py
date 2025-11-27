# tavily_nosni.py  (diagnostic / temporary)
import os
import certifi
import requests
from requests.adapters import HTTPAdapter
import urllib3
from urllib3.connection import HTTPSConnection
from urllib3.util import ssl_
import ssl
from typing import List, Dict

class NoSNIHTTPSConnection(HTTPSConnection):
    def connect(self):
        conn = self._new_conn()
        if getattr(self, "_tunnel_host", None):
            self._tunnel()
        ctx = ssl.create_default_context()
        ctx.load_verify_locations(cafile=certifi.where())
        # server_hostname=None disables SNI (diagnostic only)
        self.sock = ssl_.ssl_wrap_socket(conn, ctx, tls_in_tls=False, server_hostname=None)

class NoSNIAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            connection_class=NoSNIHTTPSConnection
        )

class TavilyClientNoSNI:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY not set.")
        self.base = "https://api.tavily.ai/v1"
        self.session = requests.Session()
        self.session.mount("https://", NoSNIAdapter())

    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        endpoint = f"{self.base}/search"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"query": query, "max_results": max_results}
        resp = self.session.post(endpoint, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return [{
            "title": r.get("title") or r.get("headline") or "Untitled",
            "url": r.get("url"),
            "content": r.get("content") or r.get("snippet") or ""
        } for r in data.get("results", [])[:max_results]]
