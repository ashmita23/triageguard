from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_ui_homepage_loads():
    response = client.get("/")
    assert response.status_code == 200
    assert "TriageGuard Review UI" in response.text


def test_sample_cases_endpoint_returns_list():
    response = client.get("/sample-cases")
    assert response.status_code == 200
    sample_cases = response.json()
    assert isinstance(sample_cases, list)
    assert any(case["case_id"] == "CASE-001" for case in sample_cases)
    assert any("customer_profile" in case for case in sample_cases)


def test_review_endpoint_with_sample_case():
    response = client.get("/sample-cases")
    assert response.status_code == 200
    sample_cases = response.json()
    if not sample_cases:
        raise AssertionError("No sample cases were returned")

    request_payload = sample_cases[0]
    review_response = client.post("/review", json=request_payload)
    assert review_response.status_code == 200
    payload = review_response.json()
    assert payload["case_id"] == request_payload["case_id"]
    assert payload["policy_evidence"]
    assert payload["structured_output"]["case_id"] == request_payload["case_id"]
