"""
Payment Controller - Thanh toán QR Banking
"""
from fastapi import APIRouter, Request, Depends, Form, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
from typing import Optional

from Data.database import get_db, engine
from Services.CartService import CartService
from Services.PaymentService import PaymentService, BANK_CONFIG
from Services.AuthService import AuthService
from Utilities.auth import require_account
from Utilities.http import is_ajax_request
from Models.Payment import PaymentStatus

router = APIRouter(prefix="/Checkout")


def _ensure_payment_schema():
    """Tao bang Payments neu local DB cu chua co."""
    with engine.begin() as connection:
        connection.execute(text("""
            IF OBJECT_ID('Payments', 'U') IS NULL
            BEGIN
                CREATE TABLE Payments (
                    payment_id INT IDENTITY(1,1) PRIMARY KEY,
                    order_id NVARCHAR(50) NOT NULL UNIQUE,
                    account_id INT NULL,
                    amount BIGINT NOT NULL,
                    payment_method NVARCHAR(20) NOT NULL DEFAULT 'QR_BANKING',
                    transaction_code NVARCHAR(100) NULL,
                    transfer_content NVARCHAR(200) NULL,
                    status NVARCHAR(20) NOT NULL DEFAULT 'PENDING',
                    qr_data NVARCHAR(MAX) NULL,
                    qr_image_base64 NVARCHAR(MAX) NULL,
                    bank_code NVARCHAR(20) NULL,
                    bank_account NVARCHAR(50) NULL,
                    bank_account_name NVARCHAR(200) NULL,
                    created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
                    paid_at DATETIME2 NULL,
                    expires_at DATETIME2 NULL,
                    verified_by NVARCHAR(50) NULL,
                    notes NVARCHAR(500) NULL,
                    CONSTRAINT FK_Payments_Accounts_Runtime_Controller FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
                )
            END
        """))


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
    _ensure_payment_schema()

    try:
        account = require_account(request, db)
    except HTTPException:
        return RedirectResponse(url="/Auth/Login", status_code=303)

    cart_service = CartService(db)
    cart = cart_service.get_or_create_cart(account.account_id)
    items = cart_service.get_cart_items(cart.cart_id)

    if not items:
        return RedirectResponse(url="/Cart/", status_code=303)

    # Kiểm tra các sản phẩm có variants nhưng chưa chọn option
    unselected_items = []
    for item in items:
        if item.variant_id:
            continue
        # Kiểm tra sản phẩm này có variants không
        from Models.Product import ProductVariant
        has_variants = db.query(ProductVariant).filter(
            ProductVariant.product_id == item.product_id,
            ProductVariant.is_active == True
        ).count() > 0
        if has_variants:
            unselected_items.append(item)

    if unselected_items:
        # Chuyển về giỏ hàng kèm thông báo
        names = ", ".join([item.product.name if item.product else f"Sản phẩm #{item.product_id}" for item in unselected_items[:3]])
        if len(unselected_items) > 3:
            names += f" và {len(unselected_items) - 3} sản phẩm khác"
        from fastapi import Query
        import urllib.parse
        msg = urllib.parse.quote(f"Các sản phẩm sau chưa chọn option (màu/dung lượng): {names}")
        return RedirectResponse(url=f"/Cart/?error={msg}", status_code=303)

    # Tính tổng tiền (đã có VAT 10%)
    subtotal = sum(item.subtotal for item in items)
    tax = subtotal * 0.10
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
    _ensure_payment_schema()
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
    _ensure_payment_schema()
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

    # Kiểm tra xem đơn hàng đã được tạo trước đó chưa để tránh tạo trùng lặp (Double Order)
    from Models.Order import Order
    existing_order = db.query(Order).filter(Order.notes.like(f"%{order_id}%")).first()
    if existing_order:
        return JSONResponse({
            "success": True,
            "message": "Đã xác nhận thanh toán trước đó",
            "order_id": existing_order.order_id,
            "redirect_url": f"/Checkout/success/{existing_order.order_id}"
        })

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

    from Models.Order import Order
    payment_service = PaymentService(db)
    order = None
    payment_info = None

    if order_id.isdigit():
        # URL dạng: /Checkout/success/1 (Order.order_id)
        order = db.query(Order).filter(Order.order_id == int(order_id)).first()
        if order:
            # Trích xuất mã Payment (DHxxxxx) từ notes hoặc lấy payment gần nhất
            import re
            match = re.search(r'(DH\d+[A-Z0-9]+)', order.notes or '')
            if match:
                payment_info = payment_service.get_payment_display_info(match.group(1))
            
            if not payment_info:
                from Models.Payment import Payment, PaymentStatus
                from sqlalchemy import desc
                payment = db.query(Payment).filter(
                    Payment.account_id == account.account_id,
                    Payment.status == PaymentStatus.PAID
                ).order_by(desc(Payment.created_at)).first()
                if payment:
                    payment_info = payment_service.get_payment_display_info(payment.order_id)
    else:
        # URL dạng: /Checkout/success/DH0525... (Payment.order_id)
        payment_info = payment_service.get_payment_display_info(order_id)
        if payment_info:
            order = db.query(Order).filter(Order.notes.like(f"%{order_id}%")).first()

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
        total_amount=float(payment.amount),
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
            unit_price=unit_price,
            subtotal=subtotal,
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
