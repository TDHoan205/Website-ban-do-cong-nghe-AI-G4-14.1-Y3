"""
Constants cho ứng dụng core.
Chứa các hằng số, choices, trạng thái được sử dụng trong toàn bộ ứng dụng.
"""


# =====================
# ROLES
# =====================
class UserRole:
    ADMIN = 'Admin'
    EMPLOYEE = 'Employee'
    CUSTOMER = 'Customer'

    CHOICES = [
        (ADMIN, 'Quản trị viên'),
        (EMPLOYEE, 'Nhân viên'),
        (CUSTOMER, 'Khách hàng'),
    ]

    # Roles có quyền truy cập admin
    ADMIN_ROLES = [ADMIN, EMPLOYEE]


# =====================
# ORDER STATUS
# =====================
class OrderStatus:
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'
    PROCESSING = 'Processing'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
    CANCELLED = 'Cancelled'
    RETURNED = 'Returned'

    CHOICES = [
        (PENDING, 'Chờ xác nhận'),
        (CONFIRMED, 'Đã xác nhận'),
        (PROCESSING, 'Đang xử lý'),
        (SHIPPED, 'Đang giao hàng'),
        (DELIVERED, 'Đã giao hàng'),
        (CANCELLED, 'Đã hủy'),
        (RETURNED, 'Trả hàng'),
    ]

    # Trạng thái có thể hủy
    CANCELLABLE_STATUSES = [PENDING, CONFIRMED]

    # Trạng thái hoàn thành
    COMPLETED_STATUSES = [DELIVERED, RETURNED]


# =====================
# PAYMENT STATUS
# =====================
class PaymentStatus:
    UNPAID = 'Unpaid'
    PAID = 'Paid'
    REFUNDED = 'Refunded'

    CHOICES = [
        (UNPAID, 'Chưa thanh toán'),
        (PAID, 'Đã thanh toán'),
        (REFUNDED, 'Đã hoàn tiền'),
    ]


# =====================
# CHAT STATUS
# =====================
class ChatStatus:
    ACTIVE = 'Active'
    WAITING = 'Waiting'
    CLOSED = 'Closed'

    CHOICES = [
        (ACTIVE, 'Đang chat'),
        (WAITING, 'Đang chờ'),
        (CLOSED, 'Đã đóng'),
    ]


# =====================
# NOTIFICATION TYPES
# =====================
class NotificationType:
    ORDER = 'Order'
    PAYMENT = 'Payment'
    CHAT = 'Chat'
    SYSTEM = 'System'
    PROMOTION = 'Promotion'

    CHOICES = [
        (ORDER, 'Thông báo đơn hàng'),
        (PAYMENT, 'Thông báo thanh toán'),
        (CHAT, 'Thông báo chat'),
        (SYSTEM, 'Thông báo hệ thống'),
        (PROMOTION, 'Khuyến mãi'),
    ]


# =====================
# FAQ CATEGORIES
# =====================
class FAQCategory:
    GENERAL = 'General'
    ORDER = 'Order'
    PAYMENT = 'Payment'
    SHIPPING = 'Shipping'
    RETURN = 'Return'
    PRODUCT = 'Product'

    CHOICES = [
        (GENERAL, 'Câu hỏi chung'),
        (ORDER, 'Về đơn hàng'),
        (PAYMENT, 'Thanh toán'),
        (SHIPPING, 'Vận chuyển'),
        (RETURN, 'Đổi trả'),
        (PRODUCT, 'Sản phẩm'),
    ]


# =====================
# PAGINATION
# =====================
class Pagination:
    DEFAULT_PAGE_SIZE = 10
    PAGE_SIZE_OPTIONS = [10, 20, 50, 100]

    # Admin pages
    ADMIN_PAGE_SIZE = 20
    DASHBOARD_PAGE_SIZE = 5


# =====================
# FILE UPLOADS
# =====================
class FileUpload:
    ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB

    PRODUCT_IMAGE_PATH = 'products/'
    CATEGORY_IMAGE_PATH = 'categories/'
    SUPPLIER_IMAGE_PATH = 'suppliers/'


# =====================
# MESSAGES
# =====================
class Messages:
    # Success messages
    CREATE_SUCCESS = 'Tạo mới thành công!'
    UPDATE_SUCCESS = 'Cập nhật thành công!'
    DELETE_SUCCESS = 'Xóa thành công!'
    SAVE_SUCCESS = 'Lưu thành công!'

    # Error messages
    CREATE_ERROR = 'Tạo mới thất bại!'
    UPDATE_ERROR = 'Cập nhật thất bại!'
    DELETE_ERROR = 'Xóa thất bại!'
    SAVE_ERROR = 'Lưu thất bại!'

    # Validation messages
    REQUIRED_FIELD = 'Trường này là bắt buộc!'
    INVALID_FORMAT = 'Định dạng không hợp lệ!'
    DUPLICATE_VALUE = 'Giá trị đã tồn tại!'


# =====================
# PERMISSIONS
# =====================
class Permissions:
    # App permissions
    VIEW_ACCOUNTS = 'view_accounts'
    ADD_ACCOUNT = 'add_account'
    CHANGE_ACCOUNT = 'change_account'
    DELETE_ACCOUNT = 'delete_account'

    VIEW_PRODUCTS = 'view_products'
    ADD_PRODUCT = 'add_product'
    CHANGE_PRODUCT = 'change_product'
    DELETE_PRODUCT = 'delete_product'

    VIEW_ORDERS = 'view_orders'
    CHANGE_ORDER = 'change_order'

    VIEW_REPORTS = 'view_reports'
    EXPORT_REPORTS = 'export_reports'
