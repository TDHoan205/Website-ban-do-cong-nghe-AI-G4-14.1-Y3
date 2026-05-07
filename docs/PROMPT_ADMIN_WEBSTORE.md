# PROMPT: Xây dựng hệ thống Admin WebStore với React + Django

---

## MÔ TẢ DỰ ÁN

Bạn là chuyên gia React + Django Senior. Hãy xây dựng hệ thống Admin "WebStore" cho trang bán đồ công nghệ AI với:

- **Frontend**: React + Vite + Bootstrap 5
- **Backend**: Django + Django REST Framework
- **UI Theme**: Navy (#0F2340) theo thiết kế Wireframe

---

## NGUỒN THAM KHẢO (CONTEXT)

### 1. Models (Django ORM)

Sử dụng các models trong `store/models.py`:

```python
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, related_name='products')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Account(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('customer', 'Customer'),
    ]
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Will be hashed
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    order_number = models.CharField(max_length=50, unique=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    shipping_address = models.TextField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Cart(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
```

### 2. Cấu trúc dự án hiện tại

```
Website-ban-do-cong-nghe-AI-G4-14.1-Y3/
├── manage.py                    # Django entry point
├── store/                       # Django app chính
│   ├── __init__.py
│   ├── settings.py              # Django settings
│   ├── urls.py                  # Root URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── api/                         # Django REST Framework app
│   ├── __init__.py
│   ├── serializers.py           # DRF Serializers
│   ├── views.py                 # API Views
│   ├── urls.py                  # API URLs
│   └── admin.py
├── store/
│   ├── __init__.py
│   ├── models.py                # Django Models
│   ├── admin.py                 # Django Admin
│   └── migrations/
├── Admin/                       # React Frontend
│   └── src/
│       ├── services/
│       │   └── api.js          # API service (đã có)
│       ├── components/
│       │   └── Layout/
│       │       └── Sidebar.jsx  # Sidebar Navy (#0F2340)
│       ├── pages/
│       │   ├── Dashboard.jsx
│       │   ├── Products.jsx
│       │   ├── Orders.jsx
│       │   └── Accounts.jsx
│       └── App.jsx
```

### 3. API Service hiện có

File `Admin/src/services/api.js` đã có cấu trúc:

```javascript
const API_BASE_URL = 'http://localhost:8000/api';

// Export các API functions:
// - dashboardAPI.getStats()
// - productsAPI.getAll(), productsAPI.create(), productsAPI.update(), productsAPI.delete()
// - categoriesAPI.getAll(), categoriesAPI.create(), categoriesAPI.update(), categoriesAPI.delete()
// - suppliersAPI.getAll(), suppliersAPI.create(), suppliersAPI.update(), suppliersAPI.delete()
// - ordersAPI.getAll(), ordersAPI.getById()
// - accountsAPI.getAll()
```

### 4. Django REST Framework Backend dự kiến

#### Cấu trúc URLs:

```
/api/                          # API Root
├── dashboard/
│   └── stats/                 # GET /api/dashboard/stats/
├── categories/
│   ├── GET/POST              # /api/categories/
│   └── GET/PUT/DELETE/<id>/  # /api/categories/<id>/
├── suppliers/
│   ├── GET/POST              # /api/suppliers/
│   └── GET/PUT/DELETE/<id>/  # /api/suppliers/<id>/
├── products/
│   ├── GET/POST              # /api/products/
│   └── GET/PUT/DELETE/<id>/  # /api/products/<id>/
├── orders/
│   ├── GET/POST              # /api/orders/
│   └── GET/<id>/             # /api/orders/<id>/
├── accounts/
│   └── GET                   # /api/accounts/
└── health/
    └── GET                   # /api/health/
```

---

## NHIỆM VỤ CẦN THỰC HIỆN

### Nhiệm vụ 1: Cấu hình Django Project

Thiết lập Django project với cấu trúc:

```
store/                          # Main Django project
├── settings.py                # Cấu hình database SQLite, INSTALLED_APPS
├── urls.py                    # Root URL config
└── wsgi.py

api/                           # REST API app
├── views.py                   # APIViews
├── serializers.py             # DRF Serializers
└── urls.py                    # API routes
```

#### Cấu hình settings.py:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'store',
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Thêm vào đầu
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:5173',
]
```

### Nhiệm vụ 2: Hoàn thiện Base Layout (Sidebar + MainContent)

Kiểm tra và cập nhật `Admin/src/components/Layout/Sidebar.jsx`:

- Sidebar màu Navy (#0F2340)
- Các menu items với icon Bootstrap Icons
- Active state cho menu hiện tại
- Responsive design (collapsible trên mobile)

Cấu trúc Layout:

```
┌─────────────────────────────────────────────────┐
│  Sidebar (Navy)  │  Main Content Area (#F8FAFC) │
│  - Logo          │  ┌─────────────────────────┐  │
│  - Dashboard    │  │ Page Header             │  │
│  - Products     │  ├─────────────────────────┤  │
│  - Categories   │  │ Content Cards/Tables    │  │
│  - Suppliers    │  │                         │  │
│  - Orders       │  │                         │  │
│  - Accounts    │  └─────────────────────────┘  │
│  - Settings     │                              │
└─────────────────────────────────────────────────┘
```

### Nhiệm vụ 3: Hoàn thiện Backend API

Tạo `api/serializers.py` với DRF Serializers:

```python
from rest_framework import serializers
from store.models import Category, Supplier, Product, Order, Account

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'contact_name', 'email', 'phone', 'address', 'created_at', 'updated_at']

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'image', 
                  'category', 'category_name', 'supplier', 'supplier_name', 
                  'is_active', 'created_at', 'updated_at']
