SAMPLE_CASES = [
    {
        "case_id": "CASE-001",
        "exception_type": "KYC identity mismatch",
        "case_priority": "medium",
        "source_system": "core_banking",
        "submitted_at": "2026-07-02T09:12:00Z",
        "customer_profile": {
            "customer_id": "CUST-1001",
            "full_name": "Alice Johnson",
            "date_of_birth": "1983-06-10",
            "address": "123 Main St, Springfield, IL",
            "account_last_four": "4321",
        },
        "source_record": {
            "name": "Alice Johnson",
            "date_of_birth": "1983-06-10",
            "address": "123 Main Street, Springfield, IL",
            "account_last_four": "4321",
        },
        "documents": [
            {
                "document_id": "DOC-9001",
                "document_type": "ID Proof",
                "source": "document_upload",
                "status": "verified",
            },
            {
                "document_id": "DOC-9002",
                "document_type": "Address Proof",
                "source": "document_upload",
                "status": "pending",
            },
        ],
        "notes": "Minor address format difference.",
    },
    {
        "case_id": "CASE-002",
        "exception_type": "KYC identity mismatch",
        "case_priority": "high",
        "source_system": "mobile_app",
        "submitted_at": "2026-07-02T10:20:00Z",
        "customer_profile": {
            "customer_id": "CUST-1002",
            "full_name": "Bob Smith",
            "date_of_birth": "1979-02-14",
            "address": "456 Oak Ave, Metropolis, NY",
            "account_last_four": "9876",
        },
        "source_record": {
            "name": "Robert Smith",
            "date_of_birth": "1979-02-14",
            "address": "456 Oak Avenue, Metropolis, NY",
            "account_last_four": "9876",
        },
        "documents": [
            {
                "document_id": "DOC-9003",
                "document_type": "Selfie",
                "source": "mobile_capture",
                "status": "review_pending",
            }
        ],
        "notes": "Name variation between records.",
    },
]
