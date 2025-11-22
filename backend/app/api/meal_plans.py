from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, List
from app.database import get_db
from app.models.user import User
from app.models.meal_plan import MealPlan
from app.models.meal import Meal, FoodItem
from app.schemas.meal_plan import MealPlanCreate, MealPlanResponse
from app.schemas.meal import MealResponse, FoodItemResponse, NutritionInfoSchema, MealCreate
from app.api.auth import get_current_user
from app.services.recommendation_service import RecommendationService

router = APIRouter()

def _meal_to_response(meal: Meal) -> MealResponse:
    """Convert Meal model to MealResponse schema"""
    from app.models.meal import NutritionInfo
    
    # Convert food items
    foods = []
    for food_item in meal.food_items:
        nutrition = None
        if food_item.nutrition_info:
            nutrition = NutritionInfoSchema(**food_item.nutrition_info)
        
        foods.append(FoodItemResponse(
            id=food_item.id,
            name=food_item.name,
            quantity=food_item.quantity,
            unit=food_item.unit,
            nutrition=nutrition,
        ))
    
    # Convert meal nutrition
    meal_nutrition = None
    if meal.nutrition_info:
        meal_nutrition = NutritionInfoSchema(**meal.nutrition_info)
    
    return MealResponse(
        id=meal.id,
        name=meal.name,
        description=meal.description,
        meal_type=meal.meal_type,
        date=meal.date,
        foods=foods,
        nutrition=meal_nutrition,
    )

