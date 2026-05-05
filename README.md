# 🛒 Website-bán-đồ-Công-Nghệ-AI-G4-14.1-Y3

**Website thương mại điện tử bán đồ công nghệ với AI Chatbot hỗ trợ khách hàng**

> Phiên bản Python/FastAPI - Tham khảo từ [Website-ban-do-CN-Webstore-cs](../Website-ban-do-CN-Webstore-cs/README.md)

---

## 📋 Mapping C# → Python

| C# (ASP.NET Core) | Python (FastAPI) | Mô tả |
|-------------------|------------------|-------|
| `Models/*.cs` | `models/*.py` | Entity/Database models |
| `ViewModels/*.cs` | `schemas/*.py` | DTOs (Data Transfer Objects) |
| `Controllers/*.cs` | `routers/*.py` | API Endpoints |
| `Services/*.cs` | `services/*.py` | Business Logic Layer |
| `Data/Context.cs` | `core/database.py` | Database connection |
| `appsettings.json` | `core/config.py` | Configuration |
| `Program.cs` | `main.py` | Entry point |

---

## 📁 Cấu Trúc Thư Mục Chi Tiết

```
Website-ban-do-cong-nghe-AI-G4-14.1-Y3/
│
├── backend/                          # FastAPI Backend
│   │
│   ├── app/
│   │   ├── __init__.py             # Package init (empty)
│   │   │
│   │   ├── main.py                 # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │   │   # Tương ứng: Program.cs trong C#
│   │   │   # Mục đích: Entry point của ứng dụng FastAPI
│   │   │   # Chức năng:
│   │   │   #   - Khởi tạo FastAPI app
│   │   │   #   - Đăng ký CORS
│   │   │   #   - Mount routers (API endpoints)
│   │   │   #   - Khởi tạo database tables
│   │   │   #   - Chạy server
│   │   │   # API: http://localhost:8000
│   │   │   # Docs: http://localhost:8000/docs
│   │   │   # ReDoc: http://localhost:8000/redoc
│   │   │
│   │   ├── core/                    # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │   │   # Tương ứng: Configuration trong C#
│   │   │   # Mục đích: Các thiết lập cốt lõi của ứng dụng
│   │   │   #
│   │   │   ├── __init__.py         # Package init
│   │   │   │
│   │   │   ├── config.py           # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │   │   │   # Tương ứng: appsettings.json
│   │   │   │   # Mục đích: Cấu hình ứng dụng (settings)
│   │   │   │   # Chức năng:
│   │   │   │   #   - Database URL (SQLite/PostgreSQL)
│   │   │   │   #   - JWT Secret Key
│   │   │   │   #   - JWT Algorithm
│   │   │   │   #   - Access Token Expire Minutes
│   │   │   │   #   - CORS Origins
│   │   │   │   # Cách dùng: from app.core.config import settings
│   │   │   │
│   │   │   ├── database.py         # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │   │   │   # Tương ứng: Data/ApplicationDbContext.cs
│   │   │   │   # Mục đích: Kết nối và quản lý database
│   │   │   │   # Chức năng:
│   │   │   │   #   - Tạo SQLAlchemy Engine
│   │   │   │   #   - Tạo SessionLocal (DbContext)
│   │   │   │   #   - Dependency get_db() cho API endpoints
│   │   │   │   #   - Tạo bảng tự động (Base.metadata.create_all)
│   │   │   │   # Cách dùng: db = Depends(get_db)
│   │   │   │
│   │   │   └── security.py        # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │   │       # Tương ứng: Services/AuthService.cs (phần security)
│   │   │       # Mục đích: Bảo mật và xác thực
│   │   │       # Chức năng:
│   │   │       #   - Hash password (bcrypt)
│   │   │       #   - Verify password
│   │   │       #   - Create access token (JWT)
│   │   │       #   - Decode/Verify JWT token
│   │   │       #   - OAuth2 scheme cho FastAPI
│   │   │       #   - get_current_user dependency
│   │   │
│   │   ├── models/                 # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │   │   # Tương ứng: Models/ trong C#
│   │   │   # Mục đích: Định nghĩa các Entity/Database models
│   │   │   # ORM: SQLAlchemy
│   │   │   #
│   │   │   ├── __init__.py         # Xuất tất cả models
│   │   │   │
│   │   │   ├── user.py            # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │   │   │   # Tương ứng: Models/Account.cs, Models/Employee.cs
│   │   │   │   # Mục đích: Model User và Role
│   │   │   │   # Chức năng:
│   │   │   │   #   - User: Tài khoản người dùng
│   │   │   │   #   - Role: Phân quyền (Admin, Staff, Customer)
│   │   │   │   # Trường: user_id, username, email, password_hash,
│   │   │   │   #          full_name, phone, address, role_id, is_active
│   │   │   │
│   │   │   ├── product.py         # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │   │   │   # Tương ứng: Models/Product.cs + Models/Category.cs
│   │   │   │   # Mục đích: Model sản phẩm và danh mục
│   │   │   │   # Chức năng:
│   │   │   │   #   - Product: Sản phẩm chính
│   │   │   │   #   - Category: Danh mục sản phẩm
│   │   │   │   #   - ProductVariant: Biến thể (màu, storage, RAM)
│   │   │   │   #   - ProductImage: Hình ảnh sản phẩm
│   │   │   │   #   - Supplier: Nhà cung cấp
│   │   │   │   #   - Inventory: Tồn kho
│   │   │   │
│   │   │   ├── cart.py           # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │   │   │   # Tương ứng: Models/CartItem.cs
│   │   │   │   # Mục đích: Model giỏ hàng
│   │   │   │   # Chức năng:
│   │   │   │   #   - Cart: Giỏ hàng (có thể anonymous bằng session_id)
│   │   │   │   #   - CartItem: Item trong giỏ hàng
│   │   │   │
│   │   │   ├── order.py          # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │   │   │   # Tương ứng: Models/Order.cs + Models/OrderItem.cs
│   │   │   │   # Mục đích: Model đơn hàng
│   │   │   │   # Chức năng:
│   │   │   │   #   - Order: Đơn hàng
│   │   │   │   #   - OrderItem: Chi tiết đơn hàng
│   │   │   │
│   │   │   └── role.py           # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │   │       # Tương ứng: Models/Role.cs
│   │   │       # Mục đích: Định nghĩa các role
│   │   │       # Trường: role_id, role_name
│   │   │       # Values: Admin=1, Staff=2, Customer=3
│   │   │
│   │   ├── schemas/               # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │   │   # Tương ứng: ViewModels/ trong C#
│   │   │   # Mục đích: DTOs (Data Transfer Objects)
│   │   │   # ORM: Pydantic
│   │   │   #
│   │   │   ├── __init__.py         # Xuất tất cả schemas
│   │   │   │
│   │   │   ├── user.py            # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │   │   │   # Tương ứng: ViewModels/UserViewModel.cs
│   │   │   │   # Mục đích: DTO cho User
│   │   │   │   # Chức năng:
│   │   │   │   #   - UserCreate: Đăng ký (username, email, password)
│   │   │   │   #   - UserLogin: Đăng nhập (username, password)
│   │   │   │   #   - UserResponse: Response trả về
│   │   │   │   #   - UserUpdate: Cập nhật thông tin
│   │   │   │   #   - Token: JWT token response
│   │   │   │
│   │   │   ├── product.py         # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │   │   │   # Tương ứng: ViewModels/ProductViewModel.cs
│   │   │   │   # Mục đích: DTO cho Product
│   │   │   │   # Chức năng:
│   │   │   │   #   - ProductCreate: Tạo sản phẩm
│   │   │   │   #   - ProductUpdate: Cập nhật sản phẩm
│   │   │   │   #   - ProductResponse: Response sản phẩm
│   │   │   │   #   - ProductListResponse: Response có phân trang
│   │   │   │   #   - ProductVariant schemas
│   │   │   │
│   │   │   ├── cart.py            # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │   │   │   # Tương ứng: ViewModels/CartViewModel.cs
│   │   │   │   # Mục đích: DTO cho Cart
│   │   │   │   # Chức năng:
│   │   │   │   #   - CartItemCreate: Thêm vào giỏ
│   │   │   │   #   - CartItemUpdate: Cập nhật số lượng
│   │   │   │   #   - CartResponse: Response giỏ hàng
│   │   │   │
│   │   │   ├── order.py          # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │   │   │   # Tương ứng: ViewModels/OrderViewModel.cs
│   │   │   │   # Mục đích: DTO cho Order
│   │   │   │   # Chức năng:
│   │   │   │   #   - OrderCreate: Tạo đơn hàng
│   │   │   │   #   - OrderUpdate: Cập nhật trạng thái
│   │   │   │   #   - OrderResponse: Response đơn hàng
│   │   │   │   #   - OrderItemResponse: Chi tiết item
│   │   │   │
│   │   │   └── chat.py           # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │   │       # Mục đích: DTO cho Chat AI
│   │   │       # Chức năng:
│   │   │       #   - ChatMessage: Tin nhắn gửi lên
│   │   │       #   - ChatResponse: Response từ AI
│   │   │       # Trường: message, session_id, context, response,
│   │   │       #          intent, suggested_products, action
│   │   │
│   │   ├── routers/              # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │   │   # Tương ứng: Controllers/ trong C#
│   │   │   # Mục đích: Định nghĩa API Endpoints
│   │   │   #
│   │   │   ├── __init__.py         # Xuất tất cả routers
│   │   │   │
│   │   │   ├── auth.py            # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │   │   │   # Tương ứng: Controllers/AuthController.cs
│   │   │   │   # Mục đích: API xác thực người dùng
│   │   │   │   # Endpoints:
│   │   │   │   #   - POST /api/v1/auth/register - Đăng ký
│   │   │   │   #   - POST /api/v1/auth/login - Đăng nhập
│   │   │   │   #   - GET /api/v1/auth/me - Lấy thông tin user hiện tại
│   │   │   │   #   - PUT /api/v1/auth/password - Đổi mật khẩu
│   │   │   │
│   │   │   ├── products.py        # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │   │   │   # Tương ứng: Controllers/ProductsController.cs
│   │   │   │   # Mục đích: API quản lý sản phẩm
│   │   │   │   # Endpoints:
│   │   │   │   #   - GET /api/v1/products/ - Danh sách (phân trang)
│   │   │   │   #   - GET /api/v1/products/{id} - Chi tiết
│   │   │   │   #   - GET /api/v1/products/featured - Sản phẩm nổi bật
│   │   │   │   #   - GET /api/v1/products/search - Tìm kiếm
│   │   │   │   #   - POST /api/v1/products/ - Tạo mới (admin)
│   │   │   │   #   - PUT /api/v1/products/{id} - Cập nhật (admin)
│   │   │   │   #   - DELETE /api/v1/products/{id} - Xóa (admin)
│   │   │   │
│   │   │   ├── categories.py      # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │   │   │   # Tương ứng: Controllers/CategoriesController.cs
│   │   │   │   # Mục đích: API quản lý danh mục
│   │   │   │   # Endpoints:
│   │   │   │   #   - GET /api/v1/categories/ - Danh sách
│   │   │   │   #   - GET /api/v1/categories/{id} - Chi tiết
│   │   │   │   #   - POST /api/v1/categories/ - Tạo mới (admin)
│   │   │   │   #   - PUT /api/v1/categories/{id} - Cập nhật (admin)
│   │   │   │   #   - DELETE /api/v1/categories/{id} - Xóa (admin)
│   │   │   │
│   │   │   ├── cart.py           # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │   │   │   # Tương ứng: Controllers/CartItemsController.cs
│   │   │   │   # Mục đích: API quản lý giỏ hàng
│   │   │   │   # Endpoints:
│   │   │   │   #   - GET /api/v1/cart/ - Lấy giỏ hàng
│   │   │   │   #   - POST /api/v1/cart/add - Thêm vào giỏ
│   │   │   │   #   - PUT /api/v1/cart/update/{id} - Cập nhật số lượng
│   │   │   │   #   - DELETE /api/v1/cart/remove/{id} - Xóa khỏi giỏ
│   │   │   │   #   - DELETE /api/v1/cart/clear - Xóa toàn bộ giỏ
│   │   │   │
│   │   │   ├── orders.py         # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │   │   │   # Tương ứng: Controllers/OrdersController.cs
│   │   │   │   # Mục đích: API quản lý đơn hàng
│   │   │   │   # Endpoints:
│   │   │   │   #   - GET /api/v1/orders/ - Danh sách (phân trang)
│   │   │   │   #   - GET /api/v1/orders/{id} - Chi tiết đơn hàng
│   │   │   │   #   - POST /api/v1/orders/ - Tạo đơn hàng mới
│   │   │   │   #   - PUT /api/v1/orders/{id}/status - Cập nhật trạng thái
│   │   │   │   #   - DELETE /api/v1/orders/{id} - Hủy đơn hàng
│   │   │   │
│   │   │   └── chat.py           # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │   │       # Tương ứng: Controllers/ChatController.cs
│   │   │       # Mục đích: API AI Chatbot
│   │   │       # Endpoints:
│   │   │       #   - POST /api/v1/chat/ - Gửi tin nhắn
│   │   │       #   - WS /api/v1/chat/ws/{session_id} - WebSocket chat
│   │   │
│   │   └── services/              # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │       # Tương ứng: Services/ trong C#
│   │       # Mục đích: Business Logic Layer
│   │       #
│   │       ├── __init__.py         # Xuất tất cả services
│   │       │
│   │       ├── auth_service.py    # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │       │   # Tương ứng: Services/AuthService.cs
│   │       │   # Mục đích: Logic nghiệp vụ xác thực
│   │       │   # Chức năng:
│   │       │   #   - authenticate_user: Xác thực đăng nhập
│   │       │   #   - register_user: Đăng ký tài khoản mới
│   │       │   #   - get_user_by_username: Lấy user theo username
│   │       │   #   - create_access_token: Tạo JWT token
│   │       │
│   │       ├── product_service.py # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │       │   # Tương ứng: Services/ProductService.cs
│   │       │   # Mục đích: Logic nghiệp vụ sản phẩm
│   │       │   # Chức năng:
│   │       │   #   - get_products: Lấy danh sách (filter, sort, paginate)
│   │       │   #   - get_product_by_id: Lấy chi tiết
│   │       │   #   - get_featured_products: Sản phẩm nổi bật
│   │       │   #   - search_products: Tìm kiếm
│   │       │   #   - create_product: Tạo mới
│   │       │   #   - update_product: Cập nhật
│   │       │   #   - delete_product: Xóa
│   │       │
│   │       ├── order_service.py   # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │       │   # Tương ứng: Services/OrderService.cs
│   │       │   # Mục đích: Logic nghiệp vụ đơn hàng
│   │       │   # Chức năng:
│   │       │   #   - create_order: Tạo đơn hàng từ giỏ hàng
│   │       │   #   - get_orders: Lấy danh sách đơn hàng
│   │       │   #   - get_order_by_id: Lấy chi tiết đơn hàng
│   │       │   #   - update_order_status: Cập nhật trạng thái
│   │       │   #   - cancel_order: Hủy đơn hàng
│   │       │
│   │       ├── chatbot_service.py  # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │       │   # Mục đích: Xử lý tin nhắn chat với AI
│   │       │   # Chức năng:
│   │       │   #   - IntentClassifier: Phân loại ý định người dùng
│   │       │   #   - ChatBotService: Xử lý chat chính
│   │       │   #   - process_message: Xử lý tin nhắn, trả về response
│   │       │   # Intents: greeting, product_inquiry, price_inquiry,
│   │       │   #           order_status, cart, complaint, human_request
│   │       │
│   │       ├── rag_pipeline.py    # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │       │   # Mục đích: RAG Pipeline cho AI
│   │       │   # Chức năng:
│   │       │   #   - retrieve: Truy xuất sản phẩm liên quan
│   │       │   #   - generate_context: Tạo context cho AI
│   │       │   #   - query: Query chính (retrieve + generate)
│   │       │
│   │       └── embedding_service.py # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │           # Mục đích: Text Embedding và tìm kiếm sản phẩm
│   │           # Chức năng:
│   │           #   - get_product_text: Chuyển product thành text
│   │           #   - get_all_product_embeddings: Load tất cả embeddings
│   │           #   - search_products: Tìm kiếm sản phẩm theo query
│   │
│   ├── scripts/                   # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │   # Tương ứng: Data/Seed/SeedData.cs trong C#
│   │   # Mục đích: Các script chạy một lần (seed, setup)
│   │   │
│   │   ├── __init__.py
│   │   │
│   │   ├── seed_data.py          # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │   │   # Tương ứng: Data/Seed/SeedData.cs
│   │   │   # Mục đích: Tạo dữ liệu mẫu ban đầu
│   │   │   # Chạy: python -m scripts.seed_data
│   │   │   # Chức năng:
│   │   │   #   - seed_roles: Tạo 3 roles (Admin, Staff, Customer)
│   │   │   #   - seed_suppliers: Tạo 5 nhà cung cấp
│   │   │   #   - seed_categories: Tạo 7 danh mục
│   │   │   #   - seed_products: Tạo 12 sản phẩm mẫu
│   │   │   #   - seed_users: Tạo 3 tài khoản test
│   │   │   #   - seed_sample_orders: Tạo đơn hàng mẫu
│   │   │
│   │   └── create_embeddings.py # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │       # Mục đích: Tạo embeddings cho AI chatbot
│   │       # Chạy: python -m scripts.create_embeddings
│   │
│   ├── tests/                     # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │   # Tương ứng: UnitTests/ trong C#
│   │   # Mục đích: Unit tests cho API
│   │   │
│   │   └── test_api.py           # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │       # Mục đích: Viết tests cho các API endpoints
│   │       # Framework: pytest + FastAPI TestClient
│   │       # Chạy: pytest tests/ -v
│   │       # Tests:
│   │       #   - test_health_check: Kiểm tra /health
│   │       #   - test_register_user: Test đăng ký
│   │       #   - test_login: Test đăng nhập
│   │       #   - test_get_products: Test lấy danh sách sản phẩm
│   │       #   - test_chat: Test chat AI
│   │
│   ├── requirements.txt           # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │   # Tương ứng: webstore.csproj (packages)
│   │   # Mục đích: Danh sách Python packages cần cài đặt
│   │   # Chạy: pip install -r requirements.txt
│   │
│   ├── Dockerfile                 # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │   # Tương ứng: Dockerfile trong containerization
│   │   # Mục đích: Build Docker image cho backend
│   │   # Build: docker build -t techstore-backend .
│   │   # Run: docker run -p 8000:8000 techstore-backend
│   │
│   ├── docker-compose.yml         # ━━━━━━━━━━━━━━━━━━━━━━━━━
│   │   # Tương ứng: docker-compose.yml
│   │   # Mục đích: Chạy toàn bộ stack (Backend + DB)
│   │   # Run: docker-compose up -d
│   │
│   └── README.md                  # ━━━━━━━━━━━━━━━━━━━━━━━━━
│       # Mục đích: Tài liệu hướng dẫn sử dụng
│
├── frontend/                      # Next.js Frontend
│   │
│   ├── app/                       # App Router pages
│   │   ├── layout.tsx            # Root layout
│   │   ├── page.tsx              # Trang chủ
│   │   ├── products/page.tsx     # Danh sách sản phẩm
│   │   ├── cart/page.tsx         # Giỏ hàng
│   │   ├── login/page.tsx        # Đăng nhập
│   │   └── admin/                # Admin Dashboard
│   │
│   ├── components/                # React components
│   │   ├── navbar.tsx            # Navigation bar
│   │   ├── providers.tsx         # React Query provider
│   │   └── chat/
│   │       └── chat-widget.tsx   # AI Chat Widget
│   │
│   ├── lib/                       # Utilities
│   │   ├── api.ts                # Axios client
│   │   ├── types.ts              # TypeScript interfaces
│   │   └── utils.ts              # Helper functions
│   │
│   ├── stores/                    # Zustand stores
│   │   └── index.ts              # Auth + Cart state
│   │
│   ├── hooks/                     # Custom hooks
│   │   └── useApi.ts             # React Query hooks
│   │
│   ├── package.json               # Dependencies
│   ├── tailwind.config.js         # TailwindCSS config
│   └── tsconfig.json              # TypeScript config
│
└── README.md                      # (File này)
```

