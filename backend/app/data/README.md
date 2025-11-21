# Meal Plan Dataset

This directory contains the meal plan dataset used for personalized meal recommendations.

## Dataset File

- **meal_plan_dataset.csv**: Contains 40+ meal plan entries with:
  - Age groups (18-25, 26-35, 36-50, 50+)
  - Health goals (Weight Loss, Weight Gain, Muscle Gain, Diabetes)
  - BMI ranges
  - Activity levels (Low, Medium, High)
  - Breakfast and lunch recommendations
  - Calorie counts
  - Nutritional tags

## Dataset Structure

| Column | Description |
|--------|-------------|
| Age_Group | User age range (18-25, 26-35, 36-50, 50+) |
| Goal | Health goal (Weight Loss, Weight Gain, Muscle Gain, Diabetes) |
| BMI_Range | BMI category (18-22, 20-25, 25-30, etc.) |
| Activity_Level | Physical activity level (Low, Medium, High) |
| Breakfast | Breakfast meal recommendation |
| Lunch | Lunch meal recommendation |
| Calories | Total calories for the meal |
| Tags | Nutritional tags (comma-separated) |

## Usage

The dataset is automatically loaded by the `MealPlanDatasetLoader` class and used by the `RecommendationEngine` to provide personalized meal recommendations based on:

1. **User Age** → Maps to age group
2. **User BMI** → Calculated from height/weight, mapped to BMI range
3. **Health Goal** → User's health goal (weight_loss, muscle_gain, etc.)
4. **Activity Level** → User's activity level (sedentary, moderately_active, etc.)

## How It Works

1. When a user requests meal recommendations, the system:
   - Calculates user's age group from their age
   - Calculates user's BMI from height/weight
   - Normalizes their health goal and activity level
   - Searches the dataset for matching entries
   - Returns personalized meal recommendations

2. If no exact match is found, the system falls back to the default food database.

## Example

For a user with:
- Age: 28 (→ Age Group: 26-35)
- Height: 175 cm, Weight: 80 kg (→ BMI: 26.1 → BMI Range: 25-32)
- Goal: weight_loss
- Activity: moderately_active (→ Activity Level: Medium)

The system will find matching entries from the dataset and recommend meals like:
- Breakfast: "Fruit + yogurt" (530 calories)
- Lunch: "Grilled salmon bowl" (530 calories)

## Adding More Data

To add more meal plan entries:

1. Edit `meal_plan_dataset.csv`
2. Add new rows following the same format
3. Restart the backend server
4. The new entries will be automatically loaded

## Tags

Common tags used in the dataset:
- `low-carb`, `high-protein`
- `fiber-rich`
- `high-calorie`
- `muscle-gain`
- `low-GI`
- `diabetes-friendly`
- `heart-healthy`
- `vegetarian`
- `omega-3`
- `lean protein`
- `gym diet`
- `bulk-up`
- `easy-to-digest`
- `elder-friendly`

These tags help the system estimate nutritional values when exact macros aren't available.

