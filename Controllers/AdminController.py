"""
Admin Controller - Trang quan tri he thong (Full CRUD)
"""
from fastapi import APIRouter, Request, Depends, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, cast, Date
from sqlalchemy.orm import joinedload
from decimal import Decimal
from Data.database import get_db
from Models import (
    Account, Employee, Role, Category, Supplier,
    Product, ProductVariant, ProductImage,
    Inventory, ReceiptShipment, Cart, CartItem,
    Order, OrderItem, ChatSession, ChatMessage,
    AIConversationLog, FAQ, Notification, KnowledgeChunk
)
from Services.AuthService import AuthService
from datetime import datetime, timedelta
from Data.database import get_db
from Services.AuthService import AuthService
from Models.Account import Account, Role
from Models.Product import Product, ProductVariant, ProductImage
from Models.Category import Category
from Models.Supplier import Supplier
from Models.Order import Order, OrderItem
from Models.Order import OrderStatus
from Models.Chat import ChatSession, ChatMessage
from fastapi.templating import Jinja2Templates
import json
import os
import shutil
import uuid

templates = Jinja2Templates(directory="Views")

router = APIRouter(prefix="/Admin")


def _check_admin(request: Request, db: Session):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Login required")
    auth_service = AuthService(db)
    account = auth_service.get_current_account_from_token(token)
    if not account or account.role_name != "Admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return account


def _admin_json(request: Request, db: Session):
    try:
        admin = _check_admin(request, db)
        return admin
    except HTTPException:
        return None


# =====================================================================
# PAGES
# =====================================================================

@router.get("/Dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    try:
        admin = _check_admin(request, db)
    except HTTPException as e:
        if e.status_code == 401:
            return RedirectResponse(url="/Auth/Admin", status_code=303)
        raise

    # --- Basic stats (existing) ---
    total_products = db.query(Product).count()
    total_customers = db.query(Account).join(Role).filter(Role.role_name == "Customer").count()
    total_admins = db.query(Account).join(Role).filter(Role.role_name == "Admin").count()
    total_orders = db.query(Order).count()
    total_revenue = db.query(func.sum(Order.total_amount)).scalar() or 0
    pending_orders = db.query(Order).filter(
        or_(Order.status == "Pending", Order.status == "cho_xu_ly")
    ).count()

    recent_orders = db.query(Order).order_by(Order.created_at.desc()).limit(5).all()
    top_products = db.query(Product).filter(
        Product.is_available == True
    ).order_by(Product.rating.desc()).limit(5).all()

    # --- Financial Report: Time boundaries ---
    now = datetime.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=now.weekday())  # Monday
    month_start = today_start.replace(day=1)
    year_start = today_start.replace(month=1, day=1)

    # --- Revenue by period (only Delivered orders) ---
    def _revenue_in_period(start_dt):
        result = db.query(func.sum(Order.total_amount)).filter(
            Order.order_date >= start_dt,
            Order.status == OrderStatus.DELIVERED
        ).scalar()
        return float(result) if result else 0

    revenue_today = _revenue_in_period(today_start)
    revenue_week = _revenue_in_period(week_start)
    revenue_month = _revenue_in_period(month_start)
    revenue_year = _revenue_in_period(year_start)

    # --- Products sold by period ---
    def _products_sold_in_period(start_dt):
        result = db.query(func.sum(OrderItem.quantity)).join(
            Order, Order.order_id == OrderItem.order_id
        ).filter(
            Order.order_date >= start_dt,
            Order.status == OrderStatus.DELIVERED
        ).scalar()
        return int(result) if result else 0

    products_sold_today = _products_sold_in_period(today_start)
    products_sold_month = _products_sold_in_period(month_start)

    # --- New orders today ---
    orders_today = db.query(Order).filter(
        Order.created_at >= today_start
    ).count()

    # --- Average order value ---
    avg_order_value = db.query(func.avg(Order.total_amount)).filter(
        Order.status == OrderStatus.DELIVERED
    ).scalar()
    avg_order_value = float(avg_order_value) if avg_order_value else 0

    # --- Cancellation rate ---
    cancelled_orders = db.query(Order).filter(
        Order.status == OrderStatus.CANCELLED
    ).count()
    cancel_rate = round((cancelled_orders / total_orders * 100), 1) if total_orders > 0 else 0

    # --- 7-day revenue chart data ---
    chart_labels = []
    chart_data = []
    for i in range(6, -1, -1):
        day = today_start - timedelta(days=i)
        next_day = day + timedelta(days=1)
        day_revenue = db.query(func.sum(Order.total_amount)).filter(
            Order.order_date >= day,
            Order.order_date < next_day,
            Order.status == OrderStatus.DELIVERED
        ).scalar()
        chart_labels.append(day.strftime("%d/%m"))
        chart_data.append(float(day_revenue) if day_revenue else 0)

    # --- Top 5 best selling products this month ---
    top_selling = db.query(
        OrderItem.product_id,
        OrderItem.product_name,
        func.sum(OrderItem.quantity).label("total_qty"),
        func.sum(OrderItem.subtotal).label("total_revenue")
    ).join(Order, Order.order_id == OrderItem.order_id).filter(
        Order.order_date >= month_start,
        Order.status == OrderStatus.DELIVERED
    ).group_by(
        OrderItem.product_id, OrderItem.product_name
    ).order_by(
        func.sum(OrderItem.quantity).desc()
    ).limit(5).all()

    top_selling_list = [
        {
            "product_id": r.product_id,
            "product_name": r.product_name,
            "total_qty": int(r.total_qty or 0),
            "total_revenue": float(r.total_revenue or 0),
        }
        for r in top_selling
    ]

    # --- Low stock products (stock <= 5) ---
    low_stock_products = db.query(Product).filter(
        Product.stock_quantity <= 5,
        Product.is_available == True
    ).order_by(Product.stock_quantity.asc()).limit(10).all()

    # --- New customers this month ---
    new_customers_month = db.query(Account).join(Role).filter(
        Role.role_name == "Customer",
        Account.created_at >= month_start
    ).count()

    return templates.TemplateResponse(
        "Admin/dashboard.html",
        {
            "request": request,
            "page_title": "Dashboard",
            "admin": admin,
            "stats": {
                "total_products": total_products,
                "total_customers": total_customers,
                "total_admins": total_admins,
                "total_orders": total_orders,
                "pending_orders": pending_orders,
                "total_revenue": total_revenue,
            },
            "recent_orders": recent_orders,
            "top_products": top_products,
            "order_statuses": OrderStatus.STATUSES,
            # --- Financial report data ---
            "finance": {
                "revenue_today": revenue_today,
                "revenue_week": revenue_week,
                "revenue_month": revenue_month,
                "revenue_year": revenue_year,
                "products_sold_today": products_sold_today,
                "products_sold_month": products_sold_month,
                "orders_today": orders_today,
                "avg_order_value": avg_order_value,
                "cancel_rate": cancel_rate,
                "cancelled_orders": cancelled_orders,
                "new_customers_month": new_customers_month,
            },
            "chart_labels": json.dumps(chart_labels),
            "chart_data": json.dumps(chart_data),
            "top_selling": top_selling_list,
            "low_stock_products": low_stock_products,
        }
    )


