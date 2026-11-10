import uuid


def test_articles_crud(client, admin_headers):
    """Verifies creating, retrieving, updating, and deleting an article in Oracle Database."""
    unique_slug = f"test-article-{uuid.uuid4().hex[:8]}"
    create_payload = {
        "title": "Automated Test Article",
        "slug": unique_slug,
        "summary": "This is a test summary for automated testing.",
        "content": "Full content of the automated test article about soil microbiology.",
        "author": "QA Engineer",
        "is_published": True,
        "is_featured": False,
    }

    # 1. Create Article (POST)
    create_resp = client.post("/api/v1/articles", json=create_payload, headers=admin_headers)
    assert create_resp.status_code == 201
    created_data = create_resp.json()
    article_id = created_data["id"]
    assert created_data["slug"] == unique_slug

    # 2. Retrieve Article (GET)
    get_resp = client.get(f"/api/v1/articles/{unique_slug}")
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == article_id
    assert get_resp.json()["view_count"] >= 1

    # 3. Update Article (PUT)
    update_payload = {"title": "Updated Test Article Title"}
    put_resp = client.put(f"/api/v1/articles/{article_id}", json=update_payload, headers=admin_headers)
    assert put_resp.status_code == 200
    assert put_resp.json()["title"] == "Updated Test Article Title"

    # 4. Delete Article (DELETE)
    del_resp = client.delete(f"/api/v1/articles/{article_id}", headers=admin_headers)
    assert del_resp.status_code == 204

    # 5. Verify Deletion
    verify_resp = client.get(f"/api/v1/articles/{unique_slug}")
    assert verify_resp.status_code == 404
