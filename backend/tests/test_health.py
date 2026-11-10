def test_fastapi_startup_and_health(client):
    """Verifies that FastAPI is running and connects successfully to Oracle Database 23ai."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "database" in data
    assert data["database"]["status"] == "healthy"
    assert data["database"]["database"] == "Oracle Database 23ai"
    assert data["database"]["service"] == "FREEPDB1"
    assert data["database"]["test_query_result"] == 1
