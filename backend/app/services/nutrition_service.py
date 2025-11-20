import httpx
import os
from dotenv import load_dotenv
from typing import Optional, Dict

load_dotenv()

class NutritionService:
    def __init__(self):
        self.nutritionix_app_id = os.getenv("NUTRITIONIX_APP_ID")
        self.nutritionix_api_key = os.getenv("NUTRITIONIX_API_KEY")
        self.nutritionix_base_url = os.getenv("NUTRITIONIX_BASE_URL", "https://trackapi.nutritionix.com/v2")
        
        self.edamam_app_id = os.getenv("EDAMAM_APP_ID")
        self.edamam_api_key = os.getenv("EDAMAM_API_KEY")
        self.edamam_base_url = os.getenv("EDAMAM_BASE_URL", "https://api.edamam.com/api")
        
        self.usda_api_key = os.getenv("USDA_API_KEY")
        self.usda_base_url = os.getenv("USDA_BASE_URL", "https://api.nal.usda.gov/fdc/v1")

    async def get_nutrition_info(self, food_name: str, quantity: float = 100.0) -> Optional[Dict]:
        """
        Get nutrition information for a food item.
        Tries Nutritionix first, then Edamam, then USDA as fallback.
        """
        # Try Nutritionix first
        nutrition = await self._get_nutritionix_info(food_name, quantity)
        if nutrition:
            return nutrition
        
        # Try Edamam
        nutrition = await self._get_edamam_info(food_name, quantity)
        if nutrition:
            return nutrition
        
        # Try USDA as last resort
        nutrition = await self._get_usda_info(food_name, quantity)
        return nutrition

    async def _get_nutritionix_info(self, food_name: str, quantity: float) -> Optional[Dict]:
        """Get nutrition info from Nutritionix API"""
        if not self.nutritionix_app_id or not self.nutritionix_api_key:
            return None
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.nutritionix_base_url}/natural/nutrients",
                    headers={
                        "x-app-id": self.nutritionix_app_id,
                        "x-app-key": self.nutritionix_api_key,
                        "Content-Type": "application/json",
                    },
                    json={
                        "query": f"{quantity}g {food_name}",
                    },
                    timeout=10.0,
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if "foods" in data and len(data["foods"]) > 0:
                        food = data["foods"][0]
                        return {
                            "calories": food.get("nf_calories", 0),
                            "protein": food.get("nf_protein", 0),
                            "carbohydrates": food.get("nf_total_carbohydrate", 0),
                            "fat": food.get("nf_total_fat", 0),
                            "fiber": food.get("nf_dietary_fiber", 0),
                            "sugar": food.get("nf_sugars"),
                            "sodium": food.get("nf_sodium"),
                        }
        except Exception as e:
            print(f"Nutritionix API error: {e}")
        
        return None

    async def _get_edamam_info(self, food_name: str, quantity: float) -> Optional[Dict]:
        """Get nutrition info from Edamam API"""
        if not self.edamam_app_id or not self.edamam_api_key:
            return None
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.edamam_base_url}/food-database/v2/parser",
                    params={
                        "ingr": f"{quantity}g {food_name}",
                        "app_id": self.edamam_app_id,
                        "app_key": self.edamam_api_key,
                    },
                    timeout=10.0,
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if "parsed" in data and len(data["parsed"]) > 0:
                        food = data["parsed"][0]["food"]
                        nutrients = food.get("nutrients", {})
                        return {
                            "calories": nutrients.get("ENERC_KCAL", {}).get("quantity", 0),
                            "protein": nutrients.get("PROCNT", {}).get("quantity", 0),
                            "carbohydrates": nutrients.get("CHOCDF", {}).get("quantity", 0),
                            "fat": nutrients.get("FAT", {}).get("quantity", 0),
                            "fiber": nutrients.get("FIBTG", {}).get("quantity", 0),
                            "sugar": nutrients.get("SUGAR", {}).get("quantity"),
                            "sodium": nutrients.get("NA", {}).get("quantity"),
                        }
        except Exception as e:
            print(f"Edamam API error: {e}")
        
        return None

    async def _get_usda_info(self, food_name: str, quantity: float) -> Optional[Dict]:
        """Get nutrition info from USDA FoodData Central API"""
        if not self.usda_api_key:
            return None
        
        try:
            async with httpx.AsyncClient() as client:
                # Search for food
                search_response = await client.get(
                    f"{self.usda_base_url}/foods/search",
                    params={
                        "query": food_name,
                        "api_key": self.usda_api_key,
                        "pageSize": 1,
                    },
                    timeout=10.0,
                )
                
                if search_response.status_code == 200:
                    search_data = search_response.json()
                    if "foods" in search_data and len(search_data["foods"]) > 0:
                        food_id = search_data["foods"][0].get("fdcId")
                        
                        # Get detailed nutrition
                        detail_response = await client.get(
                            f"{self.usda_base_url}/food/{food_id}",
                            params={"api_key": self.usda_api_key},
                            timeout=10.0,
                        )
                        
                        if detail_response.status_code == 200:
                            detail_data = detail_response.json()
                            nutrients = {n["nutrient"]["name"]: n["amount"] for n in detail_data.get("foodNutrients", [])}
                            
                            # Scale by quantity (assuming USDA data is per 100g)
                            scale = quantity / 100.0
                            
                            return {
                                "calories": nutrients.get("Energy", 0) * scale,
                                "protein": nutrients.get("Protein", 0) * scale,
                                "carbohydrates": nutrients.get("Carbohydrate, by difference", 0) * scale,
                                "fat": nutrients.get("Total lipid (fat)", 0) * scale,
                                "fiber": nutrients.get("Fiber, total dietary", 0) * scale,
                                "sugar": nutrients.get("Sugars, total including NLEA", 0) * scale if "Sugars, total including NLEA" in nutrients else None,
                                "sodium": nutrients.get("Sodium, Na", 0) * scale,
                            }
        except Exception as e:
            print(f"USDA API error: {e}")
        
        return None

