# 🚀 How to Run the Web Frontend

This guide shows you how to run the web frontend for the Nutrition App.

---

## 📋 Prerequisites

- Backend API server running on `http://localhost:8000`
- A modern web browser (Chrome, Firefox, Safari, Edge)
- Python 3 (for simple web server, optional)

---

## 🎯 Quick Start (Easiest Method)

### Step 1: Start the Backend Server

Open Terminal 1 and run:

```bash
cd "/home/mausamgr/project/flutter /backend"
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Or use the startup script:**
```bash
"/home/mausamgr/project/flutter /start_backend.sh"
```

**Verify backend is running:**
- Open browser: http://localhost:8000/docs
- Or check: `curl http://localhost:8000/health`

---

### Step 2: Open the Web App

**Option A: Direct File Opening (Simplest)**
1. Navigate to the web folder:
   ```bash
   cd "/home/mausamgr/project/flutter /web"
   ```
2. Open `index.html` in your browser:
   - Right-click `index.html` → "Open with" → Your browser
   - Or drag `index.html` into your browser window
   - Or use: `xdg-open index.html` (Linux)

**Option B: Using a Web Server (Recommended)**
1. Open Terminal 2 (keep Terminal 1 running backend)
2. Navigate to web folder:
   ```bash
   cd "/home/mausamgr/project/flutter /web"
   ```
3. Start a simple web server:

   **Using Python 3:**
   ```bash
   python3 -m http.server 8080
   ```

   **Or using Python 2:**
   ```bash
   python -m SimpleHTTPServer 8080
   ```

   **Or using Node.js (if installed):**
   ```bash
   npx http-server -p 8080
   ```

4. Open your browser and go to:
   ```
   http://localhost:8080
   ```

---

## 🎉 You're Ready!

Once both are running:
- ✅ Backend API: http://localhost:8000/docs
- ✅ Web App: http://localhost:8080 (or open index.html directly)

---

## 📝 Step-by-Step Instructions

### Method 1: Direct File Opening (No Server Needed)

1. **Start Backend** (Terminal 1):
   ```bash
   cd "/home/mausamgr/project/flutter /backend"
   source venv/bin/activate
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Open Web App**:
   - Navigate to: `/home/mausamgr/project/flutter /web`
   - Double-click `index.html` or open it with your browser
   - The app will connect to `http://localhost:8000`

**Note:** Some browsers may block local file access. If you see CORS errors, use Method 2.

---

### Method 2: Using a Web Server (Recommended)

1. **Start Backend** (Terminal 1):
   ```bash
   cd "/home/mausamgr/project/flutter /backend"
   source venv/bin/activate
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Start Web Server** (Terminal 2):
   ```bash
   cd "/home/mausamgr/project/flutter /web"
   python3 -m http.server 8080
   ```

3. **Open Browser**:
   - Go to: http://localhost:8080
   - You should see the login page

---

## 🔧 Using the Startup Script

I've created a startup script for you. Run:

```bash
"/home/mausamgr/project/flutter /start_web.sh"
```

This will:
1. Check if backend is running
2. Start a web server for the frontend
3. Open the app in your browser

---

## 🌐 URLs and Endpoints

### Backend API
- **Base URL**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **API Base**: http://localhost:8000/api/v1

### Web Frontend
- **Local Server**: http://localhost:8080
- **Direct File**: Open `web/index.html` in browser

---

## ✅ Verification Checklist

After starting both services:

- [ ] Backend is running: `curl http://localhost:8000/health`
- [ ] Backend docs accessible: http://localhost:8000/docs
- [ ] Web server is running (if using Method 2): http://localhost:8080
- [ ] Can see login page in browser
- [ ] Can register/login in the app

---

## 🐛 Troubleshooting

### CORS Errors
**Problem:** Browser shows CORS errors when opening `index.html` directly.

**Solution:** Use a web server (Method 2) instead of opening the file directly.

### Backend Connection Failed
**Problem:** Web app can't connect to backend.

**Solutions:**
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check API URL in `web/js/api.js` (should be `http://localhost:8000/api/v1`)
3. Make sure backend CORS is enabled (it should be by default)

### Port 8080 Already in Use
**Problem:** `Address already in use` error.

**Solutions:**
1. Use a different port:
   ```bash
   python3 -m http.server 8081
   ```
   Then open: http://localhost:8081

2. Or find and kill the process using port 8080:
   ```bash
   lsof -ti:8080 | xargs kill
   ```

### 401 Unauthorized Errors
**Problem:** Getting 401 errors after login.

**Solutions:**
1. Clear browser localStorage:
   - Open browser DevTools (F12)
   - Go to Application/Storage tab
   - Clear Local Storage
   - Try logging in again

2. Check if token is being saved:
   - DevTools → Application → Local Storage
   - Should see `auth_token` key

### Page Not Found (404)
**Problem:** Getting 404 when navigating.

**Solution:** Make sure you're using a web server (Method 2), not opening files directly. The routing requires a server.

---

## 📱 Testing the App

1. **Register a New Account:**
   - Click "Sign up" on login page
   - Fill in all required fields
   - Submit the form

2. **Login:**
   - Enter your email and password
   - Click "Login"

3. **View Dashboard:**
   - See your profile information
   - View today's nutrition stats

4. **Generate Meal Plan:**
   - Go to "Meal Plans" page
   - Click "Generate New Meal Plan"
   - Select dates and goal
   - Click "Generate"
   - Wait for the plan to be created

---

## 🛠️ Development Tips

### View Browser Console
- Press `F12` or `Ctrl+Shift+I` (Linux/Windows) or `Cmd+Option+I` (Mac)
- Check Console tab for errors
- Check Network tab for API requests

### Debug API Calls
1. Open DevTools (F12)
2. Go to Network tab
3. Make an action in the app
4. Check the API requests and responses

### Change API URL
Edit `web/js/api.js`:
```javascript
const API_CONFIG = {
    baseUrl: 'http://localhost:8000/api/v1',
    // Change this if your backend is on a different URL
};
```

---

## 🎉 Success!

When everything is working:
- ✅ Backend API running on port 8000
- ✅ Web app accessible in browser
- ✅ Can register/login
- ✅ Can view dashboard
- ✅ Can generate meal plans

**Need help?** Check the browser console (F12) for error messages.