@router.get("/Products", response_class=HTMLResponse)
async def admin_products(request: Request, db: Session = Depends(get_db)):
    try:
        admin = _check_admin(request, db)
    except HTTPException as e:
        if e.status_code == 401:
            return RedirectResponse(url="/Auth/Admin", status_code=303)
        raise

    products = db.query(Product).order_by(Product.created_at.desc()).all()
    categories = db.query(Category).filter(Category.is_active == True).all()
    suppliers = db.query(Supplier).filter(Supplier.is_active == True).all()

    return templates.TemplateResponse(
        "Admin/products.html",
        {
            "request": request,
            "page_title": "Quản lý Sản phẩm",
            "admin": admin,
            "products": products,
            "categories": categories,
            "suppliers": suppliers,
        }
    )


@router.get("/Accounts", response_class=HTMLResponse)
async def admin_accounts(request: Request, db: Session = Depends(get_db)):
    try:
        admin = _check_admin(request, db)
    except HTTPException as e:
        if e.status_code == 401:
            return RedirectResponse(url="/Auth/Admin", status_code=303)
        raise

    accounts = db.query(Account).order_by(Account.created_at.desc()).all()
    roles = db.query(Role).all()

    return templates.TemplateResponse(
        "Admin/accounts.html",
        {
            "request": request,
            "page_title": "Quan ly Tai khoan",
            "admin": admin,
            "accounts": accounts,
            "roles": roles,
        }
    )


@router.get("/Orders", response_class=HTMLResponse)
async def admin_orders(request: Request, db: Session = Depends(get_db)):
    try:
        admin = _check_admin(request, db)
    except HTTPException as e:
        if e.status_code == 401:
            return RedirectResponse(url="/Auth/Admin", status_code=303)
        raise

    orders = db.query(Order).order_by(Order.created_at.desc()).all()

    return templates.TemplateResponse(
        "Admin/orders.html",
        {
            "request": request,
            "page_title": "Quản lý Đơn hàng",
            "admin": admin,
            "orders": orders,
            "order_statuses": OrderStatus.STATUSES,
        }
    )


@router.get("/Categories", response_class=HTMLResponse)
async def admin_categories(request: Request, db: Session = Depends(get_db)):
    try:
        admin = _check_admin(request, db)
    except HTTPException as e:
        if e.status_code == 401:
            return RedirectResponse(url="/Auth/Admin", status_code=303)
        raise

    categories = db.query(Category).order_by(Category.display_order, Category.name).all()

    return templates.TemplateResponse(
        "Admin/categories.html",
        {
            "request": request,
            "page_title": "Quản lý Danh mục",
            "admin": admin,
            "categories": categories,
        }
    )


@router.get("/Suppliers", response_class=HTMLResponse)
async def admin_suppliers(request: Request, db: Session = Depends(get_db)):
    try:
        admin = _check_admin(request, db)
    except HTTPException as e:
        if e.status_code == 401:
            return RedirectResponse(url="/Auth/Admin", status_code=303)
        raise

    suppliers = db.query(Supplier).order_by(Supplier.created_at.desc()).all()

    return templates.TemplateResponse(
        "Admin/suppliers.html",
        {
            "request": request,
            "page_title": "Quan ly Nha cung cap",
            "admin": admin,
            "suppliers": suppliers,
        }
    )


# =====================================================================
# API: CHATS (ADMIN)
# =====================================================================

@router.get("/Chats", response_class=HTMLResponse)
async def admin_chats(request: Request, db: Session = Depends(get_db)):
    try:
        admin = _check_admin(request, db)
    except HTTPException as e:
        if e.status_code == 401:
            return RedirectResponse(url="/Auth/Admin", status_code=303)
        raise

    sessions = db.query(ChatSession).order_by(ChatSession.started_at.desc()).all()

    return templates.TemplateResponse(
        "Admin/chats.html",
        {
            "request": request,
            "page_title": "Lịch sử Chat",
            "admin": admin,
            "sessions": sessions,
        }
    )


