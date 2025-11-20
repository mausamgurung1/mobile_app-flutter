from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List
from app.database import get_db
from app.models.user import User
from app.schemas.meal import MealResponse
from app.api.auth import get_current_user
from app.services.recommendation_service import RecommendationService

router = APIRouter()

@router.get("", response_model=List[MealResponse])
async def get_recommendations(
    meal_type: str = Query(..., description="Type of meal: breakfast, lunch, dinner, snack"),
    date: Optional[datetime] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get AI-powered meal recommendations based on user profile.
    """
    recommendation_service = RecommendationService()
    
    recommendations = await recommendation_service.generate_recommendations(
        user=current_user,
        meal_type=meal_type,
        date=date or datetime.now()
    )
    
    return recommendations

