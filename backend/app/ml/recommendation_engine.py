from typing import List, Dict
from datetime import datetime
import uuid
from app.models.user import User
from app.schemas.meal import MealResponse, FoodItemResponse, NutritionInfoSchema
from app.data.dataset_loader import MealPlanDatasetLoader
import random

class RecommendationEngine:
    """
    ML-powered recommendation engine for personalized meal plans.
    Uses dataset-based recommendations with fallback to default food database.
    """
    
    def __init__(self):
        """Initialize recommendation engine with dataset loader."""
        self.dataset_loader = MealPlanDatasetLoader()
    
    # Sample food database (fallback if dataset doesn't have matches)
    FOOD_DATABASE = {
        "breakfast": [
            {"name": "Oatmeal with berries", "calories": 300, "protein": 10, "carbs": 55, "fat": 5},
            {"name": "Greek yogurt with honey", "calories": 250, "protein": 20, "carbs": 30, "fat": 5},
            {"name": "Scrambled eggs with toast", "calories": 350, "protein": 20, "carbs": 30, "fat": 15},
            {"name": "Smoothie bowl", "calories": 400, "protein": 15, "carbs": 60, "fat": 10},
            {"name": "Avocado toast", "calories": 320, "protein": 12, "carbs": 40, "fat": 14},
        ],
        "lunch": [
            {"name": "Grilled chicken salad", "calories": 450, "protein": 40, "carbs": 20, "fat": 20},
            {"name": "Quinoa bowl with vegetables", "calories": 500, "protein": 18, "carbs": 70, "fat": 15},
            {"name": "Salmon with sweet potato", "calories": 550, "protein": 35, "carbs": 50, "fat": 22},
            {"name": "Turkey wrap", "calories": 400, "protein": 30, "carbs": 45, "fat": 12},
            {"name": "Lentil soup", "calories": 350, "protein": 20, "carbs": 55, "fat": 8},
        ],
        "dinner": [
            {"name": "Baked salmon with vegetables", "calories": 600, "protein": 45, "carbs": 30, "fat": 30},
            {"name": "Chicken stir-fry", "calories": 550, "protein": 40, "carbs": 50, "fat": 20},
            {"name": "Vegetable pasta", "calories": 500, "protein": 15, "carbs": 80, "fat": 12},
            {"name": "Beef and vegetable stew", "calories": 650, "protein": 50, "carbs": 40, "fat": 35},
            {"name": "Tofu curry", "calories": 450, "protein": 20, "carbs": 60, "fat": 15},
        ],
        "snack": [
            {"name": "Apple with almond butter", "calories": 200, "protein": 5, "carbs": 30, "fat": 8},
            {"name": "Greek yogurt", "calories": 150, "protein": 15, "carbs": 10, "fat": 5},
            {"name": "Mixed nuts", "calories": 250, "protein": 8, "carbs": 10, "fat": 20},
            {"name": "Protein shake", "calories": 180, "protein": 25, "carbs": 15, "fat": 3},
            {"name": "Hummus with vegetables", "calories": 220, "protein": 8, "carbs": 25, "fat": 10},
        ],
    }

    def recommend_meals(
        self,
        user: User,
        meal_type: str,
        target_calories: float
    ) -> List[MealResponse]:
        """
        Generate meal recommendations based on user profile and goals.
        First tries dataset-based recommendations, then falls back to default database.
        """
        recommendations = []
        
        # Try to get recommendations from dataset first
        dataset_meals = self.dataset_loader.find_matching_meals(user, meal_type)
        
        if dataset_meals:
            # Use dataset meals
            calorie_tolerance = target_calories * 0.3  # 30% tolerance for dataset
            
            for meal_data in dataset_meals:
                meal_calories = meal_data.get("calories", target_calories)
                
                # Check if calories are within tolerance
                if abs(meal_calories - target_calories) <= calorie_tolerance:
                    # Estimate nutrition values based on calories, tags, and diet recommendation
                    nutrition = self._estimate_nutrition_from_meal(
                        meal_data["name"],
                        meal_calories,
                        meal_data.get("tags", []),
                        meal_data.get("diet_recommendation")
                    )
                    
                    meal = MealResponse(
                        id=uuid.uuid4(),
                        name=meal_data["name"],
                        description=f"Personalized {meal_type} based on your age, BMI, goal, and activity level",
                        meal_type=meal_type,
                        date=datetime.now(),
                        foods=[
                            FoodItemResponse(
                                id=uuid.uuid4(),
                                name=meal_data["name"],
                                quantity=100.0,
                                unit="g",
                                nutrition=nutrition
                            )
                        ],
                        nutrition=nutrition
                    )
                    recommendations.append(meal)
        
        # If no dataset matches or need more recommendations, use fallback database
        if len(recommendations) < 3:
            available_foods = self._filter_foods_by_preferences(
                self.FOOD_DATABASE.get(meal_type, []),
                user
            )
            
            if not available_foods:
                available_foods = self.FOOD_DATABASE.get(meal_type, [])
            
            calorie_tolerance = target_calories * 0.2  # 20% tolerance
            
            for food in available_foods:
                if abs(food["calories"] - target_calories) <= calorie_tolerance:
                    meal = MealResponse(
                        id=uuid.uuid4(),
                        name=food["name"],
                        description=f"Recommended {meal_type} based on your profile",
                        meal_type=meal_type,
                        date=datetime.now(),
                        foods=[
                            FoodItemResponse(
                                id=uuid.uuid4(),
                                name=food["name"],
                                quantity=100.0,
                                unit="g",
                                nutrition=NutritionInfoSchema(
                                    calories=food["calories"],
                                    protein=food["protein"],
                                    carbohydrates=food["carbs"],
                                    fat=food["fat"],
                                    fiber=5.0,
                                )
                            )
                        ],
                        nutrition=NutritionInfoSchema(
                            calories=food["calories"],
                            protein=food["protein"],
                            carbohydrates=food["carbs"],
                            fat=food["fat"],
                            fiber=5.0,
                        )
                    )
                    recommendations.append(meal)
            
            # If still no matches, get closest matches
            if not recommendations:
                available_foods.sort(key=lambda x: abs(x["calories"] - target_calories))
                top_foods = available_foods[:3]
                
                for food in top_foods:
                    meal = MealResponse(
                        id=uuid.uuid4(),
                        name=food["name"],
                        description=f"Recommended {meal_type} based on your profile",
                        meal_type=meal_type,
                        date=datetime.now(),
                        foods=[
                            FoodItemResponse(
                                id=uuid.uuid4(),
                                name=food["name"],
                                quantity=100.0,
                                unit="g",
                                nutrition=NutritionInfoSchema(
                                    calories=food["calories"],
                                    protein=food["protein"],
                                    carbohydrates=food["carbs"],
                                    fat=food["fat"],
                                    fiber=5.0,
                                )
                            )
                        ],
                        nutrition=NutritionInfoSchema(
                            calories=food["calories"],
                            protein=food["protein"],
                            carbohydrates=food["carbs"],
                            fat=food["fat"],
                            fiber=5.0,
                        )
                    )
                    recommendations.append(meal)
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def _estimate_nutrition_from_meal(
        self,
        meal_name: str,
        calories: float,
        tags: List[str],
        diet_recommendation: str = None
    ) -> NutritionInfoSchema:
        """
        Estimate nutrition values from meal name, calories, and tags.
        Uses heuristics based on tags, diet recommendation, and meal type.
        """
        # Default ratios
        protein_ratio = 0.25
        carb_ratio = 0.45
        fat_ratio = 0.30
        
        # Adjust based on diet recommendation first
        if diet_recommendation:
            if diet_recommendation == "Low_Carb":
                protein_ratio = 0.40
                carb_ratio = 0.20
                fat_ratio = 0.40
            elif diet_recommendation == "Low_Sodium":
                protein_ratio = 0.30
                carb_ratio = 0.45
                fat_ratio = 0.25
            elif diet_recommendation == "Balanced":
                protein_ratio = 0.25
                carb_ratio = 0.45
                fat_ratio = 0.30
        
        # Adjust based on tags
        tags_lower = [tag.lower() for tag in tags]
        
        if "high-protein" in tags_lower or "protein" in tags_lower:
            protein_ratio = 0.35
            carb_ratio = 0.35
            fat_ratio = 0.30
        elif "low-carb" in tags_lower or "low_carb" in tags_lower:
            protein_ratio = 0.40
            carb_ratio = 0.20
            fat_ratio = 0.40
        elif "low-fat" in tags_lower:
            protein_ratio = 0.30
            carb_ratio = 0.55
            fat_ratio = 0.15
        elif "high-calorie" in tags_lower:
            protein_ratio = 0.25
            carb_ratio = 0.50
            fat_ratio = 0.25
        
        # Calculate macros (4 cal/g for protein and carbs, 9 cal/g for fat)
        protein = (calories * protein_ratio) / 4
        carbs = (calories * carb_ratio) / 4
        fat = (calories * fat_ratio) / 9
        
        # Estimate fiber (typically 5-15g per meal)
        fiber = 8.0 if "fiber-rich" in tags_lower or "fiber" in tags_lower else 5.0
        
        return NutritionInfoSchema(
            calories=calories,
            protein=round(protein, 1),
            carbohydrates=round(carbs, 1),
            fat=round(fat, 1),
            fiber=fiber
        )

    def _filter_foods_by_preferences(self, foods: List[Dict], user: User) -> List[Dict]:
        """Filter foods based on user preferences, allergies, and dietary restrictions"""
        filtered = []
        
        for food in foods:
            # Check allergies (simplified - in production, check ingredient lists)
            if user.allergies:
                food_lower = food["name"].lower()
                for allergy in user.allergies:
                    if allergy.lower() in food_lower:
                        continue  # Skip this food
            
            # Check food preferences
            if user.food_preferences:
                food_lower = food["name"].lower()
                if "vegetarian" in user.food_preferences:
                    if any(meat in food_lower for meat in ["chicken", "beef", "turkey", "salmon", "meat"]):
                        continue
                if "vegan" in user.food_preferences:
                    if any(item in food_lower for item in ["egg", "yogurt", "milk", "cheese", "butter"]):
                        continue
            
            filtered.append(food)
        
        return filtered

