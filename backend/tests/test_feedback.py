def test_feedback_submission_and_status_flow(client, admin_headers):
    """Verifies public feedback submission and admin status management."""
    submission_payload = {
        "name": "Test Farmer",
        "email": "farmer@example.com",
        "phone": "+91 99999 88888",
        "subject": "Inquiry on Sunnhemp seed availability in Tholukodu",
        "message": "Where can we acquire certified Sunnhemp seeds for pre-monsoon green manuring?",
    }

    # 1. Public Submit (POST)
    post_resp = client.post("/api/v1/feedback", json=submission_payload)
    assert post_resp.status_code == 201
    fb_data = post_resp.json()
    fb_id = fb_data["id"]
    assert fb_data["status"] == "New"

    # 2. Admin List (GET)
    admin_list = client.get("/api/v1/feedback?status=New", headers=admin_headers)
    assert admin_list.status_code == 200
    ids = [item["id"] for item in admin_list.json()]
    assert fb_id in ids

    # 3. Admin Update Status to Reviewed (PUT)
    put_resp = client.put(
        f"/api/v1/feedback/{fb_id}",
        json={"status": "Reviewed", "admin_notes": "Connected farmer with regional KVK seed coordinator."},
        headers=admin_headers,
    )
    assert put_resp.status_code == 200
    assert put_resp.json()["status"] == "Reviewed"
    assert "Connected farmer" in put_resp.json()["admin_notes"]

    # 4. Admin Update Status to Resolved (PUT)
    res_resp = client.put(
        f"/api/v1/feedback/{fb_id}",
        json={"status": "Resolved"},
        headers=admin_headers,
    )
    assert res_resp.status_code == 200
    assert res_resp.json()["status"] == "Resolved"

    # 5. Clean up
    del_resp = client.delete(f"/api/v1/feedback/{fb_id}", headers=admin_headers)
    assert del_resp.status_code == 204