---

## 🎯 Hướng Dẫn Sử Dụng

### Chạy Backend

```bash
cd backend

# 1. Tạo virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
# hoặc
source venv/bin/activate  # Linux/Mac

# 2. Cài đặt packages
pip install -r requirements.txt

# 3. Seed dữ liệu
python -m scripts.seed_data

# 4. Chạy server
uvicorn app.main:app --reload
```

### Chạy Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 🔑 Tài Khoản Test

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin |
| staff01 | staff123 | Staff |
| customer01 | customer123 | Customer |

---

## 📊 API Endpoints Summary

| Module | Endpoint | Method | Mô tả |
|--------|----------|--------|-------|
| Auth | `/api/v1/auth/register` | POST | Đăng ký |
| Auth | `/api/v1/auth/login` | POST | Đăng nhập |
| Auth | `/api/v1/auth/me` | GET | Thông tin user |
| Products | `/api/v1/products/` | GET | Danh sách sản phẩm |
| Products | `/api/v1/products/{id}` | GET | Chi tiết sản phẩm |
| Products | `/api/v1/products/featured` | GET | Sản phẩm nổi bật |
| Products | `/api/v1/products/search` | GET | Tìm kiếm |
| Categories | `/api/v1/categories/` | GET | Danh sách danh mục |
| Cart | `/api/v1/cart/` | GET | Lấy giỏ hàng |
| Cart | `/api/v1/cart/add` | POST | Thêm vào giỏ |
| Orders | `/api/v1/orders/` | GET | Danh sách đơn hàng |
| Orders | `/api/v1/orders/` | POST | Tạo đơn hàng |
| Chat | `/api/v1/chat/` | POST | Gửi tin nhắn AI |

