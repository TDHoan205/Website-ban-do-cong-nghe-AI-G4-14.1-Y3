# 📁 Cấu trúc dự án Django - Website bán đồ công nghệ AI

Tài liệu này giải thích chi tiết từng thư mục và file trong dự án, để bạn dễ dàng hiểu được mỗi phần dùng để làm gì.

---

## 📊 Sơ đồ cấu trúc thư mục đầy đủ

```
Website-ban-do-cong-nghe-AI-G4-14.1-Y3/
│
├── 🔧 config/                          # ⭐ CẤU HÌNH DJANGO
│   ├── __init__.py
│   ├── settings.py                     # Cấu hình chính Django (DB, APPS, AUTH, etc.)
│   ├── urls.py                         # Routing chính - điều hướng tất cả URL
│   ├── wsgi.py                         # Cấu hình WSGI cho production server
│   └── asgi.py                         # Cấu hình ASGI cho async/websocket
│
├── 📄 docs/                            # ⭐ TÀI LIỆU DỰ ÁN
│   ├── PROJECT_STRUCTURE.md            # Tài liệu này - hướng dẫn cấu trúc
│   └── PROMPT_ADMIN_WEBSTORE.md        # Hướng dẫn quản trị webstore
│
├── 📦 apps/                            # ⭐ CÁC ỨNG DỤNG DJANGO CHÍNH
│   ├── core/                           # Tiện ích chung (decorators, mixins, utils)
│   ├── auth/                           # Xác thực (login, register, forgot password)
│   ├── users/                          # Quản lý người dùng (User, roles, profiles)
│   ├── products/                       # Quản lý sản phẩm (Product, Category, Supplier)
│   ├── cart/                           # Giỏ hàng (Cart, CartItem)
│   ├── orders/                         # Quản lý đơn hàng (Order, OrderItem)
│   ├── inventory/                      # Quản lý kho hàng (Inventory, ReceiptShipment)
│   ├── dashboard/                      # Bảng điều khiển admin (thống kê, báo cáo)
│   ├── shop/                           # Giao diện cửa hàng (trang chủ, product list)
│   └── chat/                           # AI Chat (ChatMessage, ChatSession) - tùy chọn
│
├── 🗄️ Models/                          # Định nghĩa cấu trúc dữ liệu
│   ├── __init__.py
│   ├── Account.py                      # Model tài khoản người dùng
│   ├── User.py                         # Model người dùng (hồ sơ, thông tin)
│   ├── Product.py                      # Model sản phẩm
│   ├── Category.py                     # Model danh mục
│   ├── Supplier.py                     # Model nhà cung cấp
│   ├── Cart.py                         # Model giỏ hàng
│   ├── Order.py                        # Model đơn hàng
│   ├── Inventory.py                    # Model tồn kho
│   ├── ReceiptShipment.py              # Model phiếu nhập/xuất
│   ├── Chat.py                         # Model chat
│   └── AI.py                           # Model AI
│
├── 👁️ Views/                           # Template HTML giao diện
│   ├── Login/                          # Giao diện đăng nhập, đăng ký
│   ├── Admin/                          # Giao diện quản trị
│   └── Customer/                       # Giao diện khách hàng
│
├── 🎮 Controller/                      # Logic xử lý dữ liệu
│   └── Controller.py                   # Class Controller - CRUD operations
│
├── 💾 Data/                            # Quản lý cơ sở dữ liệu
│   ├── database.py                     # Cấu hình kết nối DB
│   └── Seed/
│       └── seed_data.py                # Script tạo dữ liệu mẫu ban đầu
│
├── 🎨 static/                          # Tệp tĩnh (CSS, JS, ảnh)
│   ├── css/
│   │   ├── homepage.css                # CSS trang chủ
│   │   ├── shop-layout-animations.css  # CSS animation cửa hàng
│   │   ├── shop-refresh.css            # CSS làm mới cửa hàng
│   │   ├── site.css                    # CSS chung
│   │   └── style.css                   # CSS chính
│   ├── js/
│   │   ├── main.js                     # JavaScript chính
│   │   └── site.js                     # JavaScript chung
│   ├── images/
│   │   └── products/                   # Ảnh sản phẩm tĩnh
│   └── lib/                            # Thư viện bên ngoài
│       ├── bootstrap/                  # Bootstrap framework
│       ├── jquery/                     # jQuery library
│       ├── jquery-validation/          # Plugin kiểm tra form
│       └── jquery-validation-unobtrusive/  # jQuery unobtrusive validation
│
├── 📄 templates/                       # Template HTML chung
│   ├── base.html                       # Template cơ sở (public site)
│   ├── base_admin.html                 # Template cơ sở (admin site)
│   └── partials/
│       ├── _messages.html              # Component hiển thị thông báo
│       └── _pagination.html            # Component phân trang
│
├── 📸 media/                           # Tệp người dùng tải lên
│   ├── products/                       # Ảnh sản phẩm
│   └── avatars/                        # Ảnh đại diện người dùng
│
├── ✅ tests/                           # Kiểm thử tự động
│   ├── __init__.py
│   ├── test_models.py                  # Test Models
│   ├── test_views.py                   # Test Views
│   └── test_services.py                # Test Services
│
├── 📋 fixtures/                        # Dữ liệu mẫu JSON
│   ├── categories.json                 # Danh mục sản phẩm mẫu
│   └── products.json                   # Sản phẩm mẫu
│
├── 🔧 SQL/                             # Script SQL
│   └── setup_database.sql              # Script thiết lập DB
│
├── 🎨 Wireframe/                       # Mockup/Thiết kế giao diện
│   ├── Biểu đồ phân cấp chức năng/
│   ├── Đăng nhập, Đăng ký/
│   ├── Danh mục/
│   ├── Dashboard/
│   ├── Đơn hàng/
│   ├── Khung AI/
│   ├── Nhà Cung Cấp/
│   ├── Quản Lý Giỏ Hàng/
│   ├── Sản Phẩm/
│   ├── Tài khoản/
│   └── Thống kê/
│
├── 🌐 wwwroot/                         # Tệp tĩnh (.NET style)
│   ├── css/                            # CSS files
│   ├── images/                         # Ảnh
│   ├── js/                             # JavaScript
│   └── lib/                            # Thư viện bên ngoài
│
├── 🐍 File gốc - Chạy dự án
│   ├── manage.py                       # ⭐ Script chính Django (runserver, migrate, etc.)
│   ├── requirements.txt                # Danh sách package Python cần cài
│   ├── run.py                          # Script khởi động (tùy chọn)
│   ├── .gitignore                      # Git ignore patterns
│   ├── __init__.py                     # Khởi tạo module Python
│   └── .git/                           # Git repository metadata
│
└── 📁 Thư mục khác
    └── .venv/                          # Virtual environment Python (nếu có)
```

