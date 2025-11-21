"""
Dataset loader for meal plan recommendations.
Loads and processes the comprehensive diet recommendations dataset CSV file.
"""
import csv
import os
from pathlib import Path
from typing import List, Dict, Optional
from app.models.user import User

class MealPlanDatasetLoader:
    """Load and query meal plan dataset based on user attributes."""
    
    def __init__(self):
        # Try comprehensive dataset first, fallback to simple dataset
        backend_dir = Path(__file__).parent.parent.parent
        comprehensive_path = backend_dir / "ml" / "diet_recommendations_dataset.csv"
        simple_path = Path(__file__).parent / "meal_plan_dataset.csv"
        
        if comprehensive_path.exists():
            self.dataset_path = comprehensive_path
            self.dataset_type = "comprehensive"
        elif simple_path.exists():
            self.dataset_path = simple_path
            self.dataset_type = "simple"
        else:
            self.dataset_path = None
            self.dataset_type = None
        
        self.dataset = []
        self._load_dataset()
    
    def _load_dataset(self):
        """Load dataset from CSV file."""
        if not self.dataset_path or not self.dataset_path.exists():
            print(f"Warning: Dataset file not found")
            return
        
        try:
            with open(self.dataset_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.dataset.append(row)
            print(f"Loaded {len(self.dataset)} entries from {self.dataset_type} dataset")
        except Exception as e:
            print(f"Error loading dataset: {e}")
            self.dataset = []
    
    def _calculate_bmi(self, user: User) -> Optional[float]:
        """Calculate BMI from user height and weight."""
        if not user.height or not user.weight:
            return None
        
        height_m = user.height / 100  # Convert cm to meters
        bmi = user.weight / (height_m ** 2)
        return round(bmi, 1)
    
    def _normalize_disease_type(self, goal: Optional[str]) -> str:
        """Map health goal to disease type in dataset."""
        if not goal:
            return "None"
        
        goal_lower = goal.lower()
        if "diabetes" in goal_lower:
            return "Diabetes"
        elif "obesity" in goal_lower or "weight_loss" in goal_lower or "weight loss" in goal_lower:
            return "Obesity"
        elif "hypertension" in goal_lower or "blood_pressure" in goal_lower:
            return "Hypertension"
        else:
            return "None"
    
    def _normalize_activity(self, activity: Optional[str]) -> str:
        """Normalize activity level to dataset format."""
        if not activity:
            return "Moderate"
        
        activity_lower = activity.lower()
        if "sedentary" in activity_lower:
            return "Sedentary"
        elif "lightly_active" in activity_lower or "lightly active" in activity_lower:
            return "Moderate"
        elif "moderately_active" in activity_lower or "moderately active" in activity_lower:
            return "Moderate"
        elif "very_active" in activity_lower or "very active" in activity_lower:
            return "Active"
        elif "extremely_active" in activity_lower or "extremely active" in activity_lower:
            return "Active"
        else:
            return "Moderate"
    
    def _get_dietary_restrictions(self, user: User) -> str:
        """Get dietary restrictions from user profile."""
        restrictions = []
        
        # Check health goal for restrictions
        if user.health_goal:
            goal_lower = user.health_goal.lower()
            if "diabetes" in goal_lower:
                restrictions.append("Low_Sugar")
            if "hypertension" in goal_lower or "blood_pressure" in goal_lower:
                restrictions.append("Low_Sodium")
        
        if restrictions:
            return ",".join(restrictions)
        return "None"
    
    def _get_allergies(self, user: User) -> str:
        """Get allergies from user profile."""
        if user.allergies:
            # Convert list to comma-separated string or return as is
            if isinstance(user.allergies, list):
                return ",".join(user.allergies)
            return str(user.allergies)
        return "None"
    
    def _get_preferred_cuisine(self, user: User) -> str:
        """Get preferred cuisine from user profile."""
        if user.food_preferences:
            prefs = user.food_preferences.lower() if isinstance(user.food_preferences, str) else str(user.food_preferences).lower()
            # Map common preferences to cuisines
            if "indian" in prefs:
                return "Indian"
            elif "chinese" in prefs:
                return "Chinese"
            elif "mexican" in prefs:
                return "Mexican"
            elif "italian" in prefs:
                return "Italian"
        return "Indian"  # Default
    
    def find_matching_meals(
        self,
        user: User,
        meal_type: str
    ) -> List[Dict]:
        """
        Find matching meals from comprehensive dataset based on user profile.
        
        Args:
            user: User model with profile information
            meal_type: Type of meal (breakfast, lunch, dinner, snack)
        
        Returns:
            List of matching meal entries from dataset
        """
        if not self.dataset:
            return []
        
        # Use comprehensive dataset matching
        if self.dataset_type == "comprehensive":
            return self._find_matches_comprehensive(user, meal_type)
        else:
            # Fallback to simple dataset matching
            return self._find_matches_simple(user, meal_type)
    
    def _find_matches_comprehensive(self, user: User, meal_type: str) -> List[Dict]:
        """Find matches using comprehensive diet recommendations dataset."""
        matches = []
        
        # Calculate user attributes
        user_bmi = self._calculate_bmi(user)
        disease_type = self._normalize_disease_type(user.health_goal)
        activity = self._normalize_activity(user.activity_level)
        dietary_restrictions = self._get_dietary_restrictions(user)
        allergies = self._get_allergies(user)
        preferred_cuisine = self._get_preferred_cuisine(user)
        
        # Score and rank matches
        scored_matches = []
        
        for entry in self.dataset:
            score = 0
            
            # Age matching (within 10 years gets points)
            entry_age = self._safe_int(entry.get("Age", ""))
            if user.age and entry_age:
                age_diff = abs(user.age - entry_age)
                if age_diff <= 5:
                    score += 10
                elif age_diff <= 10:
                    score += 5
                elif age_diff <= 15:
                    score += 2
            
            # BMI matching (within 2 points gets points)
            entry_bmi = self._safe_float(entry.get("BMI", ""))
            if user_bmi and entry_bmi:
                bmi_diff = abs(user_bmi - entry_bmi)
                if bmi_diff <= 1:
                    score += 10
                elif bmi_diff <= 2:
                    score += 5
                elif bmi_diff <= 3:
                    score += 2
            
            # Disease type matching (exact match gets high score)
            entry_disease = entry.get("Disease_Type", "")
            if entry_disease == disease_type:
                score += 15
            elif disease_type == "None" and entry_disease == "None":
                score += 10
            
            # Activity level matching
            entry_activity = entry.get("Physical_Activity_Level", "")
            if entry_activity == activity:
                score += 10
            elif entry_activity.lower() == activity.lower():
                score += 8
            
            # Dietary restrictions matching
            entry_restrictions = entry.get("Dietary_Restrictions", "")
            if entry_restrictions == dietary_restrictions:
                score += 8
            elif dietary_restrictions != "None" and entry_restrictions != "None":
                # Partial match
                user_restrictions = set(dietary_restrictions.split(","))
                entry_restrictions_set = set(entry_restrictions.split(","))
                if user_restrictions.intersection(entry_restrictions_set):
                    score += 5
            
            # Allergies matching (avoid entries with user's allergies)
            entry_allergies = entry.get("Allergies", "")
            if allergies != "None" and entry_allergies != "None":
                user_allergy_list = [a.strip().lower() for a in allergies.split(",")]
                entry_allergy_list = [a.strip().lower() for a in entry_allergies.split(",")]
                if any(allergy in entry_allergy_list for allergy in user_allergy_list):
                    score = -100  # Strong penalty - don't recommend
            
            # Preferred cuisine matching
            entry_cuisine = entry.get("Preferred_Cuisine", "")
            if entry_cuisine.lower() == preferred_cuisine.lower():
                score += 5
            
            # Gender matching (optional, but can help)
            entry_gender = entry.get("Gender", "")
            if user.gender and entry_gender:
                if user.gender.lower() == entry_gender.lower():
                    score += 3
            
            if score > 0:
                # Get daily caloric intake from dataset
                daily_calories = self._safe_float(entry.get("Daily_Caloric_Intake", ""))
                if not daily_calories:
                    daily_calories = 2000  # Default
                
                # Calculate meal calories based on meal type
                meal_calorie_ratios = {
                    "breakfast": 0.25,
                    "lunch": 0.35,
                    "dinner": 0.30,
                    "snack": 0.10,
                }
                meal_calories = daily_calories * meal_calorie_ratios.get(meal_type, 0.25)
                
                # Get diet recommendation
                diet_recommendation = entry.get("Diet_Recommendation", "Balanced")
                
                scored_matches.append({
                    "score": score,
                    "name": self._generate_meal_name(meal_type, diet_recommendation, entry_cuisine or preferred_cuisine, entry_disease),
                    "calories": round(meal_calories),
                    "daily_calories": round(daily_calories),
                    "diet_recommendation": diet_recommendation,
                    "disease_type": entry_disease,
                    "activity": entry_activity,
                    "restrictions": entry_restrictions,
                    "cuisine": entry_cuisine or preferred_cuisine,
                    "tags": self._generate_tags(diet_recommendation, entry_disease, entry_restrictions),
                })
        
        # Sort by score and return top matches
        scored_matches.sort(key=lambda x: x["score"], reverse=True)
        return scored_matches[:10]  # Return top 10 matches
    
    def _find_matches_simple(self, user: User, meal_type: str) -> List[Dict]:
        """Fallback to simple dataset matching (original method)."""
        # Get user attributes
        age_group = self._get_age_group(user.age)
        goal = self._normalize_goal(user.health_goal)
        bmi_range = self._get_bmi_range(user)
        activity = self._normalize_activity(user.activity_level)
        
        # Find matching entries
        matches = []
        for entry in self.dataset:
            if (entry.get("Age_Group") == age_group and
                entry.get("Goal") == goal and
                entry.get("BMI_Range") == bmi_range and
                entry.get("Activity_Level") == activity):
                
                # Extract meal based on meal_type
                meal_name = None
                if meal_type == "breakfast":
                    meal_name = entry.get("Breakfast", "")
                elif meal_type == "lunch":
                    meal_name = entry.get("Lunch", "")
                elif meal_type in ["dinner", "snack"]:
                    meal_name = entry.get("Lunch", "") or entry.get("Breakfast", "")
                
                if meal_name:
                    matches.append({
                        "name": meal_name,
                        "calories": int(entry.get("Calories", 500)),
                        "tags": entry.get("Tags", "").split(", ") if entry.get("Tags") else [],
                    })
        
        return matches
    
    def _get_age_group(self, age: Optional[int]) -> str:
        """Determine age group from user age (for simple dataset)."""
        if not age:
            return "26-35"
        if age < 26:
            return "18-25"
        elif age < 36:
            return "26-35"
        elif age < 51:
            return "36-50"
        else:
            return "50+"
    
    def _get_bmi_range(self, user: User) -> str:
        """Calculate BMI and determine range (for simple dataset)."""
        if not user.height or not user.weight:
            return "20-25"
        height_m = user.height / 100
        bmi = user.weight / (height_m ** 2)
        if bmi < 18:
            return "18-22"
        elif bmi < 23:
            return "18-23"
        elif bmi < 26:
            return "20-25"
        elif bmi < 28:
            return "25-30"
        elif bmi < 33:
            return "25-32"
        elif bmi < 36:
            return "27-35"
        else:
            return "27-36"
    
    def _normalize_goal(self, goal: Optional[str]) -> str:
        """Normalize health goal (for simple dataset)."""
        if not goal:
            return "Weight Loss"
        goal_lower = goal.lower()
        if "weight_loss" in goal_lower or "weight loss" in goal_lower:
            return "Weight Loss"
        elif "muscle_gain" in goal_lower or "muscle gain" in goal_lower:
            return "Muscle Gain"
        elif "weight_gain" in goal_lower or "weight gain" in goal_lower:
            return "Weight Gain"
        elif "diabetes" in goal_lower:
            return "Diabetes"
        else:
            return "Weight Loss"
    
    def _safe_int(self, value: str) -> Optional[int]:
        """Safely convert string to int."""
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return None
    
    def _safe_float(self, value: str) -> Optional[float]:
        """Safely convert string to float."""
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    
    def _generate_meal_name(self, meal_type: str, diet_recommendation: str, cuisine: str, disease_type: str = None) -> str:
        """Generate meal name based on meal type, diet recommendation, and cuisine."""
        # Base meal names by cuisine and meal type
        cuisine_meals = {
            "Indian": {
                "breakfast": ["Poha", "Upma", "Dosa", "Idli", "Paratha", "Poha with vegetables", "Vegetable upma"],
                "lunch": ["Dal rice", "Vegetable curry with roti", "Rajma rice", "Chana masala", "Palak paneer", "Mixed vegetable curry"],
                "dinner": ["Dal tadka with rice", "Vegetable biryani", "Paneer curry", "Lentil soup", "Vegetable pulao"],
                "snack": ["Fruit", "Nuts", "Yogurt", "Roasted chickpeas", "Vegetable salad"]
            },
            "Chinese": {
                "breakfast": ["Steamed buns", "Congee", "Scrambled eggs", "Vegetable soup", "Rice porridge"],
                "lunch": ["Stir-fried vegetables", "Tofu curry", "Vegetable noodles", "Steamed rice with vegetables", "Hot and sour soup"],
                "dinner": ["Vegetable fried rice", "Steamed vegetables", "Tofu stir-fry", "Mixed vegetable curry", "Clear soup"],
                "snack": ["Fruit", "Steamed dumplings", "Vegetable spring rolls", "Nuts"]
            },
            "Mexican": {
                "breakfast": ["Scrambled eggs", "Avocado toast", "Breakfast burrito", "Fruit bowl", "Oatmeal"],
                "lunch": ["Bean burrito", "Vegetable fajitas", "Rice and beans", "Guacamole with vegetables", "Vegetable quesadilla"],
                "dinner": ["Vegetable tacos", "Bean soup", "Rice bowl", "Vegetable enchiladas", "Grilled vegetables"],
                "snack": ["Fruit", "Nuts", "Vegetable sticks", "Hummus"]
            },
            "Italian": {
                "breakfast": ["Oatmeal", "Fruit bowl", "Yogurt", "Whole grain toast", "Scrambled eggs"],
                "lunch": ["Pasta with vegetables", "Minestrone soup", "Caprese salad", "Risotto", "Vegetable pizza"],
                "dinner": ["Pasta primavera", "Vegetable lasagna", "Grilled vegetables", "Risotto", "Vegetable soup"],
                "snack": ["Fruit", "Nuts", "Olives", "Cheese"]
            }
        }
        
        # Get base meal options
        meal_options = cuisine_meals.get(cuisine, {}).get(meal_type, [f"{cuisine} {meal_type}"])
        
        # Select meal based on diet recommendation
        if diet_recommendation == "Low_Carb":
            # Prefer protein-rich, low-carb options
            if meal_type == "breakfast":
                return f"Protein-rich {meal_options[0] if meal_options else 'breakfast'}"
            elif meal_type == "lunch":
                return f"Low-carb {meal_options[1] if len(meal_options) > 1 else meal_options[0] if meal_options else 'lunch'}"
            else:
                return f"Low-carb {meal_options[0] if meal_options else meal_type}"
        elif diet_recommendation == "Low_Sodium":
            return f"Low-sodium {meal_options[0] if meal_options else meal_type}"
        else:
            # Balanced diet
            meal_name = meal_options[0] if meal_options else f"{cuisine} {meal_type}"
            if disease_type and disease_type != "None":
                return f"{disease_type}-friendly {meal_name}"
            return meal_name
    
    def _generate_tags(self, diet_recommendation: str, disease_type: str, restrictions: str) -> List[str]:
        """Generate tags based on diet recommendation and restrictions."""
        tags = []
        
        if diet_recommendation:
            tags.append(diet_recommendation.lower().replace("_", "-"))
        
        if disease_type and disease_type != "None":
            tags.append(disease_type.lower())
        
        if restrictions and restrictions != "None":
            for restriction in restrictions.split(","):
                tags.append(restriction.strip().lower().replace("_", "-"))
        
        return tags
    
    def get_all_meals_for_user(self, user: User) -> Dict[str, List[Dict]]:
        """Get all meal recommendations for a user across all meal types."""
        result = {
            "breakfast": self.find_matching_meals(user, "breakfast"),
            "lunch": self.find_matching_meals(user, "lunch"),
            "dinner": self.find_matching_meals(user, "dinner"),
            "snack": self.find_matching_meals(user, "snack"),
        }
        return result

