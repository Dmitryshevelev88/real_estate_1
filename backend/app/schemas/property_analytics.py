from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class PropertyAnalyticsOut(BaseModel):
    id: int
    catalog_property_id: int
    infrastructure: int
    lighting: int
    noise: int
    insolation: int
    development: int
    source_type: str
    source_label: str | None = None
    version: int
    is_published: bool
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PropertyAnalyticsAdminUpdate(BaseModel):
    infrastructure: int | None = None
    lighting: int | None = None
    noise: int | None = None
    insolation: int | None = None
    development: int | None = None
    source_type: str | None = None
    source_label: str | None = None
    is_published: bool | None = None

    model_config = ConfigDict(extra="forbid")

    @field_validator(
        "infrastructure",
        "lighting",
        "noise",
        "insolation",
        "development",
        mode="before",
    )
    @classmethod
    def validate_score(cls, value):
        if value is None:
            return None
        value = int(value)
        if value < 0 or value > 10:
            raise ValueError("score must be between 0 and 10")
        return value