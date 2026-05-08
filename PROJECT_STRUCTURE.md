# TechShop Website - Cấu trúc dự án chi tiết

> **Mô tả:** Website bán đồ công nghệ AI - TechShop được xây dựng bằng Django Framework.
> **Ngày tạo:** 2026
> **Ngôn ngữ:** Python, HTML, CSS, JavaScript

---

## 📁 Cấu trúc thư mục tổng quan

```
Website-ban-do-cong-nghe-AI-G4-14.1-Y3/
│
├── 📂 apps/                    # Ứng dụng Django (Modules chính)
│   ├── core/                   # Lõi hệ thống (decorators, mixins, utils)
│   ├── users/                  # Quản lý tài khoản người dùng
│   ├── authentication/         # Đăng nhập, đăng ký, xác thực
│   ├── categories/             # Quản lý danh mục sản phẩm
│   ├── products/               # Quản lý sản phẩm
│   ├── suppliers/              # Quản lý nhà cung cấp
│   ├── orders/                 # Quản lý đơn hàng
│   ├── cart/                   # Quản lý giỏ hàng
│   ├── inventory/              # Quản lý tồn kho
│   ├── dashboard/              # Trang Dashboard quản trị
│   ├── reports/                # Báo cáo doanh thu
│   ├── chat/                   # Chat AI hỗ trợ khách hàng
│   ├── notifications/          # Thông báo
│   ├── faqs/                   # Câu hỏi thường gặp
│   ├── settings/               # Cài đặt website
│   ├── shop/                   # Giao diện cửa hàng (Frontend)
│   ├── brands/                 # Quản lý thương hiệu
│   ├── slides/                 # Quản lý slides/banner
│   └── reviews/                # Quản lý đánh giá sản phẩm
│
├── 📂 config/                  # Cấu hình Django
│   ├── settings.py             # Cấu hình chính
│   ├── urls.py                 # Định tuyến URL chính
│   ├── wsgi.py                # Cấu hình WSGI (deploy)
│   └── asgi.py                # Cấu hình ASGI (async)
│
├── 📂 templates/               # Template HTML
│   ├── base.html               # Template base (kế thừa)
│   ├── admin/                  # Template admin dashboard
│   ├── shop/                   # Template cửa hàng
│   ├── accounts/               # Template tài khoản
│   └── ...                     # Template các module khác
│
├── 📂 static/                  # File tĩnh
│   ├── css/                    # Stylesheets
│   ├── js/                     # JavaScript
│   └── images/                 # Hình ảnh
│
├── 📂 media/                   # Upload files (user uploads)
├── 📂 migrations_sql/          # SQL migrations (backup)
├── 📂 Models/                  # Class Model cũ (tham khảo)
├── 📂 Data/                    # Data scripts
├── 📂 scripts/                 # Scripts hỗ trợ
├── 📂 tests/                   # Unit tests
│
├── manage.py                   # Django CLI
├── run.py                      # Script chạy server
├── run_admin.bat               # Batch file chạy admin
├── requirements.txt            # Python dependencies
└── README_ADMIN.md             # Hướng dẫn cài đặt
```

---

## 🏠 Thư mục gốc (Root)

### `manage.py`
- **Chức năng:** Django Management Interface - giao diện dòng lệnh quản lý project
- **Sử dụng:** Chạy server, tạo migrations, superuser...
- **Lệnh phổ biến:**
  ```bash
  python manage.py runserver      # Chạy server
  python manage.py makemigrations # Tạo migration
  python manage.py migrate        # Áp dụng migration
  python manage.py createsuperuser # Tạo admin
  ```

### `run.py`
- **Chức năng:** Script Python khởi động server
- **Tự động:** Kích hoạt virtual environment và chạy server

### `run_admin.bat`
- **Chức năng:** Batch file chạy nhanh admin dashboard
- **Sử dụng:** Double-click để khởi động server

### `requirements.txt`
- **Chức năng:** Danh sách các thư viện Python cần cài đặt
- **Cài đặt:** `pip install -r requirements.txt`

### `README_ADMIN.md`
- **Chức năng:** Hướng dẫn cài đặt và sử dụng project

---

## ⚙️ Thư mục `config/`

### `config/settings.py`
- **Chức năng:** File cấu hình chính của Django
- **Nội dung:**
  - Cấu hình database (SQLite/SQL Server)
  - Cài đặt apps
  - Middleware
  - Static/Media files
  - Authentication settings
  - Internationalization (Tiếng Việt)

