# TechShop Admin - Hướng dẫn cài đặt và chạy

## Yêu cầu
- Python 3.9+
- pip

## Cài đặt

### 1. Tạo môi trường ảo (Virtual Environment)

```bash
# Di chuyển vào thư mục project
cd "c:\Code full\CURSOR-JG-DEV\Website-ban-do-cong-nghe-AI-G4-14.1-Y3"

# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
# Windows:
venv\Scripts\activate

# Hoặc sử dụng PowerShell:
.\venv\Scripts\Activate.ps1
```

### 2. Cài đặt các thư viện cần thiết

```bash
pip install -r requirements.txt
```

### 3. Cấu hình Database

#### Sửa file `.env` (tạo nếu chưa có):

```
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

**Nếu muốn dùng SQL Server:**
```
DB_ENGINE=django.db.backends.sqlserver
DB_HOST=localhost
DB_NAME=TechShopWebsite1
DB_USER=sa
DB_PASSWORD=your-password
```

### 4. Tạo Database và chạy Migrate

```bash
# Tạo các bảng trong database
python manage.py makemigrations
python manage.py migrate
```

### 5. Tạo tài khoản Admin

```bash
# Tạo superuser để đăng nhập admin
python manage.py createsuperuser

# Nhập thông tin:
# Username: admin
# Email: admin@example.com
# Password: admin123
# Confirm password: admin123
```

### 6. Chạy Server

```bash
python manage.py runserver
```

## Truy cập Website

Mở trình duyệt và truy cập:

| Trang | URL |
|-------|-----|
| **Admin Dashboard** | http://127.0.0.1:8000/ |
| **Login** | http://127.0.0.1:8000/accounts/login/ |
| **Django Admin** | http://127.0.0.1:8000/admin/ |

## Tài khoản mặc định

```
Username: admin
Password: admin123
```

## Các trang quản trị

| Module | URL |
|--------|-----|
| Dashboard | `/` hoặc `/dashboard/` |
| Tài khoản | `/accounts/` |
| Danh mục | `/categories/` |
| Sản phẩm | `/products/` |
| Nhà cung cấp | `/suppliers/` |
| Đơn hàng | `/orders/` |
| Giỏ hàng | `/cart/` |
| Báo cáo | `/reports/` |
| Chat AI | `/chat/` |
| Thông báo | `/notifications/` |
| FAQs | `/faqs/` |
| Cài đặt | `/settings/` |

## Cấu trúc thư mục

```
apps/
├── core/          # Decorators, Mixins, Utils, Constants
├── users/         # Account, Employee
├── categories/    # Category CRUD
├── suppliers/     # Supplier CRUD
├── products/      # Product, Variant, Image CRUD
├── orders/       # Order, OrderItem CRUD
├── cart/          # Cart CRUD
├── dashboard/     # Dashboard, Charts
├── reports/       # Revenue Reports, Export
├── chat/          # Chat Sessions, AI Logs
├── notifications/ # Notification CRUD
├── faqs/          # FAQ CRUD
└── settings/      # Site Settings
```

## Lệnh hữu ích

```bash
# Chạy server
python manage.py runserver

# Tạo migrations
python manage.py makemigrations

# Áp dụng migrations
python manage.py migrate

# Tạo superuser
python manage.py createsuperuser

# Xem tất cả URLs
python manage.py show_urls

# Shell Django
python manage.py shell
```

## Troubleshooting

### Lỗi "No module named 'crispy_forms'"
```bash
pip install django-crispy-forms
```

### Lỗi "No module named 'django_filters'"
```bash
pip install django-filter
```

### Lỗi Database
- Kiểm tra file `.env` có đúng cấu hình không
- Chạy lại migrate: `python manage.py migrate`

### Port đã bị chiếm
```bash
# Dùng port khác
python manage.py runserver 8080
```

## Màu sắc thiết kế (từ Wireframe)

```css
--primary-blue: #3F72AF   /* Nút chính, links */
--dark-navy: #112D4E       /* Sidebar, header */
--light-bg: #F9F7F7        /* Background */
--light-gray: #DBE2EF      /* Borders */
--accent-red: #E94560       /* Notifications, delete */
--success: #2ECC71         /* Success */
--warning: #F39C12         /* Warning */
--danger: #E94560          /* Danger */
```

## Tech Stack

- **Backend**: Django 4.2+
- **Database**: SQLite (mặc định) / SQL Server
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Charts**: Chart.js
- **Icons**: Bootstrap Icons
- **Forms**: Django Crispy Forms
