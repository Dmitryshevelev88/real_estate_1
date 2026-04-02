from datetime import datetime

from pydantic import BaseModel, ConfigDict


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