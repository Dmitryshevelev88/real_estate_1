from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class CsvImportRow(BaseModel):
    external_id: str
    display_name: str
    address_full: str | None = None
    project_name: str | None = None
    city: str | None = None
    street: str | None = None
    house: str | None = None
    building: str | None = None
    property_type: str | None = None
    status: str = "built"
    latitude: float | None = None
    longitude: float | None = None

    infrastructure: int
    lighting: int
    noise: int
    insolation: int
    development: int

    @field_validator("external_id", "display_name", mode="before")
    @classmethod
    def validate_required_text(cls, value):
        if value is None:
            raise ValueError("field is required")
        value = str(value).strip()
        if not value:
            raise ValueError("field must not be empty")
        return value

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
        value = int(value)
        if value < 0 or value > 10:
            raise ValueError("score must be between 0 and 10")
        return value


class ImportBatchOut(BaseModel):
    id: int
    filename: str
    source_type: str
    status: str
    rows_total: int
    rows_created: int
    rows_updated: int
    rows_failed: int
    created_at: datetime
    updated_at: datetime
    error_message: str | None = None

    model_config = ConfigDict(from_attributes=True)