<div align="center">

# 🛒 Tech Store AI

### Website Thương Mại Điện Tử Công Nghệ với AI Chatbot Thông Minh

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![SQL Server](https://img.shields.io/badge/SQL_Server-2019+-CC2927?style=for-the-badge&logo=microsoftsqlserver&logoColor=white)](https://microsoft.com/sql-server)
[![Gemini AI](https://img.shields.io/badge/Gemini_AI-Google-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

*Được xây dựng theo mô hình MVC bằng Python/FastAPI*

</div>

---

## ✨ Tính năng nổi bật

| 🛍️ Mua sắm | 🔐 Tài khoản | 🤖 AI Chatbot | 🖥️ Quản trị |
|:---:|:---:|:---:|:---:|
| Duyệt & tìm kiếm sản phẩm | Đăng ký / Đăng nhập | Tư vấn sản phẩm thông minh | Dashboard thống kê |
| Lọc theo danh mục | Quản lý hồ sơ | Hiểu ngôn ngữ tự nhiên | Quản lý kho hàng |
| Giỏ hàng & Thanh toán | Lịch sử đơn hàng | RAG từ dữ liệu thực | Duyệt & xử lý đơn |
| Đánh giá sản phẩm | Phân quyền (Admin/Staff/Customer) | Hỗ trợ 24/7 | Quản lý người dùng |

---

## 🏗️ Kiến trúc ứng dụng

### Tổng quan MVC

```
┌─────────────────────────────────────────────────────────────────┐
│                        TRÌNH DUYỆT                              │
│              (Khách hàng gửi HTTP Request)                      │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                      app.py  ⚡                                  │
│         Khởi tạo FastAPI · Đăng ký Routes · Cấu hình           │
└──────┬──────────────────────────────────────────┬──────────────┘
       │                                          │
       ▼                                          ▼
┌──────────────────┐                   ┌─────────────────────────┐
│  Controllers/ 🎮 │                   │      wwwroot/ 🎨        │
│                  │                   │  css/ · js/ · images/   │
│  Home            │                   │  (CSS, JavaScript,      │
│  Auth            │                   │   Hình ảnh tĩnh)        │
│  Products        │                   └─────────────────────────┘
│  Cart            │
│  Orders          │
│  Chat            │
│  Admin           │
└──────┬───────────┘
       │ gọi
       ▼
┌──────────────────────────────────────────────────────────────┐
│                     Services/ ⚙️                             │
│                                                              │
│  AuthService    │ ProductService  │ CartService              │
│  OrderService   │ ChatService     │ AccountService           │
└──────┬───────────────────────────────────────┬──────────────┘
       │ truy vấn                              │ gọi AI
       ▼                                       ▼
┌──────────────────┐                  ┌────────────────────────┐
│    Models/ 📦    │                  │       AI/ 🤖           │
│                  │                  │                        │
│  Product         │                  │  gemini_client.py      │
│  Category        │                  │  rag_pipeline.py       │
│  User / Account  │                  │                        │
│  Cart / Order    │                  │  Luồng AI:             │
│  Chat / AI       │                  │  Câu hỏi → Tìm SP      │
└──────┬───────────┘                  │  → Gemini → Trả lời   │
       │                              └────────────────────────┘
       ▼
┌──────────────────────────────────────────────────────────────┐
│                 SQL Server Database 🗄️                       │
│            Database: TechShopWebsite1                        │
│     14 bảng: Products · Users · Orders · Carts · Chat...    │
└──────────────────────────────────────────────────────────────┘
       │
       (Kết quả được Controller đưa vào)
       ▼
┌──────────────────────────────────────────────────────────────┐
│                     Views/ 🖼️                                │
│              Template Engine: Jinja2                         │
│                                                              │
│  Shared/base.html    →  Layout chung (Menu, Footer)          │
│  Home/index.html     →  Trang chủ                            │
│  Products/*.html     →  Danh sách & Chi tiết sản phẩm        │
│  Cart/index.html     →  Giỏ hàng                            │
│  Orders/*.html       →  Đặt hàng, Lịch sử                   │
│  Auth/*.html         →  Đăng nhập, Đăng ký                  │
│  Chat/index.html     →  AI Chatbot                          │
│  Admin/*.html        →  Trang quản trị                       │
└──────────────────────────────────────────────────────────────┘
```

### Luồng dữ liệu thực tế (Ví dụ: Xem danh sách sản phẩm)

```
① Khách gõ URL:    http://localhost:8000/Products/
② FastAPI nhận:    → ProductsController.index()
③ Controller gọi:  → ProductService.get_all_products(page=1)
④ Service truy vấn: SELECT * FROM Products WHERE is_available = 1
⑤ Service trả về:  [Product(iPhone15), Product(Samsung S24), ...]
⑥ Controller render: TemplateResponse("Products/index.html", {"products": [...]})
⑦ Jinja2 tạo HTML: {% for p in products %} <div>{{ p.name }}</div> {% endfor %}
⑧ Trình duyệt nhận: File HTML → Hiển thị giao diện đẹp
```

---

## ⚙️ Công nghệ sử dụng

<div align="center">

| 🔧 Layer | 🛠️ Công nghệ | 📝 Mục đích |
|:--------|:------------|:-----------|
| **Web Framework** | FastAPI 0.109 | Xử lý HTTP requests, routing |
| **Template Engine** | Jinja2 3.1 | Render HTML |
| **Database** | SQL Server | Lưu trữ dữ liệu chính |
| **ORM** | SQLAlchemy 2.0 | Kết nối & truy vấn DB bằng Python |
| **DB Driver** | pyodbc | Giao tiếp với SQL Server |
| **Frontend** | Bootstrap 5 + Vanilla JS | Giao diện người dùng |
| **Auth** | JWT + bcrypt (passlib) | Đăng nhập, bảo mật token |
| **AI** | Google Gemini API | Chatbot thông minh |
| **AI Method** | RAG Pipeline | Tư vấn dựa trên dữ liệu thực |
| **Server** | Uvicorn | Chạy ứng dụng Python |

</div>

---

## 🚀 Cài đặt và chạy dự án

### Yêu cầu hệ thống

- ✅ Python **3.10+**
- ✅ SQL Server (Express/Developer/Standard)
- ✅ ODBC Driver 17 for SQL Server ([Tải tại đây](https://go.microsoft.com/fwlink/?linkid=2187214))
- ✅ Git

### Các bước cài đặt

**1️⃣ Clone dự án**
```bash
git clone https://github.com/your-repo/Website-ban-do-cong-nghe-AI-G4-14.1-Y3.git
cd Website-ban-do-cong-nghe-AI-G4-14.1-Y3
```

**2️⃣ Cài đặt Python packages**
```bash
pip install -r requirements.txt
```

**3️⃣ Tạo Database trên SQL Server**

Mở **SQL Server Management Studio (SSMS)**, kết nối server, mở file và chạy:
```
SQL/schema.sql
```
> ✅ Kết quả: Database `TechShopWebsite1` được tạo với 14 bảng

**4️⃣ Cấu hình kết nối Database**

Mở `Data/database.py`, sửa thông tin server:
```python
SQL_SERVER_CONFIG = {
    "server": "localhost",          # ← Sửa thành tên SQL Server của bạn
    "database": "TechShopWebsite1", # ← Tên database (giữ nguyên)
    "driver": "ODBC Driver 17 for SQL Server",
    "trusted_connection": "yes",    # Windows Authentication (không cần nhập mật khẩu)
}
```

> 💡 **Tìm tên server:** Mở SSMS → Tên ở ô "Server name" khi đăng nhập

**5️⃣ Seed dữ liệu mẫu**
```bash
python Data/Seed/seed_data.py
```
```
✓ Đã tạo dữ liệu danh mục
✓ Đã tạo dữ liệu nhà cung cấp
✓ Đã tạo dữ liệu sản phẩm
✓ Đã tạo tài khoản admin (admin / admin123)
```

**6️⃣ Chạy ứng dụng**
```bash
uvicorn app:app --reload
```

**7️⃣ Mở trình duyệt**

| Trang | URL |
|-------|-----|
| 🏠 Website | http://localhost:8000 |
| 🛍️ Sản phẩm | http://localhost:8000/Products/ |
| 🤖 AI Chat | http://localhost:8000/Chat/ |
| 🖥️ Admin | http://localhost:8000/Admin/ |
| 📖 API Docs | http://localhost:8000/docs |

---

## 🔑 Tài khoản mặc định

| 👤 Username | 🔒 Password | 🎭 Role | 🔗 Trang |
|:-----------|:-----------|:-------|:--------|
| `admin` | `admin123` | Admin | `/Admin/` |
| `staff01` | `staff123` | Staff | `/Chat/` |
| `customer01` | `customer123` | Customer | `/` |

---

## 📁 Cấu trúc thư mục

```
📦 Website-ban-do-cong-nghe-AI-G4-14.1-Y3/
│
├── 📄 app.py                     # Entry point FastAPI
├── 📄 requirements.txt           # Python packages
│
├── 📂 Controllers/               # 🎮 Nhận request → gọi Service → trả View
│   ├── HomeController.py         #    / · /about · /contact
│   ├── AuthController.py         #    /Auth/Login · /Register · /Logout
│   ├── ProductsController.py     #    /Products/ · /{id}
│   ├── CartController.py         #    /Cart/ · /add · /remove
│   ├── OrderController.py        #    /Orders/ · /Checkout  (cần tạo)
│   ├── ChatController.py         #    /Chat/ · /Send
│   └── AdminController.py        #    /Admin/  (cần tạo)
│
├── 📂 Services/                  # ⚙️ Xử lý logic nghiệp vụ
│   ├── AuthService.py            #    Đăng nhập, JWT, bcrypt
│   ├── ProductService.py         #    CRUD, tìm kiếm, phân trang
│   ├── CartService.py            #    Thêm/xóa/sửa giỏ hàng
│   ├── OrderService.py           #    Tạo đơn, thống kê, trạng thái
│   ├── ChatService.py            #    Phiên chat, lịch sử tin nhắn
│   └── AccountService.py         #    Quản lý tài khoản
│
├── 📂 Models/                    # 📦 Cấu trúc bảng Database (SQLAlchemy)
│   ├── Product.py                #    Products, ProductVariants, ProductImages
│   ├── Category.py               #    Categories, Suppliers, Inventory
│   ├── User.py / Account.py      #    Users, Accounts, Roles
│   ├── Cart.py                   #    Carts, CartItems
│   ├── Order.py                  #    Orders, OrderItems
│   ├── Chat.py                   #    ChatSessions, ChatMessages
│   └── AI.py                     #    AIResponse, RAGContext
│
├── 📂 Views/                     # 🖼️ Giao diện HTML (Jinja2)
│   ├── Shared/
│   │   ├── base.html             #    Layout chung (menu, footer)
│   │   └── error.html            #    Trang lỗi 404/500
│   ├── Home/                     #    Trang chủ, About, Contact
│   ├── Products/                 #    Danh sách, Chi tiết sản phẩm
│   ├── Cart/                     #    Giỏ hàng
│   ├── Auth/                     #    Đăng nhập, Đăng ký, Profile
│   ├── Orders/                   #    Đặt hàng, Lịch sử  (cần tạo)
│   ├── Chat/                     #    AI Chatbot
│   └── Admin/                    #    Dashboard, Quản lý  (cần tạo)
│
├── 📂 Data/                      # 🗄️ Kết nối Database
│   ├── database.py               #    Connection string, SessionLocal
│   └── Seed/
│       └── seed_data.py          #    Script tạo dữ liệu mẫu
│
├── 📂 SQL/
│   └── schema.sql                # 📋 CREATE TABLE cho 14 bảng
│
├── 📂 AI/                        # 🤖 AI Chatbot Module (cần tạo)
│   ├── gemini_client.py          #    Kết nối Google Gemini API
│   └── rag_pipeline.py           #    RAG: DB → Context → AI → Trả lời
│
├── 📂 wwwroot/                   # 🎨 File tĩnh
│   ├── css/style.css             #    CSS toàn trang
│   ├── js/main.js                #    JavaScript, AJAX
│   └── images/                   #    Logo, banner, ảnh sản phẩm
│
└── 📂 Utilities/                 # 🔧 Hàm dùng chung (cần tạo)
    └── __init__.py               #    PagedList (phân trang)
```

---

## 👥 Nhóm phát triển

| STT | Vai trò | Phụ trách |
|:---:|:--------|:---------|
| 1 | **Backend Lead** | Controllers, Services, AI Chatbot |
| 2 | **Database Lead** | Models, SQL Server, Seed Data |
| 3 | **Frontend Lead** | Views (Khách hàng), CSS, JS |
| 4 | **Fullstack Admin** | Views (Admin), Quản lý đơn hàng |

> 📋 Xem chi tiết phân công tại file [phan_cong_CV.txt](phan_cong_CV.txt)

---

## 📄 License
python -m uvicorn app:app --reload
MIT License © 2026 — Tech Store AI Team