---

## 🎯 Giải thích chi tiết từng phần

### 1️⃣ **config/ - Cấu hình Django** ⭐ QUAN TRỌNG

Thư mục này chứa tất cả cấu hình chính của Django dự án:

| File | Mô tả |
|------|-------|
| `settings.py` | **Cấu hình chính**: Cơ sở dữ liệu, ứng dụng cài đặt, xác thực, tệp tĩnh, media files, email, logging, v.v. |
| `urls.py` | **Routing chính**: Tất cả URL của trang web được điều hướng qua đây trước khi đi đến các app khác |
| `wsgi.py` | **WSGI Application**: Dùng để chạy dự án trên máy chủ production (Apache, Nginx, Gunicorn) |
| `asgi.py` | **ASGI Application**: Dùng cho async, websocket, real-time chat |

**Khi nào chỉnh sửa?**
- `settings.py`: Khi thêm app mới, cấu hình email, đổi database, cấu hình file tĩnh
- `urls.py`: Khi thêm route mới hoặc app mới
- `wsgi.py` & `asgi.py`: Thường không cần sửa (chỉ khi deploy)

---

### 2️⃣ **docs/ - Tài liệu dự án**

Chứa các file hướng dẫn tài liệu:

| File | Mô tả |
|------|-------|
| `PROJECT_STRUCTURE.md` | 📋 Tài liệu này - giải thích cấu trúc dự án |
| `PROMPT_ADMIN_WEBSTORE.md` | 📖 Hướng dẫn quản trị webstore |

