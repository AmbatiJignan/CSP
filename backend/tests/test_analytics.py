def test_analytics_overview_contract(client, admin_headers):
    """Verifies that the analytics overview endpoint returns valid schema strictly from real records."""
    response = client.get("/api/v1/analytics/overview", headers=admin_headers)
    assert response.status_code == 200
    data = response.json()

    # Structural verification
    assert "total_responses" in data
    assert "total_articles" in data
    assert "total_resources" in data
    assert "total_faqs" in data
    assert "total_feedback" in data
    assert "farming_methods" in data
    assert "awareness_levels" in data
    assert "willingness_levels" in data
    assert "has_real_survey_data" in data

    assert isinstance(data["total_responses"], int)
    assert isinstance(data["farming_methods"], list)
