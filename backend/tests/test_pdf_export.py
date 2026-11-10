def test_csv_export(client, admin_headers):
    """Verifies that survey CSV export streams valid text/csv data."""
    response = client.get("/api/v1/surveys/export/csv", headers=admin_headers)
    assert response.status_code == 200
    assert "text/csv" in response.headers.get("content-type", "")
    assert "attachment" in response.headers.get("content-disposition", "")
    content = response.text
    assert "Respondent Code" in content
    assert "Farming Method" in content


def test_pdf_report_generation(client, admin_headers):
    """Verifies that ReportLab PDF generation creates a valid binary PDF document."""
    response = client.get("/api/v1/surveys/export/pdf", headers=admin_headers)
    assert response.status_code == 200
    assert "application/pdf" in response.headers.get("content-type", "")
    assert "attachment" in response.headers.get("content-disposition", "")
    # Check standard PDF magic header (%PDF-)
    assert response.content.startswith(b"%PDF-")
