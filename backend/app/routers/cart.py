from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import Optional
from app.core.database import get_db
from app.core.security import get_current_user_optional
from app.models.user import User
from app.models.cart import Cart, CartItem
from app.models.product import Product, ProductVariant
from app.schemas.cart import (
    CartResponse, CartItemResponse,
    AddToCartRequest, UpdateCartItemRequest
)

router = APIRouter(prefix="/cart", tags=["Cart"])


def get_or_create_cart(db: Session, user: Optional[User] = None, session_id: Optional[str] = None) -> Cart:
    if user:
        cart = db.query(Cart).filter(Cart.user_id == user.user_id).first()
        if not cart:
            role_name = user.role.role_name if user.role else "Customer"
            cart = Cart(user_id=user.user_id, role_name=role_name)
            db.add(cart)
            db.commit()
            db.refresh(cart)
    elif session_id:
        cart = db.query(Cart).filter(Cart.session_id == session_id).first()
        if not cart:
            cart = Cart(session_id=session_id, role_name="Guest")
            db.add(cart)
            db.commit()
            db.refresh(cart)
    else:
        raise HTTPException(status_code=400, detail="User or session_id required")
    return cart


def build_cart_response(cart: Cart) -> CartResponse:
    items = []
    total = 0
    item_count = 0

    for item in cart.cart_items:
        price = item.variant.price if item.variant else item.product.price
        items.append(CartItemResponse(
            cart_item_id=item.cart_item_id,
            cart_id=item.cart_id,
            product_id=item.product_id,
            variant_id=item.variant_id,
            quantity=item.quantity,
            added_date=item.added_date,
            product_name=item.product.name if item.product else None,
            product_image=item.product.image_url if item.product else None,
            variant_name=item.variant.variant_name if item.variant else None,
            unit_price=price,
        ))
        total += price * item.quantity
        item_count += item.quantity

    return CartResponse(
        cart_id=cart.cart_id,
        user_id=cart.user_id,
        session_id=cart.session_id,
        items=items,
        total_amount=total,
        item_count=item_count,
        created_at=cart.created_at,
    )


