from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.models.catalog_property import CatalogProperty
from app.schemas.imports import CatalogImportRow


def find_existing_catalog_property(
    db: Session,
    row: CatalogImportRow,
) -> CatalogProperty | None:
    if row.external_id:
        item = db.scalar(
            select(CatalogProperty).where(
                CatalogProperty.external_id == row.external_id
            )
        )
        if item:
            return item

    if row.display_name and row.address_full:
        return db.scalar(
            select(CatalogProperty).where(
                and_(
                    CatalogProperty.display_name == row.display_name,
                    CatalogProperty.address_full == row.address_full,
                )
            )
        )

    return None


def upsert_catalog_property(
    db: Session,
    row: CatalogImportRow,
) -> tuple[CatalogProperty, bool]:
    item = find_existing_catalog_property(db, row)
    created = False

    if not item:
        item = CatalogProperty()
        created = True

    item.external_id = row.external_id
    item.display_name = row.display_name
    item.address_full = row.address_full
    item.project_name = row.project_name
    item.city = row.city
    item.property_type = row.property_type
    item.is_active = True

    db.add(item)
    db.flush()

    return item, created