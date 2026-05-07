"""
Admin Controller - Quan tri he thong
"""
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from Data.database import get_db
from Models.Order import Order, OrderStatus
from Models.Product import Product
from Models.Account import Account
from Utilities.auth import require_account
from datetime import datetime, timedelta

router = APIRouter(prefix="/Admin")

templates = None


def set_templates(t):
    global templates
    templates = t

def _check_admin(request: Request, db: Session):
    try:
        account = require_account(request, db)
        if account.role and account.role.role_name == "Admin":
            return account
    except:
        pass
    return None

@router.get("/Dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    """Trang dashboard quan tri"""
    admin = _check_admin(request, db)
    if not admin:
        return RedirectResponse(url="/Auth/Login?next=/Admin/Dashboard", status_code=302)

    # Thống kê tổng hợp
    total_orders = db.query(Order).count()
    total_products = db.query(Product).count()
    total_accounts = db.query(Account).count()
    
    # Doanh thu tháng này
    start_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_revenue = db.query(Order).filter(
        Order.order_date >= start_of_month,
        Order.status == OrderStatus.DELIVERED
    ).all()
    total_revenue = sum(float(o.total_amount) for o in monthly_revenue)

    # Đơn hàng gần đây
    recent_orders = db.query(Order).order_by(Order.order_date.desc()).limit(10).all()

    return templates.TemplateResponse(
        "Admin/dashboard.html",
        {
            "request": request,
            "page_title": "Bảng điều khiển quản trị",
            "stats": {
                "total_orders": total_orders,
                "total_products": total_products,
                "total_accounts": total_accounts,
                "total_revenue": total_revenue
            },
            "recent_orders": recent_orders
        }
    )
