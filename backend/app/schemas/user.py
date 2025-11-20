from pydantic import BaseModel, EmailStr
from typing import Optional, List, Union
from datetime import datetime
import uuid
import os

class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    activity_level: Optional[str] = None
    medical_conditions: Optional[List[str]] = None
    food_preferences: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
    health_goal: Optional[str] = None
    target_weight: Optional[float] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    activity_level: Optional[str] = None
    medical_conditions: Optional[List[str]] = None
    food_preferences: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
    health_goal: Optional[str] = None
    target_weight: Optional[float] = None

# Support both UUID (PostgreSQL) and String (SQLite) for id
USE_SQLITE = os.getenv("DATABASE_URL", "").startswith("sqlite")

if USE_SQLITE:
    class UserResponse(UserBase):
        id: str
        created_at: Optional[datetime] = None

        class Config:
            from_attributes = True
else:
    class UserResponse(UserBase):
        id: uuid.UUID
        created_at: Optional[datetime] = None

        class Config:
            from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

