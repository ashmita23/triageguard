from typing import Optional

from pydantic import BaseModel, Field


class RecordDetails(BaseModel):
    full_name: str = Field(..., description="Name provided in the case or source record.")
    date_of_birth: str = Field(..., description="Date of birth in ISO format YYYY-MM-DD.")
    address: str = Field(..., description="Full address string for the customer.")
    account_last_four: str = Field(
        ..., min_length=4, max_length=4, description="Last four digits of the account.")


class ReviewCase(BaseModel):
    case_id: str = Field(..., description="Unique identifier for the exception case.")
    exception_type: str = Field(..., description="Type of exception being reviewed.")
    customer_record: RecordDetails
    source_record: RecordDetails
    notes: Optional[str] = Field(None, description="Optional notes provided by the analyst.")
