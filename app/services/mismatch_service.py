from app.schemas.review import ReviewRequest


def detect_mismatches(case: ReviewRequest) -> dict:
    mismatches = {
        "name": case.customer_profile.full_name != case.source_record.get("name", ""),
        "date_of_birth": case.customer_profile.date_of_birth != case.source_record.get("date_of_birth", ""),
        "address": case.customer_profile.address != case.source_record.get("address", ""),
        "account_last_four": case.customer_profile.account_last_four != case.source_record.get("account_last_four", ""),
    }
    mismatches["major_count"] = sum(value for key, value in mismatches.items() if key != "major_count")
    return mismatches
