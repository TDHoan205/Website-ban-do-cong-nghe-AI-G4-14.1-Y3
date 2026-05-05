# Tech Store API - Backend Documentation

## Overview

This is the backend API for a Tech Store e-commerce website with AI chatbot support, built with FastAPI.

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLAlchemy + SQLite (development) / PostgreSQL (production)
- **Authentication**: JWT (JSON Web Tokens)
- **AI**: RAG-based chatbot with intent classification
- **API Documentation**: Auto-generated OpenAPI/Swagger

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   │
│   ├── core/                # Core configuration
│   │   ├── config.py        # Settings and environment variables
│   │   ├── database.py      # Database connection
│   │   └── security.py      # JWT and authentication
│   │
│   ├── models/              # SQLAlchemy ORM models (Entities)
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── cart.py
│   │   ├── order.py
│   │   └── role.py
│   │
│   ├── schemas/             # Pydantic schemas (DTOs/ViewModels)
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── cart.py
│   │   ├── order.py
│   │   └── chat.py
│   │
│   ├── routers/             # API endpoints (Controllers)
│   │   ├── auth.py          # /api/v1/auth
│   │   ├── products.py      # /api/v1/products
│   │   ├── categories.py    # /api/v1/categories
│   │   ├── cart.py          # /api/v1/cart
│   │   ├── orders.py        # /api/v1/orders
│   │   └── chat.py          # /api/v1/chat
│   │
│   ├── services/            # Business logic layer
│   │   ├── auth_service.py
│   │   ├── product_service.py
│   │   └── order_service.py
│   │
│   └── ai/                  # AI/ML modules
│       ├── chat_service.py  # Chatbot service
│       ├── rag_pipeline.py  # RAG pipeline
│       └── embedding.py     # Text embedding
│
├── tests/                   # Unit tests
├── migrations/              # Alembic migrations
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

## API Endpoints

### Authentication (`/api/v1/auth`)
- `POST /register` - Register new user
- `POST /login` - Login (returns JWT token)
- `GET /me` - Get current user info

### Products (`/api/v1/products`)
- `GET /` - List products (with pagination, filtering, sorting)
- `GET /featured` - Get featured products
- `GET /search` - Search products
- `GET /{id}` - Get product details
- `POST /` - Create product (Admin)
- `PUT /{id}` - Update product (Admin)
- `DELETE /{id}` - Delete product (Admin)

### Categories (`/api/v1/categories`)
- `GET /` - List categories
- `GET /{id}` - Get category details
- `POST /` - Create category (Admin)
- `PUT /{id}` - Update category (Admin)
- `DELETE /{id}` - Delete category (Admin)

### Cart (`/api/v1/cart`)
- `GET /` - Get cart
- `POST /add` - Add item to cart
- `PUT /update/{product_id}` - Update quantity
- `DELETE /remove/{product_id}` - Remove item
- `DELETE /clear` - Clear cart
- `POST /merge` - Merge guest cart with user cart

### Orders (`/api/v1/orders`)
- `GET /` - List user orders
- `GET /{id}` - Get order details
- `POST /` - Create order
- `PUT /{id}` - Update order status (Admin)
- `GET /admin/all` - List all orders (Admin)

### Chat (`/api/v1/chat`)
- `POST /` - Send chat message
- `WS /ws/{session_id}` - WebSocket chat

## Running the Application

### Local Development

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

4. Access the API:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Docker

```bash
docker-compose up -d
```

## C# to Python Mapping

| C# (MVC) | Python (FastAPI) |
|----------|------------------|
| Models/*.cs | models/*.py |
| ViewModels/*.cs | schemas/*.py |
| Controllers/*.cs | routers/*.py |
| Services/*.cs | services/*.py |
| DbContext | SQLAlchemy Session |
| [ApiController] | @router decorator |
| return View() | return schema |
| HttpClient | httpx/FastAPI TestClient |

## Default Roles

| Role ID | Role Name | Permissions |
|---------|-----------|--------------|
| 1 | Admin | Full access |
| 2 | Staff | Manage products, orders |
| 3 | Customer | View, cart, orders |

## Environment Variables

See `.env.example` for configuration options.
