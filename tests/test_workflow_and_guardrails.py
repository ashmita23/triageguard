from app.agents.graph import run_review_workflow
from app.schemas.review import ReviewRequest
from app.services.guardrails import apply_guardrails


def test_workflow_returns_policy_evidence_and_decision():
    case = ReviewRequest(
        case_id="CASE-003",
        exception_type="KYC identity mismatch",
        case_priority="low",
        source_system="customer_portal",
        customer_profile={
            "customer_id": "CUST-1003",
            "full_name": "Carol Lee",
            "date_of_birth": "1990-01-01",
            "address": "789 Pine Rd, Boston, MA",
            "account_last_four": "1111",
        },
        source_record={
            "name": "Carol Lee",
            "date_of_birth": "1990-01-01",
            "address": "789 Pine Rd, Boston, MA",
            "account_last_four": "1111",
        },
    )

    response = run_review_workflow(case)

    assert response.decision == "Auto-approve"
    assert response.policy_evidence
    assert response.policy_citation == "KYC-01"


def test_guardrails_escalate_high_risk_case():
    case = ReviewRequest(
        case_id="CASE-004",
        exception_type="KYC identity mismatch",
        case_priority="high",
        source_system="branch_system",
        customer_profile={
            "customer_id": "CUST-1004",
            "full_name": "Dan Green",
            "date_of_birth": "1988-04-05",
            "address": "101 River St, Austin, TX",
            "account_last_four": "2222",
        },
        source_record={
            "name": "Dan Green",
            "date_of_birth": "1988-04-06",
            "address": "101 River St, Austin, TX",
            "account_last_four": "2222",
        },
    )

    response = apply_guardrails(case)

    assert response.human_review_required is True
    assert response.decision == "Escalate"