### `config/urls.py`
- **Chức năng:** Định tuyến URL chính của toàn bộ website
- **Nội dung:** Liệt kê tất cả URL patterns của các app
  ```python
  path('admin/', admin.site.urls),           # Django Admin
  path('accounts/', include('apps.users.urls')),  # Tài khoản
  path('products/', include('apps.products.urls')), # Sản phẩm
  path('shop/', include('apps.shop.urls')),   # Cửa hàng
  # ... và nhiều app khác
  ```

### `config/wsgi.py`
- **Chức năng:** Web Server Gateway Interface
- **Sử dụng:** Deploy lên production server (Apache, Nginx)

### `config/asgi.py`
- **Chức năng:** Asynchronous Server Gateway Interface
- **Sử dụng:** Hỗ trợ WebSocket, async operations

---

## 📦 Thư mục `apps/` - Các Ứng dụng Django

### 🔧 `apps/core/` - Lõi hệ thống

| File | Chức năng |
|------|------------|
| `decorators.py` | Custom decorators (@login_required, @role_required) |
| `mixins.py` | Base mixin classes cho View |
| `utils.py` | Hàm tiện ích (format currency, generate code...) |
| `constants.py` | Hằng số hệ thống (STATUS_CHOICES, ORDER_STATUS...) |
| `context_processors.py` | Cung cấp biến global cho template |
| `management/commands/seed_data.py` | Script tạo dữ liệu mẫu |

### 👥 `apps/users/` - Quản lý Tài khoản

| File | Chức năng |
|------|------------|
| `models.py` | **Account** (Custom User Model), **Employee** |
| `views.py` | Đăng nhập, đăng xuất, profile, danh sách tài khoản |
| `forms.py` | Form tạo/sửa tài khoản |
| `urls.py` | Định tuyến /accounts/ |

**Models:**
- `Account`: Tài khoản người dùng (Admin, Employee, Customer)
- `Employee`: Thông tin nhân viên (phòng ban, chức vụ, lương)

### 🔐 `apps/authentication/` - Xác thực

| File | Chức năng |
|------|------------|
| `views.py` | Xử lý đăng nhập, đăng xuất, đăng ký |
| `urls.py` | Định tuyến authentication |

### 📂 `apps/categories/` - Danh mục sản phẩm

| File | Chức năng |
|------|------------|
| `models.py` | **Category** (id, name, slug, icon, description) |
| `views.py` | CRUD danh mục |
| `forms.py` | Form tạo/sửa danh mục |
| `urls.py` | Định tuyến /categories/ |

### 📦 `apps/products/` - Quản lý Sản phẩm

| File | Chức năng |
|------|------------|
| `models.py` | **Product**, **ProductVariant**, **ProductImage** |
| `views.py` | CRUD sản phẩm, biến thể, hình ảnh |
| `forms.py` | Form tạo/sửa sản phẩm |
| `urls.py` | Định tuyến /products/ |

**Models:**
- `Product`: Sản phẩm chính (tên, giá, mô tả, hình ảnh, tồn kho)
- `ProductVariant`: Biến thể (màu sắc, dung lượng, RAM, SKU, giá)
- `ProductImage`: Nhiều hình ảnh cho sản phẩm

### 🚚 `apps/suppliers/` - Nhà cung cấp

| File | Chức năng |
|------|------------|
| `models.py` | **Supplier** (tên, địa chỉ, SĐT, email, trạng thái) |
| `views.py` | CRUD nhà cung cấp |
| `forms.py` | Form tạo/sửa nhà cung cấp |
| `urls.py` | Định tuyến /suppliers/ |

### 🛒 `apps/orders/` - Quản lý Đơn hàng

| File | Chức năng |
|------|------------|
| `models.py` | **Order**, **OrderItem** |
| `views.py` | CRUD đơn hàng, chi tiết đơn hàng |
| `forms.py` | Form tạo/cập nhật đơn hàng |
| `urls.py` | Định tuyến /orders/ |

**Models:**
- `Order`: Đơn hàng (mã đơn, khách hàng, tổng tiền, trạng thái, địa chỉ giao)
- `OrderItem`: Chi tiết đơn hàng (sản phẩm, số lượng, đơn giá)

### 🛍️ `apps/cart/` - Giỏ hàng

