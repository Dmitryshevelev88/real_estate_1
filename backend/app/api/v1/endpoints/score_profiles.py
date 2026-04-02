from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.score_profile import ScoreProfile
from app.models.user import User
from app.schemas.score_profile import ScoreProfileOut

router = APIRouter()


@router.get("/", response_model=list[ScoreProfileOut])
def list_score_profiles(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return list(db.scalars(select(ScoreProfile).order_by(ScoreProfile.id.asc())).all())
