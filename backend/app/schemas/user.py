from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Data received during registration
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[str] = "sales_rep"

# Data received during login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Data returned after login (never return password!)
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# JWT Token response
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse