from app.schemas.review import ReviewRequest


def explain_decision(case: ReviewRequest, policy_id: str) -> str:
    if policy_id == "KYC-01":
        return "Name variations are allowed when date of birth and account identifiers match."
    if policy_id == "KYC-02":
        return "A date of birth mismatch is a high-risk signal that requires escalation."
    if policy_id == "KYC-03":
        return "Account mismatch or address issues need rejection or additional verification."
    return "This case should be reviewed using the applicable KYC policy."
