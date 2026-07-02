from app.schemas.review import ReviewRequest


def determine_decision(case: ReviewRequest, policy_citation: str, mismatches: dict) -> dict:
    if case.customer_profile.date_of_birth != case.source_record.get("date_of_birth", ""):
        return {
            "decision": "Escalate",
            "risk_level": "High",
            "confidence": 0.95,
            "required_action": "Escalate for human review and verify the customer identity.",
            "human_review_required": True,
        }

    if case.customer_profile.account_last_four != case.source_record.get("account_last_four", ""):
        return {
            "decision": "Reject",
            "risk_level": "High",
            "confidence": 0.92,
            "required_action": "Reject the transaction and investigate the discrepancy.",
            "human_review_required": True,
        }

    if case.customer_profile.full_name != case.source_record.get("name", ""):
        return {
            "decision": "Request documents",
            "risk_level": "Medium",
            "confidence": 0.80,
            "required_action": "Request supporting identity documents.",
            "human_review_required": True,
        }

    if mismatches["major_count"] >= 2:
        return {
            "decision": "Escalate",
            "risk_level": "High",
            "confidence": 0.82,
            "required_action": "Escalate for human review due to multiple mismatches.",
            "human_review_required": True,
        }

    return {
        "decision": "Auto-approve",
        "risk_level": "Low",
        "confidence": 0.88,
        "required_action": "Approve the case and continue processing.",
        "human_review_required": False,
    }
