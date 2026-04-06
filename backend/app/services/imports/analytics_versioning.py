from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models.property_analytics import PropertyAnalytics
from app.schemas.imports import CsvImportRow


def _same_metrics(analytics: PropertyAnalytics, row: CsvImportRow) -> bool:
    return (
        analytics.infrastructure == row.infrastructure
        and analytics.lighting == row.lighting
        and analytics.noise == row.noise
        and analytics.insolation == row.insolation
        and analytics.development == row.development
    )


def publish_from_import(
    db: Session,
    *,
    catalog_property_id: int,
    row: CsvImportRow,
    source_label: str,
) -> tuple[PropertyAnalytics, str]:
    latest = db.scalar(
        select(PropertyAnalytics)
        .where(PropertyAnalytics.catalog_property_id == catalog_property_id)
        .order_by(PropertyAnalytics.version.desc(), PropertyAnalytics.id.desc())
    )

    if latest and latest.is_published and _same_metrics(latest, row):
        latest.source_type = "csv"
        latest.source_label = source_label
        db.flush()
        return latest, "unchanged"

    next_version = 1 if latest is None else latest.version + 1

    db.execute(
        update(PropertyAnalytics)
        .where(
            PropertyAnalytics.catalog_property_id == catalog_property_id,
            PropertyAnalytics.is_published.is_(True),
        )
        .values(is_published=False)
    )

    analytics = PropertyAnalytics(
        catalog_property_id=catalog_property_id,
        infrastructure=row.infrastructure,
        lighting=row.lighting,
        noise=row.noise,
        insolation=row.insolation,
        development=row.development,
        source_type="csv",
        source_label=source_label,
        version=next_version,
        is_published=True,
    )
    db.add(analytics)
    db.flush()
    return analytics, "created" if latest is None else "versioned"