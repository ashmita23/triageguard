from typing import TypedDict


class PolicyRule(TypedDict):
    title: str
    content: str
    category: str
    severity: str


POLICY_RULES: dict[str, PolicyRule] = {
    "KYC-01": {
        "title": "Acceptable name variations",
        "content": "Minor name variations such as middle-name inclusion or punctuation differences are acceptable when the account identifier and date of birth match.",
        "category": "identity",
        "severity": "low",
    },
    "KYC-02": {
        "title": "Date-of-birth mismatches",
        "content": "Any date-of-birth mismatch requires escalation and human review.",
        "category": "identity",
        "severity": "high",
    },
    "KYC-03": {
        "title": "Address verification and required documents",
        "content": "Address mismatches or account identifier mismatches require additional verification or rejection.",
        "category": "address",
        "severity": "medium",
    },
}
