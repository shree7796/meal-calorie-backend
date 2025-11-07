from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import BaseModel, EmailStr

class UserTable(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: EmailStr
    hashed_password: str

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class CalorieRequest(BaseModel):
    dish_name: str
    servings: float

class CalorieResponse(BaseModel):
    dish_name: str
    servings: float
    calories_per_serving: float
    total_calories: float
    source: str