@router.get("/API/Chats/{session_uuid}")
async def api_get_chat_messages(request: Request, session_uuid: str, db: Session = Depends(get_db)):
    try:
        admin = _check_admin(request, db)
    except HTTPException:
        return JSONResponse({"success": False, "error": "Unauthorized"}, status_code=401)

    session = db.query(ChatSession).filter(ChatSession.session_uuid == session_uuid).first()
    if not session:
        return JSONResponse({"success": False, "error": "Không tìm thấy"}, status_code=404)

    messages = db.query(ChatMessage).filter(ChatMessage.session_id == session.session_id).order_by(ChatMessage.created_at.asc()).all()

    msg_list = []
    for m in messages:
        msg_list.append({
            "message_id": m.message_id,
            "sender": m.sender_type,
            "content": m.message_content,
            "created_at": m.created_at.strftime('%H:%M:%S %d/%m/%Y') if m.created_at else ""
        })

    return JSONResponse({
        "success": True,
        "messages": msg_list
    })


# =====================================================================
# ORDER DETAIL
# =====================================================================

@router.get("/Orders/{order_id}", response_class=HTMLResponse)
async def order_detail(request: Request, order_id: int, db: Session = Depends(get_db)):
    try:
        admin = _check_admin(request, db)
    except HTTPException as e:
        if e.status_code == 401:
            return RedirectResponse(url="/Auth/Admin", status_code=303)
        raise

    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        return RedirectResponse(url="/Admin/Orders", status_code=303)

    items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()

    return templates.TemplateResponse(
        "Admin/order_detail.html",
        {
            "request": request,
            "page_title": f"Đơn hàng #{order_id}",
            "admin": admin,
            "order": order,
            "items": items,
            "order_statuses": OrderStatus.STATUSES,
        }
    )


# =====================================================================
# API: ACCOUNTS
# =====================================================================

@router.post("/API/Accounts")
async def api_create_account(
    request: Request,
    db: Session = Depends(get_db)
):
    """Them tai khoan moi"""
    try:
        admin = _check_admin(request, db)
    except HTTPException:
        return JSONResponse({"success": False, "error": "Unauthorized"}, status_code=401)

    form = await request.form()
    username = form.get("username", "").strip()
    email = form.get("email", "").strip()
    password = form.get("password", "").strip()
    full_name = form.get("full_name", "").strip()
    phone = form.get("phone", "").strip()
    address = form.get("address", "").strip()
    role_id = int(form.get("role_id", 1))

    if not username or not email or not password:
        return JSONResponse({"success": False, "error": "Thông tin bắt buộc"}, status_code=400)

    # Check exists
    existing = db.query(Account).filter(
        or_(Account.username == username, Account.email == email)
    ).first()
    if existing:
        return JSONResponse({"success": False, "error": "Username hoac email da ton tai"}, status_code=400)

    auth_svc = AuthService(db)
    account = Account(
        username=username,
        email=email,
        password_hash=auth_svc.hash_password(password),
        full_name=full_name,
        phone=phone,
        address=address,
        role_id=role_id,
        is_active=True
    )
    db.add(account)
    db.commit()
    return JSONResponse({"success": True, "account_id": account.account_id})


@router.put("/API/Accounts/{account_id}")
async def api_update_account(
    request: Request,
    account_id: int,
    db: Session = Depends(get_db)
):
    """Cap nhat tai khoan"""
    try:
        admin = _check_admin(request, db)
    except HTTPException:
        return JSONResponse({"success": False, "error": "Unauthorized"}, status_code=401)

    account = db.query(Account).filter(Account.account_id == account_id).first()
    if not account:
        return JSONResponse({"success": False, "error": "Không tìm thấy tài khoản"}, status_code=404)

    form = await request.form()
    email = form.get("email", "").strip()
    full_name = form.get("full_name", "").strip()
    phone = form.get("phone", "").strip()
    address = form.get("address", "").strip()
    role_id = int(form.get("role_id", account.role_id))
    is_active = form.get("is_active", "true").lower() == "true"

    # Check email conflict
    existing = db.query(Account).filter(
        Account.email == email,
        Account.account_id != account_id
    ).first()
    if existing:
        return JSONResponse({"success": False, "error": "Email đã được sử dụng"}, status_code=400)

    account.email = email
    account.full_name = full_name
    account.phone = phone
    account.address = address
    account.role_id = role_id
    account.is_active = is_active
    db.commit()
    return JSONResponse({"success": True})


@router.delete("/API/Accounts/{account_id}")
async def api_delete_account(
    request: Request,
    account_id: int,
    db: Session = Depends(get_db)
):
    """Xoa tai khoan"""
    try:
        admin = _check_admin(request, db)
    except HTTPException:
        return JSONResponse({"success": False, "error": "Unauthorized"}, status_code=401)

    if account_id == admin.account_id:
        return JSONResponse({"success": False, "error": "Không thể xóa tài khoản của chính mình"}, status_code=400)

    account = db.query(Account).filter(Account.account_id == account_id).first()
    if not account:
        return JSONResponse({"success": False, "error": "Không tìm thấy tài khoản"}, status_code=404)

    db.delete(account)
    db.commit()
    return JSONResponse({"success": True})