```

Tạo `api/views.py` với APIViews:

```python
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from store.models import Category, Supplier, Product, Order, Account
from .serializers import CategorySerializer, SupplierSerializer, ProductSerializer

@api_view(['GET'])
def dashboard_stats(request):
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_accounts = Account.objects.count()
    total_categories = Category.objects.count()
    
    return Response({
        'total_products': total_products,
        'total_orders': total_orders,
        'total_accounts': total_accounts,
        'total_categories': total_categories,
    })

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category', 'supplier').all()
    serializer_class = ProductSerializer
```

Tạo `api/urls.py`:

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import dashboard_stats, CategoryViewSet, SupplierViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('dashboard/stats/', dashboard_stats, name='dashboard-stats'),
    path('', include(router.urls)),
]
```

### Nhiệm vụ 4: Xây dựng React Components cho Categories

Tạo `Admin/src/pages/Categories.jsx`:

```javascript
// Tính năng:
// - Hiển thị danh sách categories trong table
// - Search/filter categories
// - Nút Thêm mới (mở Modal)
// - Nút Sửa (mở Modal với dữ liệu)
// - Nút Xóa (confirm dialog)
// - Sử dụng Bootstrap 5: table-hover, rounded-3 buttons
// - Modal Bootstrap cho form Add/Edit
```

### Nhiệm vụ 5: Xây dựng React Components cho Suppliers

Tạo `Admin/src/pages/Suppliers.jsx`:

```javascript
// Tính năng:
// - Hiển thị danh sách suppliers trong table
// - Search/filter suppliers
// - CRUD operations (Add, Edit, Delete)
// - Modal Bootstrap cho form
// - Sử dụng categoriesAPI từ services/api.js
```

---

## YÊU CẦU KỸ THUẬT

### Frontend (React)

1. **Cấu trúc Component**: Mỗi page là một file riêng trong `pages/`
2. **State Management**: Sử dụng React Hooks (useState, useEffect)
3. **API Calls**: Sử dụng functions từ `services/api.js`
4. **UI Components**:
   - Bootstrap 5 classes: `table`, `table-hover`, `btn`, `btn-primary`, `rounded-3`
   - Bootstrap Icons: `<i className="bi bi-..."></i>`
   - Modal: `className="modal fade"`, `className="modal-dialog"`
5. **Styling**: Sử dụng CSS từ `src/styles/` hoặc inline styles

### Backend (Django)

1. **Database**: Sử dụng Django ORM với SQLite (có thể chuyển sang MySQL/PostgreSQL sau)
2. **REST API**: Django REST Framework
3. **CORS**: django-cors-headers
4. **Models**: Định nghĩa trong `store/models.py`
5. **Serializers**: Chuyển đổi Django models <-> JSON
6. **Views**: ModelViewSet cho CRUD tự động
7. **Response Format**: DRF Response với structure:

```json
{
  "id": 1,
  "name": "Category Name",
  "description": "Description text"
}
```

### UI/UX

