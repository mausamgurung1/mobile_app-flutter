from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import os
from app.api import auth, users, meal_plans, nutrition, recommendations
from app.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Nutrition API",
    description="Personalized Nutrition and Diet Management Platform API",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(meal_plans.router, prefix="/api/v1/meal-plans", tags=["Meal Plans"])
app.include_router(nutrition.router, prefix="/api/v1/nutrition", tags=["Nutrition"])
app.include_router(recommendations.router, prefix="/api/v1/recommendations", tags=["Recommendations"])

# Get the project root directory (parent of backend directory)
backend_dir = Path(__file__).parent
project_root = backend_dir.parent
web_dir = project_root / "web"

# Serve static files (CSS, JS, images) if web directory exists
if web_dir.exists() and web_dir.is_dir():
    # Mount static files
    static_dir = web_dir / "css"
    if static_dir.exists():
        app.mount("/css", StaticFiles(directory=str(static_dir)), name="css")
    
    static_dir = web_dir / "js"
    if static_dir.exists():
        app.mount("/js", StaticFiles(directory=str(static_dir)), name="js")
    
    # Serve HTML files
    @app.get("/")
    async def root():
        index_file = web_dir / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))
        return {"message": "Nutrition API is running", "version": "1.0.0"}
    
    @app.get("/register.html")
    async def register_page():
        register_file = web_dir / "register.html"
        if register_file.exists():
            return FileResponse(str(register_file))
        return {"error": "Register page not found"}
    
    @app.get("/dashboard.html")
    async def dashboard_page():
        dashboard_file = web_dir / "dashboard.html"
        if dashboard_file.exists():
            return FileResponse(str(dashboard_file))
        return {"error": "Dashboard page not found"}
    
    @app.get("/meal-plans.html")
    async def meal_plans_page():
        meal_plans_file = web_dir / "meal-plans.html"
        if meal_plans_file.exists():
            return FileResponse(str(meal_plans_file))
        return {"error": "Meal plans page not found"}
else:
    # Fallback if web directory doesn't exist
    @app.get("/")
    async def root():
        return {"message": "Nutrition API is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

