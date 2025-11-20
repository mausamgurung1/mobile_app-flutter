# Personalized Nutrition and Diet Management Platform

A comprehensive AI-powered mobile application for personalized nutrition guidance and diet management.

## Project Structure

```
.
├── mobile_app/          # Flutter mobile application
├── backend/             # Python FastAPI backend
└── README.md
```

## Features

- **Personalized Meal Plans**: AI-generated meal recommendations based on user profile
- **Health Data Tracking**: Track age, activity level, medical conditions, and health goals
- **Nutrition Analysis**: Real-time nutritional feedback using external APIs
- **User Profiles**: Comprehensive user profiles with preferences and goals
- **Progress Tracking**: Monitor diet adherence and health outcomes

## Tech Stack

### Frontend
- Flutter (Dart)
- Provider/Bloc for state management
- HTTP for API communication

### Backend
- Python 3.9+
- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- Scikit-learn for ML recommendations

### External APIs
- Nutritionix API
- Edamam API
- USDA FoodData Central

## Setup Instructions

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database and API keys
```

5. Run database migrations:
```bash
alembic upgrade head
```

6. Start the server:
```bash
uvicorn main:app --reload
```

### Flutter App Setup

1. Navigate to mobile_app directory:
```bash
cd mobile_app
```

2. Install dependencies:
```bash
flutter pub get
```

3. Update API base URL in `lib/config/api_config.dart`

4. Run the app:
```bash
flutter run
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Environment Variables

Create a `.env` file in the backend directory with:

```
DATABASE_URL=postgresql://user:password@localhost/nutrition_db
SECRET_KEY=your-secret-key-here
NUTRITIONIX_APP_ID=your-nutritionix-app-id
NUTRITIONIX_API_KEY=your-nutritionix-api-key
EDAMAM_APP_ID=your-edamam-app-id
EDAMAM_API_KEY=your-edamam-api-key
USDA_API_KEY=your-usda-api-key
```

## Key Features Implementation

### Backend (Python/FastAPI)
- ✅ User authentication with JWT tokens
- ✅ User profile management with health data
- ✅ Meal plan creation and tracking
- ✅ Nutrition analysis using multiple APIs (Nutritionix, Edamam, USDA)
- ✅ AI-powered meal recommendations based on user profile
- ✅ BMR and TDEE calculations
- ✅ Database models for users, meals, meal plans, and food items

### Frontend (Flutter)
- ✅ User authentication (login/register)
- ✅ Dashboard with health stats
- ✅ Profile management
- ✅ Meal plan viewing
- ✅ Nutrition tracking interface
- ✅ Modern Material Design 3 UI
- ✅ State management with Provider

## Development Notes

### API Response Format
The backend returns responses directly (not wrapped in a `data` field):
- Single objects: Direct JSON object
- Lists: Direct JSON array
- Errors: `{"detail": "error message"}`

### Database Schema
- **Users**: Store user profiles, health data, preferences, and goals
- **Meals**: Store individual meals with nutrition info
- **FoodItems**: Store individual food items within meals
- **MealPlans**: Store weekly/daily meal plans

### ML Recommendations
The recommendation engine uses:
- User's TDEE (Total Daily Energy Expenditure)
- Health goals (weight loss, muscle gain, etc.)
- Food preferences and allergies
- Activity level
- Meal-specific calorie targets

## Next Steps for Enhancement

1. **Enhanced ML Model**: Implement collaborative filtering or deep learning models
2. **Meal Logging**: Add ability to log meals with photos
3. **Progress Tracking**: Add charts and graphs for nutrition progress
4. **Notifications**: Add reminders for meals and water intake
5. **Social Features**: Share meal plans and progress
6. **Recipe Integration**: Add detailed recipes for recommended meals
7. **Barcode Scanner**: Scan food items for quick nutrition logging

## License

MIT License

# mobile_app-flutter