@router.get("/API/Accounts/{account_id}")
async def api_get_account(
    request: Request,
    account_id: int,
    db: Session = Depends(get_db)
):
    """Lay thong tin tai khoan"""
    try:
        admin = _check_admin(request, db)
    except HTTPException:
        return JSONResponse({"success": False, "error": "Unauthorized"}, status_code=401)

    account = db.query(Account).filter(Account.account_id == account_id).first()
    if not account:
        return JSONResponse({"success": False, "error": "Không tìm thấy"}, status_code=404)

    return JSONResponse({
        "success": True,
        "account": {
            "account_id": account.account_id,
            "username": account.username,
            "email": account.email,
            "full_name": account.full_name or "",
            "phone": account.phone or "",
            "address": account.address or "",
            "role_id": account.role_id,
            "role_name": account.role_name,
            "is_active": account.is_active,
        }
    })


# =====================================================================
# API: CATEGORIES
# =====================================================================

@router.post("/API/Categories")
async def api_create_category(request: Request, db: Session = Depends(get_db)):
    try:
        admin = _check_admin(request, db)
    except HTTPException:
        return JSONResponse({"success": False, "error": "Unauthorized"}, status_code=401)

    form = await request.form()
    name = form.get("name", "").strip()
    description = form.get("description", "").strip()
    display_order = int(form.get("display_order", 0))
    is_active = form.get("is_active", "true").lower() == "true"

    if not name:
        return JSONResponse({"success": False, "error": "Tên danh mục không được để trống"}, status_code=400)

    existing = db.query(Category).filter(Category.name == name).first()
    if existing:
        return JSONResponse({"success": False, "error": "Tên danh mục đã tồn tại"}, status_code=400)

    cat = Category(
        name=name,
        description=description,
        display_order=display_order,
        is_active=is_active
    )
    db.add(cat)
    db.commit()
    return JSONResponse({"success": True, "category_id": cat.category_id})


@router.put("/API/Categories/{category_id}")
async def api_update_category(request: Request, category_id: int, db: Session = Depends(get_db)):
    try:
        admin = _check_admin(request, db)
    except HTTPException:
        return JSONResponse({"success": False, "error": "Unauthorized"}, status_code=401)

    cat = db.query(Category).filter(Category.category_id == category_id).first()
    if not cat:
        return JSONResponse({"success": False, "error": "Không tìm thấy danh mục"}, status_code=404)

    form = await request.form()
    name = form.get("name", "").strip()
    description = form.get("description", "").strip()
    display_order = int(form.get("display_order", 0))
    is_active = form.get("is_active", "true").lower() == "true"

    if not name:
        return JSONResponse({"success": False, "error": "Tên danh mục không được để trống"}, status_code=400)

    existing = db.query(Category).filter(
        Category.name == name,
        Category.category_id != category_id
    ).first()
    if existing:
        return JSONResponse({"success": False, "error": "Tên danh mục đã tồn tại"}, status_code=400)

    cat.name = name
    cat.description = description
    cat.display_order = display_order
    cat.is_active = is_active
    db.commit()
    return JSONResponse({"success": True})


@router.delete("/API/Categories/{category_id}")
async def api_delete_category(request: Request, category_id: int, db: Session = Depends(get_db)):
    try:
        admin = _check_admin(request, db)
    except HTTPException:
        return JSONResponse({"success": False, "error": "Unauthorized"}, status_code=401)

    cat = db.query(Category).filter(Category.category_id == category_id).first()
    if not cat:
        return JSONResponse({"success": False, "error": "Không tìm thấy danh mục"}, status_code=404)

    # Check if has products
    has_products = db.query(Product).filter(Product.category_id == category_id).count() > 0
    if has_products:
        return JSONResponse({
            "success": False,
            "error": "Danh mục có sản phẩm, không thể xóa. Hãy xóa hoặc chuyển sản phẩm trước."
        }, status_code=400)

    db.delete(cat)
    db.commit()
    return JSONResponse({"success": True})


@router.get("/API/Categories/{category_id}")
async def api_get_category(request: Request, category_id: int, db: Session = Depends(get_db)):
    try:
        admin = _check_admin(request, db)
    except HTTPException:
        return JSONResponse({"success": False, "error": "Unauthorized"}, status_code=401)

    cat = db.query(Category).filter(Category.category_id == category_id).first()
    if not cat:
        return JSONResponse({"success": False, "error": "Không tìm thấy"}, status_code=404)

    return JSONResponse({
        "success": True,
        "category": {
            "category_id": cat.category_id,
            "name": cat.name,
            "description": cat.description or "",
            "display_order": cat.display_order or 0,
            "is_active": cat.is_active,
        }
    })


# =====================================================================
# API: UPLOAD
# =====================================================================

