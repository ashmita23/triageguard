from pydantic import BaseModel, Field


class DecisionSummary(BaseModel):
    decision: str = Field(..., description="Final decision for the case.")
    risk_level: str = Field(..., description="Risk level for the case.")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0 and 1.")
    required_action: str = Field(..., description="The next operation to take.")
    human_review_required: bool = Field(..., description="Whether the case requires human review.")


class EvidenceItem(BaseModel):
    policy_id: str = Field(..., description="Applicable policy identifier.")
    title: str = Field(..., description="Policy title.")
    content: str = Field(..., description="Policy text.")


class StructuredDecisionOutput(BaseModel):
    case_id: str = Field(..., description="Case identifier.")
    summary: DecisionSummary
    evidence: list[EvidenceItem] = Field(default_factory=list, description="Policies used as evidence.")
    explanation: str = Field(..., description="Human-readable explanation.")