1. **Màu sắc**:
   - Sidebar: Navy (#0F2340)
   - Background: #F8FAFC
   - Primary Button: Navy
   - Success: #22C55E
   - Danger: #EF4444
   - Warning: #F59E0B

2. **Tables**: Bootstrap 5 table classes
3. **Buttons**: `rounded-3` border-radius
4. **Modals**: Bootstrap 5 modal structure
5. **Forms**: Bootstrap 5 form controls

---

## THỨ TỰ THỰC HIỆN

### Bước 1: Cài đặt Django dependencies

```bash
pip install django djangorestframework django-cors-headers
```

### Bước 2: Tạo Django project structure

```bash
django-admin startproject store .
python manage.py startapp api
```

### Bước 3: Cấu hình Django settings

Cập nhật `store/settings.py`:
- Thêm apps vào INSTALLED_APPS
- Cấu hình CORS
- Cấu hình database

### Bước 4: Tạo Models

Tạo/Update `store/models.py` với đầy đủ models

### Bước 5: Chạy migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Bước 6: Tạo Serializers

Tạo `api/serializers.py`

### Bước 7: Tạo API Views

Tạo `api/views.py` với ViewSets

### Bước 8: Cấu hình URLs

Tạo `api/urls.py` và update `store/urls.py`

### Bước 9: Kiểm tra Sidebar

Xem lại `Sidebar.jsx` đảm bảo đúng màu Navy và responsive

### Bước 10: Tạo Categories Page

Tạo `Admin/src/pages/Categories.jsx`

### Bước 11: Tạo Suppliers Page

Tạo `Admin/src/pages/Suppliers.jsx`

### Bước 12: Test toàn bộ

- Backend: `python manage.py runserver` (port 8000)
- Frontend: `npm run dev` (port 3000/5173)

---

## CÁC BƯỚC TRONG CURSOR

1. **Gắn Files (Tagging)**: Gõ `@` và chọn:
   - `@store/models.py`
   - `@api/views.py`
   - `@api/serializers.py`
   - `@Admin/src/services/api.js`
   - `@Admin/src/components/Layout/Sidebar.jsx`

2. **Đính kèm Wireframe**: Kéo ảnh Sidebar/Design vào chat (nếu có)

3. **Nhấn "Apply"**: Sau khi code được tạo

4. **Kiểm tra**:
   - Backend: `python manage.py runserver` (port 8000)
   - Frontend: `npm run dev` (port 3000)
   - Truy cập: http://localhost:8000/api/categories/
   - Kiểm tra giao diện và chức năng CRUD

---

## PROMPT CHO TỪNG BƯỚC

### Bước 1: "Thiết lập Django project"

Tạo Django project với cấu trúc:
- Django project: `store/`
- Django app: `api/`
- Cấu hình settings.py với DRF và CORS

### Bước 2: "Tạo Django Models"

Dựa trên cấu trúc SQLAlchemy hiện có, chuyển đổi sang Django ORM:
- Category, Supplier, Product, Account, Order, OrderItem, Cart, CartItem

### Bước 3: "Tạo DRF Serializers"

Tạo `api/serializers.py` với serializers cho mỗi model

### Bước 4: "Tạo API Views"

Tạo `api/views.py` với ModelViewSet cho CRUD tự động

### Bước 5: "Cấu hình URLs"

Tạo URL routing cho API endpoints

### Bước 6: "Chạy Migrations"

```bash
python manage.py makemigrations
python manage.py migrate
```

### Bước 7: "Tạo Superuser"

```bash
python manage.py createsuperuser
```

### Bước 8: "Kiểm tra Sidebar"

Hãy kiểm tra và cập nhật `Admin/src/components/Layout/Sidebar.jsx` để đảm bảo:
- Màu Navy (#0F2340) cho background
- Menu items: Dashboard, Products, Categories, Suppliers, Orders, Accounts
- Active state highlight
- Responsive collapsible

### Bước 9: "Tạo Categories Page"

Tạo `Admin/src/pages/Categories.jsx` với:
- Table Bootstrap 5
- Search functionality
- Modal Bootstrap cho Add/Edit
- Delete confirmation
- Kết nối API qua services/api.js

### Bước 10: "Tạo Suppliers Page"

Tương tự Categories page

---

## LƯU Ý QUAN TRỌNG

1. **SỬ DỤNG DJANGO** - Đây là dự án Django + React
2. **Sử dụng Django ORM** cho database operations
3. **Django REST Framework** cho API endpoints
4. **React Hooks** cho state management
5. **Bootstrap 5** cho UI components
6. **API Service** đã có trong `services/api.js` - chỉ cần gọi
7. **Màu Navy** (#0F2340) là màu chủ đạo cho Sidebar
8. **Port Django**: 8000 (thay vì 5001 như Flask)

---

## KẾT QUẢ MONG ĐỢI

- ✅ Django project cấu hình đúng cách
- ✅ Django Models tương thích với cấu trúc hiện tại
- ✅ REST API hoạt động đầy đủ
- ✅ Sidebar Navy hoạt động tốt
- ✅ Categories CRUD đầy đủ (Backend + Frontend)
- ✅ Suppliers CRUD đầy đủ (Backend + Frontend)
- ✅ Giao diện nhất quán với Bootstrap 5
- ✅ API kết nối hoạt động
