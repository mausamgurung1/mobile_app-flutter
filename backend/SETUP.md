# Backend Setup Guide

## Prerequisites

- Python 3.9 or higher
- PostgreSQL database
- pip (Python package manager)

## Installation Steps

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Database

1. Create a PostgreSQL database:
```sql
CREATE DATABASE nutrition_db;
```

2. Update the `.env` file with your database credentials:
```env
DATABASE_URL=postgresql://username:password@localhost/nutrition_db
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

Edit `.env` and add:
- Database connection string
- Secret key for JWT tokens
- API keys for Nutritionix, Edamam, and USDA (optional but recommended)

### 5. Run Database Migrations

```bash
# Initialize Alembic (if not already done)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 6. Start the Server

```bash
# Development mode with auto-reload
uvicorn main:app --reload

# Or use the Python script
python main.py
```

The API will be available at:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user info

### Users
- `GET /api/v1/users/profile` - Get user profile
- `PUT /api/v1/users/profile` - Update user profile

### Meal Plans
- `GET /api/v1/meal-plans` - Get user's meal plans
- `POST /api/v1/meal-plans` - Create new meal plan

### Nutrition
- `POST /api/v1/nutrition/analyze` - Analyze nutrition for food items

### Recommendations
- `GET /api/v1/recommendations?meal_type=breakfast` - Get meal recommendations

## Testing

You can test the API using the Swagger UI at http://localhost:8000/docs or using curl:

```bash
# Register a user
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123",
    "first_name": "Test",
    "last_name": "User"
  }'

# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123"
  }'
```

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check database credentials in `.env`
- Verify database exists

### Import Errors
- Make sure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Port Already in Use
- Change the port in `main.py` or use: `uvicorn main:app --port 8001`

