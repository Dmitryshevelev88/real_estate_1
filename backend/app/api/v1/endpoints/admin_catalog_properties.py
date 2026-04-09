from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.catalog_property import CatalogProperty
from app.models.property_analytics import PropertyAnalytics
from app.schemas.catalog_property import (
    CatalogPropertyAdminUpdate,
    CatalogPropertyOut,
)
from app.schemas.property_analytics import (
    PropertyAnalyticsAdminUpdate,
    PropertyAnalyticsOut,
)

router = APIRouter(prefix="/admin", tags=["admin-catalog"])


@router.get("/catalog-properties", response_model=list[CatalogPropertyOut])
def admin_list_catalog_properties(
    q: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    stmt = select(CatalogProperty)

    if q:
        query = q.strip()
        stmt = stmt.where(
            or_(
                CatalogProperty.display_name.ilike(f"%{query}%"),
                CatalogProperty.address_full.ilike(f"%{query}%"),
                CatalogProperty.project_name.ilike(f"%{query}%"),
            )
        )

    stmt = stmt.order_by(CatalogProperty.id.desc()).limit(limit)
    items = db.scalars(stmt).all()
    return list(items)


@router.get("/catalog-properties/{property_id}", response_model=CatalogPropertyOut)
def admin_get_catalog_property(
    property_id: int,
    db: Session = Depends(get_db),
):
    item = db.get(CatalogProperty, property_id)
    if not item:
        raise HTTPException(status_code=404, detail="Catalog property not found")
    return item


@router.patch("/catalog-properties/{property_id}", response_model=CatalogPropertyOut)
def admin_patch_catalog_property(
    property_id: int,
    payload: CatalogPropertyAdminUpdate,
    db: Session = Depends(get_db),
):
    item = db.get(CatalogProperty, property_id)
    if not item:
        raise HTTPException(status_code=404, detail="Catalog property not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get(
    "/catalog-properties/{property_id}/analytics",
    response_model=list[PropertyAnalyticsOut],
)
def admin_get_catalog_property_analytics(
    property_id: int,
    db: Session = Depends(get_db),
):
    property_item = db.get(CatalogProperty, property_id)
    if not property_item:
        raise HTTPException(status_code=404, detail="Catalog property not found")

    items = db.scalars(
        select(PropertyAnalytics)
        .where(PropertyAnalytics.catalog_property_id == property_id)
        .order_by(PropertyAnalytics.version.desc(), PropertyAnalytics.id.desc())
    ).all()
    return list(items)


@router.patch("/property-analytics/{analytics_id}", response_model=PropertyAnalyticsOut)
def admin_patch_property_analytics(
    analytics_id: int,
    payload: PropertyAnalyticsAdminUpdate,
    db: Session = Depends(get_db),
):
    item = db.get(PropertyAnalytics, analytics_id)
    if not item:
        raise HTTPException(status_code=404, detail="Property analytics not found")

    data = payload.model_dump(exclude_unset=True)

    if data.get("is_published") is True:
        others = db.scalars(
            select(PropertyAnalytics).where(
                PropertyAnalytics.catalog_property_id == item.catalog_property_id,
                PropertyAnalytics.id != item.id,
                PropertyAnalytics.is_published.is_(True),
            )
        ).all()
        for other in others:
            other.is_published = False
            db.add(other)

    for field, value in data.items():
        setattr(item, field, value)

    db.add(item)
    db.commit()
    db.refresh(item)
    return item