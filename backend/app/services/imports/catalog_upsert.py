from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.catalog_property import CatalogProperty
from app.schemas.imports import CsvImportRow


def upsert_catalog_property(
    db: Session,
    row: CsvImportRow,
) -> tuple[CatalogProperty, str]:
    item = db.scalar(
        select(CatalogProperty).where(CatalogProperty.external_id == row.external_id)
    )

    if item is None:
        item = CatalogProperty(
            external_id=row.external_id,
            display_name=row.display_name,
            address_full=row.address_full,
            project_name=row.project_name,
            city=row.city,
            street=row.street,
            house=row.house,
            building=row.building,
            property_type=row.property_type,
            status=row.status,
            latitude=row.latitude,
            longitude=row.longitude,
            is_active=True,
        )
        db.add(item)
        db.flush()
        return item, "created"

    item.display_name = row.display_name
    item.address_full = row.address_full
    item.project_name = row.project_name
    item.city = row.city
    item.street = row.street
    item.house = row.house
    item.building = row.building
    item.property_type = row.property_type
    item.status = row.status
    item.latitude = row.latitude
    item.longitude = row.longitude
    item.is_active = True

    db.flush()
    return item, "updated"