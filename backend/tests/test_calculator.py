def test_calculator_acres_and_tonnes(client):
    """Verifies calculation with Acres and tonnes/acre."""
    payload = {
        "cultivated_area": 2.5,
        "area_unit": "Acres",
        "application_rate": 4.0,
        "rate_unit": "tonnes/acre",
        "input_type_name": "Farmyard Manure",
    }
    response = client.post("/api/v1/calculator/estimate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["estimated_quantity"] == 10.0
    assert data["quantity_unit"] == "tonnes"
    assert "2.5 Acres" in data["formula"]
    assert "4.0 tonnes/acre" in data["formula"]
    assert "10.0 tonnes" in data["formula"]


def test_calculator_hectares_and_kg(client):
    """Verifies calculation with Hectares and kg/hectare."""
    payload = {
        "cultivated_area": 1.2,
        "area_unit": "Hectares",
        "application_rate": 50.0,
        "rate_unit": "kg/hectare",
        "input_type_name": "Biofertiliser Inoculant",
    }
    response = client.post("/api/v1/calculator/estimate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["estimated_quantity"] == 60.0
    assert data["quantity_unit"] == "kg"
    assert "60.00 kg" in data["explanation"]


def test_calculator_invalid_input(client):
    """Verifies validation when non-positive numbers are passed."""
    payload = {
        "cultivated_area": -1.0,
        "area_unit": "Acres",
        "application_rate": 0,
        "rate_unit": "kg/acre",
    }
    response = client.post("/api/v1/calculator/estimate", json=payload)
    assert response.status_code == 422
