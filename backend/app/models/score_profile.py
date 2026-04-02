from datetime import datetime

from sqlalchemy import DateTime, Float, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class ScoreProfile(Base):
    __tablename__ = "score_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    infrastructure_weight: Mapped[float] = mapped_column(Float, default=0.2)
    lighting_weight: Mapped[float] = mapped_column(Float, default=0.2)
    noise_weight: Mapped[float] = mapped_column(Float, default=0.2)
    insolation_weight: Mapped[float] = mapped_column(Float, default=0.2)
    development_weight: Mapped[float] = mapped_column(Float, default=0.2)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    assessments = relationship("Assessment", back_populates="score_profile")