| File | Chức năng |
|------|------------|
| `models.py` | **Cart**, **CartItem** |
| `views.py` | Xem giỏ hàng, thêm/xóa/sửa sản phẩm |
| `forms.py` | Form cập nhật giỏ hàng |
| `urls.py` | Định tuyến /cart/ |

**Models:**
- `Cart`: Giỏ hàng của user
- `CartItem`: Sản phẩm trong giỏ (sản phẩm, biến thể, số lượng)

### 📊 `apps/inventory/` - Quản lý Tồn kho

| File | Chức năng |
|------|------------|
| `models.py` | **Inventory**, **InventoryTransaction** |
| `views.py` | Xem tồn kho, điều chỉnh tồn kho |
| `forms.py` | Form điều chỉnh tồn kho |
| `urls.py` | Định tuyến /inventory/ |

### 📈 `apps/dashboard/` - Dashboard quản trị

| File | Chức năng |
|------|------------|
| `views.py` | Trang chủ admin, thống kê, biểu đồ |
| `forms.py` | Form lọc thống kê |
| `urls.py` | Định tuyến /dashboard/ |

**Chức năng:** Hiển thị tổng quan doanh thu, đơn hàng, sản phẩm, biểu đồ Chart.js

### 📉 `apps/reports/` - Báo cáo

| File | Chức năng |
|------|------------|
| `views.py` | Báo cáo doanh thu, xuất Excel/PDF |
| `forms.py` | Form lọc báo cáo (theo ngày, tháng) |
| `urls.py` | Định tuyến /reports/ |

### 💬 `apps/chat/` - Chat AI

| File | Chức năng |
|------|------------|
| `models.py` | **ChatSession**, **ChatMessage**, **AILog** |
| `views.py` | Chat interface, quản lý phiên chat |
| `services/ai_service.py` | Xử lý AI (GPT integration) |
| `services/rule_based.py` | AI dựa trên luật (fallback) |
| `services/product_recommender.py` | Gợi ý sản phẩm |
| `urls.py` | Định tuyến /chat/ |

**Chức năng:** Chat widget hỗ trợ khách hàng 24/7

### 🔔 `apps/notifications/` - Thông báo

| File | Chức năng |
|------|------------|
| `models.py` | **Notification** (tiêu đề, nội dung, loại, đã đọc) |
| `views.py` | CRUD thông báo |
| `forms.py` | Form tạo thông báo |
| `urls.py` | Định tuyến /notifications/ |

### ❓ `apps/faqs/` - Câu hỏi thường gặp

| File | Chức năng |
|------|------------|
| `models.py` | **FAQ** (câu hỏi, câu trả lời, thứ tự) |
| `views.py` | CRUD FAQs |
| `forms.py` | Form tạo FAQ |
| `urls.py` | Định tuyến /faqs/ |

### ⚙️ `apps/settings/` - Cài đặt

| File | Chức năng |
|------|------------|
| `models.py` | **SiteSetting** (key-value settings) |
| `views.py` | Quản lý cài đặt website |
| `forms.py` | Form cài đặt |
| `urls.py` | Định tuyến /settings/ |

### 🏪 `apps/shop/` - Giao diện Cửa hàng (Frontend)

| File | Chức năng |
|------|------------|
| `views.py` | Trang chủ, danh sách sản phẩm, chi tiết, giỏ hàng, checkout |
| `urls.py` | Định tuyến /shop/ |

**Templates:** `home.html`, `products.html`, `product_detail.html`, `cart.html`, `checkout.html`

### 🏷️ `apps/brands/` - Thương hiệu

| File | Chức năng |
|------|------------|
| `models.py` | **Brand** (tên, logo, mô tả) |
| `views.py` | CRUD thương hiệu |
| `forms.py` | Form tạo thương hiệu |
| `urls.py` | Định tuyến /brands/ |

### 🎠 `apps/slides/` - Slides/Banner

| File | Chức năng |
|------|------------|
| `models.py` | **Slide** (hình ảnh, tiêu đề, link, thứ tự) |
| `views.py` | CRUD slides |
| `forms.py` | Form tạo slide |
| `urls.py` | Định tuyến /slides/ |

### ⭐ `apps/reviews/` - Đánh giá

| File | Chức năng |
|------|------------|
| `models.py` | **Review** (sản phẩm, user, rating, bình luận) |
| `views.py` | CRUD đánh giá |
| `forms.py` | Form đánh giá |
| `urls.py` | Định tuyến /reviews/ |

