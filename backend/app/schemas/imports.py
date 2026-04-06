from pydantic import BaseModel, Field, field_validator


class CatalogImportRow(BaseModel):
    external_id: str | None = None
    display_name: str
    address_full: str | None = None
    project_name: str | None = None
    city: str | None = None
    property_type: str | None = None

    infrastructure: int
    lighting: int
    noise: int
    insolation: int
    development: int

    version: int = 1
    source_label: str | None = None

    @field_validator(
        "infrastructure", "lighting", "noise", "insolation", "development"
    )
    @classmethod
    def validate_metric(cls, value: int) -> int:
        if value < 0 or value > 10:
            raise ValueError("Metric must be between 0 and 10")
        return value