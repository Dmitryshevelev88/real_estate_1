from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class PropertyAnalytics(Base):
    __tablename__ = "property_analytics"

    id: Mapped[int] = mapped_column(primary_key=True)
    catalog_property_id: Mapped[int] = mapped_column(
        ForeignKey("catalog_properties.id"), index=True
    )

    infrastructure: Mapped[int] = mapped_column(Integer)
    lighting: Mapped[int] = mapped_column(Integer)
    noise: Mapped[int] = mapped_column(Integer)
    insolation: Mapped[int] = mapped_column(Integer)
    development: Mapped[int] = mapped_column(Integer)

    source_type: Mapped[str] = mapped_column(String(50), default="csv")
    source_label: Mapped[str | None] = mapped_column(String(255), nullable=True)
    version: Mapped[int] = mapped_column(Integer, default=1)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    catalog_property = relationship("CatalogProperty", back_populates="analytics")