import uuid

from fastapi.testclient import TestClient

from app.main import app
from app import crud

client = TestClient(app)


def setup_function():
    crud._store.clear()


def test_read_users_initially_empty():
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == []


def test_create_user_returns_201_and_user_body():
    payload = {
        "email": "test@example.com",
        "password": "TestPass123",
        "full_name": "Test User",
    }

    response = client.post("/users", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["email"] == payload["email"]
    assert data["full_name"] == payload["full_name"]
    assert data["is_active"] is True
    assert "id" in data
    assert "created_at" in data


def test_get_user_by_id_returns_user():
    payload = {
        "email": "detail@example.com",
        "password": "DetailPass123",
        "full_name": "Detail User",
    }

    create_response = client.post("/users", json=payload)
    assert create_response.status_code == 201
    user_id = create_response.json()["id"]

    read_response = client.get(f"/users/{user_id}")
    assert read_response.status_code == 200

    data = read_response.json()
    assert data["id"] == user_id
    assert data["email"] == payload["email"]
    assert data["full_name"] == payload["full_name"]


def test_update_user_changes_user_fields():
    payload = {
        "email": "update@example.com",
        "password": "UpdatePass123",
        "full_name": "Update User",
    }

    create_response = client.post("/users", json=payload)
    assert create_response.status_code == 201
    user_id = create_response.json()["id"]

    update_payload = {
        "email": "updated@example.com",
        "full_name": "Updated User",
        "is_active": False,
    }
    update_response = client.put(f"/users/{user_id}", json=update_payload)
    assert update_response.status_code == 200

    updated = update_response.json()
    assert updated["email"] == update_payload["email"]
    assert updated["full_name"] == update_payload["full_name"]
    assert updated["is_active"] is False


def test_delete_user_removes_user():
    payload = {
        "email": "delete@example.com",
        "password": "DeletePass123",
        "full_name": "Delete User",
    }

    create_response = client.post("/users", json=payload)
    assert create_response.status_code == 201
    user_id = create_response.json()["id"]

    delete_response = client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 204
    assert delete_response.text == ""

    not_found_response = client.get(f"/users/{user_id}")
    assert not_found_response.status_code == 404
    assert not_found_response.json()["detail"] == "User not found"


def test_create_user_duplicate_email_returns_409():
    payload = {
        "email": "duplicate@example.com",
        "password": "DuplicatePass123",
        "full_name": "Duplicate User",
    }

    first_response = client.post("/users", json=payload)
    assert first_response.status_code == 201

    second_response = client.post("/users", json=payload)
    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Email already registered"
