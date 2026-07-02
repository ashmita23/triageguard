from app.schemas.review import ReviewRequest


POLICY_RULES = {
    "KYC-01": {
        "title": "Acceptable name variations",
        "content": "Minor name variations such as middle-name inclusion or punctuation differences are acceptable when the account identifier and date of birth match.",
    },
    "KYC-02": {
        "title": "Date-of-birth mismatches",
        "content": "Any date-of-birth mismatch requires escalation and human review.",
    },
    "KYC-03": {
        "title": "Address verification and required documents",
        "content": "Address mismatches or account identifier mismatches require additional verification or rejection.",
    },
}


def retrieve_policy(case: ReviewRequest, classification: str) -> list[dict]:
    if classification == "identity_mismatch":
        if case.customer_profile.date_of_birth != case.source_record.get("date_of_birth", ""):
            return [{"policy_id": "KYC-02", **POLICY_RULES["KYC-02"]}]

        if case.customer_profile.full_name != case.source_record.get("name", ""):
            return [{"policy_id": "KYC-01", **POLICY_RULES["KYC-01"]}]

        return [{"policy_id": "KYC-01", **POLICY_RULES["KYC-01"]}]

    if classification == "address_mismatch":
        return [{"policy_id": "KYC-03", **POLICY_RULES["KYC-03"]}]

    return [{"policy_id": "KYC-01", **POLICY_RULES["KYC-01"]}]
