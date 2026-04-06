from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.catalog_property import CatalogProperty
from app.models.property_analytics import PropertyAnalytics
from app.models.score_profile import ScoreProfile
from app.schemas.catalog_property import CatalogPropertyOut, CatalogPropertySearchOut
from app.schemas.evaluation import PropertyEvaluationOut
from app.schemas.property_analytics import PropertyAnalyticsOut
from app.services.scoring import calculate_score_from_analytics

router = APIRouter()


def _get_active_catalog_property(db: Session, property_id: int) -> CatalogProperty:
    item = db.get(CatalogProperty, property_id)
    if not item or not item.is_active:
        raise HTTPException(status_code=404, detail="Property not found")
    return item


def _get_latest_published_analytics(
    db: Session, property_id: int
) -> PropertyAnalytics:
    analytics = db.scalar(
        select(PropertyAnalytics)
        .where(
            PropertyAnalytics.catalog_property_id == property_id,
            PropertyAnalytics.is_published.is_(True),
        )
        .order_by(
            PropertyAnalytics.version.desc(),
            PropertyAnalytics.id.desc(),
        )
    )
    if not analytics:
        raise HTTPException(status_code=404, detail="Analytics not found")
    return analytics


@router.get("/search", response_model=list[CatalogPropertySearchOut])
def search_catalog_properties(
    q: str = Query(..., min_length=2),
    db: Session = Depends(get_db),
):
    query = q.strip()
    if len(query) < 2:
        raise HTTPException(status_code=422, detail="Query is too short")

    stmt = (
        select(CatalogProperty)
        .join(
            PropertyAnalytics,
            PropertyAnalytics.catalog_property_id == CatalogProperty.id,
        )
        .where(
            CatalogProperty.is_active.is_(True),
            PropertyAnalytics.is_published.is_(True),
            or_(
                CatalogProperty.display_name.ilike(f"%{query}%"),
                CatalogProperty.address_full.ilike(f"%{query}%"),
                CatalogProperty.project_name.ilike(f"%{query}%"),
            ),
        )
        .distinct()
        .order_by(CatalogProperty.id.desc())
        .limit(10)
    )

    items = db.scalars(stmt).all()
    return list(items)


@router.get("/{property_id}", response_model=CatalogPropertyOut)
def get_catalog_property(
    property_id: int,
    db: Session = Depends(get_db),
):
    return _get_active_catalog_property(db, property_id)


@router.get("/{property_id}/analytics", response_model=PropertyAnalyticsOut)
def get_catalog_property_analytics(
    property_id: int,
    db: Session = Depends(get_db),
):
    _get_active_catalog_property(db, property_id)
    return _get_latest_published_analytics(db, property_id)


@router.get("/{property_id}/evaluation", response_model=PropertyEvaluationOut)
def get_catalog_property_evaluation(
    property_id: int,
    db: Session = Depends(get_db),
):
    item = _get_active_catalog_property(db, property_id)
    analytics = _get_latest_published_analytics(db, property_id)

    profile = db.scalar(select(ScoreProfile).order_by(ScoreProfile.id.asc()))
    if not profile:
        raise HTTPException(status_code=400, detail="Score profile not found")

    total_score, breakdown = calculate_score_from_analytics(analytics, profile)

    return {
        "property": item,
        "analytics": analytics,
        "score_profile_name": profile.name,
        "total_score": total_score,
        "breakdown": breakdown,
    }