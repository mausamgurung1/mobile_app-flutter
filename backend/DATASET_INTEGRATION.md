# Meal Plan Dataset Integration

The meal plan recommendation system now uses a comprehensive dataset with 40+ entries based on age, BMI, health goals, and activity levels.

## ✅ What Was Added

1. **Dataset File** (`app/data/meal_plan_dataset.csv`)
   - 40+ meal plan entries
   - Covers all age groups, goals, BMI ranges, and activity levels
   - Includes breakfast and lunch recommendations

2. **Dataset Loader** (`app/data/dataset_loader.py`)
   - Loads and parses the CSV dataset
   - Maps user attributes to dataset entries
   - Finds matching meals based on user profile

3. **Updated Recommendation Engine** (`app/ml/recommendation_engine.py`)
   - Uses dataset for primary recommendations
   - Falls back to default food database if no matches
   - Estimates nutrition values from meal names and tags

## 🎯 How It Works

### User Profile Mapping

The system automatically maps user attributes to dataset criteria:

**Age Groups:**
- < 26 → "18-25"
- 26-35 → "26-35"
- 36-50 → "36-50"
- 50+ → "50+"

**BMI Calculation:**
- Calculated from user's height and weight
- Mapped to appropriate BMI range in dataset

**Goal Normalization:**
- `weight_loss` → "Weight Loss"
- `muscle_gain` → "Muscle Gain"
- `weight_gain` → "Weight Gain"
- `diabetes_management` → "Diabetes"

**Activity Level:**
- `sedentary`, `lightly_active` → "Low"
- `moderately_active` → "Medium"
- `very_active`, `extremely_active` → "High"

### Recommendation Process

1. User requests meal recommendations
2. System calculates user's age group, BMI range, goal, and activity level
3. Searches dataset for matching entries
4. Returns personalized meals from dataset
5. If no matches, falls back to default food database

## 📊 Dataset Coverage

The dataset includes:

- **4 Age Groups**: 18-25, 26-35, 36-50, 50+
- **4 Health Goals**: Weight Loss, Weight Gain, Muscle Gain, Diabetes
- **Multiple BMI Ranges**: 18-22, 20-25, 25-30, 25-32, 27-35, 27-36
- **3 Activity Levels**: Low, Medium, High
- **2 Meal Types**: Breakfast, Lunch (dinner/snack use lunch as reference)

## 🔧 Usage

No code changes needed! The dataset is automatically used when:
- Users generate meal plans
- Users request meal recommendations
- The recommendation API is called

## 📝 Example

**User Profile:**
- Age: 28
- Height: 175 cm
- Weight: 80 kg
- Goal: weight_loss
- Activity: moderately_active

**System Processing:**
1. Age Group: 26-35
2. BMI: 26.1 → Range: 25-32
3. Goal: Weight Loss
4. Activity: Medium

**Dataset Match:**
- Breakfast: "Fruit + yogurt" (530 calories, omega-3)
- Lunch: "Grilled salmon bowl" (530 calories, omega-3)

## 🚀 Benefits

1. **Personalized Recommendations**: Based on actual user profile data
2. **Age-Appropriate Meals**: Different recommendations for different age groups
3. **Goal-Specific**: Tailored to user's health goals
4. **Activity-Aware**: Adjusts for user's activity level
5. **BMI-Conscious**: Considers user's body composition

## 📈 Future Enhancements

Potential improvements:
- Add more dataset entries for better coverage
- Include dinner and snack recommendations
- Add more detailed nutrition information
- Support for more dietary restrictions
- Machine learning model training on the dataset

## 🔍 Testing

To test the dataset integration:

1. Create a user account with complete profile
2. Generate a meal plan
3. Check that recommendations match your profile
4. Verify meals are appropriate for your age, goal, and activity level

The system will automatically use the dataset for recommendations!

