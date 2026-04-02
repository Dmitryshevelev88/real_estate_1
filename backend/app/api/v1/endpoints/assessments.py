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
from app.services.scoring import calculate_score

router = APIRouter()


@router.get("/", response_model=list[AssessmentOut])
def list_assessments(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list(db.scalars(select(Assessment).where(Assessment.assessor_id == current_user.id).order_by(Assessment.id.desc())).all())


@router.post("/", response_model=AssessmentOut)
def create_assessment(payload: AssessmentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    property_item = db.get(Property, payload.property_id)
    if not property_item:
        raise HTTPException(status_code=404, detail="Property not found")

    profile = db.get(ScoreProfile, payload.score_profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Score profile not found")

    item = Assessment(**payload.model_dump(), assessor_id=current_user.id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.post("/{assessment_id}/recompute", response_model=ComputedScoreOut)
def recompute_score(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assessment = db.scalar(
        select(Assessment).where(Assessment.id == assessment_id)
    )
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    property_obj = db.scalar(
        select(Property).where(Property.id == assessment.property_id)
    )
    if not property_obj or property_obj.created_by_id != current_user.id:
        raise HTTPException(status_code=404, detail="Assessment not found")

    profile = db.scalar(
        select(ScoreProfile).where(ScoreProfile.id == assessment.score_profile_id)
    )
    if not profile:
        raise HTTPException(status_code=400, detail="Score profile not found")

    total_score, details = calculate_score(assessment, profile)

    existing = db.scalar(
        select(ComputedScore).where(ComputedScore.assessment_id == assessment.id)
    )

    if existing:
        existing.total_score = total_score
        existing.details_json = details
        existing.calculation_version = profile.name
        db.commit()
        db.refresh(existing)
        return existing

    computed = ComputedScore(
        assessment_id=assessment.id,
        total_score=total_score,
        details_json=details,
        calculation_version=profile.name,
    )
    db.add(computed)
    db.commit()
    db.refresh(computed)
    return computed