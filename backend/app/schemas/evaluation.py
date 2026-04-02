from pydantic import BaseModel

from app.schemas.catalog_property import CatalogPropertyOut
from app.schemas.property_analytics import PropertyAnalyticsOut


class EvaluationBreakdown(BaseModel):
    infrastructure_score: float
    lighting_score: float
    noise_score: float
    insolation_score: float
    development_score: float


class PropertyEvaluationOut(BaseModel):
    property: CatalogPropertyOut
    analytics: PropertyAnalyticsOut
    score_profile_name: str
    total_score: float
    breakdown: EvaluationBreakdown