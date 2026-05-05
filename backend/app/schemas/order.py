from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class OrderItemBase(BaseModel):
    product_id: int
    variant_id: Optional[int] = None
    quantity: int = Field(..., ge=1)
    unit_price: int = Field(..., ge=0)


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(OrderItemBase):
    order_item_id: int
    order_id: int
    product_name: Optional[str] = None
    product_image: Optional[str] = None

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = Field(None, max_length=20)
    customer_address: Optional[str] = Field(None, max_length=255)
    notes: Optional[str] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None


class OrderResponse(OrderBase):
    order_id: int
    user_id: Optional[int] = None
    order_date: Optional[datetime] = None
    total_amount: int
    status: str
    items: List[OrderItemResponse] = []
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    items: List[OrderResponse]
    total: int
    page: int
    page_size: int
