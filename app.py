"""
Tech Store - Main Application Entry Point

Chạy: uvicorn app:app --reload
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, Response
import os
import re
from sqlalchemy import text

from Data.database import init_db, get_connection_info, engine
from Controllers import (
    HomeController,
    ProductsController,
    CartController,
    AuthController,
    ChatController,
    AccountsController,
    CategoriesController,
    SuppliersController,
    EmployeesController,
    InventoryController,
    OrdersController,
    OrderItemsController,
    ReceiptShipmentsController,
    CartItemsController,
    ShopController,
    StatisticsController,
    AdminController,
    PaymentController,
)

# =====================================================================
# FastAPI Application
# =====================================================================
app = FastAPI(
    title="Tech Store - Website bán đồ công nghệ",
    description="Website thương mại điện tử với AI Chatbot",
    version="1.0.0",
    debug=True,
)

# =====================================================================
# Middleware to inject current_user into all templates
# =====================================================================
@app.middleware("http")
async def inject_current_user(request: Request, call_next):
    from Data.database import SessionLocal
    from Services.AuthService import AuthService

    current_user = None
    token = request.cookies.get("access_token")

    if token:
        try:
            db = SessionLocal()
            auth_service = AuthService(db)
            current_user = auth_service.get_current_account_from_token(token)
            db.close()
        except Exception:
            pass

    request.state.current_user = current_user

    response = await call_next(request)
    return response


@app.middleware("http")
async def force_utf8_encoding(request: Request, call_next):
    response = await call_next(request)
    # Force UTF-8 charset on all text-based responses
    content_type = response.headers.get("content-type", "")
    if any(ct in content_type for ct in ("application/javascript", "text/css", "text/html", "application/json")):
        if "charset" not in content_type.lower():
            content_type += "; charset=utf-8"
            response.headers["content-type"] = content_type
    return response


@app.middleware("http")
async def normalize_vietnamese_html_response(request: Request, call_next):
    response = await call_next(request)
    content_type = response.headers.get("content-type", "")
    if "text/html" not in content_type.lower():
        return response

    body = b""
    async for chunk in response.body_iterator:
        body += chunk

    try:
        html = body.decode("utf-8")
    except UnicodeDecodeError:
        html = body.decode("utf-8", errors="replace")

    fixed_html = normalize_vietnamese_display(html)
    headers = dict(response.headers)
    headers.pop("content-length", None)
    headers["content-type"] = "text/html; charset=utf-8"

    return Response(
        content=fixed_html.encode("utf-8"),
        status_code=response.status_code,
        headers=headers,
        media_type=None,
        background=response.background,
    )


# =====================================================================
# Override TemplateResponse to inject current_user
# =====================================================================

# =====================================================================
# Static Files
# =====================================================================
wwwroot_path = os.path.join(os.path.dirname(__file__), "wwwroot")
os.makedirs(wwwroot_path, exist_ok=True)
app.mount("/static", StaticFiles(directory=wwwroot_path), name="static")

# =====================================================================
# Templates Configuration
# =====================================================================
views_path = os.path.join(os.path.dirname(__file__), "Views")
templates = Jinja2Templates(directory=views_path)


def static_url(path):
    """Convert /images/... paths to /static/images/... so images are served correctly."""
    if path and path.startswith("/images/"):
        return "/static" + path
    return path or "/static/images/no-image.png"


templates.env.filters["static_url"] = static_url


def normalize_vietnamese_display(value):
    if not isinstance(value, str):
        return value

    exact_replacements = {
        "?i?n tho?i": "Điện thoại",
        "?i?n tho?i di d?ng": "Điện thoại di động",
        "??ng h? th?ng minh": "Đồng hồ thông minh",
        "??ng h? thông minh": "Đồng hồ thông minh",
        "?ồng hồ thông minh": "Đồng hồ thông minh",
        "Qu?n tr? viên": "Quản trị viên",
        "Qu?n tr? vi?n": "Quản trị viên",
        "Qu?n Tr? Viên": "Quản Trị Viên",
        "M? ??N": "MÃ ĐƠN",
        "M? ĐƠN": "MÃ ĐƠN",
        "Danh s?ch": "Danh sách",
        "T?t c?": "Tất cả",
        "Kh?ch h?ng": "Khách hàng",
        "Ng?y ??t": "Ngày đặt",
        "T?ng ti?n": "Tổng tiền",
        "Thao t?c": "Thao tác",
        "Chi ti?t": "Chi tiết",
        "C?u h?i": "Câu hỏi",
        "C?u tr? l?i": "Câu trả lời",
        "v? v?n chuy?n": "về vận chuyển",
        "v? v?n chuyển": "về vận chuyển",
        "V? v?n chuy?n": "Về vận chuyển",
        "V? v?n chuyển": "Về vận chuyển",
        "V?n chuy?n": "Vận chuyển",
        "Thanh to?n": "Thanh toán",
        "B?o h?nh": "Bảo hành",
        "Đ?i tr?": "Đổi trả",
        "?n": "Ẩn",
        "Ð?n h?ng": "Đơn hàng",
        "Đ?n h?ng": "Đơn hàng",
        "Ch? x? l?": "Chờ xử lý",
        "Ð? x?c nh?n": "Đã xác nhận",
        "Đ? x?c nh?n": "Đã xác nhận",
        "Ðang x? l?": "Đang xử lý",
        "Đang x? l?": "Đang xử lý",
        "Ðang giao": "Đang giao",
        "Ð? giao": "Đã giao",
        "Đ? giao": "Đã giao",
        "Ð? h?y": "Đã hủy",
        "Đ? h?y": "Đã hủy",
        "Apple Vi?t Nam": "Apple Việt Nam",
        "Samsung Vi?t Nam": "Samsung Việt Nam",
        "Sony Vi?t Nam": "Sony Việt Nam",
        "Nguy?n V?n A": "Nguyễn Văn A",
        "Nguy?n Văn A": "Nguyễn Văn A",
        "Tr?n Th? B": "Trần Thị B",
        "Lê V?n C": "Lê Văn C",
        "Ph?m Th? D": "Phạm Thị D",
    }
    replacements = {
        "Ð": "Đ",
        "??ng h? th?ng minh": "Đồng hồ thông minh",
        "??ng h? thông minh": "Đồng hồ thông minh",
        "?i?n tho?i": "Điện thoại",
        "Ð?ng h? thông minh": "Đồng hồ thông minh",
        "Đ?ng h? thông minh": "Đồng hồ thông minh",
        "Ði?n tho?i di d?ng": "Điện thoại di động",
        "Đi?n tho?i di d?ng": "Điện thoại di động",
        "Ði?n tho?i": "Điện thoại",
        "Đi?n tho?i": "Điện thoại",
        "Ph? ki?n": "Phụ kiện",
        "Máy tính b?ng": "Máy tính bảng",
        "Qu?n tr? viên": "Quản trị viên",
        "Qu?n Tr? Viên": "Quản Trị Viên",
        "Qu?n tr?": "Quản trị",
        "Qu?n lý": "Quản lý",
        "M? ??N": "MÃ ĐƠN",
        "M? ĐƠN": "MÃ ĐƠN",
        "M? đơn": "Mã đơn",
        "m? đơn": "mã đơn",
        "M? ??n": "Mã đơn",
        "m? ??n": "mã đơn",
        "Danh s?ch": "Danh sách",
        "danh s?ch": "danh sách",
        "T?t c?": "Tất cả",
        "t?t c?": "tất cả",
        "Kh?ch h?ng": "Khách hàng",
        "kh?ch h?ng": "khách hàng",
        "Kh?ch vãng lai": "Khách vãng lai",
        "Ng?y ??t": "Ngày đặt",
        "ng?y ??t": "ngày đặt",
        "T?ng ti?n": "Tổng tiền",
        "t?ng ti?n": "tổng tiền",
        "Thao t?c": "Thao tác",
        "thao t?c": "thao tác",
        "Chi ti?t": "Chi tiết",
        "chi ti?t": "chi tiết",
        "S?a": "Sửa",
        "s?a": "sửa",
        "X?a": "Xóa",
        "x?a": "xóa",
        "Ch?a c?": "Chưa có",
        "ch?a c?": "chưa có",
        "C?p nh?t": "Cập nhật",
        "c?p nh?t": "cập nhật",
        "C?u h?i": "Câu hỏi",
        "C?u tr? l?i": "Câu trả lời",
        "c?u h?i": "câu hỏi",
        "c?u tr? l?i": "câu trả lời",
        "v? v?n chuy?n": "về vận chuyển",
        "v? v?n chuyển": "về vận chuyển",
        "Tr? l?i": "Trả lời",
        "tr? l?i": "trả lời",
        "Th? t?": "Thứ tự",
        "th? t?": "thứ tự",
        "K?ch ho?t": "Kích hoạt",
        "k?ch ho?t": "kích hoạt",
        "Nh?p": "Nhập",
        "nh?p": "nhập",
        "t?i đây": "tại đây",
        "t?i ?ây": "tại đây",
        "Ð?ng b?": "Đồng bộ",
        "Đ?ng b?": "Đồng bộ",
        "d?ng b?": "đồng bộ",
        "??ng b?": "Đồng bộ",
        "V?n chuy?n": "Vận chuyển",
        "Thanh to?n": "Thanh toán",
        "B?o h?nh": "Bảo hành",
        "Ð?i tr?": "Đổi trả",
        "Đ?i tr?": "Đổi trả",
        ">?n<": ">Ẩn<",
        " ?n ": " Ẩn ",
        "Khách hàng mua s?m": "Khách hàng mua sắm",
        "Nhân viên c?a hàng": "Nhân viên cửa hàng",
        "Tr? s?": "Trụ sở",
        "Ðơn hàng": "Đơn hàng",
        "Ð?n h?ng": "Đơn hàng",
        "Đ?n h?ng": "Đơn hàng",
        "đ?n h?ng": "đơn hàng",
        "Ð? h?y": "Đã hủy",
        "Đ? h?y": "Đã hủy",
        "Ð? giao": "Đã giao",
        "Đ? giao": "Đã giao",
        "Ð? x?c nh?n": "Đã xác nhận",
        "Đ? x?c nh?n": "Đã xác nhận",
        "Ðang x? l?": "Đang xử lý",
        "Đang x? l?": "Đang xử lý",
        "Ch? x? l?": "Chờ xử lý",
        "Chuy?n": "Chuyển",
        "chuy?n": "chuyển",
        "x?c nh?n": "xác nhận",
        "h?y": "hủy",
        "giao h?ng": "giao hàng",
        "to?n qu?c": "toàn quốc",
        "kh?ng": "không",
        "c? h? tr?": "có hỗ trợ",
        "v? v?n chuy?n": "về vận chuyển",
        "Đơn hàng test c?a admin": "Đơn hàng test của admin",
        "Vi?t Nam": "Việt Nam",
        "Nguy?n": "Nguyễn",
        "Tr?n": "Trần",
        "vi?n": "viên",
        "Th?": "Thị",
        "V?n": "Văn",
        "Lê V?n": "Lê Văn",
        "Ph?m": "Phạm",
        "C?u Gi?y": "Cầu Giấy",
        "Hà N?i": "Hà Nội",
        "TP.HCM": "TP.HCM",
        "S?n ph?m": "Sản phẩm",
        "Danh m?c": "Danh mục",
        "Nhà cung c?p": "Nhà cung cấp",
        "Tài kho?n": "Tài khoản",
        "Tr?ng thái": "Trạng thái",
        "Tr?ng th?i": "Trạng thái",
        "tr?ng thái": "trạng thái",
        "tr?ng th?i": "trạng thái",
        "Thao tác": "Thao tác",
        "Hi?n th?": "Hiển thị",
        "hi?n th?": "hiển thị",
        "H? tr?": "Hỗ trợ",
        "Hỗ tr?": "Hỗ trợ",
        "h? tr?": "hỗ trợ",
        "hỗ tr?": "hỗ trợ",
        "h? th?ng": "hệ thống",
        "th?ng minh": "thông minh",
        "d?ng": "dòng",
        "dòng": "dòng",
    }

    priority_replacements = {
        "M? ??N": "MÃ ĐƠN",
        "M? ĐƠN": "MÃ ĐƠN",
        "M? ??n": "Mã đơn",
        "m? ??n": "mã đơn",
        "Danh s?ch": "Danh sách",
        "danh s?ch": "danh sách",
        "T?t c?": "Tất cả",
        "t?t c?": "tất cả",
        "Kh?ch h?ng": "Khách hàng",
        "kh?ch h?ng": "khách hàng",
        "Ng?y ??t": "Ngày đặt",
        "ng?y ??t": "ngày đặt",
        "T?ng ti?n": "Tổng tiền",
        "t?ng ti?n": "tổng tiền",
        "Tr?ng th?i": "Trạng thái",
        "tr?ng th?i": "trạng thái",
        "Tr?ng thái": "Trạng thái",
        "tr?ng thái": "trạng thái",
        "Thao t?c": "Thao tác",
        "thao t?c": "thao tác",
        "Chi ti?t": "Chi tiết",
        "chi ti?t": "chi tiết",
        "Hi?n th?": "Hiển thị",
        "hi?n th?": "hiển thị",
        "Th? t? hi?n th?": "Thứ tự hiển thị",
        "Tìm c?u h?i": "Tìm câu hỏi",
        "C?u h?i v? v?n chuy?n": "Câu hỏi về vận chuyển",
        "C?u h?i v? v?n chuyển": "Câu hỏi về vận chuyển",
        "c?u h?i v? v?n chuy?n": "câu hỏi về vận chuyển",
        "c?u h?i v? v?n chuyển": "câu hỏi về vận chuyển",
        "v? v?n chuy?n": "về vận chuyển",
        "v? v?n chuyển": "về vận chuyển",
        "C?u h?i": "Câu hỏi",
        "c?u h?i": "câu hỏi",
        "C?u tr? l?i": "Câu trả lời",
        "c?u tr? l?i": "câu trả lời",
        "Nh?p c?u tr? l?i chi ti?t t?i ??y": "Nhập câu trả lời chi tiết tại đây",
        "Nh?p c?u tr? l?i chi ti?t t?i ?ây": "Nhập câu trả lời chi tiết tại đây",
        "t?i ??y": "tại đây",
        "t?i ?ây": "tại đây",
        "n?o": "nào",
        "Ch?a c? ??n h?ng n?o": "Chưa có đơn hàng nào",
        "Ch?a c? Đ?n h?ng n?o": "Chưa có đơn hàng nào",
        "Chưa có Đơn hàng nào": "Chưa có đơn hàng nào",
        "Ch?a c? FAQ n?o": "Chưa có FAQ nào",
        "C?p nh?t tr?ng th?i ??n h?ng": "Cập nhật trạng thái đơn hàng",
        "C?p nh?t tr?ng th?i Đ?n h?ng": "Cập nhật trạng thái đơn hàng",
        "Cập nhật trạng thái Đơn hàng": "Cập nhật trạng thái đơn hàng",
        "??n h?ng": "Đơn hàng",
        "??n hàng": "Đơn hàng",
        "?? x?c nh?n": "Đã xác nhận",
        "?? giao": "Đã giao",
        "?? h?y": "Đã hủy",
        "?ang x? l?": "Đang xử lý",
    }

    normalized = value
    for broken, fixed in priority_replacements.items():
        normalized = normalized.replace(broken, fixed)
    if normalized in exact_replacements:
        return exact_replacements[normalized]
    for broken, fixed in replacements.items():
        normalized = normalized.replace(broken, fixed)
    regex_replacements = [
        (r"[?ĐÐ]i[?ệ]n tho[?ạ]i(?: di d[?ộ]ng)?", "Điện thoại"),
        (r"\?{1,2}ng h\? th\?ng minh", "Đồng hồ thông minh"),
        (r"[?ĐÐ]{1,2}ng h[?ồ] thông minh", "Đồng hồ thông minh"),
        (r"Ph[?ụ] ki[?ệ]n", "Phụ kiện"),
        (r"Qu[?ả]n tr[?ị] vi[?ê]n", "Quản trị viên"),
        (r"Qu[?ả]n Tr[?ị] Vi[?ê]n", "Quản Trị Viên"),
        (r"H[?ỗ] tr[?ợ]", "Hỗ trợ"),
        (r"C[?â]u h[?ỏ]i", "Câu hỏi"),
        (r"C[?â]u tr[?ả] l[?ờ]i", "Câu trả lời"),
        (r"v[?ề] v[?ậ]n chuy[?ể]n", "về vận chuyển"),
        (r"V[?ậ]n chuy[?ể]n", "Vận chuyển"),
        (r"Thanh to[?á]n", "Thanh toán"),
        (r"B[?ả]o h[?à]nh", "Bảo hành"),
        (r"[?ĐÐ][?ổ]i tr[?ả]", "Đổi trả"),
        (r"[?ĐÐ][?ơ]n h[?à]ng", "Đơn hàng"),
        (r"Ch[?ờ] x[?ử] l[?ý]", "Chờ xử lý"),
        (r"[?ĐÐ][?ã] x[?á]c nh[?ậ]n", "Đã xác nhận"),
        (r"[?ĐÐ]ang x[?ử] l[?ý]", "Đang xử lý"),
        (r"[?ĐÐ][?ã] giao", "Đã giao"),
        (r"[?ĐÐ][?ã] h[?ủ]y", "Đã hủy"),
        (r"Danh s[?á]ch", "Danh sách"),
        (r"Kh[?á]ch h[?à]ng", "Khách hàng"),
        (r"Ng[?à]y [?�Đđ]{1,2}t", "Ngày đặt"),
        (r"T[?ổ]ng ti[?ề]n", "Tổng tiền"),
        (r"Tr[?ạ]ng th[?á]i", "Trạng thái"),
        (r"Thao t[?á]c", "Thao tác"),
        (r"Chi ti[?ế]t", "Chi tiết"),
        (r"Vi[?ệ]t Nam", "Việt Nam"),
        (r"\bNguy[?ễ]n\b", "Nguyễn"),
        (r"\bTr[?ầ]n\b", "Trần"),
        (r"\bTh[?ị]\b", "Thị"),
        (r"\bV[?ă]n\b", "Văn"),
        (r"\bPh[?ạ]m\b", "Phạm"),
    ]
    for pattern, fixed in regex_replacements:
        normalized = re.sub(pattern, fixed, normalized)

    final_replacements = {
        "Chưa có Đơn hàng nào": "Chưa có đơn hàng nào",
        "Cập nhật trạng thái Đơn hàng": "Cập nhật trạng thái đơn hàng",
    }
    for broken, fixed in final_replacements.items():
        normalized = normalized.replace(broken, fixed)
    return normalized


templates.env.finalize = normalize_vietnamese_display
templates.env.filters["vi_text"] = normalize_vietnamese_display

# Global variables cho tat ca templates
templates.env.globals.update({
    "app_name": "Tech Store",
    "app_version": "1.0.0",
    "current_year": 2024,
})


def get_user_from_request(request):
    return getattr(request.state, "current_user", None)

templates.env.globals["get_current_user"] = get_user_from_request


def repair_vietnamese_seed_text():
    """
    Fix sample rows that were inserted through non-Unicode parameters and
    ended up as strings like "Ði?n tho?i" or "Qu?n tr? viên" in SQL Server.
    This keeps existing schema intact and only normalizes known seed/demo data.
    """
    updates = [
        (
            "Roles",
            "role_id",
            1,
            {"description": "Quản trị viên hệ thống cao nhất"},
        ),
        (
            "Roles",
            "role_id",
            2,
            {"description": "Khách hàng mua sắm"},
        ),
        (
            "Roles",
            "role_id",
            3,
            {"description": "Nhân viên cửa hàng"},
        ),
        (
            "Accounts",
            "Accounts",
            "account_id",
            1,
            {"full_name": "Quản Trị Viên", "address": "Trụ sở Tech Store"},
        ),
        (
            "Users",
            "user_id",
            1,
            {"full_name": "Quản Trị Viên", "address": "Trụ sở Tech Store"},
        ),
        (
            "Employees",
            "employee_id",
            1,
            {"department": "Ban Giám Đốc", "position": "Giám đốc"},
        ),
        (
            "Categories",
            "category_id",
            1,
            {"name": "Điện thoại", "description": "Smartphone các hãng Apple, Samsung..."},
        ),
        (
            "Categories",
            "category_id",
            2,
            {"name": "Laptop", "description": "Máy tính xách tay phục vụ làm việc, gaming"},
        ),
        (
            "Categories",
            "category_id",
            3,
            {"name": "Tablet", "description": "Tablet iPad, Galaxy Tab..."},
        ),
        (
            "Categories",
            "category_id",
            4,
            {"name": "Tai nghe", "description": "Tai nghe Bluetooth, tai nghe chống ồn và phụ kiện âm thanh"},
        ),
        (
            "Categories",
            "category_id",
            5,
            {"name": "Đồng hồ thông minh", "description": "Đồng hồ thông minh và vòng đeo tay sức khỏe"},
        ),
        (
            "Categories",
            "category_id",
            6,
            {"name": "Phụ kiện", "description": "Tai nghe, củ sạc, ốp lưng, bàn phím..."},
        ),
        (
            "Suppliers",
            "supplier_id",
            1,
            {"name": "Apple Việt Nam", "contact_person": "Nguyễn Văn A", "address": "Q1, TP.HCM"},
        ),
        (
            "Suppliers",
            "supplier_id",
            2,
            {"name": "Samsung Việt Nam", "contact_person": "Trần Thị B", "address": "Q9, TP.HCM"},
        ),
        (
            "Suppliers",
            "supplier_id",
            3,
            {"name": "Sony Việt Nam", "contact_person": "Lê Văn C", "address": "Cầu Giấy, Hà Nội"},
        ),
        (
            "Suppliers",
            "supplier_id",
            4,
            {"name": "ASUS Vietnam", "contact_person": "Phạm Thị D", "address": "Q3, TP.HCM"},
        ),
        (
            "Products",
            "product_id",
            1,
            {"description": "Điện thoại flagship cao cấp nhất của Apple."},
        ),
        (
            "Products",
            "product_id",
            2,
            {"description": "Smartphone tích hợp Galaxy AI mạnh mẽ."},
        ),
        (
            "Products",
            "product_id",
            3,
            {"description": "Laptop chuyên nghiệp dành cho dân đồ họa, lập trình."},
        ),
        (
            "Products",
            "product_id",
            4,
            {"description": "Laptop Windows cao cấp viền màn hình siêu mỏng."},
        ),
        (
            "Products",
            "product_id",
            5,
            {"description": "Máy tính bảng hiệu năng ngang ngửa laptop."},
        ),
        (
            "Products",
            "product_id",
            6,
            {"description": "Tai nghe true wireless chống ồn chủ động tốt nhất."},
        ),
        (
            "ProductVariants",
            "variant_id",
            1,
            {"color": "Titan Tự nhiên", "variant_name": "iPhone 15 Pro Max Titan Tự nhiên 256GB"},
        ),
        (
            "ProductVariants",
            "variant_id",
            2,
            {"color": "Titan Đen", "variant_name": "iPhone 15 Pro Max Titan Đen 256GB"},
        ),
        (
            "ProductVariants",
            "variant_id",
            3,
            {"color": "Xám Titan", "variant_name": "Galaxy S24 Ultra Xám 256GB"},
        ),
        (
            "ProductVariants",
            "variant_id",
            7,
            {"color": "Trắng"},
        ),
        (
            "Orders",
            "order_id",
            1,
            {"customer_name": "Quản Trị Viên", "customer_address": "Trụ sở Tech Store", "notes": "Đơn hàng test của admin"},
        ),
        (
            "OrderItems",
            "order_item_id",
            1,
            {"variant_name": "iPhone 15 Pro Max Titan Tự nhiên 256GB"},
        ),
        (
            "FAQs",
            "faq_id",
            1,
            {
                "question": "Shop có hỗ trợ giao hàng toàn quốc không?",
                "answer": "Có. Tech Store hỗ trợ giao hàng toàn quốc, thời gian giao hàng phụ thuộc vào địa chỉ nhận hàng.",
                "category": "Vận chuyển",
            },
        ),
        (
            "FAQs",
            "faq_id",
            2,
            {
                "question": "Tôi có thể thanh toán bằng hình thức nào?",
                "answer": "Bạn có thể thanh toán khi nhận hàng, chuyển khoản hoặc sử dụng phương thức thanh toán trực tuyến được hỗ trợ.",
                "category": "Thanh toán",
            },
        ),
        (
            "FAQs",
            "faq_id",
            3,
            {
                "question": "Sản phẩm được bảo hành bao lâu?",
                "answer": "Thời gian bảo hành tùy từng sản phẩm và nhà sản xuất. Thông tin bảo hành được hiển thị trong chi tiết sản phẩm.",
                "category": "Bảo hành",
            },
        ),
        (
            "FAQs",
            "faq_id",
            4,
            {
                "question": "Tôi có thể đổi trả sản phẩm không?",
                "answer": "Bạn có thể đổi trả theo chính sách của cửa hàng nếu sản phẩm còn đủ điều kiện đổi trả.",
                "category": "Đổi trả",
            },
        ),
        (
            "FAQs",
            "faq_id",
            5,
            {
                "question": "Tôi quên mật khẩu thì phải làm gì?",
                "answer": "Bạn có thể sử dụng chức năng quên mật khẩu trên trang đăng nhập để đặt lại mật khẩu.",
                "category": "Tài khoản",
            },
        ),
    ]

    try:
        with engine.begin() as connection:
            for table, key_column, key_value, values in updates:
                assignments = ", ".join(f"{column} = :{column}" for column in values)
                params = dict(values)
                params["key_value"] = key_value
                connection.execute(
                    text(f"UPDATE {table} SET {assignments} WHERE {key_column} = :key_value"),
                    params,
                )
        return "OK"
    except Exception as exc:
        return f"FAIL: {exc}"


def ensure_runtime_schema_compatibility():
    """
    Add small, backward-compatible columns used by current ORM models.
    This prevents 500 errors when the app runs against an older local DB.
    """
    statements = [
        """
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
                CONSTRAINT FK_Payments_Accounts_Runtime FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
            )
        END
        """,
        """
        IF OBJECT_ID('Payments', 'U') IS NOT NULL AND COL_LENGTH('Payments', 'qr_image_base64') IS NULL
        BEGIN
            ALTER TABLE Payments ADD qr_image_base64 NVARCHAR(MAX) NULL
        END
        """,
        """
        IF OBJECT_ID('Payments', 'U') IS NOT NULL AND COL_LENGTH('Payments', 'transfer_content') IS NULL
        BEGIN
            ALTER TABLE Payments ADD transfer_content NVARCHAR(200) NULL
        END
        """,
        """
        IF OBJECT_ID('Payments', 'U') IS NOT NULL AND COL_LENGTH('Payments', 'verified_by') IS NULL
        BEGIN
            ALTER TABLE Payments ADD verified_by NVARCHAR(50) NULL
        END
        """,
        """
        IF OBJECT_ID('Payments', 'U') IS NOT NULL AND COL_LENGTH('Payments', 'notes') IS NULL
        BEGIN
            ALTER TABLE Payments ADD notes NVARCHAR(500) NULL
        END
        """,
        """
        IF COL_LENGTH('ProductVariants', 'color_hex') IS NULL
        BEGIN
            ALTER TABLE ProductVariants ADD color_hex NVARCHAR(7) NULL
        END
        """,
        """
        IF COL_LENGTH('ProductImages', 'variant_id') IS NULL
        BEGIN
            ALTER TABLE ProductImages ADD variant_id INT NULL
        END
        """,
        """
        IF COL_LENGTH('KnowledgeChunks', 'metadata_json') IS NULL
        BEGIN
            ALTER TABLE KnowledgeChunks ADD metadata_json NVARCHAR(MAX) NULL
        END
        """,
        """
        IF OBJECT_ID('LiveChatConversations', 'U') IS NULL
        BEGIN
            CREATE TABLE LiveChatConversations (
                conversation_id INT IDENTITY(1,1) PRIMARY KEY,
                session_id INT NULL,
                customer_account_id INT NULL,
                staff_account_id INT NULL,
                status NVARCHAR(20) NOT NULL DEFAULT 'waiting',
                subject NVARCHAR(200) NULL,
                customer_name NVARCHAR(100) NULL,
                created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
                accepted_at DATETIME2 NULL,
                closed_at DATETIME2 NULL,
                CONSTRAINT FK_LiveChat_ChatSessions_RT FOREIGN KEY (session_id) REFERENCES ChatSessions(session_id),
                CONSTRAINT FK_LiveChat_CustAcct_RT FOREIGN KEY (customer_account_id) REFERENCES Accounts(account_id),
                CONSTRAINT FK_LiveChat_StaffAcct_RT FOREIGN KEY (staff_account_id) REFERENCES Accounts(account_id)
            )
        END
        """,
        """
        IF OBJECT_ID('LiveChatMessages', 'U') IS NULL
        BEGIN
            CREATE TABLE LiveChatMessages (
                message_id INT IDENTITY(1,1) PRIMARY KEY,
                conversation_id INT NOT NULL,
                sender_type NVARCHAR(20) NOT NULL,
                sender_account_id INT NULL,
                content NVARCHAR(MAX) NOT NULL,
                is_read BIT NOT NULL DEFAULT 0,
                created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
                CONSTRAINT FK_LCMsg_Conv_RT FOREIGN KEY (conversation_id) REFERENCES LiveChatConversations(conversation_id) ON DELETE CASCADE,
                CONSTRAINT FK_LCMsg_Acct_RT FOREIGN KEY (sender_account_id) REFERENCES Accounts(account_id)
            )
        END
        """,
    ]

    try:
        with engine.begin() as connection:
            for statement in statements:
                connection.execute(text(statement))
        return "OK"
    except Exception as exc:
        return f"FAIL: {exc}"


# =====================================================================
# Register Controllers voi templates
# =====================================================================
HomeController.set_templates(templates)
ProductsController.set_templates(templates)
CartController.set_templates(templates)
AuthController.set_templates(templates)
ChatController.set_templates(templates)
AdminController.set_templates(templates)
OrdersController.set_templates(templates)
PaymentController.set_templates(templates)

# =====================================================================
# Include Routers
# =====================================================================
app.include_router(HomeController.router)
app.include_router(ProductsController.router)
app.include_router(CartController.router)
app.include_router(AuthController.router)
app.include_router(ChatController.router)
app.include_router(AdminController.router)
app.include_router(AccountsController.router)
app.include_router(CategoriesController.router)
app.include_router(SuppliersController.router)
app.include_router(EmployeesController.router)
app.include_router(InventoryController.router)
app.include_router(OrdersController.router)
app.include_router(OrderItemsController.router)
app.include_router(ReceiptShipmentsController.router)
app.include_router(CartItemsController.router)
app.include_router(ShopController.router)
app.include_router(StatisticsController.router)
app.include_router(PaymentController.router)


# =====================================================================
# Startup & Shutdown Events
# =====================================================================

@app.on_event("startup")
async def startup():
    """Khởi động ứng dụng"""
    db_info = get_connection_info()
    db_status = "FAILED"
    db_error = None
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        db_status = "OK"
    except Exception as exc:
        db_error = str(exc)

    schema_status = ensure_runtime_schema_compatibility()

    # Seed 2 roles mac dinh (Admin va Customer)
    roles_status = "SKIPPED"
    try:
        from Data.database import SessionLocal
        from Services.AuthService import AuthService
        db = SessionLocal()
        auth_service = AuthService(db)
        auth_service.seed_roles()
        db.close()
        roles_status = "OK"
    except Exception as exc:
        roles_status = f"FAIL: {exc}"

    vietnamese_text_status = repair_vietnamese_seed_text()

    print(f"""
