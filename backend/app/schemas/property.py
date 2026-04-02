from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PropertyCreate(BaseModel):
    title: str
    address: str
    description: str | None = None
    city: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    property_type: str | None = None


class PropertyOut(PropertyCreate):
    id: int
    created_by_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PropertyUpdate(BaseModel):
    title: str | None = None
    address: str | None = None
    description: str | None = None
    city: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    property_type: str | None = None