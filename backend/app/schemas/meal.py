from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

class NutritionInfoSchema(BaseModel):
    calories: float
    protein: float
    carbohydrates: float
    fat: float
    fiber: float
    sugar: Optional[float] = None
    sodium: Optional[float] = None

class FoodItemCreate(BaseModel):
    name: str
    quantity: float
    unit: Optional[str] = "g"
    nutrition: Optional[NutritionInfoSchema] = None

class FoodItemResponse(BaseModel):
    id: uuid.UUID
    name: str
    quantity: float
    unit: Optional[str] = None
    nutrition: Optional[NutritionInfoSchema] = None

    class Config:
        from_attributes = True

class MealCreate(BaseModel):
    name: str
    description: Optional[str] = None
    meal_type: str
    date: datetime
    foods: List[FoodItemCreate]
    nutrition: Optional[NutritionInfoSchema] = None

class MealResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = None
    meal_type: str
    date: datetime
    foods: List[FoodItemResponse]
    nutrition: Optional[NutritionInfoSchema] = None

    class Config:
        from_attributes = True

