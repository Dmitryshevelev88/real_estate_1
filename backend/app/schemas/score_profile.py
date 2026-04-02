from pydantic import BaseModel


class ScoreProfileOut(BaseModel):
    id: int
    name: str
    infrastructure_weight: float
    lighting_weight: float
    noise_weight: float
    insolation_weight: float
    development_weight: float

    class Config:
        from_attributes = True
