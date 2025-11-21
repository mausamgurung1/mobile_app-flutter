# Comprehensive Diet Recommendations Dataset Integration

The meal plan recommendation system now uses the comprehensive `diet_recommendations_dataset.csv` with 1000+ patient records.

## ✅ What Changed

1. **Dataset Loader Updated** (`app/data/dataset_loader.py`)
   - Automatically detects and loads the comprehensive dataset
   - Uses intelligent scoring system to match users to dataset entries
   - Considers multiple factors: Age, BMI, Disease Type, Activity Level, Dietary Restrictions, Allergies, Preferred Cuisine

2. **Smart Matching Algorithm**
   - Scores each dataset entry based on similarity to user profile
   - Considers:
     - **Age** (within 5 years = high score, 10 years = medium, 15 years = low)
     - **BMI** (within 1 point = high score, 2 points = medium, 3 points = low)
     - **Disease Type** (exact match = high score)
     - **Activity Level** (exact match = high score)
     - **Dietary Restrictions** (exact match = high score)
     - **Allergies** (strong penalty if entry contains user's allergies)
     - **Preferred Cuisine** (bonus points for matching)
     - **Gender** (small bonus for matching)

3. **Meal Plan Generation**
   - Uses `Daily_Caloric_Intake` from matching dataset entries
   - Calculates meal-specific calories based on meal type:
     - Breakfast: 25% of daily calories
     - Lunch: 35% of daily calories
     - Dinner: 30% of daily calories
     - Snack: 10% of daily calories
   - Applies `Diet_Recommendation` (Balanced, Low_Carb, Low_Sodium) to meal nutrition

## 🎯 How It Works

### User Profile Mapping

The system maps user attributes to dataset criteria:

**Disease Type:**
- `diabetes_management` → "Diabetes"
- `weight_loss` → "Obesity"
- `hypertension` or `blood_pressure` → "Hypertension"
- Other → "None"

**Activity Level:**
- `sedentary` → "Sedentary"
- `lightly_active`, `moderately_active` → "Moderate"
- `very_active`, `extremely_active` → "Active"

**Dietary Restrictions:**
- Automatically inferred from health goal:
  - Diabetes → Low_Sugar
  - Hypertension → Low_Sodium

**Allergies:**
- Directly from user profile
- Entries with matching allergies are excluded

**Preferred Cuisine:**
- Extracted from food_preferences
- Defaults to "Indian" if not specified

### Matching Process

1. **Calculate User Attributes:**
   - BMI from height/weight
   - Disease type from health goal
   - Activity level normalization
   - Dietary restrictions inference
   - Allergies extraction
   - Preferred cuisine detection

2. **Score Dataset Entries:**
   - Each entry gets a similarity score
   - Higher score = better match
   - Negative scores for incompatible entries (allergies)

3. **Select Top Matches:**
   - Sort by score (highest first)
   - Return top 10 matches
   - Use their `Daily_Caloric_Intake` and `Diet_Recommendation`

4. **Generate Meals:**
   - Create meal names based on cuisine and diet type
   - Calculate meal calories from daily intake
   - Estimate nutrition based on diet recommendation

## 📊 Dataset Features Used

| Dataset Column | How It's Used |
|----------------|---------------|
| Age | Matched within ±15 years (closer = higher score) |
| Gender | Small bonus for matching gender |
| Weight_kg, Height_cm, BMI | BMI calculated and matched within ±3 points |
| Disease_Type | Exact match gets high score |
| Physical_Activity_Level | Exact match gets high score |
| Daily_Caloric_Intake | Used to calculate meal-specific calories |
| Dietary_Restrictions | Matched with user's inferred restrictions |
| Allergies | Used to exclude incompatible entries |
| Preferred_Cuisine | Bonus points for matching cuisine |
| Diet_Recommendation | Applied to meal nutrition calculations |

## 🍽️ Meal Generation

Meals are generated based on:
- **Cuisine** (Indian, Chinese, Mexican, Italian)
- **Diet Recommendation** (Balanced, Low_Carb, Low_Sodium)
- **Disease Type** (for disease-specific naming)
- **Meal Type** (breakfast, lunch, dinner, snack)

Example meal names:
- "Low-carb Indian lunch" (for diabetes, Low_Carb diet)
- "Low-sodium Chinese breakfast" (for hypertension, Low_Sodium diet)
- "Balanced Mexican dinner" (for general health, Balanced diet)

## 📈 Benefits

1. **Personalized Recommendations**: Based on 1000+ real patient profiles
2. **Accurate Calorie Calculation**: Uses actual daily caloric intake from similar profiles
3. **Disease-Specific**: Considers disease type (Diabetes, Obesity, Hypertension)
4. **Allergy-Aware**: Automatically excludes meals with user's allergies
5. **Cuisine Preferences**: Respects user's preferred cuisine
6. **Activity-Aware**: Adjusts for user's activity level
7. **Restriction-Compliant**: Matches dietary restrictions automatically

## 🔍 Example

**User Profile:**
- Age: 45
- Gender: Female
- Height: 165 cm
- Weight: 75 kg
- BMI: 27.5
- Goal: diabetes_management
- Activity: moderately_active
- Allergies: Peanuts
- Food Preferences: Indian

**System Processing:**
1. Calculates BMI: 27.5
2. Maps to Disease_Type: "Diabetes"
3. Maps to Activity: "Moderate"
4. Infers Restrictions: "Low_Sugar"
5. Finds matching entries in dataset
6. Scores entries (e.g., P0002, P0005, P0012, etc.)
7. Selects top matches with Low_Carb diet recommendation
8. Generates meals like:
   - "Low-carb Indian breakfast" (530 calories)
   - "Low-carb Indian lunch" (750 calories)
   - "Diabetes-friendly Indian dinner" (650 calories)

## 🚀 Usage

No code changes needed! The system automatically:
- Detects the comprehensive dataset
- Uses it for all meal plan generation
- Falls back to simple dataset if comprehensive dataset not found

## 📝 Notes

- The comprehensive dataset doesn't have specific meal names, so the system generates appropriate meal names based on cuisine, diet type, and disease
- Meal calories are calculated from the `Daily_Caloric_Intake` field in matching entries
- Nutrition values are estimated based on the `Diet_Recommendation` type
- The system prioritizes safety by excluding entries with user's allergies

## 🔧 Future Enhancements

Potential improvements:
- Add specific meal recipes based on cuisine and diet type
- Use actual nutrition data from external APIs
- Machine learning model training on the dataset
- More sophisticated scoring algorithm
- Consider severity and other health metrics

