import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.fixture
def user_with_token():
    def _create_user(username, email, password):
        client.post(
            "/register",
            json={"username": username, "email": email, "password": password},
        )
        response = client.post(
            "/login", data={"username": username, "password": password}
        )
        token = response.json().get("access_token") or response.json().get("token")
        return {"Authorization": f"Bearer {token}"}

    return _create_user


def test_create_idea(user_with_token):
    headers = user_with_token("ideauser", "ideauser@example.com", "testpassword")
    response = client.post(
        "/ideas/",
        json={"title": "Test Idea", "description": "Test Description"},
        headers=headers,
    )
    assert response.status_code == 201 or response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Idea"
    assert data["description"] == "Test Description"
    assert "id" in data


def test_read_ideas(user_with_token):
    headers = user_with_token("readuser", "readuser@example.com", "testpassword")
    client.post(
        "/ideas/",
        json={"title": "Read Idea", "description": "Read Description"},
        headers=headers,
    )
    response = client.get("/ideas/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any("title" in idea for idea in data)


def test_read_single_idea(user_with_token):
    headers = user_with_token("singleuser", "singleuser@example.com", "testpassword")
    create_resp = client.post(
        "/ideas/",
        json={"title": "Single Idea", "description": "Single Description"},
        headers=headers,
    )
    idea_id = create_resp.json()["id"]
    response = client.get(f"/ideas/{idea_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == idea_id
    assert data["title"] == "Single Idea"


def test_update_idea(user_with_token):
    headers = user_with_token("updateuser", "updateuser@example.com", "testpassword")
    create_resp = client.post(
        "/ideas/",
        json={"title": "Old Title", "description": "Old Description"},
        headers=headers,
    )
    idea_id = create_resp.json()["id"]
    response = client.put(
        f"/ideas/{idea_id}",
        json={"title": "New Title", "description": "New Description"},
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["description"] == "New Description"


def test_delete_idea(user_with_token):
    headers = user_with_token("deleteuser", "deleteuser@example.com", "testpassword")
    create_resp = client.post(
        "/ideas/",
        json={"title": "Delete Me", "description": "To be deleted"},
        headers=headers,
    )
    idea_id = create_resp.json()["id"]
    response = client.delete(f"/ideas/{idea_id}", headers=headers)
    assert response.status_code == 204 or response.status_code == 200
    get_resp = client.get(f"/ideas/{idea_id}", headers=headers)
    assert get_resp.status_code == 404
