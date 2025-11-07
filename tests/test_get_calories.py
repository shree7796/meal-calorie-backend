import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_invalid_servings():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/get-calories", json={"dish_name":"chicken rice", "servings": 0})
    assert r.status_code == 400