---

## 🔄 So Sánh C# vs Python

### 1. Entry Point

```csharp
// C# - Program.cs
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddControllersWithViews();
var app = builder.Build();
```

```python
# Python - main.py
from fastapi import FastAPI
app = FastAPI()
```

### 2. Database Model

```csharp
// C# - Models/Product.cs
public class Product {
    public int ProductId { get; set; }
    public string Name { get; set; }
    public decimal Price { get; set; }
}
```

```python
# Python - models/product.py
class Product(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
```

### 3. API Controller

```csharp
// C# - Controllers/ProductsController.cs
[HttpGet]
public async Task<ActionResult<IEnumerable<Product>>> GetProducts() {
    return await _context.Products.ToListAsync();
}
```

```python
# Python - routers/products.py
@router.get("/", response_model=PaginatedResponse)
async def get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products
```

### 4. DTO/Schema

```csharp
// C# - ViewModels/ProductViewModel.cs
public class ProductCreateDto {
    public string Name { get; set; }
    public decimal Price { get; set; }
}
```

```python
# Python - schemas/product.py
class ProductCreate(BaseModel):
    name: str
    price: float
```

---

## 👥 Phân Công Công Việc

| Người | Nhiệm vụ | Thời gian |
|-------|----------|-----------|
| Người 1 | Backend API, AI Core | 7 ngày |
| Người 2 | Database, Vector DB, Seed Data | 3 ngày |
| Người 3 | Frontend User UI | 7 ngày |
| Người 4 | Admin Dashboard, Staff Chat | 7 ngày |

---

## 📝 Ghi Chú

- Cấu trúc này tham khảo từ [Website-ban-do-CN-Webstore-cs](../Website-ban-do-CN-Webstore-cs/README.md)
- Backend sử dụng **FastAPI** thay vì ASP.NET Core
- Frontend sử dụng **Next.js 14** (App Router) thay vì Razor Pages
- AI Chatbot sử dụng **RAG Pipeline** để tư vấn sản phẩm
