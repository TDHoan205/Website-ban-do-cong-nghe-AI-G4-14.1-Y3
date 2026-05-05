from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CartItemBase(BaseModel):
    product_id: int
    variant_id: Optional[int] = None
    quantity: int = Field(..., ge=1)


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(BaseModel):
    quantity: int = Field(..., ge=1)


class CartItemResponse(BaseModel):
    cart_item_id: int
    cart_id: int
    product_id: int
    variant_id: Optional[int] = None
    quantity: int
    added_date: Optional[datetime] = None
    product_name: Optional[str] = None
    product_image: Optional[str] = None
    variant_name: Optional[str] = None
    unit_price: Optional[int] = None

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    cart_id: int
    user_id: Optional[int] = None
    session_id: Optional[str] = None
    items: List[CartItemResponse] = []
    total_amount: int = 0
    item_count: int = 0
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AddToCartRequest(BaseModel):
    product_id: int
    variant_id: Optional[int] = None
    quantity: int = Field(1, ge=1)


class UpdateCartItemRequest(BaseModel):
    quantity: int = Field(..., ge=1)
