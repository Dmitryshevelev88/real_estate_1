from datetime import datetime
from pydantic import BaseModel, Field


class AssessmentCreate(BaseModel):
    infrastructure: int = Field(ge=0, le=10)
    lighting: int = Field(ge=0, le=10)
    noise: int = Field(ge=0, le=10)
    insolation: int = Field(ge=0, le=10)
    development: int = Field(ge=0, le=10)
    notes: str | None = None


class AssessmentOut(BaseModel):
    id: int
    property_id: int
    assessor_id: int
    score_profile_id: int | None = None
    infrastructure: int
    lighting: int
    noise: int
    insolation: int
    development: int
    notes: str | None = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True