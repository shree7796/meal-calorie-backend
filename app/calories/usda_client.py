import httpx
from typing import List, Dict, Any
from ..config import settings

class USDAClient:
    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key or settings.USDA_API_KEY
        self.base_url = base_url or settings.USDA_BASE_URL

    async def search(self, query: str, page_size: int = None) -> List[Dict[str, Any]]:
        params = {"query": query, "api_key": self.api_key, "pageSize": page_size or settings.PAGE_SIZE}
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(self.base_url, params=params)
            resp.raise_for_status()
            data = resp.json()
        return data.get("foods", [])
