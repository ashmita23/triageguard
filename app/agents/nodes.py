from app.schemas.review import ReviewRequest, ReviewResponse
from app.schemas.structured_output import StructuredDecisionOutput
from app.services.classification_service import classify_exception
from app.services.explanation_service import explain_decision
from app.services.mismatch_service import detect_mismatches
from app.services.policy_service import retrieve_policy
from app.services.rule_decision_service import determine_decision


def classify_node(case: ReviewRequest) -> str:
    return classify_exception(case)


def compare_node(case: ReviewRequest) -> dict:
    return detect_mismatches(case)


def retrieve_policy_node(case: ReviewRequest, classification: str) -> list[dict]:
    return retrieve_policy(case, classification)


def decide_node(case: ReviewRequest, policy_evidence: list[dict], mismatches: dict) -> dict:
    policy_id = policy_evidence[0]["policy_id"]
    decision_data = determine_decision(case, policy_id, mismatches)
    decision_data["explanation"] = explain_decision(case, policy_id)
    return decision_data


def create_response_node(case: ReviewRequest, decision_data: dict, policy_evidence: list[dict]) -> ReviewResponse:
    structured_output = StructuredDecisionOutput(
        case_id=case.case_id,
        summary={
            "decision": decision_data["decision"],
            "risk_level": decision_data["risk_level"],
            "confidence": decision_data["confidence"],
            "required_action": decision_data["required_action"],
            "human_review_required": decision_data["human_review_required"],
        },
        evidence=policy_evidence,
        explanation=decision_data["explanation"],
    ).model_dump()

    case_metadata = {
        "source_system": case.source_system,
        "case_priority": case.case_priority,
        "submitted_at": case.submitted_at.isoformat() if case.submitted_at else None,
        "document_count": len(case.documents),
    }

    return ReviewResponse(
        case_id=case.case_id,
        decision=decision_data["decision"],
        risk_level=decision_data["risk_level"],
        confidence=decision_data["confidence"],
        explanation=decision_data["explanation"],
        required_action=decision_data["required_action"],
        policy_citation=policy_evidence[0]["policy_id"],
        human_review_required=decision_data["human_review_required"],
        policy_evidence=policy_evidence,
        structured_output=structured_output,
        case_metadata=case_metadata,
    )
