from enum import Enum
from typing import Callable

from app.schemas.review import ReviewRequest, ReviewResponse
from app.services.review_service import build_review_response


class GuardrailType(str, Enum):
    DATE_OF_BIRTH = "date_of_birth_mismatch"
    ACCOUNT = "account_mismatch"
    ADDRESS = "address_mismatch"
    MULTIPLE_MAJOR = "multiple_major_mismatches"


def dob_guardrail(case: ReviewRequest) -> bool:
    return case.customer_profile.date_of_birth != case.source_record.get("date_of_birth", "")


def account_guardrail(case: ReviewRequest) -> bool:
    return case.customer_profile.account_last_four != case.source_record.get("account_last_four", "")


def address_guardrail(case: ReviewRequest) -> bool:
    same_name = case.customer_profile.full_name == case.source_record.get("name", "")
    same_dob = case.customer_profile.date_of_birth == case.source_record.get("date_of_birth", "")
    same_account = case.customer_profile.account_last_four == case.source_record.get("account_last_four", "")
    return not (same_name and same_dob and same_account) and case.customer_profile.address != case.source_record.get("address", "")


def multiple_major_guardrail(case: ReviewRequest) -> bool:
    mismatches = [
        dob_guardrail(case),
        account_guardrail(case),
        case.customer_profile.address != case.source_record.get("address", ""),
    ]
    return sum(bool(value) for value in mismatches) >= 2


GUARDRAILS: list[tuple[GuardrailType, Callable[[ReviewRequest], bool]]] = [
    (GuardrailType.DATE_OF_BIRTH, dob_guardrail),
    (GuardrailType.ACCOUNT, account_guardrail),
    (GuardrailType.ADDRESS, address_guardrail),
    (GuardrailType.MULTIPLE_MAJOR, multiple_major_guardrail),
]


def apply_guardrails(case: ReviewRequest, response: ReviewResponse | None = None) -> ReviewResponse:
    if response is None:
        response = build_review_response(case)

    fired: list[str] = []
    for guardrail_type, guardrail_fn in GUARDRAILS:
        if guardrail_fn(case):
            fired.append(guardrail_type.value)

    if fired:
        return ReviewResponse(
            case_id=response.case_id,
            decision="Escalate",
            risk_level="High",
            confidence=0.96,
            explanation="Guardrail triggered: high-risk mismatch requires human review.",
            required_action="Escalate for human review.",
            policy_citation=response.policy_citation,
            human_review_required=True,
            policy_evidence=response.policy_evidence,
            structured_output=response.structured_output,
            case_metadata={**response.case_metadata, "guardrails_fired": fired},
        )

    return response
