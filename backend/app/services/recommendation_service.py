from datetime import datetime
from typing import List, Dict
from app.models.user import User
from app.schemas.meal import MealResponse
from app.services.nutrition_service import NutritionService
from app.ml.recommendation_engine import RecommendationEngine

class RecommendationService:
    def __init__(self):
        self.nutrition_service = NutritionService()
        self.ml_engine = RecommendationEngine()

    async def generate_recommendations(
        self,
        user: User,
        meal_type: str,
        date: datetime
    ) -> List[MealResponse]:
        """
        Generate personalized meal recommendations using ML.
        """
        # Get user's TDEE and nutrition targets
        tdee = user.calculate_tdee()
        if not tdee:
            # Default values if user profile is incomplete
            tdee = 2000
        
        # Calculate meal-specific calorie targets
        meal_calorie_targets = {
            "breakfast": tdee * 0.25,
            "lunch": tdee * 0.35,
            "dinner": tdee * 0.30,
            "snack": tdee * 0.10,
        }
        
        target_calories = meal_calorie_targets.get(meal_type, tdee * 0.25)
        
        # Use ML engine to generate recommendations
        recommendations = self.ml_engine.recommend_meals(
            user=user,
            meal_type=meal_type,
            target_calories=target_calories
        )
        
        return recommendations

