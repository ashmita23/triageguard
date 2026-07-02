from pydantic import BaseModel, Field


class DecisionOutput(BaseModel):
    decision: str = Field(..., description="Final decision for the case.")
    risk_level: str = Field(..., description="Risk classification for the case.")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0 and 1.")
    explanation: str = Field(..., description="Human-readable explanation for the decision.")
    required_action: str = Field(..., description="Next recommended action.")
    policy_citation: str = Field(..., description="Policy identifier used for the decision.")
    human_review_required: bool = Field(..., description="Whether the case should be escalated for human review.")
