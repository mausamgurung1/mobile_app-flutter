from sqlalchemy import Column, String, Integer, Float, DateTime, ARRAY, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import os
from app.database import Base

# Use String for SQLite, UUID for PostgreSQL
USE_SQLITE = os.getenv("DATABASE_URL", "").startswith("sqlite")

class User(Base):
    __tablename__ = "users"

    if USE_SQLITE:
        id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    else:
        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    gender = Column(String)  # male, female, other
    height = Column(Float)  # in cm
    weight = Column(Float)  # in kg
    activity_level = Column(String)  # sedentary, lightly_active, etc.
    medical_conditions = Column(JSON if USE_SQLITE else ARRAY(String))
    food_preferences = Column(JSON if USE_SQLITE else ARRAY(String))  # vegetarian, vegan, etc.
    allergies = Column(JSON if USE_SQLITE else ARRAY(String))
    health_goal = Column(String)  # weight_loss, muscle_gain, maintenance, diabetes_management
    target_weight = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def calculate_bmr(self):
        """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
        if not all([self.age, self.height, self.weight, self.gender]):
            return None
        
        if self.gender.lower() == "male":
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age + 5
        else:
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age - 161
        
        return bmr

    def calculate_tdee(self):
        """Calculate Total Daily Energy Expenditure"""
        bmr = self.calculate_bmr()
        if not bmr:
            return None
        
        activity_multipliers = {
            "sedentary": 1.2,
            "lightly_active": 1.375,
            "moderately_active": 1.55,
            "very_active": 1.725,
            "extremely_active": 1.9,
        }
        
        multiplier = activity_multipliers.get(self.activity_level, 1.2)
        return bmr * multiplier

