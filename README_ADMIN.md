# TechShop Website - Hướng dẫn cài đặt và chạy

## Mục lục
1. [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
2. [Cài đặt nhanh](#cài-đặt-nhanh)
3. [Cấu hình Database](#cấu-hình-database)
4. [Chạy website](#chạy-website)
5. [Truy cập các trang](#truy-cập-các-trang)
6. [Cấu trúc thư mục](#cấu-trúc-thư-mục)
7. [Xử lý lỗi thường gặp](#xử-lý-lỗi-thường-gặp)

---

## Yêu cầu hệ thống

| Yêu cầu | Phiên bản tối thiểu |
|----------|---------------------|
| Python | 3.9+ |
| pip | Mới nhất |
| RAM | 4GB trở lên |
| Dung lượng ổ cứng | 500MB |

**Tùy chọn Database:**
- **SQLite** (Mặc định - không cần cài đặt thêm)
- **SQL Server** (Cần SQL Server 2016+)

---

## Cài đặt nhanh

### Bước 1: Tải và giải nén project

```bash
# Di chuyển vào thư mục project
cd "C:\Code full\CURSOR-JG-DEV\Website-ban-do-cong-nghe-AI-G4-14.1-Y3"
```

### Bước 2: Tạo môi trường ảo (Virtual Environment)

```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
# Windows CMD:
venv\Scripts\activate

# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Linux/Mac:
source venv/bin/activate
```

> **Lưu ý:** Nếu gặp lỗi khi chạy PowerShell, hãy chạy lệnh sau trước:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### Bước 3: Cài đặt các thư viện

```bash
pip install -r requirements.txt
```

Nếu gặp lỗi, cài đặt thủ công:
```bash
pip install Django==4.2.9
pip install django-crispy-forms
pip install django-filter
pip install python-dotenv
pip install requests
pip install Pillow
```

---

## Cấu hình Database

### Cách 1: Sử dụng SQLite (Mặc định - Khuyến nghị)

Tạo file `.env` trong thư mục gốc project với nội dung:

```env
SECRET_KEY=django-insecure-abc123xyz456... (tạo chuỗi ngẫu nhiên)
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# SQLite (Mặc định)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

### Cách 2: Sử dụng SQL Server

```env
SECRET_KEY=django-insecure-abc123xyz456...
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# SQL Server
DB_ENGINE=django.db.backends.sqlserver
DB_HOST=localhost
DB_PORT=1433
DB_NAME=TechShopWebsite1
DB_USER=sa
DB_PASSWORD=YourPassword123
```

**Tạo Database trong SQL Server:**
```sql
-- Chạy trong SQL Server Management Studio (SSMS)
CREATE DATABASE TechShopWebsite1;
```

---

## Chạy website

### Bước 1: Tạo Database và Migrate

```bash
# Chạy migrations để tạo các bảng
python manage.py migrate
```

### Bước 2: (Tùy chọn) Tạo dữ liệu mẫu

```bash
# Tạo dữ liệu mẫu (users, products, categories...)
python manage.py shell < scripts/create_sample_data.py
```

Hoặc chạy file Python trực tiếp:
```bash
python fake_migration.py
python fake_users_migration.py
```

### Bước 3: Tạo tài khoản Admin

```bash
python manage.py createsuperuser
```

Nhập thông tin khi được yêu cầu:
```
Username: admin
Email: admin@example.com
Password: **********
Confirm password: **********
```

### Bước 4: Chạy Server

```bash
python manage.py runserver
```

---

## Truy cập các trang

### Website người dùng (Frontend)

| Trang | URL |
|-------|-----|
| Trang chủ | http://127.0.0.1:8000/ |
| Sản phẩm | http://127.0.0.1:8000/shop/products/ |
| Chi tiết sản phẩm | http://127.0.0.1:8000/shop/products/{id}/ |
| Giỏ hàng | http://127.0.0.1:8000/shop/cart/ |
| Thanh toán | http://127.0.0.1:8000/shop/checkout/ |
| Đăng nhập | http://127.0.0.1:8000/accounts/login/ |
| Đăng ký | http://127.0.0.1:8000/accounts/register/ |
| Quên mật khẩu | http://127.0.0.1:8000/accounts/password-reset/ |

### Trang quản trị (Admin)

| Trang | URL |
|-------|-----|
| Trang chủ Admin | http://127.0.0.1:8000/ |
| Dashboard | http://127.0.0.1:8000/dashboard/ |
| Django Admin | http://127.0.0.1:8000/admin/ |
| Quản lý Users | http://127.0.0.1:8000/accounts/ |
| Quản lý Sản phẩm | http://127.0.0.1:8000/products/ |
| Quản lý Danh mục | http://127.0.0.1:8000/categories/ |
| Quản lý Thương hiệu | http://127.0.0.1:8000/brands/ |
| Quản lý Nhà cung cấp | http://127.0.0.1:8000/suppliers/ |
| Quản lý Đơn hàng | http://127.0.0.1:8000/orders/ |
| Quản lý Giỏ hàng | http://127.0.0.1:8000/cart/ |
| Quản lý Slides | http://127.0.0.1:8000/slides/ |
| Báo cáo | http://127.0.0.1:8000/reports/ |
| Chat AI | http://127.0.0.1:8000/chat/ |
| Thông báo | http://127.0.0.1:8000/notifications/ |
| FAQs | http://127.0.0.1:8000/faqs/ |
| Cài đặt | http://127.0.0.1:8000/settings/ |

---

## Tài khoản mặc định

```
Username: admin
Password: (tự tạo ở bước 3)
```

---

## Cấu trúc thư mục

```
Website-ban-do-cong-nghe-AI-G4-14.1-Y3/
├── apps/                          # Ứng dụng Django
│   ├── core/                      # Utils, decorators, mixins
│   ├── users/                     # Tài khoản, nhân viên
│   ├── authentication/             # Đăng nhập, đăng ký
│   ├── categories/                # Quản lý danh mục
│   ├── brands/                    # Quản lý thương hiệu
│   ├── suppliers/                 # Quản lý nhà cung cấp
│   ├── products/                  # Sản phẩm, biến thể, hình ảnh
│   ├── orders/                    # Đơn hàng, chi tiết đơn hàng
│   ├── cart/                      # Giỏ hàng
│   ├── inventory/                 # Quản lý kho hàng
│   ├── dashboard/                 # Trang tổng quan
│   ├── reports/                   # Báo cáo doanh thu
│   ├── chat/                      # Chat AI, chatbot
│   ├── notifications/             # Thông báo
│   ├── faqs/                      # Câu hỏi thường gặp
│   ├── reviews/                   # Đánh giá sản phẩm
│   ├── settings/                  # Cài đặt website
│   ├── slides/                   # Slides, banners
│   └── shop/                      # Frontend (người dùng)
├── config/                        # Cấu hình Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/                    # Template HTML
│   ├── shop/                      # Frontend templates
│   ├── admin/                     # Admin templates
│   └── accounts/                  # Auth templates
├── static/                        # CSS, JS, Images
│   ├── css/
│   ├── js/
│   └── images/
├── migrations_sql/                # Script SQL tạo bảng
├── scripts/                       # Script Python hỗ trợ
├── tests/                         # Unit tests
├── .env                           # Biến môi trường
├── requirements.txt              # Thư viện Python
├── manage.py                      # Django CLI
└── README.md                      # File này
```

---

## Xử lý lỗi thường gặp

### Lỗi "No module named 'django'"
```
pip install Django==4.2.9
```

### Lỗi "No module named 'crispy_forms'"
```
pip install django-crispy-forms
```

### Lỗi "No module named 'django_filters'"
```
pip install django-filter
```

### Lỗi "No module named 'dotenv'"
```
pip install python-dotenv
```

### Lỗi Database SQLite
```bash
# Xóa database cũ và tạo lại
del db.sqlite3
python manage.py migrate
```

### Lỗi kết nối SQL Server
1. Kiểm tra SQL Server đang chạy
2. Kiểm tra credentials trong `.env`
3. Kiểm tra Windows Firewall cho port 1433

### Lỗi Port bị chiếm
```bash
# Dùng port khác
python manage.py runserver 8080
python manage.py runserver 3000
```

### Lỗi Migration
```bash
# Fake migration để bỏ qua
python manage.py migrate --fake

# Hoặc reset hoàn toàn
python manage.py migrate --run-syncdb
```

---

## Các lệnh hữu ích

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

# Mở Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic

# Tạo app mới
python manage.py startapp app_name
```

---

## Tech Stack

| Công nghệ | Mô tả |
|-----------|-------|
| **Backend** | Django 4.2+ (Python) |
| **Database** | SQLite / SQL Server |
| **Frontend** | HTML5, CSS3, Bootstrap 5 |
| **JavaScript** | Vanilla JS, jQuery (CDN) |
| **Charts** | Chart.js |
| **Icons** | Font Awesome 6, Bootstrap Icons |
| **AI Chat** | OpenAI API Integration |

---

## Liên hệ hỗ trợ

Nếu gặp lỗi không có trong danh sách, vui lòng:
1. Kiểm tra file `.env` có đúng format không
2. Đảm bảo đã chạy `pip install -r requirements.txt`
3. Kiểm tra Python version: `python --version`
