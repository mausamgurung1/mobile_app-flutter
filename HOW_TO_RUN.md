# 🚀 How to Run Flutter App and Backend

This guide shows you how to run both the Flutter mobile app and the backend API server.

---

## 📋 Prerequisites

- Python 3.9+ installed
- Flutter SDK installed
- Android emulator or physical device
- Terminal access

---

## 🎯 Quick Start (Two Terminals)

### Terminal 1: Backend Server

Open a new terminal and run:

```bash
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Or use the startup script:**
```bash
"/home/mausamgr/flutter /start_backend.sh"
```

**What you'll see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Keep this terminal open!** The backend must stay running.

---

### Terminal 2: Flutter App

Open another terminal and run:

```bash
export PATH="/tmp:$PATH"
flutter devices
flutter run -d emulator-5554
```

**Or if you want Flutter to auto-select device:**
```bash
cd "/home/mausamgr/flutter /mobile_app"
export PATH="/tmp:$PATH"
flutter run
```

**What you'll see:**
- Building progress
- App launching on emulator
- Hot reload enabled (press `r` to reload)

---

## 🔧 Step-by-Step Instructions

### Step 1: Start Backend Server

1. **Open Terminal 1**
2. **Navigate to backend directory:**
   ```bash
   cd "/home/mausamgr/flutter /backend"
   ```

3. **Activate virtual environment:**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies (if needed):**
   ```bash
   pip install -r requirements.txt
   pip install email-validator
   ```

5. **Start the server:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

6. **Verify it's running:**
   - Open browser: http://localhost:8000/docs
   - Or check health: `curl http://localhost:8000/health`

---

### Step 2: Start Android Emulator (if not running)

1. **List available emulators:**
   ```bash
   flutter emulators
   ```

2. **Launch emulator:**
   ```bash
   flutter emulators --launch Medium_Phone_API_36.1
   ```

3. **Wait for emulator to boot** (about 20-30 seconds)

4. **Verify emulator is running:**
   ```bash
   flutter devices
   ```
   You should see: `sdk gphone64 x86 64 (mobile) • emulator-5554`

---

### Step 3: Start Flutter App

1. **Open Terminal 2** (keep Terminal 1 running backend)

2. **Navigate to Flutter app directory:**
   ```bash
   cd "/home/mausamgr/flutter /mobile_app"
   ```

3. **Add ninja to PATH** (required for Android builds):
   ```bash
   export PATH="/tmp:$PATH"
   ```

4. **Get dependencies:**
   ```bash
   flutter pub get
   ```

5. **Run the app:**
   ```bash
   flutter run -d emulator-5554
   ```

   **Or let Flutter auto-select:**
   ```bash
   flutter run
   ```

6. **Wait for build to complete** (first time may take 1-2 minutes)

---

## 📱 Running on Physical Android Device

1. **Enable USB Debugging** on your phone:
   - Settings → About Phone
   - Tap "Build Number" 7 times
   - Settings → Developer Options
   - Enable "USB Debugging"

2. **Connect phone via USB**

3. **Verify device is detected:**
   ```bash
   flutter devices
   ```

4. **Run the app:**
   ```bash
   cd "/home/mausamgr/flutter /mobile_app"
   export PATH="/tmp:$PATH"
   flutter run
   ```

---

## 🛠️ Useful Commands

### Backend Commands

**Check if backend is running:**
```bash
curl http://localhost:8000/health
```

**View backend logs:**
```bash
tail -f /tmp/backend.log
```

**Stop backend:**
```bash
pkill -f "uvicorn main:app"
```

**Restart backend:**
```bash
cd "/home/mausamgr/flutter /backend"
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

### Flutter Commands

**List available devices:**
```bash
flutter devices
```

**Check Flutter setup:**
```bash
flutter doctor
```

**Hot reload** (while app is running):
- Press `r` in the Flutter terminal

**Hot restart** (while app is running):
- Press `R` in the Flutter terminal

**Stop Flutter app:**
- Press `q` in the Flutter terminal

**Clean build:**
```bash
cd "/home/mausamgr/flutter /mobile_app"
flutter clean
flutter pub get
```

---

## 🌐 URLs and Endpoints

### Backend API
- **Base URL**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **API Base**: http://localhost:8000/api/v1

### Android Emulator Access
- **Backend from emulator**: http://10.0.2.2:8000
- (The app is configured to use this automatically)

---

## ✅ Verification Checklist

After starting both services, verify:

- [ ] Backend is running: `curl http://localhost:8000/health`
- [ ] Backend docs accessible: http://localhost:8000/docs
- [ ] Android emulator is running: `flutter devices`
- [ ] Flutter app is installed: `adb devices`
- [ ] App is visible on emulator screen
- [ ] Can register/login in the app

---

## 🐛 Troubleshooting

### Backend won't start
- Check if port 8000 is already in use: `lsof -i :8000`
- Verify virtual environment is activated
- Check `.env` file exists in backend directory
- Install missing dependencies: `pip install -r requirements.txt`

### Flutter app won't build
- Ensure ninja is in PATH: `export PATH="/tmp:$PATH"`
- Clean and rebuild: `flutter clean && flutter pub get`
- Check Android SDK is installed: `flutter doctor`

### Emulator not detected
- Wait longer for emulator to boot (30-60 seconds)
- Restart emulator: `flutter emulators --launch Medium_Phone_API_36.1`
- Check ADB: `adb devices`

### App can't connect to backend
- Verify backend is running: `curl http://localhost:8000/health`
- Check API config in app uses: `http://10.0.2.2:8000` (for emulator)
- For physical device, use your computer's IP address

---

## 📝 Quick Reference

### Start Both Services

**Terminal 1 - Backend:**
```bash
cd "/home/mausamgr/flutter /backend" && source venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Flutter:**
```bash
cd "/home/mausamgr/flutter /mobile_app" && export PATH="/tmp:$PATH" && flutter run -d emulator-5554
```

---

## 🎉 Success!

When both are running:
- ✅ Backend API: http://localhost:8000/docs
- ✅ Flutter App: Visible on Android emulator
- ✅ You can register/login and use all features!

---

**Need help?** Check the logs in each terminal for error messages.



flutter emulators --launch Medium_Phone_API_36.1
