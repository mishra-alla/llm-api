# app/schemas/auth.py
from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"