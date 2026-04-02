from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class ComputedScore(Base):
    __tablename__ = "computed_scores"

    id: Mapped[int] = mapped_column(primary_key=True)
    assessment_id: Mapped[int] = mapped_column(ForeignKey("assessments.id"), unique=True)
    total_score: Mapped[float] = mapped_column(Float)
    calculation_version: Mapped[str] = mapped_column(String(50), default="v1")
    details_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    computed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    assessment = relationship("Assessment", back_populates="computed_score")
