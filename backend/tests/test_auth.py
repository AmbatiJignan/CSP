def test_admin_login_success(client):
    """Verifies that the administrator can authenticate with correct credentials."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "AdminPass123!"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["username"] == "admin"
    assert data["role"] == "superadmin"


def test_admin_login_invalid_password(client):
    """Verifies that invalid credentials are rejected with 401."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "WrongPassword!"},
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_admin_me_endpoint(client, admin_headers):
    """Verifies that the /me endpoint returns the authenticated admin profile."""
    response = client.get("/api/v1/auth/me", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "admin"
    assert data["is_active"] is True


def test_unauthorized_access_rejected(client):
    """Verifies that protected admin endpoints reject unauthenticated requests with 401."""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
