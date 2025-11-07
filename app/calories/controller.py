from fastapi import APIRouter, Depends, HTTPException
from ..models import CalorieRequest, CalorieResponse
from .service import CalorieService, USDAClient
from ..deps import get_usda_client

router = APIRouter(prefix="", tags=["calories"])

@router.post("/get-calories", response_model=CalorieResponse)
async def get_calories(payload: CalorieRequest, service: CalorieService = Depends(lambda: CalorieService(get_usda_client()))):
    # Validate servings
    if payload.servings <= 0:
        raise HTTPException(status_code=400, detail="Servings must be positive")
    try:
        result = await service.get_calories_for(payload.dish_name, payload.servings)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal error")
    return result
