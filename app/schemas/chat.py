# app/schemas/chat.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from pydantic import ConfigDict

class ChatRequest(BaseModel):
    prompt: str = Field(..., description="User prompt to send to LLM")
    system: Optional[str] = Field(None, description="System instruction for the model")
    max_history: int = Field(10, description="Maximum number of history messages to include", ge=1, le=50)
    temperature: float = Field(0.7, description="Temperature for response generation", ge=0.0, le=2.0)

class ChatResponse(BaseModel):
    answer: str

class MessagePublic(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)