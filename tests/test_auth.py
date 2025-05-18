from fastapi.testclient import TestClient
import sys
import os

# Get the absolute path to the project's root directory (one level up from the 'tests' folder)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the project root to sys.path if it's not already there
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from main import app


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
    response = client.post(
        "/api/auth/login", data={"email": "alkadiene@gmail.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data or "token" in data
