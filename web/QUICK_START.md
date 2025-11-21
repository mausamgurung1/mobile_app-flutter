# ⚡ Quick Start - Web Frontend

## 🚀 Fastest Way to Run

### Terminal 1: Backend
```bash
cd "/home/mausamgr/project/flutter /backend"
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Terminal 2: Web Frontend
```bash
# Option 1: Use the startup script (easiest)
"/home/mausamgr/project/flutter /start_web.sh"

# Option 2: Manual start
cd "/home/mausamgr/project/flutter /web"
python3 -m http.server 8080
```

### Open Browser
- Go to: **http://localhost:8080**
- Or open `web/index.html` directly in your browser

---

## ✅ That's It!

1. Backend running on port 8000 ✅
2. Web server running on port 8080 ✅
3. Open http://localhost:8080 in browser ✅

---

## 🎯 What You'll See

1. **Login Page** - Register or login
2. **Dashboard** - Your profile and nutrition stats
3. **Meal Plans** - Generate personalized meal plans

---

## 🐛 Quick Fixes

**CORS Error?** → Use web server (Method 2), don't open file directly

**Backend not found?** → Make sure backend is running on port 8000

**Port 8080 busy?** → Use different port: `python3 -m http.server 8081`

**401 Unauthorized?** → Clear browser localStorage and login again

---

For detailed instructions, see `HOW_TO_RUN.md`

