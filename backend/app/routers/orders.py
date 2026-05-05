from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import Optional, List
from app.core.database import get_db
from app.core.security import get_current_user, get_current_user_optional, require_role
from app.models.user import User
from app.models.cart import Cart, CartItem
from app.models.order import Order, OrderItem
from app.models.product import Product, ProductVariant
from app.schemas.order import (
    OrderCreate, OrderUpdate, OrderResponse,
    OrderListResponse, OrderItemResponse
)

router = APIRouter(prefix="/orders", tags=["Orders"])


def build_order_response(order: Order) -> OrderResponse:
    items = []
    for item in order.order_items:
        items.append(OrderItemResponse(
            order_item_id=item.order_item_id,
            order_id=item.order_id,
            product_id=item.product_id,
            variant_id=item.variant_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            product_name=item.product.name if item.product else None,
            product_image=item.product.image_url if item.product else None,
        ))

    return OrderResponse(
        order_id=order.order_id,
        user_id=order.user_id,
        order_date=order.order_date,
        total_amount=order.total_amount,
        status=order.status,
        customer_name=order.customer_name,
        customer_phone=order.customer_phone,
        customer_address=order.customer_address,
        notes=order.notes,
        items=items,
        created_at=order.created_at,
    )


@router.get("/", response_model=OrderListResponse)
async def get_orders(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    session_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    if current_user:
        query = db.query(Order).options(
            joinedload(Order.order_items).joinedload(OrderItem.product)
        ).filter(Order.user_id == current_user.user_id)
    elif session_id:
        cart = db.query(Cart).filter(Cart.session_id == session_id).first()
        if not cart:
            return OrderListResponse(items=[], total=0, page=page, page_size=page_size)
        query = db.query(Order).filter(Order.user_id == None)
    else:
        return OrderListResponse(items=[], total=0, page=page, page_size=page_size)

    if status:
        query = query.filter(Order.status == status)

    query = query.order_by(Order.order_date.desc())
    total = query.count()
    orders = query.offset((page - 1) * page_size).limit(page_size).all()

    return OrderListResponse(
        items=[build_order_response(o) for o in orders],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    session_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    order = db.query(Order).options(
        joinedload(Order.order_items).joinedload(OrderItem.product),
        joinedload(Order.order_items).joinedload(OrderItem.variant),
    ).filter(Order.order_id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if current_user and order.user_id != current_user.user_id:
        if current_user.role.role_name not in ["Admin", "Staff"]:
            raise HTTPException(status_code=403, detail="Not authorized")

    return build_order_response(order)


@router.post("/", response_model=OrderResponse, status_code=201)
async def create_order(
    order_data: OrderCreate,
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
        raise HTTPException(status_code=400, detail="User or session_id required")

    if not cart or not cart.cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_amount = 0
    order_items = []
    for item in cart.cart_items:
        price = item.variant.price if item.variant else item.product.price
        total_amount += price * item.quantity
        order_items.append({
            "product_id": item.product_id,
            "variant_id": item.variant_id,
            "quantity": item.quantity,
            "unit_price": price,
        })

    new_order = Order(
        user_id=current_user.user_id if current_user else None,
        total_amount=total_amount,
        status="Pending",
        customer_name=order_data.customer_name or (current_user.full_name if current_user else None),
        customer_phone=order_data.customer_phone or (current_user.phone if current_user else None),
        customer_address=order_data.customer_address or (current_user.address if current_user else None),
        notes=order_data.notes,
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item_data in order_items:
        order_item = OrderItem(order_id=new_order.order_id, **item_data)
        db.add(order_item)

        product = db.query(Product).filter(Product.product_id == item_data["product_id"]).first()
        if product:
            product.stock_quantity = max(0, product.stock_quantity - item_data["quantity"])

        if item_data.get("variant_id"):
            variant = db.query(ProductVariant).filter(
                ProductVariant.variant_id == item_data["variant_id"]
            ).first()
            if variant:
                variant.stock_quantity = max(0, variant.stock_quantity - item_data["quantity"])

    db.query(CartItem).filter(CartItem.cart_id == cart.cart_id).delete()
    db.commit()

    new_order = db.query(Order).options(
        joinedload(Order.order_items).joinedload(OrderItem.product),
        joinedload(Order.order_items).joinedload(OrderItem.variant),
    ).filter(Order.order_id == new_order.order_id).first()

    return build_order_response(new_order)


@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: int,
    order_data: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["Admin", "Staff"]))
):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order_data.status:
        valid_statuses = ["Pending", "Confirmed", "Processing", "Shipped", "Delivered", "Cancelled"]
        if order_data.status not in valid_statuses:
            raise HTTPException(status_code=400, detail="Invalid status")
        order.status = order_data.status

    if order_data.notes is not None:
        order.notes = order_data.notes

    db.commit()
    db.refresh(order)

    order = db.query(Order).options(
        joinedload(Order.order_items).joinedload(OrderItem.product),
        joinedload(Order.order_items).joinedload(OrderItem.variant),
    ).filter(Order.order_id == order_id).first()

    return build_order_response(order)


@router.get("/admin/all", response_model=OrderListResponse)
async def get_all_orders(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["Admin", "Staff"]))
):
    query = db.query(Order).options(
        joinedload(Order.order_items).joinedload(OrderItem.product)
    )

    if status:
        query = query.filter(Order.status == status)

    query = query.order_by(Order.order_date.desc())
    total = query.count()
    orders = query.offset((page - 1) * page_size).limit(page_size).all()

    return OrderListResponse(
        items=[build_order_response(o) for o in orders],
        total=total,
        page=page,
        page_size=page_size,
    )
