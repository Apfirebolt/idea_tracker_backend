import pytest
from fastapi.testclient import TestClient

from main import app  # Adjust import if your FastAPI app is in a different module

client = TestClient(app)


def test_register():
    response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data or "username" in data


def test_login():
    # Ensure the user exists (register if needed)
    client.post(
        "/register",
        json={
            "username": "testuser2",
            "email": "testuser2@example.com",
            "password": "testpassword",
        },
    )
    response = client.post(
        "/login", data={"username": "testuser2", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data or "token" in data
