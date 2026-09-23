from pydantic import BaseModel, Field


class InvestigationRequest(BaseModel):
    host: str = Field(min_length=1)
    checks: list[str] = Field(default_factory=list)


class InvestigationResponse(BaseModel):
    host: str
    platform: str
    evidence_records: int
    findings: list[dict]