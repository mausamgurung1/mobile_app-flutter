# How to Run the Nutrition App Project

## Prerequisites Check

Before running, ensure you have:
- Python 3.9+ installed
- Flutter SDK installed
- PostgreSQL database (optional - can use SQLite for testing)
- At least 2GB free disk space

## Step 1: Backend Setup

### 1.1 Navigate to backend directory
```bash
cd ~/Desktop/flutter\ /backend
```

### 1.2 Create and activate virtual environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

### 1.3 Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 1.4 Create .env file
Create a `.env` file in the backend directory with:
```env
# Database Configuration (using SQLite for simplicity)
DATABASE_URL=sqlite:///./nutrition.db

# JWT Configuration
SECRET_KEY=your-secret-key-change-this-in-production-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Optional: External API Keys (for nutrition data)
# NUTRITIONIX_APP_ID=your-nutritionix-app-id
# NUTRITIONIX_API_KEY=your-nutritionix-api-key
# EDAMAM_APP_ID=your-edamam-app-id
# EDAMAM_API_KEY=your-edamam-api-key
# USDA_API_KEY=your-usda-api-key
```

### 1.5 Update database.py for SQLite (if not using PostgreSQL)
If you want to use SQLite instead of PostgreSQL, update `backend/app/database.py`:
```python
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./nutrition.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
```

### 1.6 Run database migrations (if using Alembic)
```bash
# Initialize Alembic (if not already done)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

**OR** if using SQLite, the tables will be created automatically on first run.

### 1.7 Start the backend server
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Start the server
uvicorn main:app --reload

# Or use Python directly
python main.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Step 2: Flutter App Setup

### 2.1 Navigate to mobile_app directory
```bash
cd ~/Desktop/flutter\ /mobile_app
```

### 2.2 Install Flutter dependencies
```bash
flutter pub get
```

### 2.3 Update API Configuration (if needed)
The API base URL is already set to `http://localhost:8000/api/v1` in `lib/config/api_config.dart`.

**For Android Emulator**: Use `http://10.0.2.2:8000/api/v1`
**For iOS Simulator**: Use `http://localhost:8000/api/v1`
**For Physical Device**: Use your computer's IP address, e.g., `http://192.168.1.100:8000/api/v1`

### 2.4 Check available devices
```bash
flutter devices
```

### 2.5 Run the Flutter app
```bash
# Run on default device
flutter run

# Run on specific device
flutter run -d <device-id>

# Run in release mode (for better performance)
flutter run --release
```

## Step 3: Testing the Application

### 3.1 Test Backend API
1. Open http://localhost:8000/docs in your browser
2. Try the `/api/v1/auth/register` endpoint to create a user
3. Try the `/api/v1/auth/login` endpoint to login

### 3.2 Test Flutter App
1. Open the app on your device/emulator
2. Register a new account
3. Complete your profile with health information
4. Explore the dashboard and features

## Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn main:app --reload --port 8001
```

**Database connection error:**
- Check your `.env` file has correct DATABASE_URL
- Ensure PostgreSQL is running (if using PostgreSQL)
- For SQLite, ensure write permissions in the backend directory

**Import errors:**
- Make sure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

### Flutter Issues

**API connection error:**
- Ensure backend is running
- Check API URL in `api_config.dart`
- For physical device, use your computer's IP address instead of localhost
- Check firewall settings

**Build errors:**
```bash
# Clean and rebuild
flutter clean
flutter pub get
flutter run
```

**No devices found:**
- Start an Android emulator or iOS simulator
- Connect a physical device with USB debugging enabled
- Run `flutter doctor` to check Flutter setup

### Disk Space Issues

If you encounter "No space left on device":
```bash
# Check disk space
df -h

# Clean up pip cache
pip cache purge

# Clean up Flutter build cache
flutter clean
```

## Quick Start Commands

### Terminal 1 - Backend
```bash
cd ~/Desktop/flutter\ /backend
source venv/bin/activate
uvicorn main:app --reload
```

### Terminal 2 - Flutter App
```bash
cd ~/Desktop/flutter\ /mobile_app
flutter run
```

## API Endpoints Summary

- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user
- `GET /api/v1/users/profile` - Get user profile
- `PUT /api/v1/users/profile` - Update user profile
- `GET /api/v1/meal-plans` - Get meal plans
- `POST /api/v1/meal-plans` - Create meal plan
- `POST /api/v1/nutrition/analyze` - Analyze nutrition
- `GET /api/v1/recommendations?meal_type=breakfast` - Get recommendations

## Next Steps

1. Set up PostgreSQL database for production
2. Add nutrition API keys for real nutrition data
3. Configure push notifications
4. Set up CI/CD pipeline
5. Deploy backend to cloud (Heroku, AWS, etc.)
6. Build and publish Flutter app to app stores