---

## 🎨 Thư mục `templates/`

### `base.html`
- **Chức năng:** Template base - kế thừa bởi tất cả các template khác
- **Nội dung:** Header, Footer, CSS/JS cơ bản

### `templates/admin/`
| File | Chức năng |
|------|------------|
| `base.html` | Template base admin |
| `header.html` | Header với user menu |
| `sidebar.html` | Sidebar navigation |

### `templates/shop/`
| File | Chức năng |
|------|------------|
| `base_shop.html` | Template base cửa hàng |
| `home.html` | Trang chủ shop |
| `products.html` | Danh sách sản phẩm |
| `product_detail.html` | Chi tiết sản phẩm |
| `cart.html` | Trang giỏ hàng |
| `checkout.html` | Trang thanh toán |
| `partials/product_card.html` | Component card sản phẩm |

### `templates/accounts/`
| File | Chức năng |
|------|------------|
| `login.html` | Trang đăng nhập |
| `register.html` | Trang đăng ký |
| `profile.html` | Trang thông tin cá nhân |
| `account_list.html` | Danh sách tài khoản (admin) |

### `templates/partials/`
| File | Chức năng |
|------|------------|
| `_pagination.html` | Component phân trang |
| `_messages.html` | Component hiển thị messages |

---

## 📁 Thư mục `static/`

### `static/css/`
| File | Chức năng |
|------|------------|
| `admin.css` | Stylesheet cho admin dashboard |
| `homepage.css` | Stylesheet cho trang chủ/shop |

### `static/js/`
| File | Chức năng |
|------|------------|
| `admin.js` | JavaScript cho admin (interactions) |

### `static/images/`
- Chứa hình ảnh tĩnh (logo, icons, placeholders)

---

## 🔧 Thư mục `Models/` (Cũ - Tham khảo)

Chứa các class Model cũ dùng để tham khảo cấu trúc:
- `User.py` - Người dùng
- `Product.py` - Sản phẩm
- `Category.py` - Danh mục
- `Order.py` - Đơn hàng
- `Cart.py` - Giỏ hàng
- `Supplier.py` - Nhà cung cấp
- `AI.py` - AI Service
- `Inventory.py` - Tồn kho

---

## 📋 Luồng hoạt động

### 1. Luồng Mua hàng
```
Home → Products → Product Detail → Add to Cart → Cart → Checkout → Order
```

### 2. Luồng Admin
```
Login → Dashboard → Products/Categories/Orders → CRUD Operations
```

### 3. Luồng Chat AI
```
Customer clicks chat → Chat widget opens → Send message → AI responds → Suggest products
```

---

## 🎯 URL Patterns chính

| URL | Module | Chức năng |
|-----|--------|----------|
| `/` | Dashboard | Trang chủ admin |
| `/shop/` | Shop | Cửa hàng |
| `/accounts/login/` | Users | Đăng nhập |
| `/products/` | Products | Quản lý sản phẩm |
| `/categories/` | Categories | Quản lý danh mục |
| `/orders/` | Orders | Quản lý đơn hàng |
| `/cart/` | Cart | Quản lý giỏ hàng |
| `/reports/` | Reports | Báo cáo doanh thu |
| `/chat/` | Chat | Chat AI hỗ trợ |
| `/admin/` | Django | Django Admin |

---

## 💾 Database

### SQLite (Mặc định)
- Phù hợp cho development
- File: `db.sqlite3`

### SQL Server (Production)
- Cần cấu hình trong `.env`
- Host: `localhost`
- Database: `TechShopWebsite1`

---

## 🚀 Cách chạy project

```bash
# 1. Di chuyển vào thư mục project
cd "c:\Code full\CURSOR-JG-DEV\Website-ban-do-cong-nghe-AI-G4-14.1-Y3"

# 2. Cài đặt thư viện
pip install -r requirements.txt

# 3. Tạo database
python manage.py migrate

# 4. Tạo tài khoản admin
python manage.py createsuperuser

# 5. Chạy server
python manage.py runserver
```

Hoặc đơn giản click đúp vào file `run_admin.bat`

---

## 📞 Liên hệ & Hỗ trợ

Nếu có thắc mắc về cấu trúc project, vui lòng đọc:
- `README_ADMIN.md` - Hướng dẫn cài đặt
- File `models.py` trong từng app để hiểu cấu trúc dữ liệu
