def test_faqs_crud(client, admin_headers):
    """Verifies creating, listing, updating, and deleting an FAQ in Oracle Database."""
    create_payload = {
        "category": "Composting",
        "question": "What is the optimum C:N ratio for rapid composting?",
        "answer": "The ideal carbon-to-nitrogen ratio is approximately 25:1 to 30:1 for rapid microbial breakdown.",
        "display_order": 99,
        "is_published": True,
    }

    # 1. Create (POST)
    resp = client.post("/api/v1/faqs", json=create_payload, headers=admin_headers)
    assert resp.status_code == 201
    faq_id = resp.json()["id"]

    # 2. List (GET)
    list_resp = client.get("/api/v1/faqs?category=Composting")
    assert list_resp.status_code == 200
    faq_ids = [f["id"] for f in list_resp.json()]
    assert faq_id in faq_ids

    # 3. Update (PUT)
    put_resp = client.put(f"/api/v1/faqs/{faq_id}", json={"display_order": 10}, headers=admin_headers)
    assert put_resp.status_code == 200
    assert put_resp.json()["display_order"] == 10

    # 4. Delete (DELETE)
    del_resp = client.delete(f"/api/v1/faqs/{faq_id}", headers=admin_headers)
    assert del_resp.status_code == 204
