# Running Backend in Separate Terminal

## 🎯 Setup: Two Terminals

For the app to fetch data properly, you need **TWO terminals**:

### Terminal 1: Backend API Server

**Purpose**: Runs the backend API that serves data to the Flutter app

**Commands:**
```bash
cd ~/Desktop/flutter\ /backend
source venv/bin/activate
uvicorn main:app --reload
```

**Or use the script:**
```bash
cd ~/Desktop/flutter\ /
./RUN_BACKEND.sh
```

**What you'll see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Keep this terminal open!** The backend must stay running.

---

### Terminal 2: Flutter App

**Purpose**: Runs the Flutter app on iPhone 16 Pro Max simulator

**Commands:**
```bash
cd ~/Desktop/flutter\ /mobile_app
flutter run -d "iPhone 16 Pro Max"
```

**What you'll see:**
- Compilation progress
- App launching on simulator
- Hot reload messages

---

## ✅ Current Status

**Backend**: Should be running in background
- URL: http://localhost:8000
- Docs: http://localhost:8000/docs

**Flutter App**: Should be launching on simulator

---

## 🔍 Verify Backend is Running

Check if backend is accessible:
```bash
curl http://localhost:8000/health
```

Should return: `{"status":"healthy"}`

---

## 🚀 Quick Start (Two Terminals)

### Terminal 1 - Backend:
```bash
cd ~/Desktop/flutter\ /backend
source venv/bin/activate
uvicorn main:app --reload
```

### Terminal 2 - Flutter:
```bash
cd ~/Desktop/flutter\ /mobile_app
flutter run -d "iPhone 16 Pro Max"
```

---

## 📊 How They Work Together

```
Terminal 1 (Backend)          Terminal 2 (Flutter App)
     │                              │
     │  Running API Server          │  Running App
     │  Port 8000                  │  Simulator
     │                              │
     │  ←───────────────────────────│  HTTP Requests
     │                              │  (Fetch data)
     │  ───────────────────────────→│  JSON Responses
     │                              │  (Display data)
```

---

## 🛠️ Troubleshooting

### Backend Not Running?
```bash
# Check if running
curl http://localhost:8000/health

# Start it
cd ~/Desktop/flutter\ /backend
source venv/bin/activate
uvicorn main:app --reload
```

### Port Already in Use?
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn main:app --port 8001
```

### App Can't Connect?
- Ensure backend is running
- Check API URL in `mobile_app/lib/config/api_config.dart`
- For iOS Simulator, `localhost` works fine

---

## 📝 Important Notes

1. **Backend must run continuously** - Keep Terminal 1 open
2. **Flutter app connects to backend** - Needs Terminal 1 running
3. **Both can run simultaneously** - They work together
4. **Backend serves data** - Flutter app displays it

---

**Keep both terminals running for the app to fetch data!** 🚀

