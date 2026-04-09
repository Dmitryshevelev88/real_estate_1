from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CatalogImportRow(BaseModel):
    external_id: str | None = None
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

    version: int | None = None
    source_label: str | None = None

    @field_validator(
        "external_id",
        "address_full",
        "project_name",
        "city",
        "street",
        "house",
        "building",
        "property_type",
        "source_label",
        mode="before",
    )
    @classmethod
    def normalize_optional_text(cls, value):
        if value is None:
            return None
        value = str(value).strip()
        return value or None

    @field_validator("display_name", mode="before")
    @classmethod
    def validate_display_name(cls, value):
        if value is None:
            raise ValueError("display_name is required")
        value = str(value).strip()
        if not value:
            raise ValueError("display_name must not be empty")
        return value

    @field_validator("status", mode="before")
    @classmethod
    def normalize_status(cls, value):
        if value is None:
            return "built"
        value = str(value).strip()
        return value or "built"

    @field_validator("latitude", "longitude", mode="before")
    @classmethod
    def normalize_coordinates(cls, value):
        if value in (None, ""):
            return None
        return float(value)

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

    @field_validator("version", mode="before")
    @classmethod
    def validate_version(cls, value):
        if value in (None, ""):
            return None
        value = int(value)
        if value < 1:
            raise ValueError("version must be >= 1")
        return value


CsvImportRow = CatalogImportRow


class ImportRowError(BaseModel):
    row_number: int
    row_data: dict[str, Any]
    error: str


class CatalogCsvImportResult(BaseModel):
    batch_id: int
    status: str
    rows_total: int
    rows_created: int
    rows_updated: int
    rows_failed: int
    errors: list[ImportRowError] = Field(default_factory=list)


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