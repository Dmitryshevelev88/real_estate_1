from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.assessment import Assessment
from app.models.computed_score import ComputedScore
from app.models.property import Property
from app.models.score_profile import ScoreProfile
from app.models.user import User
from app.schemas.assessment import AssessmentCreate, AssessmentOut
from app.schemas.computed_score import ComputedScoreOut
from app.schemas.property import PropertyCreate, PropertyOut
from app.services.scoring import calculate_score

router = APIRouter()


@router.post("", response_model=PropertyOut)
def create_property(
    payload: PropertyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = Property(**payload.model_dump(), created_by_id=current_user.id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("", response_model=list[PropertyOut])
def list_properties(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items = db.scalars(
        select(Property)
        .where(Property.created_by_id == current_user.id)
        .order_by(Property.created_at.desc())
    ).all()
    return list(items)


@router.get("/{property_id}", response_model=PropertyOut)
def get_property(
    property_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = db.scalar(
        select(Property).where(
            Property.id == property_id,
            Property.created_by_id == current_user.id,
        )
    )
    if not item:
        raise HTTPException(status_code=404, detail="Property not found")
    return item


@router.post("/{property_id}/assessments", response_model=AssessmentOut)
def create_assessment_for_property(
    property_id: int,
    payload: AssessmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    property_obj = db.scalar(
        select(Property).where(
            Property.id == property_id,
            Property.created_by_id == current_user.id,
        )
    )
    if not property_obj:
        raise HTTPException(status_code=404, detail="Property not found")

    profile = db.scalar(select(ScoreProfile).order_by(ScoreProfile.id.asc()))
    if not profile:
        raise HTTPException(status_code=400, detail="No score profile found")

    assessment = Assessment(
        property_id=property_id,
        assessor_id=current_user.id,
        score_profile_id=profile.id,
        infrastructure=payload.infrastructure,
        lighting=payload.lighting,
        noise=payload.noise,
        insolation=payload.insolation,
        development=payload.development,
        notes=payload.notes,
        status="submitted",
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return assessment


@router.get("/{property_id}/assessments", response_model=list[AssessmentOut])
def get_property_assessments(
    property_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    property_obj = db.scalar(
        select(Property).where(
            Property.id == property_id,
            Property.created_by_id == current_user.id,
        )
    )
    if not property_obj:
        raise HTTPException(status_code=404, detail="Property not found")

    items = db.scalars(
        select(Assessment)
        .where(Assessment.property_id == property_id)
        .order_by(Assessment.created_at.desc())
    ).all()
    return list(items)


@router.post("/{property_id}/compute-score", response_model=ComputedScoreOut)
def compute_score_for_property(
    property_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    property_obj = db.scalar(
        select(Property).where(
            Property.id == property_id,
            Property.created_by_id == current_user.id,
        )
    )
    if not property_obj:
        raise HTTPException(status_code=404, detail="Property not found")

    latest_assessment = db.scalar(
        select(Assessment)
        .where(Assessment.property_id == property_id)
        .order_by(Assessment.created_at.desc())
    )
    if not latest_assessment:
        raise HTTPException(status_code=400, detail="No assessments found for property")

    profile = db.scalar(select(ScoreProfile).order_by(ScoreProfile.id.asc()))
    if not profile:
        raise HTTPException(status_code=400, detail="No score profile found")

    total_score, details = calculate_score(latest_assessment, profile)

    existing = db.scalar(
        select(ComputedScore).where(ComputedScore.assessment_id == latest_assessment.id)
    )

    if existing:
        existing.total_score = total_score
        existing.details_json = details
        existing.calculation_version = profile.name
        db.commit()
        db.refresh(existing)
        return existing

    computed = ComputedScore(
        assessment_id=latest_assessment.id,
        total_score=total_score,
        details_json=details,
        calculation_version=profile.name,
    )
    db.add(computed)
    db.commit()
    db.refresh(computed)
    return computed


@router.get("/{property_id}/computed-scores", response_model=list[ComputedScoreOut])
def get_property_computed_scores(
    property_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    property_obj = db.scalar(
        select(Property).where(
            Property.id == property_id,
            Property.created_by_id == current_user.id,
        )
    )
    if not property_obj:
        raise HTTPException(status_code=404, detail="Property not found")

    assessment_ids = db.scalars(
        select(Assessment.id).where(Assessment.property_id == property_id)
    ).all()

    if not assessment_ids:
        return []

    items = db.scalars(
        select(ComputedScore)
        .where(ComputedScore.assessment_id.in_(assessment_ids))
        .order_by(ComputedScore.computed_at.desc())
    ).all()
    return list(items)