"""Schemas describing the contract analysis response payload."""

from pydantic import BaseModel, Field


class AnalysisResponse(BaseModel):
    """Structured response returned to the frontend."""

    risk_score: float = Field(..., ge=0, le=10)
    red_flags: list[str]
    summary: str
    raw_model_output: dict[str, object] | None = None
