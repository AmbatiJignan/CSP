import uuid


def test_survey_crud_and_validation(client, admin_headers):
    """Verifies creating, validating, updating, and deleting farmer survey records in Oracle 23ai."""
    unique_code = f"TEST-TK-{uuid.uuid4().hex[:6].upper()}"

    survey_payload = {
        "respondent_code": unique_code,
        "village": "Tholukodu",
        "farming_experience_years": 15,
        "land_holding_acres": 4.5,
        "primary_crops": "Paddy, Groundnut",
        "farming_method": "Partially Organic",
        "organic_input_usage": "Farmyard Manure, Neem Cake",
        "awareness_level": "Moderate",
        "knowledge_of_advantages": "Reduces input expenditure and preserves soil moisture",
        "primary_challenges": "Initial labor requirement for weeding",
        "willingness_to_adopt": "Willing with Support",
        "support_needed": "Bio-fertiliser supply and training",
        "additional_comments": "Keen to shift remaining acreage if market prices hold.",
        "consent_confirmed": True,
        "survey_date": "2026-11-01",
        "surveyor_name": "Field Officer Kumar",
    }

    # 1. Create Survey (POST)
    create_resp = client.post("/api/v1/surveys", json=survey_payload, headers=admin_headers)
    assert create_resp.status_code == 201
    created_data = create_resp.json()
    survey_id = created_data["id"]
    assert created_data["respondent_code"] == unique_code
    assert created_data["village"] == "Tholukodu"

    # 2. Reject Duplicate Respondent Code (400)
    dup_resp = client.post("/api/v1/surveys", json=survey_payload, headers=admin_headers)
    assert dup_resp.status_code == 400
    assert "already exists" in dup_resp.json()["detail"]

    # 3. Retrieve Single Survey Record (GET)
    get_resp = client.get(f"/api/v1/surveys/{survey_id}", headers=admin_headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["respondent_code"] == unique_code

    # 4. Update Survey (PUT)
    update_payload = {"awareness_level": "High", "land_holding_acres": 5.0}
    put_resp = client.put(f"/api/v1/surveys/{survey_id}", json=update_payload, headers=admin_headers)
    assert put_resp.status_code == 200
    assert put_resp.json()["awareness_level"] == "High"
    assert put_resp.json()["land_holding_acres"] == 5.0

    # 5. Delete Survey (DELETE)
    del_resp = client.delete(f"/api/v1/surveys/{survey_id}", headers=admin_headers)
    assert del_resp.status_code == 204

    # 6. Verify Deletion
    get_again = client.get(f"/api/v1/surveys/{survey_id}", headers=admin_headers)
    assert get_again.status_code == 404
