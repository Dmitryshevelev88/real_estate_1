from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.property_analytics import PropertyAnalytics
from app.schemas.imports import CatalogImportRow


def unpublish_previous_analytics(db: Session, catalog_property_id: int) -> None:
    items = db.scalars(
        select(PropertyAnalytics).where(
            PropertyAnalytics.catalog_property_id == catalog_property_id,
            PropertyAnalytics.is_published.is_(True),
        )
    ).all()

    for item in items:
        item.is_published = False
        db.add(item)


def get_next_analytics_version(db: Session, catalog_property_id: int) -> int:
    current_max = db.scalar(
        select(func.max(PropertyAnalytics.version)).where(
            PropertyAnalytics.catalog_property_id == catalog_property_id
        )
    )
    return (current_max or 0) + 1


def create_analytics_version(
    db: Session,
    catalog_property_id: int,
    row: CatalogImportRow,
    default_source_label: str | None = None,
) -> PropertyAnalytics:
    unpublish_previous_analytics(db, catalog_property_id)

    analytics = PropertyAnalytics(
        catalog_property_id=catalog_property_id,
        infrastructure=row.infrastructure,
        lighting=row.lighting,
        noise=row.noise,
        insolation=row.insolation,
        development=row.development,
        source_type="csv",
        source_label=row.source_label or default_source_label,
        version=get_next_analytics_version(db, catalog_property_id),
        is_published=True,
    )

    db.add(analytics)
    db.flush()
    return analytics