---

### 3️⃣ **apps/ - Các ứng dụng Django** ⭐ LÕI ỨNG DỤNG

Đây là phần **LÕI** của dự án - chứa tất cả logic chính, chia thành các module độc lập:

#### 🔧 **apps/core/** - Tiện ích chung
Chứa các hàm, decorator, mixin dùng chung cho toàn bộ ứng dụng:
- `decorators.py` - Decorator kiểm tra quyền (@admin_required, @login_required, etc.)
- `mixins.py` - Mixin class cho class-based views
- `utils.py` - Hàm tiện ích dùng chung

#### 🔐 **apps/auth/** - Xác thực & Đăng nhập
Quản lý tất cả xác thực người dùng:
- **Chức năng**: Đăng nhập, đăng xuất, đăng ký, quên mật khẩu
- **Files**: views.py, forms.py, urls.py, templates/
- **URL routes**: `/auth/login/`, `/auth/register/`, `/auth/logout/`, `/auth/forgot-password/`

#### 👥 **apps/users/** - Quản lý người dùng
Quản lý thông tin người dùng, hồ sơ, quyền hạn:
- **Models**: User (thừa kế AbstractUser), Roles (Admin, Employee, Customer)
- **Chức năng**: CRUD tài khoản, chỉnh sửa hồ sơ, phân quyền
- **Admin**: Quản lý danh sách người dùng trong Django Admin

#### 🛍️ **apps/products/** - Quản lý sản phẩm ⭐ QUAN TRỌNG
Quản lý tất cả sản phẩm, danh mục, nhà cung cấp:
- **Models**:
  - `Category` - Danh mục (Laptop, Desktop, Smartphone, etc.)
  - `Product` - Sản phẩm chi tiết
  - `Supplier` - Nhà cung cấp
  - `ProductVariant` - Biến thể (màu sắc, kích thước, RAM)
  - `ProductImage` - Ảnh sản phẩm
- **Chức năng**: CRUD sản phẩm, danh mục, nhà cung cấp
- **URL routes**: `/products/admin/`, `/categories/admin/`, `/suppliers/admin/`
- **Admin**: Quản lý tất cả sản phẩm

#### 🛒 **apps/cart/** - Giỏ hàng
Quản lý giỏ hàng khách hàng:
- **Models**: Cart, CartItem
- **Chức năng**: Thêm/xóa/cập nhật giỏ hàng (AJAX - không reload trang)
- **URL routes**: `/cart/add/`, `/cart/update/`, `/cart/remove/`

#### 📦 **apps/orders/** - Quản lý đơn hàng ⭐ QUAN TRỌNG
Quản lý tất cả đơn hàng từ khách hàng:
- **Models**: Order, OrderItem
- **Chức năng**: Tạo, xem, cập nhật trạng thái, hủy đơn hàng
- **Trạng thái**: Chưa xử lý → Đã xác nhận → Đang giao → Đã giao
- **URL routes**: `/orders/`, `/orders/<id>/`, `/orders/<id>/update-status/`
- **Admin**: Quản lý tất cả đơn hàng

#### 📊 **apps/inventory/** - Quản lý kho hàng
Quản lý tồn kho sản phẩm:
- **Models**: Inventory, ReceiptShipment (phiếu nhập/xuất)
- **Chức năng**: Cập nhật số lượng, theo dõi kho, nhập/xuất hàng
- **URL routes**: `/inventory/`, `/inventory/add/`, `/inventory/update/`

#### 📈 **apps/dashboard/** - Bảng điều khiển Admin
Trang tổng quan cho Admin với thống kê:
- **Hiển thị**: Tổng sản phẩm, tổng đơn hàng, doanh thu, số khách, v.v.
- **Chức năng**: Biểu đồ, báo cáo, thống kê doanh số
- **URL routes**: `/dashboard/`, `/dashboard/stats/`, `/dashboard/reports/`

