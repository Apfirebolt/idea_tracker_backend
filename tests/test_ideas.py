import pytest
from fastapi.testclient import TestClient
import sys
import os

# Get the absolute path to the project's root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the project root to sys.path if it's not already there
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from main import app  # Import your FastAPI app instance

client = TestClient(app)  # Create a TestClient instance for making requests


@pytest.fixture
def user_with_token():
    """
    Pytest fixture to create a user and return their authentication headers.
    This fixture encapsulates the login logic, making tests cleaner.
    """
    def _create_user():
        #  It's good practice to use more descriptive variable names.
        login_data = {"email": "alkadiene@gmail.com", "password": "pass12345"}  # Use "email" instead of "alkadiene"
        response = client.post("api/auth/login", json=login_data)  # Send data as JSON

        #  Check for successful login before extracting the token.  This is crucial.
        assert response.status_code == 200, f"Login failed: {response.text}.  Request: {login_data}"

        response_json = response.json()
        #  Use a more robust way to get the token, handling potential key errors.
        token = response_json.get("access_token") or response_json.get("token")
        assert token is not None, f"Token not found in login response: {response_json}"
        return {"Authorization": f"Bearer {token}"}

    return _create_user



def test_create_idea(user_with_token):
    """
    Test case for creating an idea.
    Uses the user_with_token fixture to get the authentication headers.
    """
    headers = user_with_token()
    idea_data = {"title": "New Again", "description": "New idea description test"}
    response = client.post("api/ideas", json=idea_data, headers=headers)

    #  Check the response status code and the content.
    assert response.status_code == 201, f"Failed to create idea: {response.text}"
    response_json = response.json()
    assert response_json["title"] == "New Again", "Incorrect title in response"


def test_get_ideas(user_with_token):
    """
    Test case for retrieving all ideas.
    Uses the user_with_token fixture to get the authentication headers.
    """
    headers = user_with_token()
    response = client.get("api/ideas", headers=headers)

    #  Check the response status code and the content.
    assert response.status_code == 200, f"Failed to retrieve ideas: {response.text}"
    response_json = response.json()
    assert isinstance(response_json, list), "Response is not a list"
    assert len(response_json) > 0, "No ideas found in response"


def test_get_idea_by_id(user_with_token):
    """
    Test case for retrieving an idea by its ID.
    Uses the user_with_token fixture to get the authentication headers.
    """
    headers = user_with_token()
    idea_id = 3  # Replace with a valid idea ID
    response = client.get(f"api/ideas/{idea_id}", headers=headers)
    #  Check the response status code and the content.
    assert response.status_code == 200, f"Failed to retrieve idea: {response.text}"


def test_update_idea(user_with_token):
    """
    Test case for updating an idea.
    Uses the user_with_token fixture to get the authentication headers.
    """
    headers = user_with_token()
    idea_id = 3  # Replace with a valid idea ID

    update_data = {"title": "Updated Idea", "description": "Updated description"}
    response = client.put(f"api/ideas/{idea_id}", json=update_data, headers=headers)
    #  Check the response status code and the content.
    assert response.status_code == 200, f"Failed to update idea: {response.text}"
    response_json = response.json()
    assert response_json["title"] == "Updated Idea", "Title not updated correctly"
    assert response_json["description"] == "Updated description", "Description not updated correctly"


def test_delete_idea(user_with_token):
    """
    Test case for deleting an idea.
    Uses the user_with_token fixture to get the authentication headers.
    """
    headers = user_with_token()
    idea_id = 2  # Replace with a valid idea ID

    response = client.delete(f"api/ideas/{idea_id}", headers=headers)
    #  Check the response status code.
    assert response.status_code == 204, f"Failed to delete idea: {response.text}"