+==============================================================+
|              TECH STORE APPLICATION STARTED                   |
+==============================================================+
|  Database : {db_info['database']:<46} |
|  Server   : {db_info['server']:<46} |
|  Auth     : {db_info['auth_mode']:<46} |
|  SQL Test : {db_status:<46} |
|  Schema   : {schema_status:<46} |
|  Roles    : {roles_status:<46} |
|  Unicode  : {vietnamese_text_status:<46} |
|  URL      : http://localhost:8000                         |
|  Docs     : http://localhost:8000/docs                    |
+==============================================================+
    """)
    if db_error:
        print(f"SQL Test Error: {db_error}")


@app.on_event("shutdown")
async def shutdown():
    """Tắt ứng dụng"""
    print("\nTech Store Application Shutdown")


# =====================================================================
# Error Handlers
# =====================================================================

@app.exception_handler(404)
async def not_found(request: Request, exc):
    """Xử lý lỗi 404"""
    return templates.TemplateResponse(
        "Shared/error.html",
        {
            "request": request,
            "error_code": 404,
            "error_message": "Trang không tìm thấy"
        },
        status_code=404
    )


@app.exception_handler(500)
async def server_error(request: Request, exc):
    """Xử lý lỗi 500"""
    return templates.TemplateResponse(
        "Shared/error.html",
        {
            "request": request,
            "error_code": 500,
            "error_message": "Lỗi server"
        },
        status_code=500
    )


# =====================================================================
# Development Entry Point
# =====================================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
