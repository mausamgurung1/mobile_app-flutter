# Setup Instructions - Nutrition App

## ⚠️ IMPORTANT: Disk Space Issue

Your disk is **100% full** (437GB used out of 460GB). You need to free up space before proceeding.

### Free Up Disk Space

1. **Clean Flutter cache:**
   ```bash
   flutter clean
   rm -rf ~/.pub-cache
   ```

2. **Clean pip cache:**
   ```bash
   pip cache purge
   ```

3. **Clean system caches:**
   ```bash
   # macOS
   sudo rm -rf ~/Library/Caches/*
   ```

4. **Remove unused files:**
   - Empty Trash
   - Delete old downloads
   - Remove unused applications
   - Clear browser caches

**Target:** Free up at least 5-10GB before proceeding.

---

## Step-by-Step Setup

### 1. Backend Setup

#### Navigate to backend
```bash
cd ~/Desktop/flutter\ /backend
```

#### Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Create .env file
```bash
cat > .env << 'EOF'
DATABASE_URL=sqlite:///./nutrition.db
SECRET_KEY=your-secret-key-change-this-in-production-min-32-chars-long-please
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
EOF
```

#### Start the server
```bash
source venv/bin/activate
uvicorn main:app --reload
```

**Backend will run at:** http://localhost:8000
**API Docs:** http://localhost:8000/docs

---

### 2. Flutter App Setup

#### Navigate to mobile_app
```bash
cd ~/Desktop/flutter\ /mobile_app
```

#### Install dependencies
```bash
flutter pub get
```

#### Run the app
```bash
# List available devices
flutter devices

# Run on macOS desktop
flutter run -d macos

# Run on Chrome (web)
flutter run -d chrome

# Run on iOS Simulator (if available)
flutter run -d ios

# Run on Android Emulator (if available)
flutter run -d android
```

---

## Quick Commands

### Terminal 1 - Backend
```bash
cd ~/Desktop/flutter\ /backend
source venv/bin/activate
uvicorn main:app --reload
```

### Terminal 2 - Flutter App
```bash
cd ~/Desktop/flutter\ /mobile_app
flutter run -d macos  # or chrome, ios, android
```

---

## Configuration for Physical Devices

If running on a physical Android/iOS device, update the API URL:

1. Find your computer's IP address:
   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1
   # Or
   ipconfig getifaddr en0
   ```

2. Update `mobile_app/lib/config/api_config.dart`:
   ```dart
   static const String baseUrl = 'http://YOUR_IP_ADDRESS:8000/api/v1';
   ```

   Example:
   ```dart
   static const String baseUrl = 'http://192.168.1.100:8000/api/v1';
   ```

---

## Testing the Application

1. **Start Backend:**
   - Terminal 1: Run `uvicorn main:app --reload`
   - Visit http://localhost:8000/docs to see API documentation

2. **Start Flutter App:**
   - Terminal 2: Run `flutter run -d macos` (or your preferred device)

3. **Test Flow:**
   - Register a new account
   - Login
   - Complete your profile
   - Explore the dashboard
   - Log meals
   - View nutrition tracking

---

## Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
lsof -ti:8000 | xargs kill -9
```

**Database errors:**
- SQLite database will be created automatically
- Check file permissions in backend directory

**Import errors:**
- Ensure virtual environment is activated
- Reinstall: `pip install -r requirements.txt --force-reinstall`

### Flutter Issues

**Dependency conflicts:**
- Already fixed in pubspec.yaml (intl and form_builder_validators updated)

**Build errors:**
```bash
flutter clean
flutter pub get
flutter run
```

**No devices:**
- Start emulator/simulator
- Check `flutter doctor` for setup issues

**API connection:**
- Ensure backend is running
- Check API URL in `api_config.dart`
- For physical devices, use IP address not localhost

---

## Project Structure

```
flutter/
├── backend/              # Python FastAPI backend
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── models/      # Database models
│   │   ├── schemas/     # Pydantic schemas
│   │   └── services/    # Business logic
│   ├── main.py          # FastAPI entry point
│   └── requirements.txt # Python dependencies
│
├── mobile_app/          # Flutter mobile app
│   ├── lib/
│   │   ├── screens/     # UI screens
│   │   ├── widgets/     # Reusable widgets
│   │   ├── services/    # API services
│   │   └── models/      # Data models
│   └── pubspec.yaml     # Flutter dependencies
│
└── README.md            # Project documentation
```

---

## Next Steps After Setup

1. ✅ Free up disk space (5-10GB minimum)
2. ✅ Install backend dependencies
3. ✅ Create .env file
4. ✅ Start backend server
5. ✅ Install Flutter dependencies
6. ✅ Run Flutter app
7. ✅ Test registration and login
8. ✅ Complete user profile
9. ✅ Test meal logging
10. ✅ Explore dashboard features

---

## Support

- **Backend API Docs:** http://localhost:8000/docs
- **Backend ReDoc:** http://localhost:8000/redoc
- **Flutter Docs:** https://flutter.dev/docs

Good luck! 🚀

