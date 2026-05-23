"""
Categories Controller - Quan ly danh muc
Tuong duong Controllers/CategoriesController.cs trong C#
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from Data.database import get_db
from Models.Category import Category
from Models.Product import Product

router = APIRouter(prefix="/Categories")


class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    display_order: Optional[int] = 0
    is_active: Optional[bool] = True


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None


def _category_to_dict(cat: Category) -> dict:
    return {
        "category_id": cat.category_id,
        "name": cat.name,
        "description": cat.description,
        "image_url": cat.image_url,
        "display_order": cat.display_order,
        "is_active": cat.is_active,
    }


@router.get("")
def list_categories(
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    db: Session = Depends(get_db),
):
    query = db.query(Category)
    if search:
        query = query.filter(Category.name.ilike(f"%{search}%"))
    total = query.count()
    items = query.order_by(Category.display_order, Category.name).offset((page - 1) * page_size).limit(page_size).all()
    return {
        "items": [_category_to_dict(c) for c in items],
        "page": page,
        "page_size": page_size,
        "total": total,
    }


@router.get("/{category_id}")
def get_category(category_id: int, db: Session = Depends(get_db)):
    cat = db.query(Category).filter(Category.category_id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    return _category_to_dict(cat)


@router.post("")
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    name = (payload.name or "").strip()
    if not name:
        raise HTTPException(status_code=400, detail="Category name is required")
    exists = db.query(Category).filter(Category.name == name).first()
    if exists:
        raise HTTPException(status_code=400, detail="Category name already exists")
    data = payload.model_dump()
    data["name"] = name
    cat = Category(**data)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return _category_to_dict(cat)


@router.put("/{category_id}")
def update_category(category_id: int, payload: CategoryUpdate, db: Session = Depends(get_db)):
    cat = db.query(Category).filter(Category.category_id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    data = payload.model_dump(exclude_unset=True)
    if "name" in data:
        name = (data["name"] or "").strip()
        if not name:
            raise HTTPException(status_code=400, detail="Category name is required")
        dup = db.query(Category).filter(
            Category.name == name,
            Category.category_id != category_id
        ).first()
        if dup:
            raise HTTPException(status_code=400, detail="Category name already exists")
        data["name"] = name
    for key, value in data.items():
        setattr(cat, key, value)
    db.commit()
    db.refresh(cat)
    return _category_to_dict(cat)


@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    cat = db.query(Category).filter(Category.category_id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    in_use = db.query(Product).filter(Product.category_id == category_id).count()
    if in_use > 0:
        raise HTTPException(status_code=400, detail="Category is in use by products")
    db.delete(cat)
    db.commit()
    return {"success": True}
