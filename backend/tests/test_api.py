from fastapi.testclient import TestClient

from app import crud
from app.main import app

client = TestClient(app)


def setup_function():
    crud._store.clear()


def test_health_api_returns_ok_status():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_user_list_api_returns_json_array():
    response = client.get("/users/")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)


def test_create_user_api_returns_created_user_json():
    payload = {
        "email": "ci-user@example.com",
        "password": "StrongPass123",
        "full_name": "CI Test User",
    }

    response = client.post("/users/", json=payload)

    assert response.status_code == 201

    data = response.json()
    assert isinstance(data, dict)
    assert isinstance(data["id"], str)
    assert data["email"] == payload["email"]
    assert data["full_name"] == payload["full_name"]
    assert data["is_active"] is True
    assert "created_at" in data
    assert "password" not in data
    assert "hashed_password" not in data