@router.get("/", response_model=CartResponse)
async def get_cart(
    session_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    if current_user:
        cart = db.query(Cart).options(
            joinedload(Cart.cart_items).joinedload(CartItem.product),
            joinedload(Cart.cart_items).joinedload(CartItem.variant)
        ).filter(Cart.user_id == current_user.user_id).first()
    elif session_id:
        cart = db.query(Cart).options(
            joinedload(Cart.cart_items).joinedload(CartItem.product),
            joinedload(Cart.cart_items).joinedload(CartItem.variant)
        ).filter(Cart.session_id == session_id).first()
    else:
        return CartResponse(cart_id=0, items=[], total_amount=0, item_count=0)

    if not cart:
        return CartResponse(cart_id=0, items=[], total_amount=0, item_count=0)

    return build_cart_response(cart)


@router.post("/add", response_model=CartResponse)
async def add_to_cart(
    request: AddToCartRequest,
    session_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    cart = get_or_create_cart(db, current_user, session_id)

    product = db.query(Product).filter(Product.product_id == request.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if request.variant_id:
        variant = db.query(ProductVariant).filter(
            ProductVariant.variant_id == request.variant_id,
            ProductVariant.product_id == request.product_id
        ).first()
        if not variant:
            raise HTTPException(status_code=400, detail="Invalid variant")

    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.cart_id,
        CartItem.product_id == request.product_id,
        CartItem.variant_id == request.variant_id
    ).first()

    if existing_item:
        existing_item.quantity += request.quantity
    else:
        new_item = CartItem(
            cart_id=cart.cart_id,
            product_id=request.product_id,
            variant_id=request.variant_id,
            quantity=request.quantity,
        )
        db.add(new_item)

    db.commit()

    cart = db.query(Cart).options(
        joinedload(Cart.cart_items).joinedload(CartItem.product),
        joinedload(Cart.cart_items).joinedload(CartItem.variant)
    ).filter(Cart.cart_id == cart.cart_id).first()

    return build_cart_response(cart)


@router.put("/update/{product_id}", response_model=CartResponse)
async def update_cart_item(
    product_id: int,
    request: UpdateCartItemRequest,
    variant_id: Optional[int] = None,
    session_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    if current_user:
        cart = db.query(Cart).filter(Cart.user_id == current_user.user_id).first()
    elif session_id:
        cart = db.query(Cart).filter(Cart.session_id == session_id).first()
    else:
        raise HTTPException(status_code=400, detail="User or session_id required")

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    item = db.query(CartItem).filter(
        CartItem.cart_id == cart.cart_id,
        CartItem.product_id == product_id,
        CartItem.variant_id == variant_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found in cart")

    item.quantity = request.quantity
    db.commit()

    cart = db.query(Cart).options(
        joinedload(Cart.cart_items).joinedload(CartItem.product),
        joinedload(Cart.cart_items).joinedload(CartItem.variant)
    ).filter(Cart.cart_id == cart.cart_id).first()

    return build_cart_response(cart)


@router.delete("/remove/{product_id}", response_model=CartResponse)
async def remove_from_cart(
    product_id: int,
    variant_id: Optional[int] = None,
    session_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    if current_user:
        cart = db.query(Cart).filter(Cart.user_id == current_user.user_id).first()
    elif session_id:
        cart = db.query(Cart).filter(Cart.session_id == session_id).first()
    else:
        raise HTTPException(status_code=400, detail="User or session_id required")

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    item = db.query(CartItem).filter(
        CartItem.cart_id == cart.cart_id,
        CartItem.product_id == product_id,
        CartItem.variant_id == variant_id
    ).first()

    if item:
        db.delete(item)
        db.commit()

    cart = db.query(Cart).options(
        joinedload(Cart.cart_items).joinedload(CartItem.product),
        joinedload(Cart.cart_items).joinedload(CartItem.variant)
    ).filter(Cart.cart_id == cart.cart_id).first()

    return build_cart_response(cart)


@router.delete("/clear", response_model=CartResponse)
async def clear_cart(
    session_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    if current_user:
        cart = db.query(Cart).filter(Cart.user_id == current_user.user_id).first()
    elif session_id:
        cart = db.query(Cart).filter(Cart.session_id == session_id).first()
    else:
        raise HTTPException(status_code=400, detail="User or session_id required")

    if cart:
        db.query(CartItem).filter(CartItem.cart_id == cart.cart_id).delete()
        db.commit()

    return CartResponse(cart_id=cart.cart_id if cart else 0, items=[], total_amount=0, item_count=0)


@router.post("/merge", response_model=CartResponse)
async def merge_guest_cart(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional)
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Login required")

    guest_cart = db.query(Cart).options(
        joinedload(Cart.cart_items)
    ).filter(Cart.session_id == session_id).first()

    user_cart = db.query(Cart).options(
        joinedload(Cart.cart_items).joinedload(CartItem.product),
        joinedload(Cart.cart_items).joinedload(CartItem.variant)
    ).filter(Cart.user_id == current_user.user_id).first()

    if not guest_cart or not user_cart:
        return user_cart if user_cart else CartResponse(cart_id=0, items=[], total_amount=0, item_count=0)

    for guest_item in guest_cart.cart_items:
        existing = next(
            (i for i in user_cart.cart_items if i.product_id == guest_item.product_id and i.variant_id == guest_item.variant_id),
            None
        )
        if existing:
            existing.quantity += guest_item.quantity
            db.delete(guest_item)
        else:
            guest_item.cart_id = user_cart.cart_id

    db.delete(guest_cart)
    db.commit()

    user_cart = db.query(Cart).options(
        joinedload(Cart.cart_items).joinedload(CartItem.product),
        joinedload(Cart.cart_items).joinedload(CartItem.variant)
    ).filter(Cart.cart_id == user_cart.cart_id).first()

    return build_cart_response(user_cart)
