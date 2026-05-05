from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    category_id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProductVariantResponse(BaseModel):
    variant_id: int
    product_id: int
    color: Optional[str] = None
    storage: Optional[str] = None
    ram: Optional[str] = None
    variant_name: Optional[str] = None
    sku: Optional[str] = None
    price: Optional[int] = None
    original_price: Optional[int] = None
    stock_quantity: int = 0

    class Config:
        from_attributes = True


class ProductImageResponse(BaseModel):
    image_id: int
    product_id: int
    image_url: str
    display_order: int = 0
    is_primary: bool = False

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    image_url: Optional[str] = Field(None, max_length=500)
    price: int = Field(..., ge=0)
    original_price: Optional[int] = None
    stock_quantity: int = 0
    is_available: bool = True
    rating: int = 5
    is_new: bool = False
    is_hot: bool = False
    discount_percent: int = 0
    specifications: Optional[str] = None
    category_id: Optional[int] = None
    supplier_id: Optional[int] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    image_url: Optional[str] = Field(None, max_length=500)
    price: Optional[int] = None
    original_price: Optional[int] = None
    stock_quantity: Optional[int] = None
    is_available: Optional[bool] = None
    rating: Optional[int] = None
    is_new: Optional[bool] = None
    is_hot: Optional[bool] = None
    discount_percent: Optional[int] = None
    specifications: Optional[str] = None
    category_id: Optional[int] = None
    supplier_id: Optional[int] = None


class ProductResponse(ProductBase):
    product_id: int
    category_name: Optional[str] = None
    supplier_name: Optional[str] = None
    variants: List[ProductVariantResponse] = []
    images: List[ProductImageResponse] = []
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    items: List[ProductResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class ProductSearchResponse(BaseModel):
    product_id: int
    name: str
    price: int
    image_url: Optional[str] = None
    category_name: Optional[str] = None
