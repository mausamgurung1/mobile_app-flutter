# Manual Start Instructions

## ⚠️ Disk Space Issue

Your disk is **100% full**. You MUST free up space before running the project.

### Quick Space Cleanup

```bash
# 1. Clean Flutter cache
cd ~/Desktop/flutter\ /mobile_app
flutter clean

# 2. Remove pub cache
rm -rf ~/.pub-cache

# 3. Clean pip cache
pip cache purge

# 4. Empty Trash
# (Do this manually from Finder)

# 5. Check space
df -h ~
```

**Target:** Free up at least **5-10GB** before proceeding.

---

## Option 1: Use the Start Script

```bash
cd ~/Desktop/flutter\ /
./START_PROJECT.sh
```

---

## Option 2: Manual Start (Two Terminals)

### Terminal 1 - Backend

```bash
# Navigate to backend
cd ~/Desktop/flutter\ /backend

# Activate virtual environment
source venv/bin/activate

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Start server
uvicorn main:app --reload
```

**Backend will be available at:**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

---

### Terminal 2 - Flutter App

```bash
# Navigate to mobile app
cd ~/Desktop/flutter\ /mobile_app

# Install dependencies (if not already installed)
flutter pub get

# Run the app
flutter run -d macos
# OR
flutter run -d chrome
# OR
flutter run -d ios
```

---

## Quick Commands Summary

### Backend Setup (One-time)
```bash
cd ~/Desktop/flutter\ /backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Backend Start (Every time)
```bash
cd ~/Desktop/flutter\ /backend
source venv/bin/activate
uvicorn main:app --reload
```

### Flutter Setup (One-time, after freeing space)
```bash
cd ~/Desktop/flutter\ /mobile_app
flutter pub get
```

### Flutter Start (Every time)
```bash
cd ~/Desktop/flutter\ /mobile_app
flutter run -d macos
```

---

## Troubleshooting

### "No space left on device"
- **MUST free up disk space first**
- Follow cleanup steps above
- Delete unused files, empty Trash
- Target: 5-10GB free space

### Backend won't start
```bash
# Check if port 8000 is in use
lsof -ti:8000 | xargs kill -9

# Check if dependencies are installed
cd ~/Desktop/flutter\ /backend
source venv/bin/activate
pip list | grep fastapi
```

### Flutter dependencies fail
```bash
# Clean and retry
cd ~/Desktop/flutter\ /mobile_app
flutter clean
flutter pub get
```

### API connection error in app
- Ensure backend is running on http://localhost:8000
- Check `mobile_app/lib/config/api_config.dart`
- For physical devices, use your computer's IP address

---

## Current Status

✅ Backend configuration: Ready (SQLite database)
✅ Flutter configuration: Ready (dependencies fixed)
✅ .env file: Created
❌ Dependencies: Need disk space to install
❌ Backend: Not started (dependencies not installed)
❌ Flutter: Not started (dependencies not installed)

---

## Next Steps

1. **FREE UP DISK SPACE** (5-10GB minimum)
2. Install backend dependencies: `pip install -r requirements.txt`
3. Install Flutter dependencies: `flutter pub get`
4. Start backend: `uvicorn main:app --reload`
5. Start Flutter: `flutter run -d macos`

Good luck! 🚀

