from app.schemas.review import ReviewRequest


def classify_exception(case: ReviewRequest) -> str:
    exception_type = case.exception_type.lower()
    if "identity mismatch" in exception_type:
        return "identity_mismatch"
    if "address" in exception_type:
        return "address_mismatch"
    return "general_exception"
