def test_public_pages_render_html(client):
    """Verifies that all required public modules render responsive HTML pages with HTTP 200."""
    pages = [
        "/",
        "/about",
        "/advantages",
        "/conventional-risks",
        "/techniques",
        "/comparison",
        "/guidance",
        "/calculator",
        "/resources",
        "/faqs",
        "/contact",
        "/videos",
        "/search",
        "/admin/login",
    ]
    for page in pages:
        res = client.get(page)
        assert res.status_code == 200, f"Page {page} returned status {res.status_code}"
        assert "text/html" in res.headers.get("content-type", "")
        assert "GreenGrow" in res.text
