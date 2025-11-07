from .usda_client import USDAClient
from .fuzzy import best_match
from cachetools import TTLCache
from typing import Optional

# simple in-memory cache: allow caching frequent lookups
CACHE = TTLCache(maxsize=1024, ttl=60*60)  # 1 hour TTL

class CalorieService:
    def __init__(self, usda_client: USDAClient = None):
        self.usda = usda_client or USDAClient()

    async def get_calories_for(self, dish_name: str, servings: float):
        key = f"{dish_name.lower()}:{servings}"
        if key in CACHE:
            return CACHE[key]

        results = await self.usda.search(dish_name)
        if not results:
            raise ValueError("Dish not found")

        best, score = best_match(dish_name, results, key="description", score_cutoff=55)
        if not best:
            # fallback: take first with warning
            best = results[0]

        calories_per_100g = None
        # USDA returns nutrients differently; find energy/kcal value
        for nutrient in best.get("foodNutrients", []):
            if nutrient.get("nutrientName", "").lower() in ("energy", "energy (kcal)", "calories"):
                calories_per_100g = nutrient.get("value")
                break

        # If calories per 100g not found, check 'servingSize' fields
        calories_per_serving = None
        if calories_per_100g:
            calories_per_serving = calories_per_100g
        else:
            for nutrient in best.get("foodNutrients", []):
                if "kcal" in str(nutrient.get("nutrientName","")).lower():
                    calories_per_serving = nutrient.get("value")
                    break

        if calories_per_serving is None:
            raise ValueError("Calorie info not available for selected item")

        total_calories = float(calories_per_serving) * float(servings)

        response = {
            "dish_name": dish_name,
            "servings": servings,
            "calories_per_serving": float(calories_per_serving),
            "total_calories": float(total_calories),
            "source": "USDA FoodData Central",
        }

        CACHE[key] = response
        return response
