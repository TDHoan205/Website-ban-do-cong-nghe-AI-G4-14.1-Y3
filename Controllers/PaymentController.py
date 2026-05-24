"""
Payment Controller - Thanh toán QR Banking
"""
from fastapi import APIRouter, Request, Depends, Form, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from decimal import Decimal
from datetime import datetime
from typing import Optional

from Data.database import get_db
from Services.CartService import CartService
from Services.PaymentService import PaymentService, BANK_CONFIG
from Services.AuthService import AuthService
from Utilities.auth import require_account
from Utilities.http import is_ajax_request
from Models.Payment import PaymentStatus

router = APIRouter(prefix="/Checkout")


def _get_cart_count(request: Request, db: Session) -> int:
    token = request.cookies.get("access_token")
    if not token:
        return 0
    auth_service = AuthService(db)
    account = auth_service.get_current_account_from_token(token)
    if not account:
        return 0
    cart_service = CartService(db)
    return cart_service.get_cart_item_count(account.account_id)


def _get_current_user(request: Request, db: Session):
    token = request.cookies.get("access_token")
    if not token:
        return None
    auth_service = AuthService(db)
    return auth_service.get_current_account_from_token(token)


# ============================================================
# CHECKOUT PAGE
# ============================================================

@router.get("/", response_class=HTMLResponse)
async def checkout_page(request: Request, db: Session = Depends(get_db)):
    """Trang checkout - hiển thị QR thanh toán"""
    try:
        account = require_account(request, db)
    except HTTPException:
        return RedirectResponse(url="/Auth/Login", status_code=303)

    cart_service = CartService(db)
    cart = cart_service.get_or_create_cart(account.account_id)
    items = cart_service.get_cart_items(cart.cart_id)

    if not items:
        return RedirectResponse(url="/Cart/", status_code=303)

    # Tính tổng tiền (đã có VAT 10%)
    subtotal = sum(item.subtotal for item in items)
    tax = subtotal * Decimal("0.10")
    total = subtotal + tax
    total_int = int(total)

    current_user = _get_current_user(request, db)
    cart_count = _get_cart_count(request, db)

    # Tạo payment record
    payment_service = PaymentService(db)
    payment = payment_service.create_payment(
        account_id=account.account_id,
        amount=total_int,
    )

    payment_info = payment_service.get_payment_display_info(payment.order_id)

    return templates.TemplateResponse(
        "Checkout/checkout.html",
        {
            "request": request,
            "page_title": "Thanh toán QR",
            "cart_items": items,
            "cart": cart,
            "subtotal": float(subtotal),
            "tax": float(tax),
            "total": float(total),
            "total_int": total_int,
            "payment": payment_info,
            "bank_config": BANK_CONFIG,
            "current_user": current_user,
            "cart_count": cart_count,
        }
    )


# ============================================================
# API: Lấy thông tin thanh toán (polling)
# ============================================================

@router.get("/api/payment/status/{order_id}")
async def get_payment_status(order_id: str, request: Request, db: Session = Depends(get_db)):
    """API lấy trạng thái thanh toán - dùng cho polling"""
    payment_service = PaymentService(db)
    info = payment_service.get_payment_display_info(order_id)

    if not info:
        return JSONResponse({"error": "Không tìm thấy thanh toán"}, status_code=404)

    return JSONResponse(info)


# ============================================================
# API: Xác nhận thanh toán (Tôi đã thanh toán)
# ============================================================

