# Quick Start Guide

## ⚠️ Disk Space Warning
Your disk is nearly full (100% used). Please free up some space before installing dependencies.

## Quick Setup (After Freeing Disk Space)

### Backend (Terminal 1)
```bash
cd ~/Desktop/flutter\ /backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
DATABASE_URL=sqlite:///./nutrition.db
SECRET_KEY=your-secret-key-change-this-in-production-min-32-chars-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
EOF

# Start server
uvicorn main:app --reload
```

### Flutter App (Terminal 2)
```bash
cd ~/Desktop/flutter\ /mobile_app
flutter pub get
flutter run
```

## For Physical Devices

### Android
Update `mobile_app/lib/config/api_config.dart`:
```dart
static const String baseUrl = 'http://YOUR_COMPUTER_IP:8000/api/v1';
```

### iOS
Update `mobile_app/lib/config/api_config.dart`:
```dart
static const String baseUrl = 'http://YOUR_COMPUTER_IP:8000/api/v1';
```

Find your IP:
```bash
# macOS/Linux
ifconfig | grep "inet " | grep -v 127.0.0.1

# Or
ipconfig getifaddr en0
```

## Test the Setup

1. Backend should be running at http://localhost:8000/docs
2. Flutter app should launch on your device/emulator
3. Register a new account in the app
4. Complete your profile
5. Explore the dashboard!

See RUN_PROJECT.md for detailed instructions.