@router.post("/API/Upload")
async def api_upload_image(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload hình ảnh lên server"""
    try:
        admin = _check_admin(request, db)
    except HTTPException:
        return JSONResponse({"success": False, "error": "Unauthorized"}, status_code=401)

    # Validate file type
    if not file.content_type.startswith("image/"):
        return JSONResponse({"success": False, "error": "Chỉ chấp nhận file hình ảnh"}, status_code=400)

    # Create directory if not exists
    upload_dir = os.path.join("wwwroot", "uploads", "products")
    os.makedirs(upload_dir, exist_ok=True)

    # Generate unique filename
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    filepath = os.path.join(upload_dir, filename)

    # Save file
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return JSONResponse({
        "success": True,
        "image_url": f"/static/uploads/products/{filename}"
    })


# =====================================================================
# API: PRODUCTS
# =====================================================================

@router.post("/API/Products")
async def api_create_product(request: Request, db: Session = Depends(get_db)):
    try:
        admin = _check_admin(request, db)
    except HTTPException:
        return JSONResponse({"success": False, "error": "Unauthorized"}, status_code=401)

    form = await request.form()
    name = form.get("name", "").strip()
    price = float(form.get("price", 0))
    description = form.get("description", "").strip()
    image_url = form.get("image_url", "").strip()
    stock = int(form.get("stock_quantity", 0))
    category_id = form.get("category_id")
    supplier_id = form.get("supplier_id")
    is_available = form.get("is_available", "true").lower() == "true"
    is_new = form.get("is_new", "false").lower() == "true"
    is_hot = form.get("is_hot", "false").lower() == "true"
    discount = int(form.get("discount_percent", 0))
    original_price = float(form.get("original_price", 0)) or None

    if not name or price <= 0:
        return JSONResponse({"success": False, "error": "Tên và giá sản phẩm không hợp lệ"}, status_code=400)

    prod = Product(
        name=name,
        price=Decimal(str(price)),
        original_price=Decimal(str(original_price)) if original_price else None,
        description=description,
        image_url=image_url or None,
        stock_quantity=stock,
        category_id=int(category_id) if category_id else None,
        supplier_id=int(supplier_id) if supplier_id else None,
        is_available=is_available,
        is_new=is_new,
        is_hot=is_hot,
        discount_percent=discount,
        rating=Decimal("4.5"),
    )
    db.add(prod)
    db.commit()
    return JSONResponse({"success": True, "product_id": prod.product_id})


@router.put("/API/Products/{product_id}")
async def api_update_product(request: Request, product_id: int, db: Session = Depends(get_db)):
    try:
        admin = _check_admin(request, db)
    except HTTPException:
        return JSONResponse({"success": False, "error": "Unauthorized"}, status_code=401)

    prod = db.query(Product).filter(Product.product_id == product_id).first()
    if not prod:
        return JSONResponse({"success": False, "error": "Không tìm thấy sản phẩm"}, status_code=404)

    form = await request.form()
    name = form.get("name", "").strip()
    price = float(form.get("price", 0))
    description = form.get("description", "").strip()
    image_url = form.get("image_url", "").strip()
    stock = int(form.get("stock_quantity", 0))
    category_id = form.get("category_id")
    supplier_id = form.get("supplier_id")
    is_available = form.get("is_available", "true").lower() == "true"
    is_new = form.get("is_new", "false").lower() == "true"
    is_hot = form.get("is_hot", "false").lower() == "true"
    discount = int(form.get("discount_percent", 0))
    original_price = float(form.get("original_price", 0)) or None

    if not name or price <= 0:
        return JSONResponse({"success": False, "error": "Tên và giá sản phẩm không hợp lệ"}, status_code=400)

    prod.name = name
    prod.price = price
    prod.original_price = original_price
    prod.description = description
    prod.image_url = image_url or None
    prod.stock_quantity = stock
    prod.category_id = int(category_id) if category_id else None
    prod.supplier_id = int(supplier_id) if supplier_id else None
    prod.is_available = is_available
    prod.is_new = is_new
    prod.is_hot = is_hot
    prod.discount_percent = discount
    db.commit()
    return JSONResponse({"success": True})


@router.delete("/API/Products/{product_id}")
async def api_delete_product(request: Request, product_id: int, db: Session = Depends(get_db)):
    try:
        admin = _check_admin(request, db)
    except HTTPException:
        return JSONResponse({"success": False, "error": "Unauthorized"}, status_code=401)

    prod = db.query(Product).filter(Product.product_id == product_id).first()
    if not prod:
        return JSONResponse({"success": False, "error": "Không tìm thấy sản phẩm"}, status_code=404)

    db.delete(prod)
    db.commit()
    return JSONResponse({"success": True})


@router.get("/API/Products/{product_id}")
async def api_get_product(request: Request, product_id: int, db: Session = Depends(get_db)):
    try:
        admin = _check_admin(request, db)
    except HTTPException:
        return JSONResponse({"success": False, "error": "Unauthorized"}, status_code=401)

    prod = db.query(Product).filter(Product.product_id == product_id).first()
    if not prod:
        return JSONResponse({"success": False, "error": "Không tìm thấy"}, status_code=404)

    # Safe load - use separate queries to avoid DB column errors
    try:
        variants = db.query(ProductVariant).filter(ProductVariant.product_id == product_id).all()
        product_images = db.query(ProductImage).filter(ProductImage.product_id == product_id).all()
    except Exception:
        variants = []
        product_images = []

    return JSONResponse({
        "success": True,
        "product": {
            "product_id": prod.product_id,
            "name": prod.name,
            "price": float(prod.price),
            "original_price": float(prod.original_price) if prod.original_price else 0,
            "description": prod.description or "",
            "image_url": prod.image_url or "",
            "stock_quantity": prod.stock_quantity or 0,
            "category_id": prod.category_id,
            "supplier_id": prod.supplier_id,
            "is_available": prod.is_available,
            "is_new": prod.is_new,
            "is_hot": prod.is_hot,
            "discount_percent": prod.discount_percent or 0,
            "variants": [
                {
                    "variant_id": v.variant_id,
                    "color": v.color or "",
                    "color_hex": getattr(v, "color_hex", "") or "",
                    "storage": v.storage or "",
                    "ram": v.ram or "",
                    "variant_name": v.variant_name or "",
                    "sku": v.sku or "",
                    "price": float(v.price) if v.price else None,
                    "stock_quantity": v.stock_quantity or 0,
                    "is_active": v.is_active,
                }
                for v in variants
            ],
            "product_images": [
                {"image_id": i.image_id, "image_url": i.image_url, "is_primary": i.is_primary}
                for i in product_images
            ],
        }
    })


# =====================================================================
# TRANG: CHỈNH SỬA SẢN PHẨM (với Variant Management)
# =====================================================================

@router.get("/Products/{product_id}/edit", response_class=HTMLResponse)
async def edit_product_page(request: Request, product_id: int, db: Session = Depends(get_db)):
    try:
        admin = _check_admin(request, db)
    except HTTPException:
        return RedirectResponse(url="/Admin/Login", status_code=303)

    prod = db.query(Product).filter(Product.product_id == product_id).first()
    if not prod:
        return RedirectResponse(url="/Admin/Products", status_code=303)

    categories = db.query(Category).filter(Category.is_active == True).all()
    suppliers = db.query(Supplier).filter(Supplier.is_active == True).all()

    # Safe load - use separate queries to avoid DB column errors
    try:
        variants_list = db.query(ProductVariant).filter(ProductVariant.product_id == product_id).all()
        all_images = db.query(ProductImage).filter(ProductImage.product_id == product_id).all()
    except Exception:
        variants_list = []
        all_images = []

    # Build variants_data
    variants_data = []
    for v in variants_list:
        imgs = [i for i in all_images if getattr(i, "variant_id", None) == v.variant_id]
        variants_data.append({
            "variant_id": v.variant_id,
            "color": v.color or "",
            "color_hex": getattr(v, "color_hex", "") or "",
            "storage": v.storage or "",
            "ram": v.ram or "",
            "variant_name": v.variant_name or "",
            "sku": v.sku or "",
            "price": float(v.price) if v.price else None,
            "original_price": float(v.original_price) if v.original_price else None,
            "stock_quantity": v.stock_quantity or 0,
            "display_order": v.display_order or 0,
            "is_active": v.is_active,
            "images": [
                {"image_id": i.image_id, "image_url": i.image_url,
                 "is_primary": i.is_primary, "display_order": i.display_order}
                for i in imgs
            ]
        })

    # Product-level images (no variant)
    product_images = [
        {"image_id": i.image_id, "image_url": i.image_url,
         "is_primary": i.is_primary, "display_order": i.display_order}
        for i in all_images if not getattr(i, "variant_id", None)
    ]

    return templates.TemplateResponse(
        "Admin/product_edit.html",
        {
            "request": request,
            "admin": admin,
            "product": prod,
            "categories": categories,
            "suppliers": suppliers,
            "variants": variants_data,
            "product_images": product_images,
        }
    )


# =====================================================================
# API: VARIANTS (CRUD)
# =====================================================================

@router.post("/API/Variants")
async def api_create_variant(request: Request, db: Session = Depends(get_db)):
    try:
        admin = _check_admin(request, db)
    except HTTPException:
        return JSONResponse({"success": False, "error": "Unauthorized"}, status_code=401)
    except Exception as e:
        return JSONResponse({"success": False, "error": f"Loi xac thuc: {str(e)}"}, status_code=500)

    form = await request.form()
    product_id = int(form.get("product_id", 0))
    if not db.query(Product).filter(Product.product_id == product_id).first():
        return JSONResponse({"success": False, "error": "Sản phẩm không tồn tại"}, status_code=404)

    try:
        variant = ProductVariant(
            product_id=product_id,
            color=form.get("color", "").strip() or None,
            color_hex=form.get("color_hex", "").strip() or None,
            storage=form.get("storage", "").strip() or None,
            ram=form.get("ram", "").strip() or None,
            variant_name=form.get("variant_name", "").strip() or None,
            sku=form.get("sku", "").strip() or None,
            price=float(form.get("price")) if form.get("price") else None,
            original_price=float(form.get("original_price")) if form.get("original_price") else None,
            stock_quantity=int(form.get("stock_quantity", 0)),
            display_order=int(form.get("display_order", 0)),
            is_active=True,
        )
        db.add(variant)
        db.commit()
        db.refresh(variant)
        return JSONResponse({"success": True, "variant_id": variant.variant_id})
    except Exception as e:
        db.rollback()
        return JSONResponse({"success": False, "error": f"Loi luu variant: {str(e)}"}, status_code=500)


@router.put("/API/Variants/{variant_id}")
async def api_update_variant(request: Request, variant_id: int, db: Session = Depends(get_db)):
    try:
        admin = _check_admin(request, db)
    except HTTPException:
        return JSONResponse({"success": False, "error": "Unauthorized"}, status_code=401)

    variant = db.query(ProductVariant).filter(ProductVariant.variant_id == variant_id).first()
    if not variant:
        return JSONResponse({"success": False, "error": "Không tìm thấy biến thể"}, status_code=404)

    form = await request.form()
    variant.color = form.get("color", "").strip() or None
    variant.color_hex = form.get("color_hex", "").strip() or None
    variant.storage = form.get("storage", "").strip() or None
    variant.ram = form.get("ram", "").strip() or None
    variant.variant_name = form.get("variant_name", "").strip() or None
    variant.sku = form.get("sku", "").strip() or None
    if form.get("price"):
        variant.price = float(form.get("price"))
    if form.get("original_price"):
        variant.original_price = float(form.get("original_price"))
    variant.stock_quantity = int(form.get("stock_quantity", 0))
    variant.display_order = int(form.get("display_order", 0))
    variant.is_active = form.get("is_active", "true") == "true"

    db.commit()
    return JSONResponse({"success": True})


@router.delete("/API/Variants/{variant_id}")
async def api_delete_variant(request: Request, variant_id: int, db: Session = Depends(get_db)):
    try:
        admin = _check_admin(request, db)
    except HTTPException:
        return JSONResponse({"success": False, "error": "Unauthorized"}, status_code=401)

    variant = db.query(ProductVariant).filter(ProductVariant.variant_id == variant_id).first()
    if not variant:
        return JSONResponse({"success": False, "error": "Không tìm thấy biến thể"}, status_code=404)

    db.delete(variant)
    db.commit()
    return JSONResponse({"success": True})


@router.get("/API/Variants/{variant_id}")
async def api_get_variant(request: Request, variant_id: int, db: Session = Depends(get_db)):
    try:
        admin = _check_admin(request, db)
    except HTTPException:
        return JSONResponse({"success": False, "error": "Unauthorized"}, status_code=401)

    variant = db.query(ProductVariant).filter(ProductVariant.variant_id == variant_id).first()
    if not variant:
        return JSONResponse({"success": False, "error": "Không tìm thấy"}, status_code=404)

    imgs = db.query(ProductImage).filter(
        ProductImage.variant_id == variant_id
    ).order_by(ProductImage.display_order).all()

    return JSONResponse({
        "success": True,
        "variant": {
            "variant_id": variant.variant_id,
            "product_id": variant.product_id,
            "color": variant.color or "",
            "color_hex": variant.color_hex or "",
            "storage": variant.storage or "",
            "ram": variant.ram or "",
            "variant_name": variant.variant_name or "",
            "sku": variant.sku or "",
            "price": float(variant.price) if variant.price else None,
            "original_price": float(variant.original_price) if variant.original_price else None,
            "stock_quantity": variant.stock_quantity or 0,
            "display_order": variant.display_order or 0,
            "is_active": variant.is_active,
            "images": [
                {"image_id": i.image_id, "image_url": i.image_url,
                 "is_primary": i.is_primary, "display_order": i.display_order}
                for i in imgs
            ]
        }
    })


# =====================================================================
# API: PRODUCT IMAGES
# =====================================================================

@router.post("/API/ProductImages")
async def api_upload_product_image(request: Request, db: Session = Depends(get_db)):
    try:
        admin = _check_admin(request, db)
    except HTTPException:
        return JSONResponse({"success": False, "error": "Unauthorized"}, status_code=401)
    except Exception as e:
        return JSONResponse({"success": False, "error": f"Loi xac thuc: {str(e)}"}, status_code=500)

    form = await request.form()
    product_id = int(form.get("product_id", 0))
    variant_id = form.get("variant_id")
    variant_id = int(variant_id) if variant_id and variant_id != "" else None
    file = form.get("file")
    is_primary = form.get("is_primary", "false") == "true"
    display_order = int(form.get("display_order", 0))

    if not db.query(Product).filter(Product.product_id == product_id).first():
        return JSONResponse({"success": False, "error": "Sản phẩm không tồn tại"}, status_code=404)

    if variant_id:
        variant = db.query(ProductVariant).filter(ProductVariant.variant_id == variant_id).first()
        if not variant:
            return JSONResponse({"success": False, "error": "Bien the khong ton tai"}, status_code=404)

    image_url = ""
    if file and hasattr(file, "filename"):
        upload_dir = os.path.join("wwwroot", "uploads", "products")
        os.makedirs(upload_dir, exist_ok=True)
        ext = os.path.splitext(file.filename)[1] if file.filename else ".jpg"
        filename = f"{uuid.uuid4()}{ext}"
        filepath = os.path.join(upload_dir, filename)
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        image_url = f"/static/uploads/products/{filename}"
    else:
        image_url = form.get("image_url", "").strip()

    if not image_url:
        return JSONResponse({"success": False, "error": "Không có ảnh nào được upload"}, status_code=400)

    try:
        if is_primary and variant_id:
            db.query(ProductImage).filter(
                ProductImage.variant_id == variant_id
            ).update({"is_primary": False})
        elif is_primary:
            db.query(ProductImage).filter(
                ProductImage.product_id == product_id,
                ProductImage.variant_id == None
            ).update({"is_primary": False})

        img = ProductImage(
            product_id=product_id,
            variant_id=variant_id,
            image_url=image_url,
            is_primary=is_primary,
            display_order=display_order,
        )
        db.add(img)
        db.commit()
        db.refresh(img)
        return JSONResponse({
            "success": True,
            "image": {
                "image_id": img.image_id,
                "image_url": img.image_url,
                "is_primary": img.is_primary,
                "display_order": img.display_order,
            }
        })
    except Exception as e:
        db.rollback()
        return JSONResponse({"success": False, "error": f"Loi luu anh: {str(e)}"}, status_code=500)


@router.delete("/API/ProductImages/{image_id}")
async def api_delete_product_image(request: Request, image_id: int, db: Session = Depends(get_db)):
    try:
        admin = _check_admin(request, db)
    except HTTPException:
        return JSONResponse({"success": False, "error": "Unauthorized"}, status_code=401)

    img = db.query(ProductImage).filter(ProductImage.image_id == image_id).first()
    if not img:
        return JSONResponse({"success": False, "error": "Không tìm thấy ảnh"}, status_code=404)

    db.delete(img)
    db.commit()
    return JSONResponse({"success": True})


@router.put("/API/ProductImages/{image_id}")
async def api_update_product_image(request: Request, image_id: int, db: Session = Depends(get_db)):
    try:
        admin = _check_admin(request, db)
    except HTTPException:
        return JSONResponse({"success": False, "error": "Unauthorized"}, status_code=401)

    img = db.query(ProductImage).filter(ProductImage.image_id == image_id).first()
    if not img:
        return JSONResponse({"success": False, "error": "Không tìm thấy ảnh"}, status_code=404)

    form = await request.form()
    if form.get("is_primary") == "true":
        db.query(ProductImage).filter(
            ProductImage.variant_id == img.variant_id,
            ProductImage.image_id != image_id
        ).update({"is_primary": False})
        img.is_primary = True
    img.display_order = int(form.get("display_order", 0))

    db.commit()
    return JSONResponse({"success": True})


# =====================================================================
# API: ORDERS
# =====================================================================

@router.put("/API/Orders/{order_id}/status")
async def api_update_order_status(
    request: Request,
    order_id: int,
    db: Session = Depends(get_db)
):
    try:
        admin = _check_admin(request, db)
    except HTTPException:
        return JSONResponse({"success": False, "error": "Unauthorized"}, status_code=401)

    form = await request.form()
    new_status = form.get("status", "").strip()

    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        return JSONResponse({"success": False, "error": "Không tìm thấy đơn hàng"}, status_code=404)

    valid_statuses = [s[0] for s in OrderStatus.STATUSES]
    if new_status not in valid_statuses:
        return JSONResponse({"success": False, "error": "Trang thai khong hop le"}, status_code=400)

    order.status = new_status
    db.commit()
    return JSONResponse({"success": True})


@router.delete("/API/Orders/{order_id}")
async def api_delete_order(request: Request, order_id: int, db: Session = Depends(get_db)):
    try:
        admin = _check_admin(request, db)
    except HTTPException:
        return JSONResponse({"success": False, "error": "Unauthorized"}, status_code=401)

    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        return JSONResponse({"success": False, "error": "Không tìm thấy đơn hàng"}, status_code=404)

    db.delete(order)
    db.commit()
    return JSONResponse({"success": True})


# =====================================================================
# API: SUPPLIERS
# =====================================================================

@router.post("/API/Suppliers")
async def api_create_supplier(request: Request, db: Session = Depends(get_db)):
    try:
        admin = _check_admin(request, db)
    except HTTPException:
        return JSONResponse({"success": False, "error": "Unauthorized"}, status_code=401)

    form = await request.form()
    name = form.get("name", "").strip()
    contact_person = form.get("contact_person", "").strip()
    phone = form.get("phone", "").strip()
    email = form.get("email", "").strip()
    address = form.get("address", "").strip()

    if not name:
        return JSONResponse({"success": False, "error": "Tên nhà cung cấp không được để trống"}, status_code=400)

    sup = Supplier(
        name=name,
        contact_person=contact_person,
        phone=phone,
        email=email,
        address=address,
        is_active=True
    )
    db.add(sup)
    db.commit()
    return JSONResponse({"success": True, "supplier_id": sup.supplier_id})


@router.put("/API/Suppliers/{supplier_id}")
async def api_update_supplier(request: Request, supplier_id: int, db: Session = Depends(get_db)):
    try:
        admin = _check_admin(request, db)
    except HTTPException:
        return JSONResponse({"success": False, "error": "Unauthorized"}, status_code=401)

    sup = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not sup:
        return JSONResponse({"success": False, "error": "Không tìm thấy nhà cung cấp"}, status_code=404)

    form = await request.form()
    name = form.get("name", "").strip()
    contact_person = form.get("contact_person", "").strip()
    phone = form.get("phone", "").strip()
    email = form.get("email", "").strip()
    address = form.get("address", "").strip()
    is_active = form.get("is_active", "true").lower() == "true"

    if not name:
        return JSONResponse({"success": False, "error": "Tên nhà cung cấp không được để trống"}, status_code=400)

    sup.name = name
    sup.contact_person = contact_person
    sup.phone = phone
    sup.email = email
    sup.address = address
    sup.is_active = is_active
    db.commit()
    return JSONResponse({"success": True})


@router.delete("/API/Suppliers/{supplier_id}")
async def api_delete_supplier(request: Request, supplier_id: int, db: Session = Depends(get_db)):
    try:
        admin = _check_admin(request, db)
    except HTTPException:
        return JSONResponse({"success": False, "error": "Unauthorized"}, status_code=401)

    sup = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not sup:
        return JSONResponse({"success": False, "error": "Không tìm thấy nhà cung cấp"}, status_code=404)

    has_products = db.query(Product).filter(Product.supplier_id == supplier_id).count() > 0
    if has_products:
        return JSONResponse({
            "success": False,
            "error": "Nhà cung cấp có sản phẩm, không thể xóa."
        }, status_code=400)

    db.delete(sup)
    db.commit()
    return JSONResponse({"success": True})


@router.get("/API/Suppliers/{supplier_id}")
async def api_get_supplier(request: Request, supplier_id: int, db: Session = Depends(get_db)):
    try:
        admin = _check_admin(request, db)
    except HTTPException:
        return JSONResponse({"success": False, "error": "Unauthorized"}, status_code=401)

    sup = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not sup:
        return JSONResponse({"success": False, "error": "Không tìm thấy"}, status_code=404)

    return JSONResponse({
        "success": True,
        "supplier": {
            "supplier_id": sup.supplier_id,
            "name": sup.name,
            "contact_person": sup.contact_person or "",
            "phone": sup.phone or "",
            "email": sup.email or "",
            "address": sup.address or "",
            "is_active": sup.is_active,
        }
    })


# =====================================================================
# Templates
# =====================================================================
templates = None

def set_templates(t):
    global templates
    templates = t
