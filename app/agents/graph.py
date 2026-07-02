from app.schemas.review import ReviewRequest, ReviewResponse
from app.agents.nodes import (
    classify_node,
    compare_node,
    create_response_node,
    decide_node,
    retrieve_policy_node,
)
from app.services.guardrails import apply_guardrails


def run_review_workflow(case: ReviewRequest) -> ReviewResponse:
    classification = classify_node(case)
    mismatches = compare_node(case)
    policy_evidence = retrieve_policy_node(case, classification)
    decision_data = decide_node(case, policy_evidence, mismatches)
    response = create_response_node(case, decision_data, policy_evidence)
    return apply_guardrails(case, response)
