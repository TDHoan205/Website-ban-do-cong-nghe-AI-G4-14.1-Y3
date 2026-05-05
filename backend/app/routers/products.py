from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from typing import Optional, List
from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.models.user import User
from app.models.product import Product, ProductVariant, ProductImage, Category
from app.schemas.product import (
    ProductCreate, ProductUpdate, ProductResponse,
    ProductListResponse, ProductSearchResponse
)

router = APIRouter(prefix="/products", tags=["Products"])


def build_product_response(product: Product) -> ProductResponse:
    category_name = product.category.name if product.category else None
    supplier_name = product.supplier.name if product.supplier else None
    variants = [
        {
            "variant_id": v.variant_id,
            "product_id": v.product_id,
            "color": v.color,
            "storage": v.storage,
            "ram": v.ram,
            "variant_name": v.variant_name,
            "sku": v.sku,
            "price": v.price,
            "original_price": v.original_price,
            "stock_quantity": v.stock_quantity,
        }
        for v in product.variants
    ]
    images = [
        {
            "image_id": img.image_id,
            "product_id": img.product_id,
            "image_url": img.image_url,
            "display_order": img.display_order,
            "is_primary": img.is_primary,
        }
        for img in product.images
    ]
    return ProductResponse(
        product_id=product.product_id,
        name=product.name,
        description=product.description,
        image_url=product.image_url,
        price=product.price,
        original_price=product.original_price,
        stock_quantity=product.stock_quantity,
        is_available=product.is_available,
        rating=product.rating,
        is_new=product.is_new,
        is_hot=product.is_hot,
        discount_percent=product.discount_percent,
        specifications=product.specifications,
        category_id=product.category_id,
        supplier_id=product.supplier_id,
        category_name=category_name,
        supplier_name=supplier_name,
        variants=variants,
        images=images,
        created_at=product.created_at,
    )


@router.get("/", response_model=ProductListResponse)
async def get_products(
    search: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    sort_by: Optional[str] = Query("newest"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    min_price: Optional[int] = Query(None),
    max_price: Optional[int] = Query(None),
    filter_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Product).options(
        joinedload(Product.category),
        joinedload(Product.supplier),
        joinedload(Product.variants),
        joinedload(Product.images)
    )

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Product.name.ilike(search_term),
                Product.description.ilike(search_term),
            )
        )

    if category_id:
        query = query.filter(Product.category_id == category_id)

    if min_price:
        query = query.filter(
            or_(Product.price >= min_price, Product.variants.any(ProductVariant.price >= min_price))
        )

    if max_price:
        query = query.filter(
            or_(Product.price <= max_price, Product.variants.any(ProductVariant.price <= max_price))
        )

    if filter_type:
        if filter_type.lower() == "new":
            query = query.filter(Product.is_new == True)
        elif filter_type.lower() == "hot":
            query = query.filter(Product.is_hot == True)
        elif filter_type.lower() == "deal":
            query = query.filter(
                or_(Product.discount_percent > 0, Product.original_price != None)
            )

    sort_options = {
        "name": Product.name.asc(),
        "name_desc": Product.name.desc(),
        "price": Product.price.asc(),
        "price_desc": Product.price.desc(),
        "newest": Product.product_id.desc(),
        "rating": Product.rating.desc(),
    }
    query = query.order_by(sort_options.get(sort_by, Product.product_id.desc()))

    total = query.count()
    products = query.offset((page - 1) * page_size).limit(page_size).all()

    return ProductListResponse(
        items=[build_product_response(p) for p in products],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.get("/featured", response_model=List[ProductResponse])
async def get_featured_products(
    type: str = Query("new", regex="^(new|hot|deal)$"),
    count: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    query = db.query(Product).options(
        joinedload(Product.category),
        joinedload(Product.supplier),
        joinedload(Product.variants),
        joinedload(Product.images)
    )

    if type == "new":
        query = query.order_by(Product.is_new.desc(), Product.product_id.desc())
    elif type == "hot":
        query = query.filter(Product.is_hot == True)
    elif type == "deal":
        query = query.filter(
            or_(Product.discount_percent > 0, Product.original_price != None)
        )

    products = query.limit(count).all()
    return [build_product_response(p) for p in products]


@router.get("/search", response_model=List[ProductSearchResponse])
async def search_products(
    q: str = Query(..., min_length=2),
    count: int = Query(10, ge=1, le=20),
    db: Session = Depends(get_db)
):
    search_term = f"%{q}%"
    products = db.query(Product).options(
        joinedload(Product.category)
    ).filter(
        or_(
            Product.name.ilike(search_term),
            Product.description.ilike(search_term),
        )
    ).limit(count).all()

    return [
        ProductSearchResponse(
            product_id=p.product_id,
            name=p.name,
            price=p.price,
            image_url=p.image_url,
            category_name=p.category.name if p.category else None,
        )
        for p in products
    ]


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).options(
        joinedload(Product.category),
        joinedload(Product.supplier),
        joinedload(Product.variants),
        joinedload(Product.images),
        joinedload(Product.inventory),
    ).filter(Product.product_id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return build_product_response(product)


@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["Admin", "Staff"]))
):
    new_product = Product(**product_data.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return build_product_response(new_product)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["Admin", "Staff"]))
):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return build_product_response(product)


@router.delete("/{product_id}", status_code=204)
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["Admin"]))
):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return None
