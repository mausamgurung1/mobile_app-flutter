from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import os
from app.database import Base

# Use String for SQLite, UUID for PostgreSQL
USE_SQLITE = os.getenv("DATABASE_URL", "").startswith("sqlite")

class Meal(Base):
    __tablename__ = "meals"

    if USE_SQLITE:
        id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
        user_id = Column(String, ForeignKey("users.id"), nullable=False)
    else:
        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    meal_type = Column(String, nullable=False)  # breakfast, lunch, dinner, snack
    date = Column(DateTime(timezone=True), nullable=False)
    nutrition_info = Column(JSON)  # Store nutrition data as JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="meals")
    food_items = relationship("FoodItem", back_populates="meal", cascade="all, delete-orphan")

class FoodItem(Base):
    __tablename__ = "food_items"

    if USE_SQLITE:
        id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
        meal_id = Column(String, ForeignKey("meals.id"), nullable=False)
    else:
        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        meal_id = Column(UUID(as_uuid=True), ForeignKey("meals.id"), nullable=False)
    name = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)  # in grams
    unit = Column(String, default="g")
    nutrition_info = Column(JSON)  # Store nutrition data as JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    meal = relationship("Meal", back_populates="food_items")

# Pydantic models for nutrition info (used in API)
class NutritionInfo:
    def __init__(self, calories=0, protein=0, carbohydrates=0, fat=0, fiber=0, sugar=None, sodium=None):
        self.calories = calories
        self.protein = protein
        self.carbohydrates = carbohydrates
        self.fat = fat
        self.fiber = fiber
        self.sugar = sugar
        self.sodium = sodium

    def to_dict(self):
        return {
            "calories": self.calories,
            "protein": self.protein,
            "carbohydrates": self.carbohydrates,
            "fat": self.fat,
            "fiber": self.fiber,
            "sugar": self.sugar,
            "sodium": self.sodium,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            calories=data.get("calories", 0),
            protein=data.get("protein", 0),
            carbohydrates=data.get("carbohydrates", 0),
            fat=data.get("fat", 0),
            fiber=data.get("fiber", 0),
            sugar=data.get("sugar"),
            sodium=data.get("sodium"),
        )