#### 🏪 **apps/shop/** - Giao diện cửa hàng công khai
Trang chủ và giao diện mua sắm cho khách hàng:
- **Chức năng**: Hiển thị sản phẩm, tìm kiếm, lọc theo danh mục, xem chi tiết
- **URL routes**: `/shop/`, `/shop/products/`, `/shop/products/<id>/`
- **Templates**: index.html, products.html, product_detail.html

#### 💬 **apps/chat/** - AI Chat (Tùy chọn)
Chatbot AI để hỗ trợ khách hàng:
- **Models**: ChatMessage, ChatSession
- **Chức năng**: Gửi/nhận tin nhắn, quản lý phiên chat
- **URL routes**: `/chat/api/send/`, `/chat/api/messages/`

---

### 4️⃣ **Models/ - Định nghĩa cấu trúc dữ liệu**

Thư mục này chứa các file Python định nghĩa Models (cấu trúc bảng database):

| File | Mô tả | Bảng database |
|------|-------|---------------|
| `User.py` | Model người dùng (tài khoản, hồ sơ) | users |
| `Product.py` | Model sản phẩm chi tiết | products |
| `Category.py` | Model danh mục sản phẩm | categories |
| `Supplier.py` | Model nhà cung cấp | suppliers |
| `Cart.py` | Model giỏ hàng | carts |
| `Order.py` | Model đơn hàng | orders |
| `Inventory.py` | Model tồn kho | inventories |
| `ReceiptShipment.py` | Model phiếu nhập/xuất | receipt_shipments |
| `Chat.py` | Model tin nhắn chat | chat_messages |
| `AI.py` | Model AI settings | ai_configs |

**Lưu ý**: Các models này được định nghĩa trong file riêng, nhưng trong Django thực tế thường được đặt trong `apps/<app_name>/models.py`

---

### 5️⃣ **Views/ - Template HTML**

Thư mục chứa các file HTML giao diện:

| Thư mục | Mô tả |
|---------|-------|
| `Login/` | Giao diện đăng nhập (login.html), đăng ký (register.html) |
| `Admin/` | Giao diện quản trị (dashboard, quản lý sản phẩm, đơn hàng) |
| `Customer/` | Giao diện khách hàng (trang chủ, sản phẩm, tài khoản) |

---

### 6️⃣ **Controller/ - Logic xử lý dữ liệu**

Chứa các class/function xử lý logic:
- `Controller.py` - Chứa các method CRUD (Create, Read, Update, Delete)

**Lưu ý**: Trong Django, logic này thường nằm ở `apps/<app_name>/views.py` hoặc `services.py`

---

### 7️⃣ **Data/ - Quản lý cơ sở dữ liệu**

| File | Mô tả |
|------|-------|
| `database.py` | Cấu hình kết nối cơ sở dữ liệu |
| `Seed/seed_data.py` | Script tạo dữ liệu mẫu ban đầu |

**Khi nào dùng?**
- Chạy `seed_data.py` để nạp dữ liệu mẫu vào database
- Cấu hình kết nối database khác nhau (SQLite, PostgreSQL, MySQL)

---

### 8️⃣ **static/ - Tệp tĩnh** 🎨

Chứa CSS, JavaScript, ảnh không thay đổi:

```
static/
├── css/
│   ├── homepage.css               # CSS trang chủ
│   ├── shop-layout-animations.css # CSS animation cửa hàng (hiệu ứng)
│   ├── shop-refresh.css           # CSS phần làm mới sản phẩm
│   ├── site.css                   # CSS chung toàn site
│   └── style.css                  # CSS chính
├── js/
│   ├── main.js                    # JavaScript chính
│   └── site.js                    # JavaScript chung
├── images/
│   └── products/                  # Ảnh sản phẩm tĩnh (placeholder)
└── lib/
    ├── bootstrap/                 # Bootstrap CSS framework
    ├── jquery/                    # jQuery library
    ├── jquery-validation/         # Plugin kiểm tra form
    └── jquery-validation-unobtrusive/  # Unobtrusive validation plugin
```

