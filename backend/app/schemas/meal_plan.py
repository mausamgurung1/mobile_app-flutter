from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime
import uuid
import os
from .meal import MealResponse, NutritionInfoSchema

class MealPlanCreate(BaseModel):
    start_date: datetime
    end_date: datetime
    goal: Optional[str] = None

# Support both UUID (PostgreSQL) and String (SQLite) for id
USE_SQLITE = os.getenv("DATABASE_URL", "").startswith("sqlite")

if USE_SQLITE:
    class MealPlanResponse(BaseModel):
        id: str
        user_id: str
        start_date: datetime
        end_date: datetime
        meals: list[MealResponse]
        daily_nutrition: Optional[NutritionInfoSchema] = None
        goal: Optional[str] = None
        created_at: Optional[datetime] = None

        class Config:
            from_attributes = True
else:
    class MealPlanResponse(BaseModel):
        id: uuid.UUID
        user_id: uuid.UUID
        start_date: datetime
        end_date: datetime
        meals: list[MealResponse]
        daily_nutrition: Optional[NutritionInfoSchema] = None
        goal: Optional[str] = None
        created_at: Optional[datetime] = None

        class Config:
            from_attributes = True

