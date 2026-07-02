from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class DocumentReference(BaseModel):
    document_id: str = Field(..., description="Identifier for the referenced document.")
    document_type: str = Field(..., description="Type of document, e.g. ID, address proof.")
    source: str = Field(..., description="Source system or uploader for the document.")
    status: Optional[str] = Field(None, description="Current verification status of the document.")


class CustomerProfile(BaseModel):
    customer_id: Optional[str] = Field(None, description="Unique customer identifier.")
    full_name: str = Field(..., description="Customer full name.")
    date_of_birth: str = Field(..., description="Customer date of birth in ISO format.")
    address: str = Field(..., description="Customer address from the case record.")
    account_last_four: str = Field(..., min_length=4, max_length=4, description="Last four digits of the account.")


class ReviewRequest(BaseModel):
    case_id: str = Field(..., description="Unique identifier for the exception case.")
    exception_type: str = Field(..., description="Type of exception being reviewed.")
    case_priority: str = Field("medium", description="Case priority such as low, medium, or high.")
    source_system: str = Field(..., description="Originating system for the case.")
    submitted_at: Optional[datetime] = Field(None, description="Timestamp when the case was submitted.")
    customer_profile: CustomerProfile
    source_record: dict[str, str] = Field(..., description="Source record values used for comparison.")
    documents: List[DocumentReference] = Field(default_factory=list, description="List of related document references.")
    notes: Optional[str] = Field(None, description="Optional analyst notes.")


class ReviewResponse(BaseModel):
    case_id: str
    decision: str
    risk_level: str
    confidence: float
    explanation: str
    required_action: str
    policy_citation: str
    human_review_required: bool
    policy_evidence: list[dict] = Field(default_factory=list)
    structured_output: dict = Field(default_factory=dict)
    case_metadata: dict = Field(default_factory=dict)
