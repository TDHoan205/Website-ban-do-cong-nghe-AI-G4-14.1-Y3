"""
Admin Controller - Trang quan tri he thong (Full CRUD)
"""
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from Data.database import get_db
from Services.AuthService import AuthService
from Models.Account import Account, Role
from Models.Product import Product
from Models.Category import Category
from Models.Supplier import Supplier
from Models.Order import Order, OrderItem
from Models.Order import OrderStatus
import json

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
            "page_title": "Quan ly San pham",
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
            "page_title": "Quan ly Don hang",
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
            "page_title": "Quan ly Danh muc",
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
            "page_title": f"Don hang #{order_id}",
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
        return JSONResponse({"success": False, "error": "Thong tin bat buoc"}, status_code=400)

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
        return JSONResponse({"success": False, "error": "Khong tim thay tai khoan"}, status_code=404)

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
        return JSONResponse({"success": False, "error": "Email da duoc su dung"}, status_code=400)

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
        return JSONResponse({"success": False, "error": "Khong the xoa tai khoan cua chinh minh"}, status_code=400)

    account = db.query(Account).filter(Account.account_id == account_id).first()
    if not account:
        return JSONResponse({"success": False, "error": "Khong tim thay tai khoan"}, status_code=404)

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
        return JSONResponse({"success": False, "error": "Khong tim thay"}, status_code=404)

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
        return JSONResponse({"success": False, "error": "Ten danh muc khong duoc trong"}, status_code=400)

    existing = db.query(Category).filter(Category.name == name).first()
    if existing:
        return JSONResponse({"success": False, "error": "Ten danh muc da ton tai"}, status_code=400)

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
        return JSONResponse({"success": False, "error": "Khong tim thay danh muc"}, status_code=404)

    form = await request.form()
    name = form.get("name", "").strip()
    description = form.get("description", "").strip()
    display_order = int(form.get("display_order", 0))
    is_active = form.get("is_active", "true").lower() == "true"

    if not name:
        return JSONResponse({"success": False, "error": "Ten danh muc khong duoc trong"}, status_code=400)

    existing = db.query(Category).filter(
        Category.name == name,
        Category.category_id != category_id
    ).first()
    if existing:
        return JSONResponse({"success": False, "error": "Ten danh muc da ton tai"}, status_code=400)

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
        return JSONResponse({"success": False, "error": "Khong tim thay danh muc"}, status_code=404)

    # Check if has products
    has_products = db.query(Product).filter(Product.category_id == category_id).count() > 0
    if has_products:
        return JSONResponse({
            "success": False,
            "error": "Danh muc co san pham, khong the xoa. Hay xoa hoac chuyen san pham truoc."
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
        return JSONResponse({"success": False, "error": "Khong tim thay"}, status_code=404)

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
        return JSONResponse({"success": False, "error": "Ten va gia san pham khong hop le"}, status_code=400)

    prod = Product(
        name=name,
        price=price,
        original_price=original_price,
        description=description,
        image_url=image_url or None,
        stock_quantity=stock,
        category_id=int(category_id) if category_id else None,
        supplier_id=int(supplier_id) if supplier_id else None,
        is_available=is_available,
        is_new=is_new,
        is_hot=is_hot,
        discount_percent=discount,
        rating=4.5,
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
        return JSONResponse({"success": False, "error": "Khong tim thay san pham"}, status_code=404)

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
        return JSONResponse({"success": False, "error": "Ten va gia san pham khong hop le"}, status_code=400)

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
        return JSONResponse({"success": False, "error": "Khong tim thay san pham"}, status_code=404)

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
        return JSONResponse({"success": False, "error": "Khong tim thay"}, status_code=404)

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
        }
    })


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
        return JSONResponse({"success": False, "error": "Khong tim thay don hang"}, status_code=404)

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
        return JSONResponse({"success": False, "error": "Khong tim thay don hang"}, status_code=404)

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
        return JSONResponse({"success": False, "error": "Ten nha cung cap khong duoc trong"}, status_code=400)

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
        return JSONResponse({"success": False, "error": "Khong tim thay nha cung cap"}, status_code=404)

    form = await request.form()
    name = form.get("name", "").strip()
    contact_person = form.get("contact_person", "").strip()
    phone = form.get("phone", "").strip()
    email = form.get("email", "").strip()
    address = form.get("address", "").strip()
    is_active = form.get("is_active", "true").lower() == "true"

    if not name:
        return JSONResponse({"success": False, "error": "Ten nha cung cap khong duoc trong"}, status_code=400)

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
        return JSONResponse({"success": False, "error": "Khong tim thay nha cung cap"}, status_code=404)

    has_products = db.query(Product).filter(Product.supplier_id == supplier_id).count() > 0
    if has_products:
        return JSONResponse({
            "success": False,
            "error": "Nha cung cap co san pham, khong the xoa."
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
        return JSONResponse({"success": False, "error": "Khong tim thay"}, status_code=404)

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
