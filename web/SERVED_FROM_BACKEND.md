# 🌐 Web Frontend Served from Backend

The web frontend is now integrated with the backend and served directly from the FastAPI server.

## ✅ What Changed

- **Backend** (`backend/main.py`) now serves static files (HTML, CSS, JS)
- **API Configuration** updated to use relative paths
- **Navigation** updated to use absolute paths
- **Single Server** - Everything runs from one place!

## 🚀 How to Run

### Single Command (Everything in One Server)

```bash
cd "/home/mausamgr/project/flutter /backend"
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

That's it! The backend now serves:
- **Web App**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **API**: http://localhost:8000/api/v1

## 📍 URLs

- **Home/Login**: http://localhost:8000/
- **Register**: http://localhost:8000/register.html
- **Dashboard**: http://localhost:8000/dashboard.html
- **Meal Plans**: http://localhost:8000/meal-plans.html
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🎯 Benefits

1. **Single Server** - No need to run separate web server
2. **No CORS Issues** - Everything served from same origin
3. **Simpler Deployment** - One process to manage
4. **Easier Development** - Just start the backend

## 📝 Notes

- The web files are still in the `web/` directory
- Backend automatically detects and serves them
- API calls use relative paths (`/api/v1`)
- All navigation uses absolute paths (`/dashboard.html`)

## 🔄 Migration from Separate Server

If you were using the separate web server before:

**Old Way:**
- Terminal 1: Backend on port 8000
- Terminal 2: Web server on port 8080

**New Way:**
- Terminal 1: Backend on port 8000 (serves everything)

No more Terminal 2 needed! 🎉

