"""
AI Models - AI Response và RAG Context
"""
from typing import Optional, List
from pydantic import BaseModel


class AIResponse(BaseModel):
    """Response từ AI"""
    message: str
    intent: str
    confidence: float
    suggested_product_ids: Optional[List[int]] = None
    requires_human: bool = False


class RAGContext(BaseModel):
    """Context cho RAG pipeline"""
    user_query: str
    session_id: int
    account_id: Optional[int] = None
    conversation_history: List[dict] = []


class ProductContext(BaseModel):
    """Context về sản phẩm cho AI"""
    product_id: int
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None
    specs: Optional[dict] = None