@router.post("/api/payment/verify")
async def verify_payment(
    request: Request,
    order_id: str = Form(...),
    transaction_code: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Xác nhận thanh toán - tạo đơn hàng nếu chưa có
    """
    payment_service = PaymentService(db)

    # 1. Verify payment
    ok, message = payment_service.verify_payment(
        order_id=order_id,
        transaction_code=transaction_code,
        verified_by="manual"
    )

    if not ok:
        return JSONResponse({"success": False, "message": message}, status_code=400)

    # 2. Lấy payment đã verified
    payment = payment_service.get_payment_by_order_id(order_id)
    if not payment:
        return JSONResponse({"success": False, "message": "Lỗi hệ thống"}, status_code=500)

    # 3. Tạo đơn hàng
    try:
        order = await _create_order_from_payment(db, payment)
        return JSONResponse({
            "success": True,
            "message": message,
            "order_id": order.order_id,
            "redirect_url": f"/Checkout/success/{order.order_id}"
        })
    except Exception as e:
        print(f"[Payment/verify] Order creation error: {e}")
        return JSONResponse({
            "success": False,
            "message": f"Thanh toán thành công nhưng tạo đơn hàng thất bại: {str(e)}"
        }, status_code=500)


# ============================================================
# SUCCESS PAGE
# ============================================================

@router.get("/success/{order_id}", response_class=HTMLResponse)
async def success_page(order_id: str, request: Request, db: Session = Depends(get_db)):
    """Trang thành công"""
    try:
        account = require_account(request, db)
    except HTTPException:
        return RedirectResponse(url="/Auth/Login", status_code=303)

    # Lấy thông tin payment
    payment_service = PaymentService(db)
    payment_info = payment_service.get_payment_display_info(order_id)

    # Lấy thông tin order
    from Models.Order import Order
    order = db.query(Order).filter(Order.order_id == order_id).first()

    current_user = _get_current_user(request, db)
    cart_count = _get_cart_count(request, db)

    return templates.TemplateResponse(
        "Checkout/success.html",
        {
            "request": request,
            "page_title": "Thanh toán thành công",
            "order": order,
            "payment": payment_info,
            "current_user": current_user,
            "cart_count": 0,
        }
    )


# ============================================================
# INTERNAL: Tạo đơn hàng từ payment
# ============================================================

async def _create_order_from_payment(db: Session, payment) -> "Order":
    """Tạo đơn hàng từ payment đã verified"""

    from Models.Order import Order, OrderItem
    from Models.Cart import Cart, CartItem
    from sqlalchemy.orm import joinedload

    # Lấy cart items
    cart = db.query(Cart).filter(Cart.account_id == payment.account_id).first()
    if not cart:
        raise Exception("Không tìm thấy giỏ hàng")

    cart_items = db.query(CartItem).options(
        joinedload(CartItem.product),
        joinedload(CartItem.variant)
    ).filter(CartItem.cart_id == cart.cart_id).all()

    if not cart_items:
        raise Exception("Giỏ hàng trống")

    # Lấy thông tin account
    from Models.Account import Account
    account = db.query(Account).filter(Account.account_id == payment.account_id).first()

    # Tạo order
    order = Order(
        account_id=payment.account_id,
        total_amount=Decimal(str(payment.amount)),
        status="Confirmed",
        customer_name=account.full_name if account else "Khách hàng",
        customer_phone=account.phone if account else "",
        customer_address=account.address if account else "",
        notes=f"Thanh toán QR - Mã GD: {payment.transaction_code or payment.order_id}",
    )
    db.add(order)
    db.flush()  # Lấy order_id

    # Tạo order items
    for item in cart_items:
        product = item.product
        variant = item.variant
        unit_price = float(variant.price if variant and variant.price else product.price)
        subtotal = unit_price * item.quantity

        order_item = OrderItem(
            order_id=order.order_id,
            product_id=item.product_id,
            variant_id=item.variant_id,
            product_name=product.name if product else "Sản phẩm",
            variant_name=variant.variant_name if variant and variant.variant_name else "",
            quantity=item.quantity,
            unit_price=Decimal(str(unit_price)),
            subtotal=Decimal(str(subtotal)),
        )
        db.add(order_item)

        # Trừ stock variant
        if variant and hasattr(variant, 'stock_quantity'):
            variant.stock_quantity = max(0, (variant.stock_quantity or 0) - item.quantity)
        # Trừ stock product
        if product and hasattr(product, 'stock_quantity'):
            product.stock_quantity = max(0, (product.stock_quantity or 0) - item.quantity)

    # Xóa cart items
    db.query(CartItem).filter(CartItem.cart_id == cart.cart_id).delete()

    db.commit()
    db.refresh(order)

    print(f"[Payment] Order created: {order.order_id} for payment {payment.order_id}")
    return order


# ============================================================
# CANCEL PAGE
# ============================================================

@router.get("/cancel/{order_id}", response_class=HTMLResponse)
async def cancel_page(order_id: str, request: Request, db: Session = Depends(get_db)):
    """Trang hủy thanh toán"""
    payment_service = PaymentService(db)
    payment_service.get_payment_by_order_id(order_id)
    current_user = _get_current_user(request, db)
    cart_count = _get_cart_count(request, db)

    return templates.TemplateResponse(
        "Checkout/cancel.html",
        {
            "request": request,
            "page_title": "Hủy thanh toán",
            "order_id": order_id,
            "current_user": current_user,
            "cart_count": cart_count,
        }
    )


# ============================================================
# EXPIRED PAGE
# ============================================================

@router.get("/expired/{order_id}", response_class=HTMLResponse)
async def expired_page(order_id: str, request: Request, db: Session = Depends(get_db)):
    """Trang hết hạn thanh toán"""
    current_user = _get_current_user(request, db)
    cart_count = _get_cart_count(request, db)

    return templates.TemplateResponse(
        "Checkout/expired.html",
        {
            "request": request,
            "page_title": "Thanh toán hết hạn",
            "order_id": order_id,
            "current_user": current_user,
            "cart_count": cart_count,
        }
    )


# Templates
templates = None

def set_templates(t):
    global templates
    templates = t
