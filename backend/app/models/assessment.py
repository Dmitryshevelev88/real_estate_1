import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class AssessmentStatus(str, enum.Enum):
    draft = "draft"
    submitted = "submitted"


class Assessment(Base):
    __tablename__ = "assessments"

    id: Mapped[int] = mapped_column(primary_key=True)
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"))
    assessor_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    score_profile_id: Mapped[int] = mapped_column(ForeignKey("score_profiles.id"))
    infrastructure: Mapped[float] = mapped_column(Float)
    lighting: Mapped[float] = mapped_column(Float)
    noise: Mapped[float] = mapped_column(Float)
    insolation: Mapped[float] = mapped_column(Float)
    development: Mapped[float] = mapped_column(Float)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[AssessmentStatus] = mapped_column(Enum(AssessmentStatus), default=AssessmentStatus.draft)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    property = relationship("Property", back_populates="assessments")
    assessor = relationship("User", back_populates="assessments")
    score_profile = relationship("ScoreProfile", back_populates="assessments")
    computed_score = relationship("ComputedScore", back_populates="assessment", uselist=False)
    attachments = relationship("Attachment", back_populates="assessment")