**Khi nào thêm file?**
- Viết CSS mới → `static/css/`
- Viết JavaScript mới → `static/js/`
- Thêm ảnh tĩnh (logo, icons) → `static/images/`
- Thêm thư viện → `static/lib/`

---

### 9️⃣ **templates/ - Template HTML chung**

Chứa các file HTML dùng chung cho toàn ứng dụng:

| File | Mô tả |
|------|-------|
| `base.html` | 📄 **Template cơ sở** - Header, footer, navigation cho trang công khai |
| `base_admin.html` | 📄 **Template cơ sở Admin** - Sidebar, header cho trang quản trị |
| `partials/_messages.html` | 🔔 Component hiển thị thông báo/cảnh báo |
| `partials/_pagination.html` | 📑 Component phân trang (Previous, Next buttons) |

**Cách dùng**:
- Các template khác `{% extends "base.html" %}` để thừa kế
- `{% include "partials/_messages.html" %}` để include components

---

### 🔟 **media/ - Tệp người dùng tải lên** 📸

Chứa tất cả ảnh do người dùng hoặc admin tải lên:

```
media/
├── products/    # Ảnh sản phẩm (được admin tải lên)
│   ├── iphone-13.jpg
│   ├── laptop-asus.png
│   └── ...
└── avatars/     # Ảnh đại diện người dùng
    ├── user-1.jpg
    ├── user-2.jpg
    └── ...
```

**Lưu ý**: Những file này được lưu trên máy chủ khi người dùng upload, không nên commit lên Git

---

### 1️⃣1️⃣ **tests/ - Kiểm thử tự động** ✅

Chứa các file kiểm thử để đảm bảo code hoạt động đúng:

| File | Mô tả |
|------|-------|
| `test_models.py` | Kiểm thử tất cả Models (xem có lỗi không) |
| `test_views.py` | Kiểm thử tất cả Views (URL, Response) |
| `test_services.py` | Kiểm thử Services (Business logic) |

**Chạy tests**:
```bash
python manage.py test
```

---

### 1️⃣2️⃣ **fixtures/ - Dữ liệu mẫu**

Chứa dữ liệu JSON để nạp vào database:

```
fixtures/
├── categories.json    # Danh mục sản phẩm mẫu
│   [
│     {"name": "Laptop", "description": "Máy tính xách tay"},
│     {"name": "Desktop", "description": "Máy tính để bàn"}
│   ]
│
└── products.json      # Sản phẩm mẫu
    [
      {"name": "iPhone 13", "price": 999, "category": 1},
      {"name": "MacBook Pro", "price": 1999, "category": 1}
    ]
```

**Nạp dữ liệu mẫu**:
```bash
python manage.py loaddata fixtures/categories.json fixtures/products.json
```

---

### 1️⃣3️⃣ **SQL/ - Script SQL**

Chứa các script SQL:

| File | Mô tả |
|------|-------|
| `setup_database.sql` | Script SQL thiết lập database ban đầu (tạo bảng, trigger, etc.) |

---

### 1️⃣4️⃣ **Wireframe/ - Thiết kế giao diện**

Chứa mockup/thiết kế giao diện dự án:

```
Wireframe/
├── Biểu đồ phân cấp chức năng/    # Sơ đồ các chức năng chính
├── Đăng nhập, Đăng ký/           # Thiết kế trang login/register
├── Danh mục/                     # Thiết kế trang danh mục
├── Dashboard/                    # Thiết kế dashboard admin
├── Đơn hàng/                     # Thiết kế trang đơn hàng
├── Khung AI/                     # Thiết kế khung chat AI
├── Nhà Cung Cấp/                 # Thiết kế quản lý nhà cung cấp
├── Quản Lý Giỏ Hàng/             # Thiết kế giỏ hàng
├── Sản Phẩm/                     # Thiết kế trang sản phẩm
├── Tài khoản/                    # Thiết kế trang tài khoản
└── Thống kê/                     # Thiết kế trang thống kê
```

