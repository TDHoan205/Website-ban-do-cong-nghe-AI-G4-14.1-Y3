from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1)
    session_id: Optional[str] = None
    context: Optional[dict] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str
    intent: Optional[str] = None
    action: Optional[dict] = None
    suggested_products: Optional[List[dict]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatHistoryItem(BaseModel):
    role: str
    content: str
    timestamp: datetime


class ChatSessionResponse(BaseModel):
    session_id: str
    messages: List[ChatHistoryItem] = []
    created_at: datetime
