from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CatalogPropertySearchOut(BaseModel):
    id: int
    display_name: str
    address_full: str | None = None
    project_name: str | None = None
    city: str | None = None
    property_type: str | None = None
    status: str

    model_config = ConfigDict(from_attributes=True)


class CatalogPropertyOut(BaseModel):
    id: int
    external_id: str | None = None
    display_name: str
    address_full: str | None = None
    project_name: str | None = None
    city: str | None = None
    street: str | None = None
    house: str | None = None
    building: str | None = None
    property_type: str | None = None
    status: str
    latitude: float | None = None
    longitude: float | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)