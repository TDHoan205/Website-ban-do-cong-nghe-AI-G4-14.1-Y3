"""
Database Configuration - Kết nối SQL Server
Tương tự Data/AppDbContext.cs trong ASP.NET Core
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
import urllib

# Cấu hình SQL Server - Sửa theo server của bạn
SQL_SERVER_CONFIG = {
    "server": "DESKTOP-1TM8FSO",
    "database": "TechShopWebsite2",
    "driver": "ODBC Driver 17 for SQL Server",
    "trusted_connection": "yes",  # Windows Authentication
    # Nếu dùng SQL Authentication:
    # "username": "sa",
    # "password": "YourPassword",
    # "trusted_connection": "no",
}


def build_connection_string() -> str:
    """Xây dựng Connection String cho SQL Server"""
    if SQL_SERVER_CONFIG.get("trusted_connection", "yes") == "yes":
        params = urllib.parse.quote(
            f"DRIVER={{{SQL_SERVER_CONFIG['driver']}}};"
            f"SERVER={SQL_SERVER_CONFIG['server']};"
            f"DATABASE={SQL_SERVER_CONFIG['database']};"
            f"Trusted_Connection=yes;"
            f"TrustServerCertificate=yes;"
        )
    else:
        username = SQL_SERVER_CONFIG.get("username", "")
        password = SQL_SERVER_CONFIG.get("password", "")
        params = urllib.parse.quote(
            f"DRIVER={{{SQL_SERVER_CONFIG['driver']}}};"
            f"SERVER={SQL_SERVER_CONFIG['server']};"
            f"DATABASE={SQL_SERVER_CONFIG['database']};"
            f"UID={username};"
            f"PWD={password};"
            f"TrustServerCertificate=yes;"
        )
    return f"mssql+pyodbc:///?odbc_connect={params}"


# SQLAlchemy Engine
DATABASE_URL = build_connection_string()

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False,  # Bật True để xem SQL logs
)

# Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative Base (tương đương Entity base class)
Base = declarative_base()


def get_db():
    """Dependency Injection cho Database Session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Khởi tạo Database - Import tất cả models"""
    from Models import (
        Account, Employee, Role,
        Category, Supplier, Inventory, ReceiptShipment,
        Product, ProductVariant, ProductImage,
        Cart, CartItem,
        Order, OrderItem,
        ChatSession, ChatMessage, AIConversationLog, FAQ, Notification, KnowledgeChunk
    )
    Base.metadata.create_all(bind=engine)


def get_connection_info() -> dict:
    """Lấy thông tin kết nối"""
    return {
        "server": SQL_SERVER_CONFIG["server"],
        "database": SQL_SERVER_CONFIG["database"],
        "auth_mode": "Windows" if SQL_SERVER_CONFIG.get("trusted_connection") == "yes" else "SQL",
    }
