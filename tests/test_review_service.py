from app.schemas.review import ReviewRequest
from app.services.review_service import build_review_response


def test_auto_approve_for_matching_case():
    case = ReviewRequest(
        case_id="CASE-001",
        exception_type="KYC identity mismatch",
        case_priority="medium",
        source_system="core_banking",
        customer_profile={
            "customer_id": "CUST-1001",
            "full_name": "Alice Johnson",
            "date_of_birth": "1983-06-10",
            "address": "123 Main St, Springfield, IL",
            "account_last_four": "4321",
        },
        source_record={
            "name": "Alice Johnson",
            "date_of_birth": "1983-06-10",
            "address": "123 Main St, Springfield, IL",
            "account_last_four": "4321",
        },
    )

    response = build_review_response(case)

    assert response.decision == "Auto-approve"
    assert response.human_review_required is False
    assert response.policy_citation == "KYC-01"
    assert response.policy_evidence[0]["policy_id"] == "KYC-01"


def test_escalate_for_date_of_birth_mismatch():
    case = ReviewRequest(
        case_id="CASE-002",
        exception_type="KYC identity mismatch",
        case_priority="high",
        source_system="mobile_app",
        customer_profile={
            "customer_id": "CUST-1002",
            "full_name": "Bob Smith",
            "date_of_birth": "1979-02-14",
            "address": "456 Oak Ave, Metropolis, NY",
            "account_last_four": "9876",
        },
        source_record={
            "name": "Bob Smith",
            "date_of_birth": "1980-02-14",
            "address": "456 Oak Ave, Metropolis, NY",
            "account_last_four": "9876",
        },
    )

    response = build_review_response(case)

    assert response.decision == "Escalate"
    assert response.human_review_required is True
