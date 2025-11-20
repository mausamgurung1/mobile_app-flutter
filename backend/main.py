from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

@app.get("/")
async def root():
    return {"message": "Nutrition API is running", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