---

### 1️⃣5️⃣ **wwwroot/ - Tệp tĩnh (.NET style)**

Thư mục tệp tĩnh thay thế (có thể từ .NET legacy):

```
wwwroot/
├── css/               # CSS files
├── images/            # Ảnh
├── js/                # JavaScript
└── lib/               # Thư viện bên ngoài
```

---

### 1️⃣6️⃣ **File gốc - Chạy dự án**

| File | Mô tả | Khi nào dùng |
|------|-------|-------------|
| `manage.py` | ⭐ **Script chính Django** | Mọi lệnh Django: runserver, migrate, makemigrations, etc. |
| `requirements.txt` | Danh sách package Python cần cài | `pip install -r requirements.txt` để cài tất cả package |
| `run.py` | Script khởi động (tùy chọn) | Thay thế cho `python manage.py runserver` |
| `.gitignore` | Git ignore patterns | Chỉ định file không commit lên Git |
| `__init__.py` | Khởi tạo module Python | Bắt buộc để Python nhận diện đây là package |

---

## 📋 Bảng so sánh nhanh

| Thư mục | Mục đích | Ví dụ | Khi nào sửa |
|---------|---------|--------|-----------|
| **config/** | Cấu hình Django | settings.py, urls.py | Thêm app, cấu hình DB |
| **docs/** | Tài liệu | README, hướng dẫn | Cập nhật hướng dẫn |
| **apps/** | Logic ứng dụng | users, products, orders | Phát triển tính năng mới |
| **Models/** | Cấu trúc DB | User, Product, Order | Thêm bảng, fields mới |
| **Views/** | Giao diện HTML | login.html, dashboard | Thiết kế UI/UX |
| **Controller/** | Xử lý logic | CRUD operations | Viết logic xử lý |
| **Data/** | Quản lý DB | database config | Thay đổi DB connection |
| **static/** | CSS, JS, ảnh tĩnh | bootstrap, main.js | Thêm style, animation |
| **templates/** | HTML chung | base.html, components | Cập nhật layout chung |
| **media/** | Ảnh người dùng | product images | Automatic (user upload) |
| **tests/** | Kiểm thử | test_models.py | Viết test khi dev |
| **fixtures/** | Dữ liệu mẫu | categories.json | Thêm dữ liệu mẫu |
| **SQL/** | Script DB | setup.sql | Thiết lập DB mới |
| **Wireframe/** | Mockup | dashboard design | Design phase |
| **wwwroot/** | Tệp tĩnh (.NET) | CSS, JS | Legacy code |

---

## 🚀 Quick Start - Bắt đầu nhanh

### 1. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 2. Chạy migrations (tạo bảng database)
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Tạo tài khoản admin
```bash
python manage.py createsuperuser
# Nhập username, email, password
```

### 4. Chạy server
```bash
python manage.py runserver
# Hoặc: python run.py
```

### 5. Truy cập
- 🏪 **Cửa hàng:** http://localhost:8000
- 🔐 **Đăng nhập:** http://localhost:8000/auth/login
- 👨‍💼 **Admin:** http://localhost:8000/admin

---

## 📌 Những thứ cần nhớ

✅ **LUÔN** chạy `python manage.py makemigrations && python manage.py migrate` sau khi thay đổi Models

✅ **LUÔN** dùng `/media/` cho ảnh người dùng tải lên, `/static/` cho ảnh tĩnh

✅ **LUÔN** thêm app vào `config/settings.py` trong `INSTALLED_APPS` khi tạo app mới

✅ **KHÔNG** commit `/media/`, `/static/collections/`, `*.sqlite3`, `.env` lên Git

❌ **KHÔNG** sửa `/config/wsgi.py` hay `/config/asgi.py` khi develop

❌ **KHÔNG** đặt secret key, password vào code - dùng `.env` file thay

---

## 📚 Tài liệu thêm

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Best Practices](https://docs.djangoproject.com/en/stable/intro/install/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [jQuery Documentation](https://jquery.com/)