@router.get("", response_model=List[MealPlanResponse])
async def get_meal_plans(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(MealPlan).filter(MealPlan.user_id == current_user.id)
    
    if start_date:
        query = query.filter(MealPlan.start_date >= start_date)
    if end_date:
        query = query.filter(MealPlan.end_date <= end_date)
    
    meal_plans = query.all()
    
    # Convert to response format
    result = []
    for plan in meal_plans:
        # Get meals for this plan
        meals = db.query(Meal).filter(
            Meal.user_id == current_user.id,
            Meal.date >= plan.start_date,
            Meal.date <= plan.end_date
        ).all()
        
        # Convert meals to response format
        meal_responses = [_meal_to_response(m) for m in meals]
        
        # Convert daily nutrition
        daily_nutrition = None
        if plan.daily_nutrition_target:
            daily_nutrition = NutritionInfoSchema(**plan.daily_nutrition_target)
        
        result.append(MealPlanResponse(
            id=plan.id,
            user_id=plan.user_id,
            start_date=plan.start_date,
            end_date=plan.end_date,
            meals=meal_responses,
            daily_nutrition=daily_nutrition,
            goal=plan.goal,
            created_at=plan.created_at,
        ))
    
    return result

@router.post("", response_model=MealPlanResponse, status_code=status.HTTP_201_CREATED)
async def create_meal_plan(
    meal_plan_data: MealPlanCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_meal_plan = MealPlan(
        user_id=current_user.id,
        start_date=meal_plan_data.start_date,
        end_date=meal_plan_data.end_date,
        goal=meal_plan_data.goal,
    )
    
    db.add(db_meal_plan)
    db.commit()
    db.refresh(db_meal_plan)
    
    daily_nutrition = None
    if db_meal_plan.daily_nutrition_target:
        daily_nutrition = NutritionInfoSchema(**db_meal_plan.daily_nutrition_target)
    
    return MealPlanResponse(
        id=db_meal_plan.id,
        user_id=db_meal_plan.user_id,
        start_date=db_meal_plan.start_date,
        end_date=db_meal_plan.end_date,
        meals=[],
        daily_nutrition=daily_nutrition,
        goal=db_meal_plan.goal,
        created_at=db_meal_plan.created_at,
    )

@router.post("/generate", response_model=MealPlanResponse, status_code=status.HTTP_201_CREATED)
async def generate_meal_plan(
    start_date: datetime = Query(..., description="Start date for meal plan"),
    end_date: datetime = Query(..., description="End date for meal plan"),
    goal: Optional[str] = Query(None, description="Health goal: weight_loss, muscle_gain, maintenance, diabetes_management"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Automatically generate a complete meal plan with meals for each day.
    Uses AI recommendations based on user profile, preferences, and goals.
    """
    # Validate date range
    if end_date <= start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date must be after start date"
        )
    
    # Calculate number of days
    days_diff = (end_date - start_date).days + 1
    if days_diff > 30:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Meal plan cannot exceed 30 days"
        )
    
    # Calculate user's daily nutrition targets
    tdee = current_user.calculate_tdee() or 2000  # Default to 2000 if not calculated
    goal = goal or current_user.health_goal or "maintenance"
    
    # Adjust calories based on goal
    calorie_adjustments = {
        "weight_loss": 0.85,  # 15% deficit
        "muscle_gain": 1.15,  # 15% surplus
        "maintenance": 1.0,
        "diabetes_management": 0.95,  # Slight deficit
    }
    daily_calories = tdee * calorie_adjustments.get(goal, 1.0)
    
    # Calculate macronutrient targets (based on goal)
    if goal == "muscle_gain":
        protein_ratio = 0.30  # 30% protein
        carb_ratio = 0.40     # 40% carbs
        fat_ratio = 0.30      # 30% fat
    elif goal == "weight_loss":
        protein_ratio = 0.35  # Higher protein for satiety
        carb_ratio = 0.35
        fat_ratio = 0.30
    else:  # maintenance or diabetes_management
        protein_ratio = 0.25
        carb_ratio = 0.45
        fat_ratio = 0.30
    
    daily_protein = (daily_calories * protein_ratio) / 4  # 4 cal per gram
    daily_carbs = (daily_calories * carb_ratio) / 4
    daily_fat = (daily_calories * fat_ratio) / 9  # 9 cal per gram
    
    # Create meal plan
    db_meal_plan = MealPlan(
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date,
        goal=goal,
        daily_nutrition_target={
            "calories": daily_calories,
            "protein": daily_protein,
            "carbohydrates": daily_carbs,
            "fat": daily_fat,
            "fiber": 25.0,  # Recommended daily fiber
        }
    )
    
    db.add(db_meal_plan)
    db.commit()
    db.refresh(db_meal_plan)
    
    # Generate meals for each day
    recommendation_service = RecommendationService()
    meal_types = ["breakfast", "lunch", "dinner", "snack"]
    
    # Meal calorie distribution
    meal_calorie_distribution = {
        "breakfast": 0.25,
        "lunch": 0.35,
        "dinner": 0.30,
        "snack": 0.10,
    }
    
    created_meals = []
    current_date = start_date
    
    while current_date <= end_date:
        for meal_type in meal_types:
            target_calories = daily_calories * meal_calorie_distribution[meal_type]
            
            # Get recommendations
            recommendations = await recommendation_service.generate_recommendations(
                user=current_user,
                meal_type=meal_type,
                date=current_date
            )
            
            if recommendations:
                # Use the first recommendation
                recommended_meal = recommendations[0]
                
                # Create meal
                meal_nutrition = recommended_meal.nutrition
                db_meal = Meal(
                    user_id=current_user.id,
                    name=recommended_meal.name,
                    description=recommended_meal.description or f"Generated {meal_type}",
                    meal_type=meal_type,
                    date=current_date,
                    nutrition_info=meal_nutrition.dict() if meal_nutrition else None,
                )
                
                db.add(db_meal)
                db.flush()  # Get meal ID
                
                # Create food items
                for food_item in recommended_meal.foods:
                    food_nutrition = food_item.nutrition
                    db_food_item = FoodItem(
                        meal_id=db_meal.id,
                        name=food_item.name,
                        quantity=food_item.quantity,
                        unit=food_item.unit,
                        nutrition_info=food_nutrition.dict() if food_nutrition else None,
                    )
                    db.add(db_food_item)
                
                created_meals.append(db_meal)
        
        # Move to next day
        current_date += timedelta(days=1)
    
    db.commit()
    
    # Refresh all meals to get IDs
    for meal in created_meals:
        db.refresh(meal)
    
    # Convert meals to response format
    meal_responses = [_meal_to_response(m) for m in created_meals]
    
    # Get daily nutrition
    daily_nutrition = NutritionInfoSchema(**db_meal_plan.daily_nutrition_target)
    
    return MealPlanResponse(
        id=db_meal_plan.id,
        user_id=db_meal_plan.user_id,
        start_date=db_meal_plan.start_date,
        end_date=db_meal_plan.end_date,
        meals=meal_responses,
        daily_nutrition=daily_nutrition,
        goal=db_meal_plan.goal,
        created_at=db_meal_plan.created_at,
    )

@router.post("/meals", response_model=MealResponse, status_code=status.HTTP_201_CREATED)
async def create_meal(
    meal_data: MealCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a single meal and associate it with a meal plan for that date.
    If no meal plan exists for the date, one will be created automatically.
    """
    # Check if meal plan exists for this date
    meal_date_start = meal_data.date.replace(hour=0, minute=0, second=0, microsecond=0)
    meal_date_end = meal_data.date.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    meal_plan = db.query(MealPlan).filter(
        MealPlan.user_id == current_user.id,
        MealPlan.start_date <= meal_data.date,
        MealPlan.end_date >= meal_data.date
    ).first()
    
    # Create meal plan if it doesn't exist
    if not meal_plan:
        meal_plan = MealPlan(
            user_id=current_user.id,
            start_date=meal_date_start,
            end_date=meal_date_end,
            goal=current_user.health_goal,
        )
        db.add(meal_plan)
        db.flush()
    
    # Create meal
    db_meal = Meal(
        user_id=current_user.id,
        name=meal_data.name,
        description=meal_data.description,
        meal_type=meal_data.meal_type,
        date=meal_data.date,
        nutrition_info=meal_data.nutrition.dict() if meal_data.nutrition else None,
    )
    db.add(db_meal)
    db.flush()  # Get meal ID
    
    # Create food items
    for food_item in meal_data.foods:
        food_nutrition = food_item.nutrition
        db_food_item = FoodItem(
            meal_id=db_meal.id,
            name=food_item.name,
            quantity=food_item.quantity,
            unit=food_item.unit,
            nutrition_info=food_nutrition.dict() if food_nutrition else None,
        )
        db.add(db_food_item)
    
    db.commit()
    db.refresh(db_meal)
    
    return _meal_to_response(db_meal)

