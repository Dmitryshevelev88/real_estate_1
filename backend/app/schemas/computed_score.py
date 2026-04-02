from datetime import datetime
from pydantic import BaseModel


class ComputedScoreOut(BaseModel):
    id: int
    assessment_id: int
    total_score: float
    calculation_version: str
    details_json: dict
    computed_at: datetime

    class Config:
        from_attributes = True
