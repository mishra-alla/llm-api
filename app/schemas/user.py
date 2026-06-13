# app/schemas/user.py
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime

class UserPublic(BaseModel):
    id: int
    email: EmailStr
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)