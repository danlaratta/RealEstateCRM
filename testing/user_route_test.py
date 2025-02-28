import requests

BASE_URL = "http://localhost:5000"

def test_get_user():
    user_id = 1  # Change this to a valid user ID
    response = requests.get(f"{BASE_URL}/api/users/{user_id}")

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert "name" in response.json(), "Response JSON missing 'name' field"

def test_non_existent_user():
    user_id = 9999  # Non-existent user
    response = requests.get(f"{BASE_URL}/api/users/{user_id}")

    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
