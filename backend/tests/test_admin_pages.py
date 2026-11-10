def test_admin_pages_require_auth_or_render(client, admin_headers):
    """Verifies that admin pages require authentication or render with valid credentials."""
    # 1. Unauthenticated requests to /admin/dashboard redirect to /admin/login (303)
    resp = client.get("/admin/dashboard", follow_redirects=False)
    assert resp.status_code == 303
    assert "/admin/login" in resp.headers.get("location", "")

    # 2. Login with valid session
    login_resp = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "AdminPass123!"},
    )
    assert login_resp.status_code == 200

    # 3. Test that all admin pages render HTTP 200 with cookie session
    admin_routes = [
        "/admin/dashboard",
        "/admin/surveys",
        "/admin/surveys/new",
        "/admin/articles",
        "/admin/articles/new",
        "/admin/resources",
        "/admin/videos",
        "/admin/faqs",
        "/admin/feedback",
        "/admin/users",
        "/admin/audit-logs",
    ]
    for route in admin_routes:
        r = client.get(route)
        assert r.status_code == 200, f"Route {route} failed with status {r.status_code}"
        assert "text/html" in r.headers.get("content-type", "")
        assert "GreenGrow" in r.text
