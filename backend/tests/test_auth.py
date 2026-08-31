"""
StudyChart AI - Authentication Tests.
"""

def test_register_and_login_flow(client):
    # 1. Register User
    reg_data = {
        "name": "Alice Johnson",
        "email": "alice@studychart.ai",
        "password": "SecurePassword123!",
        "confirm_password": "SecurePassword123!"
    }
    resp = client.post("/api/v1/auth/register", json=reg_data)
    assert resp.status_code == 201, resp.text
    data = resp.json()
    assert "access_token" in data
    assert data["email"] == "alice@studychart.ai"

    # 2. Login User
    login_data = {
        "email": "alice@studychart.ai",
        "password": "SecurePassword123!"
    }
    login_resp = client.post("/api/v1/auth/login", json=login_data)
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]

    # 3. Access Protected Profile
    headers = {"Authorization": f"Bearer {token}"}
    me_resp = client.get("/api/v1/me", headers=headers)
    assert me_resp.status_code == 200
    assert me_resp.json()["email"] == "alice@studychart.ai"

def test_duplicate_registration_rejected(client):
    reg_data = {
        "name": "Alice Duplicate",
        "email": "alice@studychart.ai",
        "password": "SecurePassword123!",
        "confirm_password": "SecurePassword123!"
    }
    resp = client.post("/api/v1/auth/register", json=reg_data)
    assert resp.status_code == 400
    assert "already exists" in resp.json()["error"]["message"]

def test_invalid_password_rejected(client):
    login_data = {
        "email": "alice@studychart.ai",
        "password": "WrongPassword!"
    }
    resp = client.post("/api/v1/auth/login", json=login_data)
    assert resp.status_code == 401
