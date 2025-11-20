from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.database import get_db
from app.models.user import User
from app.schemas.meal import FoodItemCreate, NutritionInfoSchema
from app.api.auth import get_current_user
from app.services.nutrition_service import NutritionService

router = APIRouter()

class NutritionAnalysisRequest(BaseModel):
    foods: List[FoodItemCreate]

@router.post("/analyze", response_model=NutritionInfoSchema)
async def analyze_nutrition(
    request: NutritionAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze nutrition information for a list of food items.
    Uses external APIs to get nutrition data.
    """
    nutrition_service = NutritionService()
    
    foods = request.foods
    
    total_nutrition = {
        "calories": 0,
        "protein": 0,
        "carbohydrates": 0,
        "fat": 0,
        "fiber": 0,
        "sugar": 0,
        "sodium": 0,
    }
    
    for food in foods:
        nutrition = await nutrition_service.get_nutrition_info(food.name, food.quantity)
        if nutrition:
            # Scale nutrition by quantity
            scale = food.quantity / 100  # Assuming nutrition is per 100g
            total_nutrition["calories"] += nutrition.get("calories", 0) * scale
            total_nutrition["protein"] += nutrition.get("protein", 0) * scale
            total_nutrition["carbohydrates"] += nutrition.get("carbohydrates", 0) * scale
            total_nutrition["fat"] += nutrition.get("fat", 0) * scale
            total_nutrition["fiber"] += nutrition.get("fiber", 0) * scale
            total_nutrition["sugar"] += nutrition.get("sugar", 0) * scale
            total_nutrition["sodium"] += nutrition.get("sodium", 0) * scale
    
    return NutritionInfoSchema(**total_nutrition)

