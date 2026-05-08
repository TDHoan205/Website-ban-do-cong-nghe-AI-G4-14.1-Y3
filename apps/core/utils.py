"""
Utility functions cho core app.
Chứa các hàm helper dùng chung trong toàn bộ ứng dụng.
"""
import hashlib
import random
import string
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


def paginate_queryset(request, queryset, per_page: int = 10) -> Tuple[Any, Any]:
    """
    Phân trang queryset và trả về kết quả đã phân trang.

    Args:
        request: Django request object
        queryset: QuerySet cần phân trang
        per_page: Số item trên mỗi trang

    Returns:
        Tuple (page_obj, paginator)
    """
    paginator = Paginator(queryset, per_page)
    page = request.GET.get('page')
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    return paginated_queryset, paginator


def format_currency(amount: float) -> str:
    """
    Format số tiền thành định dạng tiền Việt Nam.

    Args:
        amount: Số tiền

    Returns:
        Chuỗi định dạng: "1.234.567 đ"
    """
    try:
        return f"{float(amount):,.0f} đ".replace(",", ".")
    except (ValueError, TypeError):
        return "0 đ"


def format_datetime(dt: datetime, format_str: str = '%d/%m/%Y %H:%M') -> str:
    """
    Format datetime thành chuỗi theo định dạng Việt Nam.

    Args:
        dt: Datetime object
        format_str: Chuỗi định dạng

    Returns:
        Chuỗi datetime đã format
    """
    if not dt:
        return ''
    return dt.strftime(format_str)


def generate_order_code() -> str:
    """
    Tạo mã đơn hàng duy nhất.

    Returns:
        Mã đơn hàng: ORD-YYYYMMDD-XXXXXX
    """
    prefix = datetime.now().strftime('%Y%m%d')
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"ORD-{prefix}-{suffix}"


def generate_employee_code() -> str:
    """
    Tạo mã nhân viên duy nhất.

    Returns:
        Mã nhân viên: NV-XXXX
    """
    suffix = ''.join(random.choices(string.digits, k=4))
    return f"NV-{suffix}"


def generate_reset_token() -> str:
    """
    Tạo token reset password ngẫu nhiên.

    Returns:
        Token 64 ký tự hex
    """
    return hashlib.sha256(
        f"{random.random()}{datetime.now()}".encode()
    ).hexdigest()


def get_client_ip(request) -> str:
    """
    Lấy địa chỉ IP của client từ request.

    Args:
        request: Django request object

    Returns:
        Địa chỉ IP
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
    return ip


def get_file_extension(filename: str) -> str:
    """
    Lấy phần mở rộng của file.

    Args:
        filename: Tên file

    Returns:
        Phần mở rộng (ví dụ: '.jpg')
    """
    return filename[filename.rfind('.'):].lower()


def is_valid_image_extension(filename: str) -> bool:
    """
    Kiểm tra file có phải là ảnh hợp lệ không.

    Args:
        filename: Tên file

    Returns:
        True nếu là ảnh hợp lệ
    """
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    return get_file_extension(filename) in allowed_extensions


def json_response(data: Dict[str, Any], success: bool = True,
                  message: str = '', status: int = 200) -> JsonResponse:
    """
    Tạo JSON response chuẩn cho API.

    Args:
        data: Dữ liệu trả về
        success: Trạng thái thành công
        message: Thông báo
        status: HTTP status code

    Returns:
        JsonResponse
    """
    return JsonResponse({
        'success': success,
        'message': message,
        'data': data
    }, status=status)


def error_response(message: str, status: int = 400) -> JsonResponse:
    """
    Tạo JSON response cho lỗi.

    Args:
        message: Thông báo lỗi
        status: HTTP status code

    Returns:
        JsonResponse
    """
    return JsonResponse({
        'success': False,
        'message': message,
        'data': None
    }, status=status)


def success_response(data: Any = None, message: str = '',
                    status: int = 200) -> JsonResponse:
    """
    Tạo JSON response cho thành công.

    Args:
        data: Dữ liệu trả về
        message: Thông báo
        status: HTTP status code

    Returns:
        JsonResponse
    """
    return JsonResponse({
        'success': True,
        'message': message,
        'data': data
    }, status=status)


def calculate_discount_percent(original_price: float, sale_price: float) -> int:
    """
    Tính phần trăm giảm giá.

    Args:
        original_price: Giá gốc
        sale_price: Giá bán

    Returns:
        Phần trăm giảm giá (0-100)
    """
    if not original_price or original_price <= 0:
        return 0
    discount = ((original_price - sale_price) / original_price) * 100
    return max(0, min(100, int(discount)))


def get_date_range(days: int = 30) -> Tuple[datetime, datetime]:
    """
    Lấy khoảng thời gian.

    Args:
        days: Số ngày tính từ hiện tại

    Returns:
        Tuple (start_date, end_date)
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date


def truncate_string(text: str, length: int = 50) -> str:
    """
    Cắt chuỗi đến độ dài nhất định.

    Args:
        text: Chuỗi cần cắt
        length: Độ dài tối đa

    Returns:
        Chuỗi đã cắt
    """
    if not text:
        return ''
    if len(text) <= length:
        return text
    return text[:length] + '...'


def clean_html(text: str) -> str:
    """
    Loại bỏ các thẻ HTML khỏi text.

    Args:
        text: Chuỗi chứa HTML

    Returns:
        Chuỗi không có HTML
    """
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)
