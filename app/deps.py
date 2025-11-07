from functools import lru_cache
from app.calories.usda_client import USDAClient
from app.config import settings

@lru_cache()
def get_usda_client():
    return USDAClient(api_key=settings.USDA_API_KEY, base_url=settings.USDA_BASE_URL)
