"""
Test API Script
Chạy: pytest tests/ -v
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import Base, engine, SessionLocal
from app.models import Role


@pytest.fixture(scope="module")
def test_client():
    Base.metadata.create_all(bind=engine)
    client = TestClient(app)
    yield client
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    db = session

    role = Role(role_id=3, role_name="Customer")
    db.add(role)
    db.commit()

    yield db

    db.close()
    Base.metadata.drop_all(bind=engine)


def test_health_check(test_client):
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert "Tech Store API" in response.json()["message"]


def test_register_user(test_client):
    response = test_client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "full_name": "Test User",
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"


def test_login(test_client):
    test_client.post(
        "/api/v1/auth/register",
        json={
            "username": "logintest",
            "email": "login@example.com",
            "password": "testpass123",
        }
    )

    response = test_client.post(
        "/api/v1/auth/login",
        data={
            "username": "logintest",
            "password": "testpass123",
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(test_client):
    response = test_client.post(
        "/api/v1/auth/login",
        data={
            "username": "nonexistent",
            "password": "wrongpass",
        }
    )
    assert response.status_code == 401


def test_get_products(test_client):
    response = test_client.get("/api/v1/products/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data


def test_get_featured_products(test_client):
    response = test_client.get("/api/v1/products/featured?type=new&count=5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_search_products(test_client):
    response = test_client.get("/api/v1/products/search?q=iPhone&count=5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_categories(test_client):
    response = test_client.get("/api/v1/categories/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_chat(test_client):
    response = test_client.post(
        "/api/v1/chat/",
        json={
            "message": "Tôi muốn mua laptop",
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "session_id" in data
