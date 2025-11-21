# Nutrition App - Web Frontend

A modern, responsive web application for nutrition tracking and meal planning, built with HTML, CSS, and JavaScript.

## Features

- 🔐 **User Authentication** - Login and registration
- 📊 **Dashboard** - View your profile and today's nutrition stats
- 🍽️ **Meal Plans** - Generate personalized meal plans based on your goals
- 📈 **Nutrition Tracking** - Track calories, protein, carbs, and fat
- 🎨 **Modern UI** - Beautiful, responsive design that works on all devices

## File Structure

```
web/
├── index.html          # Login page
├── register.html       # Registration page
├── dashboard.html      # Main dashboard
├── meal-plans.html     # Meal plans management
├── css/
│   └── style.css       # All styles
├── js/
│   ├── api.js          # API service for backend communication
│   ├── auth.js         # Authentication utilities
│   ├── login.js        # Login page logic
│   ├── register.js     # Registration page logic
│   ├── dashboard.js    # Dashboard functionality
│   └── meal-plans.js   # Meal plans functionality
└── README.md           # This file
```

## Setup

### Prerequisites

- Backend API server running on `http://localhost:8000`
- A modern web browser (Chrome, Firefox, Safari, Edge)

### Running the Web App

1. **Start the Backend Server** (if not already running):
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Open the Web App**:
   - Option 1: Open `index.html` directly in your browser
   - Option 2: Use a local web server (recommended):
     ```bash
     # Using Python
     cd web
     python3 -m http.server 8080
     # Then open http://localhost:8080 in your browser
     
     # Or using Node.js
     npx http-server web -p 8080
     ```

3. **Access the App**:
   - Open your browser and navigate to:
     - `http://localhost:8080` (if using a web server)
     - Or open `index.html` directly

## Usage

### First Time Setup

1. **Register a New Account**:
   - Click "Sign up" on the login page
   - Fill in your personal information
   - Set your health goals and activity level
   - Submit the form

2. **Login**:
   - Enter your email and password
   - Click "Login"

### Using the Dashboard

- View your profile information
- See today's nutrition summary (calories, protein, carbs, fat)
- View today's meals
- Navigate to meal plans

### Generating Meal Plans

1. Go to the "Meal Plans" page
2. Click "Generate New Meal Plan"
3. Select start and end dates (up to 30 days)
4. Optionally select a health goal
5. Click "Generate"
6. Wait for the AI to create your personalized meal plan

## API Configuration

The web app is configured to connect to the backend API at `http://localhost:8000/api/v1`.

To change the API URL, edit `web/js/api.js`:

```javascript
const API_CONFIG = {
    baseUrl: 'http://localhost:8000/api/v1',
    // Change this to your backend URL
};
```

For production, you might want to use:
```javascript
const API_CONFIG = {
    baseUrl: window.location.origin + '/api/v1',
};
```

## Features in Detail

### Authentication
- JWT token-based authentication
- Tokens stored in browser localStorage
- Automatic redirect to login if not authenticated
- Logout functionality

### Dashboard
- Displays user profile information
- Shows today's nutrition progress with visual progress bars
- Lists all meals logged for today
- Quick access to generate meal plans

### Meal Plans
- View all your meal plans
- Generate new meal plans with AI recommendations
- Filter by date range
- See daily nutrition targets
- View all meals in each plan

## Browser Compatibility

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Troubleshooting

### CORS Errors
If you see CORS errors, make sure:
- The backend server is running
- CORS is enabled in the backend (it should be by default)
- You're accessing the web app from the same origin or using a web server

### 401 Unauthorized Errors
- Make sure you're logged in
- Check if your token expired (try logging in again)
- Clear browser localStorage and login again

### API Connection Issues
- Verify the backend is running on `http://localhost:8000`
- Check browser console for error messages
- Verify the API URL in `js/api.js`

## Development

### Adding New Features

1. **New Page**: Create a new HTML file and corresponding JS file
2. **New API Endpoint**: Add method to `js/api.js`
3. **Styling**: Add styles to `css/style.css`

### Code Structure

- **api.js**: Centralized API communication
- **auth.js**: Authentication utilities and route protection
- **Page-specific JS files**: Handle page-specific functionality
- **style.css**: All styling in one file for easy maintenance

## Notes

- The web app uses vanilla JavaScript (no frameworks)
- All data is stored in browser localStorage (tokens only)
- The app requires the backend API to be running
- Responsive design works on mobile, tablet, and desktop

## Support

For issues or questions:
1. Check the browser console for errors
2. Verify the backend API is running
3. Check network requests in browser DevTools
4. Review the backend API documentation at `http://localhost:8000/docs`

