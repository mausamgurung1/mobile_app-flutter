from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import os
from app.database import Base

# Use String for SQLite, UUID for PostgreSQL
USE_SQLITE = os.getenv("DATABASE_URL", "").startswith("sqlite")

class MealPlan(Base):
    __tablename__ = "meal_plans"

    if USE_SQLITE:
        id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
        user_id = Column(String, ForeignKey("users.id"), nullable=False)
    else:
        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    goal = Column(String)  # weight_loss, muscle_gain, maintenance, diabetes_management
    daily_nutrition_target = Column(JSON)  # Target nutrition per day
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", backref="meal_plans")

